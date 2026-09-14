def send_email(
    recipient: str,
    subject: str,
    body: str,
):
    if not recipient:
        return {
            "success": False,
            "error": "Recipient email is required.",
        }

    if not subject:
        return {
            "success": False,
            "error": "Email subject is required.",
        }

    if not body:
        return {
            "success": False,
            "error": "Email body is required.",
        }

    return {
        "success": True,
        "message": "Email prepared successfully.",
        "email": {
            "recipient": recipient,
            "subject": subject,
            "body": body,
        },
    }