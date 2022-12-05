import re

import pandas as pd
path = '파일경로'
data = pd.read_csv(path)
title = data['Title']
data['engkor'] = 0 #영어1, 한국어0

for t in title:
    reg = re.compile(r'[a-zA-Z]')
    e_sum = 0
    for i in t:
        if reg.match(i):
            e_sum +=1
    if e_sum > len(t)*0.5:
        data.loc[data['Title'] == t, 'engkor'] == 1
        pass
    else:
        pass

con1 = data['engkor'] == 1
a = data.loc[con1, 'Content']
a.to_csv('파일경로')