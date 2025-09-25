# ⚡ SocialSync - Social Media Automation Dashboard

![Python](https://img.shields.io/badge/Python-3.11%2B-blue)
![Flask](https://img.shields.io/badge/Flask-3.0%2B-black)
![MySQL](https://img.shields.io/badge/MySQL-8.0%2B-blue)
![License: MIT](https://img.shields.io/badge/License-MIT-green)


**SocialSync** is a multi-page web application built with **Python** and **Streamlit** that simulates a comprehensive social media management tool.  
It provides a functional backend with a dedicated **SQLite** database, allowing users to **sign up, log in, schedule posts, manage marketing campaigns**, and **view a real-time analytics dashboard** that updates dynamically.

---

## ✨ Key Features

- 🔐 **Secure User Authentication**: Full sign-up and login functionality with password hashing (`hashlib`) to ensure user data is stored securely.
- 🧭 **Multi-Page Navigation**: A robust, multi-page user interface that separates functionalities into **Dashboard**, **Scheduler**, and **Campaigns** sections.
- 📅 **Dynamic Post Scheduler**: Users can schedule posts for various platforms (Instagram, Twitter, etc.), which are saved to a persistent database.
- 🎯 **Campaign Management**: Create, track, and manage marketing campaigns. The application automatically links scheduled posts to their respective campaigns.
- 📊 **Real-Time Analytics Dashboard**: Features interactive charts (powered by **Plotly**) that display live engagement metrics (likes, shares, comments) for all published posts.
- ⚙️ **Simulated Background Tasks**: A task runner script simulates real-time updates by automatically "publishing" scheduled posts and generating random engagement data.
- 💾 **Persistent Data Storage**: All user data, posts, and campaigns are stored in a local **SQLite** database, ensuring data persistence across sessions.

---

## 🛠️ Technology Stack

- **Backend**: Python  
- **Web Framework**: Streamlit  
- **Data Manipulation**: Pandas  
- **Database**: SQLite  
- **Data Visualization**: Plotly  
- **Authentication**: `hashlib` (for secure password hashing)

---

## 📂 Project Structure

```
social\_sync\_app/
│
├── app.py              # Main app: Handles Login/Sign Up
├── database.py         # Module for all SQLite database operations
├── tasks.py            # Module for simulating background tasks (posting & engagement)
│
├── pages/
│   ├── 1\_Dashboard.py    # Analytics dashboard page
│   ├── 2\_Scheduler.py    # Post scheduling page
│   └── 3\_Campaigns.py    # Campaign management page
│
├── social\_sync.db      # SQLite database file (created on first run)
└── requirements.txt    # Project dependencies

```

---

## 🚀 Getting Started

Follow these instructions to set up and run the project on your local machine.

### ✅ Prerequisites
- **Python 3.8+** installed

---

### 1. Clone the Repository

```bash
git clone https://github.com/Atharva-Kulkarni-694/Social-Media-Automation.git
cd Social-Media-Automation
````

---

### 2. Create a Virtual Environment (Recommended)

**Windows:**

```bash
python -m venv venv
.\venv\Scripts\activate
```

**macOS / Linux:**

```bash
python3 -m venv venv
source venv/bin/activate
```

---

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

> 💡 If you haven’t created a `requirements.txt` yet, you can install manually:

```bash
pip install streamlit pandas plotly
```

---

### 4. Run the Application

```bash
streamlit run app.py
```

Your web browser will open to the app’s **Login Page**. Create an account and start using the platform!

---

## 💡 How It Works

1. **Database Initialization**: On the first run, `database.py` creates a `social_sync.db` file with tables for `users`, `posts`, and `campaigns`.
2. **Authentication Flow**: `app.py` handles user sign-ups and logins. Sessions are managed using **Streamlit's session state**.
3. **Task Simulation**: `tasks.py` checks for scheduled posts that should be published. It updates their status and simulates engagement data.
4. **Data Visualization**: The **Dashboard** and **Campaigns** pages query the database and render interactive charts using **Plotly**.

---

## 🔮 Future Improvements

* 🔗 **Connect to Real APIs**: Integrate with Twitter, Facebook, or LinkedIn APIs to publish real posts.
* 🔐 **OAuth2 Integration**: Enable users to securely connect their social media accounts.
* 📈 **Advanced Analytics**: Add follower growth charts, engagement rate calculations, and posting time suggestions.
* ☁️ **Deployment**: Deploy the app to **Streamlit Cloud**, **Heroku**, or **AWS**.

---

## 📄 License

This project is licensed under the **MIT License**. See the `LICENSE` file for details.

---

