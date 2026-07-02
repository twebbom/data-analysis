import seaborn as sns
import matplotlib.pyplot as plt

# 데이터셋 로드
iris = sns.load_dataset("iris")

# 히스토그램
plt.figure(figsize=(8,6))
sns.histplot(iris['sepal_length'], bins=15, kde=True)
plt.title('히스토그램 (Sepal Length)')
#%%
# 박스 플롯
plt.figure(figsize=(8,6))
sns.boxplot(x='species', y='sepal_length', data=iris)
plt.title('박스플롯 (Sepal Length)')
#%%
# 바이올린 플롯
plt.figure(figsize=(8,6))
sns.violinplot(x='species', y='sepal_length', data=iris)
plt.title('바이올린플롯 (Sepal Length)')

#%%
# 히트맵
# 'species' 열을 제외한 나머지 열들을 서브셋으로 선택
plt.figure(figsize=(8,6))
subset = iris.drop(columns=['species'])
# 상관 행렬 계산
corr = subset.corr()
sns.heatmap(corr, annot=True, cmap='coolwarm', square=True)
#annot: 각 셀에 숫자 값을 표시할지 
#cmap: 히트맵의 색상 맵 'coolwarm', 'viridis', 'plasma'
plt.title('Iris 데이터의 상관관계 히트맵')

#%%
# 선 그래프 (Petal Length)
plt.figure(figsize=(8,6))
sns.lineplot(x=iris.index, y='petal_length', hue='species', data=iris)
#hue: 데이터를 구분할 기준, 색상의 다르게
plt.title('선그래프 (Petal Length)')

#%%
# 산점도
plt.figure(figsize=(8,6))
sns.scatterplot(x='sepal_length', y='sepal_width', hue='species', data=iris)
plt.title('산점도 (Sepal Length vs Sepal Width)')


