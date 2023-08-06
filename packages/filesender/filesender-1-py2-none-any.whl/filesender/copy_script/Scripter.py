import os


class Scripter:
    """
    Template for script
    """
    destination_directory = None
    file_name = None
    url = None
    cmd = []

    def __init__(self, file_name, destination_directory, url):
        self.file_name = file_name
        self.destination_directory = destination_directory
        self.url = url

    def replace_tag(self, cmd):
        """
        Replace all tag by the value
        :param cmd:
        :return:
        """
        return self.replace_personnal_tag(cmd.replace("<DEST_DIR>", self.destination_directory)
                                          .replace("<FILE>", self.file_name)
                                          .replace("<URL>", self.url)
                                          .replace("<TARGET_FILE>",
                                                   self.create_path_to_file(self.destination_directory,
                                                                            self.file_name)))

    def create_path_to_file(self, directory, file_name):
        """
        Create a path to the file
        :param directory: the directory of the file
        :param file_name: the name of the file
        :return: the path
        """
        return os.path.join(directory, file_name)

    def replace_personnal_tag(self, cmd):
        """
        Place here all replace of personal tag
        :param cmd:
        :return:
        """
        return cmd

    def get_one_line_script(self):
        """
        Retrun the script where command are join with &&
        :return:
        """
        return self.replace_tag(" && ".join(self.cmd))

    def get_script_as_list(self):
        """
        retrun a list of command for the script
        :return:
        """
        return [self.replace_tag(elem) for elem in self.cmd]
