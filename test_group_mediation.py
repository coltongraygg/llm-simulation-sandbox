import requests
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

BASE_URL = "http://localhost:8000"

def test_group_mediation_flow():
    """Test the new group mediation flow"""
    
    print("🧪 Testing Group Mediation Flow")
    print("Testing: All participants speak first, then AI mediates the group")
    print()
    
    # Create a scenario with multiple participants
    scenario_data = {
        "name": "Group Mediation Test",
        "participants": [
            {
                "name": "Alice",
                "role": "Team member feeling overworked",
                "perspective": "Believes the workload is unfairly distributed",
                "meta_tags": ["frustrated", "tired"],
                "initial_message": "I feel like I'm doing most of the work on this project while others aren't pulling their weight."
            },
            {
                "name": "Bob",
                "role": "Team member feeling criticized",
                "perspective": "Thinks Alice is being unfair and doesn't see the full picture",
                "meta_tags": ["defensive", "confused"],
                "initial_message": "That's not fair, Alice. I've been working hard too, just on different parts that maybe you don't see."
            },
            {
                "name": "Carol",
                "role": "Team leader trying to mediate",
                "perspective": "Wants to resolve the conflict and improve team dynamics",
                "meta_tags": ["diplomatic", "concerned"],
                "initial_message": "I can see there's some tension here. Let's work together to understand everyone's contributions and find a better way forward."
            }
        ],
        "system_prompt": "You are Driftwood, a professional team mediator. Help the team members understand each other's perspectives and work toward a collaborative solution. Address the group as a whole and acknowledge the different viewpoints that have been shared.",
        "settings": {
            "model": "gpt-4",
            "temperature": 0.7,
            "max_tokens": 500
        }
    }
    
    try:
        # Create scenario
        print("📝 Creating test scenario...")
        scenario_response = requests.post(f"{BASE_URL}/scenarios", json=scenario_data)
        
        if scenario_response.status_code != 200:
            print(f"❌ Failed to create scenario: {scenario_response.status_code}")
            print(f"Error: {scenario_response.text}")
            return
        
        scenario = scenario_response.json()
        print(f"✅ Scenario created: {scenario['name']}")
        
        # Run simulation
        print("🚀 Running group mediation simulation...")
        run_response = requests.post(f"{BASE_URL}/run?scenario_id={scenario['id']}")
        
        if run_response.status_code != 200:
            print(f"❌ Simulation failed: {run_response.status_code}")
            print(f"Error: {run_response.text}")
            return
        
        run_data = run_response.json()
        print(f"✅ Simulation completed: {run_data['id']}")
        
        # Analyze the conversation flow
        print("\n📊 Analyzing conversation flow:")
        log = run_data['log']
        print(f"Total messages: {len(log)}")
        
        # Expected flow: 3 participants + 1 AI response = 4 messages
        expected_messages = len(scenario_data['participants']) + 1
        
        if len(log) == expected_messages:
            print(f"✅ Expected message count: {expected_messages}")
        else:
            print(f"⚠️  Expected {expected_messages} messages, got {len(log)}")
        
        # Check the flow order
        print("\n💬 Conversation Flow:")
        participants_spoken = set()
        ai_responses = 0
        
        for i, msg in enumerate(log, 1):
            speaker = msg['speaker']
            content_preview = msg['content'][:80] + "..." if len(msg['content']) > 80 else msg['content']
            
            print(f"{i}. {speaker}: {content_preview}")
            
            if speaker == "AI":
                ai_responses += 1
                if ai_responses == 1:
                    # First AI response should come after all participants
                    if len(participants_spoken) == len(scenario_data['participants']):
                        print("   ✅ AI responded after all participants spoke")
                    else:
                        print(f"   ⚠️  AI responded after only {len(participants_spoken)} participants")
            else:
                participants_spoken.add(speaker)
        
        # Verify all participants spoke
        expected_participants = {p['name'] for p in scenario_data['participants']}
        if participants_spoken == expected_participants:
            print(f"✅ All participants spoke: {list(participants_spoken)}")
        else:
            missing = expected_participants - participants_spoken
            print(f"⚠️  Missing participants: {missing}")
        
        # Check AI response quality
        ai_message = next((msg for msg in log if msg['speaker'] == 'AI'), None)
        if ai_message:
            print(f"\n🤖 AI Response Analysis:")
            ai_content = ai_message['content']
            print(f"Length: {len(ai_content)} characters")
            
            # Check for problematic patterns
            if "AI:" in ai_content or "Driftwood:" in ai_content:
                print("⚠️  AI response contains speaker labels")
            else:
                print("✅ No problematic speaker labels found")
            
            # Check if AI is speaking for participants
            participant_names = [p['name'] for p in scenario_data['participants']]
            speaking_for_others = any(f"{name}:" in ai_content for name in participant_names)
            
            if speaking_for_others:
                print("⚠️  AI appears to be speaking for participants")
            else:
                print("✅ AI is not speaking for participants")
        
        print(f"\n🎉 Group mediation test completed!")
        
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to server. Make sure it's running on localhost:8000")
    except Exception as e:
        print(f"❌ Test failed: {e}")

def verify_server_connection():
    """Verify the server is running and accessible"""
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print("✅ Server is running and accessible")
            return True
        else:
            print(f"❌ Server responded with status {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server. Please start the server first.")
        return False

if __name__ == "__main__":
    if not verify_server_connection():
        exit(1)
    
    test_group_mediation_flow()
    
    print("\n" + "=" * 60)
    print("✨ New Group Mediation Flow:")
    print("   1. All participants share their initial messages")
    print("   2. AI mediator responds to the group as a whole")
    print("   3. AI has full context of all participants and their perspectives")
    print("   4. AI facilitates group dialogue rather than individual counseling")
    print("=" * 60)