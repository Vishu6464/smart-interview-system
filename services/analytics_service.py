def calculate_overall_analytics(attempts):

    if not attempts:
        return 0, 0

    total = len(attempts)
    avg = sum(a.score for a in attempts) / total

    return total, round(avg, 2)