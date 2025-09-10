# report.py
import datetime

def generate_report(mode, target, method="overwrite", verified=True):
    """
    Creates a structured report after wiping.
    """
    report = {
        "timestamp": str(datetime.datetime.now()),
        "mode": mode,
        "target": target,
        "method": method,
        "verified": verified
    }
    print("Generated Report:", report)
    return report
