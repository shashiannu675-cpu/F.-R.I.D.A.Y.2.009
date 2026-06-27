from fastapi import FastAPI, UploadFile, File, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from config import settings
from services.friday_engine import engine
import os
import shutil

app = FastAPI(title=settings.APP_NAME, version=settings.VERSION)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"message": "System fault prevented crash.", "details": str(exc)},
    )

@app.get("/")
async def health_check():
    return {"status": "Friday Core Online"}

@app.post("/api/v1/{user_id}/chat")
async def chat_with_friday(user_id: str, prompt: str):
    response = await engine.process_request(user_id, prompt)
    return response

@app.post("/api/v1/{user_id}/upload")
async def upload_file(user_id: str, file: UploadFile = File(...)):
    try:
        safe_filename = f"{user_id}_{file.filename}"
        file_path = os.path.join(settings.UPLOAD_DIR, safe_filename)
        
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        return {"status": "success", "filename": safe_filename}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Upload failed.")

