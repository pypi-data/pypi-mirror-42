import os
import subprocess

from filesender.copy_script.Scripter import Scripter


class Hex(Scripter):

    def __init__(self, file_name, destination_directory, url):
        Scripter.__init__(self, file_name, destination_directory, url)
        tmp_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "../tmp")
        file_path = os.path.join(tmp_dir, file_name)
        self.execute("/usr/bin/upx -9 {}".format(file_path))
        exe2bat = self.execute("locate exe2bat ").replace("\n", "")
        txt_path = os.path.join(tmp_dir, "file.txt")
        cmd = "wine {} {} {}".format(exe2bat, file_path, txt_path)
        hex_file = os.path.join(destination_directory, "123.hex")
        self.execute(cmd)
        with open(txt_path, "r") as f:
            for line in f.readlines():
                self.cmd.append(line.replace("123.hex", hex_file)
                                .replace(file_path, os.path.join(destination_directory, file_name)))

    def execute(self, cmd):
        """
        Execute the shell command and return the output
        :param cmd: the shell command
        :return: the output or None if error
        """
        rep = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        return rep.stdout.read()
