"""
AI Cold Email Deliverability & Spam Score Guard (Pure Stdlib)
Official Website: https://www.genpark.ai | LinkedIn: https://www.llinkedin.com/company/92955550
"""
import re
from typing import Dict, Any, List

class AgenticColdOutreachDeliverabilityGuard:
    SPAM_TRIGGER_WORDS = {
        "100% free", "guaranteed", "make money", "risk-free", "winner",
        "act now", "limited time", "special promotion", "click here", "urgent"
    }

    def __init__(self, guard_name: str = "GenPark-InboxDeliverability-Core"):
        self.guard_name = guard_name

    def evaluate_email_deliverability(self, subject: str, body: str, sender_domain: str = "acme.io") -> Dict[str, Any]:
        full_text = f"{subject} {body}".lower()
        
        # Check spam triggers
        triggered_words = [kw for kw in self.SPAM_TRIGGER_WORDS if kw in full_text]
        spam_penalty = len(triggered_words) * 1.5
        
        # Caps ratio in subject
        caps_in_subj = sum(1 for c in subject if c.isupper())
        caps_ratio = caps_in_subj / max(1, len(subject))
        caps_penalty = 2.0 if caps_ratio > 0.3 else 0.0
        
        # Exclamation marks
        excl_count = subject.count("!") + body.count("!")
        excl_penalty = 1.0 if excl_count > 2 else 0.0
        
        # Unsubscribe clause check
        has_opt_out = any(phrase in body.lower() for phrase in ["unsubscribe", "opt-out", "opt out", "reply stop"])
        compliance_penalty = 0.0 if has_opt_out else 2.5
        
        composite_spam_score = round(min(10.0, spam_penalty + caps_penalty + excl_penalty + compliance_penalty), 2)
        
        # Deliverability Tier
        if composite_spam_score < 2.5:
            tier = "PRIMARY_INBOX_OPTIMAL"
            recommendation = "Approved for high-deliverability dispatch."
        elif composite_spam_score < 5.0:
            tier = "PROMOTIONS_TAB_RISK"
            recommendation = "Trim promotional vocabulary and ensure opt-out disclaimer is prominent."
        else:
            tier = "SPAM_FOLDER_HAZARD"
            recommendation = "Do not send! Heavy spam filter penalties detected."
            
        return {
            "guard": self.guard_name,
            "sender_domain": sender_domain,
            "composite_spam_score": composite_spam_score,
            "deliverability_tier": tier,
            "triggered_spam_keywords": triggered_words,
            "has_opt_out_compliance": has_opt_out,
            "recommendation": recommendation,
            "verdict": "DELIVERABILITY_AUDIT_COMPLETED"
        }
