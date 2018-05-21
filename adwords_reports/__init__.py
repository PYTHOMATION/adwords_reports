#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

__version__ = "1.2.1"
app_dir = os.path.dirname(__file__)
base_dir = os.path.dirname(app_dir)

from adwords_reports.client import Client
from adwords_reports.report_definition import ReportDefinition
