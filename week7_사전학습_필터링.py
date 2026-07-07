import pandas as pd

df = pd.DataFrame({
    "이름": ["김철수", "이영희", "박민수", "최수진", "정우성", "한지민"],
    "지역": ["서울특별시", "부산광역시", "대전광역시", "제주특별자치도", "경기도", "서울특별시"],
    "출생아수": [65000, 42000, 38000, 12000, 51000, 47000]
})

print(df)


#%%
# @ (외부 변수 참조)
threshold = 50000

df.query("출생아수 >= @threshold")


#%%
#isin() (여러 값 중 하나 포함)

df[df["지역"].isin(["서울특별시", "부산광역시"])]


df.query("지역 in ['서울특별시', '부산광역시']")


#%%
#문자열 검색(str)
df[df["지역"].str.contains("광역시")]

df.query("지역.str.contains('광역시')")

#startswith()
df[df["지역"].str.startswith("서")]

df.query("지역.str.startswith('서')")

#endswith()
df[df["지역"].str.endswith("도")]

df.query("지역.str.endswith('도')")


#%%
df.query("지역.str.contains('특별') and 출생아수 >= 45000")

df[
    (df["지역"].str.contains("특별")) &
    (df["출생아수"] >= 45000)
]