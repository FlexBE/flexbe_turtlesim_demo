#!/usr/bin/env python3

# Copyright 2026 Christopher Newport University
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Publish command velocity FlexBE state."""

from flexbe_core import EventState, Logger
from flexbe_core.proxy import ProxyPublisher

from geometry_msgs.msg import Twist

from rclpy.duration import Duration

# Based on flexible_navigation : flex_nav_flexbe_states: TimedTwistState
# but removes TwistStamped handling


class TimedCmdVelState(EventState):
    """
    This state publishes an open loop constant Twist command based on parameters.

    -- target_time          float     Time which needs to have passed since the behavior started.
    -- velocity             float     Body velocity (m/s)
    -- rotation_rate        float     Angular rotation (radians/s)
    -- cmd_topic            string    Topic name of the robot velocity command (default: 'cmd_vel')
    -- desired_rate         float     Desired state update rate (default: 50 Hz)
    <= done                 Given time has passed.
    """

    def __init__(self, target_time, velocity, rotation_rate, cmd_topic='cmd_vel', desired_rate=50):
        """
        Declare outcomes, input_keys, and output_keys by calling the super constructor with the corresponding arguments.

        NOTE: Uses desired update rate added to ROS 2 version of FlexBE flexbe_core.ros_state
         This state should run faster than default 10 Hz state update
         The outcomes must come last in kwargs list due to FlexBE UI parsing!
        """
        super().__init__(desired_rate=desired_rate, outcomes=['done'])

        # Store state parameter for later use.
        self._target_time = Duration(seconds=target_time)

        # The constructor is called when building the state machine, not when actually starting the behavior.
        # Thus, we cannot save the starting time now and will do so later.
        self._start_time = None
        self._pause_time = None
        self._paused_duration_ns = 0

        self._return = None  # Track the outcome so we can detect if transition is blocked

        self._twist = Twist()
        self._twist.linear.x = velocity
        self._twist.angular.z = rotation_rate
        self._stop_twist = Twist()
        self._cmd_topic = cmd_topic

        # FlexBE uses "proxies" for publishers, subscribers, and service callers
        # so that all states in a behavior can share a single subscription/publisher
        ProxyPublisher.initialize(TimedCmdVelState._node)  # the class must know the behavior node
        self._pub = ProxyPublisher()
        self._pub.create_publisher(cmd_topic, Twist)

    def execute(self, userdata):
        """
        Call this method periodically while the state is active.

        If no outcome is returned, the state will stay active.
        """
        if self._return is not None:
            # We have completed the state, and therefore must be blocked by autonomy level
            # Stop the robot and return the prior outcome
            self._publish_stop()
            return self._return

        now_ns = self._node.get_clock().now().nanoseconds
        elapsed_ns = now_ns - self._start_time.nanoseconds - self._paused_duration_ns
        if elapsed_ns > self._target_time.nanoseconds:
            # Normal completion, do not bother repeating the publish
            # We won't bother publishing a 0 command unless blocked (above)
            # so that we can chain multiple motions together
            self._return = 'done'
            Logger.localinfo(f"{self._name} : returning 'done'")  # For initial debugging
            return 'done'

        # Normal operation
        if self._cmd_topic:
            Logger.localinfo_throttle(0.5, f'{self._name} : {self._twist}')
            self._pub.publish(self._cmd_topic, self._twist)

        return None

    def on_enter(self, userdata):
        """
        Call this method when the state becomes active.

        i.e. a transition from another state to this one is taken.
        """
        self._start_time = self._node.get_clock().now()
        self._pause_time = None
        self._paused_duration_ns = 0
        self._return = None  # reset the completion flag

    def on_pause(self):
        """Stop motion while the behavior is paused with this state active."""
        self._pause_time = self._node.get_clock().now()
        self._publish_stop()

    def on_resume(self, userdata):
        """Exclude paused time from the active motion duration."""
        if self._pause_time is not None:
            self._paused_duration_ns += self._node.get_clock().now().nanoseconds - self._pause_time.nanoseconds
            self._pause_time = None

    def on_exit(self, userdata):
        """Stop motion if this state is interrupted before its normal completion."""
        if self._return is None:
            self._publish_stop()

    def on_stop(self):
        """Stop motion and remove publisher whenever the behavior stops or is preempted."""
        self._publish_stop()  # Note, this happens regardless of whether this state is active
        ProxyPublisher.remove_publisher(self._cmd_topic)

    def _publish_stop(self):
        """Publish a zero twist when we need to stop an in-flight open-loop command."""
        if self._cmd_topic:
            self._pub.publish(self._cmd_topic, self._stop_twist)
