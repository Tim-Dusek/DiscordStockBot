FROM uselagoon/python-3.8

ENV API_Key=""

RUN pip install -r requirements.txt

CMD ["python", "StonkBot.py", "-k", "$API_Key"]
