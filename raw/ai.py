import requests

def askAI(prompt):
    try:
        r = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "qwen2.5:0.5b",
                "prompt": prompt,
                "stream": False,
                "keep_alive": "30m"
            },
            timeout=60
        )

        return r.json()["response"]
    except Exception as e:
        return f"Error: {e}"