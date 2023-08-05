# -*- coding: utf-8 -*-
'''
    :copyright: © 2017-2019 by Farhan Ahmed.
    :license: BSD-3-Clause, see LICENSE for more details.
'''

import pytest
import re

from unittest.mock import Mock
from flux.machine import StateMachine
from flux.state  import State, StateCallbacks
from flux.event  import Event
from flux.errors import StateMachineStateError
from flux        import constants as STATE_MACHINE

class TestState(object):

    def test_initializing_state_successfully(self):
        some_state = State(name='a_state')

        assert some_state.name == 'a_state'

    def test_state_object_str_method(self):
        some_state = State(name='Busy')

        assert str(some_state) == '<State Busy>'

    def test_state_object_repr_method(self):
        some_state = State(name='Busy')
        pattern    = re.compile(r'\s0x.[a-z0-9]*')
        match      = pattern.search(some_state.__repr__())
        result     = some_state.__repr__().replace(match.group(0), '')

        assert result == '<State> Busy'

    def test_initializing_state_info_without_any_callbacks(self):
        info = StateCallbacks()

        assert info.will_enter_state == None
        assert info.did_enter_state == None
        assert info.will_exit_state == None
        assert info.did_exit_state == None

    def test_will_enter_state_callback_is_invoked(self):
        will_enter_mock = Mock()
        callbacks = StateCallbacks(will_enter_state=will_enter_mock)
        start_state = State(name='start', callbacks=callbacks)
        busy_state  = State(name='busy')
        do_work_event = Event(name='do_work', source_states=[start_state], destination_state=busy_state)

        fsm = StateMachine(states=[start_state, busy_state],
                           events=[do_work_event],
                           initial_state=start_state)

        fsm.activate()

        will_enter_mock.assert_called()

    def test_did_enter_state_callback_is_invoked(self):
        did_enter_mock = Mock()
        callbacks = StateCallbacks(did_enter_state=did_enter_mock)
        start_state = State(name='start', callbacks=callbacks)
        busy_state  = State(name='busy')
        do_work_event = Event(name='do_work', source_states=[start_state], destination_state=busy_state)

        fsm = StateMachine(states=[start_state, busy_state],
                           events=[do_work_event],
                           initial_state=start_state)

        fsm.activate()

        did_enter_mock.assert_called()

    def test_will_exit_state_callback_is_invoked(self):
        will_exit_mock = Mock()
        callbacks = StateCallbacks(will_exit_state=will_exit_mock)
        start_state = State(name='start', callbacks=callbacks)
        busy_state  = State(name='busy')
        do_work_event = Event(name='do_work', source_states=[start_state], destination_state=busy_state)

        fsm = StateMachine(states=[start_state, busy_state],
                           events=[do_work_event],
                           initial_state=start_state)

        fsm.activate()
        fsm.fire_event(do_work_event)

        will_exit_mock.assert_called()

    def test_did_exit_state_callback_is_invoked(self):
        did_exit_mock = Mock()
        callbacks = StateCallbacks(did_exit_state=did_exit_mock)
        start_state = State(name='start', callbacks=callbacks)
        busy_state  = State(name='busy')
        do_work_event = Event(name='do_work', source_states=[start_state], destination_state=busy_state)

        fsm = StateMachine(states=[start_state, busy_state],
                           events=[do_work_event],
                           initial_state=start_state)

        fsm.activate()
        fsm.fire_event(do_work_event)

        did_exit_mock.assert_called()
