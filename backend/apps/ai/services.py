import os
from groq import Groq
class AIServiceError(Exception): pass
def analyze_bid(payload):
 key=os.getenv("GROQ_API_KEY")
 if not key: raise AIServiceError("AI service is not configured.")
 try:
  result=Groq(api_key=key,timeout=12,max_retries=1).chat.completions.create(model=os.getenv("GROQ_MODEL","llama-3.3-70b-versatile"),temperature=.2,max_tokens=250,messages=[{"role":"system","content":"Provide concise, neutral public-procurement compliance rationale. Never autonomously decide qualification. State human review is required."},{"role":"user","content":f"Bidder: {payload['bidder']}\nTender: {payload['tender']}\nScore: {payload['score']}\nFindings: {', '.join(payload['findings'])}"}])
  text=result.choices[0].message.content.strip()
  if not text: raise AIServiceError("AI returned no usable analysis.")
  return text
 except AIServiceError: raise
 except Exception: raise AIServiceError("AI analysis is temporarily unavailable.")
