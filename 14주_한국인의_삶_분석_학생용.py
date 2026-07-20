# =====================================================================
# 14주차 실습 - 한국인의 삶을 파악하라! (한국복지패널 데이터 분석)
# 빈칸(_______________)을 채워 완성하세요. 힌트는 주석에 있습니다.
# 명령 프롬프트(cmd)에서:  pip install pyreadstat openpyxl
# 데이터/코드북 파일은 이 스크립트와 같은 폴더에 둡니다.
#   - Koweps_hpwc20_2025_beta1.sav
#   - Koweps_Codebook_2019.xlsx

# ---------------------------------------------------------------------
# [1] 패키지 불러오기 & 그래프 기본 설정
# ---------------------------------------------------------------------
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

plt.rc('font', family='gulim')      # 한글 폰트 (윈도우 기본 굴림)

# 강의 표준 색상 (네이비 계열)
NAVY = ['#092D3D', '#314B98', '#6B9FD4']

#%%
# ---------------------------------------------------------------------
# [2] 데이터 불러오기
# ---------------------------------------------------------------------
# sav 파일 불러오기 (pyreadstat 필요)
raw_welfare = pd.read_spss('Koweps_hpwc20_2025_beta1.sav')

# 복사본 만들기 (원본 보존)
welfare = raw_welfare.copy()

# ---------------------------------------------------------------------
# [3] 데이터 검토하기
# ---------------------------------------------------------------------
print(welfare.shape)       # 행, 열 개수 출력
print(welfare)             # 앞부분, 뒷부분 출력
welfare.info()             # 변수 속성 출력 (info는 스스로 출력함)
print(welfare.describe())  # 요약 통계량

#%%
# ---------------------------------------------------------------------
# [4] 변수명 바꾸기 (변수명 확인: 20차 머지데이터_변수명.xlsx)
# ---------------------------------------------------------------------
welfare = welfare.rename(columns = {'h20_g3'     : 'sex',            # 성별
                                    'h20_g4'     : 'birth',          # 태어난 연도
                                    'h20_g10'    : 'marriage_type',  # 혼인 상태
                                    'h20_g11'    : 'religion',       # 종교
                                    'p2002_8aq1' : 'income',         # 월급
                                    'h20_eco9'   : 'code_job',       # 직업 코드
                                    'h20_reg7'   : 'code_region'})   # 지역 코드

#%%
# =====================================================================
# 분석 1. 성별에 따른 월급 차이 - 성별에 따라 월급이 다를까?
#        분석 2부터는 이 패턴을 그대로 응용합니다.
# =====================================================================

# --- 1-1. 성별 변수 검토 및 전처리 ---
print(welfare['sex'].dtypes)          # 변수 타입 출력
print(welfare['sex'].value_counts())  # 빈도 구하기

# 성별 항목 이름 부여 (1 → male, 2 → female)
welfare['sex'] = np.where(welfare['sex'] == 1, 'male', 'female')
print(welfare['sex'].value_counts())

#%%
# 빈도 막대 그래프
sns.countplot(data = welfare, x = 'sex', hue = 'sex',
              palette = NAVY[:2], width=0.5)
plt.title('성별 빈도')
plt.show()

#%%
# --- 1-2. 월급 변수 검토 ---
print(welfare['income'].dtypes)                    # 변수 타입 출력
sns.histplot(data = welfare, x = 'income', color = NAVY[1])
plt.title('월급 분포')
plt.show()
print(welfare['income'].isna().sum())              # 결측치(무응답) 확인

# [주의] welfare = welfare.dropna(...) 로 덮어쓰지 않는다!
#        월급이 없는 사람(무직자, 학생, 고령자 등)을 전체 데이터에서
#        지워 버리면 분석 7(이혼율), 분석 8(지역별 연령대)이 왜곡된다.
#        월급 분석에서만 아래처럼 체인 안에서 제외한다.

#%%
# --- 1-3. 성별 월급 평균표 만들기 ---
# 공식: ① 나누고(groupby) → ② 요약하고(mean) → ③ 그리기(barplot)
sex_income = welfare.dropna(subset = ['income']) \
                    .groupby('sex', as_index = False)['income'] \
                    .mean()
print(sex_income)

# --- 1-4. 그래프 만들기 ---
sns.barplot(data = sex_income, x = 'sex', y = 'income',
            hue = 'sex', palette = NAVY[:2])
plt.legend().remove()
plt.title('성별에 따른 월급 차이')
plt.show()

#%%
# =====================================================================
# 분석 2. 나이와 월급의 관계 - 몇 살 때 월급을 가장 많이 받을까?
# =====================================================================

# --- 2-1. 나이 변수 검토 및 전처리 ---
print(welfare['birth'].dtypes)                    # 변수 타입 출력
sns.histplot(data = welfare, x = 'birth', color = NAVY[1])
plt.title('출생 연도 분포')
plt.show()
print(welfare['birth'].isna().sum())              # 결측치 확인

# Q1. 나이 파생변수 만들기
# [주의] 이 데이터는 2025년 조사 자료 → 2025년 기준으로 계산!
# 힌트: 나이 = 2025 - 태어난 연도 + 1
welfare['age'] = 2025 - welfare['birth'] + 1
print(welfare['age'].describe())                  # 요약 통계량

#%%
sns.histplot(data = welfare, x = 'age', color= NAVY[1])
plt.title('나이 분포')
plt.show()


# --- 2-2. 나이별 월급 평균표 만들기 ---
# Q2. 나이별 월급 평균표 만들기
# 힌트: 분석 1-3의 코드에서 그룹 변수만 'age'로 바꾸면 됩니다.
age_income = welfare.dropna(subset = ['income']) \
                    .groupby('age', as_index = False)['income'] \
                    .mean()
print(age_income.head())

# --- 2-3. 선 그래프 만들기 ---
# Q3. 선 그래프 만들기
# 힌트: x축은 나이, y축은 월급 / sns.lineplot() 사용
sns.lineplot(data = age_income, x = 'age', y = 'income', color = NAVY[0])
plt.title('나이에 따른 월급 차이')
plt.show()

#%%
# =====================================================================
# 분석 3. 연령대에 따른 월급 차이 - 어떤 연령대의 월급이 가장 많을까?
# =====================================================================

# --- 3-1. 연령대 파생변수 만들기 ---
# 30 미만 → young, 60 미만 → middle, 그 외 → old
# Q4. 연령대 파생변수 만들기 (np.select)
# 힌트: np.select(조건 리스트, 값 리스트, default = 그 외 값)
conditions = [welfare['age'] < 30,
              welfare['age'] < 60]
choices    = ['young', 'middle']
welfare['ageg'] = np.select(conditions, choices, default = 'old')
print(welfare['ageg'].value_counts())             # 빈도 구하기


# 빈도 막대 그래프 - dodge 비교 시연
# Q5. dodge=False로 고쳐 그리기
# 힌트: x와 hue가 같은 변수면 칸 나누기를 꺼서(dodge=False) 정중앙 정렬
sns.countplot(data = welfare, x = 'ageg', hue = 'ageg',
              order = ['young', 'middle', 'old'],
              dodge = False,
              palette = NAVY)
plt.title('연령대별 인원수')
plt.show()

# --- 3-2. 연령대별 월급 평균표 만들기 ---
# Q6. 연령대별 월급 평균표 만들기
# 힌트: ① 나누고(ageg) → ② 요약하고(mean)
ageg_income = welfare.dropna(subset = ['income']) \
                     .groupby('ageg', as_index = False)['income'] \
                     .mean()
print(ageg_income)

# --- 3-3. 막대 그래프 만들기 ---
# Q7. 막대 그래프 만들기
# 힌트: sns.barplot() / x축은 연령대, y축은 월급
sns.barplot(data = ageg_income, x = 'ageg', y = 'income',
            hue = 'ageg', order = ['young', 'middle', 'old'],
            palette = NAVY, dodge=False)
plt.title('연령대별 월급 차이')
plt.show()

#%%
# =====================================================================
# 분석 4-1. 연령대 및 성별 월급 차이 - 성별 월급 차이는 연령대별로 다를까?
# =====================================================================

# --- 평균표 만들기 (groupby에 리스트로 두 변수 전달) ---
# Q8. 연령대 및 성별 월급 평균표 만들기
# 힌트: 그룹 변수가 두 개면 리스트로 전달합니다. → groupby(['ageg', 'sex'])
sex_income = welfare.dropna(subset = ['income']) \
                    .groupby(['ageg', 'sex'], as_index = False)['income'] \
                    .mean()
print(sex_income)

# Q9. 그래프 만들기
# 힌트: 성별을 색으로 구분하려면 hue = 'sex' 를 추가합니다.
sns.barplot(data = sex_income, x = 'ageg', y = 'income', hue = 'sex',
            order = ['young', 'middle', 'old'], palette = NAVY[:2])
plt.title('연령대 및 성별 월급 차이')
plt.show()

#%%
# =====================================================================
# 분석 4-2. 나이 및 성별 월급 차이
# =====================================================================
# --- 평균표 만들기 ---
# Q10. 나이 및 성별 월급 평균표 만들기
# 힌트: 그룹 변수는 ['age', 'sex']
sex_age = welfare.dropna(subset = ['income']) \
                 .groupby(['age', 'sex'], as_index = False)['income'] \
                 .mean()
print(sex_age.head())

# --- 선 그래프 만들기 ---
# Q11. 선 그래프 만들기
# 힌트: sns.lineplot() / 성별 구분은 hue
sns.lineplot(data = sex_age, x = 'age', y = 'income',  hue = 'sex',
             palette = NAVY[:2])
plt.title('나이 및 성별 월급 차이')
plt.show()

#%%
# =====================================================================
# 분석 5. 직업별 월급 차이 - 어떤 직업이 월급을 가장 많이 받을까?
# =====================================================================
# --- 5-1. 직업 변수 검토 ---
print(welfare['code_job'].dtypes)          # 변수 타입 출력
print(welfare['code_job'].value_counts())  # 빈도 구하기

# --- 5-2. 직종코드 불러와서 결합하기 (merge) ---
# 직업 이름표: 교재 코드북(2019)의 '직종코드' 시트 재사용
list_job = pd.read_excel('Koweps_Codebook_2019.xlsx',
                         sheet_name = '직종코드')
print(list_job.head())
print(list_job.shape)

# welfare에 list_job을 code_job 기준으로 결합
# Q12. welfare에 list_job을 code_job 기준으로 결합하기
# 힌트: merge(결합할 표, how = 'left', on = '공통 열 이름')
welfare = welfare.merge(list_job, how = 'left', on = 'code_job')
print(welfare['code_job'].isna().sum())    # 결측치 확인 (무직자는 직업 코드 없음)

# --- 5-3. 직업별 월급 평균표 만들기 ---
# Q13. 직업별 월급 평균표 만들기
# 힌트: job과 income의 결측치를 함께 제거 → dropna(subset = ['job', 'income'])
#       그 다음은 늘 하던 공식: 나누고(job) → 요약하고(mean)
job_income = welfare.dropna(subset = ['job', 'income']) \
                    .groupby('job', as_index = False)['income'] \
                    .mean()
print(job_income.head())

# --- 5-4. 월급 상위 10개 직업 ---
# Q14. 월급 상위 10개 직업 추출하기
# 힌트: sort_values('income', ascending = False) 로 내림차순 정렬 후 head(10)
top10 = job_income.sort_values('income', ascending = False).head(10)
print(top10)

sns.barplot(data = top10, y = 'job', x = 'income', color = NAVY[1])
plt.title('월급 상위 10개 직업')
plt.show()

# --- 5-5. 월급 하위 10개 직업 ---
bottom10 = job_income.sort_values('income').head(10)
print(bottom10)

# xlim을 상위 그래프와 맞춰서 상/하위를 같은 잣대로 비교 (20차 최고 약 1,144)
sns.barplot(data = bottom10, y = 'job', x = 'income', color = NAVY[2]) \
   .set(xlim = [0, 1150])
plt.title('월급 하위 10개 직업')
plt.show()

#%%
# =====================================================================
# 분석 6. 성별 직업 빈도 - 성별에 따라 어떤 직업이 가장 많을까?
# =====================================================================
# [통일] 남녀 모두 .agg(n = ('job', 'count')) 패턴 사용
#        (income.count()는 "월급 응답자 수"라서 직업 빈도가 아님)

# --- 남성 직업 빈도 상위 10개 ---
job_male = welfare.query('sex == "male"') \
                  .groupby('job', as_index = False) \
                  .agg(n = ('job', 'count')) \
                  .sort_values('n', ascending = False) \
                  .head(10)
print(job_male)

# --- 여성 직업 빈도 상위 10개 ---
# Q15. 여성 직업 빈도 상위 10개 추출하기
# 힌트: 위의 남성 코드에서 조건만 바꾸면 됩니다.
job_female = welfare.query('sex == "female"') \
                    .groupby('job', as_index = False) \
                    .agg(n = ('job', 'count')) \
                    .sort_values('n', ascending = False) \
                    .head(10)
print(job_female)

# --- 그래프 만들기 ---
# xlim: 20차 남성 1위(작물 재배 종사자)가 561명이라 600으로 설정
sns.barplot(data = job_male, y = 'job', x = 'n',
            color = NAVY[0]).set(xlim = [0, 600])
plt.title('남성 직업 빈도 상위 10개')
plt.show()

# Q16. 여성 직업 빈도 그래프 만들기
sns.barplot(data = job_female, y = 'job', x = 'n',
            color = NAVY[2]).set(xlim = [0, 600])
plt.title('여성 직업 빈도 상위 10개')
plt.show()

#%%
# =====================================================================
# 분석 7. 종교 유무에 따른 이혼율 - 종교가 있으면 이혼을 덜 할까?
# =====================================================================
# welfare를 덮어쓰지 않았으므로 월급이 없는 사람도 포함된
# "전체 인구" 기준으로 이혼율을 계산할 수 있다.

# --- 7-1. 종교 변수 전처리 ---
print(welfare['religion'].value_counts())  # 빈도 구하기

# [주의] 이 셀은 한 번만 실행! 두 번 실행하면 값이 이미 문자('yes'/'no')라
#        조건 == 1 이 전부 거짓 → 모두 'no'로 덮어써집니다.
#        꼬였으면 [2]의 복사본 만들기부터 다시 실행하세요.
# Q17. 종교 유무 이름 부여하기 (1 → 'yes', 2 → 'no')
# 힌트: 분석 1의 성별 이름 부여와 같은 패턴 (np.where)
welfare['religion'] = np.where(welfare['religion'] == 1, 'yes', 'no')
print(welfare['religion'].value_counts())

# Q18. 종교 유무 빈도 막대 그래프 만들기
# 힌트: 빈도 그래프는 sns.countplot()
sns.countplot(data = welfare, x = 'religion', hue = 'religion',
              palette = NAVY[:2], dodge=False)
plt.title('종교 유무')
plt.show()

#%%
# --- 7-2. 혼인 상태 변수 전처리 ---
print(welfare['marriage_type'].dtypes)
print(welfare['marriage_type'].value_counts())

# 이혼 여부 파생변수 (1 → marriage, 3 → divorce, 그 외 → etc)
# 세 갈래 분류이므로 분석 3처럼 np.select 사용
conditions = [welfare['marriage_type'] == 1,
              welfare['marriage_type'] == 3]
welfare['marriage'] = np.select(conditions, ['marriage', 'divorce'],
                                default = 'etc')

# 이혼 여부별 빈도
n_divorce = welfare.groupby('marriage', as_index = False) \
                   .agg(n = ('marriage', 'count'))
print(n_divorce)

sns.barplot(data = n_divorce, x = 'marriage', y = 'n',
            hue = 'marriage', palette = NAVY, dodge=False)
plt.title('이혼 여부별 빈도')
plt.show()

# --- 7-3. 종교 유무에 따른 이혼율 표 만들기 ---
# religion으로 그룹을 나눈 뒤, 그룹 안에서 marriage 값의 "비율" 계산
# normalize = True : 개수 대신 비율(합이 1)을 구함
# Q19. 이혼율 표 만들기
# 힌트: ① etc 제외(query) → ② religion별로 나누고 → ③ marriage 비율 구하기
rel_div = welfare.query('marriage != "etc"') \
                 .groupby('religion', as_index = False)['marriage'] \
                 .value_counts(normalize = True)
print(rel_div)

# divorce만 추출하고 백분율로 변환
rel_div = rel_div.query('marriage == "divorce"')
rel_div['proportion'] = round(rel_div['proportion'] * 100, 1)
print(rel_div)

sns.barplot(data = rel_div, x = 'religion', y = 'proportion',
            hue = 'religion', palette = NAVY[:2], dodge=False)
plt.title('종교 유무에 따른 이혼율(%)')
plt.show()

#%%
# =====================================================================
# 분석 8. 지역별 연령대 비율 - 어느 지역에 노년층이 많을까?
# =====================================================================
# welfare를 덮어쓰지 않았으므로 데이터를 다시 불러올 필요가 없다!

# --- 8-1. 지역 코드 목록 만들기 ---
list_region = pd.DataFrame({'code_region' : [1, 2, 3, 4, 5, 6, 7],
                            'region'      : ['서울',
                                             '수도권(인천/경기)',
                                             '부산/경남/울산',
                                             '대구/경북',
                                             '대전/충남',
                                             '강원/충북',
                                             '광주/전남/전북/제주도']})
print(list_region)

# --- 8-2. 지역명 결합하기 ---
print(welfare['code_region'].dtypes)
print(welfare['code_region'].value_counts())

# Q20. welfare에 list_region을 code_region 기준으로 결합하기
# 힌트: 분석 5의 merge와 같은 패턴
welfare = welfare.merge(list_region, how = 'left', on = 'code_region')
print(welfare[['code_region', 'region']].head())

# --- 8-3. 지역별 연령대 비율표 만들기 ---
# Q21. 지역별 연령대 비율표 만들기
# 힌트: 분석 7의 이혼율 표와 같은 패턴 (region별로 나누고 → ageg 비율)
region_ageg = welfare.groupby('region', as_index = False)['ageg'] \
                     .value_counts(normalize = True)
print(region_ageg)

# 백분율로 변환
region_ageg = region_ageg.assign(proportion = region_ageg['proportion'] * 100) \
                         .round(1)
print(region_ageg)

# --- 8-4. 그래프 만들기 ---
# Q22. 그래프 만들기
# 힌트: 지역 이름이 길어서 가로 막대가 좋습니다. → y = 'region', x = 'proportion'
#       연령대 구분은 hue
sns.barplot(data = region_ageg, y = 'region', x = 'proportion',
            hue = 'ageg', palette = NAVY)
plt.title('지역별 연령대 비율(%)')
plt.show()

# =====================================================================
# 제출 전 체크: 질문 22개(빈칸 37개)를 모두 채웠나요? 그래프가 전부 그려지나요?
# =====================================================================
