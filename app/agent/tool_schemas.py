TOOL_SCHEMAS = [
    {
        "name": "get_customer",
        "description": "Find a customer by customer ID or email address.",
        "parameters": {
            "type": "object",
            "properties": {
                "customer_id": {
                    "type": "integer",
                    "description": "Customer ID."
                },
                "email": {
                    "type": "string",
                    "description": "Customer email address."
                }
            },
            "required": []
        }
    },
    {
        "name": "get_payment_status",
        "description": "Check a customer's latest payment, a specific payment, or failed payments.",
        "parameters": {
            "type": "object",
            "properties": {
                "customer_id": {
                    "type": "integer",
                    "description": "Customer ID."
                },
                "payment_id": {
                    "type": "integer",
                    "description": "Specific payment ID."
                },
                "failed_only": {
                    "type": "boolean",
                    "description": "Return only failed payments."
                }
            },
            "required": ["customer_id"]
        }
    },
    {
        "name": "get_invoice",
        "description": "Get a customer's latest invoice, a specific invoice, or unpaid invoices.",
        "parameters": {
            "type": "object",
            "properties": {
                "customer_id": {
                    "type": "integer",
                    "description": "Customer ID."
                },
                "invoice_id": {
                    "type": "integer",
                    "description": "Specific invoice ID."
                },
                "unpaid_only": {
                    "type": "boolean",
                    "description": "Return only unpaid or overdue invoices."
                }
            },
            "required": ["customer_id"]
        }
    },
    {
        "name": "create_support_ticket",
        "description": "Create a support ticket for a customer.",
        "parameters": {
            "type": "object",
            "properties": {
                "customer_id": {
                    "type": "integer",
                    "description": "Customer ID."
                },
                "subject": {
                    "type": "string",
                    "description": "Support ticket subject."
                },
                "description": {
                    "type": "string",
                    "description": "Detailed description of the issue."
                },
                "priority": {
                    "type": "string",
                    "enum": ["low", "medium", "high"],
                    "description": "Ticket priority."
                }
            },
            "required": ["customer_id", "subject", "description"]
        }
    },
    {
        "name": "send_email",
        "description": "Prepare an email to send to a customer.",
        "parameters": {
            "type": "object",
            "properties": {
                "recipient": {
                    "type": "string",
                    "description": "Recipient email address."
                },
                "subject": {
                    "type": "string",
                    "description": "Email subject."
                },
                "body": {
                    "type": "string",
                    "description": "Email body."
                }
            },
            "required": ["recipient", "subject", "body"]
        }
    }
]