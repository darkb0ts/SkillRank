from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from nlp_model.ml_model import *
from celery_work.worker import score_resume_task
import re
import os
import redis


app = FastAPI()


class Resume(BaseModel):
    text: str


@app.get("/")
async def read_root():
    return {"message": "Hello, World!"}


@app.post('/process')
async def process_resumes(job_tags: list, job_description: str, files: list[UploadFile] = File(...)):
    filtered_files = []

    task_done = []

    for resume in files:

        filename = resume.filename

        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

        resume.file.seek(0)

        with open(file_path, "wb") as buffer:

            buffer.write(resume.file.read())
        preprocessed_text = predictResume(
            os.path.join(app.config['UPLOAD_FOLDER'], resume))

        task_process, task = score_resume_task.delay(
            preprocessed_text, job_tags, job_description, files, file_path)

        if task_process:
            task_done.append(task)
    return JSONResponse(content={"res": res})
