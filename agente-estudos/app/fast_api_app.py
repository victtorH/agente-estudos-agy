# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import contextlib
import os
import time
from collections import defaultdict
from collections.abc import AsyncIterator

from a2a.server.tasks import InMemoryTaskStore
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Request
from google.adk.cli.fast_api import get_fast_api_app
from google.adk.runners import Runner

from app.app_utils import services
from app.app_utils.a2a import attach_a2a_routes

load_dotenv()
allow_origins = (
    os.getenv("ALLOW_ORIGINS", "").split(",") if os.getenv("ALLOW_ORIGINS") else None
)
otel_to_cloud = True

AGENT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


@contextlib.asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    from app.agent import app as adk_app
    from app.agent import root_agent

    runner = Runner(
        app=adk_app,
        session_service=services.get_session_service(),
        artifact_service=services.get_artifact_service(),
        auto_create_session=True,
    )
    app.state.runner = runner
    app.state.agent_app_name = adk_app.name
    await attach_a2a_routes(
        app,
        agent=root_agent,
        runner=runner,
        task_store=InMemoryTaskStore(),
        rpc_path=f"/a2a/{adk_app.name}",
    )
    yield


app: FastAPI = get_fast_api_app(
    agents_dir=AGENT_DIR,
    web=True,
    artifact_service_uri=services.ARTIFACT_SERVICE_URI,
    allow_origins=allow_origins,
    session_service_uri=services.SESSION_SERVICE_URI,
    otel_to_cloud=otel_to_cloud,
    lifespan=lifespan,
)
app.title = "agente-estudos"
app.description = "API for interacting with the Agent agente-estudos"

REQUEST_COUNTS = defaultdict(list)
MAX_REQUESTS_PER_MINUTE = 30


@app.middleware("http")
async def anti_abuse_middleware(request: Request, call_next):
    path = request.url.path
    if (
        path in ["/healthz", "/docs", "/openapi.json", "/favicon.ico"]
        or path.startswith("/static")
        or path.endswith((".js", ".css", ".png", ".svg", ".ico"))
    ):
        return await call_next(request)

    client_ip = request.client.host if request.client else "unknown"
    now = time.time()
    REQUEST_COUNTS[client_ip] = [t for t in REQUEST_COUNTS[client_ip] if now - t < 60]

    if len(REQUEST_COUNTS[client_ip]) >= MAX_REQUESTS_PER_MINUTE:
        raise HTTPException(
            status_code=429,
            detail="Muitas requisições. Para manter este serviço gratuito e acessível a todos, aguarde 1 minuto.",
        )

    REQUEST_COUNTS[client_ip].append(now)
    return await call_next(request)


@app.get("/healthz")
async def healthz():
    return {"status": "ok"}


# Main execution
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
