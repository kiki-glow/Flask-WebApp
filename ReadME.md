# Web Application with Flask and MongoDB

## Description
This is a simple web application built using Flask, MongoDB, and Bootstrap. The application allows users to register, log in, reset passwords, and manage their profiles. It features a polished UI, responsive design, and functionality for handling user authentication.

## Features
- **User Registration**: Create a new account with validation checks.
- **Login System**: Secure login using username and password.
- **Forgot Password**: Reset password functionality with email integration.
- **Responsive Design**: Optimized for desktops, tablets, and mobile devices.
- **Modern Styling**: Utilizes Bootstrap and custom CSS for an aesthetically pleasing interface.

---

## Technologies Used
- **Backend**: Python, Flask
- **Database**: MongoDB
- **Frontend**: HTML, CSS, Bootstrap
- **Email Service**: Flask-Mail (SMTP configuration for sending emails)
- **Development Tools**: 
  - Virtual Environment (venv)
  - Jinja2 for templating

---

## Project Structure
```
WebApp/
│
├── app.py                   # Main application file
├── templates/               # HTML templates
│   ├── index.html           # Homepage
│   ├── login.html           # Login page
│   ├── register.html        # Registration page
│   ├── forgot_password.html # Forgot password page
│
├── static/                  # Static files
│   ├── css/
│   │   └── styles.css       # Custom styles
│   └── js/                  # Optional JS files
│
├── requirements.txt         # Python dependencies
├── README.md                # Project documentation
└── config.py                # Configuration settings
```

---

## Installation and Setup

### Prerequisites
- Python 3.8 or higher
- MongoDB installed and running
- SMTP credentials for email functionality

### Steps to Run the Project

1. **Clone the Repository**
   ```bash
   git clone https://github.com/your-repo/webapp.git
   cd webapp
   ```

2. **Create a Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # For Linux/Mac
   venv\Scripts\activate     # For Windows
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up Environment Variables**
   Create a `.env` file with the following:
   ```
   SECRET_KEY=your_secret_key
   MONGO_URI=your_mongo_connection_string
   MAIL_SERVER=smtp.gmail.com
   MAIL_PORT=587
   MAIL_USERNAME=your_email@gmail.com
   MAIL_PASSWORD=your_email_password
   MAIL_USE_TLS=True
   ```

5. **Run the Application**
   ```bash
   flask run
   ```

6. **Access the Application**
   Open a browser and go to:
   ```
   http://127.0.0.1:5000
   ```

---

## Usage

### Pages
1. **Home Page**: Access general information about the app.
2. **Login**: Enter username and password to log in.
3. **Register**: Create a new account.
4. **Forgot Password**: Reset your password via email.

### Admin Features
- Can view all users.
- Manage and delete user accounts.

---

## Future Enhancements
- Add role-based access control (e.g., Admin vs. User).
- Enhance the UI with animations and additional styling.
- Implement password hashing for added security.
- Add testing coverage for all endpoints.

---

## Contributing
1. Fork the repository.
2. Create a new branch (`git checkout -b feature/your-feature`).
3. Commit your changes (`git commit -m 'Add some feature'`).
4. Push to the branch (`git push origin feature/your-feature`).
5. Open a pull request.

---

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.

---

## Contact
For questions or feedback, contact:
- **Email**: support@glowtechs.com
- **GitHub**: [Your GitHub Profile](https://github.com/your-profile) 

Enjoy building with Flask! 🎉