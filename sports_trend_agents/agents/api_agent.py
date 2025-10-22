# agents/api_agent.py - QUERY-AWARE VERSION

import feedparser
import requests
import logging
from .utils import TrendResult

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def fetch_sports_trend(query=""):
    """
    Fetch sports trends from multiple sources based on user query.
    Now supports sport-specific feeds!
    """
    logger.info(f"🚀 Starting BULLETPROOF sports trend fetch with query: '{query}'")
    
    # Detect which sport the user is asking about
    query_lower = query.lower()
    
    # Sport-specific ESPN RSS feeds
    sport_feeds = {
        'nba': {
            'keywords': ['nba', 'basketball', 'lakers', 'warriors', 'celtics', 'nets', 'bucks'],
            'feed': 'http://www.espn.com/espn/rss/nba/news',
            'name': 'ESPN NBA'
        },
        'nfl': {
            'keywords': ['nfl', 'football', 'patriots', 'cowboys', 'eagles', 'chiefs', 'packers'],
            'feed': 'http://www.espn.com/espn/rss/nfl/news',
            'name': 'ESPN NFL'
        },
        'mlb': {
            'keywords': ['mlb', 'baseball', 'yankees', 'red sox', 'dodgers', 'cubs', 'mets'],
            'feed': 'http://www.espn.com/espn/rss/mlb/news',
            'name': 'ESPN MLB'
        },
        'soccer': {
            'keywords': ['soccer', 'football', 'premier league', 'messi', 'ronaldo', 'uefa', 'fifa'],
            'feed': 'http://www.espn.com/espn/rss/soccer/news',
            'name': 'ESPN Soccer'
        },
        'nhl': {
            'keywords': ['nhl', 'hockey', 'bruins', 'maple leafs', 'canadiens', 'rangers'],
            'feed': 'http://www.espn.com/espn/rss/nhl/news',
            'name': 'ESPN NHL'
        }
    }
    
    # Try to match query to a specific sport
    selected_feed = None
    selected_name = None
    
    for sport, data in sport_feeds.items():
        if any(keyword in query_lower for keyword in data['keywords']):
            selected_feed = data['feed']
            selected_name = data['name']
            logger.info(f"🎯 Detected sport: {sport.upper()} - Using {selected_name}")
            break
    
    # If no specific sport detected, use top headlines
    if not selected_feed:
        selected_feed = 'http://www.espn.com/espn/rss/news'
        selected_name = 'ESPN Top Headlines'
        logger.info("📰 Using ESPN Top Headlines (no specific sport detected)")
    
    # ==== ESPN RSS FEED (Sport-specific or Top Headlines) ====
    logger.info(f"📡 Fetching from {selected_name}...")
    
    try:
        logger.info(f"🔍 Trying: {selected_name}")
        feed = feedparser.parse(selected_feed)
        
        if feed.entries:
            entry = feed.entries[0]
            
            title = entry.get('title', 'No title')
            summary = entry.get('summary', 'No summary available')
            link = entry.get('link', '')
            published = entry.get('published', 'Unknown date')
            
            logger.info(f"✅ SUCCESS from {selected_name}: {title}")
            
            return TrendResult(
                title=title,
                summary=summary,
                impact=f"From {selected_name} - Published {published}"
            )
        else:
            logger.warning(f"⚠️ No entries found in {selected_name}")
    except Exception as e:
        logger.error(f"❌ Error fetching from {selected_name}: {str(e)}")
    
    # ==== BBC SPORT RSS (Fallback) ====
    logger.info("📡 Trying BBC Sport as fallback...")
    
    try:
        bbc_feed = 'http://feeds.bbci.co.uk/sport/rss.xml'
        feed = feedparser.parse(bbc_feed)
        
        if feed.entries:
            entry = feed.entries[0]
            
            title = entry.get('title', 'No title')
            summary = entry.get('summary', 'No summary available')
            published = entry.get('published', 'Unknown date')
            
            logger.info(f"✅ SUCCESS from BBC Sport: {title}")
            
            return TrendResult(
                title=title,
                summary=summary,
                impact=f"From BBC Sport - Published {published}"
            )
    except Exception as e:
        logger.error(f"❌ Error fetching from BBC Sport: {str(e)}")
    
    # ==== REDDIT SPORTS (Final Fallback) ====
    logger.info("📡 Trying Reddit r/sports as final fallback...")
    
    try:
        reddit_url = 'https://www.reddit.com/r/sports/top.json?limit=5'
        headers = {'User-Agent': 'Sports Trend Agent/1.0'}
        
        response = requests.get(reddit_url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            
            if data.get('data', {}).get('children'):
                post = data['data']['children'][0]['data']
                
                title = post.get('title', 'No title')
                selftext = post.get('selftext', '')
                score = post.get('score', 0)
                
                summary = selftext[:200] + "..." if len(selftext) > 200 else selftext
                if not summary:
                    summary = f"Trending post with {score} upvotes"
                
                logger.info(f"✅ SUCCESS from Reddit: {title}")
                
                return TrendResult(
                    title=title,
                    summary=summary,
                    impact=f"From Reddit r/sports - {score} upvotes"
                )
    except Exception as e:
        logger.error(f"❌ Error fetching from Reddit: {str(e)}")
    
    # ==== ALL FAILED ====
    logger.error("❌ All API sources failed!")
    return None