import matplotlib.pyplot as plt

# 데이터 생성
x = [1, 2, 3, 4, 5]
y = [2, 3, 5, 7, 11]

# 그래프 생성
plt.plot(x, y, label='데이터')
# y=4 위치에 수평선 추가
plt.axhline(y=4, color='r', linestyle='--', linewidth=2, label='y=4 기준선')

plt.title('axhline 예제')
plt.legend()

# 그래프 출력
plt.show()
#%%
import matplotlib.pyplot as plt

# 데이터 생성
x = [1, 2, 3, 4, 5]
y = [2, 3, 5, 7, 11]

# 그래프 생성
plt.plot(x, y, label='데이터')

# x=3 위치에 수직선 추가
plt.axvline(x=3, color='g', linestyle='--', linewidth=2, label='x=3 기준선')

plt.title('axvline 예제')
plt.legend()

# 그래프 출력
plt.show()
