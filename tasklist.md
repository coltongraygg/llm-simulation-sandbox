# Driftwood LLM Simulation Lab - Development Tasklist

## Instructions for LLM
- **Completed tasks**: Add 🟢 emoji in brackets next to task item
- **In progress tasks**: Add 🟡 emoji in brackets next to task item  
- **Incomplete tasks**: Leave brackets empty [ ]
- Update the "Notes:" section for each phase with implementation details, errors, or post-mortem analysis (1 paragraph)
- View llm.md for additional info. 

---

## Phase 1: Project Setup & Backend Foundation
- [ ] Initialize Python FastAPI project structure
- [ ] Set up SQLite database connection
- [ ] Create database schema (scenarios and runs tables)
- [ ] Set up basic FastAPI server with CORS
- [ ] Create requirements.txt with dependencies
- [ ] Test basic server startup

**Notes:** [LLM: Document any setup issues, dependency conflicts, or initial configuration challenges here]

---

## Phase 2: Database Models & API Endpoints
- [ ] Create SQLAlchemy models for Scenarios table
- [ ] Create SQLAlchemy models for Runs table
- [ ] Implement GET /scenarios endpoint
- [ ] Implement POST /scenarios endpoint
- [ ] Implement GET /runs endpoint
- [ ] Implement GET /runs/{id} endpoint
- [ ] Test all endpoints with sample data

**Notes:** [LLM: Note any database schema adjustments, JSON handling issues, or API design decisions here]

---

## Phase 3: OpenAI Integration & Simulation Engine
- [ ] Set up OpenAI client configuration for GPT-4 real-time model
- [ ] Create simulation runner function
- [ ] Implement participant conversation flow logic
- [ ] Implement POST /run endpoint
- [ ] Add proper error handling for API failures
- [ ] Test simulation with sample participants
- [ ] Validate conversation log format

**Notes:** [LLM: Document OpenAI API integration challenges, conversation flow logic, or model response handling issues here]

---

## Phase 4: Frontend Structure & Static Serving
- [ ] Create HTML file structure for main interface
- [ ] Set up CSS for responsive layout
- [ ] Configure FastAPI to serve static files
- [ ] Create basic JavaScript module structure
- [ ] Implement navigation between views
- [ ] Test static file serving

**Notes:** [LLM: Note any frontend architecture decisions, CSS framework choices, or static serving configuration issues here]

---

## Phase 5: Scenario Builder Interface
- [ ] Create scenario builder HTML form
- [ ] Implement participant add/remove functionality
- [ ] Add system prompt text area
- [ ] Create model settings controls (temperature, max_tokens)
- [ ] Implement form validation
- [ ] Connect to POST /scenarios API
- [ ] Add "Run Simulation" button functionality

**Notes:** [LLM: Document form validation logic, user experience decisions, or API integration challenges here]

---

## Phase 6: Conversation Viewer Interface
- [ ] Create split-panel layout (left: settings, right: chat)
- [ ] Display system prompt and participant details in left panel
- [ ] Implement chat log display in right panel
- [ ] Add proper message formatting with speaker identification
- [ ] Implement real-time updates during simulation
- [ ] Add loading states and notifications
- [ ] Test with various conversation lengths

**Notes:** [LLM: Note any layout challenges, real-time update implementation, or UI/UX improvements made here]

---

## Phase 7: Simulation History & Management
- [ ] Create simulation history list interface
- [ ] Implement star/unstar functionality
- [ ] Add run metadata display (timestamp, scenario name)
- [ ] Create view button to open conversation viewer
- [ ] Implement sorting (latest first)
- [ ] Add visual indicators for starred runs
- [ ] Test history navigation and data persistence

**Notes:** [LLM: Document any data management decisions, UI patterns used, or performance considerations here]

---

## Phase 8: Testing & Polish
- [ ] Test full simulation workflow end-to-end
- [ ] Verify database persistence across sessions
- [ ] Test error handling for invalid inputs
- [ ] Validate OpenAI API error scenarios
- [ ] Test UI responsiveness on different screen sizes
- [ ] Add proper logging throughout application
- [ ] Create basic documentation for running the app

**Notes:** [LLM: Summarize testing results, bugs found and fixed, performance observations, or deployment considerations here]

---

## Phase 9: Final Integration & Deployment
- [ ] Verify all features work together seamlessly
- [ ] Test simulation quality with various scenarios
- [ ] Optimize database queries and API performance
- [ ] Add any missing error messages or user feedback
- [ ] Create startup script for easy local deployment
- [ ] Document any known limitations or future improvements

**Notes:** [LLM: Document final integration challenges, performance optimizations made, or recommendations for future development here]