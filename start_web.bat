@echo off
echo.
echo 🏦 Bank Statement Processor - Web Application
echo ==============================================
echo.

REM Check if virtual environment exists
if not exist "venv\" (
    echo ❌ Virtual environment not found!
    echo Please run: python -m venv venv ^&^& venv\Scripts\activate ^&^& pip install -r requirements.txt
    exit /b 1
)

REM Activate virtual environment
echo 📦 Activating virtual environment...
call venv\Scripts\activate

REM Check if models exist
if not exist "models\classifier.joblib" (
    echo ⚠️  ML models not found. Training models...
    python scripts\generate_training_data.py
    python scripts\train_classifier.py
    echo ✅ Models trained successfully!
    echo.
)

REM Create necessary directories
if not exist "uploads\" mkdir uploads
if not exist "outputs\" mkdir outputs
if not exist "logs\" mkdir logs

echo 🚀 Starting web server...
echo.
echo Access the application at: http://localhost:5000
echo Press Ctrl+C to stop the server
echo.

python app.py
