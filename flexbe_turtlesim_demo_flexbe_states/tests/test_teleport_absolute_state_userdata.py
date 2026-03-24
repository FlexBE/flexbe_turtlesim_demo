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

"""Regression tests for TeleportAbsoluteState userdata validation."""

import unittest
from types import SimpleNamespace
from unittest.mock import patch

from flexbe_turtlesim_demo_flexbe_states.teleport_absolute_state import TeleportAbsoluteState


class _FakeTime:

    nanoseconds = 0


class _FakeClock:

    def now(self):
        return _FakeTime()


class _FakeNode:

    def get_clock(self):
        return _FakeClock()


class _FakeServiceCaller:

    def __init__(self):
        self.available_calls = []
        self.call_async_calls = []

    def is_available(self, topic, wait_duration=0.0):
        self.available_calls.append((topic, wait_duration))
        return False

    def call_async(self, topic, request, wait_duration=0.0):
        self.call_async_calls.append((topic, request, wait_duration))
        return object()


class _FakeUserdata(SimpleNamespace):

    def __contains__(self, key):
        return hasattr(self, key)


class TestTeleportAbsoluteStateUserdata(unittest.TestCase):
    """Ensure invalid pose userdata fails instead of reusing a stale request."""

    def _make_state(self):
        state = object.__new__(TeleportAbsoluteState)
        state._name = 'TeleportAbsoluteState'
        state._srv_request = SimpleNamespace(x=1.0, y=2.0, theta=3.0)
        state._srv_topic = '/turtle1/teleport_absolute'
        state._node = _FakeNode()
        state._srv = _FakeServiceCaller()
        state._return = 'done'
        state._service_called = True
        state._start_time = None
        return state

    @patch('flexbe_turtlesim_demo_flexbe_states.teleport_absolute_state.Logger.logwarn')
    def test_invalid_pose_type_fails_without_reusing_stale_request(self, logwarn):
        """A present but invalid pose should fail immediately and never call the service."""
        state = self._make_state()

        state.on_enter(_FakeUserdata(pose='bad-pose'))

        self.assertEqual('failed', state._return)
        self.assertFalse(state._service_called)
        self.assertIsNone(state._start_time)
        self.assertEqual([], state._srv.available_calls)
        self.assertEqual([], state._srv.call_async_calls)
        self.assertEqual(1.0, state._srv_request.x)
        self.assertEqual(2.0, state._srv_request.y)
        self.assertEqual(3.0, state._srv_request.theta)
        logwarn.assert_called_once()


if __name__ == '__main__':
    unittest.main()
