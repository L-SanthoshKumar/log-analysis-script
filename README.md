# Log Analysis Script

## Overview
This project involves a Python script designed to analyze server log files, identify patterns, and detect suspicious activity. It performs the following tasks:
1. Counts requests from each unique IP address.
2. Identifies the most frequently accessed endpoint.
3. Detects IP addresses with suspicious activities such as multiple failed login attempts.

The results are saved in a CSV file for easy access and visualization.

---

## Features
- **Requests per IP Address**: Counts and lists the number of requests made by each IP address.
- **Most Accessed Endpoint**: Identifies the endpoint accessed most frequently.
- **Suspicious Activity Detection**: Flags IPs with high numbers of failed login attempts.
- **CSV Export**: Results are saved to a CSV file (`results.csv`).

---
