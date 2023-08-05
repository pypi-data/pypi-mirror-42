# -*- coding: utf-8 -*-
'''
    :copyright: © 2017-2019 by Farhan Ahmed.
    :license: BSD-3-Clause, see LICENSE for more details.
'''

from string import Template

ACTIVATE_EVENT_NAME = 'activate_event'

# Error Identifiers
STATE_NOT_FOUND_IDENTIFIER                              = 'state_not_found'
EVENT_NOT_FOUND_IDENTIFIER                              = 'event_not_found'
STATE_MACHINE_IS_IMMUTABLE_IDENTIFIER                   = 'state_machine_is_immutable'
NOT_ACTIVATED_IDENTIFIER                                = 'not_activated'
INVALID_EVENT_IDENTIFIER                                = 'invalid_event'
DECLINED_EVENT_IDENTIFIER                               = 'declined_event'
DOES_NOT_HAVE_STATES_IDENTIFIER                         = 'does_not_have_states'
DOES_NOT_HAVE_EVENTS_IDENTIFIER                         = 'does_not_have_events'
DOES_NOT_HAVE_INITIAL_STATE_IDENTIFIER                  = 'does_not_have_initial_state'
INITIAL_STATE_MUST_BE_ONE_OF_PROVIDED_STATES_IDENTIFIER = 'initial_state_must_be_one_of_provided_states'
INVALID_EVENT_DESTINATION_STATE_IDENTIFIER              = 'invalid_event_destination_state'
INVALID_EVENT_SOURCE_STATES_IDENTIFIER                  = 'invalid_event_source_states'

STATE_MACHINE_ERROR_MESSAGE_TEMPLATES = {
    STATE_NOT_FOUND_IDENTIFIER: Template('State `$state` was not found.'),
    EVENT_NOT_FOUND_IDENTIFIER: Template('Event `$event` was not found.'),
    STATE_MACHINE_IS_IMMUTABLE_IDENTIFIER: 'The state machine is immutable.',
    NOT_ACTIVATED_IDENTIFIER: 'Not activated.',
    INVALID_EVENT_IDENTIFIER: Template('Event `$event` is not a valid event for the current state; which is `$state`.'),
    DECLINED_EVENT_IDENTIFIER: Template('Event `$event` was declined for the current state; which is `$state`.'),
    DOES_NOT_HAVE_STATES_IDENTIFIER: 'At least one state is required for the state machine.',
    DOES_NOT_HAVE_EVENTS_IDENTIFIER: 'At least one event is required for the state machine.',
    DOES_NOT_HAVE_INITIAL_STATE_IDENTIFIER: 'An initial state is required for the state machine.',
    INITIAL_STATE_MUST_BE_ONE_OF_PROVIDED_STATES_IDENTIFIER: Template('The initial state must be one of the defined states. Available states are: $states'),
    INVALID_EVENT_DESTINATION_STATE_IDENTIFIER: Template('$event does not have valid destination state. A valid destination state is require for an event.'),
    INVALID_EVENT_SOURCE_STATES_IDENTIFIER: Template('All states must be of type `State`. The following states are invalid: $states.')
}
