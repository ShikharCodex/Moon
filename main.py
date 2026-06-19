import os
import json
import re
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI
from rich.console import Console

# ----------------------------
# Setup
# ----------------------------

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

console = Console()

PROJECTS_DIR = Path("projects")
PROJECTS_DIR.mkdir(exist_ok=True)

# ----------------------------
# Helpers
# ----------------------------

def slugify(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-")


def create_project_folder(project_name: str) -> Path:
    project_path = PROJECTS_DIR / project_name
    project_path.mkdir(parents=True, exist_ok=True)
    return project_path


def save_files(project_path: Path, files: dict):
    for filename, content in files.items():

        file_path = project_path / filename

        file_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        with open(
            file_path,
            "w",
            encoding="utf-8"
        ) as f:
            f.write(content)

        console.print(
            f"[green]✓ Created:[/green] {filename}"
        )


# ----------------------------
# AI Generator
# ----------------------------

def generate_project(user_prompt: str):

    prompt = f"""
You are an expert software engineer.

Create a complete project.

User Request:
{user_prompt}

Return ONLY valid JSON.

Format:

{{
  "project_name": "snake-game",
  "files": {{
      "index.html": "...",
      "style.css": "...",
      "script.js": "..."
  }}
}}

Rules:
1. Return only JSON.
2. No markdown.
3. No explanations.
4. Include complete working code.
"""

    response = client.responses.create(
        model="gpt-5",
        input=prompt
    )

    text = response.output_text.strip()

    try:
        data = json.loads(text)
        return data

    except Exception as e:
        console.print(
            f"[red]JSON Error:[/red] {e}"
        )

        print(text)
        return None


# ----------------------------
# Main
# ----------------------------

def main():

    console.print(
        "\n[bold cyan]The Moon AI Agent[/bold cyan]\n"
    )

    user_prompt = input(
        "What do you want to build today?\n> "
    )

    console.print(
        "\n[yellow]Generating project...[/yellow]\n"
    )

    result = generate_project(
        user_prompt
    )

    if not result:
        return

    project_name = result["project_name"]

    files = result["files"]

    project_path = create_project_folder(
        project_name
    )

    save_files(
        project_path,
        files
    )

    console.print(
        f"\n[bold green]Project created:[/bold green]"
    )

    console.print(
        str(project_path.resolve())
    )


if __name__ == "__main__":
    main()