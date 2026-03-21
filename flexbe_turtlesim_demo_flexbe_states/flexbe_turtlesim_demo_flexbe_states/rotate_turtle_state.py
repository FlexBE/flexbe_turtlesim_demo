#!/usr/bin/env python

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

"""Rotate turtle FlexBE state."""

import math

from action_msgs.msg import GoalStatus

from flexbe_core import EventState, Logger
from flexbe_core.proxy import ProxyActionClient

from rclpy.duration import Duration

# example import of required action
try:
    # Kilted and newer
    from turtlesim_msgs.action import RotateAbsolute
except ModuleNotFoundError:
    # Jazzy and older
    from turtlesim.action import RotateAbsolute


class RotateTurtleState(EventState):
    """
    Actionlib actions are the most common basis for state implementations.

    These are used to interface with longer running more computationally intensive calculations in a
    non-blocking manner.

    State implementations should be lightweight and non-blocking so that they execute() completes within the
    desired update period.

    The ROS 2 action library provides a non-blocking, high-level interface for robot capabilities.

    Elements defined here for UI
    Parameters
    -- timeout             Maximum time allowed (seconds)
    -- action_topic        Name of action to invoke

    Outputs
    <= rotation_complete   Only a few dishes have been cleaned.
    <= failed              Failed for some reason.
    <= canceled            User canceled before completion.
    <= timeout             The action has timed out.

    User data
    ># angle     float     Desired rotational angle in (degrees) (Input)
    #> duration  float     Amount time taken to complete rotation (seconds) (Output)

    """

    def __init__(self, timeout, action_topic='/turtle1/rotate_absolute'):
        """Configure the rotate action state and its timeout."""
        super().__init__(outcomes=['rotation_complete', 'failed', 'canceled', 'timeout'],
                         input_keys=['angle'],
                         output_keys=['duration'])

        self._timeout = Duration(seconds=timeout)
        self._timeout_sec = timeout
        self._topic = action_topic

        # Create the action client when building the behavior.
        # Using the proxy client provides asynchronous access to the result and status
        # and makes sure only one client is used, no matter how often this state is used in a behavior.
        ProxyActionClient.initialize(RotateTurtleState._node)

        self._client = None

        # It may happen that the action client fails to send the action goal.
        self._error = False
        self._return = None  # Retain return value in case the outcome is blocked by operator
        self._start_time = None
        self._goal_sent = False
        self._goal = None

    def on_start(self):
        """Create the shared action client when the behavior starts."""
        self._client = ProxyActionClient({self._topic: RotateAbsolute}, wait_duration=0.0)

    def on_stop(self):
        """Remove the shared action client when the behavior stops."""
        ProxyActionClient.remove_client(self._topic)
        self._client = None

    def execute(self, userdata):
        """Send the goal once and then monitor action status until completion."""
        # While this state is active, check if the action has been finished and evaluate the result.

        # Check if the client failed to send the goal.
        if self._error:
            return 'failed'

        if self._return is not None:
            # Return prior outcome in case transition is blocked by autonomy level
            return self._return

        elapsed = self._node.get_clock().now() - self._start_time

        if not self._goal_sent:
            try:
                if self._client.is_available(self._topic):
                    self._client.send_goal(self._topic, self._goal, wait_duration=0.0)
                    self._goal_sent = True
                elif elapsed > self._timeout:
                    Logger.logwarn('Timeout waiting for action server!')
                    self._return = 'timeout'
                    return self._return
                return None
            except (AttributeError, RuntimeError, TypeError, ValueError) as exc:
                # Since a state failure not necessarily causes a behavior failure,
                # it is recommended to only print warnings, not errors.
                # Using a linebreak before appending the error log enables the operator to collapse details in the GUI.
                Logger.logwarn(f'Failed to send the RotateAbsolute command:\n  {type(exc)} - {exc}')
                self._error = True
        else:
            # Check if the action has been finished
            status = self._client.get_status(self._topic)
            if status == GoalStatus.STATUS_CANCELED:
                Logger.loginfo('Rotation goal was canceled')
                self._return = 'canceled'
                return self._return
            if status == GoalStatus.STATUS_ABORTED:
                Logger.logwarn('Rotation goal was aborted')
                self._return = 'failed'
                return self._return

            if self._client.has_result(self._topic):
                _ = self._client.get_result(self._topic)  # The delta result value is not useful here
                status = self._client.get_status(self._topic)
                if status == GoalStatus.STATUS_SUCCEEDED:
                    userdata.duration = self._node.get_clock().now() - self._start_time
                    Logger.loginfo('Rotation complete')
                    self._return = 'rotation_complete'
                    return self._return

            if elapsed > self._timeout:
                # Checking for timeout after we check for goal response
                self._return = 'timeout'
                Logger.logwarn('Timeout waiting for action response!')
                return 'timeout'

        # If the action has not yet finished, no outcome will be returned and the state stays active.
        return None

    def on_enter(self, userdata):
        """Validate input userdata and prepare the action goal."""
        # make sure to reset the error state since a previous state execution might have failed
        self._error = False
        self._return = None
        self._goal_sent = False

        if 'angle' not in userdata:
            self._error = True
            Logger.logwarn('RotateTurtleState requires userdata.angle key!')
            return

        # Recording the start time to set rotation duration output
        self._start_time = self._node.get_clock().now()

        goal = RotateAbsolute.Goal()

        if isinstance(userdata.angle, (float, int)):
            goal.theta = (userdata.angle * math.pi) / 180  # convert to radians
            self._goal = goal
        else:
            self._error = True
            Logger.logwarn(f'Input is {type(userdata.angle).__name__}. Expects an int or a float.')

    def on_exit(self, userdata):
        """Cancel the active goal if the state is interrupted mid-rotation."""
        # Make sure that the action is not running when leaving this state.
        # A situation where the action would still be active is for example
        # when the operator manually triggers an outcome.

        if self._goal_sent and not self._client.has_result(self._topic):
            self._client.cancel(self._topic)
            Logger.loginfo('Cancelled active action goal.')
