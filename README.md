## Requirements

- [ ]  [Pytest를 이용한 테스트 코드 작성법 이해](./Django/Pytest.md)
- [ ]  [Django를 이용한 인증과 권한 이해](./Django/인증과권한.md)
- [ ]  [JWT와 구체적인 알고리즘의 이해](./Django/JWT.md)
- [ ]  [PR 날려보기](./Django/PR.md)
- [ ]  리뷰 바탕으로 개선하기
- [ ]  EC2에 배포해보기

### 시나리오 설계!

**Django기본 이해**

- [ ]  [Middleware란 무엇인가? (with Decorators)](./Django/Middleware.md)
- [ ]  [Django란?](./Django/django.md)

**JWT 기본 이해**

- [ ]  [JWT란 무엇인가요?](./Django/JWTcode.md)

### 시나리오 설계 및 코딩 시작!

**토큰 발행과 유효성 확인**

- [ ]  [Access / Refresh Token 발행과 검증에 관한 테스트 시나리오 작성하기](./Django/token.md)

**유닛 테스트 작성**

- [ ]  [Pytest를 이용한 JWT Unit 테스트 코드 작성해보기](./Django/testToken.md)

### 백엔드 배포하기

**테스트 완성**

- [ ]  [백엔드 유닛 테스트 완성하기](./Django/viewtest.md)

**로직 작성**

- [ ]  백엔드 로직을 django로
    - [ ]  [회원가입 - /signup](./Django/signup.md)
        - [ ]  Request Message
            
            ```json
            json코드 복사
            {
            	"username": "JIN HO",
            	"password": "12341234",
            	"nickname": "Mentos"
            }
            
            ```
            
        - [ ]  Response Message
            
            ```json
            json코드 복사
            {
            	"username": "JIN HO",
            	"nickname": "Mentos",
            	"roles": [
            			{
            					"role": "USER"
            			}
            	]
            }
            
            ```
            
    - [ ]  [로그인 - /login](./Django/login.md)
        - [ ]  Request Message
            
            ```json
            json코드 복사
            {
            	"username": "JIN HO",
            	"password": "12341234"
            }
            
            ```
            
        - [ ]  Response Message
            
            ```json
            json코드 복사
            {
            	"token": "eKDIkdfjoakIdkfjpekdkcjdkoIOdjOKJDFOlLDKFJKL"
            }
            
            ```
            

### 백엔드 배포하고 개선하기

**배포해보기**

- [ ]  AWS EC2에 배포하기

**API 접근과 검증**

- [ ]  Swagger UI로 접속 가능하게 하기

[Git 커밋 메시지 잘 쓰는 법 | GeekNews](https://news.hada.io/topic?id=9178&utm_source=slack&utm_medium=bot&utm_campaign=TQ595477U)

**AI-assisted programming**

- [ ]  AI에게 코드리뷰 받아보기

**Refactoring**

- [ ]  피드백 받아서 코드 개선하기

**마무리**

- [ ]  AWS EC2 재배포하기
