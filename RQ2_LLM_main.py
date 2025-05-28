from openai import OpenAI
from dotenv import load_dotenv
import os
import sys

load_dotenv()
openai = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


