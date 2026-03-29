---
title: AI Smart Support Platform
emoji: 🤖
colorFrom: blue
colorTo: indigo
sdk: docker
pinned: false
---

# AI Smart Support Platform

AI Smart Support Platform is a FastAPI-based customer support automation system.

It helps users submit issues and instantly get:
- issue classification
- priority level
- suggested solution
- escalation status
- ticket tracking

It also includes an admin dashboard to view and manage support tickets.

## Features

- Analyze customer issues in real time
- Classify tickets into categories such as:
  - Account Access
  - Billing
  - Security
  - Technical Issue
  - Feature Request
  - General Support
- Assign priority levels:
  - Low
  - Medium
  - High
- Suggest a possible solution
- Mark risky cases for escalation
- Store ticket history with timestamps
- Update ticket status from the admin dashboard

## Tech Stack

- FastAPI
- Python
- HTML
- CSS
- JavaScript
- Jinja2 Templates
- Uvicorn

## Project Structure

```text
.
├── app
│   └── main.py
├── static
│   ├── script.js
│   └── style.css
├── templates
│   ├── index.html
│   └── admin.html
├── requirements.txt
├── Dockerfile
└── README.md