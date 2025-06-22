from datetime import datetime
from app import create_app, db
from app.models import SocialMediaPost

app = create_app()

with app.app_context():
    # Create tables
    db.create_all()
    
    # Add sample data
    if not SocialMediaPost.query.first():
        sample_post = SocialMediaPost(
            platform='twitter',
            content='Test post',
            scheduled_time=datetime.utcnow()
        )
        db.session.add(sample_post)
        db.session.commit()
        print("✅ Database initialized with sample data!")