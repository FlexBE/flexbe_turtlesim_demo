#!/usr/bin/env python3

# Copyright 2026 Christopher Newport University
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#    * Redistributions of source code must retain the above copyright
#      notice, this list of conditions and the following disclaimer.
#    * Redistributions in binary form must reproduce the above copyright
#      notice, this list of conditions and the following disclaimer in the
#      documentation and/or other materials provided with the distribution.
#    * Neither the name of the Philipp Schillinger, Team ViGIR, Christopher Newport University nor the names of its
#      contributors may be used to endorse or promote products derived from
#      this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

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
