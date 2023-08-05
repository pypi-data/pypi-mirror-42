# -*- coding: utf-8 -*-
'''
    :copyright: © 2017-2019 by Farhan Ahmed.
    :license: BSD-3-Clause, see LICENSE for more details.
'''

from .state      import State
from .event      import Event
from .transition import Transition
from .errors     import StateMachineError, StateMachineEventError
from .           import constants as STATE_MACHINE

class StateMachine:
    '''The class provides an interface for modeling a state machine. The state machine 
    supports the registration of an arbitrary number of states and events that trigger 
    transitions between the states.

    When a state machine is activated, the following callbacks are invoked:

    #. Initial State: ``will_enter_state``: The callback set on the ``initial_state`` is invoked.
    #. The ``current_state`` changes from ``None`` to ``initial_state``.
    #. Initial State: ``did_enter_state``: The callback set on the ``initial_state`` is invoked.

    Each time an event is fired, the following callbacks are invoked:

    #. ``should_fire_event``: The callback set on the event being fired is consulted to determine if the event can be fired. If ``False`` is returned then the event is declined and no further callbacks are invoked
    #. ``will_fire_event``: The callback set on the event being fired is invoked.
    #. ``will_exit_state`` (Old State): The callback set on the outgoing state is invoked.
    #. ``will_enter_state`` (New State): The callback set on the incoming state is invoked.
    #. The ``current_state`` changes from the old state to the new state.
    #. ``did_exit_state`` (Old State): The callback set on the old state is invoked.
    #. ``did_enter_state`` (New State): The callback set on the new current state is invoked.
    #. ``did_fire_event``: The callback set on the event being fired is invoked.
    '''
    states        = None
    events        = None
    initial_state = None
    is_active     = False
    
    # Private
    _current_state                        = None
    _did_change_state_transition_info_key = {}
    
    def __init__(self, states=None, events=None, initial_state=None):
        '''Initialize the state machine'''
        
        if states is None or len(states) == 0:
            raise StateMachineError(STATE_MACHINE.DOES_NOT_HAVE_STATES_IDENTIFIER)
        
        if events is None or len(events) == 0:
            raise StateMachineError(STATE_MACHINE.DOES_NOT_HAVE_EVENTS_IDENTIFIER)
        
        if initial_state is None:
            raise StateMachineError(STATE_MACHINE.DOES_NOT_HAVE_INITIAL_STATE_IDENTIFIER)
        
        if initial_state not in set(states):
            states = ', '.join([state.name for state in states])
            raise StateMachineError(STATE_MACHINE.INITIAL_STATE_MUST_BE_ONE_OF_PROVIDED_STATES_IDENTIFIER,
                                    substitute={'states': states})
        
        self.states                                = set(states)
        self.events                                = set(events)
        self.initial_state                         = initial_state
        self.is_active                             = False
        self._current_state                        = None
        self._did_change_state_transition_info_key = {}
    
    @property
    def current_state(self):
        '''Returns the current state for the state machine.'''
        return self._current_state
    
    @current_state.setter
    def current_state(self, state):
        if state:
            self._current_state = state
        else:
            # Nothing to do since a valid
            # state was not provided.
            pass
    
    def state_by_name(self, name):
        '''Look up a state by name.
        
        :param name:  Name of the state.
        
        :raises:      ``state_not_found`` when a state is not found.
        :return:      An instance of ``State``, when there's a match.
        '''
        found_state = [state for state in self.states if state.name == name]
        
        if len(found_state) == 0:
            raise StateMachineError(STATE_MACHINE.STATE_NOT_FOUND_IDENTIFIER, substitute={'state': name})
        
        return found_state[0]
    
    def in_state_by_name(self, name):
        '''Determines if the state machine is in the provided state.
        
        :param name:   Name of the state.
        
        :return:       True if matched otherwise False.
        '''
        is_in_state = False
        
        try:
            state = self.state_by_name(name)
            is_in_state = state == self.current_state
        except StateMachineError as e:
            # Nothing to do, the return value is already
            # initialized to False
            raise
        
        return is_in_state
    
    def in_state(self, state):
        '''Determines if the state machine in the provided state.
        This is a convenience method for the ``in_state_by_name``.
        
        :param state:  An instance of the State object.
        
        :return:       True if matched otherwise False.
        '''
        return self.in_state_by_name(state.name)
    
    def event_by_name(self, name):
        '''Look up a event by name.
        
        :param name:  Name of the event.
        :raises:      ``event_not_found`` when a event is not found.
        
        :return:      An instance of ``Event``, when there's a match.
        '''
        found_event = [event for event in self.events if event.name == name]
        
        if len(found_event) == 0:
            raise StateMachineError(STATE_MACHINE.EVENT_NOT_FOUND_IDENTIFIER, substitute={'event': name})
        
        return found_event[0]
    
    def activate(self):
        '''Activates the state machine'''
        if not self.is_active:            
            initial_event = Event(name='activate_event', 
                                  source_states=[self.initial_state],
                                  destination_state=self.initial_state)            
            transition    = Transition(event=initial_event, 
                                       source_state=self.initial_state, 
                                       state_machine=self, 
                                       user_info={})
            
            self._trigger_transition_block(kind=self.initial_state, transition=transition, block=self.initial_state.will_enter)
            self._trigger_transition_block(kind=self.initial_state, transition=transition, block=self.initial_state.did_enter)
            
            self.current_state = self.initial_state
            self.is_active     = True
        else:
            # State machine has been activated already.
            # Nothing else needs to be done.
            pass
    
    # Triggering Events
    
    def can_fire_event_with_name(self, name):
        '''Returns a Boolean value that indicates if the specified event can be fired.
        
        * If the ``source_states`` of the event is ``None``, then the event can be fired from any state.
        * If the ``sources_states`` is not ``None``, then the event can only be fired if it includes the `current_state` of the receiver.
        
        :param name: A string that identifies an event by name. The source states of the 
                     specified event is compared with the current state of the receiver.
        
        :returns: ``True`` if the event can be fired, otherwise ``False``.
        '''
        should_trigger_event = False
        
        if self.is_active and self.current_state is not None:
            try:
                event = self.event_by_name(name)
                
                can_fire_in_all_states    = len(event.source_states) == 0
                can_fire_in_current_state = self.current_state in event.source_states
                
                should_trigger_event = can_fire_in_all_states or can_fire_in_current_state
            except StateMachineError as e:
                # Nothing to do here, the return
                # value is already initialized to False
                raise
        else:
            # Nothing to do here
            pass
        
        return should_trigger_event
    
    def can_fire_event(self, event):
        '''This is a convenience method for the :meth:`can_fire_event_with_name`'''
        return self.can_fire_event_with_name(event.name)
    
    def fire_event_with_name(self, name, user_info=None):
        '''Returns a Boolean value that indicates if the specified event was fired.
        The state machine must be activated and it must be in a proper state.
        
        :param name: A string that identifies an event by name. The source states of the 
                     specified event is compared with the current state of the receiver.
        :param user_info: An optional dictionary of user info.
        
        :raises: When the event cannot be fired (the :meth:`can_fire_event` returns ``False``) for the ``current_state``; an error is raised of type :class:`StateMachineEventError` with its identifier set to ``invalid_event``.
        :raises: When the :meth:`should_fire` method returns ``False`` for the event; an error is raised of type :class:`StateMachineEventError` with its identifier set to ``declined_event``
        
        :returns: ``True`` if the event can be fired, otherwise ``False``.
        '''
        did_fire_event = False
        
        if self.is_active and self.current_state is not None:
            try:
                event = self.event_by_name(name)
                
                if self.can_fire_event(event):                    
                    transition = Transition(event=event, 
                                            source_state=self.current_state, 
                                            state_machine=self, 
                                            user_info=user_info)
                    
                    if event.should_fire(transition):
                        did_fire_event = self._trigger_transitions(event=event, state=self.current_state, transition=transition)
                    else:
                        raise StateMachineEventError(STATE_MACHINE.DECLINED_EVENT_IDENTIFIER, 
                                                     substitute={'event': event.name, 'state': self.current_state.name})
                else:
                    raise StateMachineEventError(STATE_MACHINE.INVALID_EVENT_IDENTIFIER, 
                                                 substitute={'event': event.name, 'state': self.current_state.name})
            except StateMachineEventError as e:
                # Nothing to do here, the return
                # value is already initialized to False
                raise
        else:
             # Nothing to do here
            pass
        
        return did_fire_event
    
    def fire_event(self, event, user_info=None):
        '''This is a convenience method for the ``fire_event_with_name``'''
        did_fire_event = False
        
        try:
            did_fire_event = self.fire_event_with_name(event.name, user_info=user_info)
        except StateMachineEventError as e:
            raise
        
        return did_fire_event
    
    # Helpers
    
    def _trigger_transitions(self, event=None, state=None, transition=None):
        old_state = state
        new_state = event.destination_state
        
        self._trigger_transition_block(kind=event, transition=transition, block=event.will_fire)
        self._trigger_transition_block(kind=old_state, transition=transition, block=old_state.will_exit)
        self._trigger_transition_block(kind=new_state, transition=transition, block=new_state.will_enter)
        
        self.current_state = new_state
        
        self._trigger_transition_block(kind=old_state, transition=transition, block=old_state.did_exit)
        self._trigger_transition_block(kind=new_state, transition=transition, block=new_state.did_enter)
        self._trigger_transition_block(kind=event, transition=transition, block=event.did_fire)
        
        if old_state != new_state:
            # TODO: Fire a notification for changing of state
            pass
        else:
            # No notification needs to be fired since
            # the state has not changed.
            pass
        
        return True
    
    def _trigger_transition_block(self, kind=None, transition=None, block=None):
        '''Executes a block'''
        if block:
            block(transition)
        else:
            # Nothing to do. Move along.
            pass
