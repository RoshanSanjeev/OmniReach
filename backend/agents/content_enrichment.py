# backend/agents/content_enrichment_agent.py

from typing import Dict, List
import random

# Sample CTA phrases and templates
CTA_PHRASES = [
    "Tap to explore!",
    "See more inside!",
    "Unleash performance.",
    "Ride into style.",
    "Click to learn more!",
    "Tap to reveal!"
]

HASHTAG_POOL = [
    # Luxury Cars
    "#luxurycars", "#supercars", "#exoticcars", "#luxuryride", "#bmwlife",
    "#mercedesbenz", "#ferrarilifestyle", "#lamborghini", "#bentleymotors",
    "#rollsroyce", "#mclaren", "#maserati", "#porschelife", "#drivestyle",
    "#executivestyle", "#carluxury", "#carswithoutlimits", "#autoluxury",
    "#luxurylifestylecars", "#fastlife",

    # Luxury Travel
    "#luxurytravel", "#luxuryvacation", "#travelinstyle", "#privatejetlife",
    "#firstclasslife", "#5starhotel", "#overwaterbungalow", "#luxgetaway",
    "#jetsetter", "#resortlife", "#passportready", "#travelgoals",
    "#dreamvacation", "#luxurydestination", "#travelinspo", "#hiddenluxury",
    "#luxuryescapes", "#wanderlux", "#travelluxury", "#viptravel",

    # Luxury Perfumes & Beauty
    "#luxuryfragrance", "#nicheperfume", "#fragranceaddict", "#scentoftheday",
    "#luxuryscent", "#oudperfume", "#perfumecollector", "#roja",
    "#creedaventus", "#tomfordbeauty", "#maisonfrancis", "#parfumdeluxe",
    "#highendbeauty", "#fragrancelovers", "#luxbeauty", "#exclusivescent",
    "#elegantscent", "#perfumeobsessed", "#designerfragrance",
    "#fragrancelife",

    # Luxury Restaurants & Dining
    "#luxurydining", "#michelinstar", "#finecuisine", "#gourmetlife",
    "#chefspecial", "#eatingwithstyle", "#culinaryart", "#finewine",
    "#exclusiveeats", "#dineinstyle", "#finediningexperience", "#gastrojourney",
    "#luxuryrestaurant", "#cheflife", "#privatechef", "#wineanddine",
    "#tableforvip", "#gastronomy", "#tastetheluxury", "#luxfoodie"
]

def generate_caption(creator_handle: str, campaign_name: str, matched_hashtags: List[str]) -> str:
    base_caption = f"{creator_handle} just dropped a fresh take on {campaign_name}!"
    hashtags = " ".join(matched_hashtags[:2])
    cta = random.choice(CTA_PHRASES)
    return f"{base_caption} {cta} {hashtags}"

def enrich_video_data(video: Dict, campaign_name: str) -> Dict:
    enriched = video.copy()
    enriched["caption"] = generate_caption(
        creator_handle=video.get("creator", {}).get("username", "@creator"),
        campaign_name=campaign_name,
        matched_hashtags=video.get("matched_hashtags", [])
    )

    # Add or expand hashtags
    existing_tags = set(video.get("matched_hashtags", []))
    additional_tags = list(set(HASHTAG_POOL) - existing_tags)
    random.shuffle(additional_tags)
    enriched["final_hashtags"] = list(existing_tags) + additional_tags[:2]
    return enriched

def enrich_campaign_videos(videos: List[Dict], campaign_name: str) -> List[Dict]:
    return [enrich_video_data(video, campaign_name) for video in videos]

# Example usage
if __name__ == "__main__":
    test_video = {
        "video_url": "https://tiktok.com/@bmwfan/video/123",
        "creator": {"username": "@bmwfan"},
        "matched_hashtags": ["#luxury", "#bmw"]
    }
    enriched = enrich_video_data(test_video, "BMW Summer Drive")
    print(enriched)
