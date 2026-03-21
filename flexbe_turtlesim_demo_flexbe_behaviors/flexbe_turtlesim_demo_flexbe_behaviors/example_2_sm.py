#!/usr/bin/env python
# -*- coding: utf-8 -*-

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

###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

"""
Define Example 2 Behavior.

Created on Thursday 30-June-2023
@author: David Conner
"""


from flexbe_core import Autonomy, Behavior, ConcurrencyContainer, Logger, OperatableStateMachine, PriorityContainer

from flexbe_states.log_state import LogState

from flexbe_turtlesim_demo_flexbe_states.example_state import ExampleState as flexbe_turtlesim_demo_flexbe_states__ExampleState

# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


class Example2SM(Behavior):
    """
    Define Example State Behavior.

    This is a simple example for a behavior using custom ExampleState that logs each function in life cycle.
    """

    def __init__(self, node):
        """Initialize ROS resources and behavior parameters."""
        super().__init__()
        self.name = 'Example 2'

        # parameters of this behavior
        self.add_parameter('waiting_time', 3)

        # references to used behaviors
        OperatableStateMachine.initialize_ros(node)
        ConcurrencyContainer.initialize_ros(node)
        PriorityContainer.initialize_ros(node)
        Logger.initialize(node)
        LogState.initialize_ros(node)
        flexbe_turtlesim_demo_flexbe_states__ExampleState.initialize_ros(node)

        # Additional initialization code can be added inside the following tags
        # [MANUAL_INIT]

        # [/MANUAL_INIT]

        # Behavior comments:

    def create(self):
        """Build the behavior state machine."""
        start_msg = 'Demo started!'
        done_msg = 'Demo finished!'
        # x:823 y:238, x:836 y:155
        _state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])

        # Additional creation code can be added inside the following tags
        # [MANUAL_CREATE]

        # [/MANUAL_CREATE]
        with _state_machine:
            # x:52 y:78
            OperatableStateMachine.add('Start',
                                       LogState(text=start_msg, severity=Logger.REPORT_HINT),
                                       transitions={'done': 'A'},
                                       autonomy={'done': Autonomy.Low})

            # x:562 y:190
            OperatableStateMachine.add('Done',
                                       LogState(text=done_msg, severity=Logger.REPORT_HINT),
                                       transitions={'done': 'finished'},
                                       autonomy={'done': Autonomy.Off})

            # x:224 y:81
            OperatableStateMachine.add('A',
                                       flexbe_turtlesim_demo_flexbe_states__ExampleState(target_time=self.waiting_time),
                                       transitions={'done': 'Done', 'failed': 'failed'},
                                       autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off})

        return _state_machine

    # Private functions can be added inside the following tags
    # [MANUAL_FUNC]

    # [/MANUAL_FUNC]
