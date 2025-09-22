# Diary App (main branch)

**Banner:** MAIN – Production

## Start (lokal)
```bash
pip install -r requirements.txt
export PASSWORD=deinSicheresPasswort
export SECRET_KEY=einGeheimerSchlüssel
python app.py
```

## Unterschiede dieser Variante
- DEBUG: False
- "/add_entry" ohne Login erlaubt: False


## Pre-commit Hooks
Installation:
```bash
python -m pip install pre-commit black flake8 flake8-bugbear pytest
pre-commit install
pre-commit install --hook-type pre-push
pre-commit run --all-files
