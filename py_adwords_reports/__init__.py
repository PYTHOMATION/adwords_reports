#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

__version__ = "1.0.0"
app_dir = os.path.dirname(__file__)
app_dir_components = app_dir.split(os.sep)
base_dir = os.sep.join(app_dir_components[:-1])

from py_adwords_reports.client import AdWordsClient
from py_adwords_reports.handler_reports import ReportDefinition
