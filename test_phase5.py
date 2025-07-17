import requests
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

BASE_URL = "http://localhost:8000"

def test_scenario_creation_and_simulation():
    """Test Phase 5: Scenario Builder with various participant and meta tag configurations"""
    
    # Test Case 1: Single participant with 2 meta tags
    print("=" * 60)
    print("TEST CASE 1: Single participant with 2 meta tags")
    print("=" * 60)
    
    scenario_1 = {
        "name": "Solo Reflection Session",
        "participants": [
            {
                "name": "Sarah",
                "role": "Self-reflecting individual",
                "perspective": "Feeling overwhelmed and needs guidance to process emotions",
                "meta_tags": ["overwhelmed", "confused"],
                "initial_message": "I've been feeling really overwhelmed lately and I don't know how to process all these emotions I'm having."
            }
        ],
        "system_prompt": "You are Driftwood, a compassionate AI counselor. Help individuals process their emotions with empathy and practical guidance. Ask thoughtful questions and provide supportive responses.",
        "settings": {
            "model": "gpt-4",
            "temperature": 0.8,
            "max_tokens": 300
        }
    }
    
    test_scenario_flow("Single Participant", scenario_1)
    
    # Test Case 2: Two participants - one with 0 meta tags, one with 3 meta tags
    print("\n" + "=" * 60)
    print("TEST CASE 2: Two participants (0 tags vs 3 tags)")
    print("=" * 60)
    
    scenario_2 = {
        "name": "Workplace Conflict Resolution",
        "participants": [
            {
                "name": "Manager Mike",
                "role": "Team supervisor",
                "perspective": "Believes in maintaining professional standards but struggles with communication",
                "meta_tags": [],  # 0 meta tags
                "initial_message": "I need to address some performance issues with my team, but I want to make sure I'm being fair and constructive."
            },
            {
                "name": "Employee Emma",
                "role": "Team member feeling criticized",
                "perspective": "Feels singled out and unfairly judged by management",
                "meta_tags": ["defensive", "frustrated", "misunderstood"],  # 3 meta tags
                "initial_message": "I feel like I'm constantly being criticized and nothing I do is ever good enough for management."
            }
        ],
        "system_prompt": "You are Driftwood, a workplace mediation specialist. Help resolve professional conflicts by fostering understanding between different perspectives. Focus on constructive solutions.",
        "settings": {
            "model": "gpt-4",
            "temperature": 0.7,
            "max_tokens": 400
        }
    }
    
    test_scenario_flow("Two Participants", scenario_2)
    
    # Test Case 3: Three participants with mixed meta tag counts (2, 1, 3)
    print("\n" + "=" * 60)
    print("TEST CASE 3: Three participants (2, 1, 3 meta tags)")
    print("=" * 60)
    
    scenario_3 = {
        "name": "Family Dinner Discussion",
        "participants": [
            {
                "name": "Parent Pat",
                "role": "Concerned parent",
                "perspective": "Wants to maintain family harmony while addressing important issues",
                "meta_tags": ["worried", "protective"],  # 2 meta tags
                "initial_message": "I'm concerned about some of the choices you kids are making, but I want us to talk about this as a family."
            },
            {
                "name": "Teen Taylor",
                "role": "Independent teenager",
                "perspective": "Feels controlled and wants more freedom",
                "meta_tags": ["rebellious"],  # 1 meta tag
                "initial_message": "I'm not a little kid anymore! I can make my own decisions and I don't need you monitoring everything I do."
            },
            {
                "name": "Sibling Sam",
                "role": "Middle child mediator",
                "perspective": "Caught between parent and sibling, wants peace but also understanding",
                "meta_tags": ["anxious", "diplomatic", "torn"],  # 3 meta tags
                "initial_message": "Can we please just have one family dinner without arguing? I understand both sides but this tension is really hard for me."
            }
        ],
        "system_prompt": "You are Driftwood, a family counseling AI. Help family members communicate more effectively by acknowledging each person's feelings and guiding them toward mutual understanding. Keep responses warm but structured.",
        "settings": {
            "model": "gpt-4",
            "temperature": 0.6,
            "max_tokens": 350
        }
    }
    
    test_scenario_flow("Three Participants", scenario_3)

def test_scenario_flow(test_name, scenario_data):
    """Test the complete flow: create scenario -> run simulation -> verify output"""
    
    try:
        # Step 1: Create scenario
        print(f"\n🔧 Creating scenario: {scenario_data['name']}")
        print(f"   Participants: {len(scenario_data['participants'])}")
        for i, p in enumerate(scenario_data['participants'], 1):
            tag_count = len(p['meta_tags'])
            tags_str = f"[{', '.join(p['meta_tags'])}]" if p['meta_tags'] else "[none]"
            print(f"   - {p['name']}: {tag_count} meta tags {tags_str}")
        
        response = requests.post(f"{BASE_URL}/scenarios", json=scenario_data)
        
        if response.status_code != 200:
            print(f"❌ Failed to create scenario: {response.status_code}")
            print(f"   Error: {response.text}")
            return
        
        scenario = response.json()
        scenario_id = scenario["id"]
        print(f"✅ Scenario created successfully! ID: {scenario_id}")
        
        # Verify scenario data
        print(f"   Saved name: {scenario['name']}")
        print(f"   Participants saved: {len(scenario['participants'])}")
        
        # Step 2: Run simulation
        print(f"\n🚀 Running simulation for scenario {scenario_id}")
        run_response = requests.post(f"{BASE_URL}/run?scenario_id={scenario_id}")
        
        if run_response.status_code != 200:
            print(f"❌ Simulation failed: {run_response.status_code}")
            print(f"   Error: {run_response.text}")
            return
        
        run_data = run_response.json()
        print(f"✅ Simulation completed! Run ID: {run_data['id']}")
        
        # Step 3: Analyze results
        print(f"\n📊 Analyzing conversation log:")
        log = run_data['log']
        print(f"   Total messages: {len(log)}")
        
        # Count messages by speaker
        speaker_counts = {}
        for msg in log:
            speaker = msg['speaker']
            speaker_counts[speaker] = speaker_counts.get(speaker, 0) + 1
        
        for speaker, count in speaker_counts.items():
            print(f"   - {speaker}: {count} messages")
        
        # Show conversation flow
        print(f"\n💬 Conversation Flow:")
        for i, msg in enumerate(log, 1):
            content_preview = msg['content'][:80] + "..." if len(msg['content']) > 80 else msg['content']
            print(f"   {i}. {msg['speaker']}: {content_preview}")
        
        # Verify expected behavior
        expected_messages = len(scenario_data['participants']) * 2  # Each participant + AI response
        if len(log) == expected_messages:
            print(f"✅ Expected message count: {expected_messages} (got {len(log)})")
        else:
            print(f"⚠️  Expected {expected_messages} messages, got {len(log)}")
        
        # Verify each participant spoke
        participant_names = [p['name'] for p in scenario_data['participants']]
        speakers_in_log = set(msg['speaker'] for msg in log if msg['speaker'] != 'AI')
        
        if set(participant_names) == speakers_in_log:
            print(f"✅ All participants spoke: {list(speakers_in_log)}")
        else:
            print(f"⚠️  Expected speakers {participant_names}, found {list(speakers_in_log)}")
        
        print(f"\n🎉 {test_name} test completed successfully!")
        
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
        print("❌ Cannot connect to server. Please start the server with:")
        print("   source venv/bin/activate && python main.py")
        return False

if __name__ == "__main__":
    print("🧪 Testing Phase 5: Scenario Builder Interface")
    print("Testing various participant and meta tag configurations")
    print()
    
    if not verify_server_connection():
        exit(1)
    
    test_scenario_creation_and_simulation()
    
    print("\n" + "=" * 60)
    print("🏁 All Phase 5 tests completed!")
    print("=" * 60)