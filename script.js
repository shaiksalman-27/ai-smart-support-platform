const API_BASE = "";

async function analyzeIssue() {
    const issueInput = document.getElementById("issueInput");
    const resultBox = document.getElementById("resultBox");
    const issue = issueInput.value.trim();

    if (!issue) {
        resultBox.innerHTML = "<p>Please enter an issue first.</p>";
        return;
    }

    resultBox.innerHTML = "<p>Analyzing issue...</p>";

    try {
        const response = await fetch(`${API_BASE}/analyze`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ issue: issue })
        });

        if (!response.ok) {
            throw new Error(`Server error: ${response.status}`);
        }

        const data = await response.json();

        if (data.ticket) {
            const ticket = data.ticket;
            resultBox.innerHTML = `
                <p><strong>Ticket ID:</strong> ${ticket.id}</p>
                <p><strong>Issue:</strong> ${ticket.issue}</p>
                <p><strong>Category:</strong> ${ticket.category}</p>
                <p><strong>Priority:</strong> ${ticket.priority}</p>
                <p><strong>Suggested Solution:</strong> ${ticket.solution}</p>
                <p><strong>Status:</strong> ${ticket.status}</p>
            `;
        } else {
            resultBox.innerHTML = "<p>Could not analyze issue.</p>";
        }

        issueInput.value = "";
        loadTickets();
    } catch (error) {
        resultBox.innerHTML = "<p>Error connecting to backend.</p>";
        console.error("Analyze error:", error);
    }
}

async function loadTickets() {
    const ticketsList = document.getElementById("ticketsList");
    const totalTickets = document.getElementById("totalTickets");
    const openTickets = document.getElementById("openTickets");
    const closedTickets = document.getElementById("closedTickets");

    try {
        const response = await fetch(`${API_BASE}/tickets`);

        if (!response.ok) {
            throw new Error(`Server error: ${response.status}`);
        }

        const data = await response.json();

        totalTickets.innerText = data.summary.total;
        openTickets.innerText = data.summary.open;
        closedTickets.innerText = data.summary.closed;

        if (!data.tickets || data.tickets.length === 0) {
            ticketsList.innerHTML = "<p>No tickets available.</p>";
            return;
        }

        ticketsList.innerHTML = data.tickets.map(ticket => `
            <div class="ticket-card">
                <p><strong>ID:</strong> ${ticket.id}</p>
                <p><strong>Issue:</strong> ${ticket.issue}</p>
                <p><strong>Category:</strong> ${ticket.category}</p>
                <p><strong>Priority:</strong> ${ticket.priority}</p>
                <p><strong>Solution:</strong> ${ticket.solution}</p>
                <p><strong>Status:</strong> ${ticket.status}</p>
                ${ticket.status === "Open" ? `<button onclick="closeTicket(${ticket.id})">Close Ticket</button>` : ""}
            </div>
        `).join("");
    } catch (error) {
        ticketsList.innerHTML = "<p>Could not load tickets.</p>";
        console.error("Load tickets error:", error);
    }
}

async function closeTicket(ticketId) {
    try {
        const response = await fetch(`${API_BASE}/tickets/${ticketId}`, {
            method: "PUT"
        });

        if (!response.ok) {
            throw new Error(`Server error: ${response.status}`);
        }

        loadTickets();
    } catch (error) {
        console.error("Error closing ticket:", error);
    }
}

window.onload = loadTickets;