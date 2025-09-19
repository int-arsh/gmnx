# gmnx

A powerful, colorful, and easy-to-use command-line assistant powered by the Google Gemini API. Get instant help with commands, code snippets, and explanations directly in your terminal, without switching to a browser.

The output is beautifully formatted with syntax highlighting, similar to the `bat` command, for maximum readability.

## Features

-   **Direct Terminal Access:** Get help where you need it most—your command line.
-   **Rich, Colorful Output:** Uses the `rich` library to parse Markdown and provide syntax highlighting for code blocks.
-   **Expert System Prompt:** Engineered to provide concise, accurate, and relevant answers for a command-line environment.
-   **Modern Python SDK:** Built with the latest `google-genai` SDK for Python.
-   **Simple & Secure:** Easy to set up with an alias. Securely uses an environment variable for your API key.

## 🛠️ Setup and Installation

Follow these steps to get the Gemini CLI Assistant running on your system.

### Prerequisites

-   Python 3.x 
-   A Google Gemini API Key. You can get one from [Google AI Studio](https://aistudio.google.com/app/apikey).

### 1. Clone the Repository

If you have uploaded the project to GitHub, clone it to your local machine.

```bash
git clone [https://github.com/your-username/gemini-cli-tool.git](https://github.com/your-username/gemini-cli-tool.git)
cd gemini-cli-tool
```

If you are just setting it up locally, simply navigate to your project directory.
2. Create and Activate a Virtual Environment

It is highly recommended to use a virtual environment to manage project dependencies.

### Create the virtual environment
```bash
python3 -m venv .venv
```
### Activate it
```bash
source .venv/bin/activate
```

### Install Dependencies (local, optional)

If you prefer running locally without Docker:
```bash
pip install -r requirements.txt
```
### Make the Script Executable

This step gives your system permission to run the ask.py file as a program.
```bash
chmod +x ask.py
```
### Set Your API Key and Alias

To make the tool accessible from anywhere, you need to set an environment variable for your API key and create a command-line alias.

Open your shell's configuration file (e.g., ~/.bashrc, ~/.zshrc):
```bash
nano ~/.bashrc
```
Add the following lines to the end of the file. Remember to replace your_api_key_here with your actual key and update the path to your script.

```bash
# Gemini CLI Assistant
export GEMINI_API_KEY='your_api_key_here'
alias ask='/path/to/your/project/gemini-cli-tool/ask.py'
```

Save the file and reload your shell configuration:

```bash
source ~/.bashrc
```

## Usage

You can now use the ask command directly in your terminal. Just wrap your question in quotes.
Examples

Get a Linux command:
```bash
ask "how to find all files larger than 50MB in my home directory"
```
Explain a concept:
```bash
ask "explain the difference between a soft link and a hard link"
```
Get a code snippet:
```bash
ask "write a python function that takes a list and returns a new list with only the even numbers"
```

## You can Read 
https://ai.google.dev/gemini-api/docs/migrate#client \
https://googleapis.github.io/python-genai/index.html \
https://ai.google.dev/gemini-api/docs/pricing

## 🐳 Docker

### Why Docker?
- Consistent environment (no local Python setup required)
- Easy to share and run everywhere
- Keeps your laptop clean and isolated

### Build the image
```bash
docker build -t gmnx .
```

### Run the CLI via Docker
Pass your API key at runtime and your question as args:
```bash
docker run --rm -e GEMINI_API_KEY="$GEMINI_API_KEY" gmnx "explain the difference between soft and hard links"
```

### Optional: mount current directory and set working dir
```bash
docker run --rm -e GEMINI_API_KEY="$GEMINI_API_KEY" -v "$PWD":/work -w /work gmnx "give me a one-liner to count lines"
```

### Optional alias to use `ask` like a local command
```bash
alias ask='docker run --rm -e GEMINI_API_KEY="$GEMINI_API_KEY" gmnx'
ask "how to list all running docker containers"
```

## 🚀 Publish to Docker Hub (easy steps)

### 1) Create a Docker Hub repo
- Go to `https://hub.docker.com`, sign in, click "Create Repository".
- Name it `gmnx` (final image name will be `YOUR_USERNAME/gmnx`).

### 2) Create a Docker Hub access token
- Docker Hub → Account Settings → Security → New Access Token.
- Copy the token (you'll use it in GitHub).

### 3) Add GitHub Secrets to your repo
- On GitHub, open your repo → Settings → Secrets and variables → Actions → New repository secret.
- Add two secrets:
  - `DOCKERHUB_USERNAME` = your Docker Hub username
  - `DOCKERHUB_TOKEN` = the access token you created

### 4) Automatic builds via GitHub Actions
- A workflow at `.github/workflows/docker-publish.yml` builds and pushes images:
  - On push to `main`: tags `latest`
  - On git tag (e.g. `v1.0.0`): tags `v1.0.0` (and keeps `latest` on default branch)

### 5) Trigger a build
```bash
git add .
git commit -m "setup: docker publish workflow"
git push origin main
```
Then check GitHub → Actions for progress. When done, you can pull it:
```bash
docker pull YOUR_USERNAME/gmnx:latest
```

### 6) Create a versioned release (optional)
```bash
git tag v1.0.0
git push origin v1.0.0
```
This publishes `YOUR_USERNAME/gmnx:v1.0.0`.
