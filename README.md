# YummyApp Mobile Backend — CI/CD Pipeline

[![CI Pipeline](https://github.com/vuong123s/yummyapp-cicd/actions/workflows/yummyapp-ci.yml/badge.svg)](https://github.com/vuong123s/yummyapp-cicd/actions)
![Python Version](https://img.shields.io/badge/python-3.11-blue.svg)
![Coverage](https://img.shields.io/badge/coverage-99%25-brightgreen.svg)
![Code Style](https://img.shields.io/badge/code%20style-flake8-blue.svg)

Backend service for YummyApp with automated mobile peripheral testing, mocking, and Continuous Integration (CI) pipeline using GitHub Actions.

---

## 📌 Project Overview
* **Student:** Phan Khánh Vương
* **Student ID (MSSV):** 2312802
* **Course:** Software Testing (Kiểm thử Phần mềm) - Lab 7

## 🚀 Core Features
1. **Order Total Calculation:** Computes total cart pricing according to item unit price and quantity.
2. **Promo Code Verification:** Validates promo codes, checks OS version requirements, and handles network offline status (`ConnectionError`).
3. **Nearby Restaurants Recommendation:** Interfaces with GPS hardware service (`get_current_location`) to find matching restaurants.

## 🧪 Testing & Mocking Strategy
* **Unit Testing:** Built with Python `unittest` standard library.
* **Peripheral Mocking:** Employs `unittest.mock.patch` to stub GPS hardware coordinates and simulate hardware fault conditions (`GPSSignalLostError`) without physical devices.
* **Test Matrix:** 13 test cases covering all edge cases, exceptions, and business flows.

## ⚙️ CI Pipeline & Quality Gates (GitHub Actions)
The automated workflow is configured in `.github/workflows/yummyapp-ci.yml`:
1. **Source Checkout:** `actions/checkout@v4`
2. **Python Setup:** `actions/setup-python@v5` (Python 3.11)
3. **Dependency Installation:** `pip install -r requirements.txt` (Pinned versions)
4. **Static Code Analysis (Fail-Fast):** `flake8` syntax and structural checks
5. **Quality Gate Enforcement:** `coverage report --fail-under=80` (Current: **99%**)
6. **Artifact Archiving:** Uploads `coverage_html/` report via `actions/upload-artifact@v4`
