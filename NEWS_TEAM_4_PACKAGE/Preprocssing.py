import re


def preprocessing_korean(data):
    fi_da=re.sub("[^가-힣ㄱ-ㅎㅏ-ㅣ.*\\s]",'',data).replace('\xa0','')
    return fi_da