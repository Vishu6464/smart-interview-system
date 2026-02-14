def calculate_score(user_answer: str, ideal_answer: str) -> int:
    if not user_answer.strip():
        return 0

    user_words = set(user_answer.lower().split())
    ideal_words = set(ideal_answer.lower().split())

    common = user_words.intersection(ideal_words)

    similarity = len(common) / max(len(ideal_words), 1)

    return int(similarity * 10)