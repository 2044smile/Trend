import time, os, requests
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


# #naver
def naver_trend():
    # naver로 부터 text, headers, ststus, ok 정보를 받아 req 오브젝트에 저장
    req = requests.get('https://www.naver.com/')
    html = req.text

    # 노란색 글씨
    C_YELLOW = '\033[33m'
    rank_data = {}
    while True:
        soup = BeautifulSoup(html, 'html.parser')

        rank_title = soup.select( # 네이버 인기검색어의 이름 ex) 조국 . . . 1~20등 까지의 모든 title
            '#PM_ID_ct > div.header > div.section_navbar > div.area_hotkeyword.PM_CL_realtimeKeyword_base > div.ah_roll.PM_CL_realtimeKeyword_rolling_base > div > ul > li > a > span.ah_k'
        )
        rank_num = soup.select( # 네이버 인기검색어의 순위 ex) 1  . . . 1~20까지의 모든 number
            '#PM_ID_ct > div.header > div.section_navbar > div.area_hotkeyword.PM_CL_realtimeKeyword_base > div.ah_roll.PM_CL_realtimeKeyword_rolling_base > div > ul > li > a > span.ah_r'
        )
        for i in range(20): # 20위 까지 받기 위해서
            rank_data[i] = {rank_num[i].text: rank_title[i].text}
            if len(rank_num[i].text) == 1: # 1~9의 수는 앞에 0을 붙이게끔
                cprint('0' + str(rank_num[i].text) + ' ' + rank_title[i].text, 'yellow') # ex) 01 조국 노란색으로 출력
            else: # 그렇지않으면 그냥 출력
                cprint(rank_num[i].text + ' ' + rank_title[i].text, 'yellow') # 10 조국 노란색으로 출력
        time.sleep(5) # 5초 마다 반복
        os.system('cls') # 화면 클리어
        return rank_data


if __name__ == '__main__':
    NaverRank.objects.all().delete()
    rank_data_dict = naver_trend() # naver_trend 크롤링 돌아가는 함수 부분
    for n, t in rank_data_dict.items():
        NaverRank(rank_num=n+1, rank_title=t).save()
    print('Naver 업로드 완료')


# daum
def daum_trend():
    req = requests.get('https://www.daum.net/')
    html = req.text

    # 노란색 글씨
    C_YELLOW = '\033[33m'
    rank_data = {}
    while True:
        soup = BeautifulSoup(html, 'html.parser')

        rank_title = soup.select(  # 네이버 인기검색어의 이름 ex) 조국 . . . 1~20등 까지의 모든 title
            '#mArticle > div.cmain_tmp > div.section_media > div.hot_issue.issue_mini > div.hotissue_mini > ol > li > div > div > span.txt_issue'
        )
        rank_num = soup.select(  # 네이버 인기검색어의 순위 ex) 1  . . . 1~20까지의 모든 number
            '#mArticle > div.cmain_tmp > div.section_media > div.hot_issue.issue_mini > div.hotissue_mini > ol > li > div > div > span.num_pctop > span'
        )
        for i in range(10):  # 20위 까지 받기 위해서
            rank_data[i] = {rank_num[i].text: rank_title[i].text}
            cprint(rank_num[i].text + ' ' + rank_title[i].text, 'yellow')  # 10 조국 노란색으로 출력
            # if len(rank_num[i].text) == 1:  # 1~9의 수는 앞에 0을 붙이게끔
            #     cprint('0' + str(rank_num[i].text) + ' ' + rank_title[i].text, 'yellow')  # ex) 01 조국 노란색으로 출력
            # else:  # 그렇지않으면 그냥 출력
            #     cprint(rank_num[i].text + ' ' + rank_title[i].text, 'yellow')  # 10 조국 노란색으로 출력
        time.sleep(5)  # 5초 마다 반복
        os.system('cls')  # 화면 클리어
        return rank_data


if __name__ == '__main__':
    DaumRank.objects.all().delete()
    rank_data_dict = daum_trend()  # naver_trend 크롤링 돌아가는 함수 부분
    for n, t in rank_data_dict.items():
        DaumRank(rank_num=n + 1, rank_title=t).save()
    print('Daum 업로드 완료')


# # google
# def google_trend():
#     req = requests.get('https://www.daum.net/')
#     html = req.text
#
#     # 노란색 글씨
#     C_YELLOW = '\033[33m'
#     rank_data = {}
#     while True:
#         soup = BeautifulSoup(html, 'html.parser')
#
#         rank_title = soup.select(
#             '#feed-item > div.details-wrapper > div.details > div.details-top > div > span > a'
#         )
#         print(rank_title)
#         rank_num = soup.select(
#             '#feed-item-US_lnk_TbVm5AAwAAAr4M_en > div.details-wrapper > div'
#         )
#         # for i in range(20):
#         #     rank_data[i] = {rank_num[i].text: rank_title[i].text}
#         #     cprint(rank_num[i].text + ' ' + rank_title[i].text, 'yellow')
#             # if len(rank_num[i].text) == 1:  # 1~9의 수는 앞에 0을 붙이게끔
#             #     cprint('0' + str(rank_num[i].text) + ' ' + rank_title[i].text, 'yellow')  # ex) 01 조국 노란색으로 출력
#             # else:  # 그렇지않으면 그냥 출력
#             #     cprint(rank_num[i].text + ' ' + rank_title[i].text, 'yellow')  # 10 조국 노란색으로 출력
#         time.sleep(5)  # 5초 마다 반복
#         os.system('cls')  # 화면 클리어
#         return rank_data
#
#
# if __name__ == '__main__':
#     GoogleRank.objects.all().delete()
#     rank_data_dict = google_trend()
#     for n, t in rank_data_dict.items():
#         GoogleRank(rank_num=n + 1, rank_title=t).save()
#     print('Google 업로드 완료')


naver_trend()
daum_trend()
# google_trend()