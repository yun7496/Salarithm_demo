from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  

from pydantic import BaseModel
import joblib
import numpy as np

# FastAPI 앱 생성
app = FastAPI()

# ✅ CORS 미들웨어 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 또는 ["http://127.0.0.1:5500"] 등 지정해도 됨
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 모델 로딩
model = joblib.load('model.pkl')
le_univ = joblib.load('le_univ.pkl')
le_major = joblib.load('le_major.pkl')

# 요청 데이터 스키마
class SalaryInput(BaseModel):
    university: str
    major: str
    gpa: float
    experience: int
    certification: int
    language_score: int

# 예측 API
@app.post("/predict")
def predict_salary(input: SalaryInput):
    university_encoded = le_univ.transform([input.university])[0]
    major_encoded = le_major.transform([input.major])[0]

    features = np.array([[university_encoded, major_encoded, input.gpa, input.experience, input.certification, input.language_score]])
    prediction = model.predict(features)[0]
    prediction_rounded = int(round(prediction))

    return {"predicted_salary": prediction_rounded}