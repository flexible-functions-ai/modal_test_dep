# test_modal_api.py
import requests
import json
import sys

# Your Modal API URLs (these are example - replace with your actual endpoints)
HEALTH_URL = "https://flexible-functions-ai--sticker-sales-api-health.modal.run"
PREDICT_URL = "https://flexible-functions-ai--sticker-sales-api-predict-api.modal.run"

def test_health():
    """Test the health endpoint"""
    print("\n🔍 Testing health endpoint...")
    try:
        response = requests.get(HEALTH_URL)
        if response.status_code == 200:
            print("✅ Health check successful!")
            print(f"Response: {response.json()}")
        else:
            print(f"❌ Health check failed with status code: {response.status_code}")
            print(f"Response: {response.text}")
    except Exception as e:
        print(f"❌ Error connecting to health endpoint: {e}")

def test_prediction():
    """Test the prediction endpoint"""
    print("\n🔍 Testing prediction endpoint...")
    
    # Sample test data - adjust based on your model's expected input
    test_data = {
        "date": "2023-01-15",
        "country": "US",
        "store": "Store_001",
        "product": "Sticker_A"
    }
    
    try:
        response = requests.post(
            PREDICT_URL,
            json=test_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            print("✅ Prediction successful!")
            print(f"Input: {json.dumps(test_data, indent=2)}")
            print(f"Prediction: {json.dumps(response.json(), indent=2)}")
        else:
            print(f"❌ Prediction failed with status code: {response.status_code}")
            print(f"Response: {response.text}")
    except Exception as e:
        print(f"❌ Error connecting to prediction endpoint: {e}")

if __name__ == "__main__":
    print("=== Modal API Test ===")
    test_health()
    test_prediction()
    print("\n=== Test Complete ===")