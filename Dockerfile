FROM python:3.6
ENV PYTHONUNBUFFERED 1

# Allows docker to cache installed dependencies between builds
#COPY ./requirements.txt requirements.txt


# Adds our application code to the image
COPY . code
WORKDIR code

RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple pipenv && \
    pip install --upgrade pip && \
    pipenv install --system --deploy --ignore-pipfile


EXPOSE 8000

# Migrates the database, uploads staticfiles, and runs the production server
CMD ./manage.py migrate && \
    ./manage.py collectstatic --noinput && \
    newrelic-admin run-program gunicorn --bind 0.0.0.0:$PORT --access-logfile - MSBlog.wsgi:application
