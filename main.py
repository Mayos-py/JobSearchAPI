from fastapi import FastAPI, UploadFile, File, Query
import uvicorn
import PyPDF2
import io
import requests
import os
from dotenv import load_dotenv


rapidAPIKey = os.getenv("RAPIDAPI_KEY")
rapidAPIHost = os.getenv("RAPIDAPI_HOST")

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Job Application Automation API"}

@app.post("/upload-resume/")
async def upload_resume(file: UploadFile = File(...)):
    content = await file.read()
    pdf_reader = PyPDF2.PdfReader(io.BytesIO(content))
    text = "\n".join([page.extract_text() for page in pdf_reader.pages if page.extract_text()])
    return {"filename": file.filename, "extracted_text": text}

@app.get("/search-jobs/")
def search_jobs(query: str = Query(..., title="Job Title"), location: str = Query("", title="Job Location")):
    url = "https://jsearch.p.rapidapi.com/search"
    headers = {
        "X-RapidAPI-Key": rapidAPIKey, 
        "X-RapidAPI-Host": rapidAPIHost
    }
    params = {"query": f"{query} in {location}", "num_pages": 1}
    
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code == 200:
        return response.json()
    
    return {"error": f"Failed to fetch jobs, Status Code: {response.status_code}", "details": response.text}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
