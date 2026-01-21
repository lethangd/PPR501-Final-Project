# Desktop App (Tkinter)

This folder contains the Tkinter desktop UI (primary UI).

## Run (requires Python)

1. Start backend services:

```bash
docker compose up --build -d db backend
```

2. Create a virtualenv and install dependencies:

```powershell
cd desktop_app
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Or one-click from project root:

```powershell
.\run_desktop.ps1
```

3. Run the app:

```powershell
cd ..
python -m desktop_app.app --api http://localhost:8000/api
```

## Notes

- The API returns XML for successful responses.
- The Statistics tab uses seaborn/matplotlib for charts.
- Run from project root so Python can find the `desktop_app` package.
