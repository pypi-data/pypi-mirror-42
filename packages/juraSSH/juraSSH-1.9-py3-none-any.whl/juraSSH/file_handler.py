from time import gmtime, strftime


def file_writer(data):
    """This function will be use to append all unreachable hosts to the 'unreachable_hosts file'
       Each file will have the timestamp appended to it, to make it easy to track.
    """

    with open("unreachable-hosts.txt", mode="a") as f:
        f.write(data)
        f.write("\n")

