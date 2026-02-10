"""
Simple API test script to verify all endpoints are working
Run this after starting the server: python manage.py runserver
Then in another terminal: python test_api.py
"""

import requests
import json

BASE_URL = 'http://localhost:8000/api'

def print_response(title, response):
    print(f"\n{'='*60}")
    print(f"TEST: {title}")
    print(f"{'='*60}")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print(f"{'='*60}\n")

def test_registration():
    """Test user registration"""
    url = f"{BASE_URL}/auth/register/"
    data = {
        "email": "teststudent@amit.edu",
        "password": "Test@123456",
        "password2": "Test@123456",
        "name": "Test Student",
        "role": "student"
    }
    response = requests.post(url, json=data)
    print_response("User Registration", response)
    return response.status_code == 201

def test_login():
    """Test user login"""
    url = f"{BASE_URL}/auth/login/"
    data = {
        "email": "teststudent@amit.edu",
        "password": "Test@123456"
    }
    response = requests.post(url, json=data)
    print_response("User Login", response)
    
    if response.status_code == 200:
        return response.json()['tokens']['access']
    return None

def test_verify_token(token):
    """Test token verification"""
    url = f"{BASE_URL}/auth/verify-token/"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    print_response("Token Verification", response)
    return response.status_code == 200

def test_contact_form():
    """Test contact form submission"""
    url = f"{BASE_URL}/contact/submit/"
    data = {
        "name": "John Doe",
        "email": "john@example.com",
        "phone": "+919876543210",
        "message": "This is a test message from the API test script."
    }
    response = requests.post(url, json=data)
    print_response("Contact Form Submission", response)
    return response.status_code == 201

def test_forgot_password():
    """Test forgot password"""
    url = f"{BASE_URL}/auth/forgot-password/"
    data = {
        "email": "teststudent@amit.edu"
    }
    response = requests.post(url, json=data)
    print_response("Forgot Password", response)
    return response.status_code == 200

def main():
    print("\n" + "="*60)
    print("COLLEGE MANAGEMENT SYSTEM - API TESTS")
    print("="*60)
    print("\nMake sure the server is running: python manage.py runserver")
    print("\nStarting tests...\n")
    
    results = {
        "Registration": False,
        "Login": False,
        "Token Verification": False,
        "Contact Form": False,
        "Forgot Password": False
    }
    
    try:
        # Test 1: Registration
        results["Registration"] = test_registration()
        
        # Test 2: Login
        token = test_login()
        results["Login"] = token is not None
        
        # Test 3: Token Verification
        if token:
            results["Token Verification"] = test_verify_token(token)
        
        # Test 4: Contact Form
        results["Contact Form"] = test_contact_form()
        
        # Test 5: Forgot Password
        results["Forgot Password"] = test_forgot_password()
        
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: Could not connect to server!")
        print("Make sure the server is running: python manage.py runserver")
        return
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        return
    
    # Print summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    for test_name, passed in results.items():
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{test_name}: {status}")
    
    total = len(results)
    passed = sum(results.values())
    
    print(f"\nTotal: {passed}/{total} tests passed")
    print("="*60 + "\n")
    
    if passed == total:
        print("🎉 All tests passed! Your backend is working perfectly!")
    else:
        print("⚠️ Some tests failed. Check the output above for details.")

if __name__ == "__main__":
    main()
