from cloudshell.cli.session.session_exceptions import CommandExecutionException


class BaseAlcatelError(Exception):
    """Base Alcatel Exception"""


class AlcatelCommandExecutionException(CommandExecutionException, BaseAlcatelError):
    """Command Execution Exception"""


class CopyError(AlcatelCommandExecutionException):
    """Copy Error"""
