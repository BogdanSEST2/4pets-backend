from app.extensions import openai_client



def ask_chatgpt(message):
    try:
        response = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": message}
            ],
            temperature=0.7,
            max_tokens=1000
        )
        return {
            "status": "success",
            "reply": response.choices[0].message.content
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }
