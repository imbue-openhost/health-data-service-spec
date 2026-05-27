"""Health data service interface types.

These attrs classes define the wire format for the OpenHost health-data
service (github.com/imbue-openhost/openhost/services/health-data).
Providers serialize these to JSON; consumers deserialize them.

All timestamps are datetime.datetime objects (should be timezone-aware UTC).
On the wire they are serialized as ISO 8601 strings.
"""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any

import attr
import attrs

## Samples

@attr.s(auto_attribs=True, frozen=True)
class Sample[T]:
    timestamp: datetime
    value: T


@attr.s(auto_attribs=True, frozen=True)
class IntervalSample[T](Sample[T]):
    # this sample covers the interval [timestamp, end_timestamp)
    end_timestamp: datetime


## Metrics

@attr.s(auto_attribs=True, frozen=True)
class ScalarMetric[T]:
    """A single metric with no timestamp, usually associated with a container."""
    # Metric identifier, e.g. "heart_rate"
    metric_id: str
    display_name: str

    # Unit of measurement, e.g. "bpm"
    unit: str | None

    value: T

    # Data source identifier, e.g. "oura", "apple_watch", etc
    source: str


@attr.s(auto_attribs=True, frozen=True)
class TimeSeries:
    """A sequence of samples for one metric."""
    # Metric identifier, e.g. "heart_rate"
    metric_id: str
    display_name: str

    # Unit of measurement, e.g. "bpm"
    unit: str | None

    samples: list[Sample]

    # Data source identifier, e.g. "oura", "apple_watch", etc
    source: str


@attr.s(auto_attribs=True, frozen=True)
class Container:
    """Groups metrics together that are derived from a single event, eg a sleep session or workout."""
    start: datetime
    end: datetime
    # scalars:  dict[str, Any]
    # time_series: dict[str, float]



class WorkoutType(str, Enum):
    RUNNING = "running"
    CYCLING = "cycling"
    SWIMMING = "swimming"
    WALKING = "walking"
    HIKING = "hiking"
    STRENGTH = "strength"
    YOGA = "yoga"
    OTHER = "other"


@attr.s(auto_attribs=True, frozen=True)
class Workout:
    """An exercise session."""

    # One of the WorkoutType values, or a free-form string
    workout_type: str

    start: datetime
    end: datetime

    # Summary metrics for this workout. Common keys:
    #   duration_s (seconds), distance_m (meters), calories (kcal),
    #   average_heart_rate (bpm), max_heart_rate (bpm),
    #   average_pace_s_per_km (seconds per km), elevation_gain_m (meters)
    metrics: dict[str, float] = attrs.Factory(dict)

    source: str | None = None
    id: str | None = None
