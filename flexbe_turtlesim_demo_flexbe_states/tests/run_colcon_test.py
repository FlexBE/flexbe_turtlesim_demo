# Copyright 2026 Christopher Newport University
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#    * Redistributions of source code must retain the above copyright
#      notice, this list of conditions and the following disclaimer.
#
#    * Redistributions in binary form must reproduce the above copyright
#      notice, this list of conditions and the following disclaimer in the
#      documentation and/or other materials provided with the distribution.
#
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


"""Pytest testing for flexbe_turtlesim_demo_flexbe_states."""

from pathlib import Path

from flexbe_testing.py_tester import PyTester


class TestFlexBETurtleSimDemoStates(PyTester):
    """Pytest testing for flexbe_turtlesim_demo_flexbe_states."""

    # def __init__(self, *args, **kwargs):
    #     """Initialize unit test."""
    #     super().__init__(*args, **kwargs)

    @classmethod
    def setUpClass(cls):
        """Point PyTester at the installed test assets for this package."""
        PyTester._package = 'flexbe_turtlesim_demo_flexbe_states'
        PyTester._tests_folder = 'tests'

        PyTester.setUpClass()  # Do this last after setting package and tests folder


_TEST_TIMEOUTS = {
    'clear_turtlesim_state': {'timeout_sec': 2.0, 'max_cnt': 5000},
    'rotate_turtle_state': {'timeout_sec': 2.0, 'max_cnt': 5000},
    'teleport_absolute_state': {'timeout_sec': 2.0, 'max_cnt': 5000},
    'timed_cmd_vel_state': {'timeout_sec': 2.0, 'max_cnt': 5000},
}


def _make_flexbe_test(test_name):
    """Create a pytest/unittest-compatible test method for a single FlexBE .test file."""

    def _test(self):
        self.run_test(test_name, **_TEST_TIMEOUTS.get(test_name, {}))

    _test.__name__ = f'test_{test_name}'
    _test.__doc__ = f"Run FlexBE unit test from '{test_name}.test'."
    return _test


for _test_file in sorted(Path(__file__).resolve().parent.glob('*.test')):
    setattr(TestFlexBETurtleSimDemoStates, f'test_{_test_file.stem}', _make_flexbe_test(_test_file.stem))
