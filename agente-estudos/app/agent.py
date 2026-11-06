import datetime
import os
from pathlib import Path

from google.adk.agents import Agent
from google.adk.apps import App
from google.adk.environment import LocalEnvironment
from google.adk.models import Gemini
from google.adk.skills import load_skill_from_dir
from google.adk.tools.environment import EnvironmentToolset
from google.adk.tools.skill_toolset import SkillToolset
from google.genai import types


class FerramentasDeArquivo(EnvironmentToolset):
    """Toolset de ambiente restrito apenas a leitura e escrita de arquivos."""

    async def get_tools(self, readonly_context=None):
        tools = await super().get_tools(readonly_context)
        return [t for t in tools if t.name in ("ReadFile", "WriteFile")]


# Resolução de caminhos a partir da localização de agent.py
BASE_DIR = Path(__file__).resolve().parent
SKILLS_DIR = BASE_DIR / "skills" / "plano-de-estudos"
PLANOS_DIR = BASE_DIR.parent / "planos"
PLANOS_DIR.mkdir(parents=True, exist_ok=True)

# Carregamento da skill e das ferramentas de arquivo
skill = load_skill_from_dir(SKILLS_DIR)
skill_toolset = SkillToolset(skills=[skill])
file_toolset = FerramentasDeArquivo(
    environment=LocalEnvironment(working_dir=str(PLANOS_DIR))
)

MODEL_NAME = os.getenv("MODEL", "gemini-3.8-flash")


def instruction_provider(context=None) -> str:
    hoje = datetime.date.today().strftime("%d/%m/%Y")
    return (
        f"Hoje é {hoje}.\n"
        "Você é um mentor especialista em estudos. Seu objetivo é ajudar a pessoa a organizar "
        "seus estudos de forma personalizada, criando planos executáveis com base na skill plano-de-estudos.\n"
        "Siga a regra de gating da skill: se faltar objetivo, prazo, disponibilidade ou nível atual, "
        "pergunte apenas o que falta e não carregue recursos antecipadamente.\n"
        "Quando tiver todas as informações, siga o workflow da skill e salve o CSV em plano-de-estudos.csv "
        "com a ferramenta WriteFile."
    )


root_agent = Agent(
    # Keep in sync with create_params.root_agent_name in agents-cli-manifest.yaml:
    name="agente_estudos",
    model=Gemini(
        model=MODEL_NAME,
        retry_options=types.HttpRetryOptions(attempts=3),
    ),
    instruction=instruction_provider,
    tools=[skill_toolset, file_toolset],
)

app = App(
    root_agent=root_agent,
    name="app",
)
