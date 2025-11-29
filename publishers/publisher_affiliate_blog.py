import openai

def publish_affiliate_blog(task):
    print("📝 Creating SEO affiliate article...")

    prompt = "Write a 400 word SEO affiliate article about a trending product."

    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    text = response.choices[0].message.content

    print("✍ Article Generated:")
    print(text[:200], "...")  # preview
    print("✔ Article ready for publishing (manual upload).")
    
