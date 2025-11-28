import json
import random
import datetime

def run():
    """
    JRAVIS Worker — Stream 6
    Task: Amazon KDP Book Content Generator (Hybrid Automation)
    Output: JSON
    """

    # High-demand KDP niches
    niches = [
        "Self Improvement",
        "Motivation",
        "Personal Finance",
        "Mental Health",
        "Productivity",
        "Fitness & Wellness",
        "Business & Entrepreneurship",
        "Relationships",
        "Career Growth",
        "Young Adult Fiction"
    ]

    title_templates = [
        "The {topic} Blueprint",
        "Mastering Your {topic}",
        "The Ultimate Guide to {topic}",
        "{topic}: A New Approach",
        "Unlocking Your {topic}",
        "The Psychology of {topic}",
        "Daily Habits for Better {topic}",
    ]

    chapter_templates = [
        "Understanding the Basics of {topic}",
        "Why {topic} Matters More Today",
        "Common Mistakes People Make in {topic}",
        "The Step-by-Step Framework to Improve {topic}",
        "Tools, Mindsets, and Techniques for {topic}",
        "Real Stories and Examples of {topic} Success",
        "Long-Term Growth & Future of {topic}",
    ]

    topic = random.choice(niches)
    title = random.choice(title_templates).format(topic=topic)
    
    # Description generation
    description = (
        f"This book explores powerful insights about {topic.lower()}, "
        "offering practical strategies and real-life examples. "
        "It provides a step-by-step blueprint that readers can apply immediately."
    )

    # Generate 7 chapters
    chapters = [
        chapter_templates[i].format(topic=topic)
        for i in range(len(chapter_templates))
    ]

    # Sample content for chapter 1
    sample_chapter = (
        f"Chapter 1: {chapters[0]}\n\n"
        f"In this chapter, we explore the foundations of {topic.lower()}, "
        "why it matters, and how you can start applying these principles today. "
        "The goal is to provide a simple, relatable, and actionable introduction."
    )

    # KDP keywords
    keywords = [
        f"{topic.lower()} book",
        f"how to improve {topic.lower()}",
        f"{topic.lower()} tips",
        f"{topic.lower()} guide",
        f"{topic.lower()} motivation"
    ]

    # Cover prompt for AI generator
    cover_prompt = (
        f"A clean minimal book cover for a book titled '{title}', "
        f"theme: {topic.lower()}, soft colors, modern typography."
    )

    output = {
        "stream": "kdp_books",
        "status": "completed",
        "title": title,
        "topic": topic,
        "description": description,
        "chapters": chapters,
        "sample_chapter": sample_chapter,
        "keywords": keywords,
        "cover_prompt": cover_prompt,
        "mode": "hybrid",
        "note": (
            "JRAVIS generated full book structure & content. "
            "Manual Step: Convert text to formatted PDF + generate cover, "
            "upload to Amazon KDP dashboard."
        ),
        "timestamp": str(datetime.datetime.utcnow())
    }

    print(json.dumps(output, indent=4))
