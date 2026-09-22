# AI Customer Support Agent

An AI-powered customer support backend built with FastAPI, PostgreSQL, SQLAlchemy, Gemini, and AI tool calling.

This project demonstrates how an AI agent can understand customer requests, select the right tools, execute multi-step workflows, retrieve real customer data, maintain conversation context, and safely perform customer support actions.

## Features

- AI Agent with Gemini
- Function / Tool Calling
- Multi-step Agent Workflows
- Conversation Memory
- Customer Management
- Order Management
- Payment Management
- Invoice Management
- Support Ticket Management
- JWT Authentication
- Role-Based Access Control (RBAC)
- Customer Data Isolation
- Human-in-the-Loop Confirmation
- Tool Error Handling
- Maximum Agent Iteration Control
- PostgreSQL
- SQLAlchemy ORM
- Alembic Migrations
- Pytest Test Suite
- Docker
- Swagger / OpenAPI Documentation
- ReDoc API Documentation

## AI Agent Workflow

```text
User Request
     ↓
AI Agent
     ↓
Understand User Intent
     ↓
Select Appropriate Tool
     ↓
Execute Tool
     ↓
Tool Result
     ↓
Agent Decision
     ↓
Use Another Tool if Needed
     ↓
Final Response
Supported Agent Tools
Tool	Purpose
get_customer	Retrieve customer information
get_payment_status	Check payment status
get_invoice	Retrieve invoice information
get_order	Retrieve order information
create_support_ticket	Create a support ticket
get_support_ticket	Retrieve a support ticket
send_email	Prepare customer email
Example Agent Workflows
1. Check Failed Payment

User:

My payment failed. Check what happened.

Agent workflow:

User Request
    ↓
get_payment_status
    ↓
Payment Result
    ↓
Analyze Failure
    ↓
Final Response

Example:

Your payment failed because of insufficient funds.
2. Failed Payment → Support Ticket

User:

My payment failed. Create a support ticket for me.

Agent workflow:

User Request
    ↓
get_payment_status
    ↓
Detect Failed Payment
    ↓
Request User Confirmation
    ↓
create_support_ticket
    ↓
Return Ticket Information

This workflow demonstrates multi-step agent execution.

3. Get Customer Order

User:

What did I order?

Agent workflow:

User Request
    ↓
get_order
    ↓
Retrieve Customer Order
    ↓
Final Response
4. Get Support Ticket

User:

Show me my support ticket.

Agent workflow:

User Request
    ↓
get_support_ticket
    ↓
Verify Customer Ownership
    ↓
Return Ticket Information
5. Get Latest Invoice

User:

Show me my latest invoice.

Agent workflow:

User Request
    ↓
get_invoice
    ↓
Retrieve Latest Invoice
    ↓
Final Response
Authentication

The API uses JWT-based authentication.

Authentication flow:

Register
   ↓
User Account
   ↓
Password Hashing
   ↓
Login
   ↓
JWT Access Token
   ↓
Authenticated API Requests

Passwords are securely hashed before being stored in the database.

Role-Based Access Control

The application supports role-based authorization.

Example roles:

customer
admin

Protected endpoints verify the authenticated user's role before allowing restricted operations.

Customer Data Isolation

Customer-specific data is protected using the authenticated user's customer identity.

JWT
 ↓
Authenticated User
 ↓
Customer Profile
 ↓
Authenticated Customer ID
 ↓
Agent Tool
 ↓
Database Query

The application does not trust a customer ID supplied by the LLM for protected operations.

For example, even if the model attempts:

{
  "customer_id": 999,
  "order_id": 10
}

the application replaces the customer ID with the authenticated customer's ID.

This prevents the AI agent from accessing another customer's private information.

Customer isolation is implemented for:

Orders
Payments
Invoices
Support Tickets
Conversations
Agent Tools
Human-in-the-Loop

Sensitive actions require user confirmation before execution.

Currently protected actions include:

Creating support tickets
Sending emails

Example:

User
 ↓
Agent decides a ticket is required
 ↓
Confirmation Required
 ↓
User confirms
 ↓
Tool executes

This prevents the agent from automatically performing sensitive actions without user approval.

Conversation Memory

The application stores conversation history in PostgreSQL.

Conversation structure:

Conversation
    ├── User Message
    ├── Assistant Message
    ├── User Message
    ├── Assistant Message
    └── ...

Previous messages can be loaded and provided to the agent so it can maintain context across multiple requests.

Example:

User:
My payment failed.

Agent:
Your payment failed because of insufficient funds.

User:
What was the reason again?

Agent:
The payment failed because of insufficient funds.
Agent Loop

The agent uses an iterative tool-calling loop.

Conceptually:

while max_iterations:
    Send request to LLM
    ↓
    Does LLM request a tool?
        ↓
       Yes
        ↓
    Execute tool
        ↓
    Return tool result to LLM
        ↓
    Continue

       No
        ↓
    Return final response

A maximum iteration limit is used to prevent infinite agent loops.

Error Handling

The agent handles tool and service failures gracefully.

Examples include:

Tool errors
Missing customer data
Missing orders
Missing invoices
Missing payments
Missing support tickets
Unknown tools
Gemini API quota errors
Maximum iteration limits

Gemini quota errors are returned as a user-friendly response instead of exposing internal API errors.

Database

The project uses PostgreSQL with SQLAlchemy ORM.

Main database entities:

User
Customer
Order
Payment
Invoice
SupportTicket
Conversation
Message

Relationships:

User
 ↓
Customer
 ↓
Order
 ├── Payment
 └── Invoice

Customer
 ├── Payments
 ├── Invoices
 ├── Support Tickets
 └── Conversations
       ↓
     Messages
Order Workflow

The project includes a simplified order checkout workflow.

Customer
   ↓
Create Order
   ↓
Create Payment
   ↓
Create Invoice
   ↓
Store Transaction Data

The current implementation uses a simplified successful checkout flow for demonstration purposes.

Project Structure
ai-customer-support-agent/
│
├── app/
│   ├── agent/
│   │   ├── agent.py
│   │   └── tools.py
│   │
│   ├── api/
│   │   ├── agent.py
│   │   ├── auth.py
│   │   ├── conversation.py
│   │   ├── customer.py
│   │   ├── invoice.py
│   │   ├── order.py
│   │   ├── payment.py
│   │   └── ticket.py
│   │
│   ├── db/
│   │   ├── database.py
│   │   └── seed.py
│   │
│   ├── models/
│   │   └── models.py
│   │
│   ├── schems/
│   │   ├── auth.py
│   │   ├── customer.py
│   │   ├── invoice.py
│   │   ├── order.py
│   │   ├── payment.py
│   │   └── ticket.py
│   │
│   ├── services/
│   │   ├── auth_service.py
│   │   ├── conversation_service.py
│   │   ├── customer_service.py
│   │   ├── invoice_service.py
│   │   ├── order_service.py
│   │   ├── payment_service.py
│   │   └── ticket_service.py
│   │
│   ├── tools/
│   │   ├── customer_tools.py
│   │   ├── email_tools.py
│   │   ├── invoice_tools.py
│   │   ├── order_tools.py
│   │   ├── payment_tools.py
│   │   └── ticket_tools.py
│   │
│   ├── config.py
│   ├── dependencies.py
│   ├── main.py
│   ├── rbac.py
│   └── security.py
│
├── tests/
│   ├── conftest.py
│   ├── test_agent_confirmation.py
│   ├── test_agent_order.py
│   ├── test_agent_robustness.py
│   ├── test_agent_ticket.py
│   └── test_security.py
│
├── alembic/
│
├── .env.example
├── .gitignore
├── docker-compose.yml
├── requirements.txt
└── README.md
Tech Stack
Backend
Python
FastAPI
Pydantic
SQLAlchemy
Database
PostgreSQL
Alembic
AI
Google Gemini
Gemini Function Calling
AI Agent Architecture
Authentication & Security
JWT
Password Hashing
RBAC
Customer Data Isolation
Testing
Pytest
Mock-based Agent Testing
Security Testing
Agent Workflow Testing
Infrastructure
Docker
Docker Compose
Uvicorn
Installation
1. Clone Repository
git clone https://github.com/Almas-Web/ai-customer-support-agent.git
cd ai-customer-support-agent
2. Create Virtual Environment

Windows:

python -m venv venv

Activate:

venv\Scripts\activate
3. Install Dependencies
pip install -r requirements.txt
4. Configure Environment Variables

Create a .env file based on .env.example.

Example:

DATABASE_URL=postgresql://postgres:postgres@localhost:5435/ai_support_agent
GEMINI_API_KEY=your_gemini_api_key
JWT_SECRET_KEY=your_jwt_secret_key
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=60

Never commit the real .env file to GitHub.

5. Start PostgreSQL
docker compose up -d

Check running containers:

docker ps
6. Run Database Migrations
alembic upgrade head
7. Start FastAPI
uvicorn app.main:app --reload

The API will be available at:

http://127.0.0.1:8000
API Documentation

Swagger UI:

http://127.0.0.1:8000/docs

ReDoc:

http://127.0.0.1:8000/redoc
Testing

Run the complete test suite:

pytest -v

The test suite covers:

Authentication
Authorization
RBAC
Customer data isolation
Order security
Payment security
Invoice security
Ticket security
Conversation security
Agent customer isolation
Agent order workflow
Agent ticket workflow
Human-in-the-loop confirmation
Agent tool failure handling
Maximum iteration handling
Security Testing

The project includes tests verifying that one customer cannot access another customer's:

Payment
Invoice
Support Ticket
Conversation
Order

Agent tools are also tested against cross-customer access.

Environment Variables

The application requires:

Variable	Description
DATABASE_URL	PostgreSQL connection URL
GEMINI_API_KEY	Gemini API key
JWT_SECRET_KEY	JWT signing secret
JWT_ALGORITHM	JWT algorithm
JWT_ACCESS_TOKEN_EXPIRE_MINUTES	JWT expiration time
Learning Goals

This project was built to understand practical AI Agent engineering concepts.

The main learning areas include:

LLM-based Agents
Function Calling
Tool Calling
Tool Selection
Agent Loops
Multi-step Workflows
Conversation Memory
Database-backed Agents
Tool Execution
Authentication
Authorization
RBAC
Agent Security
Customer Data Isolation
Human-in-the-Loop
Error Handling
Maximum Iteration Control
AI Agent Testing
What This Project Demonstrates

The project focuses on the practical integration of an AI agent with a real backend system.

Instead of using an LLM only for text generation, the agent can interact with backend tools:

LLM
 ↓
Tool Selection
 ↓
FastAPI Backend
 ↓
Database
 ↓
Tool Result
 ↓
LLM
 ↓
Final Response

This architecture can be extended to real-world applications such as:

Customer support automation
SaaS support systems
E-commerce assistants
Billing assistants
Internal business assistants
AI-powered help desks
Future Improvements

Possible future improvements include:

Real email provider integration
Real payment gateway integration
Background task processing
Agent observability
Structured agent tracing
Advanced retry strategies
Production deployment
More business-specific tools
License

This project is created for learning, experimentation, and portfolio purposes.