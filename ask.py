#!/usr/bin/env python3

import os
import sys
from google import genai
from google.genai import types

from rich.console import Console
from rich.markdown import Markdown

def main():
    if not os.getenv("GEMINI_API_KEY"):
        print("Error: GEMINI_API_KEY environment variable not set.")
        print("Set it by running: export GEMINI_API_KEY='your_api_key'")
        sys.exit(1)

    try:
        client = genai.Client()
    except Exception as e:
        print(f"Error initializing GenAI Client: {e}")
        sys.exit(1)

    if len(sys.argv) < 2:
        print("Usage: ask \"Your question here\"")
        print("Example: ask \"how to list all running docker containers\"")
        sys.exit(0)

    query = " ".join(sys.argv[1:])

    system_prompt = (
    "You are an expert and helpful command-line assistant for a user on a Zsh (Z shell) Ubuntu Linux system. "
    "Provide clear, concise, and accurate answers. "
    "When suggesting commands, prefer Zsh-specific features when relevant, and give a brief one-line explanation of what the command does. "
    "You also help with general programming questions, explain error messages, debug code, and explain code in a simple and beginner-friendly way. "
    "Always format code and commands clearly, without including the word 'shell' or 'bash' in code blocks. "
    "Focus on providing useful answers with minimal fluff."
    "always answer in short unless specified to go deep")


    print("🤖 let me think......")

    try:

        response = client.models.generate_content(
            model='gemini-2.0-flash',
            contents=query,
            config=types.GenerateContentConfig(system_instruction=system_prompt)
        )
         # --- 5. Print the Response with Rich ---
        # Clear the "Asking Gemini..." line
        sys.stdout.write("\033[F\033[K") # Move cursor up one line and clear it
        
        # Initialize Rich Console
        console = Console()
        
        # Create a Markdown object from the response text
        markdown = Markdown(response.text)
        
        # Print the formatted markdown to the console
        console.print(markdown)


    except Exception as e:
        print(f"\nAn error occurred while calling the Gemini API: {e}")
        sys.exit(1)

    

if __name__ == "__main__":
    main()
