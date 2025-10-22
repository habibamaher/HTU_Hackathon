# agents/retriever_agent.py - QUERY-AWARE VERSION

from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from .utils import TrendResult
import os

# Path to ChromaDB storage
CHROMA_PATH = "./chroma_sports"

def retrieve_sports_trend(query="latest sports news"):
    """
    Retrieve relevant sports trends from ChromaDB based on query.
    Now accepts query parameter for better matching!
    """
    try:
        # Initialize embeddings
        embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
        
        # Load existing ChromaDB
        if os.path.exists(CHROMA_PATH):
            vectorstore = Chroma(
                persist_directory=CHROMA_PATH,
                embedding_function=embeddings,
                collection_name="sports_trends"
            )
            
            # Search for relevant trends using the query
            results = vectorstore.similarity_search(query, k=1)
            
            if results:
                doc = results[0]
                metadata = doc.metadata
                
                return TrendResult(
                    title=metadata.get("title", "Sports Trend"),
                    summary=doc.page_content,
                    impact=metadata.get("impact", "Retrieved from local database")
                )
        
        return None
        
    except Exception as e:
        print(f"❌ Retriever error: {str(e)}")
        return None


def initialize_sports_knowledge_base():
    """
    Initialize ChromaDB with pre-loaded sports trends.
    This is a one-time setup function.
    """
    try:
        # Initialize embeddings
        embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
        
        # Sample sports trends
        sports_trends = [
            {
                "title": "NBA Playoff Race Intensifies",
                "content": "The race for playoff spots in both conferences is heating up as teams battle for positioning with just weeks remaining in the regular season.",
                "impact": "Multiple teams within striking distance of playoff berths"
            },
            {
                "title": "NFL Draft Prospects to Watch",
                "content": "Top college football players are showcasing their skills at various pro days and the NFL Combine, impacting their draft stock.",
                "impact": "Teams evaluating talent for upcoming draft"
            },
            {
                "title": "Soccer Transfer Window Activity",
                "content": "Major European clubs are making significant moves in the transfer market, with several high-profile players changing teams.",
                "impact": "Reshaping team dynamics across leagues"
            },
            {
                "title": "MLB Spring Training Highlights",
                "content": "Teams are preparing for the upcoming season with rookies and veterans competing for roster spots in spring training.",
                "impact": "Setting the stage for the new season"
            },
            {
                "title": "Tennis Grand Slam Preparations",
                "content": "Top-ranked players are fine-tuning their games ahead of the next Grand Slam tournament with strong performances in lead-up events.",
                "impact": "Building momentum for major championships"
            },
            {
                "title": "NHL Stanley Cup Playoff Picture",
                "content": "Hockey teams are jockeying for position as the regular season winds down and playoff matchups begin to take shape.",
                "impact": "Intense competition for championship opportunity"
            },
            {
                "title": "Olympic Athletes Training Updates",
                "content": "Athletes are ramping up their training regimens in preparation for the upcoming Olympic Games.",
                "impact": "Nations competing for medal counts"
            },
            {
                "title": "College Basketball March Madness",
                "content": "NCAA tournament brackets are being filled as conference champions are crowned and at-large bids are determined.",
                "impact": "Excitement building for the tournament"
            }
        ]
        
        # Create ChromaDB
        texts = [trend["content"] for trend in sports_trends]
        metadatas = [
            {
                "title": trend["title"],
                "impact": trend["impact"]
            }
            for trend in sports_trends
        ]
        
        # Create vector store
        vectorstore = Chroma.from_texts(
            texts=texts,
            embedding=embeddings,
            metadatas=metadatas,
            persist_directory=CHROMA_PATH,
            collection_name="sports_trends"
        )
        
        print(f"✅ ChromaDB initialized with {len(sports_trends)} sports trends")
        return vectorstore
        
    except Exception as e:
        print(f"❌ Error initializing ChromaDB: {str(e)}")
        return None


# Initialize database if it doesn't exist
if not os.path.exists(CHROMA_PATH):
    print("🔄 Initializing ChromaDB for the first time...")
    initialize_sports_knowledge_base()