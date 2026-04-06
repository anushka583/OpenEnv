def baseline_agent(state):
    results = {}

    for task_id in ["easy", "medium", "hard"]:
        docs = [d["text"] for d in state.get("documents", [])]

        if task_id == "easy":
            combined = " ".join(docs)
            answer = combined[:300].strip()

        elif task_id == "medium":
            combined = " ".join(docs)
            sentences = combined.split(".")
            unique_sentences = []
            seen = set()

            for s in sentences:
                s_clean = s.strip().lower()
                if s_clean and s_clean not in seen:
                    seen.add(s_clean)
                    unique_sentences.append(s.strip())

            answer = ". ".join(unique_sentences[:3])

        elif task_id == "hard":
            pros = []
            cons = []

            for d in docs:
                text = d.lower()

                if any(word in text for word in ["benefit", "advantage", "improve", "increase"]):
                    pros.append(d.strip().split(".")[0])

                if any(word in text for word in ["risk", "drawback", "limitation", "decrease"]):
                    cons.append(d.strip().split(".")[0])

            if not pros and docs:
                pros = [docs[0][:80]]

            if not cons and len(docs) > 1:
                cons = [docs[1][:80]]

            pros = list(set(pros))
            cons = list(set(cons))

            intro = "Key advantages include " if pros else ""
            middle = "On the other hand, limitations include " if cons else ""

            answer = intro + ", ".join(pros)
            if cons:
                answer += ". " + middle + ", ".join(cons)

            if pros and cons:
                answer += ". Overall, a balance between benefits and risks is required."

        else:
            answer = ""

        answer = answer.strip().capitalize()
        answer = answer[:400]

        results[task_id] = answer

    return results