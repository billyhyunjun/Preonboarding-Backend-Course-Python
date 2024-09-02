# Pytest란?

pytest란 이름 그대로 py(thon)을 test 하는 프레임워크를 의미합니다.
Python 코드의 테스트를 작성하고 실행하는 데 사용됩니다.
* [pytest 공식 주소](https://docs.pytest.org/en/stable/)

## Pytest 이용하는 이유?

최근 많이 주목받고 있는 TDD (Test Driven Development) 즉, 본격적인 개발에 들어가기 전에 테스트 계획 및 코드를 작성하는 것을 의미
규모의 개발 상황에서 수 많은 모듈, 함수간 종속성과 매우 많은 코드 양의 오류 및 에러를 잡는데 많은 시간과 인력을 투입하게 될 것입니다.
이러한 문제를 해결하기 위해 TDD. 즉, 테스트 주도 개발이 나오게 된 것입니다. 그리고 Python에서 TDD를 하기 위해 나온 프레임워크가 pytest입니다.

## Pytest 설치 방법

`pytest`는 Python에서 널리 사용되는 테스트 프레임워크입니다. 다음 단계를 따라 설치할 수 있습니다:

### 1. Python과 pip 확인

`pytest`는 Python 패키지로 제공되므로, 먼저 Python이 설치되어 있어야 하며, Python의 패키지 관리 도구인 pip도 필요합니다. 터미널(또는 명령 프롬프트)에서 다음 명령어로 Python과 pip이 설치되어 있는지 확인합니다:

```bash
python --version
pip --version
```

pytest를 설치하려면 터미널에서 다음 명령어를 입력합니다:

```bash
pip install pytest
```

설치 버전 확인

```bash
pytest --version
```

## pytest의 핵심 문법 assert
assert는 뒤의 조건이 True가 아니면 AssertError를 발생한다.
왜 assert가 필요한 것일까?

어떤 함수는 성능을 높이기 위해 반드시 정수만을 입력받아 처리하도록 만들 수 있다. 
이런 함수를 만들기 위해서는 반드시 함수에 정수만 들어오는지 확인할 필요가 있다. 
이를 위해 if문을 사용할 수도 있고 '예외 처리'를 사용할 수도 있지만 '가정 설정문'을 사용하는 방법도 있다.

```python
def test(t):
    assert type(t) is int, '정수 아닌 값이 있네'

for i in lists:
    test(i)
#결과
AssertionError: 정수 아닌 값이 있네
```

## Test code

```python
# first_test.py

# 테스트를 해보고 싶은 함수
def func(x):
    return x + 1

# 테스트 함수
def test_answer():
    assert func(3) == 5
```

![image](https://github.com/user-attachments/assets/6042dda9-f201-41eb-8bec-d685d22830e7)

결과는 당연하게도 테스트 실패입니다. 3+1 == 5에서 오류를 발견하고 이에 에러가 있음을 알려줍니다.
뿐만 아니라, 현재 어떠한 platform에서 작동하고 있고, 
어떤 에러가 발생했는지 그리고 마지막에 요약을 통해 총 몇 개의 테스트가 통과(pass), 실패(fail)했는 지와 함께 
총 테스트 시간을 알려줍니다.

## Fixture 시스템
여기서 Fixture라는 기능을 이용하면 테스트에 필요한 초기 설정과 정리 작업을 쉽게 정의하고 재사용할 수 있습니다.

예시로 아래와 같은 계산 클래스가 정의 되었을 때에
```python
# calculator.py
class Calculator(object):
    """Calculator class"""
    def __init__(self):
        pass

    @staticmethod
    def add(a, b):
        return a + b

    @staticmethod
    def subtract(a, b):
        return a - b

    @staticmethod
    def multiply(a, b):
        return a * b

    @staticmethod
    def divide(a, b):
        return a / b
```

클래스 테스트코드를 작성한다면
```python
# test_calculator.py
from src.calculator import Calculator
def test_add():
    calculator = Calculator()
    assert calculator.add(1, 2) == 3
    assert calculator.add(2, 2) == 4

def test_subtract():
    calculator = Calculator()
    assert calculator.subtract(5, 1) == 4
    assert calculator.subtract(3, 2) == 1

def test_multiply():
    calculator = Calculator()
    assert calculator.multiply(2, 2) == 4
    assert calculator.multiply(5, 6) == 30

def test_divide():
    calculator = Calculator()
    assert calculator.divide(8, 2) == 4
    assert calculator.divide(9, 3) == 3
```
위와 같이 작성을 하지만 반복된 `calculator = Calculator()`를 fixture 기능을 이용하여

```python
import pytest
from src.calculator import Calculator

@pytest.fixture
def calculator():
    calculator = Calculator()
    return calculator

def test_add(calculator):
    assert calculator.add(1, 2) == 3
    assert calculator.add(2, 2) == 4

def test_subtract(calculator):
    assert calculator.subtract(5, 1) == 4
    assert calculator.subtract(3, 2) == 1

def test_multiply(calculator):
    assert calculator.multiply(2, 2) == 4
    assert calculator.multiply(5, 6) == 30
```
위와 같이 사용하여 재사용이 용의하게 사용할 수 있습니다.

## Django의 test.py
Django 프레임워크에도 앱 코드를 테스트할 수 있는 기능을 포함하고 있는데.
`python manage.py test`를 입력하여 django 각각의 앱들을 순회하면서 모든 test.py 를 가져와서 클래스들을 불러와 테스트를 할 수 있습니다.

* test.py

```python
from django.test import TestCase
from django.test import Client
from .models import Article
from django.contrib.auth import get_user_model

class ArticleTest(TestCase) :
    def setUp(self) :
        User = get_user_model()
        user = User.objects.create_user(username='test', password='123') # 새 계정만듬 - 회원가입
        Article.objects.create(title='hello', user=user) # 회원가입한 계정으로 게시글 생성
    
    def test_article_title(self) :
        article=Article.objects.get(pk=1)
        self.assertEqual(article.title, 'hello')
     
    def test_article_create(self) : # 게시물을 저장하기 위해 이 요청을 보냈을 때 재대로 저장이 되는지 평가
        c = Client() # 우리가 브라우저로 켜는 것 대신 얘가 요청을 보내고 처리를 대신 해줌
        # 0. 로그인 확인
        res = c.get('articles/create') # 'articles/create' 주소로 get 요청을 보내고, res에 그 응답내용을 저장
        self.assertEqual(res.status_code, 302) # res.status_code와 302가 같은지 비교, 같지 않다면 에러가 발생함.
        
        # 1. /articles/create/ 로 GET 요청
        c.login(username='test', passwrod='123') # 로그인
        res = c.get('articles/create/') # article/create 로 이동 후 res 저장
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'articles/article_form.html') # html 파일이 일치하는지 확인
        self.assertContains(res, '<h1>form</h1>') # html 문서 안에 원하는 데이터가 있는지
        
        # 2. /articles/create/ 로 POST 요청(invalid)
        res = c.post('articles/create/') # 게시글 내용없이 요청을 보내봄
        self.assertContains(res, 'This field is required') # 잘 튕겨져 나오는지 확인
        self.assertEqual(res.status_code, 200)
        
        # 3. /articles/create/ 로 POST 요청(valid)
        before = Article.objects.last() # 게시물 작성 전 맨 뒤에 게시글
        res = c.post('articles/create/', {'title':'hi'}) # 새 게시물 작성
        after = Article.objects.last() # 게시물 작성 후 맨 뒤에 게시글
        self.assertEqual(res.status_code, 302)
        self.assertEqual(res.url, 'articles/2/') # 페이지 잘 이동되었는지 확인
        self.asertNotEqual(before, after) # 새글이 잘 들어갔는지 확인/ before와 after는 서로 달라야함
        
    def test_article_list(self) :
    	c=Client()
        res = c.get('articles/')
        context_articles = res.context.get('articles')
        queryset_articles = Article.objects.all()
        
        self.assertEqual(list(context_articles), list(queryset_articles))
        self.assertTemplateUsed(res, 'articles/article_list.html')
```
위와 같이 코드를 작성하며 view.py에서 실행이 되는 각 코드의 입력 값을 넣고 해당하는 결과 값이 예상 값에 나오는지, 
잘못된 값을 넣었을 때에 오류가 나오는 지 테스트를 할 수 있습니다.

## Test의 일반적인 원칙
* 가장 단위에 집중

  * 테스트 유닛은 각 기능의 가장 작은 단위에 집중하여, 해당 기능이 정확히 동작하는지를 증명해야 합니다.

* 각 유닛 테스트는 독립적

  * 각 테스트 유닛은 반드시 독립적이어야 합니다. 각 테스트는 혼자서도 실행 가능해야하고, 테스트 슈트로도 실행 가능해야 합니다. 이 때, 호출되는 순서와 무관하게 잘 동작해야 합니다. 이 규칙이 뜻하는 바, 새로운 데이터셋으로 각각의 테스트를 로딩해야 하고, 그 실행 결과는 꼭 삭제해야합니다. 보통 setUp() 과 tearDown() 메소드로 이런 작업을 합니다.

* 테스트 시간을 최대한 단축해야한다.

  * 테스트 하나가 실행하는데 몇 밀리세컨드 이상의 시간이 걸린다면, 개발 속도가 느려지거나 테스트가 충분히 자주 수행되지 못할 것입니다.
  * 별도 테스트 슈트 분리
    * 테스트에 필요한 데이터 구조가 너무 복잡하고, 테스트를 하려면 매번 이 복잡한 데이터를 불러와야 해서 테스트를 빠르게 만들 수 없는 경우도 있습니다. 이럴 때는 무거운 테스트는 따로 분리하여 별도의 테스트 슈트를 만들어 두고 스케쥴 작업을 걸어두면 됩니다. 그리고 그 외의 다른 모든 테스트는 필요한 만큼 자주 수행하면 됩니다.

* 테스트 함수의 이름은 최대한 길고, 자세하고 서술적인 이름으로 작성할 것

  * 테스트 함수에는 길고 서술적인 이름을 사용 테스트에서의 스타일 안내서는 짧은 이름을 보다 선호하는 다른 일반적인 코드와는 조금 다릅니다. 테스트 함수는 절대 직접 호출되지 않기 때문입니다. 실제로 돌아가는 코드에서는 square() 라든가 심지어 sqr() 조차도 괜찮습니다. 하지만 테스트 코드에서는 test_square_of_number_2(), test_square_negative_number() 같은 이름을 붙여야 합니다. 이런 함수명들은 테스트가 실패할 때나 보입니다. 그러니 반드시 가능한 한 서술적인 이름을 붙여야 합니다.
