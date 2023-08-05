# -*- coding: utf-8 -*-
'''
    :copyright: © 2017-2019 by Farhan Ahmed.
    :license: BSD-3-Clause, see LICENSE for more details.
'''

from .errors import StateMachineStateError
from .       import constants as STATE_MACHINE

class StateCallbacks:
    '''A data object used for passing state information to the :class:`State` constructor
    Following callback keywords are supported:
    
    - ``will_enter_state``
    - ``did_enter_state``
    - ``will_exit_state``
    - ``did_exit_state``
    
    '''
    def __init__(self, **kwargs):
        self.will_enter_state = kwargs.get('will_enter_state', None)
        self.did_enter_state  = kwargs.get('did_enter_state', None)
        self.will_exit_state  = kwargs.get('will_exit_state', None)
        self.did_exit_state   = kwargs.get('did_exit_state', None)


class State(object):
    '''The class defines a particular state with a state machine. 
    Each state must have a unique name within the state machine in which it is used.
    '''    
    def __init__(self, name, callbacks=None):
        '''Creates and returns a new :class:`State` object with the specified name
 
        :param name: The name of the state. Cannot be blank.
        :param info: An optional object of :class:`StateInfo` type.
        :return: A newly created state object with the specified name.
        '''
        self.name = name
        
        self._will_enter_state = callbacks.will_enter_state if callbacks else None
        self._did_enter_state  = callbacks.did_enter_state if callbacks else None
        self._will_exit_state  = callbacks.will_exit_state if callbacks else None
        self._did_exit_state   = callbacks.did_exit_state if callbacks else None
    
    def __repr__(self):
        return f'<{self.__class__.__name__} {hex(id(self))}> {self.name}'
    
    def __str__(self):
        return f'<{self.__class__.__name__} {self.name}>'
    
    def will_enter(self, transition):
        '''Sets a callback to be executed before the state machine transitions 
        into the state modeled by the receiver; the block has no return value.
        
        :param transition: :class:`Transition` object modeling the state change.
        '''
        if self._will_enter_state:
            self._will_enter_state(transition)
        else:
            # Nothing else to do.
            pass
    
    def did_enter(self, transition):
        '''Sets a block to be executed after the state machine has transitioned 
        into the state modeled by the receiver; the block has no return value
        
        :param transition: :class:`Transition` object modeling the state change.
        '''
        if self._did_enter_state:
            self._did_enter_state(transition)
        else:
            # Nothing else to do.
            pass
    
    def will_exit(self, transition):
        '''Sets a block to be executed before the state machine transitions 
        out of the state modeled by the receiver; the block has no return value.
        
        :param transition: :class:`Transition` object modeling the state change.
        '''
        if self._will_exit_state:
            self._will_exit_state(transition)
        else:
            # Nothing else to do.
            pass
    
    def did_exit(self, transition):
        '''Sets a block to be executed after the state machine has transitioned 
        out of the state modeled by the receiver; the block has no return value.
        
        :param transition: :class:`Transition` object modeling the state change.
        '''
        if self._did_exit_state:
            self._did_exit_state(transition)
        else:
            # Nothing else to do.
            pass
