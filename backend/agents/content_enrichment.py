# backend/agents/content_enrichment_agent.py

from typing import Dict, List
import random
from crewai import Agent
from backend.services.masumi_transaction import (
    verify_nft_ownership,
    check_payment_status,
    initiate_payment
)

# 🧠 CrewAI Agent definition
content_enrichment_agent = Agent(
    name="ContentEnricher",
    role="Enhances video content for luxury campaigns",
    goal="Generate engaging captions and optimized hashtags for each campaign video",
    backstory="This agent crafts high-performing campaign assets by analyzing creator context and aligning messaging with luxury brand goals.",
    verbose=True
)

# Sample CTA phrases and templates
CTA_PHRASES = [
    "Tap to explore!",
    "See more inside!",
    "Limited time luxury.",
    "Unleash performance.",
    "Ride into style."
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

# ✅ Enrichment flow that also checks Masumi access
async def enrich_video_data(video: Dict, campaign_name: str, wallet: str, collection: str) -> Dict:
    enriched = video.copy()

    # Step 1: Access gating check
    access = await verify_nft_ownership(wallet, collection)
    if not access.get("has_access"):
        return {
            "wallet": wallet,
            "access": False,
            "reason": "NFT not owned"
        }

    payment = await check_payment_status(wallet)
    if payment.get("status") != "paid":
        tx = await initiate_payment(wallet)
        return {
            "wallet": wallet,
            "access": False,
            "reason": "Payment not completed",
            "next_step": "pay-to-unlock",
            "tx_link": tx.get("tx_link")
        }

    # Step 2: Enrich the content
    base_caption = f"{video.get('creator', {}).get('username', '@creator')} just dropped a fresh take on {campaign_name}!"
    cta = random.choice(CTA_PHRASES)
    hashtags = video.get("matched_hashtags", [])
    enriched["caption"] = f"{base_caption} {cta} {' '.join(hashtags[:2])}"

    # Hashtag expansion
    existing_tags = set(hashtags)
    additional_tags = list(set(HASHTAG_POOL) - existing_tags)
    random.shuffle(additional_tags)
    enriched["final_hashtags"] = list(existing_tags) + additional_tags[:2]
    enriched["access"] = True
    enriched["wallet"] = wallet
    return enriched

async def enrich_campaign_videos(videos: List[Dict], campaign_name: str, wallet: str, collection: str) -> List[Dict]:
    enriched = []
    for video in videos:
        result = await enrich_video_data(video, campaign_name, wallet, collection)
        enriched.append(result)
    return enriched