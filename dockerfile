FROM python:3.10

WORKDIR /project

COPY ./requirements.txt /project/requirements.txt
COPY ./database /project/database
COPY ./images /project/images
COPY ./migration /project/migration
COPY ./models /project/models
COPY ./routers /project/routers
COPY ./security /project/security
COPY ./utils /project/utils
COPY ./.env /project/.env
COPY ./alembic.ini /project/alembic.ini
COPY ./admin_back_auth.py /project/admin_back_auth.py
COPY ./main.py /project/main.py

RUN pip install --no-cache-dir --upgrade -r /project/requirements.txt

CMD ["gunicorn", "main:app", "--workers", "8", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind", "127.0.0.1:8000"]