import asyncio
import datetime
import os
from unittest.mock import AsyncMock, patch, MagicMock
import pytest
from app.agent import root_agent, app, instruction_provider, GCS_BUCKET_NAME, FallbackGemini
from google.adk.integrations.gcs import GCSToolset
from google.adk.tools.skill_toolset import SkillToolset
from google.adk.models import Gemini, LlmRequest, LlmResponse
from google.genai import types

def test_agent_and_app_initialization():
    assert root_agent.name == "agente_estudos"
    assert app.name == "app"
    assert app.root_agent == root_agent
    assert isinstance(root_agent.model, FallbackGemini)

def test_instruction_provider_has_current_date():
    today_str = datetime.date.today().strftime("%d/%m/%Y")
    instruction = instruction_provider()
    assert today_str in instruction
    assert "plano-de-estudos" in instruction
    assert GCS_BUCKET_NAME in instruction
    assert "create_object" in instruction

@pytest.mark.asyncio
async def test_gcs_toolset():
    gcs_toolset = next(t for t in root_agent.tools if isinstance(t, GCSToolset))
    tools = await gcs_toolset.get_tools()
    tool_names = [t.name for t in tools]
    assert sorted(tool_names) == ["create_object", "get_object_data"]

def test_skill_toolset_present():
    skill_toolset = next(t for t in root_agent.tools if isinstance(t, SkillToolset))
    assert skill_toolset is not None

@pytest.mark.asyncio
async def test_fallback_gemini_on_error():
    fallback_model = FallbackGemini(
        model="gemini-primary-test",
        fallback_model="gemini-fallback-test",
        primary_timeout_seconds=2.0,
    )
    
    mock_fallback_instance = MagicMock()
    dummy_response = MagicMock(spec=LlmResponse)
    async def mock_fallback_gen(req, stream=False):
        yield dummy_response
    mock_fallback_instance.generate_content_async.side_effect = mock_fallback_gen
    fallback_model._fallback_instance = mock_fallback_instance

    async def failing_primary(req, stream=False):
        raise RuntimeError("Primary 503 error simulated")
        yield  # make it a generator

    with patch.object(Gemini, "generate_content_async", side_effect=failing_primary):
        req = LlmRequest(model="gemini-primary-test", contents=[])
        results = [r async for r in fallback_model.generate_content_async(req)]
        assert len(results) == 1
        assert results[0] == dummy_response
        assert req.model == "gemini-fallback-test"

@pytest.mark.asyncio
async def test_fallback_gemini_on_timeout():
    fallback_model = FallbackGemini(
        model="gemini-primary-test",
        fallback_model="gemini-fallback-test",
        primary_timeout_seconds=0.1,
    )
    
    mock_fallback_instance = MagicMock()
    dummy_response = MagicMock(spec=LlmResponse)
    async def mock_fallback_gen(req, stream=False):
        yield dummy_response
    mock_fallback_instance.generate_content_async.side_effect = mock_fallback_gen
    fallback_model._fallback_instance = mock_fallback_instance

    async def hanging_primary(req, stream=False):
        await asyncio.sleep(1.0)
        yield MagicMock()

    with patch.object(Gemini, "generate_content_async", side_effect=hanging_primary):
        req = LlmRequest(model="gemini-primary-test", contents=[])
        results = [r async for r in fallback_model.generate_content_async(req)]
        assert len(results) == 1
        assert results[0] == dummy_response
        assert req.model == "gemini-fallback-test"

