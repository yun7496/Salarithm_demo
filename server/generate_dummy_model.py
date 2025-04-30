import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import LabelEncoder
import joblib

# 더미 데이터 생성
data = {
    'university': ['서울대', '연세대', '고려대', '한양대', '성균관대', '서강대', '중앙대', '이화여대'] * 3,
    'major': ['컴퓨터공학', '경영학', '경제학', '전자공학', '심리학', '기계공학', '영문학', '수학'] * 3,
    'gpa': [3.8,3.5,3.6,3.4,3.2,3.7,3.1,3.9,3.3,3.5,3.7,3.6,3.8,3.2,3.1,3.9,3.5,3.7,3.6,3.8,3.9,3.1,3.2,3.5],
    'experience': [2,1,3,0,1,4,2,0,3,1,2,5,4,2,1,3,0,2,5,4,1,2,3,0],
    'certification': [1,0,1,0,0,1,0,0,1,0,1,1,0,1,0,1,0,1,0,1,0,0,1,1],
    'language_score': [900,850,870,800,750,910,780,920,860,800,890,870,910,750,760,930,840,880,860,900,910,770,780,820],
    'salary': [5500,4500,4800,4000,3700,6000,3900,6100,4700,4200,5800,5300,5900,3800,3700,6200,4400,5700,5200,5600,6000,3900,4100,4500]
}

# 데이터프레임 생성
df = pd.DataFrame(data)

# 범주형 인코딩
le_univ = LabelEncoder()
le_major = LabelEncoder()
df['university'] = le_univ.fit_transform(df['university'])
df['major'] = le_major.fit_transform(df['major'])

# 학습
X = df[['university', 'major', 'gpa', 'experience', 'certification', 'language_score']]
y = df['salary']

model = LinearRegression()
model.fit(X, y)

# 저장
joblib.dump(model, 'model.pkl')
joblib.dump(le_univ, 'le_univ.pkl')
joblib.dump(le_major, 'le_major.pkl')

print("[완료] 모델과 인코더 저장 완료!")