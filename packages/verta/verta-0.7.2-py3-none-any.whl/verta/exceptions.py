class StateError(Exception):
    """A required parent entity has not been set."""


class NotFoundError(ValueError):
    """The requested entity could not be found."""
