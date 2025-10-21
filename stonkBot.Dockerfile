FROM python:3.11

COPY --from=uselagoon/python-3.11 /lagoon /lagoon
COPY --from=uselagoon/python-3.11 /bin/fix-permissions /bin/ep /bin/docker-sleep /bin/
COPY --from=uselagoon/python-3.11 /home /home

ENV TMPDIR=/tmp \
    TMP=/tmp \
    HOME=/home \
    # When Bash is invoked via `sh` it behaves like the old Bourne Shell and sources a file that is given in `ENV`
    ENV=/home/.bashrc \
    # When Bash is invoked as non-interactive (like `bash -c command`) it sources a file that is given in `BASH_ENV`
    BASH_ENV=/home/.bashrc \
    API_Key=""

RUN apt-get update && apt-get install -y libxml2-dev libxslt-dev make automake gcc g++ libjpeg-dev zlib1g-dev libfreetype6-dev liblcms2-dev libjpeg-dev libtiff-dev tk-dev tcl-dev libnss3 libatk-bridge2.0-0 libcups2 libxcomposite1 libxdamage1 libxfixes3 libxrandr2 libgbm1 libxkbcommon0 libpango-1.0-0 libcairo2 libasound2

COPY . /

RUN pip install --upgrade -r requirements.txt

RUN python setup.py

CMD ["python", "StonkBot.py"]