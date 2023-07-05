FROM python

EXPOSE 8501

#install pip requirements

ADD requirements.txt /rb_mig/requirements.txt
RUN python3 -m pip install -r /rb_mig/requirements.txt

WORKDIR /rb_mig
ADD . /rb_mig

CMD ["streamlit", "run", "app.py"]