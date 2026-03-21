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

"""Regression tests for TimedCmdVelState cleanup hooks."""

import unittest
from types import SimpleNamespace
from unittest.mock import patch

from flexbe_turtlesim_demo_flexbe_states.timed_cmd_vel_state import TimedCmdVelState

from geometry_msgs.msg import Twist


class _FakePublisher:

    def __init__(self):
        self.messages = []

    def publish(self, topic, msg):
        self.messages.append((topic, msg))


class _FakeTime:

    def __init__(self, nanoseconds):
        self.nanoseconds = nanoseconds


class _FakeClock:

    def __init__(self):
        self._now = _FakeTime(0)

    def now(self):
        return self._now


class _FakeNode:

    def __init__(self):
        self._clock = _FakeClock()

    def get_clock(self):
        return self._clock


class TestTimedCmdVelStateCleanup(unittest.TestCase):
    """Ensure open-loop velocity commands are cleared on interruption paths."""

    def _make_state(self):
        state = object.__new__(TimedCmdVelState)
        state._cmd_topic = '/turtle1/cmd_vel'
        state._pub = _FakePublisher()
        state._stop_twist = Twist()
        state._twist = Twist()
        state._node = _FakeNode()
        state._target_time = type('TargetTime', (), {'nanoseconds': int(1e9)})()
        state._start_time = None
        state._pause_time = None
        state._paused_duration_ns = 0
        state._return = None
        state._name = 'TimedCmdVelState'
        return state

    def test_on_pause_and_on_stop_publish_zero_twist(self):
        """Pause and stop should both actively clear the last commanded velocity."""
        state = self._make_state()

        state.on_pause()
        state.on_stop()

        self.assertEqual(2, len(state._pub.messages))
        for topic, msg in state._pub.messages:
            self.assertEqual('/turtle1/cmd_vel', topic)
            self.assertEqual(0.0, msg.linear.x)
            self.assertEqual(0.0, msg.angular.z)

    def test_on_exit_stops_only_when_interrupted(self):
        """Normal chained completion should not publish a stop, but interruption should."""
        interrupted_state = self._make_state()
        interrupted_state._return = None

        interrupted_state.on_exit(SimpleNamespace())

        self.assertEqual(1, len(interrupted_state._pub.messages))
        topic, msg = interrupted_state._pub.messages[0]
        self.assertEqual('/turtle1/cmd_vel', topic)
        self.assertEqual(0.0, msg.linear.x)
        self.assertEqual(0.0, msg.angular.z)

        completed_state = self._make_state()
        completed_state._return = 'done'

        completed_state.on_exit(SimpleNamespace())

        self.assertEqual([], completed_state._pub.messages)

    @patch('flexbe_turtlesim_demo_flexbe_states.timed_cmd_vel_state.Logger.localinfo')
    def test_on_resume_excludes_paused_time_from_completion(self, _localinfo):
        """A long pause should not cause the state to complete immediately on resume."""
        state = self._make_state()
        clock = state._node.get_clock()

        clock._now = _FakeTime(0)
        state.on_enter(SimpleNamespace())

        clock._now = _FakeTime(400_000_000)
        state.on_pause()

        clock._now = _FakeTime(2_400_000_000)
        state.on_resume(SimpleNamespace())

        clock._now = _FakeTime(2_500_000_000)
        self.assertIsNone(state.execute(SimpleNamespace()))

        clock._now = _FakeTime(3_100_000_000)
        self.assertEqual('done', state.execute(SimpleNamespace()))


if __name__ == '__main__':
    unittest.main()
