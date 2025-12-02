import json
import random
import datetime

def run():
    """
    JRAVIS Worker — Stream 4
    Task: YouTube Automation (Faceless + Shorts Scripts)
    Output: JSON
    """

    # Possible niches for the YouTube channel
    niches = [
        "Motivation",
        "AI Tools",
        "Money Making Tips",
        "Business Lessons",
        "Productivity Hacks",
        "Tech Explainers",
        "Psychology Facts",
        "Career Growth",
        "Healthy Habits",
        "Self Improvement"
    ]

    # Hook templates for viral shorts
    hook_templates = [
        "Most people don't know this about {topic}...",
        "The secret to {topic} is easier than you think.",
        "Stop scrolling! Here's the truth about {topic}.",
        "You’re doing {topic} wrong. Here's why...",
        "3 things nobody tells you about {topic}.",
        "This will change how you think about {topic} forever.",
        "If you want to improve your {topic}, watch this.",
    ]

    # Video CTA choices
    ctas = [
        "Follow for more life-changing tips!",
        "Subscribe for daily motivation!",
        "Share this with someone who needs this.",
        "Save this for later!",
        "Comment 'YES' if you want part 2!"
    ]

    topic = random.choice(niches)
    hook = random.choice(hook_templates).format(topic=topic.lower())
    cta = random.choice(ctas)

    # Script generation
    script = f"""
    HOOK: {hook}

    VALUE:
    1. {topic} tip #1 explained in simple words.
    2. {topic} tip #2 with a relatable example.
    3. Final insight that delivers emotional impact.

    CTA: {cta}
    """.strip()

    # Thumbnail ideas
    thumbnails = [
        f"Bold text: '{topic.upper()} SECRET' + shocked emoji",
        f"Minimal layout with big bold hook: '{topic} Hack'",
        f"Character reaction + keywords related to {topic}",
    ]

    # SEO metadata
    title = f"{topic} Tips You Never Heard Before"
    description = (
        f"This YouTube Short reveals powerful insights about {topic.lower()}. "
        "Subscribe for daily motivational and productivity videos."
    )

    hashtags = [
        f"#{topic.replace(' ', '')}",
        "#motivation", "#lifehacks", "#productivity", "#selfimprovement"
    ]

    output = {
        "stream": "youtube_automation",
        "status": "completed",
        "topic": topic,
        "script": script,
        "title": title,
        "description": description,
        "thumbnails": thumbnails,
        "hashtags": hashtags,
        "cta": cta,
        "mode": "hybrid",
        "note": (
            "JRAVIS generated the Short script & metadata. "
            "Manual step: Convert script to video using your video tool "
            "(CapCut/VEED/etc) or integrate YouTube API in Phase 2."
        ),
        "timestamp": str(datetime.datetime.utcnow())
    }

    print(json.dumps(output, indent=4))
  
