from unittest.mock import patch
from app.models.models import Customer, SupportTicket
from app.agent.agent import run_agent

def test_agent_can_get_support_ticket(db):
    customer = Customer(
        name="Agent Ticket Customer",
        email="agent-ticket@example.com",
    )
    db.add(customer)
    db.commit()
    db.refresh(customer)

    ticket = SupportTicket(
        customer_id=customer.id,
        subject="Payment failed",
        description="My payment failed during checkout.",
        status="open",
        priority="high",
    )
    db.add(ticket)
    db.commit()
    db.refresh(ticket)

    with patch(
        "app.agent.agent.client.models.generate_content"
    ) as mock_generate:
        first_response = type("Response", (), {})()
        first_response.function_calls = [
            type(
                "FunctionCall",
                (),
                {
                    "name": "get_support_ticket",
                    "args": {
                        "customer_id": 999999,
                        "ticket_id": ticket.id,
                    },
                },
            )()
        ]
        first_response.candidates = [
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

        second_response = type("Response", (), {})()
        second_response.function_calls = []
        second_response.text = (
            "Your support ticket #1 is open with high priority."
        )

        mock_generate.side_effect = [
            first_response,
            second_response,
        ]

        result = run_agent(
            db=db,
            user_message="Show me my support ticket.",
            customer_id=customer.id,
        )

    assert result == "Your support ticket #1 is open with high priority."
    assert mock_generate.call_count == 2