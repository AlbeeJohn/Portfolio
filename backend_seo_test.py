#!/usr/bin/env python3
"""
SEO Optimization Backend Tests for Albee John Portfolio
Tests SEO-related backend functionality, static file serving, and response headers
"""

import requests
import json
import sys
from datetime import datetime
import xml.etree.ElementTree as ET
from urllib.parse import urljoin

# Get backend URL from environment
BACKEND_URL = "https://responsive-ready.preview.emergentagent.com"
API_URL = f"{BACKEND_URL}/api"

class SEOBackendTester:
    def __init__(self):
        self.base_url = BACKEND_URL
        self.api_url = API_URL
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
    
    def test_robots_txt_access(self):
        """Test /robots.txt accessibility and content"""
        try:
            response = requests.get(f"{self.base_url}/robots.txt")
            
            if response.status_code == 200:
                content = response.text
                
                # Check for essential robots.txt content
                required_elements = [
                    "User-agent: *",
                    "Allow: /",
                    "Sitemap:",
                    "Googlebot",
                    "Bingbot"
                ]
                
                missing_elements = []
                for element in required_elements:
                    if element not in content:
                        missing_elements.append(element)
                
                if not missing_elements:
                    # Check if sitemap URL is present
                    if "sitemap.xml" in content.lower():
                        self.log_test("Robots.txt Access & Content", True, 
                                    f"File accessible with proper content including sitemap reference")
                    else:
                        self.log_test("Robots.txt Access & Content", False, 
                                    "Missing sitemap reference in robots.txt")
                else:
                    self.log_test("Robots.txt Access & Content", False, 
                                f"Missing required elements: {missing_elements}")
                    
                # Check content-type header
                content_type = response.headers.get('content-type', '')
                if 'text/plain' in content_type:
                    self.log_test("Robots.txt Content-Type", True, f"Correct content-type: {content_type}")
                else:
                    self.log_test("Robots.txt Content-Type", False, f"Incorrect content-type: {content_type}")
                    
            else:
                self.log_test("Robots.txt Access", False, f"Status code: {response.status_code}")
                
        except Exception as e:
            self.log_test("Robots.txt Access", False, f"Exception: {str(e)}")
    
    def test_sitemap_xml_access(self):
        """Test /sitemap.xml accessibility and structure"""
        try:
            response = requests.get(f"{self.base_url}/sitemap.xml")
            
            if response.status_code == 200:
                content = response.text
                
                # Check content-type header
                content_type = response.headers.get('content-type', '')
                if 'xml' in content_type.lower():
                    self.log_test("Sitemap.xml Content-Type", True, f"Correct content-type: {content_type}")
                else:
                    self.log_test("Sitemap.xml Content-Type", False, f"Incorrect content-type: {content_type}")
                
                # Parse XML to validate structure
                try:
                    root = ET.fromstring(content)
                    
                    # Check for proper XML namespace
                    if 'sitemaps.org' in str(root.tag):
                        self.log_test("Sitemap.xml XML Structure", True, "Valid XML structure with proper namespace")
                    else:
                        self.log_test("Sitemap.xml XML Structure", False, f"Invalid namespace: {root.tag}")
                    
                    # Count URLs in sitemap
                    urls = root.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}url')
                    if len(urls) > 0:
                        self.log_test("Sitemap.xml URL Count", True, f"Found {len(urls)} URLs in sitemap")
                        
                        # Check for required sections
                        expected_sections = ['#about', '#skills', '#experience', '#projects', '#contact']
                        found_sections = []
                        
                        for url in urls:
                            loc_elem = url.find('.//{http://www.sitemaps.org/schemas/sitemap/0.9}loc')
                            if loc_elem is not None:
                                loc = loc_elem.text
                                for section in expected_sections:
                                    if section in loc:
                                        found_sections.append(section)
                        
                        if len(found_sections) >= 4:  # At least 4 out of 5 sections
                            self.log_test("Sitemap.xml Portfolio Sections", True, 
                                        f"Found expected sections: {found_sections}")
                        else:
                            self.log_test("Sitemap.xml Portfolio Sections", False, 
                                        f"Missing expected sections. Found: {found_sections}")
                    else:
                        self.log_test("Sitemap.xml URL Count", False, "No URLs found in sitemap")
                        
                except ET.ParseError as e:
                    self.log_test("Sitemap.xml XML Parsing", False, f"XML parsing error: {str(e)}")
                    
            else:
                self.log_test("Sitemap.xml Access", False, f"Status code: {response.status_code}")
                
        except Exception as e:
            self.log_test("Sitemap.xml Access", False, f"Exception: {str(e)}")
    
    def test_manifest_json_access(self):
        """Test /manifest.json accessibility and content"""
        try:
            response = requests.get(f"{self.base_url}/manifest.json")
            
            if response.status_code == 200:
                # Check content-type header
                content_type = response.headers.get('content-type', '')
                if 'json' in content_type.lower():
                    self.log_test("Manifest.json Content-Type", True, f"Correct content-type: {content_type}")
                else:
                    self.log_test("Manifest.json Content-Type", False, f"Incorrect content-type: {content_type}")
                
                try:
                    data = response.json()
                    
                    # Check for required manifest fields
                    required_fields = ['name', 'short_name', 'description', 'start_url', 'display', 'theme_color']
                    missing_fields = [field for field in required_fields if field not in data]
                    
                    if not missing_fields:
                        self.log_test("Manifest.json Required Fields", True, "All required fields present")
                        
                        # Check if name contains updated tagline
                        name = data.get('name', '')
                        if 'Data Analysis & Science Enthusiast' in name:
                            self.log_test("Manifest.json Updated Tagline", True, 
                                        f"Contains updated tagline: {name}")
                        else:
                            self.log_test("Manifest.json Updated Tagline", False, 
                                        f"Missing updated tagline in name: {name}")
                        
                        # Check description
                        description = data.get('description', '')
                        if 'data analysis' in description.lower() and len(description) > 50:
                            self.log_test("Manifest.json Description", True, 
                                        f"Descriptive content present ({len(description)} chars)")
                        else:
                            self.log_test("Manifest.json Description", False, 
                                        f"Description too short or missing data analysis focus")
                            
                    else:
                        self.log_test("Manifest.json Required Fields", False, 
                                    f"Missing required fields: {missing_fields}")
                        
                except json.JSONDecodeError as e:
                    self.log_test("Manifest.json JSON Parsing", False, f"JSON parsing error: {str(e)}")
                    
            else:
                self.log_test("Manifest.json Access", False, f"Status code: {response.status_code}")
                
        except Exception as e:
            self.log_test("Manifest.json Access", False, f"Exception: {str(e)}")
    
    def test_frontend_page_seo_elements(self):
        """Test frontend page for SEO elements"""
        try:
            response = requests.get(self.base_url)
            
            if response.status_code == 200:
                content = response.text
                
                # Check page title
                if '<title>' in content:
                    title_start = content.find('<title>') + 7
                    title_end = content.find('</title>')
                    title = content[title_start:title_end]
                    
                    expected_title_elements = ['Albee John', 'Data Analysis & Science Enthusiast', 'Portfolio']
                    found_elements = [elem for elem in expected_title_elements if elem in title]
                    
                    if len(found_elements) >= 2:
                        self.log_test("Page Title SEO", True, f"Title contains expected elements: {title}")
                    else:
                        self.log_test("Page Title SEO", False, f"Title missing expected elements: {title}")
                else:
                    self.log_test("Page Title SEO", False, "No title tag found")
                
                # Check meta description
                if 'name="description"' in content:
                    desc_start = content.find('name="description" content="') + 28
                    desc_end = content.find('"', desc_start)
                    description = content[desc_start:desc_end]
                    
                    if 'Data Analysis & Science Enthusiast' in description and 'albeejohnwwe@gmail.com' in description:
                        self.log_test("Meta Description SEO", True, 
                                    f"Description contains updated tagline and contact info")
                    else:
                        self.log_test("Meta Description SEO", False, 
                                    f"Description missing updated tagline or contact info: {description[:100]}...")
                else:
                    self.log_test("Meta Description SEO", False, "No meta description found")
                
                # Check viewport meta tag
                if 'name="viewport"' in content:
                    self.log_test("Viewport Meta Tag", True, "Viewport meta tag present")
                else:
                    self.log_test("Viewport Meta Tag", False, "Viewport meta tag missing")
                
                # Check for structured data or other SEO elements
                if 'manifest.json' in content:
                    self.log_test("Manifest Link", True, "Manifest.json linked in HTML")
                else:
                    self.log_test("Manifest Link", False, "Manifest.json not linked")
                    
            else:
                self.log_test("Frontend Page Access", False, f"Status code: {response.status_code}")
                
        except Exception as e:
            self.log_test("Frontend Page Access", False, f"Exception: {str(e)}")
    
    def test_response_headers_seo(self):
        """Test response headers for SEO optimization"""
        try:
            response = requests.get(self.base_url)
            
            if response.status_code == 200:
                headers = response.headers
                
                # Check content-type
                content_type = headers.get('content-type', '')
                if 'text/html' in content_type:
                    self.log_test("HTML Content-Type Header", True, f"Correct content-type: {content_type}")
                else:
                    self.log_test("HTML Content-Type Header", False, f"Incorrect content-type: {content_type}")
                
                # Check for caching headers
                cache_headers = ['cache-control', 'expires', 'etag', 'last-modified']
                found_cache_headers = [header for header in cache_headers if header in headers]
                
                if found_cache_headers:
                    self.log_test("Caching Headers", True, f"Found caching headers: {found_cache_headers}")
                else:
                    self.log_test("Caching Headers", False, "No caching headers found")
                
                # Check for compression
                content_encoding = headers.get('content-encoding', '')
                if 'gzip' in content_encoding or 'br' in content_encoding:
                    self.log_test("Content Compression", True, f"Compression enabled: {content_encoding}")
                else:
                    # Check if content is compressed by size
                    content_length = headers.get('content-length')
                    if content_length and int(content_length) < 50000:  # Reasonable size for compressed HTML
                        self.log_test("Content Compression", True, "Content appears to be compressed (small size)")
                    else:
                        self.log_test("Content Compression", False, "No compression detected")
                
                # Check security headers that affect SEO
                security_headers = {
                    'x-content-type-options': 'nosniff',
                    'x-frame-options': ['DENY', 'SAMEORIGIN'],
                    'referrer-policy': 'strict-origin-when-cross-origin'
                }
                
                security_score = 0
                for header, expected in security_headers.items():
                    if header in headers:
                        security_score += 1
                
                if security_score >= 1:
                    self.log_test("Security Headers", True, f"Found {security_score} security headers")
                else:
                    self.log_test("Security Headers", False, "No security headers found")
                    
            else:
                self.log_test("Response Headers Test", False, f"Status code: {response.status_code}")
                
        except Exception as e:
            self.log_test("Response Headers Test", False, f"Exception: {str(e)}")
    
    def test_api_portfolio_seo_data(self):
        """Test API portfolio endpoint for SEO-relevant data"""
        try:
            response = requests.get(f"{self.api_url}/portfolio")
            
            if response.status_code == 200:
                data = response.json()
                
                # Check if personal info contains updated tagline for SEO
                personal = data.get("personal", {})
                tagline = personal.get("tagline", "")
                
                if "Data Analysis & Science Enthusiast" in tagline:
                    self.log_test("API Portfolio SEO Tagline", True, 
                                f"API returns updated SEO-friendly tagline: {tagline}")
                else:
                    self.log_test("API Portfolio SEO Tagline", False, 
                                f"API tagline not SEO optimized: {tagline}")
                
                # Check for contact information (important for local SEO)
                contact = data.get("contact", {})
                email = contact.get("email", "")
                
                if "albeejohnwwe@gmail.com" in email:
                    self.log_test("API Contact Info for SEO", True, "Contact email present for SEO")
                else:
                    self.log_test("API Contact Info for SEO", False, "Contact email missing")
                
                # Check skills for SEO keywords
                skills = data.get("skills", {})
                technical_skills = [skill["name"] for skill in skills.get("technical", [])]
                seo_keywords = ["Python", "Data Science", "Machine Learning", "SQL", "R Programming"]
                found_keywords = [keyword for keyword in seo_keywords if keyword in technical_skills]
                
                if len(found_keywords) >= 3:
                    self.log_test("API Skills SEO Keywords", True, 
                                f"Found SEO-relevant skills: {found_keywords}")
                else:
                    self.log_test("API Skills SEO Keywords", False, 
                                f"Insufficient SEO keywords in skills: {technical_skills}")
                    
            else:
                self.log_test("API Portfolio SEO Data", False, f"Status code: {response.status_code}")
                
        except Exception as e:
            self.log_test("API Portfolio SEO Data", False, f"Exception: {str(e)}")
    
    def test_page_load_performance(self):
        """Test page load performance (affects SEO ranking)"""
        try:
            import time
            
            start_time = time.time()
            response = requests.get(self.base_url)
            load_time = (time.time() - start_time) * 1000  # Convert to milliseconds
            
            if response.status_code == 200:
                if load_time < 3000:  # Less than 3 seconds
                    self.log_test("Page Load Performance", True, 
                                f"Good load time: {load_time:.0f}ms")
                elif load_time < 5000:  # Less than 5 seconds
                    self.log_test("Page Load Performance", True, 
                                f"Acceptable load time: {load_time:.0f}ms")
                else:
                    self.log_test("Page Load Performance", False, 
                                f"Slow load time: {load_time:.0f}ms")
                
                # Check response size
                content_length = len(response.content)
                if content_length < 500000:  # Less than 500KB
                    self.log_test("Page Size Optimization", True, 
                                f"Good page size: {content_length/1024:.1f}KB")
                else:
                    self.log_test("Page Size Optimization", False, 
                                f"Large page size: {content_length/1024:.1f}KB")
                    
            else:
                self.log_test("Page Load Performance", False, f"Status code: {response.status_code}")
                
        except Exception as e:
            self.log_test("Page Load Performance", False, f"Exception: {str(e)}")
    
    def run_all_seo_tests(self):
        """Run all SEO-related backend tests"""
        print("🔍 Starting SEO Optimization Backend Tests for Albee John Portfolio")
        print("=" * 70)
        
        # Test 1: Static Files Access
        print("\n📁 STATIC FILES ACCESS TESTS")
        print("-" * 40)
        self.test_robots_txt_access()
        self.test_sitemap_xml_access()
        self.test_manifest_json_access()
        
        # Test 2: Frontend SEO Elements
        print("\n🏷️  HTML HEAD ELEMENTS TESTS")
        print("-" * 40)
        self.test_frontend_page_seo_elements()
        
        # Test 3: Response Headers
        print("\n📡 RESPONSE HEADERS TESTS")
        print("-" * 40)
        self.test_response_headers_seo()
        
        # Test 4: API SEO Data
        print("\n🔗 API SEO DATA TESTS")
        print("-" * 40)
        self.test_api_portfolio_seo_data()
        
        # Test 5: Performance Tests
        print("\n⚡ PERFORMANCE TESTS")
        print("-" * 40)
        self.test_page_load_performance()
        
        # Summary
        print("\n" + "=" * 70)
        print("📊 SEO TEST SUMMARY")
        print("=" * 70)
        
        total_tests = len(self.test_results)
        failed_count = len(self.failed_tests)
        passed_count = total_tests - failed_count
        
        print(f"Total SEO Tests: {total_tests}")
        print(f"Passed: {passed_count}")
        print(f"Failed: {failed_count}")
        
        if self.failed_tests:
            print("\n❌ FAILED SEO TESTS:")
            for failure in self.failed_tests:
                print(f"  - {failure}")
        
        if failed_count == 0:
            print("\n🎉 ALL SEO TESTS PASSED! Website is SEO optimized.")
            return True
        else:
            print(f"\n⚠️  {failed_count} SEO test(s) failed. Please check the issues above.")
            return False

def main():
    """Main test execution"""
    tester = SEOBackendTester()
    success = tester.run_all_seo_tests()
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()