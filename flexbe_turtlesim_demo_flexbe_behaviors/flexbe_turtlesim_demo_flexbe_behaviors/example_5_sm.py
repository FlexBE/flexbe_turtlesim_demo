#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2026 David Conner
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
Define Example 5.

Demonstrates using a PriorityContainer inside a ConcurrencyContainer.
The PriorityContainer (Priority_Work) runs a two-step sequential initialization sequence
that blocks all sibling states from executing — including deferring their on_enter calls —
until the priority sequence completes.
Both Priority_Work and Normal_Work must complete (AND condition) before the container exits.

Created on Mon Mar 23 2026
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
from flexbe_turtlesim_demo_flexbe_states.example_state import ExampleState

# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]


# [/MANUAL_IMPORT]


class Example5SM(Behavior):
    """
    Define Example 5.

    Demonstrates using a PriorityContainer inside a ConcurrencyContainer.
    The PriorityContainer runs a two-step sequential initialization sequence that blocks
    all sibling states — including deferring their on_enter calls — until it completes.
    Both Priority_Work and Normal_Work must complete (AND condition) before the container exits.
    """

    def __init__(self, node):
        super().__init__()
        self.name = 'Example 5'

        # parameters of this behavior
        self.add_parameter('waiting_time_priority_a', 1.0)
        self.add_parameter('waiting_time_priority_b', 1.0)
        self.add_parameter('waiting_time_normal', 5.0)

        # Initialize ROS node information
        initialize_flexbe_core(node)

        # references to used behaviors

        # Additional initialization code can be added inside the following tags
        # [MANUAL_INIT]


        # [/MANUAL_INIT]

        # Behavior comments:

        # ! 400 150 /Concurrent_Priority/Priority_Work
        # PriorityContainer must be added FIRST inside ConcurrencyContainer.add() so that it claims
        # PriorityContainer.active_container from the very first execute tic.
        # While Priority_Work is active, Normal_Work is skipped each tic and its on_enter is deferred.

        # ! 400 250 /Concurrent_Priority/Normal_Work
        # Normal_Work only begins (on_enter is called) after Priority_Work has completed.
        # The ConcurrencyContainer exits with 'finished' when both states have returned 'done'.

    def create(self):
        """Create state machine."""
        # Private variables
        start_msg = 'Example 5: Priority container demo started!'
        done_msg = 'Example 5: All work complete!'

        # Root state machine
        # x:970 y:83, x:975 y:208
        _state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])

        # Additional creation code can be added inside the following tags
        # [MANUAL_CREATE]


        # [/MANUAL_CREATE]

        # x:350 y:60, x:100 y:200
        _sm_priority_work_0 = PriorityContainer(outcomes=['done', 'failed'])

        with _sm_priority_work_0:
            # x:80 y:72
            OperatableStateMachine.add('Init_A',
                                       ExampleState(target_time=self.waiting_time_priority_a),
                                       transitions={'done': 'Init_B', 'failed': 'failed'},
                                       autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off})

            # x:300 y:72
            OperatableStateMachine.add('Init_B',
                                       ExampleState(target_time=self.waiting_time_priority_b),
                                       transitions={'done': 'done', 'failed': 'failed'},
                                       autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off})

        # x:1330 y:80, x:1330 y:160, x:1330 y:240, x:1330 y:320, x:1330 y:400
        _sm_concurrent_priority_1 = ConcurrencyContainer(outcomes=['finished', 'failed'],
                                                         conditions=[('finished', [('Priority_Work', 'done'), ('Normal_Work', 'done')]),
                                                                     ('failed', [('Priority_Work', 'failed')]),
                                                                     ('failed', [('Normal_Work', 'failed')])
                                                                     ])

        with _sm_concurrent_priority_1:
            # x:30 y:40
            OperatableStateMachine.add('Priority_Work',
                                       _sm_priority_work_0,
                                       transitions={'done': 'finished', 'failed': 'failed'},
                                       autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off})

            # x:80 y:240
            OperatableStateMachine.add('Normal_Work',
                                       ExampleState(target_time=self.waiting_time_normal),
                                       transitions={'done': 'finished', 'failed': 'failed'},
                                       autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off})

        with _state_machine:
            # x:52 y:78
            OperatableStateMachine.add('Start',
                                       LogState(text=start_msg,
                                                severity=Logger.REPORT_HINT),
                                       transitions={'done': 'Concurrent_Priority'},
                                       autonomy={'done': Autonomy.Off})

            # x:350 y:78
            OperatableStateMachine.add('Concurrent_Priority',
                                       _sm_concurrent_priority_1,
                                       transitions={'finished': 'Done', 'failed': 'Failed'},
                                       autonomy={'finished': Autonomy.Inherit,
                                                 'failed': Autonomy.Inherit})

            # x:650 y:78
            OperatableStateMachine.add('Done',
                                       LogState(text=done_msg,
                                                severity=Logger.REPORT_HINT),
                                       transitions={'done': 'finished'},
                                       autonomy={'done': Autonomy.High})

            # x:650 y:200
            OperatableStateMachine.add('Failed',
                                       LogState(text='Failure encountered',
                                                severity=Logger.REPORT_ERROR),
                                       transitions={'done': 'failed'},
                                       autonomy={'done': Autonomy.High})

        return _state_machine

    # Private functions can be added inside the following tags
    # [MANUAL_FUNC]


    # [/MANUAL_FUNC]
