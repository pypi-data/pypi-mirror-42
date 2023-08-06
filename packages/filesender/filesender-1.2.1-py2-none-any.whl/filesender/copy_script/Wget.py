from filesender.copy_script.Scripter import Scripter


class Wget(Scripter):
    cmd = ["wget <URL> -o <TARGET_FILE>"]
