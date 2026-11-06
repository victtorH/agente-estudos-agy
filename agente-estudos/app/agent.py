import asyncio
import datetime
import logging
import os
from collections.abc import AsyncGenerator
from pathlib import Path

from dotenv import load_dotenv
import google.auth
from google.adk.agents import Agent
from google.adk.apps import App
from google.adk.integrations.gcs import GCSToolset
from google.adk.integrations.gcs.gcs_credentials import GCSCredentialsConfig
from google.adk.integrations.gcs.settings import Capabilities, GCSToolSettings
from google.adk.models import Gemini, LlmRequest, LlmResponse
from google.adk.skills import load_skill_from_dir
from google.adk.tools.skill_toolset import SkillToolset
from google.genai import types

load_dotenv()

logger = logging.getLogger(__name__)

# Resolução de caminhos a partir da localização de agent.py
BASE_DIR = Path(__file__).resolve().parent
SKILLS_DIR = BASE_DIR / "skills" / "plano-de-estudos"

# Carregamento da skill
skill = load_skill_from_dir(SKILLS_DIR)
skill_toolset = SkillToolset(skills=[skill])

# Configuração do GCSToolset
GCS_BUCKET_NAME = os.getenv("GCS_BUCKET_NAME", "agente-estudos-planos")

try:
    credentials, _ = google.auth.default()
    credentials_config = GCSCredentialsConfig(credentials=credentials)
except Exception:
    credentials_config = None

gcs_toolset = GCSToolset(
    tool_filter=["create_object", "get_object_data"],
    credentials_config=credentials_config,
    gcs_tool_settings=GCSToolSettings(capabilities=[Capabilities.READ_WRITE]),
)

MODEL_NAME = os.getenv("MODEL", "gemini-3.8-flash")
FALLBACK_MODEL_NAME = os.getenv("FALLBACK_MODEL", "gemini-3.5-flash")
PRIMARY_TIMEOUT = float(os.getenv("PRIMARY_MODEL_TIMEOUT", "12.0"))


class FallbackGemini(Gemini):
    fallback_model: str = "gemini-3.5-flash"
    primary_timeout_seconds: float = 12.0
    _fallback_instance: Gemini | None = None

    def _get_fallback(self) -> Gemini:
        if self._fallback_instance is None:
            self._fallback_instance = Gemini(
                model=self.fallback_model,
                retry_options=types.HttpRetryOptions(attempts=2),
            )
        return self._fallback_instance

    async def generate_content_async(
        self, llm_request: LlmRequest, stream: bool = False
    ) -> AsyncGenerator[LlmResponse, None]:
        gen = super().generate_content_async(llm_request, stream=stream)
        try:
            first_chunk = await asyncio.wait_for(
                gen.__anext__(), timeout=self.primary_timeout_seconds
            )
            yield first_chunk
            async for chunk in gen:
                yield chunk
            return
        except StopAsyncIteration:
            return
        except Exception as exc:
            await gen.aclose()
            logger.warning(
                "Modelo primário '%s' falhou ou expirou (%s: %s). Ativando fallback para '%s'.",
                self.model,
                type(exc).__name__,
                exc,
                self.fallback_model,
            )
            fallback = self._get_fallback()
            llm_request.model = self.fallback_model
            async for chunk in fallback.generate_content_async(
                llm_request, stream=stream
            ):
                yield chunk


def instruction_provider(context=None) -> str:
    hoje = datetime.date.today().strftime("%d/%m/%Y")
    return (
        f"Hoje é {hoje}.\n"
        "Você é um mentor especialista em estudos. Seu objetivo é ajudar a pessoa a organizar "
        "seus estudos de forma personalizada, criando planos executáveis com base na skill plano-de-estudos.\n"
        "Siga a regra de gating da skill: se faltar objetivo, prazo, disponibilidade ou nível atual, "
        "pergunte apenas o que falta e não carregue recursos antecipadamente.\n"
        f"Quando tiver todas as informações, siga o workflow da skill e salve o CSV no bucket '{GCS_BUCKET_NAME}' "
        "com o nome 'plano-de-estudos.csv' usando a ferramenta create_object."
    )


root_agent = Agent(
    # Keep in sync with create_params.root_agent_name in agents-cli-manifest.yaml:
    name="agente_estudos",
    model=FallbackGemini(
        model=MODEL_NAME,
        fallback_model=FALLBACK_MODEL_NAME,
        primary_timeout_seconds=PRIMARY_TIMEOUT,
        retry_options=types.HttpRetryOptions(attempts=2),
    ),
    instruction=instruction_provider,
    tools=[skill_toolset, gcs_toolset],
)

app = App(
    root_agent=root_agent,
    name="app",
)
