def evaluate_agent_response(messages):

    problems = []

    for msg in messages:

        text = msg.lower()

        if "pay immediately" in text:
            problems.append("aggressive_payment_request")

        if "you must pay" in text:
            problems.append("threatening_language")

        if "i don't understand" in text:
            problems.append("weak_response")

        if "switching phase" in text:
            problems.append("internal_logic_exposed")

    if len(problems) == 0:
        return "good"

    return {
        "issues_found": problems
    }