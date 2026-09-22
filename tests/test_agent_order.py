from unittest.mock import patch
from app.models.models import Customer, Order
from app.agent.agent import run_agent
def test_agent_can_get_customer_order(db):
    customer = Customer(
        name="Agent Order Customer",
        email="agent-order@example.com",
    )
    db.add(customer)
    db.commit()
    db.refresh(customer)
    order = Order(
        customer_id=customer.id,
        item_name="AI Backend Course",
        amount=99.99,
        status="paid",
    )
    db.add(order)
    db.commit()
    db.refresh(order)
    tool_response = {
        "success": True,
        "order": {
            "id": order.id,
            "customer_id": customer.id,
            "item_name": order.item_name,
            "amount": str(order.amount),
            "status": order.status,
            "created_at": order.created_at.isoformat(),
        },
    }
    with patch(
        "app.agent.agent.client.models.generate_content"
    ) as mock_generate:
        first_response = type("Response", (), {})()
        first_response.function_calls = [
            type(
                "FunctionCall",
                (),
                {
                    "name": "get_order",
                    "args": {
                        "customer_id": 999999,
                        "order_id": order.id,
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
        second_response.text = "You ordered AI Backend Course for $99.99."
        mock_generate.side_effect = [
            first_response,
            second_response,
        ]
        result = run_agent(
            db=db,
            user_message="What did I order?",
            customer_id=customer.id,
        )
    assert result == "You ordered AI Backend Course for $99.99."
    assert mock_generate.call_count == 2