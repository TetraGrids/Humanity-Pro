# Container for the component explorer.
# The image is only the Python runtime. Mount this repo at /src so the
# catalog can be regenerated from contracts, plugins, and programs.
#
#   docker build -f web/components/Dockerfile -t humanity-components web/components
#   docker run --rm -p 8080:8080 -v "$PWD":/src humanity-components
#
# Open http://127.0.0.1:8080/
FROM python:3.12-alpine
WORKDIR /src
ENV HUMANITY_ROOT=/src
ENV PORT=8080
EXPOSE 8080
ENTRYPOINT ["python3", "web/components/serve.py"]
