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

"""Teleport turtle FlexBE state."""

from rclpy.duration import Duration
from flexbe_core import EventState, Logger
from flexbe_core.proxy import ProxyServiceCaller

from turtlesim.srv import TeleportAbsolute


class TeleportAbsoluteState(EventState):
    """
    This state teleports the Turtlesim turtle using TeleportAbsolute service.

    Elements defined here for UI
    Parameters
    -- turtle_name   string     Turtle name (default: `turtle1`)
    -- x             float      x position (default: 0.0)
    -- y             float      y position (default: 0.0)
    -- theta         float      yaw orientation angle (radians) (default: 0.0)
    -- call_timeout  float      Timeout for completion (default: 3.0 seconds)
    -- wait_timeout  float      Duration to wait for service to become available (default: 3.0 seconds)
    -- service_name  string     Service name (default: `teleport_absolute`)

    Outputs
    <= done             Service call returned result as expected
    <= failed           Failed to make service call successfully
    <= call_timeout     Service call did not return timely result
    <= unavailable      Service is unavailable

    User data
    ># pose      float[]     Optional 2 (x, y) or 3 elements (x, y, theta_radians) as list of numbers
    """

    def __init__(self, turtle_name='turtle1', x=0.0, y=0.0, theta=0.0,
                 call_timeout=3.0, wait_timeout=3.0, service_name='teleport_absolute'):
        """Declare outcomes, input_keys, and output_keys by calling the EventState super constructor."""
        super().__init__(outcomes=['done', 'failed', 'call_timeout', 'unavailable'],
                         input_keys=['pose'])

        ProxyServiceCaller.initialize(TeleportAbsoluteState._node)

        # Store state parameters for later use.
        self._call_timeout = Duration(seconds=call_timeout)
        self._wait_timeout = Duration(seconds=wait_timeout)

        # The constructor is called when building the state machine, not when actually starting the behavior.
        # Thus, we cannot save the starting time now and will do so later.
        self._start_time = None
        self._return = None  # Track the outcome so we can detect if transition is blocked
        self._service_called = False

        self._srv_topic = f'/{turtle_name}/{service_name}'
        self._srv_result = None

        self._srv_request = TeleportAbsolute.Request()
        self._srv_request.x = x
        self._srv_request.y = y
        self._srv_request.theta = theta

        self._error = None
        self._srv = None

    def on_start(self):
        # Set up the proxy now, but do not wait on the service just yet
        self._srv = ProxyServiceCaller({self._srv_topic: TeleportAbsolute}, wait_duration=0.0)

    def on_stop(self):
        # Remove the proxy client if no longer in use
        ProxyServiceCaller.remove_client(self._srv_topic)
        self._srv = None

    def execute(self, userdata):
        """
        Execute this method periodically while the state is active.

        If no outcome is returned, the state will stay active.
        """
        if self._return:
            # We have completed the state, and therefore must be blocked by autonomy level
            return self._return

        if self._service_called:
            # Waiting for result.
            # We will do this in a non-blocking way
            if self._srv.done(self._srv_topic):
                _ = self._srv.result(self._srv_topic)  # grab empty result, but nothing to check here presume success
                self._return = 'done'
            else:

                if self._node.get_clock().now().nanoseconds - self._start_time.nanoseconds > self._call_timeout.nanoseconds:
                    # Failed to return call in timely manner
                    self._return = 'call_timeout'
                    Logger.logerr(f"{self._name}: Service {self._srv_topic} call timed out!")
        else:
            # Waiting for service to become available in non-blocking manner
            if self._srv.is_available(self._srv_topic, wait_duration=0.0):
                Logger.localinfo(f"{self._name}: Service {self._srv_topic} is now available - making service call!")
                self._do_service_call()
                # Process the result on next execute call (so some delay)
            else:
                if self._node.get_clock().now().nanoseconds - self._start_time.nanoseconds > self._wait_timeout.nanoseconds:
                    # Failed to return call in timely manner
                    self._return = 'unavailable'
                    Logger.logerr(f"{self._name}: Service {self._srv_topic} is unavailable!")

        return self._return

    def on_enter(self, userdata):
        """
        Call this method when the state becomes active.

        i.e. a transition from another state to this one is taken.
        """
        if 'pose' in userdata and isinstance(userdata.pose, (list, tuple)):
            try:
                self._srv_request.x = float(userdata.pose[0])
                self._srv_request.y = float(userdata.pose[1])
                self._srv_request.theta = 0.0
                if len(userdata.pose) == 3:
                    # setting angle is optional
                    self._srv_request.theta = float(userdata.pose[2])

                Logger.localinfo(f"Using position = ({self._srv_request.x:.3f}, {self._srv_request.y:.3f}), "
                                 f"angle={self._srv_request.theta:.3f} radians from userdata")

            except Exception as exc:  # pylint: disable=W0703
                Logger.logwarn(f"{self._name}: Invalid pose userdata {userdata.pose} - "
                               f"needs list of 2 or 3 numbers!\n  {type(exc)} - {exc}")
                self._return = 'failed'
                return
        else:
            Logger.localinfo(f"Using position = ({self._srv_request.x:.3f}, {self._srv_request.y:.3f}), "
                             f"angle={self._srv_request.theta:.3f} radians")

        self._start_time = self._node.get_clock().now()
        self._return = None  # reset the completion flag
        self._service_called = False
        try:
            if self._srv.is_available(self._srv_topic, wait_duration=0.0):
                self._do_service_call()
            else:
                Logger.logwarn(f"{self._name}: Service {self._srv_topic} is not yet available ...")
        except Exception as exc:  # pylint: disable=W0703
            Logger.logerr(f"{self._name}: Service {self._srv_topic} exception {type(exc)} - {str(exc)}")
            self._return = 'failed'

    def _do_service_call(self):
        """Make the service call using async non-blocking."""
        try:
            Logger.localinfo(f"{self._name}: Calling service {self._srv_topic} ...")
            self._srv_result = self._srv.call_async(self._srv_topic, self._srv_request, wait_duration=0.0)
            self._start_time = self._node.get_clock().now()  # Reset timer for call timeout
            self._service_called = True
        except Exception as exc:
            Logger.logerr(f"{self._name}: Service {self._srv_topic} exception {type(exc)} - {str(exc)}")
            raise exc
