from juraSSH import parallel

def run_multiple_cmds(username, password, commands, hosts_file, port=22, key=False, timeout=10, sleep_time=6):

    """
    This function allows you to run a multiple commands on multiple remote machines
        in parallel
    """

    parallel.USERNAME = username
    parallel.PASSWORD = password
    parallel.COMMAND = commands
    parallel.HOSTS_FILE = hosts_file

    parallel.KEY = key
    parallel.PORT = port
    parallel.TIMEOUT = timeout
    parallel.SLEEP_TIME = sleep_time

    parallel.selector(parallel.send_multiple_commands)
