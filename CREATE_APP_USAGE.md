# Running the Project (Quickstart)

## 1. **Clone and Install Dependencies**

```bash
git clone <your-repo-url>
cd digiletclass
pip install -r requirements.txt
```

## 2. **Run the App**

### Option A: Using Flask CLI (Recommended)

```bash
export FLASK_APP=app/webapp.py
export FLASK_ENV=development  # Optional: enables debug mode
flask run
```

### Option B: Directly with Python

```bash
python app/webapp.py
```

---

# Running the Tests

## 1. **Install pytest (if not already installed)**

```bash
pip install pytest
```

## 2. **Run the tests**

From the project root directory:

```bash
pytest
```

This will automatically discover and run all tests in the `tests/` directory.

---

# Using the `create_app()` Factory in This Project

This project now uses the Flask **application factory pattern** for better flexibility and maintainability.

## What Changed?
- The Flask app is no longer created at import time.
- Instead, you must call `create_app()` to get an app instance.

---

## How to Use

### 1. **Running the App (Development)**

**With Flask CLI:**

```bash
export FLASK_APP=app/webapp.py
export FLASK_ENV=development  # Optional: enables debug mode
flask run
```

**Directly with Python:**

```bash
python app/webapp.py
```

---

### 2. **For Testing**

In your tests, you can create an app instance with custom config:

```python
from app import create_app
import pytest

@pytest.fixture
def app():
    app = create_app({'TESTING': True})
    return app
```

---

### 3. **For Production**

Your WSGI server (e.g., Gunicorn) should use:

```bash
gunicorn 'app.webapp:app'
```

---

## Migration Notes
- **Old way:**
  ```python
  from app import app
  ```
- **New way:**
  ```python
  from app import create_app
  app = create_app()
  ```
- The `app` variable in `app/webapp.py` is now created by calling `create_app()`.

---

## Why Use the Factory Pattern?
- Supports multiple app instances (e.g., for testing)
- Cleaner configuration management
- Avoids side effects at import time
- Recommended by Flask for all but the simplest projects

---

For more, see the [Flask Application Factories documentation](https://flask.palletsprojects.com/en/latest/patterns/appfactories/). 