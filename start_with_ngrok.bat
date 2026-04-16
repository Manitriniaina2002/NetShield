@echo off
REM Start NetShield backend with ngrok tunnel

echo ===================================
echo NetShield - Backend with ngrok
echo ===================================
echo.

REM Check if backend is running
cd backend
echo Starting backend on localhost:8000...
timeout /t 2

start cmd /k "uvicorn main:app --reload --port 8000"

timeout /t 3

echo.
echo Starting ngrok tunnel to expose backend...
echo (You'll see your public URL in the ngrok terminal)
echo.
timeout /t 2

start cmd /k "ngrok http 8000"

echo.
echo ===================================
echo Both services started!
echo.
echo Backend: http://localhost:8000/api/health
echo ngrok: http://127.0.0.1:4040 (to see tunnel details)
echo.
echo Next: Copy the ngrok URL and deploy frontend to Vercel
echo ===================================
pause
