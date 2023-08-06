import logging

def enable_log(log_name):
    """ Enable logs written to file """
    logging.basicConfig(filename= log_name,
                        level=logging.INFO,
                        format='%(asctime)s %(levelname)s %(message)s')
