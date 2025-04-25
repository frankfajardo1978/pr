import openai
import os
import sys
import subprocess

# Setear la API key directamente
openai.api_key = os.getenv("OPENAI_API_KEY")

def main():
    try:
        with open("commits.txt", "r", encoding="utf-8") as f:
            commits = f.read()

        print("🔍 Enviando commits a OpenAI...\n")

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # usa gpt-4 si tenés acceso
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

        revision = response.choices[0].message["content"]

        print("🧠 Sugerencias de revisión:\n")
        print(revision)

        # Guardar resultado en archivo
        with open("revision.txt", "w", encoding="utf-8") as out:
            out.write(revision)

        # Obtener URL del PR
        os.environ["PR_URL"] = subprocess.check_output(["gh", "pr", "view", "--json", "url", "-q", ".url"]).decode().strip()

    except Exception as e:
        print("❌ Error durante la revisión:", e)
        sys.exit(1)

if __name__ == "__main__":
    main()
