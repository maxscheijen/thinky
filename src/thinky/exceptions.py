class AgentRegistrationException(Exception):
    """Raised when attempting to register an already registered agent."""


class ThinkyNoAgentResponse(Exception):
    """Raised when Agent has no response."""
