#!/usr/bin/env python3
"""
UK Trade Tariff API Test Script (UPDATED)
Тестване на UK Trade Tariff REST API за TARIC данни
"""

import logging
import time
from datetime import datetime

import requests

_logger = logging.getLogger(__name__)

# Тестови CN кодове (8-цифрени, по-надеждни)
TEST_CODES_8_DIGIT = [
    "87032310",  # Автомобили с бензинов двигател
    "84713000",  # Portable digital automatic data processing machines
    "62034290",  # Men's or boys' trousers
    "85171200",  # Telephones for cellular networks
    "27101910",  # Petroleum oils
]

# Тестови 10-цифрени TARIC кодове
TEST_CODES_10_DIGIT = [
    "8703231000",  # Автомобили
    "8471300000",  # Лаптопи
    "6203420090",  # Мъжки панталони
    "8517120000",  # Мобилни телефони
    "2710191100",  # Дизелово гориво
]


def test_uk_api_xi(cn_code):
    """Тест на UK XI (Northern Ireland - EU aligned) API"""
    _logger.info(f"\n{'=' * 70}")
    _logger.info(f"🇪🇺 Testing UK XI (NI/EU aligned) API for CN code: {cn_code}")
    _logger.info(f"{'=' * 70}")

    # XI endpoint (Northern Ireland - EU tariffs)
    formatted_code = cn_code.ljust(10, "0") if len(cn_code) < 10 else cn_code[:10]
    base_url = "https://www.trade-tariff.service.gov.uk/xi/api/v2/commodities/"
    url = f"{base_url}{formatted_code}"
    params = {"as_of": datetime.now().strftime("%Y-%m-%d")}
    headers = {
        "User-Agent": "Odoo-BG-Tariff-Test/2.0",
        "Accept": "application/vnd.uktt.v2+json",
    }

    try:
        start_time = time.time()
        response = requests.get(url, params=params, headers=headers, timeout=10)
        elapsed = time.time() - start_time

        _logger.info(f"⏱️  Response time: {elapsed:.2f}s")
        _logger.info(f"📊 Status code: {response.status_code}")
        _logger.info(f"🔗 URL: {url}")

        if response.status_code == 200:
            data = response.json()
            _logger.info("✅ Success!")

            # Извличане на description
            if "data" in data and "attributes" in data["data"]:
                desc = data["data"]["attributes"].get("description", "N/A")
                _logger.info(f"📝 Description: {desc[:100]}...")

            # Извличане на duty rates
            if "included" in data:
                measures_found = 0
                for item in data["included"]:
                    if item.get("type") == "measure":
                        attrs = item.get("attributes", {})
                        measure_type = attrs.get("measure_type_id", "")

                        if measure_type in ["103", "142", "105", "106"]:
                            measures_found += 1
                            duty_expr = attrs.get("duty_expression", {})
                            base = duty_expr.get("base", "N/A")
                            formatted = duty_expr.get("formatted_base", "N/A")
                            _logger.info(f"\n💰 Measure Type {measure_type}:")
                            _logger.info(f"   Base: {base}")
                            _logger.info(f"   Formatted: {formatted}")

                if measures_found == 0:
                    _logger.info("⚠️  No Third Country duty measures found")
                else:
                    _logger.info(f"\n✅ Found {measures_found} relevant measures!")

            return True
        elif response.status_code == 404:
            _logger.info("❌ Not Found (404) - Code may not exist or is invalid")
            return False
        else:
            _logger.info(f"❌ Failed with status: {response.status_code}")
            return False

    except requests.exceptions.Timeout:
        _logger.info("⏰ Timeout after 10 seconds")
        return False
    except requests.exceptions.RequestException as e:
        _logger.info(f"❌ Request error: {e}")
        return False
    except Exception as e:
        _logger.info(f"❌ Unexpected error: {e}")
        return False


def test_uk_api_uk(cn_code):
    """Тест на UK (Great Britain) API"""
    _logger.info(f"\n{'=' * 70}")
    _logger.info(f"🇬🇧 Testing UK (GB) API for CN code: {cn_code}")
    _logger.info(f"{'=' * 70}")

    # UK endpoint (Great Britain tariffs)
    formatted_code = cn_code.ljust(10, "0") if len(cn_code) < 10 else cn_code[:10]
    base_url = "https://www.trade-tariff.service.gov.uk/uk/api/v2/commodities/"
    url = f"{base_url}{formatted_code}"
    params = {"as_of": datetime.now().strftime("%Y-%m-%d")}
    headers = {
        "User-Agent": "Odoo-BG-Tariff-Test/2.0",
        "Accept": "application/vnd.uktt.v2+json",
    }

    try:
        start_time = time.time()
        response = requests.get(url, params=params, headers=headers, timeout=10)
        elapsed = time.time() - start_time

        _logger.info(f"⏱️  Response time: {elapsed:.2f}s")
        _logger.info(f"📊 Status code: {response.status_code}")
        _logger.info(f"🔗 URL: {url}")

        if response.status_code == 200:
            data = response.json()
            _logger.info("✅ Success!")

            # Извличане на description
            if "data" in data and "attributes" in data["data"]:
                desc = data["data"]["attributes"].get("description", "N/A")
                _logger.info(f"📝 Description: {desc[:100]}...")

            # Извличане на duty rates
            if "included" in data:
                measures_found = 0
                for item in data["included"]:
                    if item.get("type") == "measure":
                        attrs = item.get("attributes", {})
                        measure_type = attrs.get("measure_type_id", "")

                        if measure_type in ["103", "142", "105", "106"]:
                            measures_found += 1
                            duty_expr = attrs.get("duty_expression", {})
                            base = duty_expr.get("base", "N/A")
                            formatted = duty_expr.get("formatted_base", "N/A")
                            _logger.info(f"\n💰 Measure Type {measure_type}:")
                            _logger.info(f"   Base: {base}")
                            _logger.info(f"   Formatted: {formatted}")

                if measures_found == 0:
                    _logger.info("⚠️  No Third Country duty measures found")
                else:
                    _logger.info(f"\n✅ Found {measures_found} relevant measures!")

            return True
        elif response.status_code == 404:
            _logger.info("❌ Not Found (404) - Code may not exist or is invalid")
            return False
        else:
            _logger.info(f"❌ Failed with status: {response.status_code}")
            return False

    except requests.exceptions.Timeout:
        _logger.info("⏰ Timeout after 10 seconds")
        return False
    except requests.exceptions.RequestException as e:
        _logger.info(f"❌ Request error: {e}")
        return False
    except Exception as e:
        _logger.info(f"❌ Unexpected error: {e}")
        return False


def test_all_codes():
    """Тества всички CN кодове"""
    _logger.info("\n" + "=" * 70)
    _logger.info("🚀 UK Trade Tariff API Testing Suite (UPDATED)")
    _logger.info("=" * 70)
    _logger.info(f"📅 Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    results = {"xi": {"success": 0, "failed": 0}, "uk": {"success": 0, "failed": 0}}

    _logger.info(f"\n{'=' * 70}")
    _logger.info("📋 Test Set 1: 8-digit CN codes (more reliable)")
    _logger.info(f"{'=' * 70}")

    for cn_code in TEST_CODES_8_DIGIT:
        # Test XI (Northern Ireland/EU)
        if test_uk_api_xi(cn_code):
            results["xi"]["success"] += 1
        else:
            results["xi"]["failed"] += 1

        time.sleep(0.5)  # Rate limiting

        # Test UK (Great Britain)
        if test_uk_api_uk(cn_code):
            results["uk"]["success"] += 1
        else:
            results["uk"]["failed"] += 1

        time.sleep(0.5)  # Rate limiting

    _logger.info(f"\n{'=' * 70}")
    _logger.info("📋 Test Set 2: 10-digit TARIC codes (may have issues)")
    _logger.info(f"{'=' * 70}")

    for cn_code in TEST_CODES_10_DIGIT[:2]:  # Test first 2 only
        # Test XI only
        if test_uk_api_xi(cn_code):
            results["xi"]["success"] += 1
        else:
            results["xi"]["failed"] += 1

        time.sleep(0.5)

    # Summary
    _logger.info("\n" + "=" * 70)
    _logger.info("📊 TEST SUMMARY")
    _logger.info("=" * 70)

    total_xi = results["xi"]["success"] + results["xi"]["failed"]
    total_uk = results["uk"]["success"] + results["uk"]["failed"]

    _logger.info("\n🇪🇺 UK XI (Northern Ireland/EU aligned) Results:")
    _logger.info(f"   ✅ Success: {results['xi']['success']}/{total_xi}")
    _logger.info(f"   ❌ Failed:  {results['xi']['failed']}/{total_xi}")

    _logger.info("\n🇬🇧 UK (Great Britain) API Results:")
    _logger.info(f"   ✅ Success: {results['uk']['success']}/{total_uk}")
    _logger.info(f"   ❌ Failed:  {results['uk']['failed']}/{total_uk}")

    # Recommendations
    _logger.info("\n💡 RECOMMENDATIONS:")

    if results["xi"]["success"] > 0:
        _logger.info(
            "   ✅ UK XI (NI/EU) API работи! Използвайте този endpoint за "
            "EU-aligned данни"
        )

    if results["uk"]["success"] > 0:
        _logger.info("   ✅ UK (GB) API работи! Подходящ за UK tariff данни")

    if results["xi"]["success"] == 0 and results["uk"]["success"] == 0:
        _logger.info("   ⚠️  Нито един API endpoint не връща данни")
        _logger.info("   📝 Възможни причини:")
        _logger.info("       - CN кодовете са невалидни или остарели")
        _logger.info("       - API-то изисква различен формат на кодовете")
        _logger.info("       - Network/firewall проблеми")
        _logger.info("\n   🔧 Решения:")
        _logger.info("       - Използвайте default rates за production")
        _logger.info("       - Изтеглете TARIC database локално от CIRCABC")
        _logger.info("       - Използвайте платен Taric Support API")


def test_single_code_detailed(cn_code):
    """Подробен тест на един CN код"""
    _logger.info("\n" + "=" * 70)
    _logger.info(f"🔬 DETAILED TEST for CN code: {cn_code}")
    _logger.info("=" * 70)

    test_uk_api_xi(cn_code)
    time.sleep(1)
    test_uk_api_uk(cn_code)


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        # Test specific CN code
        cn_code = sys.argv[1]
        test_single_code_detailed(cn_code)
    else:
        # Test all predefined codes
        test_all_codes()

    _logger.info("\n✅ Testing completed!\n")
