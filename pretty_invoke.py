#!/usr/bin/env python3
"""Pretty print agentcore responses"""
import subprocess
import sys
import json
import re

def invoke(prompt):
    cmd = ['agentcore', 'invoke', json.dumps({"prompt": prompt})]
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    output = result.stdout + result.stderr
    
    # Try to extract the text content
    match = re.search(r"'text':\s*[\"'](.+?)[\"']\s*}\s*]\s*}", output, re.DOTALL)
    if match:
        text = match.group(1)
        text = text.replace('\\n', '\n')
        print("\n" + "="*60)
        print(text)
        print("="*60 + "\n")
    else:
        print(output)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        invoke(" ".join(sys.argv[1:]))
    else:
        print("Usage: python3 pretty_invoke.py <your question>")
