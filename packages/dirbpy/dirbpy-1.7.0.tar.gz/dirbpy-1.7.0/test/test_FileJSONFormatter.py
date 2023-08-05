#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
sys.path.append('src')

from unittest.mock import MagicMock
from unittest import mock

from _dirbpy.main import GENERATED_WORD_MESSAGE 
from _dirbpy.FileJSONFormatter import FileJSONFormatter
from _dirbpy.URLBruteforcer import URLBruteforcer

def test_GivenMessage_WhenGetURLWithHTTPFromMessage_ThenURLIsReturned():
    url = "http://mysite.dirbpy"
    message = URLBruteforcer.SCANNING_URL_MESSAGE.format(url)
    formatter = FileJSONFormatter()
    actual_url = formatter.get_url_from_message(message)
    assert url == actual_url

def test_GivenMessage_WhenGetURLWithHTTPSFromMessage_ThenURLIsReturned():
    url = "https://mysite.dirbpy"
    message = URLBruteforcer.SCANNING_URL_MESSAGE.format(url)
    formatter = FileJSONFormatter()
    actual_url = formatter.get_url_from_message(message)
    assert url == actual_url

def test_GivenMessage_WhenGetURLWithWWWFromMessage_ThenURLIsReturned():
    url = "https://www.mysite.dirbpy"
    message = URLBruteforcer.SCANNING_URL_MESSAGE.format(url)
    formatter = FileJSONFormatter()
    actual_url = formatter.get_url_from_message(message)
    assert url == actual_url

def test_GivenMessage_WhenGetNumberOfWordGeneratedFromMessage_ThenNumberIsReturn():
    number = "54"
    message = GENERATED_WORD_MESSAGE.format(number)
    formatter = FileJSONFormatter()
    actual_url = formatter.get_number_of_word_generated_from_message(message)
    assert number == actual_url

def test_GivenMessage_WhenGetStatusCodeFromMessage_ThenCodeIsReturn():
    number = 54
    message = "(satus code: {}) ".format(number)
    formatter = FileJSONFormatter()
    actual_url = formatter.get_status_code_from_message(message)
    assert number == actual_url

def test_GivenMessage_WhenJsonRecordHaveScanningURL_ThenDictIsReturn():
    url = "http://mysite.dirbpy"
    message = URLBruteforcer.SCANNING_URL_MESSAGE.format(url)
    formatter = FileJSONFormatter()

    actual_dict = formatter.json_record(message, {}, None)
    assert url in actual_dict.values()
    assert FileJSONFormatter.SCAN_URL_KEY in actual_dict.keys()

def test_GivenMessage_WhenJsonRecordHaveGeneratedWords_ThenDictIsReturn():
    number = '53'
    message = GENERATED_WORD_MESSAGE.format(number)
    formatter = FileJSONFormatter()

    actual_dict = formatter.json_record(message, {}, None)
    assert number in actual_dict.values()
    assert FileJSONFormatter.WORDS_GENERATED_KEY in actual_dict.keys()

def test_GivenMessage_WhenJsonRecordHaveScanningURL_ThenDictHaveAllImportantInfo():
    url = 'https://www.mysite.dirbpy/css'
    status_code = 400
    message = URLBruteforcer.URL_FOUND_MESSAGE.format(url, status_code)
    formatter = FileJSONFormatter()

    actual_dict = formatter.json_record(message, {}, None)

    assert FileJSONFormatter.URL_KEY in actual_dict.keys()
    assert url in actual_dict.values()

    assert FileJSONFormatter.STATUS_CODE_KEY in actual_dict.keys()
    assert status_code in actual_dict.values()

    assert FileJSONFormatter.TYPE_KEY in actual_dict.keys()
    assert FileJSONFormatter.TYPE_URL in actual_dict.values()





