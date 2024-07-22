import openai
from environ import Env

env = Env()
env.read_env()

openai.api_key = env('OPENAI_API_KEY')

def generate_gpt_response(prompt):

    completions = openai.Completion.create(
        model=env('FINE_TUNED_MODEL'),
        prompt=prompt,
        max_tokens=64,
        n=1,
        stop="\n",
        temperature=0.05,
    )
    response = completions.choices[0].text.strip() # type: ignore

    return response
