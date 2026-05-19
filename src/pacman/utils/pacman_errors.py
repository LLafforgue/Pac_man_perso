from typing_extensions import Self


class PacmanErrors(Exception):

    TYPES = {
        "config": "\033[1;31mConfig_error\033[0m : ",
        "ui": "\033[1;31mUser_error\033[0m : ",
        "arg": "\033[1;31mArgument_error\033[0m : ",
        "unknown": "\033[1;31mUnknown_error\033[0m : ",
    }

    def __init__(self,
                 type_error: str,
                 err_message: str,
                 program: str = '') -> Self:
        """Initialize the errors messages"""
        if type_error.lower() in self.TYPES:
            valid_type_error = self.TYPES[type_error.lower()]
        else:
            valid_type_error = self.TYPES["unknown"]

        if isinstance(err_message, str):
            valid_err_message = err_message
        else:
            valid_err_message = ""

        message = (
                    valid_type_error
                    + (valid_err_message + " "
                       if valid_err_message[-1] != ' ' else '')
                    + program
        )
        super().__init__(message)
