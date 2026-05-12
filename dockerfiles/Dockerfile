FROM docker.arvancloud.ir/python:3.14-slim

WORKDIR /usr/app


ENV PYTHONPATH=/usr/app/src


COPY requirements.txt .


RUN pip install \
	--no-cache-dir \
	-i https://mirror-pypi.runflare.com/simple \
	-r requirements.txt


COPY . .


RUN pip install .


ENTRYPOINT ["./entrypoint.sh"]


CMD ["fastapi", "run", "--host", "0.0.0.0", "--port", "8000"]
