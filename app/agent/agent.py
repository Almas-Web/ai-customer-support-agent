import json
from google import genai
from google.genai import types
from google.genai.errors import ClientError
from sqlalchemy.orm import Session
from app.config import settings
from app.agent.tools import TOOLS
from app.services.conversation_service import add_message, get_conversation, get_conversation_messages
client = genai.Client(api_key=settings.GEMINI_API_KEY)
SYSTEM_PROMPT = """
You are an AI customer support agent.
You help customers with payments, invoices, and support tickets.
You can use tools to retrieve or modify customer information.
Rules:
- Use tools when real customer data is required.
- Never invent customer, payment, invoice, or ticket information.
- You may use multiple tools when necessary.
- Keep responses clear and concise.
- Always use the authenticated customer ID provided by the application.
- Never access another customer's data.
"""
TOOL_FUNCTIONS = {
    "get_customer": TOOLS["get_customer"],
    "get_payment_status": TOOLS["get_payment_status"],
    "get_invoice": TOOLS["get_invoice"],
    "create_support_ticket": TOOLS["create_support_ticket"],
    "send_email": TOOLS["send_email"],
}
def build_gemini_tools():
    return [
        types.Tool(
            function_declarations=[
                types.FunctionDeclaration(
                    name=tool["name"],
                    description=tool["description"],
                    parameters=tool["parameters"],
                )
                for tool in [
                    {
                        "name": "get_customer",
                        "description": "Find the authenticated customer's information.",
                        "parameters": {
                            "type": "OBJECT",
                            "properties": {
                                "customer_id": {"type": "INTEGER"},
                                "email": {"type": "STRING"},
                            },
                        },
                    },
                    {
                        "name": "get_payment_status",
                        "description": "Check the authenticated customer's payment status.",
                        "parameters": {
                            "type": "OBJECT",
                            "properties": {
                                "customer_id": {"type": "INTEGER"},
                                "payment_id": {"type": "INTEGER"},
                                "failed_only": {"type": "BOOLEAN"},
                            },
                            "required": ["customer_id"],
                        },
                    },
                    {
                        "name": "get_invoice",
                        "description": "Get the authenticated customer's invoice information.",
                        "parameters": {
                            "type": "OBJECT",
                            "properties": {
                                "customer_id": {"type": "INTEGER"},
                                "invoice_id": {"type": "INTEGER"},
                                "unpaid_only": {"type": "BOOLEAN"},
                            },
                            "required": ["customer_id"],
                        },
                    },
                    {
                        "name": "create_support_ticket",
                        "description": "Create a support ticket for the authenticated customer.",
                        "parameters": {
                            "type": "OBJECT",
                            "properties": {
                                "customer_id": {"type": "INTEGER"},
                                "subject": {"type": "STRING"},
                                "description": {"type": "STRING"},
                                "priority": {
                                    "type": "STRING",
                                    "enum": ["low", "medium", "high"],
                                },
                            },
                            "required": [
                                "customer_id",
                                "subject",
                                "description",
                            ],
                        },
                    },
                    {
                        "name": "send_email",
                        "description": "Prepare an email for the authenticated customer. Use this after retrieving invoice or payment information when the customer asks to receive that information by email.",
                        "parameters": {
                            "type": "OBJECT",
                            "properties": {
                                "recipient": {"type": "STRING"},
                                "subject": {"type": "STRING"},
                                "body": {"type": "STRING"},
                            },
                            "required": [
                                "recipient",
                                "subject",
                                "body",
                            ],
                        },
                    },
                ]
            ]
        )
    ]
def run_agent(
    db: Session,
    user_message: str,
    customer_id: int,
    conversation_id: int | None = None,
    max_iterations: int = 5,
):
    if conversation_id is not None:
        conversation = get_conversation(
            db,
            conversation_id,
            customer_id,
        )
        if not conversation:
            return "Conversation not found."
        previous_messages = get_conversation_messages(
            db,
            conversation_id,
        )
        contents = [
            types.Content(
                role="user" if message.role == "user" else "model",
                parts=[types.Part(text=message.content)],
            )
            for message in previous_messages
        ]
    else:
        contents = []
    contents.append(
        types.Content(
            role="user",
            parts=[types.Part(text=user_message)],
        )
    )
    if conversation_id is not None:
        add_message(
            db=db,
            conversation_id=conversation_id,
            role="user",
            content=user_message,
        )
    for _ in range(max_iterations):
        try:
            response = client.models.generate_content(
                model="gemini-3.5-flash",
                contents=contents,
                config=types.GenerateContentConfig(
                    system_instruction=SYSTEM_PROMPT,
                    tools=build_gemini_tools(),
                ),
            )
        except ClientError as exc:
            if exc.code == 429:
                return "The AI service is temporarily unavailable because the Gemini API quota has been reached. Please try again later."
            return "The AI service could not process your request right now. Please try again later."
        if not response.function_calls:
            final_response = response.text
            if conversation_id is not None:
                add_message(
                    db=db,
                    conversation_id=conversation_id,
                    role="assistant",
                    content=final_response,
                )
            return final_response
        contents.append(response.candidates[0].content)
        for function_call in response.function_calls:
            function_name = function_call.name
            function_args = dict(function_call.args or {})
            function = TOOL_FUNCTIONS.get(function_name)
            if function_name != "send_email":
                function_args["customer_id"] = customer_id
            if not function:
                tool_result = {
                    "success": False,
                    "error": f"Unknown tool: {function_name}",
                }
            else:
                try:
                    if function_name == "send_email":
                        tool_result = function(**function_args)
                    else:
                        tool_result = function(
                            db=db,
                            **function_args,
                        )
                except Exception as exc:
                    tool_result = {
                        "success": False,
                        "error": str(exc),
                    }
            contents.append(
                types.Content(
                    role="tool",
                    parts=[
                        types.Part.from_function_response(
                            name=function_name,
                            response=tool_result
                        )
                    ]
                )
            )
    return "I could not complete the request within the allowed number of steps."