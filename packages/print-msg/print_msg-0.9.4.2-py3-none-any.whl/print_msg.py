from termcolor import colored


def print_msg(status: str, msg: str, end='\n'):
    """Print status messages.
    status = 'ok', 'status' or 'error'."""
    if status == 'ok':
        print('[--{0}--] - {1}'.format(colored('OK', 'green'),
                                       colored(msg, 'yellow')), end=end)
    elif status == 'error':
        print('[{0}] - {1}'.format(colored('ERROR!', 'red'),
                                   colored(msg, 'magenta')), end=end)
    elif status == 'status':
        print('[{0}] - {1}'.format(colored('STATUS', 'yellow'),
                                   colored(msg, 'green')), end=end)
    elif status == 'time':
        print('[-{0}-] - {1}'.format(colored('TIME', 'magenta'),
              'Execution time -> {0}'.format(msg)), end=end)
