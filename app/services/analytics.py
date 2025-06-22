import pandas as pd
from app.models import UserEngagement, SocialMediaPost, db
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import seaborn as sns
import io
import base64

class Analytics:
    def __init__(self, time_period=30):
        self.time_period = time_period
    
    def get_engagement_data(self, platform=None):
        query = UserEngagement.query
        
        if platform:
            query = query.filter_by(platform=platform)
            
        return query.filter(
            UserEngagement.timestamp >= datetime.now() - timedelta(days=self.time_period)
        ).all()
    
    def get_post_performance(self):
        posts = SocialMediaPost.query.filter(
            SocialMediaPost.posted == True,
            SocialMediaPost.engagement_data.isnot(None)
        ).all()
        
        return [
            {
                'platform': post.platform,
                'scheduled_time': post.scheduled_time,
                'engagement': post.engagement_data.get('likes', 0) + 
                             post.engagement_data.get('comments', 0) + 
                             post.engagement_data.get('shares', 0),
                'reach': post.engagement_data.get('reach', 0)
            }
            for post in posts
        ]
    
    def generate_engagement_plot(self, platform=None):
        data = self.get_engagement_data(platform)
        if not data:
            return None
            
        df = pd.DataFrame([{
            'timestamp': e.timestamp,
            'engagement_rate': e.engagement_rate,
            'platform': e.platform
        } for e in data])
        
        plt.figure(figsize=(10, 6))
        
        if platform:
            sns.lineplot(data=df, x='timestamp', y='engagement_rate')
            plt.title(f'Engagement Rate - {platform.capitalize()}')
        else:
            sns.lineplot(data=df, x='timestamp', y='engagement_rate', hue='platform')
            plt.title('Engagement Rate - All Platforms')
            
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        return base64.b64encode(buf.read()).decode('utf-8')