from unittest.mock import patch
from app.models.models import Customer
from app.agent.agent import run_agent

def test_agent_requires_confirmation_for_ticket(db):
    customer = Customer(
        name="Confirmation Customer",
        email="confirmation@example.com",
    )
    db.add(customer)
    db.commit()
    db.refresh(customer)

    with patch(
        "app.agent.agent.client.models.generate_content"
    ) as mock_generate:
        response = type("Response", (), {})()
        response.function_calls = [
            type(
                "FunctionCall",
                (),
                {
                    "name": "create_support_ticket",
                    "args": {
                        "customer_id": 999999,
                        "subject": "Payment failed",
                        "description": "My payment failed.",
                        "priority": "high",
                    },
                },
            )()
        ]
        response.candidates = [
            type(
                "Candidate",
                (),
                {
                    "content": type(
                        "Content",
                        (),
                        {
                            "role": "model",
                            "parts": [],
                        },
                    )()
                },
            )()
        ]
        mock_generate.return_value = response

        result = run_agent(
            db=db,
            user_message="Create a ticket for my failed payment.",
            customer_id=customer.id,
        )

    assert "Confirmation required" in result
    assert mock_generate.call_count == 1