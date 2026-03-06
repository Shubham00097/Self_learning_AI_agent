# Phase 2: Ingestion & Architecture - Context

**Gathered:** 2026-03-06
**Status:** Ready for planning

## Phase Boundary
Enable the agent to safely ingest local/remote repositories and support extensible behaviors through a Plugin Task architecture.

## Implementation Decisions

### Repository Ingestion
- **DECIDED:** Clone to a MANAGED workspace at `~/.sg_agent/workspaces/<repo-name>`
- **DECIDED:** If repo already exists, do a `git pull` to update instead of re-cloning
- **DECIDED:** Keep a registry in SQLite of all managed repos (url, local path, last updated)
- **DECIDED:** Cleanup command: `agent remove <repo-name>` to delete workspace + registry entry
- **DECIDED:** No temporary dirs — we want repos to persist between daemon restarts

### Path Filtering
- **DECIDED:** Use a MIX of hardcoded defaults, global config, and local config
- **DECIDED:** Hardcoded defaults: `.git`, `__pycache__`, `node_modules`, `.env`, `*.pyc`
- **DECIDED:** Configurable via `~/.sg_agent/config.yaml` under `ignore_patterns:`
- **DECIDED:** Respect `.gitignore` if present in the repo
- **DECIDED:** Local config `.sg_agent.yaml` can override global ignore patterns per project

### Plugin Architecture
- **DECIDED:** Plugins live in a dedicated folder: `~/.sg_agent/plugins/`
- **DECIDED:** Each plugin is a single Python file with a standard interface (Must have: `PLUGIN_NAME`, `PLUGIN_VERSION`, `run(event, context)` function)
- **DECIDED:** Auto-discovered on daemon startup by scanning the plugins folder
- **DECIDED:** No manual registration needed — just drop a file in the folder
- **DECIDED:** Built-in plugins: file_sorter, code_cleanup (as examples)

### Shutdown & Error Handling
- **DECIDED:** Graceful shutdown timeout: 10 seconds to flush queues before force exit
- **DECIDED:** Clone failures: retry 3 times with 5 second delay, then surface clear error
- **DECIDED:** Permission errors: log clearly and skip that file/folder, never crash
- **DECIDED:** Show all errors in `agent status` output so user can see what was skipped

## Specific Ideas
- "No temporary dirs — we want repos to persist between daemon restarts"
- "No manual registration needed — just drop a file in the folder"

## Deferred Ideas
None

---
*Phase: 02-ingestion-architecture*
*Context gathered: 2026-03-06*
