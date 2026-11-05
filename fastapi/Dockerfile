# syntax=docker/dockerfile:1.7
# ---------- deps ----------
FROM python:3.12-slim AS deps

WORKDIR /build

COPY requirements.txt .

RUN --mount=type=cache,target=/root/.cache/pip \
    pip install \
    --prefix=/install \
    -r requirements.txt
# ---------- Common Git Stage ----------
FROM deps AS git-base

COPY --from=deps /install /usr/local

RUN --mount=type=cache,target=/var/cache/apt \
    apt-get update && \
    apt-get install -y git

# ---------- aegis link ----------
FROM git-base AS link

COPY --from=deps /install /usr/local

RUN git clone --depth=1 https://github.com/bearddaniel80-netizen/aegis-link.git

WORKDIR aegis-link/src

RUN python -m build

RUN mv dist/*.whl /tmp/

# ------------ aql -----------------
FROM git-base AS aql

COPY --from=deps /install /usr/local

WORKDIR /downloads

RUN git clone --depth=1 https://github.com/bearddaniel80-netizen/aql-public.git

WORKDIR /downloads/aql-public/src

RUN python -m build

RUN mv dist/*.whl /tmp/

WORKDIR /app

RUN cp -R /downloads/aql-public/data/* .

RUN cp /downloads/aql-public/README.md .

# ----------- runtime ------

FROM deps AS runtime

COPY --from=deps /install /usr/local

COPY --from=link /tmp/*.whl /tmp
RUN pip install /tmp/*.whl

COPY --from=aql /tmp/*.whl /tmp
RUN pip install /tmp/*.whl

WORKDIR /app

COPY --from=aql /app .

# Linux tool md2html
RUN --mount=type=cache,target=/var/cache/apt \
    apt-get update && \
    apt-get install -y pandoc

COPY . .

CMD [  "uvicorn",  "app.main:app",  "--host",  "0.0.0.0",  "--port",  "8000"]