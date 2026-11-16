import os
import json
import random
import requests

def generate_gemini_quiz(animal_name: str, category_name: str = "Wildlife"):
    """
    Generate 10 MCQs directly from Gemini API for a specified animal.
    Falls back to dynamic smart quiz generator if key is missing or call fails.
    """
    api_key = os.getenv("GEMINI_API_KEY")

    if api_key:
        prompt = f"""You are a wildlife expert creating an engaging 10-question multiple choice quiz for a Virtual Zoo app about the animal "{animal_name}" ({category_name or 'Wildlife'}).
Generate EXACTLY 10 multiple-choice questions (MCQs).
Return ONLY a valid raw JSON array of 10 objects. Do not include markdown code block formatting (no ```json).
Each object MUST strictly have these properties:
{{
  "id": 1,
  "question": "Clear educational question about {animal_name}?",
  "options": ["Option A", "Option B", "Option C", "Option D"],
  "correctAnswer": "Exact matching string from options array",
  "explanation": "1 short interesting fact explaining why this answer is correct."
}}"""

        for model_name in ["gemini-2.5-flash", "gemini-1.5-flash"]:
            try:
                gemini_url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={api_key}"
                payload = {
                    "contents": [{"parts": [{"text": prompt}]}],
                    "generationConfig": {
                        "temperature": 0.7,
                        "maxOutputTokens": 2048,
                    }
                }
                headers = {"Content-Type": "application/json"}
                response = requests.post(gemini_url, json=payload, headers=headers, timeout=12)
                if response.status_code == 200:
                    data = response.json()
                    candidates = data.get("candidates", [])
                    if candidates:
                        parts = candidates[0].get("content", {}).get("parts", [])
                        if parts:
                            raw_text = parts[0].get("text", "")
                            cleaned_text = raw_text.replace("```json", "").replace("```", "").strip()
                            parsed = json.loads(cleaned_text)
                            if isinstance(parsed, list) and len(parsed) >= 5:
                                result = []
                                for idx, item in enumerate(parsed[:10]):
                                    result.append({
                                        "id": item.get("id", idx + 1),
                                        "question": item.get("question", ""),
                                        "options": item.get("options", []),
                                        "correctAnswer": item.get("correctAnswer", ""),
                                        "explanation": item.get("explanation", f"Learn more about {animal_name}!")
                                    })
                                return result
            except Exception as err:
                print(f"Gemini API attempt with {model_name} failed: {err}")
                continue

    # Fallback if API key missing or call fails
    return generate_dynamic_fallback_quiz(animal_name, category_name)


def generate_dynamic_fallback_quiz(animal: str, category: str = "Wildlife"):
    """
    Generates 10 structured MCQs dynamically for any animal
    """
    cat = (category or "Wildlife").upper()

    question_templates = [
        {
            "q": f"What primary biological class does the {animal} belong to?",
            "opts": list(dict.fromkeys([cat, "INSECT", "AMPHIBIAN", "FISH"])),
            "ans": cat,
            "exp": f"The {animal} is classified under {cat}."
        },
        {
            "q": f"What type of diet does the {animal} primarily consume in its natural habitat?",
            "opts": ["Herbivore", "Carnivore", "Omnivore", "Insectivore"],
            "ans": "Carnivore" if cat in ["MAMMAL", "REPTILE"] else ("Omnivore" if cat == "BIRD" else "Herbivore"),
            "exp": f"The {animal}'s diet is specially adapted to its native ecosystem."
        },
        {
            "q": f"Where is the native geographical range of the {animal}?",
            "opts": ["Tropical Rainforests & Savannas", "Arctic Tundra", "Deep Ocean Trenches", "Urban Deserts"],
            "ans": "Tropical Rainforests & Savannas",
            "exp": f"The {animal} thrives in rich natural biodiverse habitats."
        },
        {
            "q": f"Which unique physical feature helps the {animal} survive in the wild?",
            "opts": ["Specialized Camouflage & Adaptations", "Bioluminescent Wings", "Gills that process lava", "Metallic scales"],
            "ans": "Specialized Camouflage & Adaptations",
            "exp": f"Evolutionary adaptations give the {animal} an edge against predators and prey."
        },
        {
            "q": f"What is the current general conservation status of species like the {animal}?",
            "opts": ["Vulnerable / Threatened", "Least Concern", "Extinct in Wild", "Unknown"],
            "ans": "Vulnerable / Threatened",
            "exp": f"Habitat preservation efforts are crucial for sustaining {animal} populations."
        },
        {
            "q": f"How does the {animal} primarily communicate or interact with others of its species?",
            "opts": ["Vocalizations & Pheromones", "Radio Frequencies", "Color-changing flashes", "Telepathy"],
            "ans": "Vocalizations & Pheromones",
            "exp": f"Communication plays a vital role in social structure and mating for {animal}."
        },
        {
            "q": f"What is a major environmental threat to the {animal}'s wild habitat?",
            "opts": ["Deforestation & Climate Change", "Over-freezing", "Space Debris", "Volcanic Ash"],
            "ans": "Deforestation & Climate Change",
            "exp": f"Human expansion and climate shifts impact the habitats of species like {animal}."
        },
        {
            "q": f"How does the {animal} protect itself when threatened by natural predators?",
            "opts": ["Swift locomotion or defensive armor", "Flying to space", "Burrowing 50 miles deep", "Hypnotizing predators"],
            "ans": "Swift locomotion or defensive armor",
            "exp": f"The {animal} relies on quick reflexes, stealth, or natural defenses."
        },
        {
            "q": f"During which time of day is the {animal} typically most active?",
            "opts": ["Diurnal or Nocturnal based on sub-species", "Only at Solar Eclipse", "During blizzards", "Strictly at midnight"],
            "ans": "Diurnal or Nocturnal based on sub-species",
            "exp": f"Activity cycles for {animal} align with foraging and temperature balance."
        },
        {
            "q": f"Why is the {animal} considered an important part of its ecosystem?",
            "opts": ["Maintains ecological balance as a key species", "Regulates planetary gravity", "Produces electricity for forests", "Prevents earthquakes"],
            "ans": "Maintains ecological balance as a key species",
            "exp": f"Every creature like the {animal} contributes to food web stability."
        }
    ]

    result = []
    for idx, t in enumerate(question_templates):
        opts = list(t["opts"])
        if len(opts) < 4:
            for fallback_opt in ["Herbivore", "Carnivore", "Insectivore", "Omnivore"]:
                if fallback_opt not in opts:
                    opts.append(fallback_opt)
                if len(opts) == 4:
                    break
        random.shuffle(opts)
        result.append({
            "id": idx + 1,
            "question": t["q"],
            "options": opts,
            "correctAnswer": t["ans"],
            "explanation": t["exp"]
        })

    return result
