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

"""Regression tests for RotateTurtleState terminal status handling."""

from types import SimpleNamespace
from unittest.mock import patch

from action_msgs.msg import GoalStatus

from flexbe_turtlesim_demo_flexbe_states.rotate_turtle_state import RotateTurtleState

from rclpy.duration import Duration


class _FakeElapsed:
    nanoseconds = 0

    def __gt__(self, _other):
        return False


class _FakeTime:

    def __sub__(self, _other):
        return _FakeElapsed()


class _FakeClock:

    def now(self):
        return _FakeTime()


class _FakeNode:

    def get_clock(self):
        return _FakeClock()


class _FakeActionClient:

    def __init__(self, has_result=False, status=None, result=None):
        self._has_result = has_result
        self._status = status
        self._result = result

    def has_result(self, _topic):
        return self._has_result

    def get_result(self, _topic):
        return self._result

    def get_status(self, _topic):
        return self._status


@patch('flexbe_turtlesim_demo_flexbe_states.rotate_turtle_state.Logger.loginfo')
@patch('flexbe_turtlesim_demo_flexbe_states.rotate_turtle_state.Logger.logwarn')
def test_rotate_turtle_state_reports_terminal_statuses(_logwarn, _loginfo):
    """Canceled and failed action results should not be reported as success."""
    success_state = object.__new__(RotateTurtleState)
    success_state._client = _FakeActionClient(
        has_result=True,
        status=GoalStatus.STATUS_SUCCEEDED,
        result=SimpleNamespace(),
    )
    success_state._topic = '/turtle1/rotate_absolute'
    success_state._node = _FakeNode()
    success_state._start_time = _FakeTime()
    success_state._timeout = Duration(seconds=10.0)
    success_state._goal_sent = True
    success_state._error = False
    success_state._return = None
    userdata = SimpleNamespace(duration=None)

    assert success_state.execute(userdata) == 'rotation_complete'
    assert isinstance(userdata.duration, float)

    canceled_state = object.__new__(RotateTurtleState)
    canceled_state._client = _FakeActionClient(
        has_result=True,
        status=GoalStatus.STATUS_CANCELED,
        result=SimpleNamespace(),
    )
    canceled_state._topic = '/turtle1/rotate_absolute'
    canceled_state._node = _FakeNode()
    canceled_state._start_time = _FakeTime()
    canceled_state._timeout = Duration(seconds=10.0)
    canceled_state._goal_sent = True
    canceled_state._error = False
    canceled_state._return = None

    assert canceled_state.execute(SimpleNamespace(duration=None)) == 'canceled'

    aborted_state = object.__new__(RotateTurtleState)
    aborted_state._client = _FakeActionClient(
        has_result=False,
        status=GoalStatus.STATUS_ABORTED,
        result=None,
    )
    aborted_state._topic = '/turtle1/rotate_absolute'
    aborted_state._node = _FakeNode()
    aborted_state._start_time = _FakeTime()
    aborted_state._timeout = Duration(seconds=10.0)
    aborted_state._goal_sent = True
    aborted_state._error = False
    aborted_state._return = None

    assert aborted_state.execute(SimpleNamespace(duration=None)) == 'failed'
