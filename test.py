import os
import sys
import pandas as pd
import time
import plotly.graph_objs as go

TestCMD = 'python main.py https://files.cloud.naver.com/file/download.api?resourceKey=YnJhaW5lcjEyMzQ1fDEzMTg1NjcyODcyfEZ8MA -f Shin.mp4 '

Cookie = "-c '_ga=GA1.2.1604843523.1594645465; NRTK=ag#all_gr#1_ma#-2_si#0_en#0_sp#0; NDARK=Y; page_uid=Uxa2cwp0J14ssiDWNwVssssstTs-174259; nx_ssl=2; nid_inf=-957558889; NID_JKL=Dyt51oF2g4Cs3bFN7uEg71rTS3lrfTCANHUhKZakw40=; NID_SES=AAABdquM0A9Z1KDUy011l1lE4BEr5fmMb9BoS01fo3L+pwBuu7oqeM9CNQg+fHSnv21owWgQJKAKVxYKQ+ZNJFbPW7tMSx7jK4p1MF18qwx7WvPoeGituRji/SUycETxY3D8/Im2iZRg0q2KNkgP1NkaM7VU1sISR8VPNLuWNOtmyV5GJKkl1pCIRWU8uOeOrGEm25ywgj+mG6dyg+KuQ2uCPOY6wmalB8gV9+pmHld+lzm7aNO/esmQzAT/kKtbS3AYeN27BE5s/kCVztw2go8zig5MOlgzgjjGFmHESKZ8gXff9U2A4N6tIvTINU7i6s4Pi4/JR1D74vlNtOJ2jTF5tgaQ566bVmpON+iNjoXh6k3yM9mpyXwTtqUjnwqTX5df5ToCS7DReNAcXAQ8vK9RsFXVxzHN96FfEfQAkOFjgwQhAr0oO1rcD2l8N0ftyrew3M0uVWCUdv7Mqxf9Q0KoC1kmwZl+eehUDIt1Cme8lOUFR4BZtrn/2pQLRktgUwleow=='"

Result = []

for i in range (1, 9):
    CMD = TestCMD + Cookie
    
    CMD += f' -t '
    CMD += str(i)
    # print(CMD)
    
#   시간 측정 시작
    start = time.time()
    
    os.system(CMD)
    
#   시간 측정 종료
    Result.append(time.time() - start)

ResultDF = pd.DataFrame(Result).rename(columns = {0: 'Time'})
ResultDF.index.names = ['Thread_Count']
ResultDF.reset_index(level=0, inplace=True)

print(ResultDF)
ResultDF.to_csv('./Result.csv', encoding='utf-8')

"""
그래프 그리기
"""

fig = go.Figure()

fig.add_trace(
    go.Scatter(
        x=ResultDF.Thread_Count,
        y=ResultDF.Time,
        name='날짜별 AMT'
    )
)

fig
