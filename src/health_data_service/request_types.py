"""Request types for the health-data service API."""

from __future__ import annotations

from datetime import datetime

import attr


def _ts_or_none(v: datetime | None) -> str | None:
    return v.isoformat() if v else None


@attr.s(auto_attribs=True, frozen=True)
class TimeSeriesRequest:
    metric: str
    start: datetime | None = None
    end: datetime | None = None
    limit: int | None = None

    def to_params(self) -> dict[str, str]:
        p: dict[str, str] = {"metric": self.metric}
        if self.start:
            p["start"] = self.start.isoformat()
        if self.end:
            p["end"] = self.end.isoformat()
        if self.limit is not None:
            p["limit"] = str(self.limit)
        return p


@attr.s(auto_attribs=True, frozen=True)
class SleepSessionsRequest:
    start: datetime | None = None
    end: datetime | None = None
    limit: int | None = None

    def to_params(self) -> dict[str, str]:
        p: dict[str, str] = {}
        if self.start:
            p["start"] = self.start.isoformat()
        if self.end:
            p["end"] = self.end.isoformat()
        if self.limit is not None:
            p["limit"] = str(self.limit)
        return p


@attr.s(auto_attribs=True, frozen=True)
class WorkoutsRequest:
    workout_type: str | None = None
    start: datetime | None = None
    end: datetime | None = None
    limit: int | None = None

    def to_params(self) -> dict[str, str]:
        p: dict[str, str] = {}
        if self.workout_type:
            p["type"] = self.workout_type
        if self.start:
            p["start"] = self.start.isoformat()
        if self.end:
            p["end"] = self.end.isoformat()
        if self.limit is not None:
            p["limit"] = str(self.limit)
        return p
