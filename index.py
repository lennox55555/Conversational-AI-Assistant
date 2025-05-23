import json
import boto3

# init the bedrock client
bedrock = boto3.client("bedrock-runtime")

def handler(event, context):
    user_msg = event.get("body", "")

    # build the payload for text generation
    payload = {
        "inputText": user_msg,
        "textGenerationConfig": {
            "maxTokenCount": 512,
            "temperature": 0.5
        }
    }

    try:
        # invoke the bedrock model
        resp = bedrock.invoke_model(
            modelId="amazon.titan-text-premier-v1:0",
            contentType="application/json",
            accept="application/json",
            body=json.dumps(payload)
        )

        body_bytes = resp["body"].read()
        result = json.loads(body_bytes)

        assistant_reply = result["results"][0]["outputText"]

        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "text/plain",
                "Access-Control-Allow-Origin": "*"
            },
            "body": assistant_reply
        }

    except Exception as e:
        print(f"error invoking bedrock model: {e}")
        return {
            "statusCode": 500,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps({"message": "Internal server error"})
        }