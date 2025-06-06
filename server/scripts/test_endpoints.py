import requests
import json

BASE_URL = "http://localhost:5000/api"

def test_endpoint(method, endpoint, data=None, params=None):
    """Test an endpoint and print the result"""
    url = f"{BASE_URL}/{endpoint}"
    print(f"\nTesting {method} {endpoint}")
    
    try:
        if method == 'GET':
            response = requests.get(url, params=params)
        else:
            response = requests.post(url, json=data)
            
        print(f"Status Code: {response.status_code}")
        print("Response:", json.dumps(response.json(), indent=2))
        return response.status_code == 200
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return False

def run_tests():
    """Run all endpoint tests"""
    success = 0
    total = 0
    
    # Test AI endpoints
    print("\n=== Testing AI Endpoints ===")
    
    total += 1
    if test_endpoint('POST', 'ai/first-aid', {
        "condition": "bleeding",
        "language": "en"
    }):
        success += 1
        
    total += 1
    if test_endpoint('POST', 'ai/health-advice', {
        "query": "headache remedies",
        "language": "sw"
    }):
        success += 1
        
    # Test Hospital endpoints
    print("\n=== Testing Hospital Endpoints ===")
    
    total += 1
    if test_endpoint('GET', 'hospitals'):
        success += 1
        
    total += 1
    if test_endpoint('GET', 'hospitals/zones'):
        success += 1
        
    total += 1
    if test_endpoint('GET', 'hospitals/regions', params={'zone': 'Eastern'}):
        success += 1
        
    total += 1
    if test_endpoint('GET', 'hospitals/districts', params={'region': 'Dar es Salaam'}):
        success += 1
    
    # Test SMS endpoints
    print("\n=== Testing SMS Endpoints ===")
    
    total += 1
    if test_endpoint('POST', 'sms/send', {
        "phone_numbers": ["+255123456789"],
        "message": "Test message"
    }):
        success += 1
        
    # Test USSD endpoints
    print("\n=== Testing USSD Endpoints ===")
    
    total += 1
    if test_endpoint('POST', 'ussd/callback', {
        "sessionId": "test-session",
        "phoneNumber": "+255123456789",
        "text": ""
    }):
        success += 1
        
    total += 1
    if test_endpoint('POST', 'ussd/hospitals', {
        "zone": "Eastern",
        "region": "Dar es Salaam",
        "district": "Ilala"
    }):
        success += 1
        
    # Test Voice endpoints
    print("\n=== Testing Voice Endpoints ===")
    
    total += 1
    if test_endpoint('POST', 'voice/call', {
        "phone_number": "+255123456789"
    }):
        success += 1
    
    print(f"\nTest Summary: {success}/{total} endpoints working")
    
if __name__ == "__main__":
    run_tests()
