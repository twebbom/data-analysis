# ============================================================
# 6주차 실습 파일 – 1인당 교육비 분석
# ============================================================

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib
# matplotlib.rcParams['font.family'] = 'Malgun Gothic'  # Windows
# # matplotlib.rcParams['font.family'] = 'AppleGothic'  # Mac
# matplotlib.rcParams['axes.unicode_minus'] = False

plt.rc('font', family='Malgun Gothic')

#%%
# [1단계] 국립대 파일 읽기

# TODO: 국립대 엑셀 파일을 header=[3,4] 옵션으로 읽으세요.
# header=[3,4] -> 두 줄을 컬럼으로 인식
df_gov = pd.read_excel("학생 1인당 교육비(국·공립대, 국립대법인, 특별_2024-05-19111635153.xlsx",
                       header=[3,4])

# TODO: 첫 번째 레벨 컬럼만 추출해서 단일 컬럼으로 교체하세요.
# .get_level_values(0) -> 다중 인덱스 중 첫 레벨만
first_level_colums = df_gov.columns.get_level_values(0)
print(first_level_colums)

# df.columns = ... -> 단일 칼럼으로 재정의
df_gov.columns = first_level_colums
df_gov.head(2)
#%%
# [2단계] 국립대 파일 탐색 

# TODO 1: 컬럼명을 출력하세요.
print("컬럼명:", df_gov.columns)

# TODO 2: 학교종류의 고유값을 출력하세요.
print("\n학교종류:", df_gov['학교종류'].unique())


# TODO 3: 설립구분의 고유값을 출력하세요.
print("\n설립구분:", df_gov['설립구분'].unique())

# TODO 4: 상태의 고유값을 출력하세요.
print("\n상태:", df_gov['상태'].unique())


#%%
# [3단계] 국립대 전처리

# TODO 1: 폐교되지 않은 대학교 중 국립/국립대법인/공립만 필터링하세요.
df1_raw = df_gov[(df_gov['상태'] == '기존') & (df_gov['학교종류'] == '대학교') 
                 & (df_gov['설립구분'].isin(['국립', '국립대법인', '공립']))]

# TODO 2: 설립구분, 지역, 학교, 학생1인당 교육비 컬럼만 추출하세요.
#          (컬럼명은 df_gov.columns 로 확인)
df1 = df1_raw[['설립구분', '지역', '학교', '학생1인당 교육비\n(H=F/G)']]

# TODO 3: 학생1인당 교육비 컬럼 이름을 '교육비'로 변경하세요.
df1 = df1.rename(columns={'학생1인당 교육비\n(H=F/G)': '교육비'})

# TODO 4: 설립구분 값을 모두 '국립'으로 변경하세요.
df1['설립구분'] = '국립'

print("\n국립대 shape:", df1.shape)
print(df1.head(3))

#%%
# [4단계] 사립대 파일 읽기 & 전처리 
# TODO 1: 사립대 엑셀 파일을 읽으세요.
df_prv = pd.read_excel('학생 1인당 교육비(사립) (대학)_2024-05-19111655502.xlsx', header=[3,4])
df_prv.columns = df_prv.columns.get_level_values(0)

#%%
# TODO 2: 학교종류, 설립구분, 상태 고유값을 확인하세요.
print("\n사립대 학교종류:", df_prv['학교종류'].unique())
print("사립대 설립구분:", df_prv['설립구분'].unique())
print("사립대 상태:", df_prv['상태'].unique())

#%%
# TODO 3: 폐교되지 않은 대학교만 필터링하세요.
df2_raw = df_prv[(df_prv['상태'] != '폐교')]

# TODO 4: 필요한 컬럼만 추출하고 교육비로 이름 변경 후 크기 확인.
df2 = df2_raw[['설립구분','지역','학교','학생1인당\n교육비(G=E/F)']]
df2 = df2.rename(columns={'학생1인당\n교육비(G=E/F)' : '교육비'})
print("\n사립대 shape:", df2.shape)


#%%
# [5단계] DataFrame 합치기 

# TODO: df1과 df2를 세로로 합치고 인덱스를 재정렬하세요.
dfs = pd.concat([df1, df2], axis=0)
dfs.reset_index(drop=True)

print("\n전체 shape:", dfs.shape)
print(dfs.head())


#%%
#  데이터분석
# df.groupby('기준컬럼')['대상컬럼'].집계함수() 
# df.groupby('기준컬럼')['대상컬럼'].agg([집계합수])
# df.groupby('기준컬럼')['대상컬럼'].집계함수().reset_index()


# Q1 지역별 교육비 평균을 구하세요.
grouped_region = dfs.groupby('지역')['교육비'].mean()
print("\n지역별 교육비 평균:")
print(grouped_region)

# Q2  설립구분별 교육비의 평균·최대·학교 수를 한 번에 구하세요.
grouped_type = dfs.groupby('설립구분')['교육비'].agg(['mean', 'max', 'count'])
print("\n설립구분별 집계:")
print(grouped_type)

# Q3  지역·설립구분 기준 교육비 평균을 구하고 일반 DataFrame으로 변환하세요.
grouped_both = dfs.groupby(['지역', '설립구분'])['교육비'].mean()
print("\n지역·설립구분별 평균:")
print(grouped_both)


#%%
# [6단계] sort_values & 상위 30 추출 
# df.sort_values(by='컬럼명', ascending=False)

# TODO: 교육비 기준 내림차순 정렬 후 상위 30개 추출하세요.
top30 = dfs.sort_values(by='교육비', ascending=False).head(30)
print("\n교육비 상위 30위:")
print(top30)


#%%
# [7단계] 시각화
# 팔레트 설정
palette = {'국립': '#314B98', '사립': '#092D3D'}

# TODO Q1 : 교육비 하위 10개 대학을 추출하고 출력하세요.
bottom10 = dfs.sort_values(by='교육비', ascending=True).head(10)
print("\n교육비 하위 10위:")
print(bottom10)

# TODO Q2 : 설립구분별 학교 수를 구하세요.
count_by_type = dfs['설립구분'].value_counts()
print("\n설립구분별 학교 수:")
print(count_by_type)

# TODO Q3 : 지역별 교육비 최댓값을 내림차순으로 정렬하세요.
max_by_region = dfs.groupby('지역')['교육비'].max().sort_values(ascending=False)
print("\n지역별 교육비 최댓값 (내림차순):")
print(max_by_region)

#%% 7주차 추가 내용
===========================================================================
max_by_region = dfs.groupby('지역')['교육비'].max().reset_index().sort_values(by='교육비', ascending=False)
print(max_by_region)

## 참고
pd.options.display.float_format = '{:,.0f}'.format
print(max_by_region)
# reset_option을 하지 않으면 계속 유지됨
pd.reset_option('display.float_format')
==========================================================================

# TODO Q4 : 서울 사립대만 필터링해서 교육비 막대 그래프를 그리세요.
seoul_prv = dfs[(dfs['지역'] == '서울') & (dfs['설립구분'] == '사립')]

plt.figure(figsize=(12, 5))
sns.barplot(seoul_prv, x='학교', y='교육비')
plt.xticks(rotation=45, ha='right')
plt.title('서울 사립대 1인당 교육비')
plt.tight_layout()
plt.show()

# TODO Q5 : 지역·설립구분별 교육비 평균 → hue barplot 시각화
grouped_vis = dfs.groupby(['지역', '설립구분'])['교육비'].mean().reset_index()

plt.figure(figsize=(14, 5))
sns.barplot(data=grouped_vis, x='지역', y='교육비', hue='설립구분', palette=palette)
plt.title('지역별 교육비 (국립 vs 사립)')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()





