import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import re
import json
from konlpy.tag import Okt
from keras.preprocessing.sequence import pad_sequences
from keras.models import load_model
from keras.preprocessing.text import Tokenizer

okt = Okt()
tokenizer  = Tokenizer()
        
class EmotionAnalysis :
    def analyze_emotion(self):

        DATA_CONFIGS = 'data_configs.json'
        prepro_configs = json.load(open('./TEA-Time-AI/model/data/CLEAN_DATA/'+DATA_CONFIGS,'r'))
        tokenizer.fit_on_texts(prepro_configs['vocab'])

        MAX_LENGTH = 8 # 문장최대길이
        sentence = input('감성분석할 문장을 입력해 주세요.: ')
        sentence = re.sub(r'[^ㄱ-ㅎㅏ-ㅣ가-힣\\s ]','', sentence)
        stopwords = ['은','는','이','가','하','아','것','들','의','있','되','수','보','주','등','한'] # 불용어 추가할 것이 있으면 추가
        sentence = okt.morphs(sentence, stem=True) # 토큰화
        sentence = [word for word in sentence if not word in stopwords] # 불용어 제거
        vector  = tokenizer.texts_to_sequences(sentence)
        pad_new = pad_sequences(vector, maxlen = MAX_LENGTH) # 패딩

        # model.load_weights('./data/DATA_OUT/cnn_classifier_kr/weights.h5') # 모델 불러오기
        '''
        with open('./TEA-Time-AI/model/model.pkl', 'rb') as model_file:
            model = pickle.load(model_file)
        '''
        model = load_model('./TEA-Time-AI/model/')
        model.load_weights('./TEA-Time-AI/model/data/DATA_OUT/cnn_classifier_kr/weights.h5')
        predictions = model.predict(pad_new)

        # print(sentence)
        # print(predictions)

        # 주어진 결과값
        emotions = np.array(predictions)

        # 감정 레이블
        emotion_labels = ['불안', '분노', '기쁨']

        # 감정 요약 함수
        def summarize_emotion(emotions, threshold=0.35): # 임계값 설정
            summary = []
            for e in emotions:
                dominant_emotion = np.argmax(e)  # 가장 높은 점수의 감정 인덱스
                if e[dominant_emotion] > threshold:  # 임계값 이상의 점수만을 고려
                    summary.append(emotion_labels[dominant_emotion])
            return summary

        # 전체적인 기분 요약
        overall_summary = summarize_emotion(emotions)
        # print(overall_summary)

        # 실제 감정 데이터와 레이블
        emotions = np.array(predictions)
        emotion_labels = ['Anxiety', 'Anger', 'Pleasure']

        # 실제 요약된 감정 데이터
        overall_summary = summarize_emotion(emotions)

        # 요약된 감정 빈도 계산
        emotion_counts = {emotion: overall_summary.count(emotion) for emotion in emotion_labels}
        print(emotion_counts)

        # 그래프 그리기
        '''
        plt.figure(figsize=(8, 6))
        plt.bar(emotion_labels, [emotion_counts[emotion] for emotion in emotion_labels], color='skyblue')
        plt.xlabel('Emotion')
        plt.ylabel('Frequency')
        plt.title('Emotion Graph')
        plt.show()
        '''
