# Driftwood LLM Simulation Lab

## Purpose

This project is a local-first web app for testing system prompts, participant dynamics, and conflict mediation flows using the **GPT-4 real-time model (text-to-text version)**. It allows you to define simulation scenarios, trigger structured conversations, and review AI-mediated outputs with full visibility into the simulation context and settings.

Only the **GPT-4 real-time model (text-to-text)** is used for now. Future support for other models will be added later.

---

## Stack

- **Frontend**: Plain HTML, CSS, and JavaScript
- **Backend**: Python (FastAPI)
- **Database**: SQLite
- **Model**: GPT-4 real-time model via OpenAI (text input → text output)
- **Deployment**: Localhost only

The frontend is served statically by the backend — but the backend is dynamic, so you *can* use JavaScript to show loading states or notifications (e.g., “Simulation complete”).

---

## Model Clarification

This project uses the **GPT-4 real-time model** in **text-to-text mode**, not audio.


---

## Simulation Structure

### Participants (per simulation)

Each participant includes:

- `name`: string  
  e.g., `"Jordan"`

- `role`: string  
  e.g., `"Upset with Alex"`

- `perspective`: string  
  e.g., `"Feels unheard and emotionally distant from Alex."`

- `meta_tags`: array of strings  
  e.g., `["angry", "resentful", "powerless"]`

---

### System Prompt

A single string defining the AI’s role, tone, and behavioral constraints.

Example:

```
You are Driftwood, a neutral AI conflict mediator. Guide each participant toward clarity, de-escalation, and mutual understanding. Keep your tone calm and non-judgmental. After each participant speaks, respond to both content and underlying emotions.
```

---

### Settings

Each simulation includes:

- `model`: string  
  e.g., `"gpt-4"`

- `temperature`: float  
  e.g., 0.7

- `max_tokens`: integer  
  e.g., 400

---

### Conversation Log

Stored as an ordered list of entries:

```json
{
  "speaker": "AI" | "Jordan" | "Alex",
  "content": "Message text",
  "timestamp": "2025-07-17T20:30:00Z"
}
```


---

## Interface Design

### 1. Scenario Builder

- Add/edit participants (including their individual roles, perspective, and meta tags)
- Add/edit system prompt
- Set temperature and model
- Button: “Run Simulation”
- Sends data to backend and stores the full simulation log

---

### 2. Conversation Viewer (Full Page)

Split-page layout:

- **Left panel**:
  - System prompt
  - Model
  - Settings
  - Participant names, roles, perspectives, and meta_tags

- **Right panel**:
  - Full chat log of the simulation (each chat message should include who the sender was (e.g, "- Alex" or "- AI"))

---

### 3. Simulation History Viewer

- List of all past simulations (latest first)
- Each run has a **unique ID**
- Each run can be **⭐ Starred**
- Starred runs are visually marked
- View button opens that simulation’s Conversation Viewer

---

## Backend API Endpoints

- `GET /scenarios`: Get all saved scenario definitions
- `POST /scenarios`: Create or update a scenario
- `POST /run`: Run a simulation and return the full conversation log
- `GET /runs`: Get all past simulation runs (basic metadata)
- `GET /runs/{id}`: Get full details of a specific run

---

## Database Schema (Simplified)

### Scenarios Table

- `id`: UUID
- `name`: string
- `participants`: JSON
- `system_prompt`: string
- `settings`: JSON

### Runs Table

- `id`: UUID
- `scenario_id`: foreign key
- `timestamp`: datetime
- `starred`: boolean
- `log`: JSON array of `{speaker, content, timestamp}`

---

## Notes

- All functionality is local.
- The frontend can show alert notifications for when a simulation has finished running. 
