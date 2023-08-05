# -*- coding: utf-8 -*-
'''
    :copyright: © 2017-2019 by Farhan Ahmed.
    :license: BSD-3-Clause, see LICENSE for more details.
'''

import pytest
import re

from flux.errors import StateMachineStateError
from flux        import constants as STATE_MACHINE

class TestError(object):
    def test_event_object_str_method(self):
        identifier  = STATE_MACHINE.STATE_NOT_FOUND_IDENTIFIER
        state_error = StateMachineStateError(identifier)
        message     = STATE_MACHINE.STATE_MACHINE_ERROR_MESSAGE_TEMPLATES[identifier]
        expecting_result = f'{identifier.upper()}: {message}'
        
        assert str(state_error) == expecting_result
    
    def test_event_object_repr_method(self):
        identifier  = STATE_MACHINE.STATE_NOT_FOUND_IDENTIFIER
        state_error = StateMachineStateError(identifier)
        message     = STATE_MACHINE.STATE_MACHINE_ERROR_MESSAGE_TEMPLATES[identifier]
        expecting_result = f'<StateMachineStateError {identifier.upper()}: {message}>'
        pattern    = re.compile(r'\s0x.[a-z0-9]*')
        match      = pattern.search(state_error.__repr__())
        result     = state_error.__repr__().replace(match.group(0), '')

        assert result == expecting_result
