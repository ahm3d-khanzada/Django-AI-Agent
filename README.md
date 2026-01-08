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

## 🧠 System Architecture
```
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
```

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

### Clone the Repository

```bash
git clone https://github.com/ahm3d-khanzada/Django-AI-Agent.git
cd langgraph-django-permit
```
### Craete a Virual Enviorment
```bash
python -m venv venv
source venv/bin/activate     # macOS / Linux
venv\Scripts\activate        # Windows
```
### Intsall requirment.txt file
```bash
pip install -r requirements.txt
```
### Create .ENV 
```bash
DJANGO_SECRET_KEY=your-secret-key
DEBUG=True
OPENAI_API_KEY=your-openai-api-key

PERMIT_API_KEY=your-permit-api-key
PERMIT_PDP_URL=your-permit-pdp-url
PERMIT_TENANT=default
```
### Migrate DB 
```bash
python manage.py migrate
```
### Create Super-user
```bash
python manage.py createsuperuser
```
### Run the server
```bash
python manage.py runserver
```
