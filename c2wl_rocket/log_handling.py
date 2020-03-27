"""
    This module contains log handling utilitis.
    Please note, the loggers are used from cwltool.
"""

from cwltool.loghandler import _logger as logger

def error_message(step_prefix, message, is_known=True):
    error_intro = "Error with known origin occured" if is_known \
        else "Error with unknown origin occured"
    return f"[{step_prefix}] {error_intro}: {message}"

def message(step_prefix, message):
    return f"[{step_prefix}] {message}"