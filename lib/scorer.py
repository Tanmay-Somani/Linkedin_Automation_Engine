def heuristic_score(post_body, hook):
    score = 0
    
    # Rule 1: The "I" factor (Personal authority)
    if hook.lower().startswith("i "): score += 10
    
    # Rule 2: Curiosity Gap
    if "?" in hook: score += 5
    
    # Rule 3: Short is punchy
    if len(hook) < 90: score += 10
    
    # Rule 4: Anti-AI detection (Filter out typical AI phrases)
    forbidden_words = ["delve", "tapestry", "shaping the future", "unlocking", "game-changer"]
    for word in forbidden_words:
        if word in post_body.lower():
            score -= 15
            
    return score