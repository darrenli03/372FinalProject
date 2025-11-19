# 372FinalProject

(using powershell)
creating vite frontend:
npm create vite@latest react372 -- --template react

make sure to create a virtual environment to install the pip files, use CTRL+SHIFT+P in vscode then click Python: Select Interpreter and click through to setup (make it in root directory)

#activate virtual environment
.\venv\Scripts\Activate.ps1

#export current requirements to requirements.txt
pip freeze > requirements.txt

#install from requirements.txt
pip install -r requirements.txt