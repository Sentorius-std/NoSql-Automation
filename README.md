# NoSQL Injection Automation Tool
A Python-based tool for automatically detecting NoSQL injection vulnerabilities in web applications.

## Description
This tool automates the process of discovering login endpoints and testing them for NoSQL injection vulnerabilities. It's designed for security professionals and ethical hackers to test their own systems or systems they have permission to audit.

## Table of contents

- [Features](#Features)
- [Installation](#Installation)
- [Usage](#Usage)
- [How-it-Works](#How-it-works)
- [Detection-Methods](#Detection-Methods)
- [Warning](#Warning)
- [Legal-Disclaimer](#Legal-Disclaimer)
- [Contributing](#Contributing)
  
## Features
- Automatic Endpoint Discovery: Scans for common login endpoints (/login, /admin, /api/login, etc.)

- Parameter Enumeration: Tests various parameter name combinations (username/password, email/password, etc.)

- Multiple Payload Types: Uses different NoSQL injection payloads:

   - JSON-based: {"$ne": null}

   - Form-based: admin' || '' === '

   - Form with operators: password[$ne]=admin

- Intelligent Detection: Identifies vulnerabilities through:

   - Redirect analysis

   - Response status code differences

   - Content length variations

- Comprehensive Logging: Creates detailed logs of all HTTP traffic and tool operations

## Installation
###Prerequisites
- Python 3.x

- pip (Python package manager)

### Required Packages
```bash
pip install requests colorama 
```

## Usage

### Basic Usage
```bash
python3 nosql-automation.py
```
### Example
```text
Please enter the target without ['http://']: 94.237.122.95:52766


[*] Reconnaissance: Finding login endpoints...

    [*] Endpoint Found http://94.237.122.95:52766/login with Status Code 200
    [*] Endpoint Found http://94.237.122.95:52766/api/login with Status Code 403
    [*] Endpoint Found http://94.237.122.95:52766/ with Status Code 200


[*] Enumeration and Exploitation: Attempting to discover API parameters for http://94.237.122.95:52766/login and using NoSql payload ...

    [-] Could not automatically determine parameters


[*] Enumeration and Exploitation: Attempting to discover API parameters for http://94.237.122.95:52766/api/login and using NoSql payload ...

[+] High probability NoSQL injection (heuristic) detected with parameters: ['username', 'password'] and response {'resp': 'User authenticated successfully'}
```
    
### Log Files
The tool creates two log files:

1. nosql-logfile.txt - General tool operations and findings

2. fulllog.txt - Full HTTP request/response details for debugging

## How-It-Works
1. Endpoint Discovery: Scans the target for common login endpoints

2. Parameter Testing: For each endpoint, tests various parameter name combinations

3. Payload Injection: Injects different NoSQL payloads to detect vulnerabilities

4. Response Analysis: Analyzes responses for signs of successful injection

5. Vulnerability Reporting: Reports discovered vulnerabilities with details

## Detection-Methods
The tool uses multiple heuristics to detect vulnerabilities:

- Redirect Analysis: Checks if injection causes redirects to admin/dashboard pages

- Status Code Differences: Compares NoSQL vs dummy credential responses

- Content Length: Detects significant differences in response sizes

- Response Content: Looks for admin-related content in responses

##Demonstration

* PoC 1:

![PoC1](https://github.com/user-attachments/assets/665397f3-8abc-4f57-9a10-47e692a713ae)

* PoC 2:

## Warning
This tool is for authorized testing only

- Only use on systems you own or have explicit permission to test

- Unauthorized testing is illegal and unethical

= The authors are not responsible for misuse of this tool

## Contributing
Feel free to submit issues, feature requests, or pull requests to improve the tool.


