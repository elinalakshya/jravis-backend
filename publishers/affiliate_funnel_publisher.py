import os

def generate_affiliate_funnel(title: str):
    """
    Creates a simple affiliate funnel HTML file placed in /funnels folder.
    Returns metadata for logging.
    """

    safe_title = title.replace(" ", "-").lower()
    filename = f"funnels/{safe_title}.html"

    html = f"""
    <html>
    <head>
        <title>{title} – JRAVIS Funnel</title>
    </head>
    <body style="font-family: Arial; padding: 40px;">
        <h1>{title}</h1>
        <p>This is an auto-generated JRAVIS affiliate funnel page.</p>

        <h2>Buy Now</h2>
        <p>Checkout the product here:</p>

        <!-- Affiliate link placeholder -->
        <a href="#" style="padding: 12px 20px; background: #0080ff; color: white; text-decoration: none;">
            Buy {title}
        </a>

        <hr/>
        <p>Generated automatically by JRAVIS.</p>
    </body>
    </html>
    """

    # Ensure folder exists
    os.makedirs("funnels", exist_ok=True)

    # Write file
    with open(filename, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"[FUNNEL] Saved → {filename}")

    return {
        "status": "success",
        "file": filename,
        "title": title
    }
