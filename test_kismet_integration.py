#!/usr/bin/env python3
"""
NetShield Kismet Integration Test Suite

Tests Kismet API connectivity, network scanning, and data parsing validation.
Usage: python test_kismet_integration.py [--kismet-url http://localhost:2501]
"""

import asyncio
import sys
import json
import argparse
from datetime import datetime
from typing import Optional, Dict, Any

try:
    import aiohttp
    import requests
except ImportError:
    print("ERROR: Required packages not installed.")
    print("Run: pip install aiohttp requests")
    sys.exit(1)


class Colors:
    """ANSI color codes for terminal output"""
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

    @staticmethod
    def success(msg: str) -> str:
        return f"{Colors.GREEN}✓ {msg}{Colors.RESET}"

    @staticmethod
    def error(msg: str) -> str:
        return f"{Colors.RED}✗ {msg}{Colors.RESET}"

    @staticmethod
    def warning(msg: str) -> str:
        return f"{Colors.YELLOW}⚠ {msg}{Colors.RESET}"

    @staticmethod
    def info(msg: str) -> str:
        return f"{Colors.BLUE}[*] {msg}{Colors.RESET}"


class KismetIntegrationTester:
    """Test suite for Kismet integration"""

    def __init__(self, kismet_url: str = "http://localhost:2501"):
        self.kismet_url = kismet_url
        self.test_results = {
            "passed": 0,
            "failed": 0,
            "warnings": 0,
            "tests": []
        }

    def log_test(self, name: str, status: str, message: str = "", details: str = ""):
        """Log test result"""
        self.test_results["tests"].append({
            "name": name,
            "status": status,
            "message": message,
            "details": details
        })

    async def test_kismet_connectivity(self) -> bool:
        """Test 1: Basic Kismet daemon connectivity"""
        print(Colors.info(f"Testing Kismet connectivity at {self.kismet_url}..."))

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.kismet_url}/system/status", timeout=aiohttp.ClientTimeout(total=5)) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        kismet_version = data.get('response', {}).get('kismet_version', 'unknown')
                        print(Colors.success(f"Connected to Kismet (version: {kismet_version})"))
                        self.log_test("Kismet Connectivity", "passed", f"Kismet version: {kismet_version}")
                        self.test_results["passed"] += 1
                        return True
                    else:
                        print(Colors.error(f"Kismet returned status {resp.status}"))
                        self.log_test("Kismet Connectivity", "failed", f"Status: {resp.status}")
                        self.test_results["failed"] += 1
                        return False

        except aiohttp.ClientConnectorError:
            print(Colors.error(f"Cannot connect to Kismet at {self.kismet_url}"))
            print(Colors.warning("Ensure Kismet is running: sudo kismet"))
            self.log_test("Kismet Connectivity", "failed", "Connection refused")
            self.test_results["failed"] += 1
            return False
        except asyncio.TimeoutError:
            print(Colors.error("Connection timeout"))
            self.log_test("Kismet Connectivity", "failed", "Timeout")
            self.test_results["failed"] += 1
            return False
        except Exception as e:
            print(Colors.error(f"Exception: {str(e)}"))
            self.log_test("Kismet Connectivity", "failed", str(e))
            self.test_results["failed"] += 1
            return False

    async def test_get_networks(self) -> bool:
        """Test 2: Retrieve current networks"""
        print(Colors.info("Testing network retrieval..."))

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.kismet_url}/networks/summary", timeout=aiohttp.ClientTimeout(total=5)) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        networks = data.get('response', [])
                        print(Colors.success(f"Retrieved {len(networks)} networks"))
                        self.log_test("Get Networks", "passed", f"Networks found: {len(networks)}")
                        self.test_results["passed"] += 1

                        if len(networks) > 0:
                            print(f"  Sample network: {networks[0].get('essid', 'Hidden')}")
                        return True
                    else:
                        print(Colors.error(f"Status {resp.status}"))
                        self.log_test("Get Networks", "failed", f"Status: {resp.status}")
                        self.test_results["failed"] += 1
                        return False

        except Exception as e:
            print(Colors.error(f"Exception: {str(e)}"))
            self.log_test("Get Networks", "failed", str(e))
            self.test_results["failed"] += 1
            return False

    async def test_get_devices(self) -> bool:
        """Test 3: Retrieve detected devices"""
        print(Colors.info("Testing device detection..."))

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.kismet_url}/devices/summary", timeout=aiohttp.ClientTimeout(total=5)) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        devices = data.get('response', [])
                        print(Colors.success(f"Retrieved {len(devices)} devices"))
                        self.log_test("Get Devices", "passed", f"Devices found: {len(devices)}")
                        self.test_results["passed"] += 1

                        if len(devices) > 0:
                            device = devices[0]
                            mac = device.get('key', 'unknown')
                            signal = device.get('signal', {}).get('signal_dbm', 'N/A')
                            print(f"  Sample device: {mac} (Signal: {signal} dBm)")
                        return True
                    else:
                        print(Colors.error(f"Status {resp.status}"))
                        self.log_test("Get Devices", "failed", f"Status: {resp.status}")
                        self.test_results["failed"] += 1
                        return False

        except Exception as e:
            print(Colors.error(f"Exception: {str(e)}"))
            self.log_test("Get Devices", "failed", str(e))
            self.test_results["failed"] += 1
            return False

    async def test_backend_connectivity(self) -> bool:
        """Test 4: NetShield backend connectivity"""
        print(Colors.info("Testing NetShield backend..."))

        try:
            response = requests.get("http://localhost:8000/api/health", timeout=5)
            if response.status_code == 200:
                print(Colors.success("Backend is running"))
                self.log_test("Backend Connectivity", "passed", "Health check successful")
                self.test_results["passed"] += 1
                return True
            else:
                print(Colors.warning(f"Backend returned status {response.status_code}"))
                self.log_test("Backend Connectivity", "warning", f"Status: {response.status_code}")
                self.test_results["warnings"] += 1
                return False

        except requests.exceptions.ConnectionError:
            print(Colors.warning("Backend not running at http://localhost:8000"))
            print(Colors.info("Start backend: python backend/main.py"))
            self.log_test("Backend Connectivity", "warning", "Backend not accessible")
            self.test_results["warnings"] += 1
            return False
        except Exception as e:
            print(Colors.warning(f"Exception: {str(e)}"))
            self.log_test("Backend Connectivity", "warning", str(e))
            self.test_results["warnings"] += 1
            return False

    async def test_kismet_api_endpoints(self) -> bool:
        """Test 5: Verify key Kismet API endpoints"""
        print(Colors.info("Testing Kismet API endpoints..."))

        endpoints = [
            ("/system/status", "System Status"),
            ("/networks/summary", "Networks Summary"),
            ("/devices/summary", "Devices Summary"),
            ("/alerts/definitions", "Alert Definitions"),
        ]

        all_ok = True

        try:
            async with aiohttp.ClientSession() as session:
                for endpoint, name in endpoints:
                    try:
                        async with session.get(f"{self.kismet_url}{endpoint}", timeout=aiohttp.ClientTimeout(total=5)) as resp:
                            if resp.status == 200:
                                print(f"  {Colors.GREEN}✓{Colors.RESET} {name}")
                                self.test_results["passed"] += 1
                            else:
                                print(f"  {Colors.RED}✗{Colors.RESET} {name} (Status: {resp.status})")
                                self.test_results["failed"] += 1
                                all_ok = False

                    except asyncio.TimeoutError:
                        print(f"  {Colors.YELLOW}⚠{Colors.RESET} {name} (Timeout)")
                        self.test_results["warnings"] += 1
                        all_ok = False
                    except Exception as e:
                        print(f"  {Colors.RED}✗{Colors.RESET} {name} ({str(e)})")
                        self.test_results["failed"] += 1
                        all_ok = False

        except Exception as e:
            print(Colors.error(f"Session error: {str(e)}"))
            self.test_results["failed"] += 1
            return False

        self.log_test("API Endpoints", "passed" if all_ok else "warning", f"Tested {len(endpoints)} endpoints")
        return all_ok

    async def run_all_tests(self):
        """Run all tests"""
        print(Colors.BOLD + "=" * 60 + Colors.RESET)
        print(Colors.BOLD + "NetShield Kismet Integration Test Suite" + Colors.RESET)
        print(Colors.BOLD + "=" * 60 + Colors.RESET)
        print()

        # Test 1: Connectivity
        kismet_ok = await self.test_kismet_connectivity()
        print()

        if not kismet_ok:
            print(Colors.error("Cannot connect to Kismet. Skipping further tests."))
            print(Colors.info("Fix: Run 'sudo kismet' to start Kismet daemon"))
            return

        # Test 2-4: Core functionality
        await self.test_get_networks()
        print()

        await self.test_get_devices()
        print()

        await self.test_kismet_api_endpoints()
        print()

        await self.test_backend_connectivity()
        print()

    def print_summary(self):
        """Print test summary"""
        print(Colors.BOLD + "=" * 60 + Colors.RESET)
        print(Colors.BOLD + "Test Summary" + Colors.RESET)
        print(Colors.BOLD + "=" * 60 + Colors.RESET)

        passed = self.test_results["passed"]
        failed = self.test_results["failed"]
        warnings = self.test_results["warnings"]
        total = passed + failed + warnings

        if total == 0:
            print(Colors.warning("No tests were run"))
            return

        print(f"Total Tests: {total}")
        print(f"{Colors.GREEN}Passed: {passed}{Colors.RESET}")
        if warnings > 0:
            print(f"{Colors.YELLOW}Warnings: {warnings}{Colors.RESET}")
        if failed > 0:
            print(f"{Colors.RED}Failed: {failed}{Colors.RESET}")
        print()

        if failed == 0 and warnings == 0:
            print(Colors.success("All tests passed! Kismet integration ready."))
            print()
            print("Next steps:")
            print("1. Start NetShield backend: python backend/main.py")
            print("2. Start frontend: npm run dev (in frontend/)")
            print("3. Access at http://localhost:5173")
            return 0
        elif failed == 0:
            print(Colors.warning(f"{warnings} warning(s) - Kismet integration operational but check warnings"))
            return 1
        else:
            print(Colors.error(f"{failed} test(s) failed - Fix issues before proceeding"))
            return 2

    def export_results(self, filename: str = "kismet_test_results.json"):
        """Export test results to JSON"""
        with open(filename, 'w') as f:
            json.dump({
                "timestamp": datetime.now().isoformat(),
                "kismet_url": self.kismet_url,
                "results": self.test_results
            }, f, indent=2)
        print(Colors.info(f"Results exported to {filename}"))


async def main():
    parser = argparse.ArgumentParser(
        description="Test NetShield Kismet integration",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python test_kismet_integration.py
  python test_kismet_integration.py --kismet-url http://192.168.1.100:2501
  python test_kismet_integration.py --export results.json
        """
    )
    parser.add_argument(
        "--kismet-url",
        type=str,
        default="http://localhost:2501",
        help="Kismet daemon URL (default: http://localhost:2501)"
    )
    parser.add_argument(
        "--export",
        type=str,
        help="Export results to JSON file"
    )

    args = parser.parse_args()

    tester = KismetIntegrationTester(args.kismet_url)
    await tester.run_all_tests()

    exit_code = tester.print_summary()

    if args.export:
        tester.export_results(args.export)

    sys.exit(exit_code if exit_code is not None else 0)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n" + Colors.warning("Tests interrupted by user"))
        sys.exit(130)
