FROM python:3

# set work directory
WORKDIR /usr/src/app/

# copy project
COPY . /usr/src/app/

# install dependencies
RUN pip3 install --user aiogram
RUN pip3 install --user wikipedia

EXPOSE 8080

# run app
CMD ["python", "bot.py"]
