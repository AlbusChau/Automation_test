@echo off
echo --- Setting up project environment ---

:: Check if venv already exists, if not, create it
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

:: Activate the venv
echo Activating virtual environment...
call venv\Scripts\activate.bat

:: Install everything from your requirements.txt
echo Installing dependencies from requirements.txt...
pip install --upgrade pip
pip install -r requirements.txt

echo.
echo --- Setup complete! ---
echo You are now in the virtual environment.
echo You can run your tests now.
pause