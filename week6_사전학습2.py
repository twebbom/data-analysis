import pandas as pd

# 예제 데이터프레임 생성
data = {
    'Name': ['Alice', 'Bob', 'Charlie', 'David', 'Eve'],
    'Age': [24, 27, 22, 32, 29],
    'City': ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix'],
    'Salary': [70000, 80000, 65000, 120000, 110000]
}
df = pd.DataFrame(data)
print(df)

#%%
#1.조건이 1개
#나이가 25 이상인 사람들
print(df[(df['Age'] >= 25)])

#샐러리가 80000 이상인 사람들
print(df[(df['Salary'] >= 80000)])

#%%
#2. 여러 조건을 사용한 필터링
#나이가 25 이상이고 샐러리가 80000 이상인 사람들
print(df.query('Age >= 25 & Salary >= 80000'))

#도시가 뉴욕이거나 시카고인 사람들
print(df[(df['City'] == ('New York' or 'Chicago'))])



#%%
#기타
#도시 이름이 'New'로 시작하는 사람들
city_startswith_filter = df[df['City'].str.startswith('New')]
print(city_startswith_filter)

#이름에 'a'가 포함된 사람들
name_filter = df[df['Name'].str.contains('a', case=False)]
print(name_filter)
