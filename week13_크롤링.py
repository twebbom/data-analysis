import requests
from bs4 import BeautifulSoup
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


# ============================================================
# [실습 1] HTML 분석 기초 — MyTest.html
# ============================================================

# 1-1) HTML 파일 읽기 # 로컬의 파일을 읽는 방식
with open('MyTest.html', 'r', encoding='utf-8') as file:
    html_content = file.read()
    
# 웹에서 읽어올 경우
# import request
# url = '주소'
# webpage = requests.get(url).text

soup = BeautifulSoup(html_content, 'html.parser')

# 1-3) class가 red인 요소 모두 찾기
red_texts = soup.find_all(class_='red')

# 1-4) 태그를 벗기고 글자만 출력
for text in red_texts:
    print(text.get_text())

# [확인] 출력 결과: 동백꽃 필 무렵

#%%
# ============================================================
# [실습 2] 체크포인트 ① 문제 풀기
# ============================================================
# 2-1) class가 green인 글자만 출력해 보세요
green_texts = soup.find_all(class_='green')
for text in green_texts:
    print(text.get_text())
# 2-2) find_all 대신 select로 같은 결과 만들기
# 힌트: CSS 선택자에서 클래스는 마침표(.)로 시작합니다
for text in soup.select('.green'):
    print(text.get_text())
# 2-3)  id가 text인 <div> 안의 모든 글자를 한 번에 출력
print(soup.select_one('#text').get_text())

#%%
# ============================================================
# [실습 3] 네이버 뉴스 랭킹 — STEP 1: requests로 접속
# ============================================================

# JTBC(437)의 '많이 본 뉴스' 페이지
code = 437
url = f'https://media.naver.com/press/{code}/ranking?type=popular'

webpage = requests.get(url).text
print(webpage)
#%%
soup = BeautifulSoup(webpage, 'html.parser')

#%%
# ============================================================
# [실습 5] STEP 3: 기사 목록 선택
# ============================================================

# 힌트: 기사 1건을 감싸는 요소는 <li class="as_thumb">
#       태그와 클래스를 함께 쓰는 선택자: 태그명.클래스명
items = soup.select('li.as_thumb')

# [확인] 기사 개수 확인 → 20이 나오면 성공
print(len(items))

#%%
# ============================================================
# [실습 6] STEP 4: 데이터프레임 만들기
# ============================================================
data = []
for item in soup.select('li.as_thumb'):
    # 힌트: 순위는 em.list_ranking_num, 제목은 strong.list_title,
    #       조회수는 span.list_view — 각각 1개씩이므로 select_one
    rank  = item.select_one('em.list_ranking_num').text
    title = item.select_one('strong.list_title').text
    views = item.select_one('span.list_view').text
    data.append({'순위': rank, '기사제목': title, '조회수': views})

# 힌트: 딕셔너리 리스트 → 데이터프레임
df = pd.DataFrame(data)
print(df.head(3))

#%%
# ============================================================
# [실습 7] STEP 5: 조회수를 숫자로 (전처리)
# ============================================================

# 잠깐! 조회수 칸이 비어 보이나요? 
print(repr(df['조회수'][0]))
 
# 1단계: '조회수' 글자 제거
df['조회수'] = df['조회수'].str.replace('조회수', '')
print(repr(df['조회수'][0]))
# 2단계: 쉼표(,) 제거
# 힌트: 1단계와 같은 함수, 지울 대상만 다름
df['조회수'] = df['조회수'].str.replace(',', '')
print(repr(df['조회수'][0]))
# 3단계: 앞뒤 줄바꿈·공백 제거
df['조회수'] = df['조회수'].str.strip()
print(repr(df['조회수'][0]))

# 4단계: 문자열 → 정수 변환 (청소가 다 끝난 뒤 마지막에!)
# 힌트: 시리즈의 자료형을 바꾸는 함수
df['조회수'] = df['조회수'].astype(int)
 
# [확인] 조회수 열이 int64면 성공
print(df.info())

#%%

# ============================================================
# [실습 8] 함수로 만들기 — getListNews
# ============================================================

def getListNews(press, code):
    # 1) 접속
    # 힌트: 문자열 앞의 f를 잊지 마세요! ({code}가 실제 값으로 바뀌려면 필수)
    url = f'https://media.naver.com/press/{code}/ranking?type=popular'
    response = requests.get(url)

    # 2) 파싱
    soup = BeautifulSoup(response.text, 'html.parser')

    # 3) 추출
    data = []
    for item in soup.select('li.as_thumb'):
        rank  = item.select_one('em.list_ranking_num').text
        title = item.select_one('strong.list_title').text
        views = item.select_one('span.list_view').text
        data.append({'순위': rank, '기사제목': title, '조회수': views})

    # 4) 정리
    df = pd.DataFrame(data)
    df['조회수'] = df['조회수'].str.replace('조회수', '') \
                   .str.replace(',', '').str.strip().astype(int)

    # 힌트: 어느 언론사 기사인지 표시하는 열 추가 (매개변수 press 사용)
    df['언론사'] = press
    return df

#%%

# [확인] 함수 동작 테스트 — 연합뉴스 20건이 나오면 성공
print(getListNews('연합뉴스', '422'))

#%%
# ============================================================
# [실습 9] 여러 언론사 한 번에 수집
# ============================================================

pressDt = {'MBC': '214', '연합뉴스': '422',
           'KBS': '056', 'JTBC': '437'}

newdf = pd.DataFrame()
for k, v in pressDt.items():
    # 힌트: 기존 newdf와 새로 수집한 결과를 세로로 이어 붙이는 함수 (12주차까지 자주 사용)
    newdf = pd.concat([newdf, getListNews(k, v)])

# [확인] 4개 언론사 x 20건 = 80 rows
print(newdf.shape)

#%%
# ============================================================
# [실습 10] 조회수 상위 10개 기사
# ============================================================

# 힌트: 내림차순 정렬은 ascending=False
newdf10 = newdf.sort_values('조회수', ascending=False).head(10)
print(newdf10)

# 상위 10개 안에 언론사별로 몇 건씩인지 세기
# 힌트: 범주별 개수를 세는 함수
print(newdf10.value_counts('언론사'))
print(newdf10['언론사'].value_counts())
#%%
# ============================================================
# [실습 11] 시각화 — 상위 10개 기사 그래프
# ============================================================

# 한글 폰트 설정 (이 줄이 없으면 제목이 네모(□)로 깨집니다!)
# ※ 코랩 사용자는 'Malgun Gothic' 대신 'NanumBarunGothic'
plt.rc('font', family='Malgun Gothic')

# 네이비 계열 팔레트
colors = ['#092D3D', '#314B98', '#6B9FD4', '#A8C4E0']

# 힌트: 가로 막대그래프 — 조회수를 x축, 기사제목을 y축에
sns.barplot(x='조회수', y='기사제목', hue='언론사',
            data=newdf10, palette=colors)
plt.xlabel('조회수')
plt.ylabel('')
plt.title('조회수 상위 10개 기사')
plt.show()


# 전처리
# 결측치
# concat
# 파생변수
# 시각화