FROM scratch
MAINTAINER <Qianru Zhou>
RUN sudo pip install requests \
&& sudo pip install rdflib \
&& sudo pip install bottle

CMD ["/bin/bash"]
