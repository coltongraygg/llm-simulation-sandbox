# Driftwood LLM Simulation Lab - Development Tasklist

## Instructions for LLM
- **Completed tasks**: Add 🟢 emoji in brackets next to task item
- **In progress tasks**: Add 🟡 emoji in brackets next to task item  
- **Incomplete tasks**: Leave brackets empty [ ]
- Update the "Notes:" section for each phase with implementation details, errors, or post-mortem analysis (1 paragraph)
- View llm.md for additional info. 

---

## Phase 1: Project Setup & Backend Foundation
- [🟢] Initialize Python FastAPI project structure
- [🟢] Set up SQLite database connection
- [🟢] Create database schema (scenarios and runs tables)
- [🟢] Set up basic FastAPI server with CORS
- [🟢] Create requirements.txt with dependencies
- [🟢] Test basic server startup

**Notes:** Successfully completed Phase 1 with some initial dependency compatibility challenges. Created virtual environment, updated package versions for Python 3.13 compatibility (pydantic 2.5.0 → 2.10.3), and fixed SQLAlchemy UUID import issue. Server runs successfully with uvicorn and responds to health checks. Database models are properly configured with UUID primary keys and JSON columns for flexible data storage.

---

## Phase 2: Database Models & API Endpoints
- [🟢] Create SQLAlchemy models for Scenarios table
- [🟢] Create SQLAlchemy models for Runs table
- [🟢] Implement GET /scenarios endpoint
- [🟢] Implement POST /scenarios endpoint
- [🟢] Implement GET /runs endpoint
- [🟢] Implement GET /runs/{id} endpoint
- [🟢] Test all endpoints with sample data

**Notes:** Successfully completed Phase 2 with clean architecture. Refactored code organization: moved Pydantic models to `schemas.py`, API endpoints to `routes.py`, keeping `main.py` focused on app setup. All endpoints implement proper validation, error handling, and return appropriate HTTP status codes. Database models were already well-designed from Phase 1. Created comprehensive test script with sample data to verify all endpoints work correctly. JSON handling for participants and settings works seamlessly with SQLAlchemy's JSON column type.

---

## Phase 3: OpenAI Integration & Simulation Engine
- [🟢] Set up OpenAI client configuration for GPT-4 real-time model
- [🟢] Create simulation runner function
- [🟢] Implement participant conversation flow logic
- [🟢] Implement POST /run endpoint
- [🟢] Add proper error handling for API failures
- [🟢] Test simulation with sample participants
- [🟢] Validate conversation log format

**Notes:** Successfully completed Phase 3 with simplified simulation approach. Updated participant schema to include `initial_message` field. Created clean simulation engine where AI responds to each participant's initial message individually, with full context about all participants. The system prompt controls AI behavior rather than hard-coded instructions. Database models automatically support new structure via JSON columns. Added comprehensive error handling for OpenAI API failures and invalid scenario IDs. Created test script to validate end-to-end flow.

---

## Phase 4: Frontend Structure & Static Serving
- [🟢] Create HTML file structure for main interface
- [🟢] Set up CSS for responsive layout
- [🟢] Configure FastAPI to serve static files
- [🟢] Create basic JavaScript module structure
- [🟢] Implement navigation between views
- [🟢] Test static file serving

**Notes:** Successfully completed Phase 4 with clean, responsive frontend foundation. Created semantic HTML structure with three main views: Scenario Builder, History, and Conversation Viewer. Implemented mobile-first CSS with responsive breakpoints and clean typography using system fonts. Static file serving was already configured in main.py. Built modular JavaScript class with navigation system and API helper methods. Verified all static assets load correctly via FastAPI. Foundation is ready for detailed form implementation in Phase 5.

---

## Phase 5: Scenario Builder Interface
- [🟢] Create scenario builder HTML form
- [🟢] Implement participant add/remove functionality
- [🟢] Add system prompt text area
- [🟢] Create model settings controls (temperature, max_tokens)
- [🟢] Implement form validation
- [🟢] Connect to POST /scenarios API
- [🟢] Add "Run Simulation" button functionality

**Notes:** Successfully completed Phase 5 with comprehensive scenario builder interface. Created intuitive form with dynamic participant management - users can add/remove participants with all required fields (name, role, perspective, initial_message, meta_tags). Implemented interactive meta tags system where users type and press Enter to add emotional state tags. Added real-time form validation that enables "Run Simulation" button only when scenario is saved and valid. Integrated seamlessly with backend APIs for saving scenarios and running simulations. The interface includes responsive design and clear visual feedback for user actions.

---

## Phase 6: Conversation Viewer Interface
- [🟢] Create split-panel layout (left: settings, right: chat)
- [🟢] Display system prompt and participant details in left panel
- [🟢] Implement chat log display in right panel
- [🟢] Add proper message formatting with speaker identification
- [🟢] Implement real-time updates during simulation
- [🟢] Add loading states and notifications
- [🟢] Test with various conversation lengths

**Notes:** Successfully completed Phase 6 with comprehensive conversation viewer interface. Created full-page overlay with split-panel layout - left sidebar shows system prompt, model settings, and detailed participant information with tags. Right panel displays formatted chat log with speaker identification (AI vs participants), timestamps, and message styling. Implemented proper loading states with spinner and custom messages, plus toast notifications with auto-hide and type-based styling. Added responsive design for mobile devices. Tested with short (1 participant), medium (2 participants), and long (3 participants) conversations. The viewer seamlessly integrates with existing simulation data and provides excellent UX for reviewing conversations.

---

## Phase 7: Simulation History & Management
- [🟢] Create simulation history list interface
- [🟢] Implement star/unstar functionality
- [🟢] Add run metadata display (timestamp, scenario name)
- [🟢] Create view button to open conversation viewer
- [🟢] Implement sorting (latest first)
- [🟢] Add visual indicators for starred runs
- [🟢] Test history navigation and data persistence

**Notes:** Successfully completed Phase 7 with comprehensive history management system. Created intuitive list interface showing all simulation runs with metadata (timestamp, scenario name, unique ID). Implemented star/unstar functionality with PATCH endpoint and visual indicators (golden star icon and left border). Added filtering (All Runs / Starred) with proper state management. Runs are automatically sorted latest first with relative timestamps ("2 hours ago"). Each run displays a "View Conversation" button that opens the Phase 6 conversation viewer. Added proper loading states, empty states, and error handling. Data persistence works correctly - starred status and run history survive server restarts. Used efficient caching to minimize API calls while maintaining real-time updates. Responsive design works well on mobile devices.

---

## Phase 8: Testing & Polish
- [ ] Test full simulation workflow end-to-end
- [ ] Test error handling for invalid inputs
- [ ] Create basic documentation for running the app

**Notes:** [LLM: Summarize testing results, bugs found and fixed, performance observations, or deployment considerations here]

---

## Phase 9: Final Integration & Deployment
- [ ] Verify all features work together seamlessly
- [ ] Test simulation quality with various scenarios
- [ ] Create startup script for easy local deployment
- [ ] Update README.md with sections such as Overview, Tech Stack, Instructions (ie, how to use).

**Notes:** [LLM: Document final integration challenges, performance optimizations made, or recommendations for future development here]