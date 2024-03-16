import nltk  # Assuming NLTK for preprocessing
import spacy
from sklearn.feature_extraction.text import CountVectorizer
import textract
from itertools import chain
from sklearn.metrics.pairwise import cosine_similarity
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import re
import pickle
import en_core_web_sm
import pandas
import numpy as np

nlp = spacy.load("en_core_web_sm")


def cleanResume(resumeText):
    resumeText = re.sub('http\S+\s*', ' ', resumeText)
    resumeText = re.sub('RT|cc', ' ', resumeText)
    resumeText = re.sub('#\S+', '', resumeText)
    resumeText = re.sub('@\S+', '  ', resumeText)
    resumeText = re.sub('[%s]' % re.escape(
        """!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"""), ' ', resumeText)
    resumeText = re.sub(r'[^\x00-\x7f]', r' ', resumeText)
    resumeText = re.sub('\s+', ' ', resumeText)
    return resumeText


def find_score(jobdes, filename, customKeywords):
    print(jobdes, filename, customKeywords)
    resume = Preprocessfile(filename)
    customKeywords = ' '.join(customKeywords)
    jobdes = jobdes + ' ' + customKeywords
    text = [resume, jobdes]
    cv = CountVectorizer()
    count_matrix = cv.fit_transform(text)
    matchpercent = cosine_similarity(count_matrix)[0][1]*100
    matchpercent = round(matchpercent, 2)
    return matchpercent


def extract_skills(text):
    doc = nlp(text)
    skills = [ent.text for ent in doc.ents if ent.label_ == "SKILL"]
    return skills


def Preprocessfile(filename):
    text = filename
    if ".pdf" in filename:
        try:
            text = textract.process(filename)
        except UnicodeDecodeError:
            print('File', filename, 'cannot be extracted! - skipped')
        text = text.decode('utf-8').replace("\\n", " ")
    else:
        text = text.replace("\\n", " ")
    x = []
    tokens = word_tokenize(text)
    tok = [w.lower() for w in tokens]
    table = str.maketrans('', '', string.punctuation)
    strpp = [w.translate(table) for w in tok]
    words = [word for word in strpp if word.isalpha()]
    stop_words = set(stopwords.words('english'))
    words = [w for w in words if not w in stop_words]
    x.append(words)
    res = " ".join(chain.from_iterable(x))
    return res


def predictResume(filename):
    global not_check
    try:
        text = textract.process(filename)
        text = text.decode('utf-8').replace("\\n", " ")
        text = cleanResume(text)
        text = [text]
        text = np.array(text)
        vectorizer = pickle.load(open("vectorizer.pickle", "rb"))
        resume = vectorizer.transform(text)
        model = load('model.joblib')
        result = model.predict(resume)
        labeldict = {
            0: 'Arts',
            1: 'Automation Testing',
            2: 'Operations Manager',
            3: 'DotNet Developer',
            4: 'Civil Engineer',
            5: 'Data Science',
            6: 'Database',
            7: 'DevOps Engineer',
            8: 'Business Analyst',
            9: 'Health and fitness',
            10: 'HR',
            11: 'Electrical Engineering',
            12: 'Java Developer',
            13: 'Mechanical Engineer',
            14: 'Network Security Engineer',
            15: 'Blockchain ',
            16: 'Python Developer',
            17: 'Sales',
            18: 'Testing',
            19: 'Web Designing'
        }
        return [1, labeldict[result[0]]]
    except UnicodeDecodeError:
        print('File', filename, 'cannot be extracted for prediction! - skipped')
        return [0, 1]
