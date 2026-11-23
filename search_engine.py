import re
import unicodedata
from pathlib import Path
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

FIELDS = ['id','title','creators','collection','ean_isbn13','upc_isbn10','description','publisher','publish_date','group','tags','notes','age_group','ddc','call_number','copies']

def norm(value):
    return ''.join(c for c in unicodedata.normalize('NFKD',str(value).lower()) if not unicodedata.combining(c))

def load_catalog(path):
    df = pd.read_csv(path, dtype=str, keep_default_na=False).fillna('')
    for c in FIELDS:
        if c not in df: df[c] = ''
    df = df[df.title.str.strip().ne('')].drop_duplicates(subset=['id']).reset_index(drop=True)
    return df

class SearchEngine:
    def __init__(self, df):
        self.df=df
        self.texts=[]
        for _,r in df.iterrows():
            self.texts.append(norm(' '.join([r.title]*4+[r.creators]*3+[r.tags]*4+[r.group]*2+[r.description]*2+[r.publisher,r.publish_date,r.ddc,r.ean_isbn13,r.upc_isbn10])))
        self.word = TfidfVectorizer(ngram_range=(1,2),min_df=1,sublinear_tf=True,strip_accents='unicode',max_features=80000)
        self.char = TfidfVectorizer(analyzer='char_wb',ngram_range=(3,5),min_df=2,sublinear_tf=True,max_features=100000)
        self.wmat=self.word.fit_transform(self.texts)
        self.cmat=self.char.fit_transform(self.texts)

    def search(self,query,limit=24):
        q=norm(query.strip())
        if not q:return []
        ws=linear_kernel(self.word.transform([q]),self.wmat).ravel()
        cs=linear_kernel(self.char.transform([q]),self.cmat).ravel()
        score=.65*ws+.35*cs
        for i,r in self.df.iterrows():
            t=norm(r.title); a=norm(r.creators)
            if len(q)>3 and q in t: score[i]+=.5
            if len(q)>3 and q in a: score[i]+=.25
        inds=np.argsort(-score)[:limit]
        return [(self.df.iloc[int(i)].to_dict(),round(float(score[i]),4)) for i in inds if score[i]>.008]

def public_link():
    return 'https://www.libib.com/u/contenedor'

def compact_book(r,number):
    fields=['title','creators','description','tags','group','publisher','publish_date','age_group','ddc','ean_isbn13','copies']
    return {'numero':number,'id':r['id'],**{k:str(r.get(k,'') or '')[:950 if k=='description' else 180] for k in fields}}
