# -*- coding: utf-8 -*-
'''
    :copyright: © 2017-2019 by Farhan Ahmed.
    :license: BSD-3-Clause, see LICENSE for more details.
'''

import pytest

from flux.machine import StateMachine
from flux.state import State
from flux.event import Event, EventCallbacks
from flux.transition import Transition
from flux.errors import StateMachineError, StateMachineEventError
from flux import constants as STATE_MACHINE

class TestStateMachine(object):
    
    def test_activate_state_machine_successfully(self):
        start_state = State(name='start')
        busy_state  = State(name='busy')
        do_work_event = Event(name='do_work', source_states=[start_state], destination_state=busy_state)
        
        fsm = StateMachine(states=[start_state, busy_state], 
                           events=[do_work_event], 
                           initial_state=start_state)
        
        fsm.activate()
        
        assert fsm.is_active

    def test_initialize_state_machine_with_invalid_states(self):
        busy_state  = State(name='busy')
        do_work_event = Event(name='do_work', source_states=[busy_state], destination_state=busy_state)
        
        with pytest.raises(StateMachineError) as context_manager:
            fsm = StateMachine(states=[], events=[do_work_event], initial_state=busy_state)
        
        expected_exception = context_manager.value
        assert expected_exception.identifier == STATE_MACHINE.DOES_NOT_HAVE_STATES_IDENTIFIER
    
    def test_initialize_state_machine_with_invalid_events(self):
        start_state = State(name='start')
        
        with pytest.raises(StateMachineError) as context_manager:
            fsm = StateMachine(states=[start_state], events=[], initial_state=start_state)
        
        expected_exception = context_manager.value
        assert expected_exception.identifier == STATE_MACHINE.DOES_NOT_HAVE_EVENTS_IDENTIFIER

    def test_initialize_state_machine_with_invalid_intial_state(self):
        start_state = State(name='start')
        do_work_event = Event(name='do_work', source_states=[start_state], destination_state=start_state)
        
        with pytest.raises(StateMachineError) as context_manager:
            fsm = StateMachine(states=[start_state], events=[do_work_event], initial_state=None)
        
        expected_exception = context_manager.value
        assert expected_exception.identifier == STATE_MACHINE.DOES_NOT_HAVE_INITIAL_STATE_IDENTIFIER

    def test_initial_state_is_not_a_valid_state(self):
        start_state = State(name='start')
        busy_state  = State(name='busy')
        do_work_event = Event(name='do_work', source_states=[start_state], destination_state=busy_state)
        
        with pytest.raises(StateMachineError) as context_manager:
            fsm = StateMachine(states=[start_state], events=[do_work_event], initial_state=busy_state)
        
        expected_exception = context_manager.value
        assert expected_exception.identifier == STATE_MACHINE.INITIAL_STATE_MUST_BE_ONE_OF_PROVIDED_STATES_IDENTIFIER
    
    def test_looking_up_state_by_name_sucessfully(self):
        start_state = State(name='start')
        busy_state  = State(name='busy')
        do_work_event = Event(name='do_work', source_states=[start_state], destination_state=busy_state)
        
        fsm = StateMachine(states=[start_state, busy_state], events=[do_work_event], initial_state=start_state)
        
        found_state = fsm.state_by_name('busy')
        
        assert found_state == busy_state
    
    def test_looking_up_state_by_name_returning_not_found(self):
        start_state = State(name='start')
        do_work_event = Event(name='do_work', source_states=[start_state], destination_state=start_state)
        
        fsm = StateMachine(states=[start_state], events=[do_work_event], initial_state=start_state)
        
        with pytest.raises(StateMachineError) as context_manager:
            fsm.state_by_name('busy')
        
        expected_exception = context_manager.value
        assert expected_exception.identifier == STATE_MACHINE.STATE_NOT_FOUND_IDENTIFIER
    
    def test_looking_up_event_by_name_successfully(self):
        start_state = State(name='start')
        busy_state  = State(name='busy')
        do_work_event = Event(name='do_work', source_states=[start_state], destination_state=busy_state)
        
        fsm = StateMachine(states=[start_state, busy_state], events=[do_work_event], initial_state=start_state)
        
        found_event = fsm.event_by_name('do_work')
        
        assert found_event == do_work_event
    
    def test_looking_up_event_by_name_returning_not_found(self):
        start_state = State(name='start')
        busy_state  = State(name='busy')
        do_work_event = Event(name='do_work', source_states=[start_state], destination_state=busy_state)
        
        fsm = StateMachine(states=[start_state, busy_state], events=[do_work_event], initial_state=start_state)
        
        with pytest.raises(StateMachineError) as context_manager:
            found_event = fsm.event_by_name('more_work')
        
        expected_exception = context_manager.value
        assert expected_exception.identifier == STATE_MACHINE.EVENT_NOT_FOUND_IDENTIFIER
    
    def test_can_fire_event_with_name_successfully(self):
        start_state = State(name='start')
        busy_state  = State(name='busy')
        do_work_event = Event(name='do_work', source_states=[start_state], destination_state=busy_state)
        
        fsm = StateMachine(states=[start_state, busy_state], events=[do_work_event], initial_state=start_state)
        fsm.activate()
        
        assert fsm.can_fire_event_with_name('do_work')
    
    def test_can_fire_event_with_name_failure(self):
        start_state = State(name='start')
        busy_state  = State(name='busy')
        do_work_event = Event(name='do_work', source_states=[busy_state], destination_state=busy_state)
        
        fsm = StateMachine(states=[start_state, busy_state], events=[do_work_event], initial_state=start_state)
        fsm.activate()
        
        assert fsm.can_fire_event_with_name('do_work') == False
    
    def test_can_fire_event_with_name_failure_with_invalid_event(self):
        start_state = State(name='start')
        busy_state  = State(name='busy')
        do_work_event = Event(name='do_work', source_states=[busy_state], destination_state=busy_state)
        
        fsm = StateMachine(states=[start_state, busy_state], events=[do_work_event], initial_state=start_state)
        fsm.activate()
        
        with pytest.raises(StateMachineError) as context:
            fsm.can_fire_event_with_name('no_work')
        
        expected_exception = context.value
        assert expected_exception.identifier == STATE_MACHINE.EVENT_NOT_FOUND_IDENTIFIER
    
    def test_firing_event_with_name_successfully(self):
        start_state = State(name='start')
        busy_state  = State(name='busy')
        do_work_event = Event(name='do_work', source_states=[start_state], destination_state=busy_state)
        
        fsm = StateMachine(states=[start_state, busy_state], events=[do_work_event], initial_state=start_state)
        fsm.activate()
        
        assert fsm.fire_event_with_name('do_work')
    
    def test_firing_event_with_name_that_is_declined(self):
        
        def decline_event(transition):
            return False
        
        start_state = State(name='start')
        busy_state  = State(name='busy')
        
        do_work_info  = EventCallbacks(should_fire_event=decline_event)
        do_work_event = Event(name='do_work', 
                              source_states=[start_state], 
                              destination_state=busy_state, 
                              callbacks=do_work_info)
        
        fsm = StateMachine(states=[start_state, busy_state], events=[do_work_event], initial_state=start_state)
        fsm.activate()
        
        with pytest.raises(StateMachineEventError) as context_manager:
            fsm.fire_event_with_name('do_work')
        
        expected_exception = context_manager.value
        assert expected_exception.identifier == STATE_MACHINE.DECLINED_EVENT_IDENTIFIER
    
    def test_firing_event_with_name_with_invalid_event_name(self):
        start_state = State(name='start')
        busy_state  = State(name='busy')
        do_work_event = Event(name='do_work', source_states=[start_state], destination_state=busy_state)
        
        fsm = StateMachine(states=[start_state, busy_state], events=[do_work_event], initial_state=busy_state)
        fsm.activate()
        
        with pytest.raises(StateMachineEventError) as context:
            fsm.fire_event_with_name('do_work')
        
        expected_exception = context.value
        assert expected_exception.identifier == STATE_MACHINE.INVALID_EVENT_IDENTIFIER
    
    def test_firing_event_successfully(self):
        start_state = State(name='start')
        busy_state  = State(name='busy')
        do_work_event = Event(name='do_work', source_states=[start_state], destination_state=busy_state)
        
        fsm = StateMachine(states=[start_state, busy_state], events=[do_work_event], initial_state=start_state)
        fsm.activate()
        
        assert fsm.fire_event(do_work_event)
    
    def test_firing_event_that_is_declined(self):
        
        def decline_event(transition):
            return False
        
        start_state = State(name='start')
        busy_state  = State(name='busy')
        
        do_work_info  = EventCallbacks(should_fire_event=decline_event)
        do_work_event = Event(name='do_work',
                              source_states=[start_state], 
                              destination_state=busy_state, 
                              callbacks=do_work_info)
        
        fsm = StateMachine(states=[start_state, busy_state], events=[do_work_event], initial_state=start_state)
        fsm.activate()
        
        with pytest.raises(StateMachineEventError) as context_manager:
            fsm.fire_event(do_work_event)
        
        expected_exception = context_manager.value
        assert expected_exception.identifier == STATE_MACHINE.DECLINED_EVENT_IDENTIFIER
    
    def test_in_state_by_name_for_a_valid_current_state(self):
        start_state = State(name='start')
        busy_state  = State(name='busy')
        do_work_event = Event(name='do_work', source_states=[start_state], destination_state=busy_state)
        
        fsm = StateMachine(states=set([start_state, busy_state]), 
                           events=set([do_work_event]), 
                           initial_state=start_state)
        
        fsm.activate()
        
        assert fsm.in_state_by_name('start')
    
    def test_in_state_by_name_for_wrong_current_state(self):
        start_state = State(name='start')
        busy_state  = State(name='busy')
        do_work_event = Event(name='do_work', source_states=[start_state], destination_state=busy_state)
        
        fsm = StateMachine(states=set([start_state, busy_state]), 
                           events=set([do_work_event]), 
                           initial_state=start_state)
        
        fsm.activate()
        
        assert fsm.in_state_by_name('busy') == False
    
    def test_in_state_by_name_for_an_invalid_state(self):
        start_state = State(name='start')
        busy_state  = State(name='busy')
        do_work_event = Event(name='do_work', source_states=[start_state], destination_state=busy_state)
        
        fsm = StateMachine(states=set([start_state, busy_state]), 
                           events=set([do_work_event]), 
                           initial_state=start_state)
        
        fsm.activate()
        
        with pytest.raises(StateMachineError) as context:
            fsm.in_state_by_name('stop')
        
        expected_exception = context.value
        assert expected_exception.identifier == STATE_MACHINE.STATE_NOT_FOUND_IDENTIFIER
    
    def test_state_machine_is_in_correct_state(self):
        start_state = State(name='start')
        busy_state  = State(name='busy')
        do_work_event = Event(name='do_work', source_states=[start_state], destination_state=busy_state)
        
        fsm = StateMachine(states=set([start_state, busy_state]), 
                           events=set([do_work_event]), 
                           initial_state=start_state)
        
        fsm.activate()
        
        assert fsm.in_state(start_state)
