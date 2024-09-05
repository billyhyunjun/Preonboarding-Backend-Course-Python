# EC2 배포 하기

작성된 웹 어플리케이션을 github로 이동하고 해당 코드를 EC2에 배포해 보기

### 인스턴스 생성

![image](https://github.com/user-attachments/assets/ec898ee7-b6dc-427a-96b5-76e5472ff3f9)

### 터미널을 이용한 서버 설정

![image](https://github.com/user-attachments/assets/266e1e2a-fc79-400a-bc34-6e965dddf789)

### 보안 규칙 설정

![image](https://github.com/user-attachments/assets/0958cf84-27cb-435c-b657-f2069d5b911f)

### mobaXterm을 이용한 터미널 실행

![image](https://github.com/user-attachments/assets/2a02224a-2932-4d52-855e-515cefd1f533)


### 필수 설치

```bash
sudo apt update -y  # 패키지 목록 업데이트
sudo apt upgrade -y  # 시스템 패키지 업그레이드
sudo apt install python3-pip python3-venv git -y  # Python, pip, virtualenv, Git 설치

python3 -m venv venv
source venv/bin/activate

git clone https://github.com/billyhyunjun/Preonboarding-Backend-Course-Python.git
cd Preonboarding-Backend-Course-Python

sudo pip install -r requirements.txt

python manage.py migrate

python manage.py collectstatic

sudo pip install gunicorn

sudo apt install nginx -y
```

### 서버 실행

![image](https://github.com/user-attachments/assets/1ba40c9e-8625-4661-b7ac-d483207d0587)

### 서버 접속 

![image](https://github.com/user-attachments/assets/4b0158f6-ba1e-4e95-8eb9-bd7b2e8cc18b)
