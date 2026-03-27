"""Utility Functions"""
import os
import time

def ensure_dir(path):
    os.makedirs(path, exist_ok=True)

def get_timestamp():
    return int(time.time())

def clean_filename(name):
    return "".join(c for c in name if c.isalnum() or c in (' ', '-', '_'))
