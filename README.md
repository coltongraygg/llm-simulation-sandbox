# 🌊 Driftwood LLM Simulation Lab

A local-first web application for testing system prompts, participant dynamics, and conflict mediation flows. Driftwood allows you to define simulation scenarios, trigger structured conversations, and review AI-mediated outputs with full visibility into the simulation context and settings.

## Overview

Driftwood is designed for researchers, developers, and conflict resolution specialists who want to test and refine AI-mediated group conversations. The application provides a comprehensive environment for:

- **Scenario Building**: Create complex multi-participant scenarios with detailed psychological profiles
- **Group Mediation**: Simulate realistic conversations where AI mediates between participants
- **Analysis & Review**: Examine conversation logs with full context and participant information
- **History Management**: Save, star, and organize simulation runs for comparison and iteration

## Features

- 🎭 **Multi-Participant Scenarios**: Define participants with names, roles, perspectives, and emotional states
- 🤖 **AI-Powered Mediation**: Uses OpenAI GPT-4 to facilitate group conversations
- 📊 **Real-Time Simulation**: Watch conversations unfold with live updates and loading states
- 📝 **Conversation Analysis**: Review detailed logs with speaker identification and timestamps
- ⭐ **History Management**: Star important runs and filter by starred/all simulations
- 🗑️ **Bulk Operations**: Delete individual runs or clear all unstarred simulations
- 📱 **Responsive Design**: Works seamlessly on desktop and mobile devices
- 🔒 **Local-First**: All data stored locally with SQLite - no external dependencies

## Tech Stack

### Backend
- **FastAPI**: Modern Python web framework with automatic API documentation
- **SQLAlchemy**: SQL toolkit and ORM for database operations
- **SQLite**: Lightweight, file-based database for local storage
- **OpenAI Python SDK**: Integration with GPT-4 for AI responses
- **Pydantic**: Data validation and serialization

### Frontend
- **Vanilla JavaScript**: No framework dependencies - pure ES6+ classes
- **HTML5 & CSS3**: Semantic markup with responsive design
- **CSS Grid & Flexbox**: Modern layout techniques for responsive UI

### Key Libraries
- `uvicorn`: ASGI server for running FastAPI applications
- `aiosqlite`: Async SQLite driver for database operations
- `python-dotenv`: Environment variable management
- `python-multipart`: Form data handling

## Quick Start

### Prerequisites
- Python 3.8 or higher
- OpenAI API key

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd llm-simulation-sandbox
   ```

2. **Create and activate virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up OpenAI API key**
   
   Create a `.env` file in the project root:
   ```
   OPENAI_API_KEY=your-api-key-here
   ```
   


5. **Initialize database**
   ```bash
   python3 -c "from database import engine, Base; Base.metadata.create_all(bind=engine)"
   ```

6. **Start the server**
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000 --reload
   ```

7. **Open your browser**
   
   Navigate to: `http://localhost:8000`

## Usage Guide

### Creating a Scenario

1. **Navigate to Scenario Builder**
2. **Fill in basic information**:
   - Scenario name (e.g., "Family Conflict Resolution")
   - System prompt (instructions for the AI mediator)
3. **Add participants** (minimum 1 required):
   - Name: The participant's identifier
   - Role: Their relationship to the situation
   - Perspective: Their viewpoint or stance
   - Initial Message: What they say to start the conversation
   - Meta Tags: Emotional states (up to 3 tags)
4. **Configure model settings**:
   - Model: GPT-4 (default)
   - Temperature: Controls randomness 
   - Max Tokens: Response length limit 
5. **Click "Run Simulation"** to save and execute

### Viewing Results

After running a simulation:
- **Conversation Viewer**: Opens automatically with full conversation log
- **Context Panel**: Shows system prompt, settings, and participant details
- **Chat Log**: Displays the complete conversation with timestamps
- **Navigation**: Use "Back to History" to return to the history view

### Managing History

- **View All Runs**: See every simulation you've created
- **Filter by Starred**: Show only your favorite simulations
- **Star/Unstar**: Click the star icon to mark important runs
- **View Conversation**: Click to review any past simulation
- **Delete Runs**: Remove individual simulations or bulk delete all unstarred
- **Automatic Sorting**: Most recent simulations appear first

## API Documentation

When the server is running, visit `http://localhost:8000/docs` for interactive API documentation powered by FastAPI's automatic OpenAPI generation.

### Key Endpoints

- `GET /scenarios` - List all saved scenarios
- `POST /scenarios` - Create a new scenario
- `GET /runs` - List all simulation runs
- `POST /run?scenario_id={id}` - Execute a simulation
- `GET /runs/{id}` - Get detailed run information
- `PATCH /runs/{id}/star` - Toggle starred status
- `DELETE /runs/{id}` - Delete specific run
- `DELETE /runs` - Delete all unstarred runs

## Configuration

### Environment Variables

- `OPENAI_API_KEY`: Required for AI functionality

### Model Settings

- **Temperature**: Controls response randomness
  - 0.0: Deterministic, focused responses
  - 0.7: Balanced creativity and consistency (recommended)
  - 2.0: Highly creative, unpredictable responses
- **Max Tokens**: Limits response length (recommended: 400-800)

## Development

### Project Structure

```
llm-simulation-sandbox/
├── main.py              # FastAPI application setup
├── routes.py            # API endpoints and request handling
├── database.py          # SQLAlchemy models and database config
├── schemas.py           # Pydantic models for validation
├── simulation.py        # Core simulation engine logic
├── requirements.txt     # Python dependencies
├── static/
│   ├── index.html      # Main application interface
│   ├── app.js          # Frontend JavaScript application
│   └── styles.css      # Responsive CSS styles
└── driftwood.db        # SQLite database (created automatically)
```

### Running in Development

```bash
# Install dependencies
pip install -r requirements.txt

# Start with auto-reload
uvicorn main:app --reload --host 0.0.0.0 --port 8000

```

### Database Schema

- **scenarios**: Stores scenario definitions with participants and settings
- **runs**: Stores simulation results with conversation logs and metadata

## Troubleshooting

### Common Issues

1. **OpenAI API Key Error**
   - Verify your API key is correctly set in `.env` or environment variables
   - Check your OpenAI account has sufficient credits

2. **Database Errors**
   - Delete `driftwood.db` and restart to reset the database
   - Ensure write permissions in the project directory

3. **Port Already in Use**
   - Change the port: `uvicorn main:app --port 8001`
   - Or kill the existing process: `lsof -ti:8000 | xargs kill`

4. **Module Import Errors**
   - Ensure virtual environment is activated
   - Reinstall dependencies: `pip install -r requirements.txt`

### Getting Help

- Check the interactive API docs at `/docs` when the server is running
- Review the browser console for frontend errors
- Check the server logs for backend issues

