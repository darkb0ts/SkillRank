from celery import Celery
from redis import StrictRedis
from pyresparser import ResumeParser
import os
import json
from ..nlp_model import preprocess_resume, predictResume, find_score, Preprocessfile

redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)
celery_app = Celery("resume_scoring")
celery_app.conf.broker_url = "redis://localhost:6379"
celery_app.conf.result_backend = "redis://localhost:6379"

res = []


def job_process(job_tags, job_description, filtered_files, file_path):
    jobdes = Preprocessfile(job_description)
    customKeywords = []
    for tag in job_tags:
        temp = tag.strip()
        customKeywords.append(temp)
    res = list()
    for file in filtered_files:
        score = find_score(jobdes, file_path, customKeywords)
        user_info = ResumeParser(file_path).get_extracted_data()
        user_info['predicted'] = predictResume(file_path)
        res.append({
            'resumeId': file,
            'score': score,
            'userInfo': user_info
        })


def save_to_redis(resume_id, data):
    redis_client.set(resume_id, json.dumps(data))


@celery_app.task
def score_resume_task(preprocessed_text, job_tags, job_description, filtered_files, file_path):
    # Call predictResume with preprocessed_text
    predictResume(preprocessed_text)

    # Call job_process to further process the resumes
    for file_sys in filtered_files:
        checking_score = job_process(
            job_tags, job_description, file_sys, file_path)
        save_to_redis(file_sys, checking_score)
    return checking_score
    # store_result_in_redis(score)  # Function to store score in Redis
