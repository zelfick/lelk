# The collector is configured for simple accepts the metrics and just exports them as metrics

# To run the collector in a container
docker run -p 4317:4317 \
    -v /tmp/otel-collector-config.yaml:/etc/otel-collector-config.yaml \
    otel/opentelemetry-collector:latest \
    --config=/etc/otel-collector-config.yaml

# to run from dockercompose
docker compose -f dockercompose.collector.yaml