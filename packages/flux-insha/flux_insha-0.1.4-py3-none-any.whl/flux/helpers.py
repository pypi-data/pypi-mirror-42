# -*- coding: utf-8 -*-
'''
    :copyright: © 2017-2019 by Farhan Ahmed.
    :license: BSD-3-Clause, see LICENSE for more details.
'''

import re

def slugify(value=None):
    slug = u'%s' % value
    slug = re.sub(r'[^\w\s-]', '', slug).strip().lower()
    slug = str(re.sub(r'[-\s]+', '-', slug))
    
    return slug
