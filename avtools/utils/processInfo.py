import psutil


class ProcessInfo(object):
    """
    Helps to check if a given process/service is running.
    """
    def __init__(self):
        self.process_id = None
        self.service_name = None
        self.process_name = None
        self.counter = 0

    def get_process_status(self, process_name):
        """
        Checks for the process is running on given machine and returns
        True/False

        :param process_name:
        :return:
        """
        self.process_name = process_name
        self.process_id = self.get_process_id(self.process_name)
        if self.process_id is None and self.counter > 0:
            print "Process {} is stopped".format(self.process_name)

        elif self.process_id is None and self.counter == 0:
            print "Process {} is not running, please check your service " \
                  "launcher".format(self.process_name)

        if psutil.pid_exists(self.process_id):
            print "Process with pid {} exists".format(self.process_id)
            return True
        else:
            print "Process with pid {} does not exist".format(self.process_id)
            return False

    def get_process_id(self, process_name):
        """
        Get Process id of the given process name.
        :param process_name:
        :return:
        """
        for p in psutil.process_iter():
            if process_name in p.name():
                self.process_id = p.pid
                self.counter += 1
                print "Process with name {} found , it has process " \
                      "id {} ".format(process_name, self.process_id)
                return self.process_id

        return None

    @staticmethod
    def get_multiple_process_id(process_name):
        """
        Get pid numbers as list of a given process name.
        This helps when there are multiple instances of process runs with
        different PID's
        :param process_name:
        :return:
        """
        process_ids = []
        list_counter = 0
        for p in psutil.process_iter():
            if process_name in p.name():
                process_id = p.pid
                list_counter += 1
                print "Process with name {} found , it has process " \
                      "id {} ".format(process_name, process_id)
                process_ids.append(process_id)
        print "we have {}  Process ID's for Process Name {}".format(
                                                list_counter, process_name)

        return process_ids
