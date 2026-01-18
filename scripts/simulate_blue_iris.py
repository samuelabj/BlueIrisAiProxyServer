import requests
import argparse
import sys
import os

def simulate_request(image_path, url="http://localhost:8000/v1/vision/detection"):
    """
    Simulates a Blue Iris request to the AI Proxy.
    """
    if not os.path.exists(image_path):
        print(f"Error: Image file not found: {image_path}")
        return

    print(f"Sending {image_path} to {url}...")
    
    try:
        with open(image_path, 'rb') as f:
            # Blue Iris sends the image as a multipart form data with key 'image'
            files = {'image': f}
            response = requests.post(url, files=files)
        
        print(f"Status Code: {response.status_code}")
        try:
            print("Response JSON:")
            print(response.json())
        except:
            print("Raw Response:")
            print(response.text)
            
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to server. Is the AI-Vision-Relay service running?")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Simulate a Blue Iris AI request.")
    parser.add_argument("image", help="Path to the image file to test")
    parser.add_argument("--url", default="http://localhost:8000/v1/vision/detection", help="Server URL")
    
    args = parser.parse_args()
    simulate_request(args.image, args.url)
