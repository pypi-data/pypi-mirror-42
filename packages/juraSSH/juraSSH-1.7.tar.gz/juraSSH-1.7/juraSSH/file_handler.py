from time import gmtime, strftime


def file_writer(data):
    """This function will be use to append all unreachable hosts to the 'unreachable_hosts file'
       Each file will have the timestamp appended to it, to make it easy to track.
    """
    time = strftime("%Y-%m-%d %H:%M:%S", gmtime())

    day, hours = time.split()
    new_time = "unreachable_hosts_{}-{}.txt".format(day, hours)
    new_time = new_time.replace(":", "")

    with open(new_time, mode="a") as f:
        f.write(data)
        f.write("\n")

