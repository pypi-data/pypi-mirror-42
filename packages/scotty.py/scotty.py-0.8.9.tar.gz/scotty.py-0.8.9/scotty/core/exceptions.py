class ScottyException(Exception):
    """Scotty standardexception."""

    pass


class ExperimentException(ScottyException):
    """Exception for experiment."""

    pass


class WorkloadException(ScottyException):
    """Exception for workloads."""

    pass


class ResourceException(ScottyException):
    """Exception for resources."""

    pass
