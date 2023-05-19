# Create a virtual environment and activate it
```
python3 -m venv rolldice
source rolldice/bin/activate
```

# Install flask and run the application
```
pip install flask
flask run -p 8081
```

# Validate the application is running by curl from a terminal or just by opening in your web browser:
```
http://localhost:8081/rolldice
curl http://localhost:8081/rolldice
```

# Create and test the dockerfile
```
docker build -f rolldice.dockerfile -t zelfick/rolldice .
docker run -d --rm --name rolldice -p 8081:8081 docker.io/zelfick/rolldice
```

# Instrument opentelemetry in the app
Automatic instrumentation will generate telemetry data on your behalf. There are several options you can take, covered in more detail in Automatic Instrumentation. Here we’ll use the opentelemetry-instrument agent.
Install the opentelemetry-distro package, which contains the OpenTelemetry API, SDK and also the tools opentelemetry-bootstrap and opentelemetry-instrument you will use below.

```pip install opentelemetry-distro```

Run the opentelemetry-bootstrap command:

```opentelemetry-bootstrap -a install```

This will install Flask instrumentation.

# Run the instrumented app
You can now run your instrumented app with opentelemetry-instrument and have it print to the console for now:
```
opentelemetry-instrument \
    --traces_exporter console \
    --metrics_exporter console \
    --logs_exporter console \
    flask run -p 8081
```
# Add manual instrumentation to automatic instrumentation 
Automatic instrumentation captures telemetry at the edges of your systems, such as inbound and outbound HTTP requests, but it doesn’t capture what’s going on in your application. For that you’ll need to write some manual instrumentation. Here’s how you can easily link up manual instrumentation with automatic instrumentation.

# Traces
First, modify app.py to include code that initializes a tracer and uses it to create a trace. Run the app again to see the traces:
```
opentelemetry-instrument \
    --traces_exporter console \
    --metrics_exporter console \
    flask run -p 8081
```
The parent_id of do_roll is the same is the span_id for /rolldice, indicating a parent-child relationship!

# Metrics 
Now modify app.py to include code that initializes a meter and uses it to create a counter instrument which counts the number of rolls for each possible roll value.
Now run the app again:
```
opentelemetry-instrument \
    --traces_exporter console \
    --metrics_exporter console \
    flask run -p 8081
```
# There was defined a simple otel collector, so star it up with docker:
docker run --rm -p 4317:4317 \
    -v ${PWD}/collector/otelcollectorconfig.yaml:/etc/otel-collector-config.yaml \
    otel/opentelemetry-collector-contrib:0.77.0 --config=/etc/otel-collector-config.yaml

# Modify the command to export spans and metrics via OTLP
The next step is to modify the command to send spans and metrics to the collector via OTLP instead of the console.
To do this, install the OTLP exporter package:
```pip install opentelemetry-exporter-otlp```

The opentelemetry-instrument agent will detect the package you just installed and default to OTLP export when it’s run next. Run the application like before, but don’t export to the console:
```
opentelemetry-instrument flask run -p 8081
```
By default, opentelemetry-instrument exports traces and metrics over OTLP/gRPC and will send them to localhost:4317, which is what the collector is listening on.
When you access the /rolldice route now, you’ll see output in the collector process instead of the flask process.


# Start the project
docker compose -f dockercompose.otel.yaml up