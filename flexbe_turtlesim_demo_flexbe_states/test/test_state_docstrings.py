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

"""Validate FlexBE state docstring tags consumed by the WebUI state parser."""

from pathlib import Path

from flexbe_testing.state_docstring_tester import assert_state_docstrings_valid


def test_state_docstring_tags_are_valid():
    """Check state docstring tags for this package."""
    package_dir = Path(__file__).resolve().parents[1]
    paths = [package_dir / 'flexbe_turtlesim_demo_flexbe_states']
    assert_state_docstrings_valid(paths, strict_interface=True)
