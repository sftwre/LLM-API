FROM python:3.10

WORKDIR /usr/src/app/

COPY . .
RUN pip install --no-cache-dir -r requirements.txt

# install redis system packages
RUN apt-get update && apt-get -y install redis-server

# Expose port for uvicorn
EXPOSE 8000

# luanch application
ENTRYPOINT [ "./launch.sh" ]