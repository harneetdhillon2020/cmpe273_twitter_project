import os
import requests
import json

def lambda_handler(event, context):
    try:
        # Extract input text from the POST request
        body = json.loads(event['body'])
        input_text = body.get('text', '')
        
        if not input_text:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'Text input is required.'})
            }
        

        modified_text = f"Explain this sentence in a formal tone: {input_text}"

        # Define the request payload
        payload = {
            "contents": [{
                "parts": [{"text": modified_text}]
            }]
        }

        
        # API Key and Endpoint
        api_key = os.getenv("GEMINI")
        endpoint = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
        
        # Send POST request to the Generative Language API
        headers = {'Content-Type': 'application/json'}
        response = requests.post(endpoint, headers=headers, json=payload)
        
        # Handle response
        if response.status_code == 200:
            response_data = response.json()
            return {
                'statusCode': 200,
                'body': json.dumps(response_data)
            }
        else:
            return {
                'statusCode': response.status_code,
                'body': json.dumps({'error': response.text})
            }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }

