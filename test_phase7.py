import requests
import json
from dotenv import load_dotenv
import time

# Load environment variables
load_dotenv()

BASE_URL = "http://localhost:8000"

def test_history_management():
    """Test Phase 7: Simulation History & Management"""
    
    print("🧪 Testing Phase 7: Simulation History & Management")
    print("Testing history display, starring, and navigation functionality")
    print()
    
    # First, create some test scenarios and runs
    print("📋 Setting up test data...")
    test_runs = create_test_data()
    
    if not test_runs:
        print("❌ Failed to create test data")
        return
    
    print(f"✅ Created {len(test_runs)} test runs")
    
    # Test 1: History retrieval
    print("\n" + "=" * 60)
    print("TEST 1: History Retrieval")
    print("=" * 60)
    
    test_history_retrieval(test_runs)
    
    # Test 2: Star/unstar functionality
    print("\n" + "=" * 60)
    print("TEST 2: Star/Unstar Functionality")
    print("=" * 60)
    
    test_star_functionality(test_runs)
    
    # Test 3: Run details retrieval
    print("\n" + "=" * 60)
    print("TEST 3: Run Details Retrieval")
    print("=" * 60)
    
    test_run_details(test_runs)
    
    # Test 4: Data persistence
    print("\n" + "=" * 60)
    print("TEST 4: Data Persistence")
    print("=" * 60)
    
    test_data_persistence(test_runs)

def create_test_data():
    """Create test scenarios and runs for history testing"""
    
    test_scenarios = [
        {
            "name": "Quick Therapy Session",
            "participants": [
                {
                    "name": "Sarah",
                    "role": "Client seeking guidance",
                    "perspective": "Feeling overwhelmed with work stress",
                    "meta_tags": ["stressed", "overwhelmed"],
                    "initial_message": "I've been feeling really stressed at work lately and I don't know how to handle it."
                }
            ],
            "system_prompt": "You are a supportive therapist. Provide brief, helpful guidance.",
            "settings": {"model": "gpt-4", "temperature": 0.7, "max_tokens": 200}
        },
        {
            "name": "Relationship Conflict",
            "participants": [
                {
                    "name": "Alex",
                    "role": "Frustrated partner",
                    "perspective": "Feels unheard in the relationship",
                    "meta_tags": ["frustrated", "lonely"],
                    "initial_message": "I feel like we never really talk anymore. We just go through the motions."
                },
                {
                    "name": "Jamie",
                    "role": "Confused partner",
                    "perspective": "Doesn't understand what's wrong",
                    "meta_tags": ["confused"],
                    "initial_message": "I thought things were fine between us. I'm not sure what you mean."
                }
            ],
            "system_prompt": "You are a couples counselor. Help partners communicate better.",
            "settings": {"model": "gpt-4", "temperature": 0.6, "max_tokens": 300}
        },
        {
            "name": "Family Meeting",
            "participants": [
                {
                    "name": "Parent Pat",
                    "role": "Concerned parent",
                    "perspective": "Worried about family dynamics",
                    "meta_tags": ["worried", "caring"],
                    "initial_message": "I think we need to talk about how we communicate as a family."
                },
                {
                    "name": "Teen Tyler",
                    "role": "Resistant teenager",
                    "perspective": "Feels controlled and misunderstood",
                    "meta_tags": ["rebellious", "misunderstood"],
                    "initial_message": "Why do we always have to have these family meetings? I'm fine."
                },
                {
                    "name": "Grandparent Gail",
                    "role": "Peacemaker elder",
                    "perspective": "Wants to help bridge generational gaps",
                    "meta_tags": ["wise", "diplomatic"],
                    "initial_message": "I think we can all benefit from understanding each other better."
                }
            ],
            "system_prompt": "You are a family counselor. Help family members understand each other.",
            "settings": {"model": "gpt-4", "temperature": 0.8, "max_tokens": 400}
        }
    ]
    
    created_runs = []
    
    for i, scenario_data in enumerate(test_scenarios):
        try:
            # Create scenario
            scenario_response = requests.post(f"{BASE_URL}/scenarios", json=scenario_data)
            if scenario_response.status_code != 200:
                print(f"❌ Failed to create scenario {i+1}: {scenario_response.status_code}")
                continue
            
            scenario = scenario_response.json()
            print(f"   📝 Created scenario: {scenario['name']}")
            
            # Run simulation
            run_response = requests.post(f"{BASE_URL}/run?scenario_id={scenario['id']}")
            if run_response.status_code != 200:
                print(f"❌ Failed to run simulation {i+1}: {run_response.status_code}")
                continue
            
            run = run_response.json()
            created_runs.append(run)
            print(f"   ✅ Created run: {run['id']}")
            
            # Small delay to ensure different timestamps
            time.sleep(1)
            
        except Exception as e:
            print(f"❌ Error creating test data {i+1}: {e}")
    
    return created_runs

def test_history_retrieval(test_runs):
    """Test retrieving simulation history"""
    
    try:
        print("🔍 Testing history retrieval...")
        
        # Get all runs
        response = requests.get(f"{BASE_URL}/runs")
        
        if response.status_code != 200:
            print(f"❌ Failed to retrieve history: {response.status_code}")
            return
        
        runs = response.json()
        print(f"✅ Retrieved {len(runs)} runs from history")
        
        # Verify structure
        if runs:
            first_run = runs[0]
            required_fields = ['id', 'scenario_id', 'timestamp', 'starred', 'scenario_name']
            
            print("🔍 Verifying run structure:")
            for field in required_fields:
                if field in first_run:
                    print(f"   ✅ {field}: {first_run[field]}")
                else:
                    print(f"   ❌ {field}: missing")
        
        # Verify our test runs are in the history
        test_run_ids = {run['id'] for run in test_runs}
        history_run_ids = {run['id'] for run in runs}
        
        if test_run_ids.issubset(history_run_ids):
            print("✅ All test runs found in history")
        else:
            missing = test_run_ids - history_run_ids
            print(f"⚠️  Missing runs in history: {missing}")
        
        # Test sorting (should be latest first)
        if len(runs) > 1:
            timestamps = [run['timestamp'] for run in runs]
            is_sorted = all(timestamps[i] >= timestamps[i+1] for i in range(len(timestamps)-1))
            
            if is_sorted:
                print("✅ Runs are properly sorted (latest first)")
            else:
                print("⚠️  Runs are not properly sorted")
        
    except Exception as e:
        print(f"❌ History retrieval test failed: {e}")

def test_star_functionality(test_runs):
    """Test starring and unstarring runs"""
    
    if not test_runs:
        print("❌ No test runs available for star testing")
        return
    
    try:
        run_id = test_runs[0]['id']
        print(f"🌟 Testing star functionality with run: {run_id}")
        
        # Test starring
        print("   📌 Testing star operation...")
        star_response = requests.patch(f"{BASE_URL}/runs/{run_id}/star", json={"starred": True})
        
        if star_response.status_code != 200:
            print(f"❌ Failed to star run: {star_response.status_code}")
            return
        
        starred_run = star_response.json()
        if starred_run['starred']:
            print("   ✅ Run successfully starred")
        else:
            print("   ❌ Run not marked as starred")
        
        # Test unstarring
        print("   📌 Testing unstar operation...")
        unstar_response = requests.patch(f"{BASE_URL}/runs/{run_id}/star", json={"starred": False})
        
        if unstar_response.status_code != 200:
            print(f"❌ Failed to unstar run: {unstar_response.status_code}")
            return
        
        unstarred_run = unstar_response.json()
        if not unstarred_run['starred']:
            print("   ✅ Run successfully unstarred")
        else:
            print("   ❌ Run still marked as starred")
        
        # Test multiple stars
        print("   📌 Testing multiple star operations...")
        for i, run in enumerate(test_runs[:2]):  # Star first 2 runs
            star_response = requests.patch(f"{BASE_URL}/runs/{run['id']}/star", json={"starred": True})
            if star_response.status_code == 200:
                print(f"   ✅ Run {i+1} starred successfully")
            else:
                print(f"   ❌ Failed to star run {i+1}")
        
        # Verify starred runs in history
        print("   🔍 Verifying starred runs in history...")
        history_response = requests.get(f"{BASE_URL}/runs")
        if history_response.status_code == 200:
            runs = history_response.json()
            starred_count = sum(1 for run in runs if run['starred'])
            print(f"   ✅ Found {starred_count} starred runs in history")
        
    except Exception as e:
        print(f"❌ Star functionality test failed: {e}")

def test_run_details(test_runs):
    """Test retrieving detailed run information"""
    
    if not test_runs:
        print("❌ No test runs available for details testing")
        return
    
    try:
        run_id = test_runs[0]['id']
        print(f"📋 Testing run details retrieval for: {run_id}")
        
        # Get run details
        response = requests.get(f"{BASE_URL}/runs/{run_id}")
        
        if response.status_code != 200:
            print(f"❌ Failed to retrieve run details: {response.status_code}")
            return
        
        run_details = response.json()
        print("✅ Run details retrieved successfully")
        
        # Verify detailed structure
        detailed_fields = ['id', 'scenario_id', 'timestamp', 'starred', 'log']
        print("🔍 Verifying detailed run structure:")
        
        for field in detailed_fields:
            if field in run_details:
                if field == 'log':
                    print(f"   ✅ {field}: {len(run_details[field])} messages")
                else:
                    print(f"   ✅ {field}: present")
            else:
                print(f"   ❌ {field}: missing")
        
        # Verify log structure
        if 'log' in run_details and run_details['log']:
            first_message = run_details['log'][0]
            message_fields = ['speaker', 'content', 'timestamp']
            
            print("🔍 Verifying message structure:")
            for field in message_fields:
                if field in first_message:
                    print(f"   ✅ {field}: present")
                else:
                    print(f"   ❌ {field}: missing")
        
    except Exception as e:
        print(f"❌ Run details test failed: {e}")

def test_data_persistence(test_runs):
    """Test that data persists correctly"""
    
    print("💾 Testing data persistence...")
    
    try:
        # Get current history
        initial_response = requests.get(f"{BASE_URL}/runs")
        if initial_response.status_code != 200:
            print("❌ Failed to get initial history")
            return
        
        initial_runs = initial_response.json()
        initial_count = len(initial_runs)
        
        print(f"📊 Initial run count: {initial_count}")
        
        # Create a new run
        new_scenario = {
            "name": "Persistence Test",
            "participants": [
                {
                    "name": "Test User",
                    "role": "Test participant",
                    "perspective": "Testing data persistence",
                    "meta_tags": ["test"],
                    "initial_message": "This is a test message for persistence."
                }
            ],
            "system_prompt": "You are a test AI. Respond briefly.",
            "settings": {"model": "gpt-4", "temperature": 0.5, "max_tokens": 100}
        }
        
        # Create scenario and run
        scenario_response = requests.post(f"{BASE_URL}/scenarios", json=new_scenario)
        if scenario_response.status_code != 200:
            print("❌ Failed to create test scenario")
            return
        
        scenario = scenario_response.json()
        run_response = requests.post(f"{BASE_URL}/run?scenario_id={scenario['id']}")
        if run_response.status_code != 200:
            print("❌ Failed to create test run")
            return
        
        new_run = run_response.json()
        print(f"✅ Created new test run: {new_run['id']}")
        
        # Verify the run appears in history
        final_response = requests.get(f"{BASE_URL}/runs")
        if final_response.status_code != 200:
            print("❌ Failed to get final history")
            return
        
        final_runs = final_response.json()
        final_count = len(final_runs)
        
        if final_count == initial_count + 1:
            print("✅ Run count increased correctly")
        else:
            print(f"⚠️  Expected {initial_count + 1} runs, got {final_count}")
        
        # Verify the new run is in the list
        new_run_ids = {run['id'] for run in final_runs}
        if new_run['id'] in new_run_ids:
            print("✅ New run found in history")
        else:
            print("❌ New run not found in history")
        
        # Test starring persistence
        star_response = requests.patch(f"{BASE_URL}/runs/{new_run['id']}/star", json={"starred": True})
        if star_response.status_code == 200:
            print("✅ Run starred successfully")
            
            # Verify star persists
            check_response = requests.get(f"{BASE_URL}/runs")
            if check_response.status_code == 200:
                check_runs = check_response.json()
                starred_run = next((run for run in check_runs if run['id'] == new_run['id']), None)
                
                if starred_run and starred_run['starred']:
                    print("✅ Star status persisted correctly")
                else:
                    print("❌ Star status not persisted")
        
    except Exception as e:
        print(f"❌ Data persistence test failed: {e}")

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
    
    test_history_management()
    
    print("\n" + "=" * 60)
    print("🏁 Phase 7 History Management tests completed!")
    print("✨ The history interface should now display:")
    print("   - List of all simulation runs (latest first)")
    print("   - Star/unstar functionality with visual indicators")
    print("   - Run metadata (timestamp, scenario name)")
    print("   - Filter buttons (All Runs / Starred)")
    print("   - View buttons that open conversation viewer")
    print("   - Persistent data across sessions")
    print("=" * 60)