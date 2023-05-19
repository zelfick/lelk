from random import randint
from flask import Flask

# import traces to implement manually
from opentelemetry import trace
# import metrics to implement manually 
from opentelemetry import metrics

# Acquire a tracer
tracer = trace.get_tracer("diceroller.tracer")
# Acquire a meter.
meter = metrics.get_meter("diceroller.meter")

# Now create a counter instrument to make measurements with
roll_counter = meter.create_counter(
    "roll_counter",
    description="The number of rolls by roll value",
)

app = Flask(__name__)

@app.route("/")
def root():
    return "<p>Simple app to generate aleatory numbers at path /rolldice</p>"


@app.route("/rolldice")
def roll_dice():
    return str(do_roll())

def do_roll():
    # This creates a new span that's the child of the current one
    with tracer.start_as_current_span("do_roll") as rollspan:
        res = randint(1, 10)
        rollspan.set_attribute("roll.value", res)
        # This adds 1 to the counter for the given roll value (roll_counter)
        roll_counter.add(1, {"roll.value": res})
        return res