import json
import urllib.request
import urllib.error


OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL_NAME = "llama3.2:3b"


def analyze_transaction(issue_type, description):

    prompt = f"""
You are an AI-powered UPI Recovery Assistant for users in India.

Analyse the user's UPI problem and provide personalised
recovery guidance and an evidence checklist.

USER'S ISSUE:
{issue_type}

USER'S DESCRIPTION:
{description}

Choose exactly one category:
1. Wrong UPI Transfer
2. Suspected Fraud
3. Duplicate Payment
4. Pending Transaction
5. Other UPI Issue

Return ONLY valid JSON in this format:

{{
    "category": "Issue category",
    "analysis": "Explain the user's problem.",
    "guidance": [
        "Immediate action",
        "Recommended recovery action",
        "Evidence Checklist:",
        "Evidence item 1",
        "Evidence item 2",
        "Evidence item 3",
        "Further escalation",
        "Important precaution"
    ]
}}

EVIDENCE CHECKLIST RULES:

For Wrong UPI Transfer:
- UPI transaction ID or UTR number.
- Payment confirmation screenshot.
- Transaction date and amount.
- Recipient UPI ID, if available.

For Suspected Fraud:
- UPI transaction ID or UTR number.
- Payment confirmation screenshot.
- Suspicious messages, emails or call details.
- Relevant complaint reference, if available.

For Duplicate Payment:
- Both transaction IDs or UTR numbers.
- Screenshots of both payments.
- Transaction dates and amounts.

For Pending Transaction:
- Transaction reference number.
- Payment status screenshot.
- Bank statement showing the debit, if available.
- Any existing complaint reference.

For Other UPI Issue:
- Transaction reference number, if applicable.
- Relevant screenshots.
- Date and amount.
- Communication with bank or UPI app support, if available.

RECOVERY RULES:
- Give specific instructions for the selected issue.
- For suspected fraud, advise contacting the bank immediately
  and calling India's cyber fraud helpline 1930.
- Explain that recovery is not guaranteed.
- Never promise automatic reversal.
- Never invent official contact details.
- Recommend appropriate escalation if unresolved.

SECURITY RULES:
- Never request UPI PIN, OTP or banking passwords.
- Never ask users to share full card details.
- Never claim a complaint has been filed.
- Never claim you have contacted a bank.
- Never guarantee a refund.
- Tell users to hide sensitive personal information
  when sharing screenshots.
- Use simple English.
- Do not invent missing transaction information.
"""

    payload = {
        "model": MODEL_NAME,
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "format": "json",
        "stream": False,
        "options": {
            "temperature": 0.2
        }
    }

    request = urllib.request.Request(
        OLLAMA_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Content-Type": "application/json"
        },
        method="POST"
    )

    try:
        with urllib.request.urlopen(
            request,
            timeout=120
        ) as response:

            result = json.loads(
                response.read().decode("utf-8")
            )

        ai_response = json.loads(
            result["message"]["content"]
        )

        category = ai_response["category"]
        analysis = ai_response["analysis"]
        guidance = ai_response["guidance"]

        allowed_categories = [
            "Wrong UPI Transfer",
            "Suspected Fraud",
            "Duplicate Payment",
            "Pending Transaction",
            "Other UPI Issue"
        ]

        if category not in allowed_categories:
            raise ValueError("Invalid issue category")

        if not isinstance(guidance, list):
            raise ValueError("Invalid guidance format")

        if not all(
            isinstance(item, str) for item in guidance
        ):
            raise ValueError("Guidance must contain text items")

        if not isinstance(analysis, str):
            raise ValueError("Invalid analysis")

        return {
            "category": category,
            "analysis": analysis,
            "guidance": guidance,
            "ai_used": True
        }

    except (urllib.error.URLError, TimeoutError):
        return {
            "category": "AI Analysis Unavailable",
            "analysis": "The AI service could not be reached.",
            "guidance": [
                "Check whether Ollama is running.",
                "Check whether the AI model is installed.",
                "Try again later."
            ],
            "ai_used": False
        }

    except (
        KeyError,
        ValueError,
        json.JSONDecodeError
    ):
        return {
            "category": "AI Analysis Error",
            "analysis": "The AI returned an unexpected response.",
            "guidance": [
                "Check the AI service.",
                "Try submitting your transaction again."
            ],
            "ai_used": False
        }