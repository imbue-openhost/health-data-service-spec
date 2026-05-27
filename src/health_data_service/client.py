"""Consumer client for the OpenHost health-data service.

Usage::

    from health_data_service import HealthDataClient

    async with HealthDataClient() as client:
        hr = await client.get_time_series("heart_rate", start="2026-05-20T00:00:00+00:00")
        sessions = await client.get_sleep_sessions(start="2026-05-24T00:00:00+00:00")
        runs = await client.get_workouts(workout_type="running", limit=10)

By default reads ``OPENHOST_ROUTER_URL`` and ``OPENHOST_APP_TOKEN`` from the
environment (set automatically inside OpenHost containers). The service
shortname defaults to ``"health"`` — override if your manifest uses a
different ``[[services.v2.consumes]].shortname``.
"""

from __future__ import annotations

import os
from types import TracebackType

import attrs
import httpx

from .types import (
    MetricType,
    Sample,
    SleepSession,
    SleepStageInterval,
    TimeSeries,
    Workout,
)


def _struct(cls, d: dict):
    """Recursively build an attrs instance from a dict."""
    fields = {a.name: a for a in attrs.fields(cls)}
    kw = {}
    for k, v in d.items():
        if k not in fields:
            continue
        kw[k] = v
    return cls(**kw)


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
        return [_struct(MetricType, m) for m in resp.json()["metrics"]]

    async def get_time_series(
        self,
        metric: str,
        *,
        start: str | None = None,
        end: str | None = None,
        limit: int | None = None,
    ) -> TimeSeries:
        params: dict = {"metric": metric}
        if start:
            params["start"] = start
        if end:
            params["end"] = end
        if limit is not None:
            params["limit"] = limit
        resp = await self._http.get("/v1/time-series", params=params)
        resp.raise_for_status()
        body = resp.json()
        return TimeSeries(
            metric=body["metric"],
            unit=body["unit"],
            samples=[_struct(Sample, s) for s in body.get("samples", [])],
            source=body.get("source"),
        )

    async def get_sleep_sessions(
        self,
        *,
        start: str | None = None,
        end: str | None = None,
        limit: int | None = None,
    ) -> list[SleepSession]:
        params: dict = {}
        if start:
            params["start"] = start
        if end:
            params["end"] = end
        if limit is not None:
            params["limit"] = limit
        resp = await self._http.get("/v1/sleep-sessions", params=params)
        resp.raise_for_status()
        results = []
        for d in resp.json()["data"]:
            stages = [_struct(SleepStageInterval, s) for s in d.get("stages", [])]
            results.append(SleepSession(
                start=d["start"], end=d["end"], stages=stages,
                metrics=d.get("metrics", {}), source=d.get("source"), id=d.get("id"),
            ))
        return results

    async def get_workouts(
        self,
        *,
        workout_type: str | None = None,
        start: str | None = None,
        end: str | None = None,
        limit: int | None = None,
    ) -> list[Workout]:
        params: dict = {}
        if workout_type:
            params["type"] = workout_type
        if start:
            params["start"] = start
        if end:
            params["end"] = end
        if limit is not None:
            params["limit"] = limit
        resp = await self._http.get("/v1/workouts", params=params)
        resp.raise_for_status()
        return [_struct(Workout, w) for w in resp.json()["data"]]
