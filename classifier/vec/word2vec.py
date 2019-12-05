## create word2vec
import pandas as pd
import numpy as np
from gensim.models import Word2Vec
from sklearn.preprocessing import normalize
import sys
import re

def train(token, num_features=200, min_word=10, num_worker=40, window=10, downsampling=1e-3):
    print("train model ...")
    model = Word2Vec(token, workers=num_worker, hs = 0, sg = 1, negative = 10, iter = 25,\
            size=num_features, min_count = min_word, \
            window = window, sample =downsampling, seed=1, compute_loss = True)
    model.init_sims(replace=True)
    return model
    
def save_model(model, filename):
    print("save model ...")
    model.save(f"./{filename}")

def load_model(filename):
    print("load model ... ")
    model = Word2Vec.load(f"./{filename}")
    return model

def createVector(df, model, num_features=200):
    print("create vector ... ")
    x = np.empty((0, num_features))
    for idx, (text, label, _) in df.iterrows():
        tmp = np.array([ np.array(model.wv[word])  for word in text.split(",") if word in model.wv.vocab ])
        if len(tmp) != 0:
            x = np.append(x, np.mean(tmp, axis=0).reshape(1, num_features), axis=0)
        else:
            x = np.append(x, np.zeros((1, num_features)), axis=0)
    return x

if __name__ == "__main__":
    f = "word2vec_min1"
    PATH = "../data/train-val-wakati-juman.tsv"
    df = pd.read_table(PATH, index_col=0)
    df = df[~pd.isnull(df["text"])]
    token = df["text"].apply(lambda x: x.split(","))
    model = train(token, min_word=1)
    save_model(model, f)
    #model = load_model(f)
    x = createVector(df, model)
    np.save(f"./{f}_x.npy", x)
    np.save(f"./{f}_y.npy", np.array(df["label"]))
