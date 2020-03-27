#!/usr/bin/env python
# coding: utf-8

import warnings
warnings.filterwarnings('ignore', category = UserWarning)

import pandas as pd
import missingno as msno
# conda install -c conda-forge missingno
import folium

import matplotlib.pyplot as plt
import seaborn as sns

# 실습환경에 맞는 한글폰트 설정을 해주세요.
# Window 의 한글 폰트 설정
# plt.rc('font',family='Malgun Gothic')
# Mac 의 한글 폰트 설정
plt.rc('font', family='AppleGothic')

get_ipython().run_line_magic('matplotlib', 'inline')
get_ipython().run_line_magic('ls', 'data')


# # 2016년 상권별 업종 밀집 통계
# data load
shop = pd.read_csv("/Users/yujin/data analysis/data/상권별 업종밀집통계(2016).csv", 
                   encoding = "cp949",)

shop.shape
shop.head()

# # 상가업소정보 2018년 6월
#data load
shop_2018_01 = pd.read_csv("/Users/yujin/data analysis/data/소상공인시장진흥공단_상가업소정보_201806_01.csv", 
                   encoding = "cp949",)

shop_2018_01.head()
shop_2018_01.columns

cols = ['상호명', '지점명', '상권업종대분류명', '상권업종중분류명', '상권업종소분류명', 
        '시도명', '시군구명', '행정동명', '지번주소', '경도', '위도']
shop_2018_01[cols]

# null check
shop_2018_01.isnull().sum()

# 결측치 볼때 유용
msno.matrix(shop_2018_01)

#1000개만 위도, 경고를 산점도로
shop_2018_01[:1000].plot.scatter(x = "경도", y = "위도", grid = True)

# 산점도를 봤을때 두 개의 지역만 데이터에 있는 것으로 추측. 확인해 보자.
# 서울 데이터만 추출.
shop_seoul = shop_2018_01.loc[shop_2018_01['도로명주소'].str.startswith('서울')]
shop_except_seoul = shop_2018_01.loc[~shop_2018_01['도로명주소'].str.startswith('서울')]

# 서울이다
shop_seoul.plot.scatter(x='경도', y='위도', figsize=(16, 12), grid=True)

# 도로명 주소를 기준으로 시도, 구군으로 나누기
shop_2018_01['도로명주소'].head()

shop_2018_01['도로명주소'].str.split(' ')[0]
shop_2018_01['시도'] = shop_2018_01['도로명주소'].str.split(' ', expand = True)[0]
shop_2018_01['구군'] = shop_2018_01['도로명주소'].str.split(' ', expand = True)[1]


plt.figure(figsize=(16, 12))
sns.scatterplot(data=shop_seoul[:10000], x='경도', y='위도', hue='시군구명')

shop_seoul['상권업종대분류명'].value_counts()

plt.figure(figsize=(16, 12))
sns.scatterplot(data=shop_seoul[:10000], x='경도', y='위도', hue='상권업종대분류명')


# # 학문, 교육 업종 보기
shop_seoul_edu = shop_seoul[shop_seoul['상권업종대분류명'] == '학문/교육']

plt.figure(figsize = (16, 12))
sns.scatterplot(data = shop_seoul_edu, x = "경도", y = "위도", hue = "상권업종중분류명")


# ## 학원-컴퓨터만 보기

plt.figure(figsize = (16, 12))
shop_seoul_edu_computer = shop_seoul_edu[shop_seoul_edu['상권업종중분류명'] == '학원-컴퓨터']
sns.scatterplot(data = shop_seoul_edu_computer, x = "경도", y = "위도", hue = "상권업종중분류명")


# 지도 위에 팝업으로 마커 보여주는 함수
def show_marker_map(geo_df) :
    
    map = folium.Map(location = [geo_df['위도'].mean(), geo_df['경도'].mean()],
                     zoom_start = 12, # 1 = worldwide
                     tiles = 'Stamen Terrain')#스타일 지정
    
    for n in geo_df.index :
        shop_name = geo_df.loc[n, '상호명'] + "-" + geo_df.loc[n, '도로명주소']
        
        folium.Marker([geo_df.loc[n,'위도'],
                       geo_df.loc[n, '경도']],
                       tooltip = shop_name).add_to(map)
    
    map.save('index.html') #한글 폰트 깨져서 임시방편
    
    return map

show_marker_map(shop_seoul_edu_computer)


# # 부동산 업종 보기
shop_seoul_realestate = shop_seoul[shop_seoul['상권업종대분류명'] == '부동산']
plt.figure(figsize=(16,12))
sns.scatterplot(data = shop_seoul_realestate, x ="경도", y = "위도", hue = '상권업종중분류명')


# # 편의점, 카페 분포
shop_seoul_eat = shop_seoul[shop_seoul['상권업종중분류명'] == '커피점/카페']

plt.figure(figsize=(16, 12))
sns.scatterplot(data=shop_seoul_eat, x='경도', y='위도', hue='시군구명')


# ## 중구만 보기
geo_df = shop_seoul_eat[shop_seoul_eat["시군구명"] == "중구"]

map = folium.Map(location=[geo_df['위도'].mean(), 
                           geo_df['경도'].mean()], 
                 zoom_start=16, tiles='Stamen Terrain')

for n in geo_df.index:
    shop_name = geo_df.loc[n, '상호명'] + ' - ' + geo_df.loc[n, '도로명주소']
    folium.Marker([geo_df.loc[n, '위도'], geo_df.loc[n, '경도']], 
                  popup=shop_name).add_to(map)

map


# # 서울 외 지역보기

shop_except_seoul.head()
shop_except_seoul['구군'] = shop_except_seoul['도로명주소'].str.split(" ", expand = True)[1]

plt.figure(figsize= (10, 6))
sns.scatterplot(data=shop_except_seoul, x = '경도', y = '위도', hue = '구군')
