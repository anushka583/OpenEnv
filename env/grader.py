def grade(answer, reference):
    answer_words = set(answer.lower().split())
    ref_words = set(reference.lower().split())

    overlap = len(answer_words & ref_words)
    total = len(ref_words)
    keyword_score = overlap / total if total > 0 else 0
    length_score = min(len(answer_words) / 20, 1.0)  # cap at 1
    score = (0.6 * keyword_score) + (0.4 * length_score)

    return round(min(score, 1.0), 2)