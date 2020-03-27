

def error_message(step_prefix, message, is_known=True):
    error_intro = "Error with known origin occured" if is_known \
        else "Error with unknown origin occured"
    return f"[{step_prefix}] {error_intro}: {message}"