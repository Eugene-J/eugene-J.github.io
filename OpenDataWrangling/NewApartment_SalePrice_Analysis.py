#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
# Korean font support
plt.rc("font", family = "AppleGothic")

# load csv and set encoding(cf. default encoding : utf-8) 
df_last = pd.read_csv("/Users/yujin/data analysis/data/주택도시보증공사_전국 평균 분양가격(2019년 12월).csv", encoding = "cp949")
df_first = pd.read_csv("/Users/yujin/data analysis/data/전국 평균 분양가격(2013년 9월부터 2015년 8월까지).csv", encoding = "cp949")


# check data
df_last.shape
df_last.head()
df_last.tail()
df_last.info()

df_first.shape
df_first.head()
df_first.tail()

# nan check
df_last.isnull().sum() 
df_last.isna().sum()

# Change data type to int
df_last["분양가격(㎡)"].astype(int)

# ValueError: invalid literal for int() with base 10: '  '
# Space's type is String. Can't change to int

pd.to_numeric(df_last["분양가격(㎡)"])

# ValueError: Unable to parse string "  "
# Can't change to Numeric either

# error option : 'coerce', then invalid parsing will be set as NaN
# change type to numeric forcely
# numpy's nan is float type
df_last["분양가격"] = pd.to_numeric(df_last["분양가격(㎡)"], errors = 'coerce')

# check result
df_last["분양가격"].mean()

# match the data type from the df_fist
# 두 데이터 셋의 단위를 통일(제곱미터당 분양가격 -> 평당분양가격)
df_last["평당분양가격"] = df_last["분양가격"] * 3.3
df_last.head(1)


df_last["분양가격(㎡)"].describe() # object 타입(공백 데이터도 count)
df_last["분양가격"].describe() # 수치데이터(공백은 결측치라서 non count)


# data cleansing
# 규모구분을 전용면적 컬럼으로 변경(같은 뜻인데 전용면적이라는 말이 더 직관적)
# 규모구분 컬럼에 포함된 '전용면적' word 제거
df_last["규모구분"].unique()
df_last["규모구분"].replace("전용면적", "")

#replace는 완벽하게 같은 문자만 바꿔 주므로 str을 사용해서 단어별 screening 필요

df_last["전용면적"] = df_last["규모구분"].str.replace("전용면적", "")

df_last["전용면적"] = df_last["전용면적"].str.replace("초과", "~")
df_last["전용면적"] = df_last["전용면적"].str.replace("이하", "")
#글자 사이공백, 글자 앞뒤의 공백까지 제거(str.strip())
df_last["전용면적"] = df_last["전용면적"].str.replace(" ", "").str.strip()

df_last["전용면적"]

# Drop unnecessary column
# axis 0:row, 1: column
df_last = df_last.drop(["규모구분", "분양가격(㎡)"], axis = 1)


# groupby 로 데이터 집계하기
#df.groupby(["인덱스로 사용할 컬럼"])["계산할 컬럼"].연산종류()
df_last.groupby(['지역명'])['평당분양가격'].mean()
df_last.groupby(['지역명'])['평당분양가격'].max()
df_last.groupby(['지역명'])['평당분양가격'].min()
df_last.groupby(['지역명'])['평당분양가격'].describe()


# 전용면적 당 평당분양가격의 평균
df_last.groupby(["전용면적"])['평당분양가격'].mean()


# 지역별, 전용면적 당 평당분양가격의 평균(two indexes)
df_last.groupby(["지역명", "전용면적"])['평당분양가격'].mean()


# 전용면적 행을 열 카테로리로 changable
df_last.groupby(["지역명", "전용면적"])['평당분양가격'].mean().unstack()

# 소수점 없애기
df_last.groupby(["지역명", "전용면적"])['평당분양가격'].mean().unstack().round()

# 연도, 지역 당 평당분양가격의 평균
df_last.groupby(["연도", "지역명"])["평당분양가격"].mean().unstack()

# 행, 렬을 바꾸고 싶으면 .T , .transpose()
df_last.groupby(["연도", "지역명"])["평당분양가격"].mean().unstack().T


# pivot table로 groupby와 같은 결과 만들기. groupby : series. 속도가 약간 더 빠름 / pivot_table : data frame
# default aggfunc = mean
# 지역별 평당분양가격의 평균(two indexes)
pd.pivot_table(df_last, index = ["지역명"], values = ["평당분양가격"], aggfunc = "count")

# 전용면적 당 평당분양가격의 평균
# df_last.groupby(["전용면적"])['평당분양가격'].mean()
# pivot : 연산 하지 않고 데이터 형태만 바꿈 aggfunc가 없음 , pivot_table : aggfunc 있음
pd.pivot_table(df_last, index = "전용면적", values = "평당분양가격")

#df_last.groupby(["지역명", "전용면적"])['평당분양가격'].mean().round()
df_last.pivot_table(index = ["전용면적", "지역명"], values = "평당분양가격")

#df_last.groupby(["지역명", "전용면적"])['평당분양가격'].mean().unstack().round()
df_last.pivot_table(index = "전용면적", columns = "지역명", values = "평당분양가격").round()

#df_last.groupby(["연도", "지역명"])["평당분양가격"].mean()
p = pd.pivot_table(df_last, index = ["연도", "지역명"], values = "평당분양가격")
p.loc[2019] # index 기준으로 가져오기


# =========Visualization using matplotlib=========

# 지역별 분양가격 평균
# line graph, bar graph
# 분양가 높은 순으로 sort
g = df_last.groupby(["지역명"])["평당분양가격"].mean().sort_values(ascending = False)

# line graph
g.plot()

# bar graph
# same as g.plot(kind = "bar")
g.plot.bar(rot = 0, figsize = (10, 3)) # 아래 글씨 가로로, 그림 사이즈 지정

# 전용면적 별 평당분양가격 평균
df_last.groupby(["전용면적"])["평당분양가격"].mean().plot.bar()

# 연도별 평당분양가격 평균
df_last.groupby(["연도"])["평당분양가격"].mean().plot.bar()

# box plot by year
df_last.pivot_table(index = "연도", values = "평당분양가격")
df_last.pivot_table(index = "월", columns = "연도", values = "평당분양가격").plot.box()
p = df_last.pivot_table(index = "월", columns = ["연도", "전용면적"], values = "평당분양가격")
p.plot.box(rot = 30, figsize = (15, 3))

# pivot
p = df_last.pivot_table(index = "월", columns = "연도", values ="평당분양가격")
p.plot()


# ==========Visualization using Seaborn============

# bar plot

# 지역별 평당분양가격 
plt.figure(figsize = (10, 3))
# bar plot's default estimator : mean
# ci (신뢰구간) : 95. 이상치값 5%를 제거한 95%. 시간 좀 걸림
# ci = "sd" 표준편차를 보여줌
sns.barplot(data = df_last, x = "지역명", y = "평당분양가격", ci = None, color = "b")


# 연도별 평당분양가격
sns.barplot(data = df_last, x = "연도", y = "평당분양가격")

# hue : 카테고리 별로 색상을 나누어줌. 카테고리가 적을 때 써야 효과적
plt.figure(figsize = (15, 5))
sns.lineplot(data = df_last, x = "연도", y = "평당분양가격", hue = "지역명")

# 범례를 별도 표기하는 법(그래프에서 얼만큼 떨어지게 할건지
plt.legend(bbox_to_anchor = (1.02, 1), loc = 2, borderaxespad = 0.)

# 지역별로 subplot 그리기
# col = 어떤 기준으로 subplot 그릴건지?
sns.relplot(data = df_last, x = "연도", y = "평당분양가격", 
            hue = "지역명", kind = "line", col = "지역명", 
            col_wrap = 4, ci = None)

# 연도별 평당 가격을 지역별로 subplot bar chart로 표현
sns.catplot(data = df_last, x = "연도", y = "평당분양가격", kind = "bar",
           col = "지역명", col_wrap = 4)


# box plot
sns.boxplot(data = df_last, x = "연도", y = "평당분양가격")

# hue 사용해서 전용면적별로
plt.figure(figsize = (12, 3))
sns.boxplot(data = df_last, x = "연도", y = "평당분양가격", hue = "전용면적")

# violin plot (box plot에 밀도추정 값을 같이 볼수 있다)
sns.violinplot(data = df_last, x = "연도", y = "평당분양가격")

# ### lmplot & swarmplot
# 연도별 평당분양가격을 lmplot으로
#regplot (scatterplot에 회기선(양 또는 음의 상관관계 있는지) 추가된것)
sns.regplot(data = df_last, x = "연도", y = "평당분양가격")

# scatterplot
sns.scatterplot(data = df_last, x = "연도", y = "평당분양가격")

# regplot, lmplot, swarmplot
# lmplot : regplot에 hue값을 쓸 수 있게 만든것. 
# x, y축 모두 수치 데이터 일때 쓰는 게 적합
sns.lmplot(data = df_last, x = "연도", y = "평당분양가격", hue = "전용면적",
          col = "전용면적", col_wrap = 3)

# swarmplot 카테고리형 데이터의 산점도 표현에 적합
plt.figure(figsize = (15, 3))
sns.swarmplot(data = df_last, x = "연도", y = "평당분양가격", hue = "전용면적")


# ### 이상치 보기
df_last["평당분양가격"].describe()
max_price = df_last["평당분양가격"].max()

# 평당분양가격의 max값을 가지는 행 가져오기
df_last[df_last["평당분양가격"] == max_price]


# # Histogram
# binning(bucketing) : 수치데이터 -> 카테고리 데이터로 바꾸는 것
h = df_last["평당분양가격"].hist()

# distplot
sns.distplot(df_last["평당분양가격"])
# ValueError: cannot convert float NaN to integer
# 결측치가 있어서 distplot으로 변환 안됨

# 결측치 없애기
df_last["평당분양가격"].notnull()
# 결측치 없앤 데이터에서 평당분양가격만 가져옴
price = df_last.loc[df_last["평당분양가격"].notnull(), "평당분양가격"]

sns.distplot(price)

# displot을 ridge plot(산마루모양)으로 그리기
# subplot으로 표현해 준다
g = sns.FacetGrid(df_last, row = "지역명",
                 height = 1.7, aspect = 4,)
g.map(sns.distplot, "평당분양가격", hist = False, rug = True)

# rug : 아래에 카펫처럼 빈도수 보여줌
# sns.distplot(price, hist = False, rug = True)
sns.kdeplot(price, cumulative = True) # rug는 없지만 cumulative로 누적수 볼수 있음

# pairplot
                            # 행, 렬 같이 가져오려면 loc를 써야함
df_last_notnull = df_last.loc[df_last["평당분양가격"].notnull(), #행
                          ["연도", "월", "평당분양가격", "지역명", "전용면적"]] #열
sns.pairplot(df_last_notnull, hue = "지역명")

# 전용면적별 데이터 수 집계
df_last["전용면적"].value_counts()

# 데이터 컬럼 보이는 개수 지정 가능
pd.options.display.max_columns = 25

# null check
df_first.isnull().sum()


# # Tidy Data
# ## melt를 사용해 두개의 data set 합치기
df_first_melt = df_first.melt(id_vars = "지역", var_name = "기간", value_name = "평당분양가격")

df_first_melt.head()

# 컬럼 명을 df_last와 일치시켜준다
df_first_melt.columns = ["지역명", "기간", "평당분양가격"]
df_first_melt.head(1)

# 연도와 월 분리하기
date = "2013년12월"
date.split("년")[1] # default : 공백을 기준으로 나눔. list 형태로 반환

# 연도가져오기
date.split("년")[0]

# 월
date.split("년")[-1].replace("월", "") # 마지막이라서 -1

# 연도 반환 함수 생성. int로 반환하도록.
def parse_year(date):
    year = int(date.split("년")[0])
    return year

parse_year(date)

# 월 반환 함수 생성.
def parse_month(date):
    month = int(date.split("년")[-1].replace("월", ""))
    return month

parse_month(date)

# Create new column
# apply 사용해서 새로운 데이터 컬럼 생성
df_first_melt["연도"] = df_first_melt["기간"].apply(parse_year)
df_first_melt["월"] = df_first_melt["기간"].apply(parse_month)

df_last.columns.to_list() #리스트 형태로 반환해줌
#필요한 컬럼들
cols = ['지역명', '연도', '월', '평당분양가격']

# concat 으로 데이터 프레임 합치기
# 기준 : 이전 데이터에는 전용면적이 없으므로 최신 데이터 중 전용면적이 '전체'인 것만 가져온다
# loc를 이용해서 행은 전용면적이 '전체'인 데이터, 컬럼은 위에서 지정한 컬럼들로
# 백업의 개념으로 copy로 가져오자
df_last_prepare  = df_last.loc[df_last["전용면적"] == "전체", cols].copy()
df_last_prepare.head(1)

df_first_prepare = df_first_melt[cols].copy()
df_first_prepare.head(1)

df = pd.concat([df_first_prepare, df_last_prepare])
df.shape
df.tail()
df["연도"].value_counts(sort = False)
# 2013, 2015년은 데이터가 누락 된걸 확인 할 수 있다.


# # Pivot table
#연도를 인덱스로, 지역명을 컬럼으로, 평당분양가격을 피봇테이블로
t = pd.pivot_table(df, index = "연도", columns = "지역명", values = "평당분양가격").round()
t

# # heat map
plt.figure(figsize = (15, 7))
sns.heatmap(t, cmap = "Blues", annot = True, fmt = ".0f") #fmt : 포맷지정 ex.float형태로 소숫점 없이

#transpose
t.T

sns.heatmap(t.T, cmap = "Blues", annot = True, fmt = ".0f")

# groupby로 그려보기
# unstack : 마지막 인덱스를 컬럼명으로 만들어줌
g = df.groupby(["연도", "지역명"])["평당분양가격"].mean().unstack().round()

plt.figure(figsize = (15, 7))
sns.heatmap(g.T, annot = True, fmt = ".0f", cmap = "Greens")


# ========연도별 평당 분양 가격 시각화

# ## bar plot
sns.barplot(data = df, x = "연도", y = "평당분양가격")

# ## pointplot
plt.figure(figsize = (12, 6))
sns.pointplot(data = df, x = "연도", y = "평당분양가격", hue = "지역명")
plt.legend(bbox_to_anchor = (1.02, 1), loc = 2, borderaxespad = 0.)

df_seoul = df[df["지역명"] == "서울"].copy()
sns.barplot(data = df_seoul, x = "연도", y = "평당분양가격", color = "b")
sns.pointplot(data = df, x = "연도", y = "평당분양가격")

# ## box plot
sns.boxplot(data = df, x = "연도", y = "평당분양가격")
sns.boxenplot(data = df, x = "연도", y = "평당분양가격")

# ## violin plot
plt.figure(figsize = (10, 4))
sns.violinplot(data = df, x = "연도", y = "평당분양가격")
# 하얀 점 : 중앙 값


# ## swarmplot
plt.figure(figsize = (12, 6))
sns.swarmplot(data = df, x = "연도", y = "평당분양가격", hue = "지역명")
plt.legend(bbox_to_anchor = (1.02, 1), loc = 2, borderaxespad = 0.)

plt.figure(figsize = (12, 6))
sns.violinplot(data = df, x = "연도", y = "평당분양가격")
sns.swarmplot(data = df, x = "연도", y = "평당분양가격", hue = "지역명")
plt.legend(bbox_to_anchor = (1.02, 1), loc = 2, borderaxespad = 0.)

# ## lmplot
sns.lmplot(data = df, x = "연도", y = "평당분양가격")


# # =========지역별 평당분양가격 시각화

# ## barplot
sns.barplot(data = df, x = "지역명", y = "평당분양가격")

# ## box plot
sns.boxplot(data = df, x = "지역명", y = "평당분양가격")
sns.boxenplot(data = df, x = "지역명", y = "평당분양가격")

# ## violin plot
plt.figure(figsize = (12, 4))
sns.violinplot(data = df, x = "지역명", y = "평당분양가격")

# ## swarm plot
plt.figure(figsize = (12, 4))
sns.swarmplot(data = df, x = "지역명", y = "평당분양가격", hue = "연도")
