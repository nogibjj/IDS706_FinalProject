import sys
import os 
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import logging
import numpy as np
import sklearn
from fastapi import FastAPI,HTTPException
import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import os
import joblib
from keras.models import load_model

def loadVectorizer(vectorizer_path):
    loaded_count_vec = joblib.load(vectorizer_path) 
    return loaded_count_vec

def preprocessNewdata(raw_string, loaded_count_vec):
    new_data = pd.Series(raw_string)
    new_data_vec = loaded_count_vec.transform(new_data).todense()
    return new_data_vec

def loadModel(save_path):
    loaded_model= load_model(save_path)
    return loaded_model


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

cur_dir = os.path.curdir
vectorizer_path = os.path.join(cur_dir, "vectorizer/count_vectorizer.pkl")
loaded_count_vec = loadVectorizer(vectorizer_path)

model_path = os.path.join(cur_dir, "saved_model")
try:
    loaded_model = load_model(model_path)
except Exception as e:
    raise RuntimeError(f"Failed to load the model: {e}")
app = FastAPI()

@app.post("/")
def process_text(event,context):
    
    text = event.get('payload',"")
    logging.info(f"Processing text: {text}")
    newdataVector = preprocessNewdata(text, loaded_count_vec)
    res = np.argmax(loaded_model.predict(newdataVector))

    lookup = {0: "negative", 1: "neutral", 2: "positive"}
    result = {
        "Raw Text": text,
        "Categories": lookup[res]
    }
    print(result)
    logging.info(f"Processing result:{lookup[res]}")
    return result
