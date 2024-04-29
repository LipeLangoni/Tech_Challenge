FROM public.ecr.aws/lambda/python:3.10

COPY . ${LAMBDA_TASK_ROOT}

RUN pip install -r requirements/requirements.txt --ignore-installed --target "${LAMBDA_TASK_ROOT}"

CMD ["src.main.handler"]