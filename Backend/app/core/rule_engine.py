def evaluate_anomaly(status: int, bytes_size: float, ip_freq: int) -> str:

    if status in [401, 403]:
        return "Symptom: High volume of unauthorized (4xx) requests. Hint to LLM: Check context for recent auth or rate limiting changes."
    
    if bytes_size > 1000000:
        return "Symptom: Massive data payload detected in a single response. Hint to LLM: Check context for any intentional payload size increases."
    
    if status in [500, 502, 503]:
        return "Symptom: Server responded with fatal backend errors (5xx) with 0 byte payloads. Hint to LLM: Check context for recent architectural rewrites affecting memory or backend stability."
    
    if ip_freq > 500:
        return "Symptom: Abnormal spike in request frequency from a single IP. Hint to LLM: Check context for rate limiting status."
    
    return "Symptom: Unknown anomalous behavior."