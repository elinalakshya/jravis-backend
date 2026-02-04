from jobs.pod_job import run_pod
from jobs.gumroad_job import run_gumroad
from jobs.payhip_job import run_payhip


def run_factory():
    print("🚀 JRAVIS PHASE-1 FACTORY STARTED")

    # ⭐ PHASE 1 VOLUME
    run_pod(50)        # 50 Printify POD
    run_gumroad(20)    # 20 Gumroad
    run_payhip(20)     # 20 Payhip

    print("✅ DAILY FACTORY COMPLETED")


if __name__ == "__main__":
    run_factory()
