from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import pytz
from app.models import db, SocialMediaPost
from app.services.platform_integration import PlatformIntegration
from config import Config

class Scheduler:
    def __init__(self):
        self.scheduler = BackgroundScheduler(timezone=pytz.timezone(Config.SCHEDULER_TIMEZONE))
        self.platform_integration = PlatformIntegration()
    
    def init_app(self, app):
        self.app = app
        with app.app_context():
            self.schedule_pending_posts()
    
    def start(self):
        self.scheduler.start()
    
    def schedule_pending_posts(self):
        pending_posts = SocialMediaPost.query.filter_by(posted=False).all()
        
        for post in pending_posts:
            self.schedule_post(post)
    
    def schedule_post(self, post):
        trigger_time = post.scheduled_time.astimezone(
            pytz.timezone(Config.SCHEDULER_TIMEZONE))
            
        self.scheduler.add_job(
            self._post_to_social_media,
            'date',
            run_date=trigger_time,
            args=[post.id],
            id=f'post_{post.id}'
        )
    
    def _post_to_social_media(self, post_id):
        with self.app.app_context():
            post = SocialMediaPost.query.get(post_id)
            if post and not post.posted:
                try:
                    response = self.platform_integration.post_content(
                        platform=post.platform,
                        content=post.content
                    )
                    
                    post.posted = True
                    post.engagement_data = {
                        'initial_response': response,
                        'posted_at': datetime.now().isoformat()
                    }
                    db.session.commit()
                except Exception as e:
                    print(f"Error posting content: {e}")