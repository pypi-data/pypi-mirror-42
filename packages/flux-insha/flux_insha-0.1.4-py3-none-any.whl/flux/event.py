# -*- coding: utf-8 -*-
'''
    :copyright: © 2017-2019 by Farhan Ahmed.
    :license: BSD-3-Clause, see LICENSE for more details.
'''

from .state  import State
from .errors import StateMachineEventError
from .       import constants as STATE_MACHINE

class EventCallbacks:
    '''A data object used for passing callbacks to the :class:`Event` constructor.
    Following callback keywords are supported:
    
    - ``should_fire_event``
    - ``will_fire_event``
    - ``did_fire_event``
    '''
    def __init__(self, **kwargs):
        self.should_fire_event = kwargs.get('should_fire_event', None)
        self.will_fire_event   = kwargs.get('will_fire_event', None)
        self.did_fire_event    = kwargs.get('did_fire_event', None)

class Event(object):
    '''The class describes an event within a state machine 
    that causes a transition between states. Each event has a descriptive 
    name and specifies the state that the machine will transition into after 
    the event has been fired. Events can optionally be constrained to a set 
    of source states that the machine must be in for the event to fire.
    '''
    
    def __init__(self, name, source_states, destination_state, callbacks=None):
        '''Creates and returns a new event object with the given name, source states, 
        and destination state.
        
        :param name: The name of the event.
        :param source_states: An array of :class:`State` objects specifying the source states 
                             that the machine must be in for the event to be permitted 
                             to fire.
        :param destination_state: The state that the state machine will transition into 
                                 after the event has fired.
        :param callbacks: An optional dictionary of callbacks for the event.
        
        :return: A newly created event object.
        '''
        
        if name is None or len(name) == 0:
            raise StateMachineEventError(STATE_MACHINE.INVALID_EVENT_IDENTIFIER)
        
        if destination_state is None or not isinstance(destination_state, State):
            raise StateMachineEventError(STATE_MACHINE.INVALID_EVENT_DESTINATION_STATE_IDENTIFIER, 
                                         substitute={'event': name})
        
        invalid_states = [f'{state} ({type(state).__name__})' for state in source_states if not isinstance(state, State)]
        
        if len(invalid_states) > 0:
            raise StateMachineEventError(STATE_MACHINE.INVALID_EVENT_SOURCE_STATES_IDENTIFIER,
                                         substitute={'states': invalid_states})
        
        self.name               = name
        self.source_states      = set(source_states)
        self.destination_state  = destination_state
        self._should_fire_event = callbacks.should_fire_event if callbacks else None
        self._will_fire_event   = callbacks.will_fire_event if callbacks else None
        self._did_fire_event    = callbacks.did_fire_event if callbacks else None
    
    def __repr__(self):
        return f'<{self.__class__.__name__} {hex(id(self))}> {self.name}'
    
    def __str__(self):
        return f'<{self.__class__.__name__} {self.name}>'
    
    def should_fire(self, transition):
        '''Sets a callback to be executed in order to determines if an event 
        should be fired. If the block returns ``YES``, then the event will 
        be permitted to fire.
        
        :param transition: The associated :class:`Transition` with the event.
        '''
        fire_event = False
        
        if self._should_fire_event:
            fire_event = self._should_fire_event(transition)
        else:
            # By default all events are allowed
            fire_event = True
        
        return fire_event
    
    def will_fire(self, transition):
        '''Sets a block to be executed before an event is fired, while the 
        state machine is still in the source state; the callback has no return value.
        
        :param transition: The associated :class:`Transition` with the event.
        '''
        if self._will_fire_event:
            self._will_fire_event(transition)
        else:
            # Nothing else to do.
            pass
    
    def did_fire(self, transition):
        '''Sets a block to be executed after an event is fired, when the state 
        machine has transitioned into the destination state; the callback has no 
        return value.
        
        :param transition: The associated :class:`Transition` with event that has just been fired.
        '''
        if self._did_fire_event:
            self._did_fire_event(transition)
        else:
            # Nothing else to do.
            pass
