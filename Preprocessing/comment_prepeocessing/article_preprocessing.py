import pandas as pd
import re
from konlpy.tag import Mecab


def preprocessing_korean(data):
    fi_da=re.sub("[^가-힣ㄱ-ㅎㅏ-ㅣ.*\\s]",'',str(data)).replace('\xa0','')
    return fi_da

def mecab_morphs(data):
    pos_list = {'NNG', 'VA', 'VAX', 'MAG', 'VV'}
    mecab = Mecab()
    data_token = mecab.morphs(data)
    f = open('./stopwords-ko.txt', 'r')
    lines = f.readlines()
    
    stopwords_list= []
    for l in lines:
        l = l.replace('\n','')
        stopwords_list.append(l)
    
    result = []
    for token in data_token:
        if token not in stopwords_list:
            result.append(token)
    
    token_result = ''.join(result)
    pos_token = mecab.pos(token_result)
    pos_result = []
    for p in pos_token:
        if p[1] in pos_list:
            pos_result.append(p[0])
    pos_result = list(set(pos_result))
    
    return pos_result

def article_preprocessing(news_df): 
    '''
    데이터 프레임 각 기사 내용 전처리
    '''
    c= news_df['Content']
    content = pd.DataFrame(data=c, columns=['Content'])
    content['Content'].apply(lambda x: str(x))
    content['cleansing'] = content['Content'].apply(lambda x : preprocessing_korean(x))
    content['preprocessing'] = content['cleansing'].apply(lambda x : mecab_morphs(x))
    news_df['preprocessing'] = content['preprocessing'].apply(lambda x : ' '.join(x))
    print(news_df)
    return news_df

def create_stopword(news_df):
    '''
    불용어 사전 만드는 함수
    '''
    writer = news_df['Writer'].unique()
    press = news_df['Press'].unique()

    f = open('./stopwords-ko.txt', 'a+')
    #기자 이름 불용어 사전에 추가
    for i in writer:
        i = re.sub("[^가-힣ㄱ-ㅎㅏ-ㅣ.*\\s]",' ',i)
        i = i.split(' ')
        for name in i:
            if len(name) == 3:
                f.write(name+'\n')
    #언론사 이름 불용어 사전에 추가
    for j in press:
        j = str(j)
        re.sub("[^가-힣ㄱ-ㅎㅏ-ㅣ.*\\s]",'',j)
        f.write(j+'\n')
    f.close()

def trim_df(df):
    df.dropna(axis=0)
    df['preprocessing'].nunique()
    df.drop_duplicates(['preprocessing'], keep = 'first')
    df.drop(['Content'], axis=1, inplace=True)
    df = df.rename(columns={'preprocessing':'Content'})
    return df

news_df = pd.read_csv('./Article_news.csv') #뉴스 기사 있는 csv파일
result_df = article_preprocessing(news_df) #원래 데이터 프레임 + 전처리된 내용
preprocessed_df = trim_df(result_df)
preprocessed_df.to_csv('Article_news_preprocessing.csv')
