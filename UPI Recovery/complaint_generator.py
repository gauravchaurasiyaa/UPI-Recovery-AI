import json
import urllib.request
import urllib.error


OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL_NAME = "llama3.2:3b"


def generate_complaint(data):

    transaction_id = str(data.get("transaction_id", "Not provided"))
    amount = str(data.get("amount", "Not provided"))
    transaction_date = str(data.get("transaction_date", "Not provided"))
    issue_type = str(data.get("issue_type", "Other UPI Issue"))
    description = str(data.get("description", "Not provided"))

    prompt = f"""
You are a professional banking complaint letter assistant
for users in India.

Create a formal and clear complaint letter that a customer
can send to their bank regarding a UPI transaction problem.

TRANSACTION DETAILS:

Transaction ID: {transaction_id}
Amount: Rs. {amount}
Transaction Date: {transaction_date}
Issue Type: {issue_type}
Customer Description: {description}

INSTRUCTIONS:

1. Write a suitable complaint subject.
2. Address the letter to Bank Customer Support.
3. Include the transaction details exactly as provided.
4. Explain the customer's problem clearly.
5. Request investigation of the transaction.
6. Request guidance about the appropriate recovery process.
7. Request a complaint reference number.
8. Use professional and polite language.
9. Keep the letter concise and easy to understand.

IMPORTANT RULES:

- Never invent transaction details.
- Never claim the bank has already investigated.
- Never claim a complaint has already been registered.
- Never guarantee that money will be recovered.
- Do not invent bank names or account details.
- Do not include UPI PIN, OTP or passwords.
- Do not invent a recipient name or UPI ID.
- Do not claim that the payment was fraudulent unless
  the customer has described it as suspected fraud.

Return only the complaint letter as plain text.
Do not return JSON or additional explanations.
"""

    payload = {
        "model": MODEL_NAME,
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
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

        complaint = result["message"]["content"].strip()

        if not complaint:
            raise ValueError("Empty complaint generated")

        return complaint

    except (
        urllib.error.URLError,
        TimeoutError,
        KeyError,
        ValueError,
        json.JSONDecodeError
    ):

        return f"""
Subject: Request for Investigation of UPI Transaction

Dear Bank Customer Support Team,

I am writing to report an issue regarding my UPI transaction.

Transaction ID: {transaction_id}
Transaction Amount: Rs. {amount}
Transaction Date: {transaction_date}
Issue Type: {issue_type}

Description of the Issue:

{description}

I request you to investigate this transaction and guide me
through the appropriate complaint and recovery process.

Please provide a complaint reference number and inform me
about the next steps.

I understand that recovery depends on the investigation
and applicable banking procedures.

Thank you for your assistance.

Regards,
Customer
""".strip()