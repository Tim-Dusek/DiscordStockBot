FROM uselagoon/python-3.8

ENV API_Key=""

RUN apk add libxml2-dev libxslt-dev make automake gcc g++ jpeg-dev zlib-dev freetype-dev lcms2-dev openjpeg-dev tiff-dev tk-dev tcl-dev

COPY . /

RUN pip install -r requirements.txt

CMD ["python", "StonkBot.py", "-k", "$API_Key"]
