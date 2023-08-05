# -*- coding: utf-8 -*-
'''
    :copyright: © 2017-2019 by Farhan Ahmed.
    :license: BSD-3-Clause, see LICENSE for more details.
'''

import pytest

from flux.helpers import slugify

class TestHelpers(object):
    
    def test_creating_a_slug_from_string(self):
        name = 'Some long name for state or event.'
        slug = slugify(name)
        expected = 'some-long-name-for-state-or-event'
        
        assert slug == expected
