from time import gmtime, strftime


def file_writer(data):
    """This function will be use to append all unreachable hosts to the 'unreachable_hosts file'
       Each file will have the timestamp appended to it, to make it easy to track.
    """
    time_string = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    filename = "unreachable_{0}_hosts".format(time_string)
    with open(filename, mode="a") as f:
        f.write(data)
        f.write("\n")

