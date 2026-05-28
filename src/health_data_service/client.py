"""Consumer client for the OpenHost health-data service.

Usage::

    from health_data_service import HealthDataClient, TimeSeriesRequest

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
from types import TracebackType

import cattrs
from cattrs.preconf.json import make_converter
import httpx

from .data_types import (
    MetricType,
    TimeSeries,
)
from .specific_types import (
    SleepSession,
    Workout,
)
from .request_types import (
    SleepSessionsRequest,
    TimeSeriesRequest,
    WorkoutsRequest,
)

converter = make_converter()


def _to_params(req: object) -> dict[str, str]:
    """Unstructure an attrs request to query params, dropping None values."""
    raw = cattrs.unstructure(req)
    return {k: str(v) for k, v in raw.items() if v is not None}


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
        return converter.structure(resp.json()["metrics"], list[MetricType])

    async def get_time_series(self, req: TimeSeriesRequest) -> TimeSeries:
        resp = await self._http.get("/v1/time-series", params=_to_params(req))
        resp.raise_for_status()
        return converter.structure(resp.json(), TimeSeries)

    async def get_sleep_sessions(self, req: SleepSessionsRequest) -> list[SleepSession]:
        resp = await self._http.get("/v1/sleep-sessions", params=_to_params(req))
        resp.raise_for_status()
        return converter.structure(resp.json()["data"], list[SleepSession])

    async def get_workouts(self, req: WorkoutsRequest) -> list[Workout]:
        resp = await self._http.get("/v1/workouts", params=_to_params(req))
        resp.raise_for_status()
        return converter.structure(resp.json()["data"], list[Workout])
