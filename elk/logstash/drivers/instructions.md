# JSON driver (default)
more doc in: https://docs.docker.com/config/containers/logging/json-file/
Run a container with default driver and define its log size and quantity of files
```
docker run -it --log-opt max-size=5m --log-opt max-file=3 alpine ash
```

# Gelf driver (Recomended for logstash)
more doc in: https://docs.docker.com/config/containers/logging/gelf/
Enable a container to write to gelf server, verify the correct address of your server
```
docker run -dit --log-driver=gelf \
    --log-opt gelf-address=udp://x.x.x.x:12201 \
    alpine sh
```

# Syslog driver
You will need to run this per container, and the result is a pipeline of Docker container logs being outputted into your syslog instance. These, in turn, will be forwarded to the Logstash container for parsing and data enhancement, and from there into Elasticsearch.
```
docker run \
 --log-driver=syslog \
 --log-opt syslog-address=tcp://:5000
 \ --log-opt syslog-facility=daemon
 \ alpine ash
```