FROM python:3.7
ADD . /usr/local/app
WORKDIR /usr/local/app
RUN pip install -r requirements.txt -i https://pypi.douban.com/simple
ENTRYPOINT ["python","./mock-web.py"]