from huggingface_hub import InferenceClient

# Use lightweight hosted model
client = InferenceClient("HuggingFaceH4/zephyr-7b-beta", token='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')  # Fast & good for summarization

def call_llm(prompt):
    try:
        response = client.text_generation(prompt, max_new_tokens=200)
        return response.strip()
    except Exception as e:
        return f"❌ Error during model call: {e}"
