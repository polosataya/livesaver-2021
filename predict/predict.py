#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pandas as pd
import joblib
from catboost import CatBoostClassifier
from sklearn.feature_extraction.text import TfidfVectorizer


#Путь к файлам
path = ''
#Название тестового файла
testfile = 'test.csv'

def get_features(df: pd.DataFrame) -> pd.DataFrame:
    """Построение мешка слов TfidfVectorizer"""

    # Загружаем модель tfidf
    tfidf = TfidfVectorizer() 
    tfidf = joblib.load(path + 'tfidf.pkl') 
    
    #Загружаем тестовый датасет
    test = pd.read_csv(path + testfile, index_col=0)
    
    #Преобразуем текст
    test_tfidf = tfidf.transform(test.text)
    test_tfidf = pd.DataFrame(test_tfidf.toarray(), columns = feature_names, index = test.index)
    
    return test, test_tfidf

def predict(df: pd.DataFrame) -> pd.DataFrame:
    """Построение прогноза по тестовым данным"""

    # Загружаем модель сatboost
    cat_clf = CatBoostClassifier() 
    cat_clf.load_model(path + 'cat_clf.cbm')
    
    #Получаем фичи
    test, test_tfidf = get_features(df: pd.DataFrame)

    #Делаем прогноз
    cat_predict = cat_clf.predict_proba(test_tfidf)[:,1]    
    test['predict'] = cat_predict

    #Сохраняем таблицу с прогнозом для приложения
    df = valid.sort_values(['predict'], ascending = False)
    df.to_csv('df.csv', index=True)
