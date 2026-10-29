"""Exceptions shared by every CampusFlow module."""


class CampusFlowError(Exception):
    """Base class: main.py catches this to display any expected failure."""


class ValidationError(CampusFlowError):
    """Bad title, category, urgency, affected_users or staff name."""


class TicketNotFoundError(CampusFlowError):
    """No ticket exists with the given ID."""


class TransitionError(CampusFlowError):
    """Illegal status change, or starting an unassigned ticket."""


class StorageError(CampusFlowError):
    """Malformed JSON or JSON of the wrong shape."""