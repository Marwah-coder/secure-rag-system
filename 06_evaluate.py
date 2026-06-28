import os
import time
from dotenv import load_dotenv
from openai import OpenAI
from generate_module import generate_answer

load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)

JUDGE_MODEL = "openai/gpt-oss-120b:free"

def judge_faithfulness(question, context, answer):
    """
    LLM-as-judge: kya answer SIRF context se aaya, ya kuch khud se bana liya?
    Score 0.0 (poora hallucinated) se 1.0 (poora grounded) ke beech.
    """
    prompt = f"""You are an evaluation judge. Given a CONTEXT and an ANSWER, 
determine if every claim in the ANSWER is supported by the CONTEXT.

CONTEXT:
{context}

ANSWER:
{answer}

Rate faithfulness from 0.0 to 1.0:
- 1.0 = every claim in the answer is directly supported by the context
- 0.5 = some claims supported, some not found in context
- 0.0 = answer contains information not found in context at all (hallucination)

Respond with ONLY a number between 0.0 and 1.0, nothing else."""

    response = client.chat.completions.create(
        model=JUDGE_MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
    )
    score_text = response.choices[0].message.content.strip()
    try:
        return float(score_text)
    except ValueError:
        return None  # judge ne clean number nahi diya

def judge_relevancy(question, answer):
    """
    LLM-as-judge: kya answer actually question ka jawab deta hai?
    """
    prompt = f"""You are an evaluation judge. Given a QUESTION and an ANSWER,
determine how relevant the answer is to the question asked.

QUESTION: {question}

ANSWER: {answer}

Rate relevancy from 0.0 to 1.0:
- 1.0 = answer directly and completely addresses the question
- 0.5 = answer is partially relevant but misses parts of the question
- 0.0 = answer does not address the question at all

Respond with ONLY a number between 0.0 and 1.0, nothing else."""

    response = client.chat.completions.create(
        model=JUDGE_MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
    )
    score_text = response.choices[0].message.content.strip()
    try:
        return float(score_text)
    except ValueError:
        return None

def evaluate_query(question):
    answer, retrieved_chunks = generate_answer(question)
    context = "\n\n".join(retrieved_chunks)

    # Special case: agar system ne honestly "I don't know" bola, to ye CORRECT behavior hai
    if "don't have that information" in answer.lower():
        return {
            "question": question,
            "answer": answer,
            "faithfulness": 1.0,  # correct refusal = faithful (no hallucination)
            "relevancy": 1.0,     # correct refusal = relevant (acknowledges it can't answer)
            "note": "Correctly refused to answer (no hallucination)"
        }

    time.sleep(3)
    faithfulness = judge_faithfulness(question, context, answer)

    time.sleep(3)
    relevancy = judge_relevancy(question, answer)

    return {
        "question": question,
        "answer": answer,
        "faithfulness": faithfulness,
        "relevancy": relevancy,
        "note": ""
    }
if __name__ == "__main__":
    test_questions = [
        "How many days of annual leave do I get and can I carry it forward?",
        "What is the notice period for resignation?",
        "Who is the CEO of NovaTech Solutions?",  # <-- Edge case: handbook mein ye info nahi hai
    ]

    results = []
    for question in test_questions:
        print(f"\nEvaluating: {question}")
        result = evaluate_query(question)
        results.append(result)

        print(f"Answer: {result['answer']}")
        print(f"Faithfulness Score: {result['faithfulness']}")
        print(f"Relevancy Score: {result['relevancy']}")
        print("-" * 60)

    avg_faithfulness = sum(r['faithfulness'] for r in results if r['faithfulness'] is not None) / len(results)
    avg_relevancy = sum(r['relevancy'] for r in results if r['relevancy'] is not None) / len(results)

    print(f"\n=== Overall Results ===")
    print(f"Average Faithfulness: {avg_faithfulness:.2f}")
    print(f"Average Relevancy: {avg_relevancy:.2f}")