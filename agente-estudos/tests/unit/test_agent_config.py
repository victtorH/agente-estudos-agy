import datetime
import os
import pytest
from app.agent import root_agent, app, instruction_provider, FerramentasDeArquivo
from google.adk.tools.skill_toolset import SkillToolset

def test_agent_and_app_initialization():
    assert root_agent.name == "agente_estudos"
    assert app.name == "app"
    assert app.root_agent == root_agent

def test_instruction_provider_has_current_date():
    today_str = datetime.date.today().strftime("%d/%m/%Y")
    instruction = instruction_provider()
    assert today_str in instruction
    assert "plano-de-estudos" in instruction

@pytest.mark.asyncio
async def test_ferramentas_de_arquivo():
    file_toolset = next(t for t in root_agent.tools if isinstance(t, FerramentasDeArquivo))
    tools = await file_toolset.get_tools()
    tool_names = [t.name for t in tools]
    assert sorted(tool_names) == ["ReadFile", "WriteFile"]

def test_skill_toolset_present():
    skill_toolset = next(t for t in root_agent.tools if isinstance(t, SkillToolset))
    assert skill_toolset is not None
