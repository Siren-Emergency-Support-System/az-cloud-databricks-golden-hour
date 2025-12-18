# React Client

## VM Machine setup

VM에 React와 SSL 테스트 환경을 설치합니다.

### Nginx 설치

```sh
sudo apt update
sudo apt install nginx -y

sudo systemctl status nginx
```

### Git 설치

```sh
sudo apt update
sudo apt install git -y
git --version
```

### Self-Sign 으로 SSL 흉내 (Test)

```sh

sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
-keyout /etc/ssl/private/nginx-selfsigned.key \
-out /etc/ssl/certs/nginx-selfsigned.crt

# Common Name에는 프론트엔드 주소 입력: 20.xxx.137.72
```

### 임시 Nginx 세팅

```sh
sudo nano /etc/nginx/sites-available/emc_project
# config 내용은 하단 섹션 참조.

# 활성 링크 생성
sudo ln -s /etc/nginx/sites-available/emc_project /etc/nginx/sites-enabled/

# 기본 활성화는 제거
sudo rm /etc/nginx/sites-enabled/default

# 테스트 후 재시작
sudo nginx -t           # 설정 파일 문법에 오타가 없는지 확인
sudo systemctl restart nginx
```

**config 파일에 입력할 내용:**

```txt
server {
    listen 443 ssl;
    server_name 20.xxx.137.72;      # IP주소로 변경

    ssl_certificate /etc/ssl/certs/nginx-selfsigned.crt;
    ssl_certificate_key /etc/ssl/private/nginx-selfsigned.key;

    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;

    location / {
        root /var/www/html; # React 빌드 경로
        index index.html;
        try_files $uri $uri/ /index.html;
    }

    # API 및 WebSocket 프록시
    location /ws {
        proxy_pass http://127.0.0.1:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
    }
}

# HTTP(80)로 접속 시 HTTPS로 강제 리다이렉트
server {
    listen 80;
    server_name 서버_IP_주소;
    return 301 https://$host$request_uri;
}

```
