# -*- coding:utf-8 -*-

from lawes.db.models.base import Model
from lawes.db.models.fields import *
from lawes.db.models.query import configqueryset
from lawes.db.models.query import Q

def setup(conf):
    configqueryset._setup(conf=conf)