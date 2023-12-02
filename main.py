import sys
import os 
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from func.generalfunc import *
import logging
from fastapi import FastAPI, HTTPException

logger = logging.getLogger(__name__)
# Configure logging
logging.basicConfig(level=logging.INFO)

app = FastAPI()
cur_dir = os.path.curdir
vectorizer_path = os.path.join(cur_dir, "vectorizer/count_vectorizer.pkl")
loaded_count_vec = loadVectorizer(vectorizer_path)

model_path = os.path.join(cur_dir, "saved_model")
try:
    loaded_model = load_model(model_path)
except Exception as e:
    raise RuntimeError(f"Failed to load the model: {e}")

@app.get("/")
def index():
    logging.info("Request received at index endpoint.")
    return {"Tips:" : "This app can help you categorize sentiments into negative, neutral, or positive categories."}

@app.post("/process_text")
def process_text(text: str):
    logging.info(f"Processing text: {text}")
    try:
        newdataVector = preprocessNewdata(text, loaded_count_vec)
        res = np.argmax(loaded_model.predict(newdataVector))
        lookup = {0: "negative", 1: "neutral", 2: "positive"}
        result = {
            "Raw Text": text,
            "Categories": lookup[res]
        }
        logging.info(f"Processing result:{lookup[res]}")
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")

