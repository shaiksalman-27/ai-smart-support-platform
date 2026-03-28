from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

tickets = []

class IssueRequest(BaseModel):
    issue: str

@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/health")
def health():
    return {"status": "ok"}

def analyze_issue_logic(issue_text: str):
    text = issue_text.lower()

    category = "General"
    priority = "Low"
    solution = "Please review the issue and contact support team if needed."

    if "login" in text or "password" in text or "account" in text:
        category = "Account"
        priority = "Medium"
        solution = "Check your username and password. Try resetting your password and verify account access."

    elif "payment" in text or "transaction" in text or "upi" in text or "card" in text:
        category = "Payment"
        priority = "High"
        solution = "Check card/UPI details, account balance, and payment gateway status. Retry after a few minutes."

    elif "network" in text or "internet" in text or "wifi" in text or "connection" in text:
        category = "Network"
        priority = "Medium"
        solution = "Check your internet connection, restart your router, and verify network stability."

    elif "error" in text or "bug" in text or "crash" in text or "not working" in text:
        category = "Technical"
        priority = "High"
        solution = "Restart the app, clear cache, and check whether the latest version is installed."

    elif "slow" in text or "lag" in text or "performance" in text:
        category = "Performance"
        priority = "Medium"
        solution = "Close background apps, refresh the system, and check device memory and CPU usage."

    elif "refund" in text or "return" in text:
        category = "Refund"
        priority = "High"
        solution = "Check refund policy, verify order status, and initiate refund request from support."

    return category, priority, solution

@app.post("/analyze")
def analyze_issue(request: IssueRequest):
    category, priority, solution = analyze_issue_logic(request.issue)

    ticket_id = len(tickets) + 1
    ticket = {
        "id": ticket_id,
        "issue": request.issue,
        "category": category,
        "priority": priority,
        "solution": solution,
        "status": "Open"
    }
    tickets.append(ticket)

    return {
        "message": "Issue analyzed successfully",
        "ticket": ticket
    }

@app.get("/tickets")
def get_tickets():
    total = len(tickets)
    open_tickets = len([t for t in tickets if t["status"] == "Open"])
    closed_tickets = len([t for t in tickets if t["status"] == "Closed"])

    return {
        "summary": {
            "total": total,
            "open": open_tickets,
            "closed": closed_tickets
        },
        "tickets": tickets
    }

@app.put("/tickets/{ticket_id}")
def close_ticket(ticket_id: int):
    for ticket in tickets:
        if ticket["id"] == ticket_id:
            ticket["status"] = "Closed"
            return {"message": "Ticket closed successfully", "ticket": ticket}

    return {"message": "Ticket not found"}