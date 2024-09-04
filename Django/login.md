# 로그인
유저 데이터를 입력하고 로그인 버튼을 누르면 해당 토큰의 데이터를 표기해주기

![image](https://github.com/user-attachments/assets/c7c428bd-3210-4dea-a963-e2f408f7e29b)


## 코드
회원등록된 계정의 아이디와 비밀번호를 입력하면 access토큰 값이 출력

### view.py
djnago에 기본 내장된 TokenObtainPairSerializer를 이용하여 로그인 인증 및 토큰 발급
```python
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer

class TokenObtainPairView(APIView):
    def post(self, request):
        serializer = TokenObtainPairSerializer(data=request.data)
        if serializer.is_valid():
            token = serializer.validated_data.get('access')
            return Response({ "token": token}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
```


### html
프론트 엔드상에서 입력을 받아서 서버로 전달
```html
<body>
            <h2>Login</h2>
            <form id="login-form">
                <label for="login-username">Username:</label>
                <input type="text" id="login-username" required>
                <label for="login-password">Password:</label>
                <input type="password" id="login-password" required>
                <button type="submit">Login</button>
            </form>
</body>
<script>
        // Login
        document.getElementById('login-form').addEventListener('submit', async (e) => {
            e.preventDefault();
            const username = document.getElementById('login-username').value;
            const password = document.getElementById('login-password').value;

            try {
                const response = await fetch(`${apiBaseUrl}/api/token/`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ username, password })
                });

                const result = await response.json();
                if (response.ok) {
                    localStorage.setItem('access_token', result.access);
                    localStorage.setItem('refresh_token', result.refresh);
                    // Display token as JSON
                    document.getElementById('user-details').textContent = JSON.stringify(result);
                    document.getElementById('auth-section').style.display = 'none';
                    document.getElementById('user-info').style.display = 'block';
                } else {
                    alert('Login failed: ' + result.detail);
                }
            } catch (error) {
                console.error('Error:', error);
            }
        });
</script>
```
![image](https://github.com/user-attachments/assets/ebf73220-2ed0-4d0a-bd4c-224f0526b0c5)

## 결과

프론트엔드로 전달 받은 값을 리스폰

![image](https://github.com/user-attachments/assets/2d61ec01-7fa8-4d77-81b4-3cf5ebdfcb0a)

postman을 이용한 JSON데이터 결과값 출력

![image](https://github.com/user-attachments/assets/05361cf2-4f1f-423b-b564-384ad504a4e8)


