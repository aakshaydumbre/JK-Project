import torch
from transformers import pipeline

try:
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
except Exception as e:
    summarizer = None
    print(f"⚠️ Error loading Hugging Face model: {e}")


def generate_summary(text: str) -> str:
    """
    Generates a summary using the Hugging Face Transformers model.
    """

    # Dynamically set max_length based on input length
    input_length = len(text.split())  # Count words
    max_length = min(50, input_length)  # Ensure max_length is smaller than input

    try:
        summary = summarizer(text, max_length=max_length, min_length=10, do_sample=False)
        return summary[0]['summary_text']
    except Exception as e:
        return f"Error: {str(e)}"

def generate_review_summary(reviews: list) -> str:
    """
    Generates a summary from multiple user reviews.
    """
    combined_reviews = " ".join(reviews)
    return generate_summary(combined_reviews)

if __name__ == "__main__":
    summary = generate_summary("The Alchemist is about a young shepherd following his dreams.")
    print("Generated Summary:", summary)