import requests
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

BASE_URL = "http://localhost:8000"

def test_simulation():
    """Test the new simulation flow with initial messages"""
    
    # Create a test scenario with initial messages
    scenario_data = {
        "name": "Test Conflict Resolution",
        "participants": [
            {
                "name": "Jordan",
                "role": "Upset with Alex",
                "perspective": "Feels unheard and emotionally distant from Alex",
                "meta_tags": ["angry", "resentful", "powerless"],
                "initial_message": "I feel like you never listen to me anymore, Alex. Every time I try to talk to you about something important, you just dismiss my feelings."
            },
            {
                "name": "Alex",
                "role": "Defensive partner",
                "perspective": "Feels criticized and doesn't understand Jordan's concerns",
                "meta_tags": ["defensive", "confused", "frustrated"],
                "initial_message": "I don't understand why you think I don't listen. I'm always here for you, but it feels like nothing I do is ever good enough."
            }
        ],
        "system_prompt": "You are Driftwood, a neutral AI conflict mediator. Guide each participant toward clarity, de-escalation, and mutual understanding. Keep your tone calm and non-judgmental. After each participant speaks, respond to both content and underlying emotions.",
        "settings": {
            "model": "gpt-4",
            "temperature": 0.7,
            "max_tokens": 400
        }
    }
    
    try:
        # Create scenario
        print("Creating test scenario...")
        response = requests.post(f"{BASE_URL}/scenarios", json=scenario_data)
        if response.status_code == 200:
            scenario = response.json()
            scenario_id = scenario["id"]
            print(f"Scenario created with ID: {scenario_id}")
            
            # Run simulation (using query parameter as the endpoint expects)
            print("Running simulation...")
            run_response = requests.post(f"{BASE_URL}/run?scenario_id={scenario_id}")
            
            if run_response.status_code == 200:
                run_data = run_response.json()
                print("Simulation completed successfully!")
                print(f"Run ID: {run_data['id']}")
                print("\nConversation Log:")
                for entry in run_data["log"]:
                    print(f"[{entry['timestamp']}] {entry['speaker']}: {entry['content']}")
                    print()
            else:
                print(f"Simulation failed: {run_response.status_code}")
                print(f"Error: {run_response.text}")
        else:
            print(f"Scenario creation failed: {response.status_code}")
            print(f"Error: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("Could not connect to server. Make sure it's running on localhost:8000")
    except Exception as e:
        print(f"Test failed: {e}")

if __name__ == "__main__":
    print("Testing Phase 3 implementation...")
    test_simulation()