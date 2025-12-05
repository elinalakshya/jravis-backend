import os, json, datetime
import matplotlib.pyplot as plt

class WeeklySummary:
    def __init__(self):
        os.makedirs("output/reports/weekly", exist_ok=True)
        os.makedirs("data/intelligence/weekly_reports", exist_ok=True)

    def generate(self, revenue_history):
        # Check if charts possible
        real_values = [h["total"] for h in revenue_history[-7:] if h["total"] > 0]

        chart_path = None

        if len(real_values) >= 3:
            plt.figure(figsize=(8,4))
            plt.plot(real_values)
            plt.title("Weekly Revenue Trend")
            plt.grid(True)

            chart_path = f"output/reports/weekly/chart_{datetime.date.today()}.png"
            plt.savefig(chart_path)
            plt.close()

        summary = {
            "week_total": sum(real_values),
            "average_daily": sum(real_values) / len(real_values) if real_values else 0,
            "chart": chart_path
        }

        # Save both locations
        json.dump(summary, open(f"output/reports/weekly/{datetime.date.today()}.json", "w"), indent=2)
        json.dump(summary, open(f"data/intelligence/weekly_reports/{datetime.date.today()}.json", "w"), indent=2)

        return summary
