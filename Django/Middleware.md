# Middleware란?

Middleware는 컴퓨터 시스템에서 다양한 소프트웨어 응용 프로그램을 연결하고 상호작용을 가능하게 하는 소프트웨어 계층을 의미합니다.

Middleware의 주요 기능
1. 통신 관리: 서로 다른 애플리케이션 간의 통신을 관리하고, 네트워크 연결을 설정하며, 데이터 전송을 중재합니다.
2. 데이터 포맷 변환: 서로 다른 시스템 간의 데이터 형식을 변환하여 상호 호환성을 보장합니다.
3. 보안: 데이터 암호화, 인증 및 권한 부여를 통해 시스템 간의 안전한 통신을 지원합니다.
4. 로드 밸런싱: 시스템에 들어오는 트래픽을 균형 있게 분배하여 성능을 최적화합니다.
5. 에러 처리: 시스템 간 통신 시 발생할 수 있는 오류를 감지하고 처리합니다.

예시
1. 웹 서버와 애플리케이션 서버 간의 통신을 관리하는 웹 미들웨어 (예: Apache Tomcat, Nginx)
2. 데이터베이스 미들웨어: 데이터베이스와 애플리케이션 간의 연결을 관리하고 쿼리 처리를 돕습니다.

## Django의 미들웨어

Django의 미들웨어는 요청(request)과 응답(response) 객체를 처리하는 동안 특정한 작업을 수행할 수 있게 해주는
Django 프레임워크의 구성 요소입니다. Django 미들웨어는 요청과 응답의 처리 과정을 가로채어 필요한 조작을 하거나 
특정 기능을 추가하는 방식으로 동작합니다. 이 미들웨어는 요청이 Django의 뷰(view)에 도달하기 전에, 
그리고 응답이 클라이언트로 보내지기 전에 여러 가지 작업을 수행할 수 있는 기회를 제공합니다.

```python
# setting.py 기본 등록 미들웨어
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
```

미들웨어 등록 순서가가지는 의미는 다음과 같다

* http request가 들어오면 위에서부터 아래로 미들웨어를 적용시킨다
* http response가 나갈 때 아래서부터 위로 미들웨어를 적용시킨다

### Django 미들웨어의 사용 사례
Django 미들웨어는 다양한 기능을 추가하거나 시스템 전반에 영향을 미치는 작업을 수행할 수 있습니다. 일반적인 사용 사례는 다음과 같습니다:

* 인증 및 권한 부여: 사용자 인증 상태를 확인하고, 특정 뷰에 대한 접근 권한을 제어합니다.
* 세션 관리: 사용자의 세션을 설정하고 유지 관리합니다.
* 요청 및 응답 로깅: 요청과 응답의 정보를 기록하여 로깅 및 모니터링 목적으로 사용합니다.
* 보안: XSS, CSRF와 같은 보안 취약점을 방어하는 작업을 수행합니다.
* 캐싱: 응답을 캐시하여 성능을 향상시킵니다.
* 국제화 및 현지화: 사용자 요청에 따라 언어 및 지역 설정을 관리합니다.

### 커스텀 미들웨어
Django에서 커스텀 미들웨어는 함수나 클래스로 작성할 수 있다

```python
# custom middleware - class
class MyMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # 최초 설정 및 초기화

    def __call__(self, request):
        # 뷰가 호출되기 전에 실행될 코드들

        response = self.get_response(request)

        # 뷰가 호출된 뒤에 실행될 코드들

        return response
```

초기 생성자(`__init__`함수)와 호출 함수(`__call__` 함수) 두분으로 나뉜다
`__init__` 함수에서는 최초 설정 및 초기화를 한다
`__call__` 함수는 request를 받아서 response 를 리턴한다
get_response 는 장고에서 미들웨어를 호출할 때 넘겨주는 하나의 함수이며, view이거나 다른 미들웨어 일 수 있다

### http 요청 미들웨어

```python
def process_request(request)
  
# 장고가 view 를 호출하기 바로 직전에 불리는 훅이다
# None 이나 HttpResponse 객체를 리턴해야 한다.
# None 을 리턴하면, view 를 호출하고, HttpResponse 객체를 리턴하면,
# 해당 HttpResponse 를 미들웨어로 다시 쏘아 올린다.
def process_view(request, view_func, view_args, view_kwargs)
```

### http 응답 미들웨어

```python
# view 가 exception 을 발생시키면 호출된다.
def process_exception(request, exception)
  
# response 가 템플릿을 반환하는 경우에만
def process_template_response(request, response)
  
def process_response(request, response)
```

# 데코레이터(Decorators)
데코레이터(Decorators)는 파이썬에서 함수나 메서드의 동작을 수정하거나 확장할 때 사용하는 디자인 패턴입니다. 
데코레이터는 다른 함수를 인수로 받아들이고, 일부 처리를 한 뒤, 수정된 함수나 원래 함수를 반환하는 함수입니다.
이를 통해 코드의 중복을 줄이고, 가독성을 높이며, 기능을 쉽게 확장할 수 있습니다.

## 데코레이터의 기본 구조

### 데코레이터 선언

```python
def decorator_function(original_function):
    def wrapper_function(*args, **kwargs):
        # 원래 함수가 호출되기 전의 동작
        print("Wrapper executed this before {}".format(original_function.__name__))
        
        # 원래 함수 호출
        result = original_function(*args, **kwargs)
        
        # 원래 함수가 호출된 후의 동작
        print("Wrapper executed this after {}".format(original_function.__name__))
        
        return result
    return wrapper_function
```

### 데코레이터 사용법
```python
def log_decorator(func):
    def wrapper(*args, **kwargs):
        print(f"Function {func.__name__} started")
        result = func(*args, **kwargs)
        print(f"Function {func.__name__} ended")
        return result
    return wrapper

@log_decorator
def say_hello(name):
    print(f"Hello, {name}!")

say_hello("Alice")
```

### 결과 값
```python
Function say_hello started
Hello, Alice!
Function say_hello ended
```

### 데코레이터를 이용한 인증방법
인증 처리: 사용자가 인증되었는지 확인하는 데코레이터를 만들 수 있습니다.
```python
def require_authentication(func):
    def wrapper(user):
        if not user.get('authenticated'):
            print("User is not authenticated")
            return
        return func(user)
    return wrapper

@require_authentication
def access_dashboard(user):
    print(f"Accessing dashboard for {user['name']}")

user = {'name': 'Alice', 'authenticated': False}
access_dashboard(user)  # "User is not authenticated" 출력
```

### 데코레이터의 장점
* 코드 재사용성: 여러 함수에 동일한 기능을 적용할 때, 코드 중복을 줄이고 재사용성을 높일 수 있습니다.
* 가독성 향상: 함수가 수행하는 주요 작업과 부가 작업(예: 로깅, 인증)을 분리하여 코드 가독성을 높일 수 있습니다.
* 유지 보수 용이: 데코레이터를 사용하면 부가 기능을 별도의 함수로 관리할 수 있어, 유지 보수가 용이합니다.
