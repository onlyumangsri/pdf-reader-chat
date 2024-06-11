FROM python:3.9

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY . .

EXPOSE 8888

CMD ["panel", "serve", "/code/UsingLangchain.py", "--address", "0.0.0.0", "--port", "8888", "--allow-websocket-origin", "localhost:8888", "--allow-websocket-origin", "0.0.0.0:8888"]


