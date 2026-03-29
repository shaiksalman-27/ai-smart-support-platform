async function analyzeIssue() {
  const issueInputElement = document.getElementById("issueInput");
  const loadingMessage = document.getElementById("loadingMessage");
  const errorMessage = document.getElementById("errorMessage");
  const resultCard = document.getElementById("resultCard");
  const ticketHistory = document.getElementById("ticketHistory");
  const priorityElement = document.getElementById("ticketPriority");

  const issueInput = issueInputElement.value.trim();

  errorMessage.classList.add("hidden");
  resultCard.classList.add("hidden");

  if (!issueInput) {
    errorMessage.textContent = "Please enter an issue.";
    errorMessage.classList.remove("hidden");
    return;
  }

  loadingMessage.classList.remove("hidden");

  try {
    const response = await fetch("/analyze", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ issue: issueInput })
    });

    const data = await response.json();

    loadingMessage.classList.add("hidden");

    if (data.error) {
      errorMessage.textContent = data.error;
      errorMessage.classList.remove("hidden");
      return;
    }

    document.getElementById("ticketId").textContent = data.ticket_id;
    document.getElementById("ticketIssue").textContent = data.issue;
    document.getElementById("ticketCategory").textContent = data.category;
    document.getElementById("ticketStatus").textContent = data.status;
    document.getElementById("ticketCreatedAt").textContent = data.created_at;
    document.getElementById("ticketSolution").textContent = data.solution;
    document.getElementById("ticketEscalation").textContent = data.escalation ? "Yes" : "No";
    document.getElementById("ticketConfidence").textContent = data.confidence ?? "N/A";

    document.getElementById("ticketKeywords").textContent =
      data.matched_keywords && data.matched_keywords.length > 0
        ? data.matched_keywords.join(", ")
        : "No direct keyword match";

    priorityElement.textContent = data.priority;
    priorityElement.className = "badge";

    if (data.priority === "High") {
      priorityElement.classList.add("high");
    } else if (data.priority === "Medium") {
      priorityElement.classList.add("medium");
    } else {
      priorityElement.classList.add("low");
    }

    ticketHistory.innerHTML = "";
    data.history.forEach(item => {
      const li = document.createElement("li");
      li.textContent = item;
      ticketHistory.appendChild(li);
    });

    resultCard.classList.remove("hidden");

  } catch (error) {
    console.error(error);
    loadingMessage.classList.add("hidden");
    errorMessage.textContent = "Error analyzing issue.";
    errorMessage.classList.remove("hidden");
  }
}