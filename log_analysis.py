{
  "nbformat": 4,
  "nbformat_minor": 0,
  "metadata": {
    "colab": {
      "provenance": [],
      "authorship_tag": "ABX9TyOZy2s6V1NmKYnX9jfUwLkR",
      "include_colab_link": true
    },
    "kernelspec": {
      "name": "python3",
      "display_name": "Python 3"
    },
    "language_info": {
      "name": "python"
    }
  },
  "cells": [
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "view-in-github",
        "colab_type": "text"
      },
      "source": [
        "<a href=\"https://colab.research.google.com/github/L-SanthoshKumar/log-analysis-script/blob/main/VRV.ipynb\" target=\"_parent\"><img src=\"https://colab.research.google.com/assets/colab-badge.svg\" alt=\"Open In Colab\"/></a>"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 1,
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "JXs5jN3jhL9g",
        "outputId": "85c444ea-3a21-4179-d99c-4a9dea26f459"
      },
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "Requests per IP:\n",
            "203.0.113.5          8\n",
            "198.51.100.23        8\n",
            "192.168.1.1          7\n",
            "10.0.0.2             6\n",
            "192.168.1.100        5\n",
            "\n",
            "Most Frequently Accessed Endpoint:\n",
            "/login (Accessed 13 times)\n",
            "\n",
            "Suspicious Activity Detected:\n",
            "\n",
            "Results saved to log_analysis_results.csv\n"
          ]
        }
      ],
      "source": [
        "import re\n",
        "import csv\n",
        "from collections import defaultdict, Counter\n",
        "\n",
        "# Define the file paths\n",
        "log_file_path = \"/content/sample.log\"\n",
        "output_csv_path = \"log_analysis_results.csv\"\n",
        "\n",
        "# Function to parse the log file and extract necessary information\n",
        "def parse_log_file(file_path):\n",
        "    ip_requests = defaultdict(int)\n",
        "    endpoint_requests = defaultdict(int)\n",
        "    failed_logins = defaultdict(int)\n",
        "\n",
        "    with open(file_path, \"r\") as log_file:\n",
        "        for line in log_file:\n",
        "            # Extract IP Address\n",
        "            ip_match = re.match(r\"^(\\d{1,3}(?:\\.\\d{1,3}){3})\", line)\n",
        "            if ip_match:\n",
        "                ip_address = ip_match.group(1)\n",
        "                ip_requests[ip_address] += 1\n",
        "\n",
        "            # Extract endpoint\n",
        "            endpoint_match = re.search(r\"\\\"(?:GET|POST) ([^\\s]+)\", line)\n",
        "            if endpoint_match:\n",
        "                endpoint = endpoint_match.group(1)\n",
        "                endpoint_requests[endpoint] += 1\n",
        "\n",
        "            # Check for failed login attempts (HTTP status code 401)\n",
        "            if \"401\" in line or \"Invalid credentials\" in line:\n",
        "                if ip_match:\n",
        "                    failed_logins[ip_address] += 1\n",
        "\n",
        "    return ip_requests, endpoint_requests, failed_logins\n",
        "\n",
        "# Function to calculate results\n",
        "def analyze_logs(ip_requests, endpoint_requests, failed_logins, brute_force_threshold=10):\n",
        "    # Count requests per IP address\n",
        "    sorted_ip_requests = sorted(ip_requests.items(), key=lambda x: x[1], reverse=True)\n",
        "\n",
        "    # Find the most frequently accessed endpoint\n",
        "    most_accessed_endpoint = max(endpoint_requests.items(), key=lambda x: x[1])\n",
        "\n",
        "    # Detect suspicious activity\n",
        "    suspicious_activity = {\n",
        "        ip: count for ip, count in failed_logins.items() if count > brute_force_threshold\n",
        "    }\n",
        "\n",
        "    return sorted_ip_requests, most_accessed_endpoint, suspicious_activity\n",
        "\n",
        "# Function to save results to a CSV file\n",
        "def save_to_csv(ip_requests, most_accessed_endpoint, suspicious_activity, output_file):\n",
        "    with open(output_file, \"w\", newline=\"\") as csv_file:\n",
        "        writer = csv.writer(csv_file)\n",
        "\n",
        "        # Write Requests per IP\n",
        "        writer.writerow([\"Requests per IP\"])\n",
        "        writer.writerow([\"IP Address\", \"Request Count\"])\n",
        "        writer.writerows(ip_requests)\n",
        "\n",
        "        # Write Most Accessed Endpoint\n",
        "        writer.writerow([])\n",
        "        writer.writerow([\"Most Accessed Endpoint\"])\n",
        "        writer.writerow([\"Endpoint\", \"Access Count\"])\n",
        "        writer.writerow([most_accessed_endpoint[0], most_accessed_endpoint[1]])\n",
        "\n",
        "        # Write Suspicious Activity\n",
        "        writer.writerow([])\n",
        "        writer.writerow([\"Suspicious Activity Detected\"])\n",
        "        writer.writerow([\"IP Address\", \"Failed Login Count\"])\n",
        "        writer.writerows(suspicious_activity.items())\n",
        "\n",
        "# Main function to integrate everything\n",
        "def main():\n",
        "    # Parse the log file\n",
        "    ip_requests, endpoint_requests, failed_logins = parse_log_file(log_file_path)\n",
        "\n",
        "    # Analyze logs\n",
        "    sorted_ip_requests, most_accessed_endpoint, suspicious_activity = analyze_logs(\n",
        "        ip_requests, endpoint_requests, failed_logins\n",
        "    )\n",
        "\n",
        "    # Display the results\n",
        "    print(\"Requests per IP:\")\n",
        "    for ip, count in sorted_ip_requests:\n",
        "        print(f\"{ip:<20} {count}\")\n",
        "\n",
        "    print(\"\\nMost Frequently Accessed Endpoint:\")\n",
        "    print(f\"{most_accessed_endpoint[0]} (Accessed {most_accessed_endpoint[1]} times)\")\n",
        "\n",
        "    print(\"\\nSuspicious Activity Detected:\")\n",
        "    for ip, count in suspicious_activity.items():\n",
        "        print(f\"{ip:<20} {count}\")\n",
        "\n",
        "    # Save results to CSV\n",
        "    save_to_csv(sorted_ip_requests, most_accessed_endpoint, suspicious_activity, output_csv_path)\n",
        "    print(f\"\\nResults saved to {output_csv_path}\")\n",
        "\n",
        "if __name__ == \"__main__\":\n",
        "    main()\n"
      ]
    }
  ]
}