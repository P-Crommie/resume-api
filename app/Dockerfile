FROM amazon/aws-lambda-python:3.12

WORKDIR ${LAMBDA_TASK_ROOT}

RUN /var/lang/bin/python3.12 -m pip install --upgrade pip

COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the function code
COPY api.py .

# Set the CMD to your handler
CMD ["api.lambda_handler"]
