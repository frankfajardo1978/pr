import os
import sys
from openai import OpenAI, OpenAIError

def main():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ Falta la variable de entorno OPENAI_API_KEY.")
        sys.exit(1)

    client = OpenAI(api_key=api_key)

    try:
        with open("commits.txt", "r", encoding="utf-8") as f:
            commits = f.read().strip()

        if not commits:
            mensaje = "ℹ️ No hay commits nuevos para revisar."
            print(mensaje)
            with open("revision.txt", "w", encoding="utf-8") as out:
                out.write(mensaje)
            return

        print("🔍 Enviando commits a OpenAI (gpt-3.5-turbo)...\n")

        max_chars = 12000
        if len(commits) > max_chars:
            commits = commits[:max_chars]
            print("⚠️ Los commits fueron truncados por exceder el tamaño máximo.")

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Sos un revisor de código. Dado un resumen de cambios de un PR, "
                        "comentá si hay algo que mejorar o si está todo bien."
                    )
                },
                {
                    "role": "user",
                    "content": f"Estos son los mensajes de commit:\n\n{commits}"
                }
            ]
        )

        revision = response.choices[0].message.content.strip()
        print("🧠 Sugerencias de revisión:\n")
        print(revision)

        with open("revision.txt", "w", encoding="utf-8") as out:
            out.write(revision)

    except OpenAIError as e:
        mensaje = f"⚠️ No se pudo completar la revisión: {str(e)}"
        print(mensaje)
        with open("revision.txt", "w", encoding="utf-8") as out:
            out.write(mensaje)
        sys.exit(1)

if __name__ == "__main__":
    main()
