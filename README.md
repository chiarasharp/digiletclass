# DigiLetClass

Sito web del progetto DigiLetClass — Flask app che presenta il progetto,
le entità (persone, luoghi, organizzazioni) e le news.

Progetto finanziato da PNRR-CHANGES (Spoke 3: Cultural Heritage), Università di Bologna.

Sito: [digiletclass.unibo.it](https://digiletclass.unibo.it)
Edizione digitale: [esdcarteggiocannetifiacchi.unibo.it](https://esdcarteggiocannetifiacchi.unibo.it)

---

## Sviluppo locale

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

export FLASK_APP=app/webapp.py
flask run
```

Test:
```bash
export PYTHONPATH=.
pytest -q
```

---

## Struttura

```
app/
  blueprints/      # route Flask
  config/          # configurazione e type maps
  data/            # dati XML/JSON serviti dall'app
  static/          # CSS, JS, immagini
  templates/       # template Jinja2
  utils.py
  webapp.py        # entry point
passenger_wsgi.py  # entry point cPanel/Passenger
build.sh           # build script per Render
docs/
  DEPLOYMENT_CPANEL.md   # guida deploy cPanel
```

### Dati (`app/data/`)

| File | Contenuto |
|---|---|
| `cited-people.xml` | Persone citate nel carteggio |
| `orgs.xml` | Organizzazioni |
| `places.xml` | Luoghi |
| `news.json` | News ed eventi del progetto |

Questi file sono aggiornati manualmente quando cambiano le entità o le news.

### Route principali

| Route | Descrizione |
|---|---|
| `/` | Home |
| `/project` | Presentazione progetto |
| `/methodology` | Metodologia |
| `/entities` | Landing entità |
| `/entities/<orgs\|people\|places>` | Entità per tipo |
| `/news` | Lista news ed eventi |
| `/news/<news_id>` | Dettaglio news |

---

## Deploy

Il sito gira su cPanel (Passenger/WSGI) su server Unibo.

Per la guida completa al deploy: [docs/DEPLOYMENT_CPANEL.md](docs/DEPLOYMENT_CPANEL.md)

Aggiornamento rapido dopo modifiche:
1. Carica i file modificati via FTP o File Manager cPanel
2. Restart: cPanel → Setup Python App → Restart
   (oppure `touch tmp/restart.txt`)

---

## Repo correlati

| Repo | Ruolo |
|---|---|
| `carteggio-canneti-fiacchi-data` | Dati TEI/XML del carteggio |
| `carteggio-canneti-fiacchi-esd` | EVT viewer dell'edizione digitale |
| `esd-carteggio-canneti-fiacchi-dist` | Dist pubblicata dell'edizione digitale |
| `scripts_digiletclass` | Script di processing e publish workflow |

---

## Licenza

- Codice: MIT License
- Contenuti (testi, immagini, dati): CC BY 4.0
