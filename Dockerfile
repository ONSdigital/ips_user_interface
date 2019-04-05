FROM python:3.7

COPY . /ips
WORKDIR /ips
RUN pip install -r requirements.txt
EXPOSE 5000

ENV API_HOST=${API_HOST}
ENV API_PORT=${API_PORT}
ENV API_PROTOCOL=${API_PTOTOCOL}
ENV UI_FLASK_APP=ips
ENV FLASK_ENV=development

CMD [ "python", "-m", "flask", "run", "--host=0.0.0.0" ]