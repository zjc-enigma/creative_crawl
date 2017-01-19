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
import urllib2
import re
from urlparse import urlparse, parse_qs
import xml.etree.ElementTree as ET
from lxml import etree
import browsercookie
import urlparse
import time
import pdb


base_url = 'http://creative.mediav.com/?entity=galileo&apikey=98f15264249b555d4351662a1aa2996b&referrer=tools&advertiser_id=265868'

browser = webdriver.Chrome()
browser.get(base_url)



# def find_query(url):

#     #url = url_unquote(url)
#     arg_dict = parse_qs(urlparse(url).query)
#     query_dict = {}

#     for key in arg_dict:
#         for list_item in arg_dict[key]:
#             if re.findall(ur'[\u4e00-\u9fff]+', list_item.decode('utf8')):
#                 query_dict[key] = list_item

#     return query_dict

def save_obj_to_file(obj):
    
    obj_id = obj.attr['id']
    obj_html = obj.outerHtml()
    save_path = "../data/obj_html/" + obj_id
    wfd = open(save_path, 'w')
    wfd.write(obj_html)
    wfd.close()
    print obj_id + " crawled"

def download_resource(url):

    cj = browsercookie.chrome()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    ret = opener.open(url)
    resource_data = ret.read()
    return resource_data


def build_save_path(url):
    url_dict = urlparse.urlparse(url)
    return "../data" + url_dict.path


def save_to_disk(resource_data, save_path):

    if not os.path.exists(os.path.dirname(save_path)):
        try:
            os.makedirs(os.path.dirname(save_path))

        except OSError as exc: # Guard against race condition
            print "save exception:", str(exc)
            raise
            #if exc.errno != errno.EEXIST:
            #    raise

    with open(save_path, "wb") as f:
        f.write(resource_data)



def crawl(url):
    resource_data = download_resource(url)
    save_path = build_save_path(url)
    save_to_disk(resource_data, save_path)


def crawl_param_resource(xml_str):
    #pdb.set_trace()
    parser = etree.XMLParser(recover=True)
    root = etree.fromstring(xml_str, parser=parser)
    elem_list = root.findall('*')

    for elem in elem_list:
        attr_dict = elem.attrib
        for k, v in attr_dict.iteritems():
            # swf
            if re.search('^http://', v):
                try:
                    crawl(v)
                except Exception, e:
                    print 'crawl error skip it', str(e)
            # img
            elif re.search('\.(png|jpg|jpeg)$', v):
                v = "http://creative.mediav.com" + v
                try:
                    crawl(v)
                except Exception, e:
                    print 'crawl error skip it', str(e)


def get_page_content():

    doc = pq(browser.page_source)
    doc.xhtml_to_html()
    creative_list = doc('div.template')

    for creative in creative_list.items():
        demo = creative('div.demo')
        obj = demo('object')
        save_obj_to_file(obj)

        param = obj('param').eq(1)
        param_str = param.attr['value']
        param_dict = parse_qs(param_str)
        p = param_dict['PageData'][0]
        crawl_param_resource(p)

def click_next_page():
    browser.find_element_by_css_selector('.pagination .next').click()

page_num = 6
for i in range(page_num):
    print("starting to crawl page:" + str(i))
    get_page_content()
    click_next_page()
    time.sleep(3)
