# Club Notification System - Vue.js & Flask Backend

This project is a **Club Notification System** built using **Vue.js** for the frontend and **Flask** for the backend, integrated with **Tailwind CSS** and PostgreSQL. Follow this guide to set up and run both the frontend and backend.

---
## 🚀 Features
- **Real-time Notifications** using WebSockets (Flask-SocketIO)
- **Email Alerts** via Brevo (Sendinblue API)
- **Rate Limiting & Security** with Flask-Limiter
- **Database Connection Pooling** with PostgreSQL
- **Responsive UI** using Tailwind CSS
- **Role-based Authentication**
- **Logging & Monitoring**

---
## 📌 Prerequisites
Ensure that the following software is installed on your machine:

### Frontend (Vue.js)
- [Node.js](https://nodejs.org/) (LTS version recommended)
- [npm](https://www.npmjs.com/) (Node Package Manager)

To check installation:
```sh
node -v
npm -v
```

### Backend (Flask)
- [Python 3.8+](https://www.python.org/downloads/)
- [PostgreSQL](https://www.postgresql.org/)
- [Redis](https://redis.io/) (for background tasks & caching)

Check Python version:
```sh
python --version
```
---
## 🛠 Setup Instructions

### **1. Clone the Repository**
```sh
git clone https://github.com/Asmodeus14/Club-Notification-System
cd Club-Notification-System
```

---
## 🌟 Frontend (Vue.js)

### **2. Navigate to the Frontend Directory**
```sh
cd frontend
```

### **3. Install Dependencies**
```sh
npm install
```

### **4. Install Tailwind CSS (If not already installed)**
```sh
vue add tailwind
```
_Select "minimal" configuration when prompted._

### **5. Configure Tailwind CSS**
Update `src/assets/tailwind.css` (create if missing):
```css
@tailwind base;
@tailwind components;
@tailwind utilities;
```

Update `vue.config.js` to process Tailwind CSS:
```javascript
// vue.config.js
module.exports = {
  css: {
    loaderOptions: {
      postcss: {
        plugins: [require('tailwindcss'), require('autoprefixer')],
      },
    },
  },
};
```

### **6. Run the Vue Development Server**
```sh
npm run serve
```
Visit [http://localhost:8080](http://localhost:8080) to access the UI.

---
## 🖥 Backend (Flask & PostgreSQL)

### **2. Navigate to the Backend Directory**
```sh
cd backend
```

### **3. Create a Virtual Environment & Install Dependencies**
```sh
python -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate    # Windows
pip install -r requirements.txt
```

### **4. Set Up Environment Variables**
Create a `.env` file:
```ini
DB_NAME=your_database
DB_USER=your_username
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
BREVO_API_KEY=your_sendinblue_api_key
SECRET_KEY=your_flask_secret_key
REDIS_URL=redis://localhost:6379
```

### **5. Initialize the Database**
```sh
python App.py
```

### **6. Start the Backend Server**
```sh
flask run
```
Visit [http://127.0.0.1:5000](http://127.0.0.1:5000) for the backend API.

---
## 📜 Backend `requirements.txt`

```txt
Flask
Flask-Cors
psycopg2
psycopg2-binary
werkzeug
python-dotenv
marshmallow
flask-limiter
flask-socketio
redis
dramatiq
sib-api-v3-sdk
```

---
## 🚀 Running in Production Mode

### **Frontend** (Build for production)
```sh
npm run build
```
This generates an optimized build in the `dist/` folder.

### **Backend** (Using Gunicorn for Production)
```sh
gunicorn -w 4 -b 0.0.0.0:5000 App:app
```

---
## ✅ Troubleshooting

### 🔹 **Frontend Issues**
1. **Tailwind Not Working?** Ensure `tailwind.css` is correctly imported.
2. **Dependencies Not Installing?** Try:
   ```sh
   rm -rf node_modules package-lock.json
   npm install
   ```

### 🔹 **Backend Issues**
1. **Database Connection Failing?** Check `.env` for correct credentials.
2. **Redis Not Running?** Start Redis server:
   ```sh
   redis-server
   ```
3. **Too Many Connections?** Increase PostgreSQL max connections:
   ```sql
   ALTER SYSTEM SET max_connections = 200;
   ```

---
## 📄 License
This project is licensed under the MIT License.

---
### 🌟 **Contributions**
Contributions are welcome! Feel free to fork the repo, create a feature branch, and submit a pull request. 😊

---
### 🔗 Useful Links
- [Vue.js Documentation](https://vuejs.org/)
- [Tailwind CSS Documentation](https://tailwindcss.com/docs/)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)

🚀 **Happy Coding!**

