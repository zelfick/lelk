FROM python:3.11.0a3-alpine3.15
LABEL maintainer="jorgeherran@hotmail.com"

# upgrade pip
#RUN pip install --upgrade pip

# permissions and nonroot user for tightened security
RUN adduser -D nonroot
RUN mkdir /home/app/ && chown -R nonroot:nonroot /home/app
WORKDIR /home/app
USER nonroot
COPY --chown=nonroot:nonroot . .

# venv
ENV VIRTUAL_ENV=/home/app/venv

# python setup
RUN python -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
RUN export FLASK_APP=app.py
RUN pip install --no-cache -r requirements.txt

# define the port number the container should expose
EXPOSE 8081

# execute application
CMD ["python", "app.py"]


