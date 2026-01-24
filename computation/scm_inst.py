from circumplex.instruments.models import (
    Instrument,
    InstrumentScale,
    ResponseAnchor,
    register_instrument,
)

SCALES = (
    InstrumentScale("PAQ1", 0, label="Pleasant", items=()),
    InstrumentScale("PAQ2", 45, label="Vibrant", items=()),
    InstrumentScale("PAQ3", 90, label="Eventful", items=()),
    InstrumentScale("PAQ4", 135, label="Chaotic", items=()),
    InstrumentScale("PAQ5", 180, label="Annoying", items=()),
    InstrumentScale("PAQ6", 225, label="Monotonous", items=()),
    InstrumentScale("PAQ7", 270, label="Uneventful", items=()),
    InstrumentScale("PAQ8", 315, label="Calm", items=()),
)

ANCHORS = (
    ResponseAnchor(0, "Strongly disagree"),
    ResponseAnchor(1, "Somewhat disagree"),
    ResponseAnchor(2, "Neither agree nor disagree"),
    ResponseAnchor(3, "Somewhat agree"),
    ResponseAnchor(4, "Strongly agree"),
)

scm = Instrument(
    name="Soundscape Circumplex Model",
    abbrev="SCM",
    construct="urban soundscape perception",
    reference="Axelsson, Nilsson, & Berglund (2010)",
    url="https://doi.org/10.1121/1.3493436",
    status="open-access",
    scales=SCALES,
    anchors=ANCHORS,
    items=None,
    prefix="For each of the 8 scales below, to what extent do you agree or disagree that the present surrounding sound environment is...",
    suffix="",
)

register_instrument("scm", scm)
