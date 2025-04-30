const BASE_URL = 'http://127.0.0.1:8000'; // 서버 주소

document.getElementById('salaryForm').addEventListener('submit', async function(e) {
  e.preventDefault();

  // 입력값 수집
  const data = {
    university: document.getElementById('university').value.trim(),
    major: document.getElementById('major').value.trim(),
    gpa: parseFloat(document.getElementById('gpa').value),
    experience: parseInt(document.getElementById('experience').value),
    certification: document.getElementById('certification').value ? 1 : 0,
    language_score: parseInt(document.getElementById('languageScore').value || '0')
  };

  try {
    // 서버에 POST 요청
    const response = await fetch(`${BASE_URL}/predict`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(data)
    });

    const result = await response.json();
    const predictedSalary = result.predicted_salary;

    // 예측 결과 표시
    document.getElementById('result').textContent = `예측 연봉: 약 ${predictedSalary.toLocaleString()}만원`;

    // 차트 생성
    const ctx = document.getElementById('salaryChart');
    new Chart(ctx, {
      type: 'bar',
      data: {
        labels: ['나의 예측 연봉', '비슷한 스펙 평균', '상위 10%'],
        datasets: [{
          label: '연봉 비교 (만원)',
          data: [predictedSalary, 4200, 5000],
          backgroundColor: ['#0077cc', '#99c2ff', '#ffcc00']
        }]
      },
      options: {
        responsive: true,
        plugins: { legend: { display: false } },
        scales: { y: { beginAtZero: true } }
      }
    });

    // 추천사항
    let recommendations = [];
    if (data.language_score < 800) {
      recommendations.push("어학 점수를 850 이상으로 향상하세요.");
    }
    if (data.experience < 2) {
      recommendations.push("추가 인턴 경험을 쌓아보세요.");
    }
    if (!document.getElementById('certification').value) {
      recommendations.push("SQLD 등 자격증을 취득해보세요.");
    }

    const recHtml = "<strong>커리어 추천:</strong><br>👉 " + recommendations.join('<br>👉 ');
    const recDiv = document.getElementById('recommendation');
    recDiv.innerHTML = recHtml;
    recDiv.style.display = 'block';

  } catch (error) {
    console.error('예측 요청 실패:', error);
    alert('서버 연결 오류 또는 예측 실패!');
  }
});