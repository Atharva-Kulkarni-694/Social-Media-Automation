import sqlite3
import pandas as pd
import hashlib
from datetime import datetime

# --- DATABASE SETUP ---
def init_db():
    """Initializes the database and creates/updates tables."""
    conn = sqlite3.connect('social_sync.db')
    c = conn.cursor()
    # User table
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    # Posts table - ADDED status, likes, shares, comments, campaign_id
    c.execute('''
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY,
            user_id INTEGER NOT NULL,
            campaign_id INTEGER,
            platform TEXT NOT NULL,
            content TEXT NOT NULL,
            scheduled_time DATETIME NOT NULL,
            status TEXT DEFAULT 'Scheduled',
            likes INTEGER DEFAULT 0,
            shares INTEGER DEFAULT 0,
            comments INTEGER DEFAULT 0,
            FOREIGN KEY (user_id) REFERENCES users (id),
            FOREIGN KEY (campaign_id) REFERENCES campaigns (id)
        )
    ''')
    # Campaigns table
    c.execute('''
        CREATE TABLE IF NOT EXISTS campaigns (
            id INTEGER PRIMARY KEY,
            user_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            status TEXT NOT NULL,
            platforms TEXT NOT NULL,
            start_date DATE NOT NULL,
            end_date DATE NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    conn.commit()
    conn.close()

# --- USER FUNCTIONS ---
def hash_password(password):
    """Hashes the password for security."""
    return hashlib.sha256(password.encode()).hexdigest()

def add_user(username, password):
    """Adds a new user to the database."""
    conn = sqlite3.connect('social_sync.db')
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hash_password(password)))
        conn.commit()
        return True
    except sqlite3.IntegrityError: # This error occurs if username already exists
        return False
    finally:
        conn.close()

def validate_user(username, password):
    """Validates user credentials and returns user ID if correct."""
    conn = sqlite3.connect('social_sync.db')
    c = conn.cursor()
    c.execute("SELECT id, password FROM users WHERE username = ?", (username,))
    user = c.fetchone()
    conn.close()
    if user and user[1] == hash_password(password):
        return user[0]  # Return user ID
    return None

# --- POST FUNCTIONS ---
def add_post(user_id, platform, content, scheduled_time, campaign_id=None):
    """Adds a new post to the database, optionally linking it to a campaign."""
    conn = sqlite3.connect('social_sync.db')
    c = conn.cursor()
    c.execute("INSERT INTO posts (user_id, platform, content, scheduled_time, campaign_id) VALUES (?, ?, ?, ?, ?)",
              (user_id, platform, content, scheduled_time, campaign_id))
    conn.commit()
    conn.close()

def get_posts(user_id):
    """Retrieves all posts for a specific user as a DataFrame."""
    conn = sqlite3.connect('social_sync.db')
    df = pd.read_sql_query("""
        SELECT p.id, p.platform, p.content, p.scheduled_time, p.status, p.likes, p.shares, p.comments, c.name as campaign_name
        FROM posts p
        LEFT JOIN campaigns c ON p.campaign_id = c.id
        WHERE p.user_id = ?
        ORDER BY p.scheduled_time DESC
    """, conn, params=(user_id,))
    conn.close()
    return df

def get_due_posts(user_id):
    """Gets all posts that are scheduled for a time in the past and not yet posted."""
    conn = sqlite3.connect('social_sync.db')
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    df = pd.read_sql_query("""
        SELECT id FROM posts
        WHERE user_id = ? AND status = 'Scheduled' AND scheduled_time <= ?
    """, conn, params=(user_id, now))
    conn.close()
    return df

def update_post_status_and_engagement(post_id, status, likes, shares, comments):
    """Updates a post's status and engagement metrics after 'posting'."""
    conn = sqlite3.connect('social_sync.db')
    c = conn.cursor()
    c.execute("""
        UPDATE posts
        SET status = ?, likes = ?, shares = ?, comments = ?
        WHERE id = ?
    """, (status, likes, shares, comments, post_id))
    conn.commit()
    conn.close()

# --- CAMPAIGN FUNCTIONS ---
def add_campaign(user_id, name, status, platforms, start_date, end_date):
    """Adds a new campaign to the database."""
    conn = sqlite3.connect('social_sync.db')
    c = conn.cursor()
    platforms_str = ', '.join(platforms)
    c.execute("INSERT INTO campaigns (user_id, name, status, platforms, start_date, end_date) VALUES (?, ?, ?, ?, ?, ?)",
              (user_id, name, status, platforms_str, start_date, end_date))
    conn.commit()
    conn.close()

def get_campaigns(user_id):
    """Retrieves all campaigns for a user."""
    conn = sqlite3.connect('social_sync.db')
    df = pd.read_sql_query("SELECT id, name, status, platforms, start_date, end_date FROM campaigns WHERE user_id = ?", conn, params=(user_id,))
    conn.close()
    return df

def get_campaign_performance(user_id):
    """Calculates total engagement for each campaign."""
    conn = sqlite3.connect('social_sync.db')
    query = """
    SELECT
        c.name as campaign_name,
        c.status,
        c.platforms,
        COUNT(p.id) as total_posts,
        SUM(p.likes) as total_likes,
        SUM(p.shares) as total_shares,
        SUM(p.comments) as total_comments
    FROM campaigns c
    LEFT JOIN posts p ON c.id = p.campaign_id
    WHERE c.user_id = ?
    GROUP BY c.id
    """
    df = pd.read_sql_query(query, conn, params=(user_id,))
    conn.close()
    # Fill NaN values with 0 for campaigns with no posts yet
    df[['total_posts', 'total_likes', 'total_shares', 'total_comments']] = df[['total_posts', 'total_likes', 'total_shares', 'total_comments']].fillna(0).astype(int)
    return df

