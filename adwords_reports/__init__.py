#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

__version__ = "1.1.0"
app_dir = os.path.dirname(__file__)
app_dir_components = app_dir.split(os.sep)
base_dir = os.sep.join(app_dir_components[:-1])

from adwords_reports.client import AdWordsClient
from adwords_reports.report_definition import ReportDefinition
