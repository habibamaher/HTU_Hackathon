# agents/views.py - SIMPLE VERSION THAT WORKS

from django.shortcuts import render
import feedparser
from dataclasses import dataclass

@dataclass
class TrendResult:
    title: str
    summary: str
    impact: str

def home(request):
    report = None
    
    if request.method == "POST":
        query = request.POST.get("prompt", "latest sports news")
        
        try:
            # Simple ESPN fetch
            query_lower = query.lower()
            
            # Pick the right ESPN feed
            if any(word in query_lower for word in ['nba', 'basketball', 'lakers', 'warriors']):
                feed_url = 'http://www.espn.com/espn/rss/nba/news'
                feed_name = 'ESPN NBA'
            elif any(word in query_lower for word in ['nfl', 'football', 'patriots', 'cowboys']):
                feed_url = 'http://www.espn.com/espn/rss/nfl/news'
                feed_name = 'ESPN NFL'
            elif any(word in query_lower for word in ['mlb', 'baseball', 'yankees', 'dodgers']):
                feed_url = 'http://www.espn.com/espn/rss/mlb/news'
                feed_name = 'ESPN MLB'
            elif any(word in query_lower for word in ['soccer', 'messi', 'ronaldo']):
                feed_url = 'http://www.espn.com/espn/rss/soccer/news'
                feed_name = 'ESPN Soccer'
            elif any(word in query_lower for word in ['nhl', 'hockey', 'bruins']):
                feed_url = 'http://www.espn.com/espn/rss/nhl/news'
                feed_name = 'ESPN NHL'
            else:
                feed_url = 'http://www.espn.com/espn/rss/news'
                feed_name = 'ESPN Top Headlines'
            
            # Fetch from ESPN
            feed = feedparser.parse(feed_url)
            
            if feed.entries:
                entry = feed.entries[0]
                title = entry.get('title', 'No title')
                summary = entry.get('summary', 'No summary available')
                published = entry.get('published', 'Unknown date')
                
                # Format nicely
                report = f"""
                <div style="line-height: 1.8;">
                    <strong style="font-size: 18px; display: block; margin-bottom: 12px;">{title}</strong>
                    <p style="margin-bottom: 10px; font-size: 15px;">{summary}</p>
                    <p style="font-size: 13px; color: #999; font-style: italic;">From {feed_name} - {published}</p>
                </div>
                """
            else:
                report = "<p>No sports news available at the moment. Please try again.</p>"
                
        except Exception as e:
            report = f"<p>Error fetching news: {str(e)}</p>"
    
    return render(request, "index.html", {
        "report": report,
        "fallback": False,
        "gemini_used": False,
        "retriever_used": False,
        "total_queries": 0,
    })