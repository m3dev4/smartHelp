import base64
import mimetypes
import os
from dotenv import load_dotenv
from models.googleVitModel import google_vit_model

load_dotenv()

MODEL_NAME = os.getenv("GOOGLE_VIT_BASE_PATCHED_MODEL_NAME")

prompt = """
Analyse ce produit.

Détermine s'il présente une anomalie.

Réponds uniquement en JSON :

{
 "has_anomaly": true/false,
 "type": "cassé | rayure | fissure | normal",
 "confidence": 0-1,
 "description": ""
}
"""


def encode_image(image_path: str):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


def image_classifier(image_path: str):
    mime_type, _ = mimetypes.guess_type(image_path)
    if not mime_type:
        mime_type = "image/png"

    base64_image = encode_image(image_path)

    response = google_vit_model.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt,
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:{mime_type};base64,{base64_image}"
                        },
                    },
                ],
            }
        ]
    )
    content = response.choices[0].message.content
    if content:
        cleaned_content = content.strip()
        if cleaned_content.startswith("```json"):
            cleaned_content = cleaned_content[7:]
        if cleaned_content.startswith("```"):
            cleaned_content = cleaned_content[3:]
        if cleaned_content.endswith("```"):
            cleaned_content = cleaned_content[:-3]
        cleaned_content = cleaned_content.strip()

        try:
            import json
            return json.loads(cleaned_content)
        except Exception:
            return cleaned_content
    return content

