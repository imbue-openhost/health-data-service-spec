from enum import Enum

import attr

from src.health_data_service import TimeSeries, Sample
from src.health_data_service.data_types import IntervalSample, Container, ScalarMetric


## Sample Types

class SleepStage(str, Enum):
    DEEP = "deep"
    LIGHT = "light"
    REM = "rem"
    AWAKE = "awake"
    UNKNOWN = "unknown"

## Scalar metrics
# (these typically are associated with a container)

@attr.s(auto_attribs=True, frozen=True)
class Duration(ScalarMetric[float]):
    metric_id: str = "duration"
    display_name: str = "Duration"
    unit: str = "min"



## Time series metrics

@attr.s(auto_attribs=True, frozen=True)
class HeartRate(TimeSeries):
    metric_id: str = "heart_rate"
    display_name: str = "Heart Rate"
    unit: str = "bpm"
    samples: list[Sample[float]]


@attr.s(auto_attribs=True, frozen=True)
class HRV_RMSSD(TimeSeries):
    metric_id: str = "hrv_rmssd"
    display_name: str = "Heart Rate Variability (RMSSD)"
    unit: str = "(unitless)"
    samples: list[Sample[float]]


@attr.s(auto_attribs=True, frozen=True)
class SleepStages(TimeSeries):
    metric_id: str = "sleep_stages"
    display_name: str = "Sleep Stages"
    unit: str = "(unitless)"
    samples: list[IntervalSample[SleepStage]]

## Containers


@attr.s(auto_attribs=True, frozen=True)
class SleepSession(Container):
    """A complete sleep event (one night or nap)."""
    stages: SleepStages

    # scalars
    total_duration: Duration

