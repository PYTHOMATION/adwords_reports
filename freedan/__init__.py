#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os


__version__ = "0.1.7"

base_dir = os.path.dirname(__file__)  # deepest freedan folder

from freedan.adwords_objects.account import Account
from freedan.adwords_objects.account_label import AccountLabel
from freedan.adwords_objects.campaign import Campaign
from freedan.adwords_objects.campaign_budget import CampaignBudget
from freedan.adwords_objects.adgroup import AdGroup
from freedan.adwords_objects.keyword import Keyword
from freedan.adwords_objects.keyword_final_url import KeywordFinalUrl
from freedan.adwords_objects.negative_keyword import NegativeKeyword
from freedan.adwords_objects.label import Label
from freedan.adwords_objects.extended_text_ad import ExtendedTextAd
from freedan.adwords_objects.shared_set_overview import SharedSetOverview

from freedan.adwords_services.adwords_service import AdWordsService
from freedan.adwords_services.batch_uploader import BatchUploader
from freedan.adwords_services.standard_uploader import StandardUploader
from freedan.adwords_services.adwords_error import AdWordsError

from freedan.other_services.text_handler import TextHandler
