import math
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

# Load APi key from environment variable
api_key = os.environ["OPENAI_API_KEY"]

# Reference: https://platform.openai.com/docs/api-reference/chat/create?lang=python
client = OpenAI(api_key=api_key)

# OpenAIError: The api_key client option must be set either by passing api_key to the client or by setting the OPENAI_API_KEY environment variable

system_message = """You are a knowledgeable assistant that answers questions about food, health, and physical activities. 
For every question, you must always start with "Yes" or "No" and follow with a brief explanation. 

For example:
- Question: "Is Bread healthy?"
  Answer: "Yes, bread can be healthy, especially whole grain varieties, as they are a good source of fiber and nutrients."
  
- Question: "Can you make Pancake with Mayonnaise?"
  Answer: "No, pancakes are typically made with ingredients like flour, eggs, and milk, not mayonnaise."

- Question: "Can Beer cause LiverDisease?"
  Answer: "Yes, excessive alcohol consumption, including beer, can lead to liver disease over time."

- Question: "Can Rowing cause an Injury that can be treated by Antibiotic?"
  Answer: "No, rowing injuries are usually musculoskeletal, and antibiotics are used to treat infections, not physical injuries."

Always provide a clear and concise explanation after the initial 'Yes' or 'No'."""


def gpt_completion(sentence: str):
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": sentence},
        ],
        temperature=0.7,
        max_tokens=150,
        logprobs=True,  # for confidence score
    )
    # Extract logprobs from the completion
    token_logprobs = completion.choices[0].logprobs.content

    # Calculate confidence score using the logprobs
    confidence_score = calculate_confidence_score(token_logprobs)

    return {
        "Result": completion.choices[0].message.content,
        "confidence_score": confidence_score,
    }


def calculate_confidence_score(logprobs):
    # Sum the log probabilities
    total_logprob = sum([token_logprob.logprob for token_logprob in logprobs])

    # Calculate the average log probability
    avg_logprob = total_logprob / len(logprobs)

    # Convert average log probability back to a probability
    overall_confidence = math.exp(avg_logprob)

    return overall_confidence
