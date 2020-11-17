FROM python:3.6-slim

ENV PATH="/scripts:${PATH}"

#RUN echo -e "http://nl.alpinelinux.org/alpine/v3.12/main\nhttp://alpine.cs.nctu.edu.tw/alpine/v3.12/main" > /etc/apk/repositories
# RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.ustc.edu.cn/g' /etc/apk/repositories
# RUN apk add --update --no-cache --virtual .tmp gcc libc-dev linux-headers

RUN apt-get update && apt-get install -y --no-install-recommends \
        python3-dev \
        libxml2-dev \
        libxslt1-dev \
        libxslt-dev \
        libyajl2 \
        gcc && \
    rm -r /var/lib/apt/lists/* 
    
COPY ../requirements.txt /requirements.txt
RUN pip install -r /requirements.txt
# RUN apk del .tmp

RUN mkdir /odin_restful
COPY ../odin_restful /odin_restful
WORKDIR /odin_restful

# COPY ./scripts /scripts
# +x 給予執行權限 / -x去除執行權限。chmod +x 和chmod a+x 是一樣的(u:用戶|g:用戶組|a:所有|o:其他)
# RUN chmod +x /scripts/*  

RUN mkdir -p /vol/web/media
RUN mkdir -p /vol/web/static
# RUN adduser -D user
# RUN chown -R user:user /vol
# RUN chmod -R 755 /vol/web/
# USER user
# RUN python manage.py collectstatic --noinput
# CMD ["entrypoint.sh"]
# CMD ["uwsgi", "odin_restful_uwsgi.ini"]