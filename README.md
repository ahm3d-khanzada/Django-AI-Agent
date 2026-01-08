# 🤖 Build AI Agents with Django, LangGraph, and Permit

Build **secure, production-ready AI Agents** using **Python**, **Django**, **LangGraph**, and **Permit.io**.

Django stores and manages your data, LangGraph orchestrates intelligent multi-agent workflows, and Permit.io provides **RBAC guardrails** to ensure both users *and AI agents* can only access what they are allowed to.

🚀 **Sign up for Permit:**  
https://io.permit.io/langraph-permit

---

## 📌 Overview

This repository accompanies a full-length, hands-on course that teaches you how to design, build, and secure AI Agents that interact with real application data.

Unlike typical AI demos, this project focuses on:

- Security-first design  
- Authorization & access control  
- Scalable multi-agent systems  
- Production-ready architecture  

---

## ✅ What You Will Learn

By completing this project, you will be able to:

- Save and manage user data with **Django ORM**
- Chat directly with Django data **without vector embeddings**
- Convert Python functions into **LangChain tools**
- Integrate **third-party REST APIs** into AI agents
- Build **multi-agent systems** using LangGraph
- Create a **Supervisor Agent** to control other agents
- Swap LLM providers with minimal effort
- Implement **RBAC (Role-Based Access Control)**
- Secure AI agents with **Permit.io guardrails**
- Restrict create, read, update, delete, search, and share actions
- Enforce **instance-level permissions**
- Prevent agents from performing unauthorized actions

---

## 🧠 System Architecture

User
↓
Django Application
├── Models
├── ORM Queries
├── Users & Permissions
↓
LangGraph
├── AI Agents
├── Supervisor Agent
├── Tool Execution
↓
LLM Provider (OpenAI or others)
↓
Permit.io
├── RBAC Policies
├── Resource Permissions
├── Instance-Level Authorization



---

## 🛠️ Technology Stack

- **Python 3.10+**
- **Django**
- **LangGraph**
- **LangChain**
- **Permit.io**
- **OpenAI (or compatible LLM provider)**
- **Jupyter Notebooks**
---

## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/codingforentrepreneurs/langgraph-django-permit.git
cd langgraph-django-permit

python -m venv venv
source venv/bin/activate     # macOS / Linux
venv\Scripts\activate        # Windows

pip install -r requirements.txt

DJANGO_SECRET_KEY=your-secret-key
DEBUG=True

OPENAI_API_KEY=your-openai-api-key

PERMIT_API_KEY=your-permit-api-key
PERMIT_PDP_URL=your-permit-pdp-url
PERMIT_TENANT=default

python manage.py migrate

python manage.py createsuperuser

python manage.py runserver
```
