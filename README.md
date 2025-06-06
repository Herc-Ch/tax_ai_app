# Tax AI App

This is a React-based web application designed to provide AI-driven tax filing assistance.  
It features a responsive home page and a user-friendly form for basic tax data input.

---

## 🚀 Getting Started

### **Prerequisites**

- [Node.js](https://nodejs.org/) (v16 or newer recommended)
- npm (comes with Node.js)

---

### **Setup Process**

1. **Clone the repository**

   ```bash
   git clone https://github.com/Herc-Ch/tax_ai_app.git
   cd tax_ai_app
   ```
2. Install dependencies
   
   ```bash
   npm install
   ```  
3. Start the development server
   
   ```bash
   npm start
   ```
4. Open the App
   
- Go to http://localhost:3000 in your browser.

- The app will reload automatically as you edit the code.
---

## 🖥️ Backend API Integration

### Backend (Flask) Prerequisites

- [Python 3.8+](https://www.python.org/)
- [pip](https://pip.pypa.io/en/stable/)

### Setup & Run the Backend

1. **Navigate to the backend directory:**
   ```bash
   cd backend
   ```
2. Install Dependencies
   ```bash
   pip install flask flask-cors
   ```
3. Run the Flash backend server
   ```bash
   python app.py
   ```
   
🔗 API Endpoints
Your backend exposes these endpoints at http://localhost:5000/api/submit-tax:

Method	Endpoint	Description	Example Body (JSON)
POST	/api/submit-tax	Submit new tax data	{ "name": "Alice", "income": 1000 }
GET	/api/submit-tax	Get all tax data submissions	–
PUT	/api/submit-tax	Update existing tax data (by name)	{ "name": "Alice", "income": 1500 }
DELETE	/api/submit-tax?name=Alice	Delete submission by name	–

You can test these with Postman or your React app.

🏃 How to Run Both Servers Together
1. Start the backend in one terminal:
      ```bash
    cd backend
    python app.py
      ```
2. Start the frontend in another terminal:
      ```bash
    cd tax_ai_app
    npm start
      ```
Now your frontend at http://localhost:3000 can communicate with your backend API at http://localhost:5000/api/submit-tax.
