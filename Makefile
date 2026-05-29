.PHONY: help sync test lint format typecheck check run mcp-run install inspector inspect clean

UV_CACHE_DIR ?= .uv-cache
UV := env UV_CACHE_DIR=$(UV_CACHE_DIR) uv
MCP_SERVER := src/ddg_extension/mcp_server.py:mcp

help:
	@printf "%s\n" "Available targets:"
	@printf "  %-10s %s\n" "sync" "Install and sync dependencies"
	@printf "  %-10s %s\n" "test" "Run pytest"
	@printf "  %-10s %s\n" "lint" "Run ruff checks"
	@printf "  %-10s %s\n" "format" "Format with ruff"
	@printf "  %-10s %s\n" "typecheck" "Run ty"
	@printf "  %-10s %s\n" "check" "Run lint, typecheck, and tests"
	@printf "  %-10s %s\n" "run" "Run the MCP server with mcp run"
	@printf "  %-10s %s\n" "mcp-run" "Alias for run"
	@printf "  %-10s %s\n" "install" "Install the MCP server in Claude Desktop"
	@printf "  %-10s %s\n" "inspector" "Test the MCP server with MCP Inspector"
	@printf "  %-10s %s\n" "clean" "Remove local caches and build artifacts"

sync:
	$(UV) sync

test:
	$(UV) run pytest

lint:
	$(UV) run ruff check .

format:
	$(UV) run ruff format .

typecheck:
	$(UV) run ty check

check: lint typecheck test

run:
	$(UV) run mcp run $(MCP_SERVER)

mcp-run: run

install:
	$(UV) run mcp install $(MCP_SERVER) --name ddg-mcp --with-editable .

inspector:
	$(UV) run mcp dev $(MCP_SERVER)

inspect: inspector

clean:
	rm -rf .pytest_cache .ruff_cache .ty .uv-cache build dist *.egg-info src/*.egg-info __pycache__ src/__pycache__ tests/__pycache__ src/ddg_extension/__pycache__
