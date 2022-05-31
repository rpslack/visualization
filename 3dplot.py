import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from scipy import stats
import matplotlib.font_manager as fm
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.offline as pyo
get_ipython().run_line_magic('matplotlib', 'inline')
pyo.init_notebook_mode()

import plotly.graph_objects as go
import pandas as pd

df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminderDataFiveYear.csv')
data = [['수출바우처(내수)', 1, 5, 3],
        ['수출바우처(초보)', 2, 5, 3],
        ['수출바우처(유망)', 3, 5, 3],
        ['수출바우처(강소)', 4, 5, 3],
        ['수출바우처(혁신)', 5, 5, 3],
        ['온라인 수출대행', 1, 2, 1],
        ['온라인 직접수출', 2, 5, 1],
        ['자사몰 진출', 3, 4, 1],
        ['온라인 전시회', 4, 5, 3],
        ['온라인 공동물류', 5, 5, 3],
        ['수출인큐베이터', 3, 1, 3],
        ['KSC', 3, 1, 3],
        ['해외지사화', 3, 4, 3],
        ['융복합기술교류촉진', 4, 5, 5],
        ['청년글로벌마케터', 1, 1, 3],
        ['글로벌조달마케터', 3, 1, 5]]
        
        
df = pd.DataFrame(data, columns = ['사업명', '성장/진출단계','간접인프라~직접보조','B2C~B2B'])

start, end = 0, 15

fig = go.Figure(data=go.Scatter3d(
    x=df['성장/진출단계'][start:end],
    y=df['간접인프라~직접보조'][start:end],
    z=df['B2C~B2B'][start:end],
    text=df['사업명'][start:end],
    mode='markers',
    marker=dict(
        sizemode='diameter',
        sizeref=5,
        size=5,
        # size=df['gdpPercap'][start:end],
        # color = df['lifeExp'][start:end],
        colorscale = 'Viridis',
        colorbar_title = '성장',
        line_color='rgb(140, 140, 170)'
    )
))


fig.update_layout(height=800, width=800,
                  title='지원사업 분포도')

fig.show()
