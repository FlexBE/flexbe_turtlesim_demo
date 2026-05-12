#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2023 David Conner
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

###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

"""
Define Example 3.

This is a simple example for a behavior with a ConcurrencyContainer.

The behavior makes use of the custom ExampleState that logs each function in
life cycle.

Here we demonstrate concurrent behaviors with both OR and AND style exit
conditions.

Created on Thursday 30-June-2023
@author: David Conner
"""


from flexbe_core import Autonomy
from flexbe_core import Behavior
from flexbe_core import ConcurrencyContainer
from flexbe_core import Logger
from flexbe_core import OperatableStateMachine
from flexbe_core import PriorityContainer
from flexbe_core import initialize_flexbe_core
from flexbe_states.log_state import LogState
from flexbe_states.wait_state import WaitState
from flexbe_turtlesim_demo_flexbe_states.example_state import ExampleState

# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]


# [/MANUAL_IMPORT]


class Example3SM(Behavior):
    """
    Define Example 3.

    This is a simple example for a behavior with a ConcurrencyContainer.

    The behavior makes use of the custom ExampleState that logs each function in
    life cycle.

    Here we demonstrate concurrent behaviors with both OR and AND style exit
    conditions.
    """

    def __init__(self, node):
        super().__init__()
        self.name = 'Example 3'

        # parameters of this behavior
        self.add_parameter('waiting_time_a', 4.0)
        self.add_parameter('waiting_time_b', 2.0)
        self.add_parameter('waiting_time_c', 4.0)
        self.add_parameter('waiting_time_d', 2.0)

        # Initialize ROS node information
        initialize_flexbe_core(node)

        # references to used behaviors

        # Additional initialization code can be added inside the following tags
        # [MANUAL_INIT]


        # [/MANUAL_INIT]

        # Behavior comments:

        # ! 909 135
        # Behavior execution stops here!

        # ! 478 119 /Container_AND
        # Both C and D must return outcome Done to exit this concurrency container.
        # If one finishes, it will stop execution and exit its state, but the other state
        # will continue to execute until either done or failed

        # ! 524 140 /Concurrent_OR
        # Either A or B returning outcome will exit this concurrent container since we are using single connections!

    def create(self):
        """Create state machine."""
        # Private variables
        start_msg = 'Demo started!'
        done_msg = 'Demo finished!'

        # Root state machine
        # x:920 y:78, x:909 y:171
        _state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])

        # Additional creation code can be added inside the following tags
        # [MANUAL_CREATE]


        # [/MANUAL_CREATE]

        # x:500 y:78, x:482 y:226, x:230 y:365, x:475 y:287, x:430 y:365
        _sm_container_and_0 = ConcurrencyContainer(outcomes=['finished', 'failed'],
                                                   conditions=[('finished', [('C', 'done'), ('D', 'done')]),
                                                               ('failed', [('C', 'failed')]),
                                                               ('failed', [('D', 'failed')])
                                                               ])

        with _sm_container_and_0:
            # x:108 y:72
            OperatableStateMachine.add('C',
                                       ExampleState(target_time=self.waiting_time_c),
                                       transitions={'done': 'finished', 'failed': 'failed'},
                                       autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off})

            # x:110 y:173
            OperatableStateMachine.add('D',
                                       ExampleState(target_time=self.waiting_time_d),
                                       transitions={'done': 'finished', 'failed': 'failed'},
                                       autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off})

        # x:478 y:55, x:469 y:111, x:455 y:259, x:462 y:183, x:448 y:317, x:444 y:365
        _sm_concurrent_or_1 = ConcurrencyContainer(outcomes=['finished', 'failed'],
                                                   conditions=[('finished', [('A', 'done')]),
                                                               ('finished', [('B', 'done')]),
                                                               ('failed', [('A', 'failed')]),
                                                               ('failed', [('B', 'failed')])
                                                               ])

        with _sm_concurrent_or_1:
            # x:30 y:40
            OperatableStateMachine.add('A',
                                       ExampleState(target_time=self.waiting_time_a),
                                       transitions={'done': 'finished', 'failed': 'failed'},
                                       autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off})

            # x:30 y:168
            OperatableStateMachine.add('B',
                                       ExampleState(target_time=self.waiting_time_b),
                                       transitions={'done': 'finished', 'failed': 'failed'},
                                       autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off})

        with _state_machine:
            # x:52 y:78
            OperatableStateMachine.add('Start',
                                       LogState(text=start_msg,
                                                severity=Logger.REPORT_HINT),
                                       transitions={'done': 'Concurrent_OR'},
                                       autonomy={'done': Autonomy.Low})

            # x:128 y:201
            OperatableStateMachine.add('Concurrent_OR',
                                       _sm_concurrent_or_1,
                                       transitions={'finished': 'Delay', 'failed': 'Failed'},
                                       autonomy={'finished': Autonomy.Inherit,
                                                 'failed': Autonomy.Inherit})

            # x:565 y:166
            OperatableStateMachine.add('Container_AND',
                                       _sm_container_and_0,
                                       transitions={'finished': 'Done', 'failed': 'Failed'},
                                       autonomy={'finished': Autonomy.Inherit,
                                                 'failed': Autonomy.Inherit})

            # x:273 y:106
            OperatableStateMachine.add('Delay',
                                       WaitState(wait_time=1.0),
                                       transitions={'done': 'EnterAnd'},
                                       autonomy={'done': Autonomy.Off})

            # x:740 y:72
            OperatableStateMachine.add('Done',
                                       LogState(text=done_msg,
                                                severity=Logger.REPORT_HINT),
                                       transitions={'done': 'finished'},
                                       autonomy={'done': Autonomy.High})

            # x:424 y:107
            OperatableStateMachine.add('EnterAnd',
                                       LogState(text='Enter the AND Concurrent state ...',
                                                severity=Logger.REPORT_HINT),
                                       transitions={'done': 'Container_AND'},
                                       autonomy={'done': Autonomy.Off})

            # x:750 y:301
            OperatableStateMachine.add('Failed',
                                       LogState(text='Failure encountered',
                                                severity=Logger.REPORT_ERROR),
                                       transitions={'done': 'failed'},
                                       autonomy={'done': Autonomy.High})

        return _state_machine

    # Private functions can be added inside the following tags
    # [MANUAL_FUNC]


    # [/MANUAL_FUNC]
