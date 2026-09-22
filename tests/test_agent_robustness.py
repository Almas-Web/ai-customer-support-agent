from unittest.mock import patch
from app.models.models import Customer
from app.agent.agent import run_agent

def test_agent_handles_tool_failure(db):
    customer = Customer(
        name="Tool Failure Customer",
        email="tool-failure@example.com",
    )
    db.add(customer)
    db.commit()
    db.refresh(customer)

    with patch(
        "app.agent.agent.client.models.generate_content"
    ) as mock_generate:
        first_response = type("Response", (), {})()
        first_response.function_calls = [
            type(
                "FunctionCall",
                (),
                {
                    "name": "get_payment_status",
                    "args": {
                        "customer_id": 999999,
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
        second_response.text = "I could not retrieve your payment information."

        mock_generate.side_effect = [
            first_response,
            second_response,
        ]

        original_tool = __import__(
            "app.agent.agent",
            fromlist=["TOOL_FUNCTIONS"],
        ).TOOL_FUNCTIONS["get_payment_status"]

        with patch(
            "app.agent.agent.TOOL_FUNCTIONS",
            {
                **__import__(
                    "app.agent.agent",
                    fromlist=["TOOL_FUNCTIONS"],
                ).TOOL_FUNCTIONS,
                "get_payment_status": lambda **kwargs: {
                    "success": False,
                    "error": "Database error",
                },
            },
        ):
            result = run_agent(
                db=db,
                user_message="Check my payment.",
                customer_id=customer.id,
            )

    assert result == "I could not retrieve your payment information."
    assert mock_generate.call_count == 2

def test_agent_stops_after_max_iterations(db):
    customer = Customer(
        name="Max Iteration Customer",
        email="max-iteration@example.com",
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
                    "name": "get_payment_status",
                    "args": {
                        "customer_id": 999999,
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
            user_message="Check my payment.",
            customer_id=customer.id,
            max_iterations=2,
        )

    assert result == (
        "I could not complete the request within the allowed number of steps."
    )
    assert mock_generate.call_count == 2