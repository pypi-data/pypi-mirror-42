import logging

def enable_log(log_name):
    """ Enable logs written to file """
    logging.basicConfig(filename= log_name + ".log",
                        level=logging.DEBUG,
                        format='%(asctime)s %(levelname)s %(message)s')
