import anthropic

from app.config import Config

config = Config()

client = anthropic.Anthropic(api_key=config.ANTHROPIC_API_KEY)

message = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=1000,
    messages=[
        {
            "role": "user",
            "content": "What should I search for to find the latest developments in renewable energy?"
        }
    ]
)
print(message.content)