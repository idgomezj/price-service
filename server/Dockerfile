FROM python:3.10

# set work directory
WORKDIR /app

ENV TZ=America/New_York
ENV ENV=PRODUCTION

# Update and install tzdata
RUN apt-get update 
RUN apt-get install -y tzdata
RUN apt-get install -y jq



# install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r  requirements.txt

# copy project
COPY . .
