from scipy import stats
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import numpy as np
import pandas as pd
import seaborn as sns

df = pd.read_csv("C:/Users/1907043/Documents/valuation.csv", header=0, encoding='CP949')
df.replace('',np.nan, inplace=True)
df = df.rename(columns={'Y-5.1':'Y-5','Y-4.1':'Y-4','Y-3.1':'Y-3','Y-2.1':'Y-2',
                        'Y-5.2':'Y-5','Y-4.2':'Y-4','Y-3.2':'Y-3','Y-2.2':'Y-2',
                        'Y-5.3':'Y-5','Y-4.3':'Y-4','Y-3.3':'Y-3','Y-2.3':'Y-2',
                        'Y-5.4':'Y-5','Y-4.4':'Y-4','Y-3.4':'Y-3','Y-2.4':'Y-2',})

sns.set(style="darkgrid")
sns.set_style("ticks", {"xtick.major.size": 15, "ytick.major.size": 15})
sns.set(rc={'axes.labelsize':20,
            'figure.figsize':(16,9),
            'axes.unicode_minus': False,
           })
fm.get_fontconfig_fonts()
font_location = 'C:/Windows/Fonts/NanumGothic.ttf'
font_name = fm.FontProperties(fname=font_location).get_name()
plt.rc('font', family=font_name)

num_df = df.select_dtypes(include=["number"])
cat_df = df.select_dtypes(exclude=["number"])

num_df = num_df.mask(num_df < 0)
company_type = pd.read_csv("C:/Users/1907043/Documents/company_type.csv", header=0, dtype=str)
types = ['금속', '기계 장비', '기타서비스', '운송장비 부품', '유통', '음식료 담배', '의료 정밀기기', '일반전기전자', '제약', '화학']
cdf = pd.DataFrame()

values = ['본질가치'+'('+str('억원')+')', '수익률'+'('+str('%')+')', 'IRR'+'('+str('%')+')',
          '자산가치'+'('+str('억원')+')', '수익가치'+'('+str('억원')+')']
money = str('금액') + '(' + str('억원') + ')'

i = 0
k = 0
while i < 17:
    dfv = num_df.iloc[:,i:i+4]
    dfv_z = dfv.mask((dfv - dfv.mean()).abs() > 1 * dfv.std())
    # ax = sns.boxplot(data = dfv_z, showfliers=False)
    # plt.savefig('C:/Users/1907043/Documents/asset_total' + str(i) + '.png')
    # fig, ax = plt.subplots()
    cdf = pd.DataFrame()
    for type in types:
        dfe = cat_df.join(dfv)
        code = dfe.loc[df['업종'] == type,]
        num = code.select_dtypes(include=["number"])
        z = num.mask((num - num.mean()).abs() > 1 * num.std())
        z = z * 100
        z['업종'] = type
        z = pd.DataFrame(z, columns=['업종','Y-5','Y-4','Y-3','Y-2' ])
        cdf = cdf.append(z)
        cdf.to_csv("C:/Users/1907043/Documents/asset" + '_' + values[k] + '_' + 'z.csv',encoding='cp949')
        mdf = pd.melt(cdf, id_vars=['업종'])
        dfe = []
    
    mdf = mdf.rename(columns={'variable':'시점', 'value':values[k]})
    axa = sns.boxplot(x="업종", y=values[k], hue="시점", data=mdf, showfliers = False)
    plt.legend(bbox_to_anchor=(0, 1),loc=2, borderaxespad=1.)
    plt.savefig('C:/Users/1907043/Documents/valuation' + '_' + values[k] + '.png')
    fig, ax = plt.subplots()
    i = i+4
    k = k+1
    
    money = values[k-1]
    q2 = mdf.groupby(['업종','시점'], sort=False)[money].median().values
    aq2 = np.array(q2).tolist()
    iq2 = pd.DataFrame({'중위값':aq2})
    q1 = mdf.groupby(['업종','시점'], sort=False)[money].quantile(0.25).values
    aq1 = np.array(q1).tolist()
    iq1 = pd.DataFrame({'Q1':aq1})
    q3 = mdf.groupby(['업종', '시점'], sort=False)[money].quantile(0.75).values
    aq3 = np.array(q3).tolist()
    iq3 = pd.DataFrame({'Q3':aq3})
    mm1 = pd.concat([iq2, iq1, iq3], axis=1, sort=False)
    mm1 = mm1.reindex([0,10,20,30,40,
                       1,11,21,31,41,
                       2,12,22,32,42,
                       3,13,23,33,43,
                       4,14,24,34,44,
                       5,15,25,35,45,
                       6,16,26,36,46,
                       7,17,27,37,47,
                       8,18,28,38,48,
                       9,19,29,39,49,
                      ])
    mm1.to_csv('C:/Users/1907043/Documents/valuation' + '_' + values[k-1] + '_' + 'z' + '_data.csv',encoding='cp949')

j=5
k=0
cdf = pd.DataFrame()

values = ['수익률']

for value in values:
    dfj = cat_df.join(num_df)
    code = dfj.iloc[:,j:j+4]
    num = code.select_dtypes(include=["number"])
    z = num.mask((num - num.mean()).abs() > 1 * num.std())
    z = z * 100
    z['구분'] = value
    z = pd.DataFrame(z, columns=['구분','Y-5','Y-4','Y-3','Y-2'])
    cdf = cdf.append(z)
    mdf = pd.melt(cdf, id_vars=['구분'])
    dfj = []
    j = j+4

money = str('수익률'+'('+str('%')+')')
    
mdf = mdf.rename(columns={'variable':'시점', 'value':money})

m1 = mdf.groupby(['시점','구분'], sort=False)[money].median().values
mL1 = [str(np.round(s, 2)) for s in m1]

axa = sns.boxplot(x="구분", y=money, hue="시점", data=mdf, showfliers = False)
pos = range(len(mL1))

ind = 0
for tick in range(len(axa.get_xticklabels())):
    axa.text(tick-.30, m1[ind], mL1[ind],  horizontalalignment='center',  color='w', weight='semibold')
    axa.text(tick-.10, m1[ind+1], mL1[ind+1],  horizontalalignment='center',  color='w', weight='semibold')
    axa.text(tick+.10, m1[ind+2], mL1[ind+2],  horizontalalignment='center',  color='w', weight='semibold')
    axa.text(tick+.30, m1[ind+3], mL1[ind+3],  horizontalalignment='center',  color='w', weight='semibold')
    ind += 1

plt.legend(bbox_to_anchor=(1, 1),loc=0, borderaxespad=1.)
plt.savefig('C:/Users/1907043/Documents/return_rate_total.png')
fig, ax = plt.subplots()

tq2 = mdf.groupby(['시점','구분'], sort=False)[money].median().values
taq2 = np.array(tq2).tolist()
tiq2 = pd.DataFrame({'중위값':taq2})
tq1 = mdf.groupby(['시점','구분'], sort=False)[money].quantile(0.25).values
taq1 = np.array(tq1).tolist()
tiq1 = pd.DataFrame({'Q1':taq1})
tq3 = mdf.groupby(['시점','구분'], sort=False)[money].quantile(0.75).values
taq3 = np.array(tq3).tolist()
tiq3 = pd.DataFrame({'Q3':taq3})
tmm1 = pd.concat([tiq2, tiq1, tiq3], axis=1, sort=False)
tmm1 = tmm1.reindex([0,2,4,6,8,1,3,5,7,9])
tmm1.to_csv("C:/Users/1907043/Documents/return_z_total_data.csv", encoding='CP949')

j=9
k=0
cdf = pd.DataFrame()

values = ['IRR']

for value in values:
    dfj = cat_df.join(num_df)
    code = dfj.iloc[:,j:j+4]
    num = code.select_dtypes(include=["number"])
    z = num.mask((num - num.mean()).abs() > 1 * num.std())
    z = z * 100
    z['구분'] = value
    z = pd.DataFrame(z, columns=['구분','Y-5','Y-4','Y-3','Y-2'])
    cdf = cdf.append(z)
    mdf = pd.melt(cdf, id_vars=['구분'])
    dfj = []
    j = j+4

money = str('IRR'+'('+str('%')+')')
    
mdf = mdf.rename(columns={'variable':'시점', 'value':money})

m1 = mdf.groupby(['시점','구분'], sort=False)[money].median().values
mL1 = [str(np.round(s, 2)) for s in m1]

axa = sns.boxplot(x="구분", y=money, hue="시점", data=mdf, showfliers = False)
pos = range(len(mL1))

ind = 0
for tick in range(len(axa.get_xticklabels())):
    axa.text(tick-.30, m1[ind], mL1[ind],  horizontalalignment='center',  color='w', weight='semibold')
    axa.text(tick-.10, m1[ind+1], mL1[ind+1],  horizontalalignment='center',  color='w', weight='semibold')
    axa.text(tick+.10, m1[ind+2], mL1[ind+2],  horizontalalignment='center',  color='w', weight='semibold')
    axa.text(tick+.30, m1[ind+3], mL1[ind+3],  horizontalalignment='center',  color='w', weight='semibold')
    ind += 1

plt.legend(bbox_to_anchor=(1, 1),loc=0, borderaxespad=1.)
plt.savefig('C:/Users/1907043/Documents/irr_rate_total.png')
fig, ax = plt.subplots()

cdf.to_csv("C:/Users/1907043/Documents/valuation_z.csv")

tq2 = mdf.groupby(['시점','구분'], sort=False)[money].median().values
taq2 = np.array(tq2).tolist()
tiq2 = pd.DataFrame({'중위값':taq2})
tq1 = mdf.groupby(['시점','구분'], sort=False)[money].quantile(0.25).values
taq1 = np.array(tq1).tolist()
tiq1 = pd.DataFrame({'Q1':taq1})
tq3 = mdf.groupby(['시점','구분'], sort=False)[money].quantile(0.75).values
taq3 = np.array(tq3).tolist()
tiq3 = pd.DataFrame({'Q3':taq3})
tmm1 = pd.concat([tiq2, tiq1, tiq3], axis=1, sort=False)
tmm1 = tmm1.reindex([0,2,4,6,8,1,3,5,7,9])
tmm1.to_csv("C:/Users/1907043/Documents/irr_z_total_data.csv", encoding='CP949')




