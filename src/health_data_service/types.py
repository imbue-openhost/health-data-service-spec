"""Health data service interface types.

These attrs classes define the wire format for the OpenHost health-data
service (github.com/imbue-openhost/openhost/services/health-data).
Providers serialize these to JSON; consumers deserialize them.

All timestamps are ISO 8601 strings in UTC (ending in +00:00).
"""

from __future__ import annotations

from enum import Enum

import attrs


# ---------------------------------------------------------------------------
# Metric discovery
# ---------------------------------------------------------------------------

@attrs.define
class MetricType:
    """A metric the provider can serve."""

    name: str
    """Identifier used in queries, e.g. ``"heart_rate"``."""

    display_name: str
    """Human-readable label, e.g. ``"Heart Rate"``."""

    unit: str
    """Unit of measurement, e.g. ``"bpm"``, ``"ms"``, ``"%"``."""


# ---------------------------------------------------------------------------
# Time-series (generic numeric samples)
# ---------------------------------------------------------------------------

@attrs.define
class Sample:
    """A single numeric measurement at a point or interval in time."""

    timestamp: str
    """ISO 8601 UTC start of the measurement."""

    value: float

    end_timestamp: str | None = None
    """If set, this sample covers the interval [timestamp, end_timestamp)."""


@attrs.define
class TimeSeries:
    """A sequence of samples for one metric."""

    metric: str
    """Metric identifier, e.g. ``"heart_rate"``."""

    unit: str
    """Unit of measurement, e.g. ``"bpm"``."""

    samples: list[Sample]

    source: str | None = None
    """Data source identifier, e.g. ``"oura"``, ``"apple_health"``."""


# ---------------------------------------------------------------------------
# Sleep
# ---------------------------------------------------------------------------

class SleepStage(str, Enum):
    DEEP = "deep"
    LIGHT = "light"
    REM = "rem"
    AWAKE = "awake"
    UNKNOWN = "unknown"


@attrs.define
class SleepStageInterval:
    """A contiguous period spent in one sleep stage."""

    stage: str
    """One of the ``SleepStage`` values."""

    start: str
    """ISO 8601 UTC."""

    end: str
    """ISO 8601 UTC."""


@attrs.define
class SleepSession:
    """A complete sleep event (one night or nap)."""

    start: str
    """ISO 8601 UTC, typically bedtime."""

    end: str
    """ISO 8601 UTC, typically wake time."""

    stages: list[SleepStageInterval] = attrs.Factory(list)

    metrics: dict[str, float] = attrs.Factory(dict)
    """Summary metrics for this session. Common keys:

    - ``total_sleep_duration`` (seconds)
    - ``deep_sleep_duration`` (seconds)
    - ``light_sleep_duration`` (seconds)
    - ``rem_sleep_duration`` (seconds)
    - ``awake_time`` (seconds)
    - ``time_in_bed`` (seconds)
    - ``efficiency`` (percent, 0-100)
    - ``latency`` (seconds)
    - ``average_heart_rate`` (bpm)
    - ``lowest_heart_rate`` (bpm)
    - ``average_hrv`` (ms)
    - ``average_breath`` (breaths/min)
    - ``sleep_score`` (0-100, source-specific)
    """

    source: str | None = None
    id: str | None = None


# ---------------------------------------------------------------------------
# Workouts
# ---------------------------------------------------------------------------

class WorkoutType(str, Enum):
    RUNNING = "running"
    CYCLING = "cycling"
    SWIMMING = "swimming"
    WALKING = "walking"
    HIKING = "hiking"
    STRENGTH = "strength"
    YOGA = "yoga"
    OTHER = "other"


@attrs.define
class Workout:
    """An exercise session."""

    workout_type: str
    """One of the ``WorkoutType`` values, or a free-form string."""

    start: str
    """ISO 8601 UTC."""

    end: str
    """ISO 8601 UTC."""

    metrics: dict[str, float] = attrs.Factory(dict)
    """Summary metrics for this workout. Common keys:

    - ``duration_s`` (seconds)
    - ``distance_m`` (meters)
    - ``calories`` (kcal)
    - ``average_heart_rate`` (bpm)
    - ``max_heart_rate`` (bpm)
    - ``average_pace_s_per_km`` (seconds per km, for running/walking)
    - ``elevation_gain_m`` (meters)
    """

    source: str | None = None
    id: str | None = None


# ---------------------------------------------------------------------------
# Serialization helpers
# ---------------------------------------------------------------------------

def to_dict(obj: attrs.Attribute) -> dict:
    """Convert an attrs instance to a JSON-serializable dict, dropping None values."""
    return attrs.asdict(obj, filter=lambda a, v: v is not None)


def sample_from_dict(d: dict) -> Sample:
    return Sample(**d)


def time_series_from_dict(d: dict) -> TimeSeries:
    d = dict(d)
    d["samples"] = [sample_from_dict(s) for s in d.get("samples", [])]
    return TimeSeries(**d)


def sleep_stage_interval_from_dict(d: dict) -> SleepStageInterval:
    return SleepStageInterval(**d)


def sleep_session_from_dict(d: dict) -> SleepSession:
    d = dict(d)
    d["stages"] = [sleep_stage_interval_from_dict(s) for s in d.get("stages", [])]
    return SleepSession(**d)


def workout_from_dict(d: dict) -> Workout:
    return Workout(**d)


def metric_type_from_dict(d: dict) -> MetricType:
    return MetricType(**d)
