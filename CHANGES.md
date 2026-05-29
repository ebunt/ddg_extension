# Changes

Implemented on 2026-05-29.

## Project Structure

- Replaced the ambiguous `src` package with `ddg_extension`.
- Moved MCP registration to `src/ddg_extension/mcp_server.py`.
- Added a DuckDuckGo service layer in `src/ddg_extension/search.py`.
- Added the `ddg-mcp-server` console entry point.

## API Contract

- Kept the multi-tool MCP API:
  - `ddg-text-search`
  - `ddg-image-search`
  - `ddg-news-search`
  - `ddg-video-search`
  - `ddg-ai-chat`
- Kept the `search-results-summary` prompt.
- Search tools now return structured dictionaries instead of formatted strings.
- Search tools validate `max_results` with the range `1` to `25`.
- DuckDuckGo failures are converted into structured error responses.
- DuckDuckGo search calls pass the query positionally to match the installed `ddgs` API.
- `ddg-ai-chat` returns a structured unsupported error when the installed `ddgs` client does not expose chat.

## Tests

- Replaced stale tests that referenced missing modules and the old `web_search` tool.
- Added pytest coverage for:
  - MCP server name
  - registered tool names
  - registered prompt name
  - DuckDuckGo method arguments
  - structured result shapes
  - `max_results` validation
  - error conversion
- Tests mock the DuckDuckGo client and do not make live network calls.

## Tooling And Docs

- Updated `pyproject.toml` description.
- Added `ruff` and `ty` to the test dependency group.
- Updated `uv.lock`.
- Rewrote README to document Python 3.14+, the console entry point, Goose configuration, tools, prompt, and development commands.

## Verification

- `uv run pytest`: passed.
- `uv run ruff check .`: passed.
- `uv run ty check`: passed.
