# %%

# =============================================================================
# 실습 1. 쇼핑몰 데이터 산술 파생변수
# =============================================================================

import pandas as pd
df_o = pd.read_csv('mall_order.csv')

df = df_o.copy()

# 1. total 열 추가
df['total'] = df['price'] * df['qty']

# 2. discount_amt 열 추가
df['discount_amt'] = df['total'] * df['discount_rate'] / 100

# 3. final_price 열 추가
df['final_price'] = df['total'] - df['discount_amt']

# 4. 가장 비싼 주문 확인
idx = df['final_price'].idxmax()
df['customer'][idx]
df['product'][idx]
df.loc[idx,:]

df.loc[idx,['customer', 'product']]

# row = df.loc[df['final_price'].idxmax()]

# print(f'최고 결제 고객: {row['customer']}')
# print(f'최고 결제 상품: {row['product']}')


#%%

# =============================================================================
# 실습 2. 조건 파생변수
# =============================================================================

## 쇼핑몰 데이터
import numpy as np
# 1. 지역 간소화 열 추가 (서울 -> 수도권, 나머지 -> 지방)
df['region_simple'] = np.where(df['region']=='서울', '수도권', '지방')


# 2. 카테고리별 구매 건수가 가장 많은 category는?
print(df['category'].value_counts().idxmax())

df[df['grade']=='VIP']

df.query('grade == "VIP"')

# 3. 'VIP' 등급 고객만 추출해 고객명과 최종 금액 출력
conditions = [
    df['final_price'] >= 1000000,
    (df['final_price'] >= 300000) & (df['final_price'] < 1000000),
    df['final_price'] < 300000]
choices = ['VIP', '일반', '저가']

df['grade'] = np.select(conditions, choices, default='기타')

## mpg 데이터
df_mpg = pd.read_csv('mpg.csv')

# 1. cty + hwy 합산 연비 열 추가
df_mpg['y_p'] = df_mpg['cty'] + df_mpg['hwy']

# 2. 합산 연비 / 2 평균 연비 열 추가
df_mpg['avg_y'] = df_mpg['y_p'] / 2

# 3. 평균 연비 기준 등급 열 추가
#    (상: 25 이상 / 중: 18 이상 / 하: 18 미만)
conditions = [
    df_mpg['avg_y'] >= 25,
    (df_mpg['avg_y'] >= 18) & (df_mpg['avg_y'] < 25),
    df_mpg['avg_y'] < 18]
choices = ['상', '중', '하']

df_mpg['grade'] = np.select(conditions, choices, default='기타')

#%%

# =============================================================================
# 실습 3. 통합 실습: 파생변수 + query()
# =============================================================================

# 1. 할인율(discount_rate)이 10% 이상이고 final_price가 50만원 이상인 주문만 추출하세요.
df.query('discount_rate >= 10 and final_price >= 500000')

# 2. '전자기기' 카테고리에서 grade가 'VIP'인 고객 이름과 제품명을 출력하세요.
df.loc[(df['category'] == '전자기기') & (df['grade'] == 'VIP'),
       ['customer', 'product']]

# 3. 불쾌지수 단계가 '보통' 이상 (보통 / 높음 / 매우 높음)인 달은 총 몇 개월인지 구하세요.
df_sub = pd.read_excel("기상개황_20260701121753.xlsx")

df_sub['DI'] = (
    0.81 * df_sub['기온']
    + 0.01 * df_sub['습도'] * (0.99 * df_sub['기온'] - 14.3)
    + 46.3)

conditions = [
    df_sub['DI'] >= 80,
    (df_sub['DI'] >= 75) & (df_sub['DI'] < 80),
    (df_sub['DI'] >= 68) & (df_sub['DI'] < 75),
    df_sub['DI'] < 68]
choices = ['매우 높음', '높음', '보통', '낮음']
df_sub['DI_level'] = np.select(conditions, choices, default='기타')

print(df_sub.query('DI_level != "낮음"'))

# 4. 쇼핑몰 데이터에서 지역별(region) 평균 final_price를 계산하고 가장 높은 지역을 출력하세요.
print(df.groupby(['region'])['final_price'].mean())
print(df.groupby(['region'])['final_price'].mean().idxmax())


#%%

# =============================================================================
# 분석 도전 - midwest.csv
# =============================================================================

# 1. midwest.csv 불러오기
#    데이터 크기, 열 목록, 결측치 여부 파악
df_mid_o = pd.read_csv('midwest.csv')
df_mid = df_mid_o.copy()

df_mid.info()

df_mid.isnull().sum()
# 결측치 없음

# 2. 열 이름 변경
#    poptotal -> total, popasian -> asian
df_mid.rename(columns={'poptotal':'total', 'popasian':'asian'}, inplace=True)
df_mid.columns

# 3. 백분율 파생변수 추가
#    ratio = asian / total X 100 후 히스토그램 그리기
df_mid['ratio'] = df_mid['asian'] / df_mid['total'] * 100

# 4. 등급 파생변수 추가
#    ratio > 0.5 이면, 'large', 아니면 'small' (np.where)
df_mid['grade'] = np.where(df_mid['ratio'] < 0.5, 'large', 'small')

# 5. 빈도표 만들기
#    grade 열의 large / small 개수 확인
df_mid['grade'].value_counts()


