# coding=utf-8

"""
Author: Esteban Cairol - ecairol
Scraper that receives an Amazon Customer Reviews URL and writes a txt file per review
Labels are generated depending on the rating: Negative (1 or 2 stars) or Positive (4 or 5 stars), 0 or 1 respectively
こちらから：
https://github.com/ecairol/sklearn-amazon-reviews

このファイルを改造
/home/takayuki_kuroki/PycharmPrj/py3/DFV/getReviews/sklearn-amazon-reviews-master/scrapper_csv_simple.py
"""

import requests
from bs4 import BeautifulSoup
import csv
import re
import time
import datetime
import os.path
import sendmail     # オリジナル

sendmail.send_mail('新着セミナー情報', 'テストです\nてすと')

