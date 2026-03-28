async function loadAdminTickets() {
  const adminBox = document.getElementById("adminTickets");

  try {
    const response = await fetch("http://127.0.0.1:7860/tickets");
    const tickets = await response.json();

    if (!tickets.length) {
      adminBox.innerHTML = "<p>No tickets available.</p>";
      return;
    }

    adminBox.innerHTML = tickets.map(ticket => `
      <div class="ticket-card">
        <p><strong>Ticket ID:</strong> ${ticket.ticket_id}</p>
        <p><strong>Issue:</strong> ${ticket.message}</p>
        <p><strong>Category:</strong> ${ticket.category}</p>
        <p><strong>Priority:</strong> ${ticket.priority}</p>
        <p><strong>Status:</strong> ${ticket.status}</p>

        <select id="status-${ticket.ticket_id}">
          <option value="Open">Open</option>
          <option value="In Progress">In Progress</option>
          <option value="Resolved">Resolved</option>
        </select>

        <button onclick="updateStatus('${ticket.ticket_id}')">
          Update Status
        </button>
      </div>
    `).join("");

  } catch (error) {
    adminBox.innerHTML = "<p>Error loading tickets.</p>";
    console.error(error);
  }
}


async function updateStatus(ticketId) {
  const newStatus = document.getElementById(`status-${ticketId}`).value;

  try {
    const response = await fetch(`http://127.0.0.1:7860/tickets/${ticketId}`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        status: newStatus
      })
    });

    const data = await response.json();

    alert(`Ticket ${data.ticket_id} updated to ${data.status}`);
    loadAdminTickets();

  } catch (error) {
    alert("Error updating status");
    console.error(error);
  }
}


window.onload = loadAdminTickets;