import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib

plt.rc('font', family='Malgun Gothic')


#1. 국립대.xlsx 데이터를 읽어온다.
df = pd.read_excel('학생 1인당 교육비(국·공립대, 국립대법인, 특별_2024-05-19111635153.xlsx', header=[3,4])

df.columns = df.columns.get_level_values(0)

# "학교종류", 설립구분, 상태의 고유값을 알아본다.
print(df['학교종류'].unique())
print(df['설립구분'].unique())
print(df['상태'].unique())

# 대학교이면서 폐교되지 않은 국립, 국립대법인, 공립 자료를 df1으로 저장한다.
df1 = df[(df['학교종류']=='대학교') & (df['상태'] != '폐교') & (df['설립구분'].isin(['국립', '국립대법인', '공립']))]

#필요한 필드  '설립구분', '지역','학교','학생1인당 교육비\n(H=F/G)' 만 df1 으로 저장한다.
df1 = df1[['설립구분', '지역', '학교', '학생1인당 교육비\n(H=F/G)']]

#설립구분을 모두 '국립'으로 변경한다.
df1['설립구분'] = '국립'

# '학생1인당 교육비\n(H=F/G)'를 '교육비'로 필드명을 변경한다.
df1 = df1.rename(columns={'학생1인당 교육비\n(H=F/G)':'교육비'})

#%%
#1. 사립대.xlsx 데이터를 읽어온다.
df2 = pd.read_excel('학생 1인당 교육비(사립) (대학)_2024-05-19111655502.xlsx', header=[3,4])

df2.columns = df2.columns.get_level_values(0)

# "학교종류", 설립구분, 상태의 고유값을 알아본다.
print(df2['학교종류'].unique())
print(df2['설립구분'].unique())
print(df2['상태'].unique())

# 대학교인 자료를 df2으로 저장한다.
df2 = df2[df2['학교종류']=='대학교']

#필요한 필드  '설립구분', '지역','학교','학생1인당\n교육비(G=E/F)' 만 df2 으로 저장한다.
df2 = df2[['설립구분', '지역','학교','학생1인당\n교육비(G=E/F)']]

# '학생1인당\n교육비(G=E/F)'를 '교육비'로 필드명을 변경한다.
df2 = df2.rename(columns={'학생1인당\n교육비(G=E/F)':'교육비'})

#%%
# df1과 df2를 하나의 데이터프레임으로 만든다.
dfs = pd.concat([df1, df2], axis=0)

#지역별 교육비의 평균을 구하여 출력한다.
dfs.groupby('지역')['교육비'].mean()

#%%
max_by_region = dfs.groupby('지역')['교육비'].max().reset_index().sort_values(by='교육비', ascending=False)
print(max_by_region)

## 참고
pd.options.display.float_format = '{:,.0f}'.format
print(max_by_region)
# reset_option을 하지 않으면 계속 유지됨
pd.reset_option('display.float_format')

#%%
#seaborn을 이용하여 지역별 교육비 막대그래프를 구분은 설립구분으로 그린다.
df_bar = dfs.groupby(['지역', '설립구분'])['교육비'].mean().reset_index()

plt.figure(figsize=(12,5))
sns.barplot(data=df_bar, x='지역', y='교육비', hue='설립구분')
plt.title('지역별 교육비 (국립 vs. 사립')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

#%%
#교육비 상위 10개 대학을 구하여 출력한다.
top_10 = dfs.sort_values(by='교육비', ascending=False).head(10)

#교육비 상위 10개 대학을 seaborn 막대그래프로 그린다.
plt.figure(figsize=(14, 5))
sns.barplot(data=top_10, x='학교', y='교육비')
plt.title('교육비 상위 10개 대학')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()

