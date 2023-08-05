# -*- coding: utf-8 -*-
'''
    :copyright: © 2017-2019 by Farhan Ahmed.
    :license: BSD-3-Clause, see LICENSE for more details.
'''

class Transition(object):
    '''This class models a state change in response to an event firing within a state machine. It encapsulates all details about the change and is yielded as an argument to all callbacks within Flux. The optional dictionary of `user_info` can be used to broadcast arbitrary data across callbacks.
    '''    
    def __init__(self, event, source_state, state_machine, user_info=None):
        '''Creates and returns a new transition object describing a state change occurring
        within a state machine in response to the firing of an event.

        :param event:         The event being fired that is causing the transition to occur.
        :param source_state:  The state of the machine when the event was fired.
        :param state_machine: The state machine in which the transition is occurring.
        :param user_info:     An optional dictionary of user info supplied with the event when it was fired.
        '''
        
        self.event             = event
        self.source_state      = source_state
        self.destination_state = event.destination_state
        self.state_machine     = state_machine
        self.user_info         = user_info
