from client import AgenticColdOutreachDeliverabilityGuard

def main():
    guard = AgenticColdOutreachDeliverabilityGuard()
    s = "ACT NOW! 100% FREE GROWTH TOOL!!!"
    b = "Click here to make money guaranteed! Limited time special promotion!"
    res = guard.evaluate_email_deliverability(s, b)
    print("--- Email Deliverability Audit ---")
    print(f"Spam Score: {res['composite_spam_score']}/10 | Tier: {res['deliverability_tier']}")
    print(f"Flags: {res['triggered_spam_keywords']}")
    print(f"Recommendation: {res['recommendation']}")

if __name__ == "__main__":
    main()
