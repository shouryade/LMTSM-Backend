#
FROM python:3.10

#
WORKDIR /app

#
COPY ./requirements.txt /app/requirements.txt

#
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

#
EXPOSE 5390

#
COPY . /app/

#
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8100", "--reload"]