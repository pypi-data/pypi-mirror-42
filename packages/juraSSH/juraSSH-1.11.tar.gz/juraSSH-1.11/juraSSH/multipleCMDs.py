#!/usr/bin/env python

import paramiko
import time
from multiprocessing import Pool
from juraSSH import file_handler as fh

"""This module will be used to send multiple commands multiple remote machines in parallel.
     """


USERNAME = None
PASSWORD = None

HOSTS_FILE = []
COMMANDS = []

PORT = 22
KEY = False

TIMEOUT = 10
SLEEP_TIME = 8


def connector(hostname):
    """This function allows you to connect to multiple remote machines
    """

    ssh = paramiko.SSHClient()

    try:
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=hostname, username=USERNAME,
                    password=PASSWORD, look_for_keys=KEY, timeout=TIMEOUT, port=PORT)
        print("Connected to {0}\n".format(hostname))

    except:
        fh.file_writer(hostname)  # If a host is unreachable, it will be recorded in a file.
        ssh.close()
    else:
        channel = ssh.invoke_shell()
        channel_data = str()

        for cmd in COMMANDS:

            channel.send(cmd + "\n")
            time.sleep(4)

            output = channel.recv(99999)
            time.sleep(SLEEP_TIME)

            channel_data += output
            channel_data += "\n" * 4

        print(channel_data)
        print("#" * 120)
        print("\n")

        channel.close()
        ssh.close()
        return channel_data


def run_multiple_cmds(username, password, hosts_file, commands_file, cores=25):
    """This function will be used to send multiple commands to remote machines in parallel.
     """
    global USERNAME
    global PASSWORD
    global HOSTS_FILE
    global COMMANDS

    USERNAME = username
    PASSWORD = password
    HOSTS_FILE = hosts_file
    COMMANDS = commands_file

    started = time.asctime()

    p = Pool(cores)
    result = p.map(connector, HOSTS_FILE)
    p.close()
    p.join()

    print("\nProcessing completed !!\n".upper())
    print("Started at: {0}".format(started))
    print("Ended   at: {0}".format(time.asctime()))
    print("\nPLEASE RUN THE [ls] COMMAND TO SEE THE FILE WITH ALL UNREACHABLE HOSTS\n")














