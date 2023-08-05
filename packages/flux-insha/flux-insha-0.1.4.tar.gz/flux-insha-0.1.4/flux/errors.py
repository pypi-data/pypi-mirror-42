# -*- coding: utf-8 -*-
'''
    :copyright: © 2017-2019 by Farhan Ahmed.
    :license: BSD-3-Clause, see LICENSE for more details.
'''

from .constants import STATE_MACHINE_ERROR_MESSAGE_TEMPLATES

##############
# Exceptions #
##############
class FluxError(Exception):
    '''Base error class.'''
    def __init__(self, identifier, substitute=None):
        Exception.__init__(self)
        
        self.identifier = identifier
        
        if substitute:
            self.message = STATE_MACHINE_ERROR_MESSAGE_TEMPLATES[identifier].safe_substitute(substitute)
        else:
            self.message = STATE_MACHINE_ERROR_MESSAGE_TEMPLATES[identifier]
    
    def __repr__(self):
        return f'<{self.__class__.__name__} {hex(id(self))} {self.identifier.upper()}: {self.message}>'
    
    def __str__(self):
        return f'{self.identifier.upper()}: {self.message}'

class StateMachineError(FluxError):
    def __init__(self, identifier, substitute=None):
        super(StateMachineError, self).__init__(identifier, substitute)

class StateMachineEventError(FluxError):
    def __init__(self, identifier, substitute=None):
        super(StateMachineEventError, self).__init__(identifier, substitute)

class StateMachineStateError(FluxError):
    def __init__(self, identifier, substitute=None):
        super(StateMachineStateError, self).__init__(identifier, substitute)
