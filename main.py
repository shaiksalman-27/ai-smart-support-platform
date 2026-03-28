from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel

app = FastAPI(title="AI Smart Support Automation Platform")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

tickets = []
ticket_counter = 1


class IssueRequest(BaseModel):
    issue: str


def classify_issue(issue: str):
    text = issue.lower()

    if "password" in text or "reset" in text or "login" in text or "sign in" in text:
        return {
            "category": "Account Access",
            "priority": "Low",
            "solution": "Please use the Forgot Password option and reset your password. If the issue continues, contact support."
        }

    elif "payment" in text or "billing" in text or "charged" in text or "transaction" in text:
        return {
            "category": "Billing",
            "priority": "High",
            "solution": "Please verify your payment method and transaction ID. Billing issues should be reviewed quickly."
        }

    elif "hack" in text or "hacked" in text or "unauthorized" in text or "suspicious" in text:
        return {
            "category": "Security",
            "priority": "Critical",
            "solution": "This looks like a security risk. Please change your password immediately and escalate this case."
        }

    elif "slow" in text or "crash" in text or "bug" in text or "error" in text:
        return {
            "category": "Technical Issue",
            "priority": "Medium",
            "solution": "Please try refreshing the app, clearing cache, or reinstalling. If the issue continues, technical support should investigate."
        }

    else:
        return {
            "category": "General Support",
            "priority": "Medium",
            "solution": "Your issue has been recorded and will be reviewed by the support team."
        }


@app.post("/analyze")
def analyze_issue(data: IssueRequest):
    global ticket_counter

    result = classify_issue(data.issue)

    ticket = {
        "id": ticket_counter,
        "issue": data.issue,
        "category": result["category"],
        "priority": result["priority"],
        "solution": result["solution"],
        "status": "Open"
    }

    tickets.append(ticket)
    ticket_counter += 1

    return {"ticket": ticket}


@app.get("/tickets")
def get_tickets():
    total = len(tickets)
    open_count = sum(1 for t in tickets if t["status"] == "Open")
    closed_count = sum(1 for t in tickets if t["status"] == "Closed")

    return {
        "tickets": tickets,
        "summary": {
            "total": total,
            "open": open_count,
            "closed": closed_count
        }
    }


@app.put("/tickets/{ticket_id}")
def close_ticket(ticket_id: int):
    for ticket in tickets:
        if ticket["id"] == ticket_id:
            ticket["status"] = "Closed"
            return {"message": "Ticket closed successfully", "ticket": ticket}

    return {"message": "Ticket not found"}


app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
def serve_home():
    return FileResponse("templates/index.html")