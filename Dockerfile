FROM python:3.8 as builder

RUN curl -s https://packagecloud.io/install/repositories/github/git-lfs/script.deb.sh | bash && \
    apt-get install -y git-lfs poppler-utils cmake libpoppler-cpp0v5 libpoppler-cpp-dev poppler-utils poppler-data libpopplerkit-dev && \
    git lfs install && \
    git clone https://huggingface.co/BAAI/bge-large-en-v1.5 /embedding_model && \
    rm -rf /embedding_model/.git

RUN mkdir -p /work/store

FROM nvidia/cuda:11.6.1-devel-ubuntu20.04

COPY --from=builder /work/store /work/store
COPY --from=builder /embedding_model /embedding_model

RUN apt-get update && apt-get -y install python3-pip && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
RUN pip install -r requirements.txt

WORKDIR /work

RUN spacy download de_core_news_lg
COPY fasttext .
COPY lid.176.bin .

COPY images/ /work/images/
COPY *.py /work/

ENV PYTHONPATH /work/

CMD ["streamlit", "run", "jules_celestia.py", "--server.port", "1235"]
