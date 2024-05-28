import matplotlib.pyplot as plt
import pandas as pd
from prophet import Prophet
import matplotlib.font_manager as fm
import streamlit as st


def formChart(total_df) :
    st.markdown('## 가구 형태별 가격 추세 \n')
    # 한글 폰트 설정
    path = 'C:\\Windows\\Fonts\\H2MJRE.TTF'
    fontprop = fm.FontProperties(fname=path, size=12)

    total_df['DEAL_YMD'] = pd.to_datetime(total_df['DEAL_YMD'], format='%Y-%m-%d')
    types = total_df['HOUSE_TYPE'].unique()
    periods = 28

    # 플롯 설정
    fig, ax = plt.subplots(figsize=(10, 6), sharex=True, ncols=2, nrows=2)

    # 주거 유형별 예측
    for i, house_type in enumerate(types):
        # 프로핏 모델 객체 인스턴스 만들기
        model = Prophet()
        
        # 훈련 데이터 준비
        total_df2 = total_df[total_df['HOUSE_TYPE'] == house_type][['DEAL_YMD', 'OBJ_AMT']]
        summary_df = total_df2.groupby('DEAL_YMD')['OBJ_AMT'].mean().reset_index()
        summary_df = summary_df.rename(columns={'DEAL_YMD': 'ds', 'OBJ_AMT': 'y'})
        
        # 모델 학습
        model.fit(summary_df)
        
        # 예측 데이터 준비 및 예측
        future = model.make_future_dataframe(periods=periods)
        forecast = model.predict(future)
        
        # 서브플롯 위치 계산
        x = i // 2
        y = i % 2
        
        # 예측치 시각화
        fig = model.plot(forecast, uncertainty=True, ax=ax[x, y])
        ax[x, y].set_title(f'서울시 {house_type} 평균 가격 예측 시나리오 {periods}일간', fontproperties=fontprop)
        ax[x, y].set_xlabel('날짜', fontproperties=fontprop)
        ax[x, y].set_ylabel('평균가격(만원)', fontproperties=fontprop)
        
        # x축 레이블 회전
        for tick in ax[x, y].get_xticklabels():
            tick.set_rotation(30)

    # 레이아웃 조정 및 저장
    plt.tight_layout()
    plt.savefig('m01.png', dpi=200)
    plt.show()
