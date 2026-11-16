import os
import requests
from django.http import HttpResponse, JsonResponse

def generate_sound(prompt: str):
    """
    Generate animal sound via ElevenLabs API matching Node.js backend.
    """
    api_key = os.getenv("ELEVENLABS_API_KEY")
    if not api_key:
        return JsonResponse({"error": "Sound generation failed: API key missing"}, status=500)

    try:
        response = requests.post(
            "https://api.elevenlabs.io/v1/sound-generation",
            json={"text": prompt},
            headers={
                "xi-api-key": api_key,
                "Content-Type": "application/json"
            },
            timeout=15
        )

        if response.status_code == 200:
            return HttpResponse(response.content, content_type="audio/mpeg")
        else:
            return JsonResponse({"error": "Sound generation failed"}, status=response.status_code)
    except Exception as err:
        print(f"Sound API error: {err}")
        return JsonResponse({"error": "Sound generation failed"}, status=500)
