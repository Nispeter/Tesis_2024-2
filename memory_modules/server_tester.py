import requests
import json
import sys

# Define the base URL for the server
BASE_URL = "http://127.0.0.1:8000"

# Test data
test_question = "What are the key elements of a video game environment?"

# Functions for each endpoint
def test_rag_query():
    print("Testing /rag_query endpoint...")
    payload = {"question": test_question}
    response = requests.post(f"{BASE_URL}/rag_query", json=payload)
    
    if response.status_code == 200:
        print("Context Query Test Passed.")
        print("Answer:", response.json().get("answer"))
    else:
        print("Context Query Test Failed.")
        print("Error:", response.json().get("error", response.text))

def test_graphrag_query():
    print("Testing /graph_query endpoint...")
    payload = {"question": test_question}
    response = requests.post(f"{BASE_URL}/graphrag_query", json=payload)
    
    if response.status_code == 200:
        print("Context Query Test Passed.")
        print("Answer:", response.json().get("answer"))
    else:
        print("Context Query Test Failed.")
        print("Error:", response.json().get("error", response.text))

def test_combined_query():
    print("Testing /combined_query endpoint...")
    payload = {"question": test_question}
    response = requests.post(f"{BASE_URL}/combined_query", json=payload)
    
    if response.status_code == 200:
        print("Context Query Test Passed.")
        print("Answer:", response.json().get("answer"))
    else:
        print("Context Query Test Failed.")
        print("Error:", response.json().get("error", response.text))

def test_get_key():
    print("Testing /get_key endpoint...")
    response = requests.get(f"{BASE_URL}/get_key")
    
    if response.status_code == 200:
        print("API Key Test Passed.")
        print("API Key:", response.json().get("api_key"))
    else:
        print("API Key Test Failed.")
        print("Error:", response.json().get("error", response.text))

def test_shutdown():
    print("Testing /shutdown endpoint...")
    response = requests.post(f"{BASE_URL}/shutdown")
    
    if response.status_code == 200:
        print("Shutdown Test Passed.")
    else:
        print("Shutdown Test Failed.")
        print("Error:", response.json().get("error", response.text))

# Main function to execute based on argument
if __name__ == "__main__":
    # Check if an endpoint argument was provided
    if len(sys.argv) < 2:
        print("Usage: python test_script.py [rag|graph|combined|get_key|shutdown]")
        sys.exit(1)
    
    # Map argument to the correct test function
    option = sys.argv[1].lower()
    
    if option == "rag":
        test_rag_query()
    elif option == "graph":
        test_graphrag_query()
    elif option == "combined":
        test_combined_query()
    elif option == "get_key":
        test_get_key()
    elif option == "shutdown":
        test_shutdown()
    else:
        print("Invalid option. Use one of: context_query, get_key, shutdown.")
