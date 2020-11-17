#!/bin/sh

set -e


uwsgi --socket :8000 --master --enable-threads --module odin_restful.wsgi
