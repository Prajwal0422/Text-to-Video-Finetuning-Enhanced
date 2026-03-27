"""Helper Functions"""
def format_duration(seconds):
    return f"{int(seconds)}s"

def format_size(bytes):
    return f"{bytes / 1024 / 1024:.2f} MB"

def validate_prompt(prompt):
    return len(prompt) > 3 and len(prompt) < 500
