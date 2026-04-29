def evaluate_anomaly(status: int, bytes_size: float, ip_freq: int) -> str:

    if status in [401, 403]:
        return "Data Exfiltration / Mass Download. Action: Terminate active sessions and rotate API keys."
    
    if bytes_size > 1000000:
        return "Data Exfiltration / Mass Download. Action: Terminate active sessions and rotate API keys."
    
    if status in [500, 502, 503]:
        return "Application Crash / Backend Failure. Action: Check stack traces and restart service."
    
    if ip_freq > 500:
        return "Volumetric anomaly (High Frequency). Action: Execute iptables -A INPUT -s <IP> -j DROP."
    
    return "Unknown Anomalous Behavior. Action: Manual SRE investigation required."