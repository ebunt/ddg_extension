# DuckDuckGo MCP Extension for Goose

DuckDuckGo search tools exposed as a Model Context Protocol server for Goose.

## Requirements

- Python 3.14+
- uv

## Setup

```bash
make sync
```

## Run

```bash
make run
```

The server communicates over stdio and waits for MCP JSON-RPC input.

## MCP Inspector

Use the MCP Inspector for local manual testing:

```bash
make inspector
```

## Install In Claude Desktop

Install the server into Claude Desktop with the MCP CLI:

```bash
make install
```

## Goose Configuration

Replace `/path/to/ddg_extension` with the absolute path to this project.

```json
{
  "mcpServers": {
    "ddg_search": {
      "command": "uv",
      "args": [
        "--directory",
        "/path/to/ddg_extension",
        "run",
        "ddg-mcp-server"
      ]
    }
  }
}
```

## Tools

All search tools return structured dictionaries with `ok`, `kind`, `keywords`, and either `results` or `error`. `max_results` must be between `1` and `25`.

### `ddg-text-search`

Search web pages.

Arguments:
- `keywords`: search query
- `region`: default `wt-wt`
- `safesearch`: `on`, `moderate`, or `off`
- `timelimit`: `d`, `w`, `m`, or `y`
- `max_results`: default `10`

### `ddg-image-search`

Search images.

Arguments:
- `keywords`: search query
- `region`: default `wt-wt`
- `safesearch`: `on`, `moderate`, or `off`
- `timelimit`: `d`, `w`, `m`, or `y`
- `size`: `Small`, `Medium`, `Large`, or `Wallpaper`
- `color`: image color filter
- `type_image`: `photo`, `clipart`, `gif`, `transparent`, or `line`
- `layout`: `Square`, `Tall`, or `Wide`
- `license_image`: license filter
- `max_results`: default `10`

### `ddg-news-search`

Search news articles.

Arguments:
- `keywords`: search query
- `region`: default `wt-wt`
- `safesearch`: `on`, `moderate`, or `off`
- `timelimit`: `d`, `w`, `m`, or `y`
- `max_results`: default `10`

### `ddg-video-search`

Search videos.

Arguments:
- `keywords`: search query
- `region`: default `wt-wt`
- `safesearch`: `on`, `moderate`, or `off`
- `timelimit`: `d`, `w`, `m`, or `y`
- `resolution`: `high` or `standard`
- `duration`: `short`, `medium`, or `long`
- `license_videos`: `creativeCommon` or `youtube`
- `max_results`: default `10`

### `ddg-ai-chat`

Send a prompt to DuckDuckGo AI chat when the installed `ddgs` client supports chat.

Arguments:
- `keywords`: prompt
- `model`: default `gpt-4o-mini`

## Prompts

### `search-results-summary`

Fetches text search results and returns a prompt asking an LLM to summarize them.

Arguments:
- `query`: search query
- `style`: `brief` or `detailed`

## Development

```bash
make sync
make test
make lint
make typecheck
make build
make check
```

Useful targets:
- `make format`: format Python files with Ruff
- `make version-from-tag`: set `pyproject.toml` version from the latest `v*` tag
- `make check-version`: verify `pyproject.toml` version matches the latest `v*` tag
- `make install-hooks`: install a local pre-commit hook that runs `make check-version`
- `make clean`: remove local caches and build artifacts
- `make help`: list available targets

## GitHub Actions

- `Checks` runs on pull requests, pushes to `main`, and manual dispatch.
- `Checks` runs linting, type checking, tests, and package build.
- `Release` runs on tags matching `v*` and attaches the built wheel and source distribution to a GitHub Release.

## Release

Update `version` in `pyproject.toml`, commit the change, then create and push a tag:

```bash
git tag v0.1.0
git push origin v0.1.0
```

The `Release` workflow creates the GitHub Release and uploads files from `dist/`.

To sync `pyproject.toml` from the latest existing tag:

```bash
make version-from-tag
```

To install a local hook that blocks commits when `pyproject.toml` is out of sync with the latest `v*` tag:

```bash
make install-hooks
```
