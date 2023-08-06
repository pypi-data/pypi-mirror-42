from Scripter import Scripter


class FTP(Scripter):
    cmd = [
        'cd  <DEST_DIR> > <FTP_FILE>',
        'echo open <URL> >> <FTP_FILE>',
        'echo anonymous >> <FTP_FILE>',
        'echo whatever >> <FTP_FILE>',
        'echo binary >> <FTP_FILE>',
        'echo get <FILE> >> <FTP_FILE>',
        'echo bye >> <FTP_FILE>',
        'ftp - s:<FTP_FILE>',
    ]

    def replace_personnal_tag(self, cmd):
        return cmd.replace("<WFTP_FILE>", self.create_path_to_file(self.destination_directory, "ftp.txt"))
