# Copyright 2017 Open Source Robotics Foundation, Inc.
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

"""Run flake8 tests."""

from pathlib import Path
import warnings

from ament_flake8.main import main_with_errors

import pytest


@pytest.mark.flake8
@pytest.mark.linter
def test_flake8():
    """Run flake8 tests."""
    warnings.filterwarnings(
        'ignore',
        message=r'This process \(pid=\d+\) is multi-threaded, use of fork\(\) may lead to deadlocks in the child\.',
        category=DeprecationWarning,
    )

    test_dir = Path(__file__).resolve().parent
    package_dir = test_dir.parent / 'flexbe_turtlesim_demo_flexbe_behaviors'
    repo_root = test_dir.parent.parent
    config_file = repo_root / '.flake8'

    # Exclude generated *_sm.py files; only check hand-written sources
    hand_written = [p for p in package_dir.glob('*.py') if not p.name.endswith('_sm.py')]
    custom_argv = [
        '--config',
        str(config_file),
        *[str(p) for p in sorted(hand_written)],
        str(test_dir),
        str(test_dir.parent / 'setup.py'),
    ]
    ret, errors = main_with_errors(argv=custom_argv)
    assert ret == 0, \
        f'Found {len(errors)} code style errors / warnings:\n' + \
        '\n'.join(errors)
