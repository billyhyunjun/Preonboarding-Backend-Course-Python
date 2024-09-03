# JWT란 무엇인가요?
JWT (JSON Web Token)는 웹 애플리케이션에서 사용자 인증과 권한 부여를 위한 표준화된 토큰 형식입니다. 
JWT는 클라이언트와 서버 간에 정보를 안전하게 전달하는 데 사용됩니다. 이 토큰은 JSON 형식의 데이터 구조를 기반으로 되어 있으며 
헤더 (Header), 페이로드 (Payload), 서명 (Signature)의 정보으로 되어있으며 이들은 점(.)으로 구분됩니다.

## 헤더 (Header)
헤더는 Base64Url 인코딩을 통해 인코딩됩니다.
```python
{
  "alg": "HS256",  # 서명에 사용되는 알고리즘 (예: HS256, RS256)
  "typ": "JWT"  # 토큰의 유형 (일반적으로 "JWT")
}
```

## 페이로드 (Payload)
페이로드는 JWT에 담길 실제 데이터입니다. 이 데이터는 클레임(claims)이라고 불리며, 사용자 정보나 인증 관련 데이터를 포함할 수 있습니다.
* 등록된 클레임 (Registered Claims): 사전 정의된 클레임 (예: sub(subject), exp(expiration time), iss(issuer), aud(audience))
* 공식 클레임 (Public Claims): 사용자 정의 클레임으로, 이름이 충돌하지 않도록 등록이 필요합니다.
* 비공식 클레임 (Private Claims): 클레임의 이름과 값이 애플리케이션에 특화되어 있습니다.
```python
{
  "sub": "1234567890",
  "name": "John Doe",
  "iat": 1516239022
}
```

## 서명 (Signature)
서명은 헤더와 페이로드를 기반으로 생성되며, 토큰의 무결성을 보장합니다. 
서명은 헤더에 정의된 알고리즘을 사용하여 생성되며,
HMAC SHA256 또는 RSA SHA256과 같은 알고리즘을 사용할 수 있습니다.

서명 생성 단계
1. 헤더와 페이로드를 Base64Url로 인코딩합니다.
2. 인코딩된 헤더와 페이로드를 점(.)으로 구분하여 결합합니다.
3. 이 결합된 문자열에 비밀 키를 사용하여 서명합니다.

## 장점과 단점

* 장점
  * 자체 포함 (Self-contained): JWT는 사용자와 관련된 정보를 토큰 자체에 포함하므로, 서버가 상태를 유지할 필요가 없습니다.
  * 상태 비저장 (Stateless): 서버가 클라이언트의 상태를 저장하지 않아도 되므로, 서버 확장성과 성능이 향상됩니다.
  * 보안: 서명과 암호화를 통해 JWT의 무결성과 기밀성을 보장할 수 있습니다.
 

* 단점
  * 토큰 크기: JWT는 클레임과 서명을 포함하므로, 일반적인 세션 ID보다 크기가 커질 수 있습니다. 따라서, 특히 네트워크 대역폭이 제한된 환경에서는 부하가 될 수 있습니다.
  * 토큰의 만료: JWT는 만료 시간이 설정된 경우 만료되지만, 만료된 후에도 클라이언트에 저장된 토큰이 계속 사용될 수 있습니다. 이를 방지하기 위해 추가적인 조치를 취해야 할 수 있습니다.
 
## 코드
pyjwt 라이브러리를 사용하여 JWT를 생성하고 검증하는 방법
```python
import jwt
import datetime

# 비밀 키
SECRET_KEY = 'your_secret_key'  # SECRET_KEY는 JWT의 서명을 생성하는 데 사용되는 비밀 키

# JWT 생성
def create_jwt():
    payload = {
        'sub': '1234567890',
        'name': 'John Doe',
        'iat': datetime.datetime.utcnow()
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return token

# JWT 검증
def verify_jwt(token):
    try:
        decoded_payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return decoded_payload
    except jwt.ExpiredSignatureError:
        return 'Token has expired'
    except jwt.InvalidTokenError:
        return 'Invalid token'

# JWT 생성
token = create_jwt()
print(f"Generated JWT: {token}")

# JWT 검증
payload = verify_jwt(token)
print(f"Decoded payload: {payload}")
```
