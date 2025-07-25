import shutil
import subprocess
from importlib import resources
from pathlib import Path

import questionary

from thinky import _agents

example_file = resources.files(_agents) / "_example_agent.py"

with example_file.open("r") as fp:
    SAMPLE_AGENT = fp.read()


def sanitize(*, string: str) -> str:
    for char in [" ", "-", ".", ",", "?", "!"]:
        string = string.replace(char, "_")
    return string.lower()


def create_file(path: Path, content: str) -> None:
    path.write_text(content)


def project_init(name: str, verbose: bool = False) -> None:
    name = sanitize(string=name)

    provider = questionary.select(
        "Select a model provider", choices=["ollama", "openai", "azure"]
    ).ask()

    # Check if `uv` is avialable on the system.
    if not shutil.which("uv"):
        raise ValueError(
            "'uv' is not avialable. See: https://docs.astral.sh/uv/getting-started/installation/"
        )

    # Create project using `uv`
    project_init_cmd = ["uv", "init", "--name", name, "--lib"]

    subprocess.run(project_init_cmd)

    # Create .env with an example path
    sample_dot_env = (
        f"AGENT_DIR_PATH=src/{name}/{name}_agents\n"
        f"PROVIDER={provider}\n"
        f"BASE_URL=http://localhost:11434/v1\n"
    )
    create_file(Path(".") / ".env", sample_dot_env)

    # Create directory structure
    agent_dir = Path("src") / name / f"{name}_agents"
    agent_dir.mkdir(parents=True, exist_ok=True)
    create_file(agent_dir / "weather_agent.py", SAMPLE_AGENT)

    # TODO: PyPi or Artifactory
    thinky_cmds = ["uv", "add", "/Users/maxscheijen/projects/thinky"]

    if not verbose:
        thinky_cmds.append("-qq")

    subprocess.run(thinky_cmds)
