FROM ubuntu:22.04
RUN apt update
RUN apt install -y build-essential git
COPY . /afl
RUN cd /afl && make -j32
ENTRYPOINT ["/afl/afl-fuzz"]
