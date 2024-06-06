from fastapi import FastAPI, File, UploadFile
from app.routers import ocr
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = ["*"] # all IPs

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(ocr.router)

@app.get("/")
def root():
    return {"message": "Welcome to MedscanRx"}


