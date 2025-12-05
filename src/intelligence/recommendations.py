import datetime, json, os
RECOMMEND_FILE = "data/intelligence/recommendations_history.json"

class Recommendations:
    def __init__(self):
        os.makedirs("data/intelligence", exist_ok=True)

    def _load(self):
        if not os.path.exists(RECOMMEND_FILE):
            return []
        return json.load(open(RECOMMEND_FILE))

    def _save(self, data):
        json.dump(data, open(RECOMMEND_FILE, "w"), indent=2)

    def generate(self, growth_data):
        top_stream = growth_data["top_stream"]

        suggestions = {
            "auto_blogging": "Increase SEO pages, target long-tail keywords.",
            "affiliate": "Push new funnels, add fresh reviewed content.",
            "dropshipping": "Scale winning product variations.",
            "pod": "Publish 100 new designs daily.",
            "templates": "Launch 20 new templates.",
            "newsletter": "Grow subscribers through lead magnets.",
            "micro_saas": "Add new features with JRAVIS engine.",
            "marketplaces": "Expand digital listings across platforms."
        }

        rec = {
            "date": datetime.date.today().isoformat(),
            "priority_stream": top_stream,
            "action": suggestions.get(top_stream, "Scale operations.")
        }

        history = self._load()
        history.append(rec)
        self._save(history[-90:])

        return { "today": rec, "history": history }
