import tweepy
import facebook
from instagram_private_api import Client as InstagramAPI
from linkedin_v2 import linkedin as LinkedInAPI
from config import Config
from datetime import datetime
import logging
import json
import os

logger = logging.getLogger(__name__)

class PlatformIntegration:
    def __init__(self):
        self.twitter_api = self._init_twitter()
        self.facebook_api = self._init_facebook()
        self.instagram_api = self._init_instagram()
        self.linkedin_api = self._init_linkedin()

    def _init_twitter(self):
        try:
            auth = tweepy.OAuthHandler(
                Config.TWITTER_API_KEY,
                Config.TWITTER_API_SECRET
            )
            return tweepy.API(auth)
        except Exception as e:
            logger.error(f"Twitter init failed: {e}")
            return None

    def _init_facebook(self):
        try:
            if not Config.FACEBOOK_ACCESS_TOKEN:
                raise ValueError("Facebook access token missing")
            return facebook.GraphAPI(Config.FACEBOOK_ACCESS_TOKEN)
        except Exception as e:
            logger.error(f"Facebook init failed: {e}")
            return None

    def _init_instagram(self):
        try:
            # Try to load cached session
            cache_file = 'instagram_session.json'
            if os.path.exists(cache_file):
                with open(cache_file) as file_data:
                    cached = json.load(file_data)
                    return InstagramAPI(
                        Config.INSTAGRAM_USERNAME,
                        Config.INSTAGRAM_PASSWORD,
                        settings=cached
                    )
            
            # New login
            api = InstagramAPI(
                Config.INSTAGRAM_USERNAME,
                Config.INSTAGRAM_PASSWORD,
                on_login=lambda x: self._cache_instagram_session(x)
            )
            return api
        except Exception as e:
            logger.error(f"Instagram init failed: {e}")
            return None

    def _cache_instagram_session(self, session):
        with open('instagram_session.json', 'w') as f:
            json.dump(session, f)

    def _init_linkedin(self):
        try:
            if not Config.LINKEDIN_ACCESS_TOKEN:
                raise ValueError("LinkedIn access token missing")
            return LinkedInAPI(
                Config.LINKEDIN_CLIENT_ID,
                Config.LINKEDIN_CLIENT_SECRET,
                access_token=Config.LINKEDIN_ACCESS_TOKEN
            )
        except Exception as e:
            logger.warning(f"LinkedIn init failed (will skip LinkedIn posts): {e}")
            return None

    def post_content(self, platform, content):
        try:
            if platform == 'twitter':
                return self._post_to_twitter(content)
            elif platform == 'facebook':
                return self._post_to_facebook(content)
            elif platform == 'instagram':
                return self._post_to_instagram(content)
            elif platform == 'linkedin' and self.linkedin_api:
                return self._post_to_linkedin(content)
            else:
                raise ValueError(f"Unsupported platform: {platform}")
        except Exception as e:
            logger.error(f"Failed to post to {platform}: {e}")
            raise

    def _post_to_twitter(self, content):
        if not self.twitter_api:
            raise Exception("Twitter API not initialized")
        
        if len(content) > 280:
            content = content[:277] + '...'
            
        tweet = self.twitter_api.update_status(content)
        return {
            'tweet_id': tweet.id_str,
            'created_at': tweet.created_at.isoformat()
        }

    def _post_to_facebook(self, content):
        if not self.facebook_api:
            raise Exception("Facebook API not initialized")
            
        post = self.facebook_api.put_object(
            parent_object='me',
            connection_name='feed',
            message=content
        )
        return {
            'post_id': post['id'],
            'created_time': post.get('created_time', '')
        }

    def _post_to_instagram(self, content):
        if not self.instagram_api:
            raise Exception("Instagram API not initialized")
            
        # Simplified text post (requires media for real posts)
        result = self.instagram_api.post_photo(
            photo_data=b'',  # Replace with actual image bytes
            caption=content[:2200]
        )
        return {
            'media_id': result.get('id', ''),
            'timestamp': str(datetime.now())
        }

    def _post_to_linkedin(self, content):
        if not self.linkedin_api:
            raise Exception("LinkedIn API not initialized")
            
        # Note: Requires OAuth2 token first
        post = self.linkedin_api.submit_share(
            comment=content[:1300],
            visibility_code='anyone'
        )
        return {
            'post_id': post.get('updateKey', ''),
            'timestamp': str(datetime.now())
        }