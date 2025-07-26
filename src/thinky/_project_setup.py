import re
import shutil
import subprocess
from enum import Enum
from importlib import resources
from pathlib import Path
from typing import Type

import questionary

from thinky import _agents

example_file = resources.files(_agents) / "_example_agent.py"

with example_file.open("r") as fp:
    SAMPLE_AGENT = fp.read()


class Provider(str, Enum):
    AZURE = "azure"
    OLLAMA = "ollama"


def question_select(choice: Type[Enum]) -> questionary.Question:
    name = choice.__name__
    prompt = re.sub(r"(?<!^)(?=[A-Z])", " ", name).lower()
    choices = [option.value for option in choice]
    return questionary.select(f"Select the {prompt}:", choices=choices)


def sanitize(*, string: str) -> str:
    return re.sub(r"[ \-.,?!]+", "_", string).lower()


def create_file(path: Path, content: str) -> None:
    path.write_text(content)


def project_init(verbose: bool = False) -> None:
    name = questionary.text(
        "Name of your project:", qmark="-", default=Path.cwd().name
    ).ask()

    if not name:
        raise ValueError("Project name cannot be empty.")

    name = sanitize(string=name)

    provider = question_select(Provider).ask()
    env_lines = [
        f"AGENT_DIR_PATH=src/{name}/custom_agents",
        f"PROVIDER={provider}",
    ]

    if provider == "ollama":
        ollama_base_url = questionary.text(
            message="OLLAMA BASE URL:", qmark="-", default="http://localhost:11434/v1"
        ).ask()
        env_lines.append(f"BASE_URL={ollama_base_url}")

    if provider == "azure":
        azure_openai_endpoint = questionary.text(
            "AZURE OPENAI ENDPOINT:", qmark="-"
        ).ask()
        azure_openai_api_version = questionary.text(
            "AZURE OPENAI API VERSION:", qmark="-"
        ).ask()

        env_lines.extend(
            [
                f"AZURE_OPENAI_ENDPOINT={azure_openai_endpoint}",
                f"OPENAI_API_VERSION={azure_openai_api_version}",
            ]
        )

        azure_auth_method = questionary.select(
            "Auth method", choices=["AZURE API KEY", "TOKEN PROIVDER"]
        ).ask()

        if azure_auth_method == "AZURE API KEY":
            azure_openai_api_key = questionary.password(
                "AZURE OPENAI API KEY:", qmark="-"
            ).ask()
            env_lines.append(f"AZURE_OPENAI_API_KEY={azure_openai_api_key}")

        elif azure_auth_method == "TOKEN PROVIDER":
            raise NotImplementedError(
                "Token provider authentication is not yet implemented."
            )
    sample_dot_env = "\n".join(env_lines) + "\n"

    # Check if `uv` is avialable on the system.
    if shutil.which("uv") is None:
        raise RuntimeError(
            "'uv' is not available. Install it: https://docs.astral.sh/uv/getting-started/installation/"
        )

    # Create project using `uv`
    project_init_cmd = ["uv", "init", "--name", name, "--lib"]

    subprocess.run(project_init_cmd, check=True)

    # Create .env with an example path
    env_file = Path(".env")
    create_file(env_file, sample_dot_env)

    # Create directory structure
    agent_dir = Path("src") / name / "custom_agents"
    agent_dir.mkdir(parents=True, exist_ok=True)
    create_file(agent_dir / "weather_agent.py", SAMPLE_AGENT)

    # TODO: PyPi or Artifactory
    thinky_cmds = ["uv", "add", "/Users/maxscheijen/projects/thinky"]

    if not verbose:
        thinky_cmds.append("-qq")

    subprocess.run(thinky_cmds, check=True)
