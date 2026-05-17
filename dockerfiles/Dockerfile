FROM docker.arvancloud.ir/python:3.14-slim

WORKDIR /usr/app


RUN useradd -u 1001 nonroot


ENV PYTHONPATH=/usr/app/src


COPY requirements.txt .


RUN pip install \
	--no-cache-dir \
	-i https://pypi.devneeds.ir/simple \
	-r requirements.txt


COPY . .


RUN pip install -i https://pypi.devneeds.ir/simple .


ENTRYPOINT ["./entrypoint.sh"]


USER nonroot


EXPOSE 8000


CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--proxy-headers", "--forwarded-allow-ips", "*"]
