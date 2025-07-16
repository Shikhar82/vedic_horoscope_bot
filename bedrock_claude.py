# ---------------------- bedrock_claude.py (Final Updated for Messages API) ----------------------
import boto3
import json

bedrock = boto3.client("bedrock-runtime", region_name="us-east-1")

def get_claude_prediction(payload: dict, positions: dict) -> str:
    try:
        birth_info = f"""
        जन्म तिथि: {payload['date']}
        जन्म समय: {payload['time']}
        अक्षांश: {payload['latitude']}
        देशांतर: {payload['longitude']}
        समय क्षेत्र: {payload['timezone']}
        ग्रह स्थिति:
        """ + "\n".join([f"{k}: {v}°" for k, v in positions.items()])

        system_prompt = """
आप एक वैदिक ज्योतिष विशेषज्ञ हैं। उपयोगकर्ता द्वारा दी गई जन्म तिथि, समय, स्थान और ग्रह स्थिति के आधार पर विस्तृत हिंदी कुंडली भविष्यवाणी तैयार करें।
भविष्यवाणी में इन विषयों को शामिल करें: स्वभाव, करियर, विवाह, स्वास्थ्य और अगले 5 वर्षों के संकेत।
        """

        combined_prompt = f"{system_prompt.strip()}\n\n{birth_info.strip()}"

        body = json.dumps({
            "anthropic_version": "bedrock-2023-05-31",
            "messages": [
                {
                    "role": "user",
                    "content": combined_prompt
                }
            ],
            "max_tokens": 1000,
            "temperature": 0.7,
            "top_k": 250,
            "top_p": 0.9
        })

        response = bedrock.invoke_model(
            modelId="anthropic.claude-3-sonnet-20240229-v1:0",
            body=body,
            contentType="application/json",
            accept="application/json"
        )

        result = json.loads(response["body"].read())
        return result["content"][0]["text"].strip()

    except Exception as e:
        return f"AI Prediction Error: {e}"
