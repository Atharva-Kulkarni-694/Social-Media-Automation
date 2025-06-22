from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import (
    LoginManager,
    UserMixin,
    login_user,
    logout_user,
    login_required,
    current_user
)
from app import create_app, db
from app.models import SocialMediaPost, UserEngagement
from app.services.scheduler import Scheduler
from datetime import datetime
import logging
from werkzeug.security import generate_password_hash, check_password_hash

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create Flask application
app = create_app()
app.secret_key = 'your-secret-key-here'  # Change this for production!

# Initialize Login Manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# User Loader
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# User Model
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# Initialize scheduler
app.scheduler = Scheduler()

def initialize_application():
    """Initialize database and start scheduler"""
    with app.app_context():
        try:
            # Create database tables
            db.create_all()
            logger.info("Database tables created successfully")
            
            # Create admin user if not exists
            if not User.query.filter_by(username='admin').first():
                admin = User(username='admin')
                admin.set_password('admin123')  # Change this password!
                db.session.add(admin)
                db.session.commit()
                logger.info("Created default admin user")
            
            # Start scheduler
            app.scheduler.start()
            logger.info("Scheduler started successfully")
            
            # Add sample post if empty
            if not SocialMediaPost.query.first():
                sample_post = SocialMediaPost(
                    platform='twitter',
                    content='Welcome to Social Media Automation!',
                    scheduled_time=datetime.utcnow(),
                    posted=True
                )
                db.session.add(sample_post)
                db.session.commit()
                logger.info("Added sample post to database")
                
        except Exception as e:
            logger.error(f"Initialization failed: {e}")
            raise

# Authentication Routes
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user)
            flash('Logged in successfully!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password', 'danger')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

# Application Routes
@app.route('/')
@login_required
def dashboard():
    """Dashboard showing recent activity"""
    recent_posts = SocialMediaPost.query.order_by(
        SocialMediaPost.scheduled_time.desc()
    ).limit(5).all()
    
    return render_template('dashboard.html', recent_posts=recent_posts)

@app.route('/schedule', methods=['GET', 'POST'])
@login_required
def schedule():
    """Schedule new posts"""
    if request.method == 'POST':
        try:
            platform = request.form['platform']
            content = request.form['content']
            scheduled_time = datetime.strptime(
                request.form['scheduled_time'],
                '%Y-%m-%dT%H:%M'
            )
            
            new_post = SocialMediaPost(
                platform=platform,
                content=content,
                scheduled_time=scheduled_time,
                user_id=current_user.id
            )
            
            db.session.add(new_post)
            db.session.commit()
            
            app.scheduler.schedule_post(new_post)
            flash('Post scheduled successfully!', 'success')
            return redirect(url_for('dashboard'))
            
        except Exception as e:
            logger.error(f"Failed to schedule post: {e}")
            flash('Error scheduling post. Please try again.', 'danger')
    
    return render_template('schedule.html')

@app.route('/analytics')
@login_required
def analytics():
    """Show performance analytics"""
    # Implement real analytics queries here
    return render_template('analytics.html')

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return {'status': 'healthy', 'timestamp': datetime.utcnow().isoformat()}, 200

# Initialize the application
initialize_application()

if __name__ == '__main__':
    try:
        logger.info("Starting Flask application")
        app.run(
            host='0.0.0.0',
            port=5000,
            debug=True  # Set to False in production
        )
    except Exception as e:
        logger.critical(f"Application failed to start: {e}")