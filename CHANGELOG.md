# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Initial public release preparation

## [0.1.0] - 2025-01-08

### Added
- Core `AttributionAgent` class for 4D attribution analysis
- `DomainTemplate` for customizing analysis to different domains
- Pre-built templates: `BANKING_TEMPLATE`, `HEALTHCARE_TEMPLATE`, `ECOMMERCE_TEMPLATE`
- `DataContext` schema for organizing metrics by 4 dimensions
- CLI interface with `four-d-are` command
  - `four-d-are demo` - Run demo analysis
  - `four-d-are analyze` - Analyze with custom data
  - `four-d-are init` - Initialize new project
- MCP server framework for data source integration
  - `demo_server` - Static data for demos
  - `mysql_server` - MySQL database connector
  - `postgres_server` - PostgreSQL database connector
  - `excel_server` - Excel/CSV file connector
- Documentation
  - Getting started guide
  - Core concepts explanation
  - Domain customization guide
  - MCP integration guide
- Example scripts
  - `quickstart.py` - Basic usage example
  - `custom_domain.py` - Domain customization examples

### Technical Details
- Python 3.10+ support
- Pydantic v2 for data validation
- Typer for CLI
- OpenAI API integration (compatible with any OpenAI-compatible API)

## Research Background

This project implements the 4D-ARE framework from the research paper:

**4D-ARE: Bridging the Attribution Gap in LLM Agent Requirements Engineering**

The framework addresses the "Attribution Gap" - the tendency of LLM agents to report *what* happened without explaining *why*.

[0.1.0]: https://github.com/anthropics/4D-ARE/releases/tag/v0.1.0
[Unreleased]: https://github.com/anthropics/4D-ARE/compare/v0.1.0...HEAD
