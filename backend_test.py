#!/usr/bin/env python3
"""
Comprehensive Backend API Tests for Albee John Portfolio
Tests all API endpoints with proper validation and error handling
"""

import requests
import json
import sys
from datetime import datetime
import uuid

# Get backend URL from environment
BACKEND_URL = "https://responsive-ready.preview.emergentagent.com/api"

class PortfolioAPITester:
    def __init__(self):
        self.base_url = BACKEND_URL
        self.test_results = []
        self.failed_tests = []
        
    def log_test(self, test_name, success, details=""):
        """Log test results"""
        status = "✅ PASS" if success else "❌ FAIL"
        result = f"{status} {test_name}"
        if details:
            result += f" - {details}"
        
        self.test_results.append(result)
        if not success:
            self.failed_tests.append(f"{test_name}: {details}")
        print(result)
        
    def test_root_endpoint(self):
        """Test GET /api/ - Root endpoint"""
        try:
            response = requests.get(f"{self.base_url}/")
            
            if response.status_code == 200:
                data = response.json()
                expected_message = "Albee John Portfolio API - Data Science Professional"
                
                if "message" in data and expected_message in data["message"]:
                    self.log_test("Root Endpoint", True, f"Returned correct message: {data['message']}")
                else:
                    self.log_test("Root Endpoint", False, f"Unexpected message: {data}")
            else:
                self.log_test("Root Endpoint", False, f"Status code: {response.status_code}")
                
        except Exception as e:
            self.log_test("Root Endpoint", False, f"Exception: {str(e)}")
    
    def test_portfolio_endpoint(self):
        """Test GET /api/portfolio - Portfolio data retrieval"""
        try:
            response = requests.get(f"{self.base_url}/portfolio")
            
            if response.status_code == 200:
                data = response.json()
                
                # Verify required sections exist
                required_sections = ["personal", "skills", "experience", "projects", "contact"]
                missing_sections = [section for section in required_sections if section not in data]
                
                if missing_sections:
                    self.log_test("Portfolio Data Structure", False, f"Missing sections: {missing_sections}")
                    return
                
                # Verify personal info
                personal = data.get("personal", {})
                if personal.get("tagline") == "Data Scientist & Analytics Professional":
                    self.log_test("Portfolio Personal Info", True, "Correct tagline found")
                else:
                    self.log_test("Portfolio Personal Info", False, f"Incorrect tagline: {personal.get('tagline')}")
                
                # Verify skills include expected data science skills
                skills = data.get("skills", {})
                technical_skills = [skill["name"] for skill in skills.get("technical", [])]
                expected_skills = ["Python", "R Programming", "SQL", "Data Science", "Machine Learning"]
                found_skills = [skill for skill in expected_skills if skill in technical_skills]
                
                if len(found_skills) >= 4:  # At least 4 out of 5 expected skills
                    self.log_test("Portfolio Skills", True, f"Found expected skills: {found_skills}")
                else:
                    self.log_test("Portfolio Skills", False, f"Missing expected skills. Found: {technical_skills}")
                
                # Verify experience includes RM Plc
                experience = data.get("experience", [])
                rm_plc_found = any("RM Plc" in exp.get("company", "") for exp in experience)
                
                if rm_plc_found:
                    self.log_test("Portfolio Experience", True, "RM Plc experience found")
                else:
                    self.log_test("Portfolio Experience", False, "RM Plc experience not found")
                
                # Verify projects include Private Line
                projects = data.get("projects", [])
                private_line_found = any("Private Line" in proj.get("name", "") for proj in projects)
                
                if private_line_found:
                    self.log_test("Portfolio Projects", True, "Private Line project found")
                else:
                    self.log_test("Portfolio Projects", False, "Private Line project not found")
                
                # Verify contact info
                contact = data.get("contact", {})
                if contact.get("email") == "albeejohnwwe@gmail.com":
                    self.log_test("Portfolio Contact", True, "Correct contact email found")
                else:
                    self.log_test("Portfolio Contact", False, f"Incorrect contact email: {contact.get('email')}")
                    
            else:
                self.log_test("Portfolio Endpoint", False, f"Status code: {response.status_code}")
                
        except Exception as e:
            self.log_test("Portfolio Endpoint", False, f"Exception: {str(e)}")
    
    def test_contact_form_submission(self):
        """Test POST /api/contact - Contact form submission"""
        try:
            # Test successful submission
            test_message = {
                "name": "John Doe",
                "email": "john.doe@example.com",
                "subject": "Test Message",
                "message": "This is a test message for the portfolio contact form."
            }
            
            response = requests.post(f"{self.base_url}/contact", json=test_message)
            
            if response.status_code == 200:
                data = response.json()
                if "message" in data and "id" in data:
                    self.log_test("Contact Form Submission", True, f"Message saved with ID: {data['id']}")
                    return data["id"]  # Return ID for later tests
                else:
                    self.log_test("Contact Form Submission", False, f"Unexpected response: {data}")
            else:
                self.log_test("Contact Form Submission", False, f"Status code: {response.status_code}, Response: {response.text}")
                
        except Exception as e:
            self.log_test("Contact Form Submission", False, f"Exception: {str(e)}")
        
        return None
    
    def test_contact_form_validation(self):
        """Test POST /api/contact - Contact form validation"""
        try:
            # Test with missing required fields
            invalid_message = {
                "name": "John Doe",
                "email": "",  # Missing email
                "subject": "Test",
                "message": "Test message"
            }
            
            response = requests.post(f"{self.base_url}/contact", json=invalid_message)
            
            # Should return error for missing email
            if response.status_code in [400, 422]:  # Bad request or validation error
                self.log_test("Contact Form Validation", True, f"Properly rejected invalid data (status: {response.status_code})")
            else:
                self.log_test("Contact Form Validation", False, f"Should reject invalid data but got status: {response.status_code}")
                
        except Exception as e:
            self.log_test("Contact Form Validation", False, f"Exception: {str(e)}")
    
    def test_get_contact_messages(self):
        """Test GET /api/contact/messages - Get all contact messages"""
        try:
            response = requests.get(f"{self.base_url}/contact/messages")
            
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, list):
                    self.log_test("Get Contact Messages", True, f"Retrieved {len(data)} messages")
                    
                    # Check if our test message is in the list
                    if data:
                        # Verify message structure
                        first_message = data[0]
                        required_fields = ["id", "name", "email", "subject", "message", "created_at"]
                        missing_fields = [field for field in required_fields if field not in first_message]
                        
                        if not missing_fields:
                            self.log_test("Contact Message Structure", True, "All required fields present")
                        else:
                            self.log_test("Contact Message Structure", False, f"Missing fields: {missing_fields}")
                    
                    return data
                else:
                    self.log_test("Get Contact Messages", False, f"Expected list, got: {type(data)}")
            else:
                self.log_test("Get Contact Messages", False, f"Status code: {response.status_code}")
                
        except Exception as e:
            self.log_test("Get Contact Messages", False, f"Exception: {str(e)}")
        
        return []
    
    def test_mark_message_read(self, message_id):
        """Test PUT /api/contact/messages/{message_id}/read - Mark message as read"""
        if not message_id:
            self.log_test("Mark Message Read", False, "No message ID provided")
            return
            
        try:
            response = requests.put(f"{self.base_url}/contact/messages/{message_id}/read")
            
            if response.status_code == 200:
                data = response.json()
                if "message" in data:
                    self.log_test("Mark Message Read", True, f"Message marked as read: {data['message']}")
                else:
                    self.log_test("Mark Message Read", False, f"Unexpected response: {data}")
            elif response.status_code == 404:
                self.log_test("Mark Message Read", False, "Message not found (404)")
            else:
                self.log_test("Mark Message Read", False, f"Status code: {response.status_code}")
                
        except Exception as e:
            self.log_test("Mark Message Read", False, f"Exception: {str(e)}")
    
    def test_mark_nonexistent_message_read(self):
        """Test marking non-existent message as read"""
        try:
            fake_id = str(uuid.uuid4())
            response = requests.put(f"{self.base_url}/contact/messages/{fake_id}/read")
            
            if response.status_code == 404:
                self.log_test("Mark Nonexistent Message Read", True, "Properly returned 404 for non-existent message")
            else:
                self.log_test("Mark Nonexistent Message Read", False, f"Expected 404, got: {response.status_code}")
                
        except Exception as e:
            self.log_test("Mark Nonexistent Message Read", False, f"Exception: {str(e)}")
    
    def run_all_tests(self):
        """Run all API tests"""
        print("🚀 Starting Albee John Portfolio API Tests")
        print("=" * 60)
        
        # Test 1: Root endpoint
        self.test_root_endpoint()
        
        # Test 2: Portfolio data retrieval
        self.test_portfolio_endpoint()
        
        # Test 3: Contact form submission
        message_id = self.test_contact_form_submission()
        
        # Test 4: Contact form validation
        self.test_contact_form_validation()
        
        # Test 5: Get contact messages
        messages = self.test_get_contact_messages()
        
        # Test 6: Mark message as read (use ID from submission or first message)
        test_message_id = message_id
        if not test_message_id and messages:
            test_message_id = messages[0].get("id")
        
        self.test_mark_message_read(test_message_id)
        
        # Test 7: Error handling for non-existent message
        self.test_mark_nonexistent_message_read()
        
        # Summary
        print("\n" + "=" * 60)
        print("📊 TEST SUMMARY")
        print("=" * 60)
        
        total_tests = len(self.test_results)
        failed_count = len(self.failed_tests)
        passed_count = total_tests - failed_count
        
        print(f"Total Tests: {total_tests}")
        print(f"Passed: {passed_count}")
        print(f"Failed: {failed_count}")
        
        if self.failed_tests:
            print("\n❌ FAILED TESTS:")
            for failure in self.failed_tests:
                print(f"  - {failure}")
        
        if failed_count == 0:
            print("\n🎉 ALL TESTS PASSED! Backend API is working correctly.")
            return True
        else:
            print(f"\n⚠️  {failed_count} test(s) failed. Please check the issues above.")
            return False

def main():
    """Main test execution"""
    tester = PortfolioAPITester()
    success = tester.run_all_tests()
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()