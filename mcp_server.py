#!/usr/bin/env python3
import json
import sys
from client import AgenticColdOutreachDeliverabilityGuard

def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        guard = AgenticColdOutreachDeliverabilityGuard()
        subj = "Brief idea on AI customer routing for Acme"
        body = "Hi Alex, noticed your team scaling the support fleet. We built an open MCP server that automates triage. Would love your feedback. Reply stop to unsubscribe."
        res = guard.evaluate_email_deliverability(subj, body)
        assert res["composite_spam_score"] < 2.5
        assert res["deliverability_tier"] == "PRIMARY_INBOX_OPTIMAL"
        print(f"[TEST PASS] Deliverability Score: {res['composite_spam_score']}/10")
        sys.exit(0)

    for line in sys.stdin:
        if not line.strip():
            continue
        try:
            req = json.loads(line)
            method = req.get("method")
            msg_id = req.get("id")
            if method == "initialize":
                print(json.dumps({"jsonrpc": "2.0", "id": msg_id, "result": {"serverInfo": {"name": "genpark-cold-email-guard", "version": "1.0.0"}}}))
            elif method == "tools/list":
                print(json.dumps({"jsonrpc": "2.0", "id": msg_id, "result": {"tools": [{"name": "evaluate_email_deliverability", "description": "Evaluate cold outreach email for spam score and inbox placement"}]}}))
            elif method == "tools/call":
                args = req.get("params", {}).get("arguments", {})
                guard = AgenticColdOutreachDeliverabilityGuard()
                out = guard.evaluate_email_deliverability(args.get("subject", ""), args.get("body", ""), args.get("sender_domain", "acme.io"))
                print(json.dumps({"jsonrpc": "2.0", "id": msg_id, "result": {"content": [{"type": "text", "text": json.dumps(out)}]}}))
            else:
                print(json.dumps({"jsonrpc": "2.0", "id": msg_id, "error": {"code": -32601, "message": "Method not found"}}))
            sys.stdout.flush()
        except Exception as e:
            print(json.dumps({"jsonrpc": "2.0", "error": {"code": -32603, "message": str(e)}}))
            sys.stdout.flush()

if __name__ == "__main__":
    main()
