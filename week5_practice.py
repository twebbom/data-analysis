# ============================================================
#  5주차 실습 파일  –  데이터의 시각화
# ============================================================
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 한글 깨짐 방지 핵심 설정
plt.rc('font', family='gulim')     # 윈도우 기본 한글 폰트 설정

#%%

# ------------------------------------------------------------
# 데이터 불러오기
# ------------------------------------------------------------
df_mall = pd.read_csv('mall_order.csv')

# mall_order 컬럼 설명
# customer, product, category, price, qty, discount_rate, region
df_mall = df_mall.copy()
df_mall['total']        = df_mall['price'] * df_mall['qty']
df_mall['discount_amt'] = df_mall['total'] * df_mall['discount_rate'] / 100
df_mall['final_price']  = df_mall['total'] - df_mall['discount_amt']

# ============================================================
#  실습 ①  –  matplotlib 선 그래프  (mall_order.csv)
# ============================================================

# Q1. 선 그래프 그리기
#     customer(x축)와 final_price(y축)로 선 그래프를 그리세요.
#     마커는 'o', 색상은 'blue'로 설정하세요.

plt.figure(figsize=(10, 5))

# 여기에 코드를 작성하세요
plt.plot(df_mall['customer'], df_mall['final_price'], '-bo')

plt.show()



#%%
# Q2. 그래프 꾸미기
#     Q1 코드에 아래 요소를 추가하세요.
#     - 제목: '고객별 최종 결제금액'
#     - x축 레이블: '고객명'
#     - y축 레이블: '최종 결제금액 (원)'
#     - x축 눈금 45도 회전
#     - grid 추가 (선모양: '--', 투명도: 0.5)

plt.figure(figsize=(10, 5))

# 여기에 코드를 
plt.plot(df_mall['customer'], df_mall['final_price'], '-bo')

plt.title('고객별 최종 결제금액')
plt.xlabel('고객명')
plt.ylabel('최종 결제금액 (원)')
plt.xticks(rotation=45)
plt.grid(ls='--', alpha=0.5)

plt.show()

#%%
# Q3. 평균선 추가
#     Q2 그래프에 axhline()으로 final_price 평균값의 수평선을 추가하세요.
#     - 색상: 'red', 투명도: 0.7, 범례 레이블: '평균 결제금액'
#     - plt.legend()로 범례를 표시하세요.
#     힌트: avg = df_mall['final_price'].mean()

plt.figure(figsize=(10, 5))

# 여기에 코드를 작성하세요
plt.plot(df_mall['customer'], df_mall['final_price'], '-bo')

plt.title('고객별 최종 결제금액')
plt.xlabel('고객명')
plt.ylabel('최종 결제금액 (원)')
plt.xticks(rotation=45)
plt.grid(ls='--', alpha=0.5)

plt.axhline(y=df_mall['final_price'].mean(), color='red',
            alpha=0.7, label='평균 결제금액')
plt.legend()

plt.show()

#%%
# Q4. [도전] subplot으로 금액/수량 함께 표시
#     2행 1열 subplot으로 그래프를 나란히 그리세요.
#     - 첫 번째(위): customer vs final_price  '--bo'
#     - 두 번째(아래): customer vs qty         '-ks'
#     - plt.tight_layout()으로 겹침을 방지하세요.

plt.figure(figsize=(10, 8))

# 여기에 코드를 작성하세요
plt.subplot(2,1,1)
plt.plot(df_mall['customer'], df_mall['final_price'], '--bo')

plt.subplot(2,1,2)
plt.plot(df_mall['customer'], df_mall['qty'], '-ks')

plt.tight_layout() # 그래프의 요소들이 서로 겹치지 않도록 여백을 자동으로 조정
# subplot에서 쓰지 않으면 label이 겹칠 수 있음

plt.show()

#%%
"""
# ============================================================
#  실습 ②  –  seaborn 그래프
# ============================================================
"""
# ── ② -A  체납액 데이터 ──────────────────────────────────

df_tax  = pd.read_csv('체납액Data.csv', encoding='CP949')

# Q1. 지역별 체납금액 막대 그래프
#     sns.barplot()으로 지역(x축)과 금액(y축)을 그리세요.
#     - palette='colorblind' 사용
#     - x축 눈금 90도 회전
#     힌트: sns.set_context("notebook") 먼저 설정하세요.

plt.figure(figsize=(10, 6))

# 여기에 코드를 작성하세요
sns.set_context('notebook')

sns.barplot(data=df_tax, x='지역', y='금액', palette='colorblind')
plt.xticks(rotation=45)

plt.show()

#%%
# Q2. 건수 상위 5개 지역 막대 그래프
#     건수 기준으로 내림차순 정렬 후 상위 5개 지역만 추출해
#     sns.barplot()으로 그리세요.
#     힌트: df_top5 = df_tax.sort_values(by=___, ascending=___).head(5)

plt.figure(figsize=(8, 5))

# 여기에 코드를 작성하세요
df_top5 = df_tax.sort_values(by='건수', ascending=False).head(5)
sns.barplot(data=df_top5, x='지역', y='금액')


plt.show()

#%%
# ── ② -B  mpg 데이터 ────────────────────────────────────
df_mpg  = pd.read_csv('mpg.csv')

# Q3. 시내연비(cty) 분포 히스토그램
#     sns.histplot()으로 cty 분포를 그리고 KDE 곡선도 함께 표시하세요.
#     힌트: kde=True 파라미터 사용

plt.figure(figsize=(8, 5))

# 여기에 코드를 작성하세요
sns.histplot(data=df_mpg, x='cty', kde=True)
plt.title('시내연비 분포 히스토그램')

plt.show()

#%%
# Q4. 실린더 수에 따른 시내연비 박스 플롯
#     sns.boxplot()으로 cyl(x축)과 cty(y축)를 그리세요.

plt.figure(figsize=(8, 5))

# 여기에 코드를 작성하세요
sns.boxplot(data=df_mpg, x='cyl', y='cty')
plt.title('실린더 수에 따른 시내연비 박스 플롯')

plt.show()

#%%
# Q5. [도전] 배기량 vs 시내연비 산점도 (구동방식 색상 구분)
#     sns.scatterplot()으로 displ(x축)과 cty(y축)를 그리세요.
#     hue='drv'로 구동방식별 색상을 구분하세요.

plt.figure(figsize=(8, 5))

# 여기에 코드를 작성하세요
sns.scatterplot(data=df_mpg, x='displ', y='cty', hue='drv')
# hue='drv'를 쓰면 drv를 기준으로 색상을 구별

plt.title('배기량 vs 시내연비 산점도 (구동방식 색상 구분)')


plt.show()

#%%
"""
# ============================================================
#  분석 도전  –  mpg.csv 시각화 5가지
# ============================================================
"""
# 단계 1. 히스토그램 + KDE
#         cty 분포를 sns.histplot(kde=True)으로 그리고
#         제목('시내연비 분포')과 축 레이블을 추가하세요.

plt.figure(figsize=(8, 5))

# 여기에 코드를 작성하세요
sns.histplot(data=df_mpg, x='cty', kde=True)
plt.title('시내연비 분포')
plt.xlabel('cty 분포')

plt.show()

#%%
# 단계 2. 박스 플롯
#         실린더(cyl) 수에 따른 cty 분포를 sns.boxplot()으로 그리세요.
#         제목: '실린더 수별 시내연비 분포'

plt.figure(figsize=(8, 5))

# 여기에 코드를 작성하세요
sns.boxplot(data=df_mpg, x='cyl', y='cty')
plt.title('실린더 수별 시내연비 분포')

plt.show()

#%%
# 단계 3. 바이올린 플롯
#         구동방식(drv)에 따른 cty 분포를 sns.violinplot()으로 그리세요.
#         박스 플롯과 어떤 차이가 있는지 확인하세요.
#         제목: '구동방식별 시내연비 분포 (바이올린)'

plt.figure(figsize=(8, 5))

# 여기에 코드를 작성하세요
sns.violinplot(data=df_mpg, x='drv', y='cty')
plt.title('구동방식별 시내연비 분포 (바이올린)')

plt.show()

# boxplot은 이상치 식별
# violinplot은 실제 분포 모양(밀도) 확인


#%%
# 단계 4. 선 그래프 (연도별 평균 시내연비)
#         연도(year)별 평균 cty를 계산한 후 sns.lineplot()으로 그리세요.
#         힌트: df_year = df_mpg.groupby('year')['cty'].mean().reset_index()

plt.figure(figsize=(7, 4))

# 여기에 코드를 작성하세요
df_year = df_mpg.groupby('year')['cty'].mean().reset_index()

sns.lineplot(data=df_year, x='year', y='cty')

plt.show()

#%%
# 단계 5. 산점도 (배기량 vs 시내연비, 구동방식 색상 구분)
#         sns.scatterplot()으로 displ(x축)과 cty(y축)를 그리세요.
#         hue='drv'로 색상을 구분하고 제목을 추가하세요.
#         제목: '배기량과 시내연비의 관계'

plt.figure(figsize=(9, 6))

# 여기에 코드를 작성하세요
sns.scatterplot(data=df_mpg, x='displ', y='cty', hue='drv')
plt.title('배기량과 시내연비의 관계')

plt.show()
