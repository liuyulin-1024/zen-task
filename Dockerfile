FROM harbor.autogame.ai/backend/python-base:v1.0

COPY requirements.txt ./

RUN pip install -r requirements.txt

COPY . .

ENTRYPOINT ["python", "main"]
