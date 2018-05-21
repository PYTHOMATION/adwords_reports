#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import logging

# as described here: https://docs.python.org/2/howto/logging.html#configuring-logging-for-a-library
logger = logging.getLogger("adwords_reports")
logger.addHandler(logging.NullHandler())

__version__ = "1.2.2"
app_dir = os.path.dirname(__file__)
base_dir = os.path.dirname(app_dir)

from adwords_reports.client import Client
from adwords_reports.report_definition import ReportDefinition
