#coding=utf-8
import os
from os.path import isfile, join
import sys
reload(sys)
sys.setdefaultencoding('UTF8')
sys.path.append("/Users/Patrick/Git")
from utils import myutils
import requests
from pyquery import PyQuery as pq
import json
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import time

options = webdriver.ChromeOptions()
#options.add_argument('--user-agent=' + myutils.get_random_ua_header()['User-Agent'])
