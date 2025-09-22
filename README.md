# Diary App (LB 324)

Dies ist die Tagebuch-Applikation für die Leistungsbeurteilung **Modul 324 – DevOps**.  
Die App basiert auf **Flask (Python 3.11)** und ist mit einer vollständigen **CI/CD-Pipeline** (GitHub Actions + Azure App Service) ausgestattet.

---

##  Projektstruktur

- **main** → Production-Branch, enthält nur Code, der automatisch nach Azure deployed wird.  
- **dev** → Staging-Branch, Integration neuer Features nach Code-Review & Tests.  
- **feature/*** → Feature-Branches, auf denen neue Funktionalität entwickelt wird.  

---

## Lokale Installation & Start

1. Repository klonen:
   ```bash
   git clone https://github.com/<USER>/<REPO>.git
   cd <REPO>
Abhängigkeiten installieren:
```
bash
Copy code
pip install -r requirements.txt

```
.env-Datei im Projektordner erstellen:

```
env
Copy code
PASSWORD="deinPasswort"
SECRET_KEY="einGeheimerSchluessel"
```
App starten:
```
bash
Copy code
flask run
```
Die App ist erreichbar unter http://127.0.0.1:5000

 
 Pre-commit Hooks
Damit nur getesteter & formatierter Code eingecheckt wird, nutzen wir pre-commit.

Installation
```
bash
Copy code
pip install pre-commit
pre-commit install
pre-commit install --hook-type pre-push
pre-commit run --all-files
```
Verwendete Hooks
Black → automatisches Code-Formatieren bei jedem Commit

Flake8 → Linter, prüft Codequalität bei jedem Commit

Pytest → Tests werden bei jedem Push ausgeführt

 Continuous Integration (CI)
Im Ordner .github/workflows liegt die Datei ci.yml:

Löst aus bei jedem Commit & Pull Request

Installiert Dependencies

Führt pytest aus

Prüft auf Fehler (bricht bei Fail ab)

 Continuous Deployment (CD)
Es gibt zwei CD-Workflows:

cd-dev.yml
Läuft bei Pushes auf dev.
→ App wird automatisch in Staging (Azure Web App) deployed.

cd-main.yml
Läuft bei Pushes auf main.
→ App wird automatisch in Production (Azure Web App) deployed.

Azure Deployment
App-URL (Production)
lglb324-gubrghash6c7fqeb.germanywestcentral-01.azurewebsites.net

Secrets in GitHub
Die folgenden Secrets müssen gesetzt sein (Repo → Settings → Secrets → Actions):

AZURE_WEBAPP_NAME = Name der Web App (Prod)

AZURE_PUBLISH_PROFILE = Inhalt des Publish Profiles (XML aus Azure)

Optional für Staging:

AZURE_WEBAPP_NAME_STAGING

AZURE_PUBLISH_PROFILE_STAGING

App Settings in Azure
In der Web App → Configuration → Application settings:

PASSWORD → deinSicheresPasswort

SECRET_KEY → zufälliger String

Nach dem Speichern App neu starten.

Tests
Beispiel-Test (test_app.py):
```
python
Copy code
from app import app, entries
import pytest

@pytest.fixture()
def client():
    app.config['TESTING'] = True
    return app.test_client()

def test_add_entry_with_happiness(client):
    response = client.post(
        '/add_entry', data={'content': 'Test Entry Content', 'happiness': '😃'}
    )
    assert response.status_code == 302
    assert response.headers['Location'] == '/'

    entry = entries[0]
    assert entry.content == 'Test Entry Content'
    assert entry.happiness == '😃'
```
Tests laufen lokal mit:
```
bash
Copy code
pytest
Vorgehen (GitHub Flow)
Issue erstellen

Feature-Branch (feature/xyz) erstellen

Code + Test schreiben

Commit & Push (pre-commit sorgt für Formatierung & Tests)

Pull Request → Merge in dev (Staging-Deployment läuft)

Merge in main (Production-Deployment läuft)

Unterschiede der Branches
main (Production)

DEBUG=False

/add_entry nur mit Login erlaubt

dev (Staging)

DEBUG=True

Banner: DEV – Staging

/add_entry ohne Login erlaubt (für Testbarkeit)

feature/*
```
Entwicklungsumgebung für neue Funktionen

yaml
Copy code

---
```
## 2. `.pre-commit-config.yaml`

yaml
repos:
  - repo: https://github.com/psf/black
    rev: 24.8.0
    hooks:
      - id: black
        language_version: python3

  - repo: https://github.com/pycqa/flake8
    rev: 7.1.1
    hooks:
      - id: flake8
        additional_dependencies: [flake8-bugbear]

  - repo: local
    hooks:
      - id: pytest-on-push
        name: pytest on push
        entry: bash -c "pytest -q || exit 1"
        language: system
        pass_filenames: false
        stages: [push]
```
3. Issue-Template .github/ISSUE_TEMPLATE/anforderung.md

markdown
Copy code
---
name: Anforderung
about: Neue Funktionalität/Änderung als Anforderung erfassen
title: "[Anforderung] <kurzer Titel>"
labels: ''
assignees: ''

## Zielsystem
z. B. Tagebuch-Frontend, API, Deployment-Pipeline 

## Priorität
 muss | soll | wird 

## Systemaktivität
System soll selbständig handeln | dem Administrator die Möglichkeit bieten | fähig sein (Schnittstelle) 

## Ergänzungen
z. B. 'über das Netzwerk', 'CSV-Export' ... 

## Funktionalität
 Was genau soll passieren? 

## Bedingungen
 wenn ... | falls ... 

## Typ (Label ankreuzen)
- [ ] Funktionale Anforderung
- [ ] Qualitätsanforderung
- [ ] Randanforderung
