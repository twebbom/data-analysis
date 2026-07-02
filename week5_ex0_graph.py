import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv('체납액Data.csv', encoding='CP949')

sns.set_context("notebook")
palette = sns.color_palette("colorblind")

#%%
#선그래프
plt.figure(figsize=(10, 5))
plt.plot(df['지역'], df['금액'], '--go', label='체납금액')
plt.title('지역별 체납금액', fontsize=14)
plt.xlabel('지역')
plt.ylabel('체납금액')
plt.xticks(rotation=45)
plt.grid(ls='--', color='gray', alpha=0.5)
plt.axhline(y=20000, color='red', alpha=0.7, label='기준선')
plt.legend()
plt.show()

#%%

import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv('체납액Data.csv', encoding='CP949')

sns.set_context("notebook")
palette = sns.color_palette("colorblind")

plt.figure(figsize=(10, 6))
sns.barplot(data=df, x='지역', y='건수', palette=palette)
plt.title('지역별 체납건수', fontsize=14)
plt.xticks(rotation=45)
plt.grid(color='gray', alpha=0.5, ls='--')
plt.tight_layout()
plt.show()

#%%
#막대그래프
plt.figure(figsize=(10, 5))
plt.bar(df['지역'], df['금액'],
        color='steelblue')
plt.title('지역별 체납금액')
plt.xticks(rotation=45)
plt.show()

# 수평 막대
plt.barh(df['지역'], df['금액'])


#%%
#seaborn 막대그래프
sns.barplot(data=df,
            x='지역',
            y='금액',
            palette=palette)
plt.xticks(rotation=45)
plt.show()


#%%
#산점도
plt.figure(figsize=(6,5))
plt.scatter(df['금액'], df['건수'],
            color='green',
            alpha=0.7)
plt.xlabel('체납금액')
plt.ylabel('체납건수')
plt.title('금액 vs 건수')
plt.show()


# #%%
# from scipy.stats import pearsonr
# from scipy.stats import linregress

# x = df['금액']
# y = df['건수']
# # Pearson 상관계수 계산
# r, p = pearsonr(x, y)

# # Scatter plot
# plt.scatter(x, y, color='green', alpha=0.7)

# slope, intercept, r, p, stderr = linregress(x, y)
# plt.plot(x, intercept + slope * x, color="red", linewidth=0.5, alpha=0.7, label=r)

# # 그래프에 r 표시
# # plt.text(
# #     0.05, 0.95,
# #     f"r = {r:.3f}\np = {p:.3g}",
# #     transform=plt.gca().transAxes,
# #     fontsize=12,
# #     verticalalignment="top"
# # )

# plt.title('금액과 건수의 상관관계')
# plt.xlabel("금액")
# plt.ylabel("건수")
# plt.legend()
# plt.show()


#%%
#파이차트
plt.figure(figsize=(6,6))
plt.pie(df['금액'],
        labels=df['지역'],
        autopct='%.1f%%',
        startangle=90)
plt.title('지역별 체납금액 비율')
plt.show()
