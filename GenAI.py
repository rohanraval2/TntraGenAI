from openai import OpenAI
from transformers import pipeline

api_key = "your-OpenAI-api-key"
client = OpenAI(api_key=api_key)

import google.generativeai as genai
import os
os.environ['GOOGLE_API_KEY'] = "your-Gemini-api-key"
genai.configure(api_key=os.environ['GOOGLE_API_KEY'])
model = genai.GenerativeModel('gemini-pro')

summarizer = pipeline("summarization", model="facebook/bart-large-cnn")


system_message = {"role": "system", "content": "You are a knowledgeable and concise assistant. For every user query, briefly explain the concept in simple terms, and then provide short challenge questions to test the user's understanding of the concept."}


def summarize_to_half(text):
    original_length = len(text.split())

    max_length = (original_length * 2) // 3

    summary = summarizer(text, max_length=original_length,
                         min_length=max_length, do_sample=False)

    return summary[0]['summary_text']


def generate(title, content, summarize = False):
    if summarize:
        content = summarize_to_half(content)

    prompt = title + "\n" + f"based on the context: \n {content}"
    try:
        stream = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[system_message, {"role": "user", "content": prompt}],
            stream=True,
        )

        generated_answer = ""

        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                generated_answer += chunk.choices[0].delta.content

    except:
        generated_answer = "Empty"

    return generated_answer

def google_generate(title, content):
    try:
        explanation = model.generate_content(f"Generate a brief explanation on the following topic {title} with context : {content}")
        explanation_answer = explanation.text
        questions = model.generate_content(f"Generate 3 practical challenge questions on the following {explanation_answer}")
        question_answer = questions.text
        generated_answer = explanation_answer +"\n" + question_answer

    except:
        generated_answer = "empty"

    return generated_answer



