# jd-checker-jev

채용 공고를 붙여넣으면 내 조건과 맞는지 항목별로 체크하고 지원 여부를 판정하는 웹 도구.

판단은 [Jev](https://typesafe.ai) (TypeSafe AI의 판단 전용 모델)이 담당한다. 글을 생성하지 않고, 주어진 기준에 대해 확률·분류·점수 같은 값만 돌려주는 모델이다.

## 동작

```
공고(붙여넣기) + 내 프로필  →  Jev  →  항목별 적합도 + 지원 판정
```

- **항목별 체크 (Noul)**: 기술스택 / 경력 / 근무지 / 연봉이 각각 맞는지 확률로 평가
- **종합 판정 (Choice)**: apply(지원 권장) / maybe(검토) / skip(비권장) 중 하나 + 신뢰도

## 실행

```bash
python -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/streamlit run app.py
```

## 설정

`.env` 파일에 TypeSafe API 키를 넣는다 (`.env.example` 참고).

```
TYPESAFE_API_KEY=your_key_here
```

내 프로필(기술스택·경력·근무지·연봉)은 실행 후 화면 왼쪽 사이드바에서 입력·수정한다.
