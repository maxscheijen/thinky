import shutil
import subprocess
from pathlib import Path

SAMPLE_AGENT = '''\
# See https://modelcontextprotocol.io/quickstart/server for source of the tool.
from typing import Any, Dict, Optional

import httpx
from agents import Agent, function_tool
from thinky import register_agent

# Constants
NWS_API_BASE = "https://api.weather.gov"
USER_AGENT = "weather-app/1.0"


async def make_nws_request(url: str) -> Optional[Dict[str, Any]]:
    """Make a request to the NWS API with proper error handling."""
    headers = {"User-Agent": USER_AGENT, "Accept": "application/geo+json"}
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, timeout=30.0)
            response.raise_for_status()
            return response.json()
        except Exception:
            return None


@function_tool
async def get_forecast(latitude: float, longitude: float) -> str:
    """Get weather forecast for a location.

    Args:
        latitude: Latitude of the location
        longitude: Longitude of the location
    """
    # First get the forecast grid endpoint
    points_url = f"{NWS_API_BASE}/points/{latitude},{longitude}"
    points_data = await make_nws_request(points_url)

    if not points_data:
        return "Unable to fetch forecast data for this location."

    # Get the forecast URL from the points response
    forecast_url = points_data["properties"]["forecast"]
    forecast_data = await make_nws_request(forecast_url)

    if not forecast_data:
        return "Unable to fetch detailed forecast."

    # Format the periods into a readable forecast
    periods = forecast_data["properties"]["periods"]
    forecasts = []
    for period in periods[:5]:  # Only show next 5 periods
        forecast = f"""
{period["name"]}:
Temperature: {period["temperature"]}°{period["temperatureUnit"]}
Wind: {period["windSpeed"]} {period["windDirection"]}
Forecast: {period["detailedForecast"]}
"""
        forecasts.append(forecast)

    return "---".join(forecasts)


@register_agent
def weather_forecast_agent():
    return Agent(
        name="weather_forecast_agent", model="llama3.1:latest", tools=[get_forecast]
    )
'''


def sanitize(*, string: str):
    for char in [" ", "-", ".", ",", "?", "!"]:
        string = string.replace(char, "_")
    return string.lower()


def create_file(path: Path, content: str):
    path.write_text(content)


def project_init(name: str, verbose: bool = False) -> None:
    name = sanitize(string=name)

    # Check if `uv` is avialable on the system.
    if not shutil.which("uv"):
        raise ValueError(
            "'uv' is not avialable. See: https://docs.astral.sh/uv/getting-started/installation/"
        )

    # Create project using `uv`
    project_init_cmd = ["uv", "init", "--name", name, "--lib"]

    subprocess.run(project_init_cmd)

    # Create .env with an example path
    create_file(Path(".") / ".env", f"AGENT_DIR_PATH=src/{name}/{name}_agents")

    # Create directory structure
    agent_dir = Path("src") / name / f"{name}_agents"
    agent_dir.mkdir(parents=True, exist_ok=True)
    create_file(agent_dir / "weather_agent.py", SAMPLE_AGENT)

    # TODO: PyPi or Artifactory
    thinky_cmds = ["uv", "add", "/home/maxscheijen/projects/thinky"]

    if not verbose:
        thinky_cmds.append("-qq")

    subprocess.run(thinky_cmds)
