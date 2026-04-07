#!/usr/bin/env python
"""
Test script for NetShield Cracking API
Tests all endpoints and flows
"""

import requests
import json
import time
import sys
from typing import Dict, Any

# Configuration
BASE_URL = "http://localhost:8000/api"
NETWORK_BSSID = "AA:BB:CC:DD:EE:FF"

class CrackingAPITester:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.session = requests.Session()
        self.test_results = []
    
    def log(self, message: str, level: str = "INFO"):
        """Log a message"""
        prefix = {
            "INFO": "ℹ️",
            "SUCCESS": "✅",
            "ERROR": "❌",
            "WARNING": "⚠️"
        }.get(level, "❓")
        
        print(f"{prefix} {message}")
    
    def test_endpoint(self, name: str, method: str, endpoint: str, 
                     data: Dict[str, Any] = None, params: Dict[str, Any] = None,
                     expected_status: int = 200) -> bool:
        """Test an API endpoint"""
        try:
            url = f"{self.base_url}{endpoint}"
            
            if method.upper() == "GET":
                response = self.session.get(url, params=params, timeout=10)
            elif method.upper() == "POST":
                response = self.session.post(url, json=data, params=params, timeout=10)
            else:
                self.log(f"Unknown method: {method}", "ERROR")
                return False
            
            success = response.status_code == expected_status
            status_str = f"{response.status_code}"
            
            if success:
                self.log(f"{name}: {status_str}", "SUCCESS")
                self.test_results.append((name, True, response.json() if response.text else None))
                return True
            else:
                self.log(f"{name}: Expected {expected_status}, got {response.status_code}", "ERROR")
                self.log(f"Response: {response.text[:200]}", "ERROR")
                self.test_results.append((name, False, response.text))
                return False
        
        except requests.exceptions.ConnectionError:
            self.log(f"{name}: Cannot connect to {self.base_url}", "ERROR")
            self.test_results.append((name, False, "Connection error"))
            return False
        except Exception as e:
            self.log(f"{name}: {str(e)}", "ERROR")
            self.test_results.append((name, False, str(e)))
            return False
    
    def run_tests(self):
        """Run all tests"""
        self.log("\n=== NetShield Cracking API Test Suite ===\n")
        
        # Test 1: Health check
        self.log("Testing basic connectivity...")
        self.test_endpoint(
            "Health Check",
            "GET",
            "/cracking/status"
        )
        
        # Test 2: Get available wordlists
        self.log("\nTesting wordlist endpoint...")
        self.test_endpoint(
            "Get Available Wordlists",
            "GET",
            "/cracking/wordlists"
        )
        
        # Test 3: Get cracking methods
        self.log("\nTesting methods endpoint...")
        resp = self.session.get(f"{self.base_url}/cracking/methods", timeout=10)
        if resp.status_code == 200:
            self.log("Get Cracking Methods: 200", "SUCCESS")
            methods_data = resp.json()
            self.log(f"Available methods: {', '.join(methods_data.keys())}", "INFO")
            self.test_results.append(("Get Cracking Methods", True, methods_data))
        else:
            self.log(f"Get Cracking Methods: Expected 200, got {resp.status_code}", "ERROR")
            self.test_results.append(("Get Cracking Methods", False, resp.text))
        
        # Test 4: Get handshake capture guide
        self.log("\nTesting handshake guide endpoint...")
        self.test_endpoint(
            "Get Handshake Capture Guide",
            "GET",
            "/cracking/handshake-capture-guide"
        )
        
        # Test 5: List all jobs (should be empty initially)
        self.log("\nTesting job list endpoint...")
        resp = self.session.get(f"{self.base_url}/cracking/jobs", timeout=10)
        if resp.status_code == 200:
            self.log("List All Jobs: 200", "SUCCESS")
            jobs_data = resp.json()
            self.log(f"Current jobs: {jobs_data['total']}", "INFO")
            self.test_results.append(("List All Jobs", True, jobs_data))
        else:
            self.log(f"List All Jobs: Expected 200, got {resp.status_code}", "ERROR")
            self.test_results.append(("List All Jobs", False, resp.text))
        
        # Test 6: Start a cracking job (simulation mode)
        self.log("\nTesting cracking job start...")
        start_response = self.session.post(
            f"{self.base_url}/cracking/start",
            json={
                "network_bssid": NETWORK_BSSID,
                "method": "aircrack-ng",
                "wordlist": "academic",
                "gpu_enabled": False
            },
            timeout=10
        )
        
        if start_response.status_code == 200:
            self.log("Start Cracking Job: 200", "SUCCESS")
            job_data = start_response.json()
            job_id = job_data.get("job_id")
            self.log(f"Created job: {job_id}", "INFO")
            self.test_results.append(("Start Cracking Job", True, job_data))
            
            # Test 7: Get job status
            self.log("\nTesting job status endpoint...")
            time.sleep(1)  # Wait a bit for job to start
            status_response = self.session.get(
                f"{self.base_url}/cracking/job/{job_id}",
                timeout=10
            )
            
            if status_response.status_code == 200:
                self.log("Get Job Status: 200", "SUCCESS")
                status_data = status_response.json()
                self.log(f"Job status: {status_data['status']} ({status_data['progress']}%)", "INFO")
                self.test_results.append(("Get Job Status", True, status_data))
            else:
                self.log(f"Get Job Status: Expected 200, got {status_response.status_code}", "ERROR")
                self.test_results.append(("Get Job Status", False, status_response.text))
            
            # Test 8: Pause job
            self.log("\nTesting pause job endpoint...")
            pause_response = self.session.post(
                f"{self.base_url}/cracking/job/{job_id}/pause",
                timeout=10
            )
            
            if pause_response.status_code == 200:
                self.log("Pause Job: 200", "SUCCESS")
                self.test_results.append(("Pause Job", True, pause_response.json()))
            else:
                self.log(f"Pause Job: Expected 200, got {pause_response.status_code}", "ERROR")
                self.test_results.append(("Pause Job", False, pause_response.text))
            
            # Test 9: Cancel job
            self.log("\nTesting cancel job endpoint...")
            cancel_response = self.session.post(
                f"{self.base_url}/cracking/job/{job_id}/cancel",
                timeout=10
            )
            
            if cancel_response.status_code == 200:
                self.log("Cancel Job: 200", "SUCCESS")
                self.test_results.append(("Cancel Job", True, cancel_response.json()))
            else:
                self.log(f"Cancel Job: Expected 200, got {cancel_response.status_code}", "ERROR")
                self.test_results.append(("Cancel Job", False, cancel_response.text))
        else:
            self.log(f"Start Cracking Job: Expected 200, got {start_response.status_code}", "ERROR")
            self.log(f"Response: {start_response.text[:200]}", "ERROR")
            self.test_results.append(("Start Cracking Job", False, start_response.text))
        
        # Print summary
        self.print_summary()
    
    def print_summary(self):
        """Print test summary"""
        self.log("\n=== Test Summary ===\n")
        
        passed = sum(1 for _, success, _ in self.test_results if success)
        total = len(self.test_results)
        
        for name, success, data in self.test_results:
            status = "✅ PASS" if success else "❌ FAIL"
            self.log(f"{status}: {name}")
        
        percentage = (passed / total * 100) if total > 0 else 0
        self.log(f"\nResult: {passed}/{total} passed ({percentage:.1f}%)")
        
        return passed == total

if __name__ == "__main__":
    tester = CrackingAPITester(BASE_URL)
    success = tester.run_tests()
    sys.exit(0 if success else 1)
