# Backend Intern Assignment

## 과제명 / 목적
인턴 과제용 백엔드 서버 개발 및 JWT 기반 인증 시스템 구현

## 기술 스택
- Python 3.x
- Django 4.2
- Django REST framework
- djangorestframework-simplejwt
- drf-yasg (Swagger UI)

## 프로젝트 구조
```
backend/
├── accounts/                    # 사용자 인증 관련 앱
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── authentication.py       # JWT 인증 커스텀 클래스
│   ├── models.py
│   ├── serializers.py
│   ├── urls.py
│   └── views.py
├── backend/                    # 프로젝트 설정
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── manage.py
├── requirements.txt           # 프로젝트 의존성 패키지
└── README.md
```

## 주요 기능

### 1. 사용자 인증
- JWT 기반 인증 시스템
- 회원가입 API
- 로그인 API (JWT 토큰 발급)
- 토큰 기반 인증이 필요한 API 엔드포인트

### 2. API 문서화
- Swagger UI를 통한 API 문서 제공
- API 엔드포인트 상세 설명
- 요청/응답 예시 포함

### 3. 에러 처리
- 표준화된 에러 응답 형식
- 상세한 에러 메시지 및 코드
- 토큰 관련 에러 처리

## JWT 인증 가이드

### 인증 에러 응답

#### 1. 토큰이 없는 경우
```json
{
  "error": {
    "code": "TOKEN_NOT_FOUND",
    "message": "토큰이 없습니다."
  }
}
```

#### 2. 토큰이 만료된 경우
```json
{
  "error": {
    "code": "TOKEN_EXPIRED",
    "message": "토큰이 만료되었습니다."
  }
}
```

#### 3. 토큰이 유효하지 않은 경우
```json
{
  "error": {
    "code": "INVALID_TOKEN",
    "message": "토큰이 유효하지 않습니다."
  }
}
```

### 토큰 사용 방법

1. 로그인 API를 통해 토큰을 발급받습니다:
```json
POST /login
{
    "username": "사용자아이디",
    "password": "비밀번호"
}
```

2. 응답으로 받은 토큰을 Authorization 헤더에 포함시켜 요청합니다:
```
Authorization: Bearer {토큰}
```

### 주의사항
- 토큰은 15분 동안만 유효합니다.
- 토큰이 만료되면 다시 로그인하여 새로운 토큰을 발급받아야 합니다.
- 모든 보호된 API 엔드포인트에 접근할 때는 유효한 토큰이 필요합니다.

## 로컬 실행 방법

1. 가상환경 생성 및 활성화
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

2. 의존성 패키지 설치
```bash
pip install -r requirements.txt
```

3. 데이터베이스 마이그레이션
```bash
python manage.py migrate
```

4. 개발 서버 실행
```bash
python manage.py runserver
```

5. API 문서 확인
- Swagger UI: http://localhost:8000/swagger/
- ReDoc: http://localhost:8000/redoc/

## API 엔드포인트

### 1. 회원가입
- URL: `/signup`
- Method: POST
- Request Body:
```json
{
    "username": "사용자아이디",
    "password": "비밀번호",
    "nickname": "닉네임"
}
```

### 2. 로그인
- URL: `/login`
- Method: POST
- Request Body:
```json
{
    "username": "사용자아이디",
    "password": "비밀번호"
}
```

### 3. 메인 페이지
- URL: `/main`
- Method: GET
- 인증 필요: Yes
- Authorization 헤더 필요
