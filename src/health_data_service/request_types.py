"""Request types for the health-data service API."""

from __future__ import annotations

from datetime import datetime

import attr


@attr.s(auto_attribs=True, frozen=True)
class TimeSeriesRequest:
    metric: str
    start: datetime | None = None
    end: datetime | None = None
    limit: int | None = None


@attr.s(auto_attribs=True, frozen=True)
class SleepSessionsRequest:
    start: datetime | None = None
    end: datetime | None = None
    limit: int | None = None


@attr.s(auto_attribs=True, frozen=True)
class WorkoutsRequest:
    workout_type: str | None = None
    start: datetime | None = None
    end: datetime | None = None
    limit: int | None = None
