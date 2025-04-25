import openai
import os
import sys

# Crear cliente OpenAI con API key desde variable de entorno
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def main():
    try:
        with open("commits.txt", "r", encoding="utf-8") as f:
            commits = f.read()
        
        print("🔍 Enviando commits a OpenAI...\n")

        response = client.chat.completions.create(
            model="gpt-4o",  # ¡Usando el modelo nuevo!
            messages=[
                {
                    "role": "system",
                    "content": "Sos un revisor de código. Dado un resumen de cambios de un PR, comentá si hay algo que mejorar o si está todo bien."
                },
                {
                    "role": "user",
                    "content": f"Estos son los mensajes de commit:\n\n{commits}"
                }
            ]
        )

        print("🧠 Sugerencias de revisión:\n")
        print(response.choices[0].message.content)
    
    except Exception as e:
        print("❌ Error durante la revisión:", e)
        sys.exit(1)

if __name__ == "__main__":
    main()

