# Expendator

A small command-line expense tracker written in Python (standard library only).
Amounts are always stored as integer cents.

## Setup

With [uv](https://docs.astral.sh/uv/):

```
uv sync
```

Or with plain pip:

```
pip install -r requirements-dev.txt
```

## Usage

```
python -m expendator add food 12,05 "Lunch" --date 2025-03-14
python -m expendator list
python -m expendator list --category food
python -m expendator total
python -m expendator summary
```

Use `--file PATH` (before the subcommand) to choose the JSON file.
The default is `expenses.json` in the current directory.

## Tests

```
uv run pytest -q
```

or, without uv:

```
pytest -q
```
