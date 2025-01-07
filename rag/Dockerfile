FROM nvidia/cuda:12.6.3-cudnn-runtime-ubuntu24.04

LABEL "author"="Abraham Sanchez"

RUN apt update && \
    apt install --no-install-recommends -y \
    curl \
    python3 \
    python3-pip \
    python3-venv \
    libmagic-dev \
    ffmpeg \
    libsm6 \
    libxext6 \
    && apt clean \
    && apt autoremove \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /api

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN pip install -U -q --no-cache-dir pip wheel

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

ADD app/ app/
ADD models/ models/

EXPOSE 8080

CMD ["hypercorn", "app.main:app", "--bind", "0.0.0.0:8080", "--access-logfile", "-"]
