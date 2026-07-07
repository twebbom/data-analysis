import pandas as pd
import matplotlib.pyplot as plt

#Q. 한글 설정
plt.rc('font', family='Gulim')

#Q 인구동향 파일 읽기, 0,1이 헤더
df = pd.read_excel('월.분기.연간_인구동향_출생_사망_혼인_이혼__20240630154650.xlsx', header=[0,1])
df.head()

# 열 확인 #
df.columns

# tempdf = df[[('행정구역별(1)', '행정구역별(1)'),
#       ('2018', '출생아수(명)'),
#       ('2018', '사망자수(명)'),
#       ('2018', '혼인건수(건)'), 
#       ('2018', '이혼건수(건)')]]
# tempdf.columns = ['지역', '출생아수(명)', '사망자수(명)', '혼인건수(건)', '이혼건수(건)']
# tempdf['year'] = 2018
    
#Q 위 내용을 함수 makeDF로 만들기
def makeDF(year):
    tempdf = df[[('행정구역별(1)', '행정구역별(1)'),
          (str(year), '출생아수(명)'),
          (str(year), '사망자수(명)'),
          (str(year), '혼인건수(건)'),
          (str(year), '이혼건수(건)')]]
    tempdf.columns = ['지역', '출생아수(명)', '사망자수(명)', '혼인건수(건)', '이혼건수(건)']
    tempdf['year'] = year
    return tempdf

#%%
#반복문으로 2018 ~ 2022까지 호출해서 하나의 DF 연결하기
dfs = makeDF(2018)

#Q 들어갈 숫자는
for y in range(2019, 2023) :
    dfs = pd.concat([dfs, makeDF(y)]) #데이터프레임을 물리적으로 연결

dfs.head()


#%%
# 행인덱스 재설정 Q 이유를 색각해보자
dfs.reset_index(drop=True)
# 연도별 인덱스가 합쳐져 각각의 인덱스가 중복됨

# 행인덱스 재설정 : 최종 확정
dfs.reset_index(drop=True, inplace=True)
dfs

#%%
# df.info()

#%%
dfs.info()

print(dfs['지역'].unique())

# 지역별 카운트
print(dfs['지역'].value_counts())


#%%
"""# 조건식: () & () """
#1. 
#Q  2021년 '서울특별시', '부산광역시', '제주특별자치도' 중 하나인 데이터
# df 조건식으로 
dfs[(dfs['지역'].isin(['서울특별시', '부산광역시', '제주특별자치도'])) & (dfs['year'] == 2021)]

# query 
dfs.query("지역 in ['서울특별시', '부산광역시', '제주특별자치도'] and year == 2021")

#%%
"""# 분석1 : 연도별 전국 자료"""
df1 = dfs.query('지역 == "전국"').copy()
df1

# Q '자연증가수'  계산 출생아수 - 사망자수
df1['자연증가수'] = df1['출생아수(명)'] - df1['사망자수(명)']

# 연도별 인구동향 : 두축에 표시 전
#Q. 출생아수, 사망자수는 선그래프, 자연증가수는 막대그래프 그리기
plt.subplots(figsize=(8, 4))

plt.plot(df1['year'], df1['출생아수(명)'], '--ro', label='출생아수')
plt.plot(df1['year'], df1['사망자수(명)'], '-bs', label='사망자수')
plt.bar(df1['year'], df1['자연증가수'], color='skyblue', alpha=0.5, label='자연증가수')


plt.legend()
plt.title('연도별 인구동향')
plt.show()

#%%
# 연도별 인구동향 : 두축에 표시

fig, ax1 = plt.subplots(figsize=(8, 4))
ax1.plot(df1.year, df1['출생아수(명)'], 'b--o', label='출생아수')
ax1.plot(df1.year, df1['사망자수(명)'], 'g--o', label='사망자수')

ax2 = ax1.twinx()   #y축을 복사해서 한개더 생성
ax2.plot(df1.year, df1['자연증가수'], 'r-x', label='자연증가수')

plt.legend()
plt.title('연도별 인구동향')
plt.grid(alpha=0.5)
plt.show()

#%%
"""# 분석2   전국이 아닌 자료 추출"""
df2 = dfs.query('지역 != "전국"')
df2

#%%
import seaborn as sns

# Q. df2에서 혼인건수와 출생아수 관계를 산점도로
plt.figure(figsize=(8, 5))
sns.scatterplot(data=df2, x='혼인건수(건)', y='출생아수(명)')

plt.title('혼인건수와 출생아수 관계')
plt.show()

#%%
# 혼인건수와 출생아수 관계 분석2
import seaborn as sns
#Q df2에서 혼인건수와 출생아수 관계를 연도별 산점도
sns.scatterplot(data=df2, x='혼인건수(건)', y='출생아수(명)', hue='year')
plt.title('혼인건수와 출생아수 관계')
plt.show()

#%%
# 혼인건수와 출생아수 관계 분석2
import seaborn as sns
df2['year'] = df2['year'].astype(str)  #범주를 str로 수정 시 색상이 바뀜
sns.scatterplot(x='혼인건수(건)', y='출생아수(명)', hue='year', data=df2)
plt.title('혼인건수와 출생아수 관계')
plt.show()

#%%
# 세로 막대
#Q df2 지역별 출생아수를 세로막대로
# df2에는 여러 연도의 데이터가 섞여 있으므로 평균을 냅니다.
region_birth = df2.groupby('지역')['출생아수(명)'].mean().sort_values(ascending=False).reset_index()

# 2. 그래프 그리기
sns.barplot(data=region_birth, x='지역', y='출생아수(명)', palette='viridis')
plt.xticks(rotation=45)
plt.title('지역별 출생아수 평균')
plt.show()


#%%
"""#분석3 : 지역별 출생아/사망자수의 평균"""
dfg = df2.groupby('지역')[['출생아수(명)', '사망자수(명)']].mean().sort_values('출생아수(명)', ascending=False).reset_index()
dfg

sns.barplot(data=dfg, x='지역', y='출생아수(명)', color='skyblue',   label='출생아수')
sns.barplot(data=dfg, x='지역', y='사망자수(명)', color='salmon', label='사망자수', alpha=0.5)
plt.xticks(rotation=45)
plt.title('지역별 평균 출생아수 및 사망자수 비교')
plt.ylabel('평균 인구수(명)')
plt.legend() # 범례 표시
plt.show()

#%%
df_melt = dfg.melt(id_vars='지역', value_vars=['출생아수(명)', '사망자수(명)'])

plt.figure(figsize=(12, 6))
sns.barplot(data=df_melt, x='지역', y='value', hue='variable')
plt.xticks(rotation=45)
plt.show()
