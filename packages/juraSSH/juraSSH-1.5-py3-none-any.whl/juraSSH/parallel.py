#!/usr/bin/env python

import paramiko
import time
from multiprocessing import Pool
from juraSSH import file_handler as fh

__author__ = "David Johnnes"
__email__ = "david.johnnes@gmail.com"

"""
    This module allows you to send a single command to multiple remote host in parallel or
    multiple commands to multiple hosts in parallel.
    ================================================

    *You can create custom function by importing this module.
    *If you do not want to create you own functions , you can use the oneCDM or the multipleCDMs function,
    for they are already completed.
"""

USERNAME = ""
PASSWORD = ""

HOSTS_FILE = []
COMMAND = ""
COMMANDS = []

PORT = 22
KEY = False

TIMEOUT = 10
SLEEP_TIME = 8


def send_one_command(hostname):
    """
    This function allows you to run a single command on multiple remote machines in parallel
    """
    ssh = paramiko.SSHClient()
    try:
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        ssh.connect(hostname=hostname, username=USERNAME, password=PASSWORD,
                    port=PORT, look_for_keys=KEY, timeout=TIMEOUT)
        print("\nConnected to == >> {0}\n".format(hostname))
    except:
        fh.file_writer(hostname)    # If a host is unreachable, it will be recorded in a file.
        ssh.close()
    else:
        channel = ssh.invoke_shell()
        channel.send(COMMAND + "\n")
        time.sleep(4)

        output = channel.recv(9999)
        time.sleep(SLEEP_TIME)

        channel.send("exit\n")

        channel.close()
        ssh.close()
        print(output)
        print("#" * 120)


def send_multiple_commands(hostname):
    """
    This function allows you to run multiple commands on multiple remote machines in parallel
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
            time.sleep(2)

            output = channel.recv(99999)
            time.sleep(SLEEP_TIME)

            channel_data += output
            channel_data += "\n"*4

        print(channel_data)
        print("#" * 120)
        print("\n")

        channel.close()
        ssh.close()
        return channel_data


def selector(func_name, cores=25):
    """
     This function is used to select the function you would like to execute.
     """
    started = time.asctime()

    p = Pool(cores)
    p.map(func_name, HOSTS_FILE)
    p.close()
    p.join()

    print("\nProcessing completed !!\n".upper())
    print("Started at: {0}".format(started))
    print("Ended   at: {0}".format(time.asctime()))
    print("\nPLEASE RUN THE [ls] COMMAND TO SEE THE FILE WITH ALL UNREACHABLE HOSTS\n")


def run_onecmd(cores=25):
    """
     This function will be used to send a single command in parallel.
     """

    started = time.asctime()

    p = Pool(cores)
    p.map(send_one_command, HOSTS_FILE)
    p.close()
    p.join()

    print("\nProcessing completed !!\n".upper())
    print("Started at: {0}".format(started))
    print("Ended   at: {0}".format(time.asctime()))
    print("\nPLEASE RUN THE [ls] COMMAND TO SEE THE FILE WITH ALL UNREACHABLE HOSTS\n")


def run_multiple_cmds(cores=25):
    """
     This function will be used to send multiple commands in parallel.
     """
    started = time.asctime()

    p = Pool(cores)
    p.map(send_multiple_commands, HOSTS_FILE)
    p.close()
    p.join()

    print("\nProcessing completed !!\n".upper())
    print("Started at: {0}".format(started))
    print("Ended   at: {0}".format(time.asctime()))
    print("\nPLEASE RUN THE [ls] COMMAND TO SEE THE FILE WITH ALL UNREACHABLE HOSTS\n")











