import openai
import os
import subprocess

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def main():
    try:
        with open("commits.txt", "r", encoding="utf-8") as f:
            commits = f.read()

        if not commits.strip():
            print("ℹ️ No hay commits nuevos para revisar.")
            return

        print("🔍 Enviando commits a OpenAI (gpt-3.5-turbo)...\n")

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
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

        revision = response.choices[0].message.content

        print("🧠 Sugerencias de revisión:\n")
        print(revision)

        with open("revision.txt", "w", encoding="utf-8") as out:
            out.write(revision)

    except openai.APIStatusError as e:
        print(f"⚠️ Error de OpenAI: {e}")
        with open("revision.txt", "w", encoding="utf-8") as out:
            out.write("⚠️ No se pudo completar la revisión por un error de la API de OpenAI.")

    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        with open("revision.txt", "w", encoding="utf-8") as out:
            out.write(f"❌ Error durante la revisión automática: {e}")

if __name__ == "__main__":
    main()
