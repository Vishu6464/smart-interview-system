def calculate_score(user_answer: str, ideal_answer: str) -> int:
    if not user_answer.strip():
        return 0

    user = user_answer.lower().strip()
    ideal = ideal_answer.lower().strip()

    # Exact match
    if user == ideal:
        return 100

    user_words = set(user.split())
    ideal_words = set(ideal.split())

    common = user_words.intersection(ideal_words)

    if not ideal_words:
        return 0

    similarity = len(common) / len(ideal_words)

    # Scale properly to 100
    score = int(similarity * 100)

    # Improve fairness
    if similarity > 0.8:
        return 90
    elif similarity > 0.6:
        return 75
    elif similarity > 0.4:
        return 60
    elif similarity > 0.2:
        return 40
    else:
        return 20