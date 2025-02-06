Start-Process powershell -ArgumentList "cd D:\Club-Notification-System; npm run serve" -NoNewWindow
Start-Process powershell -ArgumentList "cd D:\Club-Notification-System\backend; python app.py" -NoNewWindow
Start-Process powershell -ArgumentList "cd D:\Club-Notification-System\backend; dramatiq email_" -NoNewWindow
Start-Process powershell -ArgumentList "docker start redis" -NoNewWindow
