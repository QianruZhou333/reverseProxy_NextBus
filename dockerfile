FROM python:2.7.12
RUN sudo pip install requests \
&& sudo pip install rdflib \
&& sudo pip install bottle

CMD ["python", "reverseProxy.py"]
