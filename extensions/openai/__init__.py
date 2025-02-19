import logging
import openai

from . import commands, env
from . import reply_listener

if not env.openai_key:
    logging.getLogger("OpenAI").error("OpenAI key is not provided.")
else:
    openai.api_key = env.openai_key

