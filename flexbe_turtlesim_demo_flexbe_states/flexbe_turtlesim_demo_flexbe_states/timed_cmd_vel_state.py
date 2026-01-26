#!/usr/bin/env python

# Copyright 2023 Christopher Newport University
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

from rclpy.duration import Duration
from flexbe_core import EventState, Logger
from flexbe_core.proxy import ProxyPublisher

from geometry_msgs.msg import Twist

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

        self._return = None  # Track the outcome so we can detect if transition is blocked

        self._twist = Twist()
        self._twist.linear.x = velocity
        self._twist.angular.z = rotation_rate
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
        if self._return:
            # We have completed the state, and therefore must be blocked by autonomy level
            # Stop the robot, but and return the prior outcome
            if self._cmd_topic:
                self._pub.publish(self._cmd_topic, Twist())

            return self._return

        if self._node.get_clock().now().nanoseconds - self._start_time.nanoseconds > self._target_time.nanoseconds:
            # Normal completion, do not bother repeating the publish
            # We won't bother publishing a 0 command unless blocked (above)
            # so that we can chain multiple motions together
            self._return = 'done'
            Logger.localinfo(f"{self._name} : returning 'done'")  # For initial debugging
            return 'done'

        # Normal operation
        if self._cmd_topic:
            Logger.localinfo(f"{self._name} : {self._twist}")  # For initial debugging
            self._pub.publish(self._cmd_topic, self._twist)

        return None

    def on_enter(self, userdata):
        """
        Call this method when the state becomes active.

        i.e. a transition from another state to this one is taken.
        """
        self._start_time = self._node.get_clock().now()
        self._return = None  # reset the completion flag
