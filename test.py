import os
import sys
import pandas as pd
import time
import plotly.graph_objs as go
import main
import os.path

Result = []

if os.path.isfile('./ARG.txt'):
    for i in range (1, 9):
        ARG = open("./ARG.txt", 'r')
        CMD = ARG.read()
        ARG.close()

        CMD += ' -t '
        CMD += str(i)

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
        name='Thread_Count별 걸린 시간'
    )
)

fig
