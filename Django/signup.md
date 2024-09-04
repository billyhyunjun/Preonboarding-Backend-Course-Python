# 회원가입
유저 데이터를 입력하고 회원가입 버튼을 누르면 해당 데이터를 표기해주기

![image](https://github.com/user-attachments/assets/25c3d3f1-50e1-4d58-b88e-4401517f4fcd)


## 코드
회원가입 양식에 맞추어 입력을 받고 기본 django User 모델에 nickname을 추가 시켜 등록 후 결과를 리스폰

### view.py
```python
class RegisterView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        nickname = request.data.get('nickname')  # nickname을 가져옵니다.
        
        if username and password:
            if User.objects.filter(username=username).exists():
                return Response({'detail': 'User already exists'}, status=status.HTTP_400_BAD_REQUEST)
            
            user = User(username=username, password=make_password(password))
            user.save()

            # nickname과 함께 사용자 프로필 저장
            UserProfile.objects.create(user=user, nickname=nickname)
            
            serializer = UserInfoSerializer(user)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({'detail': 'Invalid input'}, status=status.HTTP_400_BAD_REQUEST)
```

### model
닉네임 컬럼 생성
```python
from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=255, blank=True, null=True)
```

### serializer
모델 시리얼 라이징
```python
from rest_framework import serializers
from django.contrib.auth.models import User

# 사용자 정보를 위한 커스텀 직렬화기 정의
class UserInfoSerializer(serializers.ModelSerializer):
    roles = serializers.SerializerMethodField()
    nickname = serializers.CharField(source='userprofile.nickname') 
    
    class Meta:
        model = User
        fields = ['username', 'nickname', 'roles']
    
    def get_roles(self, obj):
        return [{"role": "USER"}]
```

### html
프론트 엔드상에서 입력을 받아서 서버로 전달
```html
<body>
        <div id="auth-section">
            <h2>Register</h2>
            <form id="register-form">
                <label for="register-username">Username:</label>
                <input type="text" id="register-username" required>
                <label for="register-password">Password:</label>
                <input type="password" id="register-password" required>
                <label for="register-nickname">Nickname:</label>
                <input type="text" id="register-nickname" required>
                <button type="submit">Register</button>
            </form>
</body>
<script>
// Registration
        document.getElementById('register-form').addEventListener('submit', async (e) => {
            e.preventDefault();
            const username = document.getElementById('register-username').value;
            const password = document.getElementById('register-password').value;
            const nickname = document.getElementById('register-nickname').value;

            try {
                const response = await fetch(`${apiBaseUrl}/register/`, {
                    method: 'POST',
                    headers: { 
                        'Content-Type': 'application/json',
                        'Accept': 'application/json'  // 클라이언트가 JSON 응답을 받을 것이라고 명시
                    },
                    body: JSON.stringify({ username, password, nickname })
                });

                const result = await response.json();
                if (response.ok) {
                    alert('Registration successful');
                } else {
                    alert('Registration failed: ' + result.detail);
                }
            } catch (error) {
                console.error('Error:', error);
            }
        });
</script>
```
![image](https://github.com/user-attachments/assets/cf298cc5-54b3-45fe-a324-eda9ca0a1637)

## 결과

프론트엔드로 전달 받은 값을 리스폰

![image](https://github.com/user-attachments/assets/df3d3e7e-06d1-46bb-8533-7b9376b048ca)


postman을 이용한 JSON데이터 결과값 출력

![image](https://github.com/user-attachments/assets/95e66d3e-a978-486b-af64-906f69a5308b)
