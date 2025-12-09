# 🔐 Proffesional Django REST Framework JWT Authentication System  :
A complete, secure & modern authentication system built using **Django**, **DRF**, and **Simple JWT**, featuring **Email Verification**, **Custom User Model**, and **Advanced Token Logging**.  
## 🚀✨ Key Features

📝 **1. User Registration (Custom User Model)**
•	Unique Username & Email  
•	Phone Number support  
•	Encrypted Password  
•	Auto-generated Email Verification Token  
•	User **cannot login until email is verified**  

---


 📧 **2. Email Verification System**
✔ User registers → system sends email  
✔ Email contains verification link  
✔ User clicks → account becomes **verified**  

📨 Sample email text:
Hi username, please click the link and verify your email.


🔗 Sample verification URL:
http://127.0.0.1:8000/verify-email/
<token>/



🔐 **3. JWT Login System (Secure)**
•	Login using **username + password/email + password**  
•	Only **verified** users can login  
	Generates:
	🔑 Access Token 
	🔁 Refresh Token  
	🆔 JTI (Token ID for security logging)

---
 📊 **4. Token Activity Logging**
Every token action is logged:
	🔵 LOGIN  
	🟡 REFRESH  
	🔴 LOGOUT  


Logged details:
	🌐 IP Address  
	💻 Device / User Agent  
	🆔 Token JTI  
	🕒 Timestamp  
-  🌐 IP Address Tracking (Advanced Security)

   
🟦 Features:
•	Last_ip automatically stored on every login
•	Login_ip_history table/model tracks all previous login ips
•	Shows:
o	🌍 IP Address
o	🕒 Login Time
o	📱 Device/User-Agent



🚨 suspicious login detection
System can detect & log:
•	New unknown ip
•	Frequent ip changes
•	Sudden location change
(useful for notifying admin or sending email alerts)



💻 Device Tracking System (Highly Secure)
🟩 Features Included:
✔ last_login_device
Stores:
	Browser name
	Os
	Device type
	User-agent
	Last Login Date
	Last Login Device Name
	Last IP Name
	Last Logout
	Login count +1………

✔ Device List API
User can see:
	All logged-in devices
	IP
	Device Name
	Login Time
	Active or Expired Status
•	IP Address

✔ Logout from a Specific Device
User can logout:
•	A single device
•	A specific session
•	All sessions except current
✔ Block a Device Permanently
If a suspicious or unwanted device logs in:
•	Mark device as blocked
•	Prevents future logins from that device
🚨 Perfect for security-focused applications like Banking, E-commerce, EdTech, Admin Dashboards etc.
________________________________________

📊 6️⃣ Token Logging System
Every action stored:
	🔵 LOGIN
	🟡 REFRESH
	🔴 LOGOUT
Logs include:
•	IP Address
•	Device Info
•	Token JTI
•	Timestamp
________________________________________
👤 7️⃣ User Profile System
Returns:
	Username
	Email
	Phone
	Role
	Verification Status
	Last Login Device
	Last Login IP
	Login Count
	List of devices (optional)

## 🛠️ Tech Stack

| Technology | Purpose |
|-----------|----------|
| 🐍 Python | Backend Language |
| ⚙️ Django | Framework |
| 🎛 DRF | REST API |
| 🔐 Simple JWT | Authentication |
| 📨 SMTP | Email Sending |
| 🗄 SQLite / PostgreSQL | Database |

```bash
git clone https://github.com/yourusername/yourrepo.git
cd yourrepo

2️⃣ Install Required Packages
pip install -r requirements.txt

3️⃣ Migrate Database
python manage.py migrate

4️⃣ Create Admin
python manage.py createsuperuser

5️⃣ Run the Development Server
python manage.py runserver

📧 Email Backend Setup
Development (Console Emails)
Add to settings.py:

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
DEFAULT_FROM_EMAIL = "noreply@example.com"
➡ Email details will show directly in your terminal — no SMTP needed.

🔗 API Endpoints (Full List)
🟢 Register

POST /register/

{
  "username": "demo",
  "email": "demo@mail.com",
  "Phone_number": "017XXXXXXXX",
  "password": "Demo@1234"
}

🔵 Verify Email

GET /verify-email/<token>/

{
  "username": "demo",
  "password": "Demo@1234"
}


🔁 Refresh Token

POST /token/refresh/

👤 Profile

GET /profile/
Header:
Authorization: Bearer <access_token>

📂 Project Structure:
project/
│
├── accounts/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   ├── utils.py
│
├── JWT/
│   ├── settings.py
│
├── requirements.txt
├── manage.py
└── README.md

🤝 Contributing

PRs are welcome!
For major changes, open an issue first.

📄 License

📝 Licensed under the MIT License.

❤️ Author

Abid Hasan
Passionate Django & DRF Backend Developer
