from jobs.pod_job import run_pod
from jobs.gumroad_job import run_gumroad
from jobs.payhip_job import run_payhip
from jobs.shopify_job import run_shopify

def run_factory():
    run_pod(20)
    run_gumroad(10)
    run_payhip(10)
    # run_shopify(10)   # disabled for now
    print("✅ DAILY FACTORY COMPLETED")

if __name__ == "__main__":
    run_factory()
