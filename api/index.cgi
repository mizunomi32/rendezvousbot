#!/usr/bin/python3.5
# -*- encoding: utf-8 -*-

from wsgiref.handlers import CGIHandler
from main import app

CGIHandler().run(app)
