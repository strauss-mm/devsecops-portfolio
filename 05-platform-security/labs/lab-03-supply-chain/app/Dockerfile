FROM python:3.12-slim AS builder
WORKDIR /build
COPY requirements.txt .
RUN pip install --no-cache-dir --target=/deps -r requirements.txt

FROM gcr.io/distroless/python3-debian12:nonroot
WORKDIR /app
COPY --from=builder /deps /deps
COPY app.py .
ENV PYTHONPATH=/deps
EXPOSE 8080
USER 65534:65534
ENTRYPOINT ["python3", "app.py"]
