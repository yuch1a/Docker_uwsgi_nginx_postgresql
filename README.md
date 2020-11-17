# Docker_uwsgi_nginx_postgresql
DockerCopmose with three container uwsgi, nginx, postgresql practice
## 概念
Docker 的系統的架構主要是 Client-Server 的架構
- Server => Docker Daemon
- Client => Docker Client

用 Restful API 連到 Docker daemon，提供 command line 操作
* Docker Image
	獲得1. Docker Hub pull 2. Dockerfile 3. 別台電腦上的Docker image 
* Docker Container
	Docker image 執行起來的 Process，同一個imag可以啟動多個Container。
* Docker Hub(Docker Registry)

---
## 常用指令
1. 安裝docker
2. 啟動docker [systemctl start docker]

執行docker-compose:
1. docker-compose up --build //rebuild
2. docker-compose up -d //背景執行
3. docker-compose -f $yourDockerComposefile up
查看docker-compose 下正在運行的container
1. docker-compose up ps

進入正在運行的容器
docker exec -it [container-id] bash

停止:
刪除所有停止懸空的容器和所有未使用的圖像，容器，捲和網絡
$ docker system prune -a
停止所有的 containers
$ docker stop $(docker ps -a -q) 
刪除所有的 containers
$ docker rm $(docker ps -a -q)
刪除所有的 images
$ docker rmi $(docker images -a -q)
刪除volumes
docker volume ls
docker volume rm volume_name volume_name

---
## 容器間溝通
docker-compose 來建立三個container(nginx, web, database)


![](https://i.imgur.com/NCPwB2C.png)

---
## 目錄結構

![檔案目錄結構](https://i.imgur.com/97fA4ox.jpg)

### nginx
(新建一個nginx資料夾，內有config檔配置以及Dockerfile)

default.conf
```conf
server {
    listen       8080;
    server_name  localhost;
    root         /odin_restful;

    location /static {
        alias /vol/static;
    }
    location / {
        include /etc/nginx/uwsgi_params;
        uwsgi_pass mysite:8001;
    }
}

```
Dockerfile
```Dockerfile
FROM nginxinc/nginx-unprivileged:1-alpine
COPY ./default.conf /etc/nginx/conf.d/default.conf
COPY ./uwsgi_params /etc/nginx/uwsgi_params
USER root
RUN mkdir -p /vol/static
RUN chmod 755 /vol/static
```

### Django
(新建一個Django資料夾，內有Django project，Dockerfile，以及requirement.txt)

Dockerfile
```Dockerfile
FROM python:3.6-slim
ENV PATH="/scripts:${PATH}"
RUN apt-get update && apt-get install -y --no-install-recommends \
        python3-dev \
        libxml2-dev \
        libxslt1-dev \
        libxslt-dev \
        libyajl2 \
        gcc && \
    rm -r /var/lib/apt/lists/* 
COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt
RUN mkdir /mysite
COPY ./mysite /mysite
WORKDIR /mysite

```

requirement.txt
```txt
asgiref==3.3.0; python_version >= '3.5'
django==3.1.3
djangorestframework==3.12.1
pytz==2020.4
sqlparse==0.4.1; python_version >= '3.5'
uwsgi==2.0.19.1
psycopg2-binary>=2.8
```
django project裡新增uwsgi.ini檔
```ini
[uwsgi]
;  指定運行目錄位置
chdir = /mysite
; 選擇協議方式|http = 0.0.0.0:5000|http-socekt = 0.0.0.0:5001|socket = :3031
socket = :8001 
; sock 文件的路径的權限
chmod-socket = 777 
; 主要運行的 py 檔案
wsgi-file =  mysite/wsgi.py 
; 開啟一個主進程，管理其他uwsgi進程(子進程)，如果kill master等於重啟所有uwsgi進程
master = true  
; 生成指定數目的進程
processes = 4
;  每個進程有2個線程
threads = 2
; --stats 设置一个地址，可以通过该地址监控运行状态，输出 JSON 格式的数据
stats = :9191
;  允许用内嵌的语言启动线程。这将允许你在app程序中产生一个子线程
enable-threads = true
;  當服務器退出的時候自動清理環境，刪除unix socket文件和pid文件
vacuum = true
;  pid 文件位置
pidfile =mysite_uwsgi.pid
```

### docker-compose-develop.yml
```yml
version: '3'

services:

  db:
    image: postgres:10
    volumes:
    - pgdata:/var/lib/postgresql/data
    environment:
    - POSTGRES_USER=postgres
    - POSTGRES_PASSWORD=q1w2e3r4
    - POSTGRES_DB=hugin
    ports:
    - "5432:5432"

  mysite:
    build:
      context: ./django
      dockerfile: Dockerfile
    volumes:
    - ./django/mysite:/mysite
    environment:
    - SECRET_KEY=samplesecret123
    - ALLOWED_HOSTS=127.0.0.1,localhost,192.168.56.112
    - DEBUG=1
    command: uwsgi --ini ./mysite_uwsgi.ini
    depends_on:
    - db
    
  nginx:
    build:
      context: ./nginx
      dockerfile: Dockerfile
    volumes:
    - static_data:/vol/static
    ports:
    - "8080:8080"

volumes:
  static_data:
  pgdata:

```


