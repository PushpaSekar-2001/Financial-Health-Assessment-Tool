@echo off
REM Clear node modules cache
echo Clearing npm cache...
cd frontend
del /Q package-lock.json
rmdir /S /Q node_modules
echo npm cache cleared.

REM Reinstall dependencies
echo Installing dependencies...
npm install

REM Start the application
echo Starting applications...
start cmd /k "cd backend && python app.py"
timeout /t 5
start cmd /k "npm start"

echo Applications started!
echo Frontend: http://localhost:3002
echo Backend: http://127.0.0.1:5000/api
