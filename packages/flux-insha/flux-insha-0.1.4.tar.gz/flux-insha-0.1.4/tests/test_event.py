# -*- coding: utf-8 -*-
'''
    :copyright: © 2017-2019 by Farhan Ahmed.
    :license: BSD-3-Clause, see LICENSE for more details.
'''

import pytest
import re

from unittest.mock import Mock
from flux.machine import StateMachine
from flux.state  import State
from flux.event  import Event, EventCallbacks
from flux.errors import StateMachineEventError
from flux        import constants as STATE_MACHINE

class TestEvent(object):
    
    def test_initializing_event_successfully(self):
        start_state = State(name='start')
        busy_state  = State(name='busy')
        do_work_event = Event(name='do_work', source_states=[start_state], destination_state=busy_state)
        
        assert do_work_event.name == 'do_work'
    
    def test_event_object_str_method(self):
        start_state = State(name='start')
        busy_state  = State(name='busy')
        do_work_event = Event(name='Do Work', source_states=[start_state], destination_state=busy_state)
        
        assert str(do_work_event) == '<Event Do Work>'
    
    def test_event_object_repr_method(self):
        start_state = State(name='start')
        busy_state  = State(name='busy')
        do_work_event = Event(name='Do Work', source_states=[start_state], destination_state=busy_state)
        pattern    = re.compile(r'\s0x.[a-z0-9]*')
        match      = pattern.search(do_work_event.__repr__())
        result     = do_work_event.__repr__().replace(match.group(0), '')
        
        assert result == '<Event> Do Work'
    
    def test_initializing_event_failure_with_invalid_event(self):
        with pytest.raises(StateMachineEventError) as context:
            do_work_event = Event(name='', source_states=[], destination_state=None)
        
        expected_exception = context.value
        
        assert expected_exception.identifier == STATE_MACHINE.INVALID_EVENT_IDENTIFIER
    
    def test_initializing_event_failure_with_invalid_destination_state(self):
        start_state = State(name='start')
        
        with pytest.raises(StateMachineEventError) as context:
            do_work_event = Event(name='do_work', source_states=[start_state], destination_state=None)
        
        expected_exception = context.value
        
        assert expected_exception.identifier == STATE_MACHINE.INVALID_EVENT_DESTINATION_STATE_IDENTIFIER
    
    def test_initializing_event_failure_with_invalid_source_state(self):
        start_state = State(name='start')
        busy_state  = State(name='busy')
        
        with pytest.raises(StateMachineEventError) as context:
            do_work_event = Event(name='do_work', 
                                  source_states=['A', 'B', start_state], 
                                  destination_state=busy_state)
        
        expected_exception = context.value
        
        assert expected_exception.identifier == STATE_MACHINE.INVALID_EVENT_SOURCE_STATES_IDENTIFIER

    def test_event_should_fire_callback(self):
        start_state = State(name='start')
        busy_state  = State(name='busy')
        
        def should_fire_callback(transition):
            return True
        
        do_work_info  = EventCallbacks(should_fire_event=should_fire_callback)
        do_work_event = Event(name='do_work', 
                              source_states=[start_state], 
                              destination_state=busy_state, 
                              callbacks=do_work_info)
        
        fsm = StateMachine(states=set([start_state, busy_state]), 
                           events=set([do_work_event]), 
                           initial_state=start_state)
        
        fsm.activate()
        
        assert fsm.is_active
        assert fsm.fire_event(do_work_event)

    def test_event_will_fire_callback(self):
        start_state = State(name='start')
        busy_state  = State(name='busy')
        will_fire_mock = Mock()
        
        do_work_info  = EventCallbacks(will_fire_event=will_fire_mock)
        do_work_event = Event(name='do_work', 
                              source_states=[start_state], 
                              destination_state=busy_state, callbacks=do_work_info)
        
        fsm = StateMachine(states=set([start_state, busy_state]), 
                           events=set([do_work_event]), 
                           initial_state=start_state)
        
        fsm.activate()
        
        assert fsm.is_active
        assert fsm.fire_event(do_work_event)
        will_fire_mock.assert_called()
    
    def test_event_did_fire_callback(self):
        start_state = State(name='start')
        busy_state  = State(name='busy')
        did_fire_mock = Mock()
        
        do_work_info  = EventCallbacks(did_fire_event=did_fire_mock)
        do_work_event = Event(name='do_work', 
                              source_states=[start_state], 
                              destination_state=busy_state, 
                              callbacks=do_work_info)
        
        fsm = StateMachine(states=set([start_state, busy_state]), 
                           events=set([do_work_event]), 
                           initial_state=start_state)
        
        fsm.activate()
        
        assert fsm.is_active
        assert fsm.fire_event(do_work_event)
        did_fire_mock.assert_called()
