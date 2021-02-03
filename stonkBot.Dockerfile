FROM python:3.8

COPY --from=uselagoon/python-3.8 /lagoon /lagoon
COPY --from=uselagoon/python-3.8 /bin/fix-permissions /bin/ep /bin/docker-sleep /bin/
COPY --from=uselagoon/python-3.8 /sbin/tini /sbin/
COPY --from=uselagoon/python-3.8 /home /home

ENV TMPDIR=/tmp \
    TMP=/tmp \
    HOME=/home \
    # When Bash is invoked via `sh` it behaves like the old Bourne Shell and sources a file that is given in `ENV`
    ENV=/home/.bashrc \
    # When Bash is invoked as non-interactive (like `bash -c command`) it sources a file that is given in `BASH_ENV`
    BASH_ENV=/home/.bashrc \
    API_Key=""

RUN apt-get install libxml2-dev libxslt-dev make automake gcc g++ jpeg-dev zlib-dev freetype-dev lcms2-dev openjpeg-dev tiff-dev tk-dev tcl-dev

RUN pip install google beautifulsoup4 discord.py yfinance lxml matplotlib arrow cryptocompare kaleido plotly psutil

COPY . /

ENTRYPOINT ["/sbin/tini", "--", "/lagoon/entrypoints.sh"]

CMD ["python", "StonkBot.py"]
