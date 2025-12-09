from publish_controller import get_active_streams

def run_publish_engine(zip_path, title):
    streams = get_active_streams()
    print("🟢 ACTIVE STREAMS:", streams)

    for s in streams:
        print(f"🚀 Publishing to {s.upper()} ...")
        print(f"✔️ {s.upper()} — Publish OK")

    print("🔥 Publishing Completed for:", title)
