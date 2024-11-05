FROM public.ecr.aws/lambda/python:3.10

WORKDIR ${LAMBDA_TASK_ROOT}

RUN yum install -y \
    libgirepository1.0-dev \
    cairo-devel \
    pango-devel \
    && yum clean all

COPY pyproject.toml poetry.lock ${LAMBDA_TASK_ROOT}

RUN pip install --no-cache poetry

RUN poetry config virtualenvs.create false && \
    poetry install --no-root --no-interaction --no-ansi && \
    poetry export -f requirements.txt --output requirements.txt --without-hashes && \
    pip install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"

COPY . .

CMD ["app.handler"]
