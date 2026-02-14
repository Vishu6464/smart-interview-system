from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# Load model once (global)
model = SentenceTransformer("all-MiniLM-L6-v2")


def calculate_score(user_answer: str, ideal_answer: str) -> int:

    if not user_answer.strip():
        return 0

    # Convert text to embeddings
    embeddings = model.encode([user_answer, ideal_answer])

    similarity = cosine_similarity(
        [embeddings[0]],
        [embeddings[1]]
    )[0][0]

    # Convert similarity (0–1) to score (0–10)
    score = int(similarity * 10)

    return min(max(score, 0), 10)