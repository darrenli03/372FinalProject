# Setup (using PowerShell)

## Creating Vite React frontend
```powershell
npm create vite@latest react372 -- --template react
```

## Creating Python virtual environment (run in project root)
```powershell
python -m venv venv
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process -Force
```
Alternatively, 
- Press Ctrl+Shift+P → "Python: Select Interpreter", click through to set up virtual environment

## Activate virtual environment
```powershell
.\venv\Scripts\Activate.ps1
```

## Export current requirements to requirements.txt
```powershell
pip freeze > requirements.txt
```

## Install from requirements.txt
```powershell
pip install -r requirements.txt
```
