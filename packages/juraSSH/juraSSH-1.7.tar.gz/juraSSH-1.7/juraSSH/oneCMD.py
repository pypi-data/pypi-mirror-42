#!/usr/bin/env python

import paramiko
import time
from multiprocessing import Pool
from juraSSH import file_handler as fh

__author__ = "David Johnnes"
__email__ = "david.johnnes@gmail.com"

"""
    This module allows you to send a single command to multiple remote host in parallel
"""

USERNAME = ""
PASSWORD = ""

HOSTS_FILE = []
COMMAND = ""

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


def run_one_cmd(username, password, hosts_file, command, cores=25):
    """This function will be used to send single command to multiple remote machines in parallel.
     """
    global USERNAME
    global PASSWORD
    global HOSTS_FILE
    global COMMAND

    USERNAME = username
    PASSWORD = password
    HOSTS_FILE = hosts_file
    COMMAND = command

    started = time.asctime()

    p = Pool(cores)
    result = p.map(connector, HOSTS_FILE)
    p.close()
    p.join()

    print("\nProcessing completed !!\n".upper())
    print("Started at: {0}".format(started))
    print("Ended   at: {0}".format(time.asctime()))
    print("\nPLEASE RUN THE [ls] COMMAND TO SEE THE FILE WITH ALL UNREACHABLE HOSTS\n")













