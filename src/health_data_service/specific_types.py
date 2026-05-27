"""Concrete metric and container types for health data.

These subclass the generic types in data_types.py to represent
real-world health data from wearables (Oura, Apple Watch, etc).
"""

from __future__ import annotations

from datetime import datetime
from enum import Enum

import attr
import attrs

from .data_types import Container, IntervalSample, Sample, ScalarMetric, TimeSeries


# ---------------------------------------------------------------------------
# Sample value types
# ---------------------------------------------------------------------------

class SleepStage(str, Enum):
    DEEP = "deep"
    LIGHT = "light"
    REM = "rem"
    AWAKE = "awake"
    UNKNOWN = "unknown"


class WorkoutType(str, Enum):
    RUNNING = "running"
    CYCLING = "cycling"
    SWIMMING = "swimming"
    WALKING = "walking"
    HIKING = "hiking"
    STRENGTH = "strength"
    YOGA = "yoga"
    OTHER = "other"


# ---------------------------------------------------------------------------
# Scalar metric types
# ---------------------------------------------------------------------------

@attr.s(auto_attribs=True, frozen=True)
class Duration(ScalarMetric[float]):
    metric_id: str = "duration"
    display_name: str = "Duration"
    unit: str = "min"


@attr.s(auto_attribs=True, frozen=True)
class HeartRateAvg(ScalarMetric[float]):
    metric_id: str = "average_heart_rate"
    display_name: str = "Avg Heart Rate"
    unit: str = "bpm"


@attr.s(auto_attribs=True, frozen=True)
class HeartRateMin(ScalarMetric[float]):
    metric_id: str = "lowest_heart_rate"
    display_name: str = "Lowest Heart Rate"
    unit: str = "bpm"


@attr.s(auto_attribs=True, frozen=True)
class HRVAvg(ScalarMetric[float]):
    metric_id: str = "average_hrv"
    display_name: str = "Avg HRV"
    unit: str = "ms"


@attr.s(auto_attribs=True, frozen=True)
class BreathRateAvg(ScalarMetric[float]):
    metric_id: str = "average_breath"
    display_name: str = "Avg Breath Rate"
    unit: str = "breaths/min"


@attr.s(auto_attribs=True, frozen=True)
class Efficiency(ScalarMetric[float]):
    metric_id: str = "efficiency"
    display_name: str = "Efficiency"
    unit: str = "%"


@attr.s(auto_attribs=True, frozen=True)
class Score(ScalarMetric[float]):
    """A 0-100 score (readiness, sleep quality, etc)."""
    metric_id: str = "score"
    display_name: str = "Score"
    unit: str | None = None


@attr.s(auto_attribs=True, frozen=True)
class Count(ScalarMetric[int]):
    metric_id: str = "count"
    display_name: str = "Count"
    unit: str | None = None


@attr.s(auto_attribs=True, frozen=True)
class TemperatureDeviation(ScalarMetric[float]):
    metric_id: str = "temperature_deviation"
    display_name: str = "Temp Deviation"
    unit: str = "°C"


@attr.s(auto_attribs=True, frozen=True)
class Distance(ScalarMetric[float]):
    metric_id: str = "distance"
    display_name: str = "Distance"
    unit: str = "m"


@attr.s(auto_attribs=True, frozen=True)
class Pace(ScalarMetric[float]):
    """Pace in seconds per kilometer."""
    metric_id: str = "pace"
    display_name: str = "Pace"
    unit: str = "s/km"


@attr.s(auto_attribs=True, frozen=True)
class Calories(ScalarMetric[float]):
    metric_id: str = "calories"
    display_name: str = "Calories"
    unit: str = "kcal"


# ---------------------------------------------------------------------------
# Time series metric types
# ---------------------------------------------------------------------------

@attr.s(auto_attribs=True, frozen=True)
class HeartRate(TimeSeries):
    metric_id: str = "heart_rate"
    display_name: str = "Heart Rate"
    unit: str = "bpm"
    samples: list[Sample[float]] = attrs.Factory(list)


@attr.s(auto_attribs=True, frozen=True)
class HRV_RMSSD(TimeSeries):
    metric_id: str = "hrv_rmssd"
    display_name: str = "Heart Rate Variability (RMSSD)"
    unit: str | None = None
    samples: list[Sample[float]] = attrs.Factory(list)


@attr.s(auto_attribs=True, frozen=True)
class SleepStages(TimeSeries):
    metric_id: str = "sleep_stages"
    display_name: str = "Sleep Stages"
    unit: str | None = None
    samples: list[IntervalSample[SleepStage]] = attrs.Factory(list)


# ---------------------------------------------------------------------------
# Containers: Sleep
# ---------------------------------------------------------------------------

@attr.s(auto_attribs=True, frozen=True)
class SleepSession(Container):
    """A complete sleep event (one night or nap)."""

    # Stage timeline
    stages: SleepStages | None = None

    # Time series during sleep
    heart_rate: HeartRate | None = None
    hrv: HRV_RMSSD | None = None

    # Duration metrics
    total_duration: Duration | None = None
    deep_sleep_duration: Duration | None = None
    light_sleep_duration: Duration | None = None
    rem_sleep_duration: Duration | None = None
    awake_time: Duration | None = None
    time_in_bed: Duration | None = None
    latency: Duration | None = None

    # Heart metrics (session-level summaries)
    average_heart_rate: HeartRateAvg | None = None
    lowest_heart_rate: HeartRateMin | None = None
    average_hrv: HRVAvg | None = None

    # Other metrics
    average_breath: BreathRateAvg | None = None
    efficiency: Efficiency | None = None
    restless_periods: Count | None = None
    sleep_score: Score | None = None

    source: str | None = None
    id: str | None = None


# ---------------------------------------------------------------------------
# Daily time series (one sample per day)
# ---------------------------------------------------------------------------

# Readiness

@attr.s(auto_attribs=True, frozen=True)
class ReadinessScore(TimeSeries):
    metric_id: str = "readiness_score"
    display_name: str = "Readiness Score"
    unit: str | None = None
    samples: list[Sample[float]] = attrs.Factory(list)


@attr.s(auto_attribs=True, frozen=True)
class ReadinessActivityBalance(TimeSeries):
    metric_id: str = "readiness_activity_balance"
    display_name: str = "Activity Balance"
    unit: str | None = None
    samples: list[Sample[float]] = attrs.Factory(list)


@attr.s(auto_attribs=True, frozen=True)
class ReadinessBodyTemperature(TimeSeries):
    metric_id: str = "readiness_body_temperature"
    display_name: str = "Body Temperature"
    unit: str | None = None
    samples: list[Sample[float]] = attrs.Factory(list)


@attr.s(auto_attribs=True, frozen=True)
class ReadinessHRVBalance(TimeSeries):
    metric_id: str = "readiness_hrv_balance"
    display_name: str = "HRV Balance"
    unit: str | None = None
    samples: list[Sample[float]] = attrs.Factory(list)


@attr.s(auto_attribs=True, frozen=True)
class ReadinessPreviousDayActivity(TimeSeries):
    metric_id: str = "readiness_previous_day_activity"
    display_name: str = "Previous Day Activity"
    unit: str | None = None
    samples: list[Sample[float]] = attrs.Factory(list)


@attr.s(auto_attribs=True, frozen=True)
class ReadinessPreviousNight(TimeSeries):
    metric_id: str = "readiness_previous_night"
    display_name: str = "Previous Night"
    unit: str | None = None
    samples: list[Sample[float]] = attrs.Factory(list)


@attr.s(auto_attribs=True, frozen=True)
class ReadinessRecoveryIndex(TimeSeries):
    metric_id: str = "readiness_recovery_index"
    display_name: str = "Recovery Index"
    unit: str | None = None
    samples: list[Sample[float]] = attrs.Factory(list)


@attr.s(auto_attribs=True, frozen=True)
class ReadinessRestingHeartRate(TimeSeries):
    metric_id: str = "readiness_resting_heart_rate"
    display_name: str = "Resting Heart Rate"
    unit: str | None = None
    samples: list[Sample[float]] = attrs.Factory(list)


@attr.s(auto_attribs=True, frozen=True)
class ReadinessSleepBalance(TimeSeries):
    metric_id: str = "readiness_sleep_balance"
    display_name: str = "Sleep Balance"
    unit: str | None = None
    samples: list[Sample[float]] = attrs.Factory(list)


@attr.s(auto_attribs=True, frozen=True)
class ReadinessSleepRegularity(TimeSeries):
    metric_id: str = "readiness_sleep_regularity"
    display_name: str = "Sleep Regularity"
    unit: str | None = None
    samples: list[Sample[float]] = attrs.Factory(list)


# Body signals

@attr.s(auto_attribs=True, frozen=True)
class BodyTemperatureDeviation(TimeSeries):
    metric_id: str = "temperature_deviation"
    display_name: str = "Temperature Deviation"
    unit: str = "°C"
    samples: list[Sample[float]] = attrs.Factory(list)


@attr.s(auto_attribs=True, frozen=True)
class BodyTemperatureTrendDeviation(TimeSeries):
    metric_id: str = "temperature_trend_deviation"
    display_name: str = "Temperature Trend Deviation"
    unit: str = "°C"
    samples: list[Sample[float]] = attrs.Factory(list)


# Sleep score

@attr.s(auto_attribs=True, frozen=True)
class SleepScore(TimeSeries):
    metric_id: str = "sleep_score"
    display_name: str = "Sleep Score"
    unit: str | None = None
    samples: list[Sample[float]] = attrs.Factory(list)


@attr.s(auto_attribs=True, frozen=True)
class SleepScoreDeepSleep(TimeSeries):
    metric_id: str = "sleep_score_deep_sleep"
    display_name: str = "Deep Sleep Score"
    unit: str | None = None
    samples: list[Sample[float]] = attrs.Factory(list)


@attr.s(auto_attribs=True, frozen=True)
class SleepScoreEfficiency(TimeSeries):
    metric_id: str = "sleep_score_efficiency"
    display_name: str = "Efficiency Score"
    unit: str | None = None
    samples: list[Sample[float]] = attrs.Factory(list)


@attr.s(auto_attribs=True, frozen=True)
class SleepScoreLatency(TimeSeries):
    metric_id: str = "sleep_score_latency"
    display_name: str = "Latency Score"
    unit: str | None = None
    samples: list[Sample[float]] = attrs.Factory(list)


@attr.s(auto_attribs=True, frozen=True)
class SleepScoreREMSleep(TimeSeries):
    metric_id: str = "sleep_score_rem_sleep"
    display_name: str = "REM Sleep Score"
    unit: str | None = None
    samples: list[Sample[float]] = attrs.Factory(list)


@attr.s(auto_attribs=True, frozen=True)
class SleepScoreRestfulness(TimeSeries):
    metric_id: str = "sleep_score_restfulness"
    display_name: str = "Restfulness Score"
    unit: str | None = None
    samples: list[Sample[float]] = attrs.Factory(list)


@attr.s(auto_attribs=True, frozen=True)
class SleepScoreTiming(TimeSeries):
    metric_id: str = "sleep_score_timing"
    display_name: str = "Timing Score"
    unit: str | None = None
    samples: list[Sample[float]] = attrs.Factory(list)


@attr.s(auto_attribs=True, frozen=True)
class SleepScoreTotalSleep(TimeSeries):
    metric_id: str = "sleep_score_total_sleep"
    display_name: str = "Total Sleep Score"
    unit: str | None = None
    samples: list[Sample[float]] = attrs.Factory(list)


# ---------------------------------------------------------------------------
# Containers: Workouts
# ---------------------------------------------------------------------------

@attr.s(auto_attribs=True, frozen=True)
class Workout(Container):
    """A generic exercise session."""

    workout_type: str = WorkoutType.OTHER

    duration: Duration | None = None
    calories: Calories | None = None
    average_heart_rate: HeartRateAvg | None = None
    max_heart_rate: HeartRateAvg | None = None

    # HR during workout
    heart_rate: HeartRate | None = None

    source: str | None = None
    id: str | None = None


@attr.s(auto_attribs=True, frozen=True)
class RunningWorkout(Workout):
    """A running session with running-specific metrics."""

    workout_type: str = WorkoutType.RUNNING

    distance: Distance | None = None
    average_pace: Pace | None = None
    elevation_gain: Distance | None = None
