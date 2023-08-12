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

"""clear turtlesim FlexBE state."""

from rclpy.duration import Duration
from flexbe_core import EventState, Logger
from flexbe_core.proxy import ProxyServiceCaller

from std_srvs.srv import Empty


class ClearTurtlesimState(EventState):
    """
    This state clears the Turtlesim window using the /clear service.

    This approach using the blocking call on enter.
    This is generally NOT advised if there are any potential concurrent operations.

    -- service_name   string    Service name (default: `/clear`)
    -- wait_timeout  float      Duration to wait for service to become available (default: 3.0 seconds)
    <= done             Service call returned result as expected
    <= failed           Service failed to return result
    <= unavailable      Service is unavailable
    """

    def __init__(self, service_name='/clear', wait_timeout=3.0):
        # Declare outcomes, input_keys, and output_keys by calling the super constructor with the corresponding arguments.
        super().__init__(outcomes=['done', 'failed', 'unavailable'])

        ProxyServiceCaller.initialize(ClearTurtlesimState._node)

        # Store state parameters for later use.
        self._wait_timeout = Duration(seconds=wait_timeout)

        # The constructor is called when building the state machine, not when actually starting the behavior.
        # Thus, we cannot save the starting time now and will do so later.
        self._start_time = None
        self._return = None  # Track the outcome so we can detect if transition is blocked
        self._service_called = False

        self._srv_topic = service_name
        self._srv_result = None

        self._srv_request = Empty.Request()

        self._error = None
        self._srv = None

    def on_start(self):
        # Set up the proxy now, but do not wait on the service just yet
        self._srv = ProxyServiceCaller({self._srv_topic: Empty}, wait_duration=0.0)

    def on_stop(self):
        # Remove the proxy client if no longer in use
        ProxyServiceCaller.remove_client(self._srv_topic)
        self._srv = None


    def execute(self, userdata):
        # Execute this method periodically while the state is active.
        # If no outcome is returned, the state will stay active.

        if self._return:
            # We have completed the state, and therefore must be blocked by autonomy level
            # Logger.localinfo(f"{self._name}: returning existing value {self._return} .")
            return self._return

        if self._service_called:
            # Called from on_enter
            # Logger.localinfo(f"{self._name}: Service called  - check result {self._srv_result} .")
            if self._srv_result is None:
                Logger.loginfo(f"{self._name}: Service {self._srv_topic} failed to return result!")
                self._return = 'failed'
            else:
                self._return = 'done'

        else:
            # Waiting for service to become available in non-blocking manner
            # Logger.localinfo(f"{self._name}: Service not called - check if {self._srv_topic} is available now ...")
            if self._srv.is_available(self._srv_topic, wait_duration=0.0):
                Logger.localinfo(f"{self._name}: Service {self._srv_topic} is now available - making service call to clear!")
                self._do_service_call()
                if self._srv_result is None:
                    Logger.logerr(f"{self._name}: Service {self._srv_topic} failed to return result!")
                    self._return = 'failed'
                else:
                    self._return = 'done'
            else:
                if self._node.get_clock().now().nanoseconds - self._start_time.nanoseconds > self._wait_timeout.nanoseconds:
                    # Failed to return call in timely manner
                    self._return = 'unavailable'
                    Logger.logerr(f"{self._name}: Service {self._srv_topic} is unavailable!")

        return self._return

    def on_enter(self, userdata):
        """
        Call when the state becomes active.

        This example does NOT use any userdata passed from upstream states.

        , i.e. a transition from another state to this one is taken.
        """
        self._start_time = self._node.get_clock().now()
        self._return = None  # reset the completion flag
        self._srv_result = None
        self._service_called = False
        try:
            if self._srv.is_available(self._srv_topic, wait_duration=0.0):
                Logger.localinfo(f"{self._name}: Service {self._srv_topic} is available ...")
                self._do_service_call()
            else:
                Logger.logwarn(f"{self._name}: Service {self._srv_topic} is not yet available ...")
        except Exception as exc:  # pylint: disable=W0703
            Logger.logerr(f"{self._name}: Service {self._srv_topic} exception {type(exc)} - {str(exc)}")

    def _do_service_call(self):
        """Make the service call using synchronous blocking call."""
        try:
            Logger.localinfo(f"{self._name}: Calling service {self._srv_topic} ...")
            self._service_called = True
            self._srv_result = self._srv.call(self._srv_topic, self._srv_request, wait_duration=0.0)
        except Exception as exc:  # pylint: disable=W0703
            Logger.logerr(f"{self._name}: Service {self._srv_topic} exception {type(exc)} - {str(exc)}")
            self._srv_result = None
