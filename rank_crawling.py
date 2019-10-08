import time, os, requests
from bs4 import BeautifulSoup
# Python이 실행될 때 DJANGO_SETTINGS_MODULE이라는 환경 변수에 현재 프로젝트의 settings.py파일 경로를 등록합니다
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Trend.settings")

# 이제 장고를 가져와 장고 프로젝트를 사용할 수 있도록 환경을 만듭니다.
import django
django.setup()
# Trend 의 NaverRank를 가져온다.
from rank.models import NaverRank, DaumRank, GoogleRank


#naver
def naver_trend():
    # naver로 부터 text, headers, ststus, ok 정보를 받아 req 오브젝트에 저장
    req = requests.get('https://www.naver.com/')
    html = req.text

    rank_data = {}
    while True:
        soup = BeautifulSoup(html, 'html.parser')

        rank_title = soup.select( # 네이버 인기검색어의 이름 ex) 조국 . . . 1~20등 까지의 모든 title
            '#PM_ID_ct > div.header > div.section_navbar > div.area_hotkeyword.PM_CL_realtimeKeyword_base > div.ah_roll.PM_CL_realtimeKeyword_rolling_base > div > ul > li > a > span.ah_k'
        )
        for i in range(20): # 20위 까지 받기 위해서
            rank_data[i] = rank_title[i].text # rank_num[i].text.zfill(2):

        link = {}
        ranklink = {}
        x = 0
        v = 0
        for a in soup.find_all('a', 'ah_a'):
            x += 1
            link_text = a['href']  # 1~40 까지의 값이 들어간다 1~20까지는 #의 값이 21~40까지는 실제 link
            link[x] = link_text

        for y in range(21, 41): # 1~20 까지는 # 21~40까지 실제 데이터가 들어있다.
            ranklink[v] = link[y]
            v += 1

        NaverRank.objects.all().delete()
        rank_data_dict = rank_data  # naver_trend 크롤링 돌아가는 함수 부분
        for n, t in rank_data_dict.items():
            NaverRank(rank_num=n+1, rank_title=t, url=ranklink[n]).save()
        return print('Naver 업로드 완료')


# daum
def daum_trend():
    req = requests.get('https://www.daum.net/')
    html = req.text

    rank_data = {}
    while True:
        soup = BeautifulSoup(html, 'html.parser')

        rank_title = soup.select(  # 네이버 인기검색어의 이름 ex) 조국 . . . 1~20등 까지의 모든 title
            '#mArticle > div.cmain_tmp > div.section_media > div.hot_issue.issue_mini > div.hotissue_mini > ol > li > div > div > span.txt_issue'
        )
        for i in range(10):  # 20위 까지 받기 위해서
            rank_data[i] = rank_title[i].text

        # Daum ranklink
        link = {}
        ranklink = {}
        x = 0
        v = 0
        for a in soup.find_all('a', 'link_issue'):  # link_issue라는 클래스가 2개 발생하여 1 3 5 7 9 식으로 데이터를 저장해야한다.
            x += 1
            link_text = a['href']
            link[x] = link_text

        for y in range(1, 20, 2): # 1 3 5 7 9 11 13 15 17 19
            ranklink[v] = link[y]
            v += 1

        DaumRank.objects.all().delete()
        rank_data_dict = rank_data  # naver_trend 크롤링 돌아가는 함수 부분
        for n, t in rank_data_dict.items():
            DaumRank(rank_num=n + 1, rank_title=t, url=ranklink[n]).save()
        return print('Daum 업로드')


def google_trend():
    req = requests.get('https://trends.google.co.kr/trends/trendingsearches/daily/rss?geo=US')
    html = req.text
    rank_data = {}
    while True:
        soup = BeautifulSoup(html, 'html.parser')
        rank_title = soup.select(
            'item > title'
        )
        for i in range(10):  # 10위 까지 받기 위해서
            rank_data[i] = rank_title[i].text
        x = 0
        v = 0
        link = {}
        ranklink = {}
        for linkElement in soup.findAll('ht:news_item_url'): # findAll xml 의 형식을 크롤링할 때 사용
            x += 1
            link[x] = linkElement.text

        for y in range(1, 20, 2): # 1 3 5 7 9 11 13 15 17 19
            # ex) 조국이라는 item에 2개의 링크가 존재하므로 2씩 증가시키면서 그 다음의 첫 번째 링크가 나오게 끔
            ranklink[v] = link[y]
            v += 1
        GoogleRank.objects.all().delete()
        rank_data_dict = rank_data  # naver_trend 크롤링 돌아가는 함수 부분
        for n, t in rank_data_dict.items():
            GoogleRank(rank_num=n+1, rank_title=t, url=ranklink[n]).save()

        return print('Google 업로드')