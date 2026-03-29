from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

app = FastAPI(title="AI Smart Support Automation Platform")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

tickets = []
ticket_counter = 1


class IssueRequest(BaseModel):
    issue: str


class StatusUpdateRequest(BaseModel):
    status: str


def get_current_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def classify_issue(issue: str):
    text = issue.lower()

    rules = [
        {
            "category": "Security",
            "priority": "High",
            "solution": "This looks like a security issue. Please change your password immediately and contact support for urgent review.",
            "escalation": True,
            "keywords": ["hacked", "fraud", "unauthorized", "stolen", "breach", "suspicious", "attack"],
        },
        {
            "category": "Billing",
            "priority": "High",
            "solution": "Please verify your payment details, transaction ID, and billing history. Our billing team will review this issue.",
            "escalation": False,
            "keywords": ["payment", "billing", "charged", "refund", "transaction", "invoice", "money", "debit"],
        },
        {
            "category": "Account Access",
            "priority": "Low",
            "solution": "Please use the Forgot Password option to reset your password. If the issue continues, contact support.",
            "escalation": False,
            "keywords": ["password", "reset", "login", "sign in", "signin", "cannot login", "can't login", "otp"],
        },
        {
            "category": "Technical Issue",
            "priority": "Medium",
            "solution": "Please try again after refreshing the page, restarting the app, or checking your internet connection.",
            "escalation": False,
            "keywords": ["error", "bug", "crash", "not working", "issue", "failed", "loading", "freeze", "stuck"],
        },
        {
            "category": "Feature Request",
            "priority": "Low",
            "solution": "Thank you for the suggestion. Our product team will review this feature request.",
            "escalation": False,
            "keywords": ["feature", "add", "request", "improve", "enhancement", "new option", "new feature"],
        },
    ]

    best_match = {
        "category": "General Support",
        "priority": "Medium",
        "solution": "Our support team will review your issue shortly.",
        "escalation": False,
        "confidence": 40,
        "matched_keywords": [],
    }

    highest_score = 0

    for rule in rules:
        matched = [word for word in rule["keywords"] if word in text]
        score = len(matched)

        if score > highest_score:
            highest_score = score
            confidence = min(60 + score * 10, 95)

            best_match = {
                "category": rule["category"],
                "priority": rule["priority"],
                "solution": rule["solution"],
                "escalation": rule["escalation"],
                "confidence": confidence,
                "matched_keywords": matched,
            }

    return best_match


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/admin", response_class=HTMLResponse)
def admin_page(request: Request):
    return templates.TemplateResponse("admin.html", {"request": request})


@app.post("/analyze")
def analyze_issue(data: IssueRequest):
    global ticket_counter

    issue_text = data.issue.strip()

    if not issue_text:
        return {"error": "Issue cannot be empty"}

    result = classify_issue(issue_text)
    current_time = get_current_time()

    ticket = {
        "ticket_id": ticket_counter,
        "issue": issue_text,
        "category": result["category"],
        "priority": result["priority"],
        "solution": result["solution"],
        "escalation": result["escalation"],
        "confidence": result["confidence"],
        "matched_keywords": result["matched_keywords"],
        "status": "Open",
        "created_at": current_time,
        "history": [
            f"Ticket created at {current_time}",
            f"Classified as {result['category']}",
            f"Priority set to {result['priority']}",
            f"Confidence score: {result['confidence']}%"
        ]
    }

    if result["matched_keywords"]:
        ticket["history"].append(
            f"Matched keywords: {', '.join(result['matched_keywords'])}"
        )

    if result["escalation"]:
        ticket["history"].append("Marked for escalation")

    tickets.append(ticket)
    ticket_counter += 1

    return ticket


@app.get("/tickets")
def get_tickets():
    return {
        "count": len(tickets),
        "tickets": tickets
    }


@app.get("/tickets/{ticket_id}")
def get_ticket(ticket_id: int):
    for ticket in tickets:
        if ticket["ticket_id"] == ticket_id:
            return ticket
    return {"error": "Ticket not found"}


@app.put("/tickets/{ticket_id}/status")
def update_ticket_status(ticket_id: int, data: StatusUpdateRequest):
    valid_statuses = ["Open", "In Progress", "Resolved", "Closed"]

    if data.status not in valid_statuses:
        return {
            "error": "Invalid status",
            "allowed_statuses": valid_statuses
        }

    for ticket in tickets:
        if ticket["ticket_id"] == ticket_id:
            ticket["status"] = data.status
            ticket["history"].append(
                f"Status changed to {data.status} at {get_current_time()}"
            )
            return {
                "message": "Status updated successfully",
                "ticket": ticket
            }

    return {"error": "Ticket not found"}