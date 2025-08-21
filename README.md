# DigiLetClass

## Quickstart

1. Setup (recommended with virtualenv):
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

2. Run the app:
   - With Flask CLI (recommended):
     ```bash
     export FLASK_APP=app/webapp.py
     flask run
     ```
   - Or directly:
     ```bash
     python app/webapp.py
     ```

3. Run tests:
   ```bash
   export PYTHONPATH=.
   pytest -q
   ```

## Main Routes

- Home: `/`
- Project: `/project`
- Methodology: `/methodology`
- Entities (landing): `/entities`
- Entities by type: `/entities/<orgs|people|places>`
- News and Events (list): `/news`
- News/Event detail: `/news/<news_id>`

## Project Structure

```
app/
  __init__.py         # App factory
  webapp.py           # Entry point
  blueprints/         # Flask blueprints (routes)
  config/             # Configuration and type maps
  static/             # CSS, JS, images
  templates/          # Jinja2 templates and macros
  utils.py            # Utility functions

tests/                # Test suite
requirements.txt      # Python dependencies
README.md             # This file
LICENSE               # MIT (code) + CC BY 4.0 (content)
```

## License

- Code: MIT License. See `LICENSE`.
- Content (data, text, images unless otherwise noted): Creative Commons Attribution 4.0 International (CC BY 4.0).

You are free to share and adapt the content with attribution. Details: https://creativecommons.org/licenses/by/4.0/