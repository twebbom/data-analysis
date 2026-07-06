"""unique 함수 """
import numpy as np

arr = np.array([1, 2, 2, 3, 4, 4, 5])
unique_arr = np.unique(arr)
print(unique_arr)

#%%
import pandas as pd
df = pd.DataFrame({
    'A': [1, 2, 2, 3, 4, 4, 5],
    'B': ['a', 'b', 'b', 'c', 'd', 'd', 'e']
})

unique_column = df['B'].unique()

print(unique_column)

#%%
""" 필터링 """
import pandas as pd

# 예제 데이터프레임 생성
data = {
    '이름': ['김철수', '이영희', '박민수', '최은영', '장서연'],
    '나이': [23, 21, 25, 22, 24],
    '성별': ['남', '여', '남', '여', '여'],
    '점수': [85, 90, 88, 92, 87]
}

df = pd.DataFrame(data)
print(df)

#필드명 비교연산자 조건

# 점수가 90점 이상인 학생 필터링
print(df[df['점수'] >= 90]) 
print(df.query('점수 >= 90'))

# 성별이 여자인 학생 필터링
print(df[df['성별'] == '여'])
print(df.query('성별 == "여"'))

# 여자이면서 나이가 23세 이상인 학생
filtered_df = df[(df['성별'] == '여') & (df['나이']>=23)]
print(filtered_df)

print(df.query("성별 == '여' & 나이 >= 23" ))

# 나이가 23세 이상이고 점수가 90점 이상인 학생 필터링
print(df[(df['나이'] >= 23) & (df['점수'] >= 90)])
print(df.query('점수 >= 90 & 나이 >= 23'))


