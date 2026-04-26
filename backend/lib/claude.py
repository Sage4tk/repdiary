import anthropic
import os

claude_client = anthropic.Anthropic(api_key=os.environ.get('ANTHROPIC_API_KEY'))