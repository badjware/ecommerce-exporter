FROM python:3.10
COPY . /tmp/package
RUN pip install --no-cache-dir /tmp/package && \
    rm -r /tmp/package
EXPOSE 8000
ENTRYPOINT ["ecommerce-exporter"]