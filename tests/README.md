# NetWatch Test Suite

This directory contains the automated test suite for NetWatch.

The project uses **pytest** for unit testing and **pytest-cov** for code coverage.

---

# Test Structure

```
tests/
│
├── controllers/
│
├── gui/
│   ├── test_details_panel.py
│   ├── test_filter_bar.py
│   ├── test_history_window.py
│   ├── test_main_window_actions.py
│   ├── test_main_window_init.py
│   ├── test_main_window_update.py
│   ├── test_process_table.py
│   ├── test_statusbar.py
│   └── test_toolbar.py
│
├── monitor/
│   ├── test_connection_cache.py
│   ├── test_connection_monitor.py
│   └── test_network_scanner.py
│
├── models/
│   ├── test_models.py
│   └── test_models_statistics.py
│
├── services/
│   ├── test_browser_service.py
│   ├── test_database.py
│   ├── test_dns_service.py
│   ├── test_dns_worker.py
│   ├── test_export_service.py
│   ├── test_filter_service.py
│   ├── test_history_search.py
│   ├── test_history_service.py
│   ├── test_icon_service.py
│   ├── test_notification_service.py
│   ├── test_process_action_service.py
│   ├── test_process_service.py
│   ├── test_publisher_service.py
│   ├── test_settings_service.py
│   └── test_statistics_service.py
│
├── utils/
│   └── test_resource_path.py
│
├── conftest.py
└── README.md
```

---

# Running Tests

Run the complete test suite:

```powershell
pytest
```

Run with verbose output:

```powershell
pytest -v
```

Run a specific file:

```powershell
pytest tests/gui/test_main_window_actions.py
```

Run a specific test:

```powershell
pytest tests/gui/test_main_window_actions.py::test_toggle_refresh_start
```

---

# Coverage

Generate coverage:

```powershell
pytest --cov=. --cov-report=term
```

Generate HTML report:

```powershell
pytest --cov=. --cov-report=html
```

Open the report:

```
htmlcov/index.html
```

---

# CI/CD

Every Push and Pull Request that modifies Python source code automatically runs:

- Dependency installation
- Complete pytest suite
- Coverage generation

Documentation-only changes do not trigger the workflow.

Ignored file types include:

- *.md
- *.html
- *.css
- *.js

---

# Branch Protection

The `main` branch is protected using GitHub Branch Protection Rules.

Pull Requests cannot be merged unless:

- All required GitHub Actions succeed
- Every test passes
- Required status checks are successful

If any test fails, GitHub blocks the merge until the issue is resolved.

---

# Writing Tests

Guidelines:

- One feature per test file.
- Keep tests independent.
- Mock external dependencies whenever possible.
- Avoid network access.
- Avoid modifying real user data.
- Use descriptive test names.
- Prefer small focused tests over large integration tests.

Example:

```python
def test_export_creates_csv():
    ...
```

instead of:

```python
def test_export():
    ...
```

---

# Test Categories

Current test coverage includes:

- GUI Components
- Monitor
- Services
- Database
- DNS Resolution
- History
- Export
- Notifications
- Models
- Controllers
- Utility Functions

---

# Mocking

The test suite uses:

- unittest.mock.MagicMock
- unittest.mock.patch

to isolate components and avoid:

- Network requests
- File system modifications
- Running external applications
- Starting background threads

---

# Coverage Goal

Target coverage:

- Minimum: 90%
- Current: Maintain above project target

All new features should include corresponding unit tests before being merged.

---

# Continuous Quality

Before opening a Pull Request, verify:

```powershell
pytest
```

and

```powershell
pytest --cov=.
```

A Pull Request should only be submitted when the entire test suite passes successfully.
