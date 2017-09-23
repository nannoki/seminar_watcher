# coding=utf-8

import requests
from bs4 import BeautifulSoup
import csv
import re
import time
import datetime
import os.path
import sendmail     # オリジナル

sendmail.send_mail('新着セミナー情報', 'テストです\n2行目です')
