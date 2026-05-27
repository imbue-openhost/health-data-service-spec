"""Consumer client for the OpenHost health-data service.

Usage::

    from health_data_service import HealthDataClient
    from health_data_service.request_types import TimeSeriesRequest

    async with HealthDataClient() as client:
        hr = await client.get_time_series(TimeSeriesRequest(metric="heart_rate", start=...))
        sessions = await client.get_sleep_sessions(SleepSessionsRequest(start=...))
        runs = await client.get_workouts(WorkoutsRequest(workout_type="running", limit=10))

By default reads ``OPENHOST_ROUTER_URL`` and ``OPENHOST_APP_TOKEN`` from the
environment (set automatically inside OpenHost containers). The service
shortname defaults to ``"health"`` — override if your manifest uses a
different ``[[services.v2.consumes]].shortname``.
"""

from __future__ import annotations

import os
from datetime import datetime
from types import TracebackType

import httpx

from .data_types import (
    MetricType,
    Sample,
    SleepSession,
    SleepStageInterval,
    TimeSeries,
    Workout,
)
from .request_types import (
    SleepSessionsRequest,
    TimeSeriesRequest,
    WorkoutsRequest,
)


def _ts(s: str) -> datetime:
    return datetime.fromisoformat(s)


def _ts_opt(s: str | None) -> datetime | None:
    return datetime.fromisoformat(s) if s else None


class HealthDataClient:
    """Async client for the health-data service."""

    def __init__(
        self,
        *,
        router_url: str | None = None,
        app_token: str | None = None,
        shortname: str = "health",
    ) -> None:
        self._router_url = (
            router_url or os.environ["OPENHOST_ROUTER_URL"]
        ).rstrip("/")
        self._app_token = app_token or os.environ["OPENHOST_APP_TOKEN"]
        self._shortname = shortname
        self._client: httpx.AsyncClient | None = None

    async def __aenter__(self) -> HealthDataClient:
        self._client = httpx.AsyncClient(
            base_url=f"{self._router_url}/api/services/v2/call/{self._shortname}",
            headers={"Authorization": f"Bearer {self._app_token}"},
            timeout=30,
        )
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        if self._client:
            await self._client.aclose()
            self._client = None

    @property
    def _http(self) -> httpx.AsyncClient:
        if self._client is None:
            raise RuntimeError("Use 'async with HealthDataClient() as client:'")
        return self._client

    async def list_metrics(self) -> list[MetricType]:
        resp = await self._http.get("/v1/metrics")
        resp.raise_for_status()
        return [MetricType(**m) for m in resp.json()["metrics"]]

    async def get_time_series(self, req: TimeSeriesRequest) -> TimeSeries:
        resp = await self._http.get("/v1/time-series", params=req.to_params())
        resp.raise_for_status()
        body = resp.json()
        return TimeSeries(
            metric=body["metric"],
            unit=body["unit"],
            samples=[
                Sample(
                    timestamp=_ts(s["timestamp"]),
                    value=s["value"],
                    end_timestamp=_ts_opt(s.get("end_timestamp")),
                )
                for s in body.get("samples", [])
            ],
            source=body.get("source"),
        )

    async def get_sleep_sessions(self, req: SleepSessionsRequest) -> list[SleepSession]:
        resp = await self._http.get("/v1/sleep-sessions", params=req.to_params())
        resp.raise_for_status()
        results = []
        for d in resp.json()["data"]:
            stages = [
                SleepStageInterval(
                    stage=s["stage"], start=_ts(s["start"]), end=_ts(s["end"]),
                )
                for s in d.get("stages", [])
            ]
            results.append(SleepSession(
                start=_ts(d["start"]), end=_ts(d["end"]), stages=stages,
                metrics=d.get("metrics", {}), source=d.get("source"), id=d.get("id"),
            ))
        return results

    async def get_workouts(self, req: WorkoutsRequest) -> list[Workout]:
        resp = await self._http.get("/v1/workouts", params=req.to_params())
        resp.raise_for_status()
        return [
            Workout(
                workout_type=w["workout_type"],
                start=_ts(w["start"]), end=_ts(w["end"]),
                metrics=w.get("metrics", {}), source=w.get("source"), id=w.get("id"),
            )
            for w in resp.json()["data"]
        ]
