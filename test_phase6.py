import requests
import json
from dotenv import load_dotenv
import time

# Load environment variables
load_dotenv()

BASE_URL = "http://localhost:8000"

def test_conversation_viewer():
    """Test Phase 6: Conversation Viewer Interface with various conversation lengths"""
    
    print("🧪 Testing Phase 6: Conversation Viewer Interface")
    print("Testing conversation display with different lengths and participant counts")
    print()
    
    # Test Case 1: Short conversation (1 participant)
    print("=" * 60)
    print("TEST CASE 1: Short conversation - 1 participant")
    print("=" * 60)
    
    short_scenario = {
        "name": "Quick Check-in",
        "participants": [
            {
                "name": "Alex",
                "role": "Person seeking brief guidance",
                "perspective": "Just needs a quick emotional check-in",
                "meta_tags": ["tired", "seeking-clarity"],
                "initial_message": "I just need a quick check-in. How do I know if I'm making the right decisions?"
            }
        ],
        "system_prompt": "You are Driftwood, a brief but thoughtful counselor. Provide concise, helpful guidance.",
        "settings": {
            "model": "gpt-4",
            "temperature": 0.7,
            "max_tokens": 150  # Short responses
        }
    }
    
    test_conversation_flow("Short Conversation", short_scenario)
    
    # Test Case 2: Medium conversation (2 participants)
    print("\n" + "=" * 60)
    print("TEST CASE 2: Medium conversation - 2 participants")
    print("=" * 60)
    
    medium_scenario = {
        "name": "Roommate Discussion",
        "participants": [
            {
                "name": "Maya",
                "role": "Concerned roommate",
                "perspective": "Wants to address living situation issues constructively",
                "meta_tags": ["diplomatic", "frustrated"],
                "initial_message": "I think we need to talk about some house rules and how we can live together more harmoniously."
            },
            {
                "name": "Jordan",
                "role": "Defensive roommate",
                "perspective": "Feels attacked and doesn't see any problems",
                "meta_tags": ["defensive", "confused", "stressed"],
                "initial_message": "I don't understand what the problem is. I think I've been a pretty good roommate."
            }
        ],
        "system_prompt": "You are Driftwood, a patient mediator helping roommates communicate effectively. Guide them toward practical solutions while validating both perspectives.",
        "settings": {
            "model": "gpt-4",
            "temperature": 0.6,
            "max_tokens": 300  # Medium responses
        }
    }
    
    test_conversation_flow("Medium Conversation", medium_scenario)
    
    # Test Case 3: Long conversation (3 participants)
    print("\n" + "=" * 60)
    print("TEST CASE 3: Long conversation - 3 participants")
    print("=" * 60)
    
    long_scenario = {
        "name": "Complex Family Dynamics",
        "participants": [
            {
                "name": "Parent Robin",
                "role": "Overwhelmed parent",
                "perspective": "Trying to balance work, family, and personal needs while maintaining household harmony",
                "meta_tags": ["overwhelmed", "responsible"],
                "initial_message": "I feel like I'm constantly juggling everyone's needs and I'm burning out. I love my family but I'm losing myself in the process."
            },
            {
                "name": "Teen Casey",
                "role": "Misunderstood teenager",
                "perspective": "Feels controlled and wants more independence while struggling with academic pressure",
                "meta_tags": ["rebellious", "stressed", "misunderstood"],
                "initial_message": "Nobody understands the pressure I'm under at school and at home. I just want some freedom to make my own choices."
            },
            {
                "name": "Grandparent Sam",
                "role": "Well-meaning elder",
                "perspective": "Wants to help but feels caught between generations with different values",
                "meta_tags": ["wise", "concerned", "traditional"],
                "initial_message": "I see both sides of this situation and I want to help, but sometimes I feel like my advice isn't welcomed or understood."
            }
        ],
        "system_prompt": "You are Driftwood, a skilled family therapist. Help each family member feel heard and understood while gently guiding them toward empathy and practical solutions. Address generational differences with sensitivity.",
        "settings": {
            "model": "gpt-4",
            "temperature": 0.8,
            "max_tokens": 500  # Longer responses
        }
    }
    
    test_conversation_flow("Long Conversation", long_scenario)

def test_conversation_flow(test_name, scenario_data):
    """Test the complete flow: create scenario -> run simulation -> verify viewer data"""
    
    try:
        # Step 1: Create scenario
        print(f"\n🔧 Creating scenario: {scenario_data['name']}")
        response = requests.post(f"{BASE_URL}/scenarios", json=scenario_data)
        
        if response.status_code != 200:
            print(f"❌ Failed to create scenario: {response.status_code}")
            return
        
        scenario = response.json()
        scenario_id = scenario["id"]
        print(f"✅ Scenario created: {scenario_id}")
        
        # Step 2: Run simulation
        print(f"🚀 Running simulation...")
        run_response = requests.post(f"{BASE_URL}/run?scenario_id={scenario_id}")
        
        if run_response.status_code != 200:
            print(f"❌ Simulation failed: {run_response.status_code}")
            return
        
        run_data = run_response.json()
        print(f"✅ Simulation completed: {run_data['id']}")
        
        # Step 3: Test conversation viewer data structure
        print(f"📊 Testing conversation viewer data:")
        
        # Verify run data structure
        required_fields = ['id', 'scenario_id', 'timestamp', 'starred', 'log']
        for field in required_fields:
            if field in run_data:
                print(f"   ✅ {field}: present")
            else:
                print(f"   ❌ {field}: missing")
        
        # Analyze conversation log
        log = run_data['log']
        print(f"   📝 Messages: {len(log)}")
        
        # Check message structure
        if log:
            first_message = log[0]
            message_fields = ['speaker', 'content', 'timestamp']
            print(f"   🔍 Message structure check:")
            for field in message_fields:
                if field in first_message:
                    print(f"      ✅ {field}: present")
                else:
                    print(f"      ❌ {field}: missing")
        
        # Test message content length variety
        message_lengths = [len(msg['content']) for msg in log]
        avg_length = sum(message_lengths) / len(message_lengths) if message_lengths else 0
        max_length = max(message_lengths) if message_lengths else 0
        min_length = min(message_lengths) if message_lengths else 0
        
        print(f"   📏 Message lengths:")
        print(f"      Average: {avg_length:.0f} characters")
        print(f"      Range: {min_length} - {max_length} characters")
        
        # Verify conversation flow
        speakers = [msg['speaker'] for msg in log]
        participant_names = [p['name'] for p in scenario_data['participants']]
        ai_messages = len([s for s in speakers if s == 'AI'])
        participant_messages = len([s for s in speakers if s != 'AI'])
        
        print(f"   🗣️  Speaker distribution:")
        print(f"      AI messages: {ai_messages}")
        print(f"      Participant messages: {participant_messages}")
        print(f"      Expected participants: {participant_names}")
        
        # Verify all participants spoke
        participants_who_spoke = set([s for s in speakers if s != 'AI'])
        expected_participants = set(participant_names)
        
        if participants_who_spoke == expected_participants:
            print(f"   ✅ All participants spoke")
        else:
            missing = expected_participants - participants_who_spoke
            extra = participants_who_spoke - expected_participants
            if missing:
                print(f"   ⚠️  Missing speakers: {missing}")
            if extra:
                print(f"   ⚠️  Unexpected speakers: {extra}")
        
        # Test scenario retrieval for viewer context
        print(f"🔍 Testing scenario retrieval for viewer:")
        scenarios_response = requests.get(f"{BASE_URL}/scenarios")
        if scenarios_response.status_code == 200:
            scenarios = scenarios_response.json()
            matching_scenario = None
            for s in scenarios:
                if s['id'] == scenario['id']:
                    matching_scenario = s
                    break
            
            if matching_scenario:
                print(f"   ✅ Scenario found for viewer context")
                print(f"   📋 Participants in scenario: {len(matching_scenario['participants'])}")
                print(f"   ⚙️  Settings: {matching_scenario['settings']}")
            else:
                print(f"   ❌ Scenario not found in list")
        else:
            print(f"   ❌ Failed to retrieve scenarios: {scenarios_response.status_code}")
        
        print(f"\n🎉 {test_name} viewer test completed!")
        
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
    
    test_conversation_viewer()
    
    print("\n" + "=" * 60)
    print("🏁 Phase 6 Conversation Viewer tests completed!")
    print("✨ The viewer should display:")
    print("   - Split-panel layout with context and chat")
    print("   - System prompt, settings, and participant details")
    print("   - Formatted messages with speaker identification")
    print("   - Proper timestamps and message counts")
    print("   - Responsive design for different screen sizes")
    print("=" * 60)