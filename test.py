import time, os, requests
from datetime import datetime
from bs4 import BeautifulSoup
from termcolor import *
import colorama
colorama.init() # color
# Python이 실행될 때 DJANGO_SETTINGS_MODULE이라는 환경 변수에 현재 프로젝트의 settings.py파일 경로를 등록합니다
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Trend.settings")

# 이제 장고를 가져와 장고 프로젝트를 사용할 수 있도록 환경을 만듭니다.
import django
django.setup()
# Trend 의 NaverRank를 가져온다.
from rank.models import NaverRank, DaumRank, GoogleRank


def google_trend():
    req = requests.get('https://trends.google.co.kr/trends/trendingsearches/daily/rss?geo=US')
    html = req.text
    rank_data = {}
    soup = BeautifulSoup(html, 'html.parser')
    rank_title = soup.select(
        'item > title'
    )
    ranklink = soup.select(
        'item > link'
    )
    for i in range(10):  # 20위 까지 받기 위해서
        rank_data[i] = rank_title[i].text

    for a in soup.find_all('link'):
        print(a.get_text())
    GoogleRank.objects.all().delete()
    rank_data_dict = rank_data  # naver_trend 크롤링 돌아가는 함수 부분
    for n, t in rank_data_dict.items():
        GoogleRank(rank_num=n+1, rank_title=t).save()
    return print('Google 업로드')


def testgoogle():
    req = requests.get('https://trends.google.co.kr/trends/trendingsearches/daily/rss?geo=US')
    html = req.text
    soup = BeautifulSoup(html, 'html.parser')
    x = 0
    v = 0
    link = {}
    ranklink = {}
    for linkElement in soup.findAll('ht:news_item_url'):
        x += 1
        link[x] = linkElement.text

    for y in range(1, 10):
        ranklink[v] = link[y]
        v += 1

    print(ranklink[0])
    # GoogleRank.objects.all().delete()
    # rank_data_dict = rank_data  # naver_trend 크롤링 돌아가는 함수 부분
    # for n, t in rank_data_dict.items():
    #     GoogleRank(rank_num=n+1, rank_title=t).save()
    return print('Google 업로드')

testgoogle()
# google_trend()