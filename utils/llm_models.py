import json
import time
import requests
import openai
import anthropic
from mistralai import Mistral
from ollama import Client
from huggingface_hub import InferenceClient
from groq import Groq


TEMPERATURE = 0.1
# For custom_model like huggingface add custom_model as value.
SUPPORTED_MODELS = {
    "Mistral Medium": "mistral-medium-latest",
    "Mistral Large": "mistral-large-latest",
    "OpenAI GPT-3.5 Turbo": "gpt-3.5-turbo",
    "OpenAI GPT-4": "gpt-4",
    "OpenAI GPT-4 Turbo": "gpt-4-turbo",
    "OpenAI GPT-4o": "gpt-4o",
    "OpenAI GPT-4o Mini": "gpt-4o-mini",
    "Claude 3.5 Sonnet": "claude-3.5-sonnet-latest",
    "Claude 3.5 Haiku": "claude-3.5-haiku-latest",
    "Claude 3 Opus": "claude-3-opus-latest",
    "HuggingFace Inference API": "custom_model",
    "Ollama Model": "custom_model",
    "Groq Model": "custom_model",
}


def openai_model(model, api_key, prompt):
    """Call OpenAI's ChatCompletion API with a given prompt."""
    openai.api_key = api_key
    response = openai.ChatCompletion.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are an expert in ATS resume scoring."},
            {"role": "user", "content": prompt},
        ],
        temperature=TEMPERATURE,
    )
    return response.choices[0].message.content


def anthropic_model(model, api_key, prompt):
    """Call Anthropic's Claude model with a given prompt."""
    client = anthropic.Anthropic(api_key=api_key)
    response = client.messages.create(
        model=model,
        max_tokens=1000,
        messages=[{"role": "user", "content": prompt}],
        temperature=TEMPERATURE,
    )
    return response.content[0].text


def mistral_model(model, api_key, prompt):
    """Call Mistral's chat completion API with a given prompt."""
    client = Mistral(api_key=api_key)
    response = client.chat.complete(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=TEMPERATURE,
    )
    return response.choices[0].message.content


def ollama_model(model, api, prompt):
    """Call Ollama's API using the official Ollama Python SDK."""

    ollama_model_name = list(model.values())[0]
    # Initialize client with custom host if provided, otherwise use default
    client = Client(host=api) if api else Client()

    try:
        # Generate response using the Ollama SDK
        response = client.generate(
            model=ollama_model_name,
            prompt=prompt,
            stream=False,
        )
        return response["response"]
    except Exception as e:
        raise Exception(f"Failed to call Ollama API: {str(e)}")


def groq_model(model, api, prompt):
    """
    Call Groq's API using the official Groq Python SDK.

    Args:
        model (dict): Dictionary containing model name as value
        api (str): Groq API key
        prompt (str): The prompt to send to the model

    Returns:
        str: The model's response text

    Raises:
        Exception: If the API call fails
    """
    groq_model_name = list(model.values())[0]

    try:
        # Initialize the Groq client with the API key
        client = Groq(api_key=api)

        # Generate response using the Groq SDK
        response = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model=groq_model_name,
            temperature=TEMPERATURE,
        )

        return response.choices[0].message.content

    except Exception as e:
        raise Exception(f"Failed to call Groq API: {str(e)}")


def huggingface_model(model, api_key, prompt):
    """Call Hugging Face's Inference API with fallback handling."""
    custom_model_name = list(model.values())[0]

    def try_inference_api():
        API_URL = f"https://api-inference.huggingface.co/models/{custom_model_name}"
        headers = {"Authorization": f"Bearer {api_key}"}
        payload = {"inputs": prompt}

        response = requests.post(API_URL, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        data = response.json()

        if isinstance(data, list) and data:
            return data[0].get("generated_text", "")
        elif isinstance(data, dict):
            return data.get("generated_text", "")
        raise ValueError(f"Unexpected response format: {data}")

    try:
        # First try the chat completions API
        client = InferenceClient(api_key=api_key)
        messages = [{"role": "user", "content": prompt}]
        completion = client.chat.completions.create(
            model=custom_model_name, messages=messages, timeout=30
        )
        return completion.choices[0].message.content
    except (requests.exceptions.HTTPError, Exception) as e:
        # Fall back to regular inference API
        return try_inference_api()


def route_llm_model(model, api_key, prompt):
    """Route the request to the appropriate LLM model with enhanced error handling."""
    model_dispatch = {
        "OpenAI": openai_model,
        "Claude": anthropic_model,
        "Mistral": mistral_model,
        "HuggingFace Inference API": huggingface_model,
        "Ollama Model": ollama_model,
        "Groq Model": groq_model,
    }

    if not model:
        raise ValueError("Model parameter cannot be None")

    if isinstance(model, dict):
        if not model:
            raise ValueError("Model dictionary cannot be empty")
        model_name = list(model.keys())[0]
    else:
        model_name = model

    # Find the appropriate model handler
    handler = None
    for key, function in model_dispatch.items():
        if model_name.startswith(key):
            handler = function
            break

    if not handler:
        raise ValueError(f"Unsupported model: {model_name}")

    # Get the specific model name or handle custom model
    sub_model_name = SUPPORTED_MODELS.get(model_name)
    if not sub_model_name:
        raise ValueError(f"Unknown model name: {model_name}")

    try:
        if sub_model_name == "custom_model":
            return handler(model, api_key, prompt)
        return handler(sub_model_name, api_key, prompt)
    except Exception as e:
        raise RuntimeError(f"Error calling {model_name}: {str(e)}")


def parse_llm_response(response_text):
    """Parse the LLM response and return a JSON object."""
    try:
        cleaned_response = response_text.strip("```").strip("json").strip('"')
        return json.loads(cleaned_response)
    except json.JSONDecodeError as e:
        raise ValueError(f"Failed to parse LLM response. Error: {e}")


def get_response_from_llm_model(model, api_key, prompt, max_retries=3, retry_delay=2):
    """Fetch response from the LLM model with retry logic."""
    for attempt in range(1, max_retries + 1):
        try:
            # Route the request to the selected LLM model
            response_text = route_llm_model(model, api_key, prompt)
            print(response_text)
            return parse_llm_response(response_text)
        except Exception as e:
            if attempt < max_retries:
                print(
                    f"Attempt {attempt}/{max_retries} failed. Retrying in {retry_delay} seconds..."
                )
                time.sleep(retry_delay)
            else:
                raise RuntimeError(
                    f"Failed to get a response from the LLM after {max_retries} attempts. Error: {e}"
                )
