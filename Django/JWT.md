# JWT
![image](https://github.com/user-attachments/assets/73b10282-a3b8-45b0-9835-f23175a6371d)


JWT(Json Web Token)은 Json 객체에 인증에 필요한 정보들을 담은 후 비밀키로 서명한 토큰으로, 인터넷 표준 인증 방식이다. 
공식적으로 인증(Authentication) & 권한허가(Authorization) 방식으로 사용된다.

## JWT 프로세스

![image](https://github.com/user-attachments/assets/584e341b-0d89-4fb3-8f6f-09602191ad71)

* JWT 발급

1. 사용자가 아이디와 비밀번호 혹은 소셜 로그인을 이용하여 서버에 로그인 요청을 보낸다.
2. 서버는 비밀키를 사용해 json 객체를 암호화한 JWT 토큰을 발급한다.
3. JWT를 헤더에 담아 클라이언트에 보낸다.

* JWT 이용
1. 클라이언트는 JWT를 로컬에 저장해놓는다.
2. API 호출을 할 때마다 header에 JWT를 실어 보낸다.
3. 서버는 헤더를 매번 확인하여 사용자가 신뢰할만한지 체크하고, 인증이 되면 API에 대한 응답을 보낸다.

## HTTP의 특성

Connectionless : 한 번 통신이 이뤄지고 난 후에 연결이 바로 끊어진다
Stateless : 이전 상태를 유지/기억하지 않는다

쉽게 설명하면 한 번 통신이 일어나고 나면 연결이 끊어진다는 것이고, 
다시 연결해도 이전 상태를 유지하지 않아 과거에 어떤 정보를 보냈었는지 기억하지 못한다는 것이다.
따라서 인증된 사용자가 어느 정도 기간동안 재인증 하지 않아도 되도록(로그인이 유지되도록) 만든 것이 Access Token이다.

## JWT의 구조

JWT는 **Header**, **Payload**, **Signature** 3개로 구성되어 있다.

📌 Header

* alg : Signature에서 사용하는 알고리즘
* typ : 토큰 타입
Signature에서 사용하는 알고리즘은 대표적으로 RS256(공개키/개인키)와 HS256(비밀키(대칭키))가 있다.
이 부분은 auth0 공식 문서에서 자세히 설명해주고 있다.


📌 Payload

사용자 정보의 한 조각인 클레임(claim)이 들어있다.

* sub : 토큰 제목(subject)
* aud : 토큰 대상자(audience)
* iat : 토큰이 발급된 시각 (issued at)
* exp : 토큰의 만료 시각 (expired)

📌 Signature

Signature는 헤더와 페이로드의 문자열을 합친 후에, 헤더에서 선언한 알고리즘과 key를 이용해 암호한 값이다.

Header와 Payload는 단순히 Base64url로 인코딩되어 있어 누구나 쉽게 복호화할 수 있지만, Signature는 key가 없으면 복호화할 수 없다. 
이를 통해 보안상 안전하다는 특성을 가질 수 있게 되었다.

앞서 언급한 것처럼 header에서 선언한 알고리즘에 따라 key는 개인키가 될 수도 있고 비밀키가 될 수도 있다. 
개인키로 서명했다면 공개키로 유효성 검사를 할 수 있고, 비밀키로 서명했다면 비밀키를 가지고 있는 사람만이 암호화 복호화, 
유효성 검사를 할 수 있다.


### 장단점

📌 장점

* 로컬에 저장하기 때문에 서버 용량에 영향을 끼치거나 받지 않는다.
* 보다 안전하다. (공개키/개인키 or 비밀키를 통해 서명되기 때문에)
* 모바일 앱에서 사용하기 적합하다.모바일 앱은 여러 플랫폼 및 기기에서 동작할 수 있고, 서로 다른 도메인에서 통신할 수도 있다. 
이때 JWT를 사용하면 플랫폼 독립적으로 사용자 인증을 처리할 수 있기 때문에 적합하다. 
* 네트워크 부하가 적다. http헤더나 url 파라미터를 통해 간단하게 전송되기 때문이다.

📌 단점

* 토큰의 크기가 커질수록 트래픽에 영향을 미칠 수 있다.
* 토큰은 발급되면 만료 기간 변경이 불가능하므로 토큰 만료 처리를 구현해야 한다.

![image](https://github.com/user-attachments/assets/74e29e65-231b-4ad8-ac1a-64efad4bed4d)


## JWT의 Access Token / Refresh Token

JWT도 제 3자에게 토큰 탈취의 위험성이 있기 때문에, 그대로 사용하는것이 아닌 Access Token, Refresh Token 으로 이중으로 나누어 인증을 하는 방식을 현업에선 취한다.
Access Token 과 Refresh Token은 둘다 똑같은 JWT이다. 다만 토큰이 어디에 저장되고 관리되느냐에 따른 사용 차이일 뿐이다.

Access Token : 클라이언트가 갖고있는 실제로 유저의 정보가 담긴 토큰으로, 클라이언트에서 요청이 오면 서버에서 해당 토큰에 있는 정보를 활용하여 사용자 정보에 맞게 응답을 진행
Refresh Token: 새로운 Access Token을 발급해주기 위해 사용하는 토큰으로 짧은 수명을 가지는 Access Token에게 새로운 토큰을 발급해주기 위해 사용. 해당 토큰은 보통 데이터베이스에 유저 정보와 같이 기록.

정리하자면, Access Token은 접근에 관여하는 토큰, Refresh Token은 재발급에 관여하는 토큰의 역할로 사용되는 JWT 이라고 말할 수 있다.

출처: https://inpa.tistory.com/entry/WEB-📚-JWTjson-web-token-란-💯-정리 [Inpa Dev 👨‍💻:티스토리]
