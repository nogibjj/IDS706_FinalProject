import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_read_main():
    response = client.get("/")

    assert response.json() == {"Tips:" : "This app can help you categorize sentiments into negative, neutral, or positive categories."}

def test_process_text():
    text_data = "This is a positive statement."
    response = client.post("/process_text?text={}".format(text_data))
    assert "Raw Text" in response.json()
    assert "Categories" in response.json()
    
    
test_read_main()
test_process_text()