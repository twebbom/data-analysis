import pandas as pd

# 첫 번째 데이터프레임
df1 = pd.DataFrame({
    'ID': [1, 2, 3, 4],
    '이름': ['김철수', '이영희', '박민수', '최은영'],
    '나이': [23, 21, 25, 22]
})

# 두 번째 데이터프레임
df2 = pd.DataFrame({
    'ID': [5, 6, 7, 8],
    '이름': ['장서연', '홍길동', '김미영', '이철호'],
    '나이': [24, 20, 27, 26]
})

print(df1)
print(df2)
# 좌우로 붙이기 (열 추가)
df = pd.concat([df1, df2], axis=1)
print(df)
# 위아래로 붙이기 (행 추가)
df = pd.concat([df1, df2], axis=0)
print(df)

#%% 시험 X, 참고용
import pandas as pd

# 첫 번째 데이터프레임
df1 = pd.DataFrame({
    'ID': [1, 2, 3, 4],
    '이름': ['김철수', '이영희', '박민수', '최은영'],
    '나이': [23, 21, 25, 22]
})

# 두 번째 데이터프레임
df2 = pd.DataFrame({
    'ID': [3, 4, 5, 6],
    '점수': [88, 92, 85, 90],
    '성별': ['남', '여', '여', '남']
})

print(df1)
print(df2)

#%%
# 열을 기준으로 병합하고 싶다면 merge를 사용 
# ID를 기준으로 합치기 (내부 조인)
merged_df = pd.merge(df1, df2, on='ID')

print("\nID를 기준으로 합친 데이터프레임 (내부 조인):")
print(merged_df)

#%%
#인덱스를 기준으로 병합하고 싶다면 join
# ID를 인덱스로 설정
df1.set_index('ID', inplace=True)
df2.set_index('ID', inplace=True)
# join 메서드 사용
joined_df = df1.join(df2, how='inner')

print("\nID를 인덱스로 설정하고 합친 데이터프레임 (내부 조인):")
print(joined_df)

#%%
# join 메서드 사용
joined_df = df1.join(df2, how='outer')

print("\nID를 인덱스로 설정하고 합친 데이터프레임 (내부 조인):")
print(joined_df)
