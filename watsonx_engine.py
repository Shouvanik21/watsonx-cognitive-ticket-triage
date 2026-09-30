import sys
import os
import json
import re
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("WATSONX_APIKEY")
PROJECT_ID = os.getenv("WATSONX_PROJECT_ID")
URL = os.getenv("WATSONX_URL", "https://us-south.ml.cloud.ibm.com")


def analyze_ticket_with_watsonx(ticket_text: str) -> dict:
    if not API_KEY or not PROJECT_ID:
        return _mock_watsonx_analysis(ticket_text)

    try:
        from ibm_watsonx_ai.foundation_models import ModelInference
        from ibm_watsonx_ai.metanames import GenTextParamsMetaNames as GenParams

        parameters = {
            GenParams.MAX_NEW_TOKENS: 400,
            GenParams.TEMPERATURE: 0.1,
        }

        model = ModelInference(
            model_id="ibm/granite-13b-chat-v2",
            params=parameters,
            credentials={"url": URL, "apikey": API_KEY},
            project_id=PROJECT_ID,
        )

        prompt = f"""
        You are an AI Cognitive Process Automation Engine. Analyze the following support ticket and return ONLY a valid JSON object with these keys:
        - "category": (Billing, Technical Bug, Account Access, or General Query)
        - "urgency_score": (Integer from 1 to 5)
        - "sentiment": (Frustrated, Neutral, or Positive)
        - "recommended_action": (Escalate to Human Agent, Auto-Resolve, or Queue for Technical Review)
        - "drafted_response": (A brief, polite customer reply)

        Ticket: "{ticket_text}"
        JSON Output:
        """

        response = model.generate_text(prompt=prompt)
        json_match = re.search(r"\{.*\}", response, re.DOTALL)
        if json_match:
            return json.loads(json_match.group(0))
        else:
            return _mock_watsonx_analysis(ticket_text)

    except Exception as e:
        return _mock_watsonx_analysis(ticket_text)


def _mock_watsonx_analysis(ticket_text: str) -> dict:
    text_lower = ticket_text.lower()
    if "charge" in text_lower or "refund" in text_lower or "billing" in text_lower:
        cat, urgency, sentiment, action = (
            "Billing",
            4,
            "Frustrated",
            "Escalate to Human Agent",
        )
        response = "We have received your billing inquiry and routed it to our finance team for immediate verification."
    elif "password" in text_lower or "login" in text_lower or "access" in text_lower:
        cat, urgency, sentiment, action = "Account Access", 3, "Neutral", "Auto-Resolve"
        response = "You can reset your account credentials by visiting our automated password recovery portal."
    else:
        urgency = 5 if "urgent" in text_lower or "down" in text_lower else 2
        cat, sentiment, action = (
            "Technical Bug",
            "Frustrated" if urgency > 3 else "Neutral",
            "Queue for Technical Review",
        )
        response = "Thank you for reporting this issue. Our engineering team has logged the bug telemetry."

    return {
        "category": cat,
        "urgency_score": urgency,
        "sentiment": sentiment,
        "recommended_action": action,
        "drafted_response": response,
    }


if __name__ == "__main__":
    ticket_input = sys.argv[1] if len(sys.argv) > 1 else ""
    output = analyze_ticket_with_watsonx(ticket_input)
    print(json.dumps(output))
