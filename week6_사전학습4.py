#%%
""" groupby - 그룹별 집계 """
# 기본 형태: df.groupby('기준컬럼')['대상컬럼'].집계함수()
import pandas as pd
# 예제 데이터프레임 생성
data = {
    '이름': ['김철수', '이영희', '박민수', '최은영', '장서연', '한지민'],
    '학과': ['경영', '심리', '경영', '심리', '기계', '기계'],
    '성별': ['남', '여', '남', '여', '여', '여'],
    '점수': [85, 90, 88, 92, 87, 95]
}
df = pd.DataFrame(data)
print(df)

#%%
# 1. 단일 집계함수
# df.groupby('기준컬럼')['대상컬럼'].집계함수()

# 학과별 점수 평균
dept_mean = df.groupby('학과')['점수'].mean()
print(dept_mean)

#Q1 성별 점수 평균 구하기
# 학과별 학생 수 구하기 (count 사용)
print(df['학과'].value_counts())
# 성별 점수 최고점 구하기 (max 사용)
print(df.groupby('성별')['점수'].max())

#%%
# 2. 여러 집계 동시 적용 (agg)
# .agg(['함수1', '함수2', ...])

# 학과별 점수의 평균, 최대, 개수를 한 번에
dept_agg = df.groupby('학과')['점수'].agg(['mean', 'max', 'count'])
print(dept_agg)

#Q2 성별 점수의 평균, 최소, 개수를 한 번에 구하기
print(df.groupby('성별')['점수'].agg(['mean', 'max', 'count']))

#%%
# 3. 여러 컬럼으로 그룹화
# df.groupby(['컬럼1', '컬럼2'])['대상컬럼'].집계함수()

# 학과 + 성별 점수 평균
dept_gender = df.groupby(['학과', '성별'])['점수'].mean()
print(dept_gender)

#Q3 학과 + 성별 점수 합계 구하기 (sum 사용)
print(df.groupby(['학과', '성별'])['점수'].sum())

#%%
# groupby 결과는 인덱스가 바뀜
# reset_index()를 붙여서 일반 DataFrame으로 
result = df.groupby('학과')['점수'].mean()
print(result)
result = df.groupby('학과')['점수'].mean().reset_index()
print(result)

#%%
import pandas as pd
# 예제 데이터프레임 생성
data = {
    'Name': ['Alice', 'Bob', 'Charlie', 'David', 'Eve', 'Frank'],
    'Department': ['Sales', 'IT', 'Sales', 'IT', 'HR', 'HR'],
    'City': ['New York', 'Chicago', 'New York', 'Chicago', 'Houston', 'Houston'],
    'Salary': [70000, 80000, 65000, 120000, 110000, 90000]
}
df = pd.DataFrame(data)
print(df)

#%%
# 1. 단일 집계함수
#Q4 부서(Department)별 평균 연봉 구하기
print(df.groupby('Department')['Salary'].mean())

#Q5 도시(City)별 직원 수 구하기
print(df.groupby('City')['Name'].count())

#%%
# 2. 여러 집계 동시 적용 (agg)
#Q6 부서별 연봉의 평균, 최대, 최소를 한 번에 구하기
print(df.groupby('Department')['Salary'].agg(['mean', 'max', 'min']))

#%%
# 3. 여러 컬럼으로 그룹화
#Q7 부서 + 도시별 연봉 합계 구하기
print(df.groupby(['Department', 'City'])['Salary'].mean())

#%%
# 기타
# 부서별 평균 연봉을 구한 뒤 reset_index()로 일반 DataFrame 만들기
dept_salary = df.groupby('Department')['Salary'].mean().reset_index()
print(dept_salary)

# 그룹별 집계 결과를 내림차순으로 정렬하기 (sort_values 사용)
sorted_salary = df.groupby('Department')['Salary'].mean().reset_index().sort_values(by="Salary", ascending=False)
print(sorted_salary)






