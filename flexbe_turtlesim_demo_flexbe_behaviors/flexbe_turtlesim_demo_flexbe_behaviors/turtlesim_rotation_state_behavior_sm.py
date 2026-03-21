#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright 2026 Collin Stone
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
Define Turtlesim Rotation State Behavior.

Created on Mon Jul 17 2023
@author: Collin Stone
"""


from flexbe_core import Autonomy, Behavior, ConcurrencyContainer, Logger, OperatableStateMachine, PriorityContainer

from flexbe_states.log_state import LogState

from flexbe_turtlesim_demo_flexbe_states.rotate_turtle_state import RotateTurtleState

# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


class TurtlesimRotationStateBehaviorSM(Behavior):
    """
    Define Turtlesim Rotation State Behavior.

    A simple behavior demonstrating the Turtlesim RotateAbsolute action interface.

    The example includes userdata defined in the statemachine configuration.

    """

    def __init__(self, node):
        """Initialize ROS resources for the fixed-angle rotate demo."""
        super().__init__()
        self.name = 'Turtlesim Rotation State Behavior'

        # parameters of this behavior

        # references to used behaviors
        OperatableStateMachine.initialize_ros(node)
        ConcurrencyContainer.initialize_ros(node)
        PriorityContainer.initialize_ros(node)
        Logger.initialize(node)
        LogState.initialize_ros(node)
        RotateTurtleState.initialize_ros(node)

        # Additional initialization code can be added inside the following tags
        # [MANUAL_INIT]

        # [/MANUAL_INIT]

        # Behavior comments:

    def create(self):
        """Build the behavior state machine."""
        # x:1096 y:62, x:1095 y:363
        _state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])
        _state_machine.userdata.angle_degrees = 90.0

        # Additional creation code can be added inside the following tags
        # [MANUAL_CREATE]

        # [/MANUAL_CREATE]
        with _state_machine:
            # x:244 y:294
            OperatableStateMachine.add('Rotate Turtle State',
                                       RotateTurtleState(timeout=10, action_topic='/turtle1/rotate_absolute'),
                                       transitions={'rotation_complete': 'Log Success', 'failed': 'Log Failed',
                                                    'canceled': 'Log Canceled', 'timeout': 'Log Timeout'},
                                       autonomy={'rotation_complete': Autonomy.Off, 'failed': Autonomy.Off,
                                                 'canceled': Autonomy.Off, 'timeout': Autonomy.Off},
                                       remapping={'angle': 'angle_degrees', 'duration': 'duration'})

            # x:659 y:190
            OperatableStateMachine.add('Log Failed',
                                       LogState(text='Failed', severity=Logger.REPORT_WARN),
                                       transitions={'done': 'failed'},
                                       autonomy={'done': Autonomy.Off})

            # x:658 y:57
            OperatableStateMachine.add('Log Success',
                                       LogState(text='Success', severity=Logger.REPORT_HINT),
                                       transitions={'done': 'finished'},
                                       autonomy={'done': Autonomy.Off})

            # x:657 y:480
            OperatableStateMachine.add('Log Timeout',
                                       LogState(text='Timeout', severity=Logger.REPORT_WARN),
                                       transitions={'done': 'failed'},
                                       autonomy={'done': Autonomy.Off})

            # x:656 y:337
            OperatableStateMachine.add('Log Canceled',
                                       LogState(text='Canceled', severity=Logger.REPORT_WARN),
                                       transitions={'done': 'failed'},
                                       autonomy={'done': Autonomy.Off})

        return _state_machine

    # Private functions can be added inside the following tags
    # [MANUAL_FUNC]

    # [/MANUAL_FUNC]
