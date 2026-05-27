"""Health data service interface types.

These attrs classes define the wire format for the OpenHost health-data
service (github.com/imbue-openhost/openhost/services/health-data).
Providers serialize these to JSON; consumers deserialize them.

All timestamps are ISO 8601 strings in UTC (ending in +00:00).
"""

from __future__ import annotations

from enum import Enum

import attr
import attrs


@attr.s(auto_attribs=True, frozen=True)
class MetricType:
    """A metric the provider can serve."""

    # Identifier used in queries, e.g. "heart_rate"
    name: str

    # Human-readable label, e.g. "Heart Rate"
    display_name: str

    # Unit of measurement, e.g. "bpm", "ms", "%"
    unit: str


@attr.s(auto_attribs=True, frozen=True)
class Sample:
    """A single numeric measurement at a point or interval in time."""

    # ISO 8601 UTC start of the measurement
    timestamp: str

    value: float

    # If set, this sample covers the interval [timestamp, end_timestamp)
    end_timestamp: str | None = None


@attr.s(auto_attribs=True, frozen=True)
class TimeSeries:
    """A sequence of samples for one metric."""

    # Metric identifier, e.g. "heart_rate"
    metric: str

    # Unit of measurement, e.g. "bpm"
    unit: str

    samples: list[Sample]

    # Data source identifier, e.g. "oura", "apple_health"
    source: str | None = None


class SleepStage(str, Enum):
    DEEP = "deep"
    LIGHT = "light"
    REM = "rem"
    AWAKE = "awake"
    UNKNOWN = "unknown"


@attr.s(auto_attribs=True, frozen=True)
class SleepStageInterval:
    """A contiguous period spent in one sleep stage."""

    # One of the SleepStage values
    stage: str

    # ISO 8601 UTC
    start: str

    # ISO 8601 UTC
    end: str


@attr.s(auto_attribs=True, frozen=True)
class SleepSession:
    """A complete sleep event (one night or nap)."""

    # ISO 8601 UTC, typically bedtime
    start: str

    # ISO 8601 UTC, typically wake time
    end: str

    stages: list[SleepStageInterval] = attrs.Factory(list)

    # Summary metrics for this session. Common keys:
    #   total_sleep_duration (seconds), deep_sleep_duration (seconds),
    #   light_sleep_duration (seconds), rem_sleep_duration (seconds),
    #   awake_time (seconds), time_in_bed (seconds),
    #   efficiency (percent 0-100), latency (seconds),
    #   average_heart_rate (bpm), lowest_heart_rate (bpm),
    #   average_hrv (ms), average_breath (breaths/min),
    #   sleep_score (0-100, source-specific)
    metrics: dict[str, float] = attrs.Factory(dict)

    source: str | None = None
    id: str | None = None


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

    # ISO 8601 UTC
    start: str

    # ISO 8601 UTC
    end: str

    # Summary metrics for this workout. Common keys:
    #   duration_s (seconds), distance_m (meters), calories (kcal),
    #   average_heart_rate (bpm), max_heart_rate (bpm),
    #   average_pace_s_per_km (seconds per km), elevation_gain_m (meters)
    metrics: dict[str, float] = attrs.Factory(dict)

    source: str | None = None
    id: str | None = None
