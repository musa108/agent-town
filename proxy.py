import requests
from flask import Flask, request, Response
from flask_cors import CORS
import os
import time

app = Flask(__name__)
CORS(app) # This allows Vercel to talk to Hugging Face

# The AXL Observer node is running internally on 9092
AXL_OBSERVER_URL = "http://127.0.0.1:9092"

@app.route('/<path:path>', methods=['GET', 'POST'])
def proxy(path):
    url = f"{AXL_OBSERVER_URL}/{path}"
    
    # Forward the request to the AXL node
    try:
        if request.method == 'GET':
            resp = requests.get(url, params=request.args, timeout=5)
        else:
            resp = requests.post(url, data=request.data, headers=request.headers, timeout=5)
            
        # Force JSON content type so the browser doesn't get confused
        headers = dict(resp.headers)
        headers['Content-Type'] = 'application/json'
        
        return Response(resp.content, resp.status_code, headers.items())
    except Exception as e:
        return f"Proxy Error: {str(e)}", 502

if __name__ == "__main__":
    # Hugging Face looks for a listener on port 7860
    port = int(os.environ.get("PORT", 7860))
    print(f"Starting CORS Proxy on port {port} -> {AXL_OBSERVER_URL}")
    app.run(host='0.0.0.0', port=port)
