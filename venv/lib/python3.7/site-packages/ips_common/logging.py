import logging


def database_logger() -> logging.Logger:
    """
    Author        : Elinor Thorne
    Date          : 5 Jan 2018
    Purpose       : Sets up and returns database logger object
    Parameters    : None
    Returns       : Database logger object
    Requirements  : None
    Dependencies  : social_surveys.setup_logging
    """
    return logging.getLogger(__name__)


def standard_log_message(err_msg: str, current_working_file: str, func_name: str) -> str:
    """
    Author        : Elinor Thorne
    Date          : 5 Jan 2018
    Purpose       : Creates a standard log message which includes the user's
                  : error message, the filename and function name
    Parameters    : err_msg - user's custom error message
                  : current_working_file - source dir path of failure
                  : func_name - source function of failure
    Returns       : String
    Requirements  : None
    Dependencies  : None
    """

    return (err_msg
            + ' - File "' + current_working_file
            + '", in ' + func_name + '()')


log = database_logger()

