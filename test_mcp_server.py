import asyncio

from mcp.server.fastmcp import FastMCP

from ddg_extension.mcp_server import mcp


def test_mcp_entrypoint_is_fastmcp() -> None:
    assert isinstance(mcp, FastMCP)
    assert mcp.name == "ddg-mcp"


def test_expected_tools_are_registered() -> None:
    tools = asyncio.run(mcp.list_tools())
    tool_names = {tool.name for tool in tools}

    assert tool_names >= {
        "ddg-text-search",
        "ddg-image-search",
        "ddg-news-search",
        "ddg-video-search",
        "ddg-ai-chat",
    }


def test_summary_prompt_is_registered() -> None:
    prompts = asyncio.run(mcp.list_prompts())
    prompt_names = {prompt.name for prompt in prompts}

    assert "search-results-summary" in prompt_names

