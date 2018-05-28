import sys
import subprocess
import time
import socket
import tempfile
from pathlib import Path


def speak_word(arg: str):
    with tempfile.NamedTemporaryFile(mode='w+t', delete=False) as tf:
        tf_path = tf.name
        tf.write(arg)

    with tempfile.NamedTemporaryFile(mode='w+t', delete=False, suffix=".wav") as sf:
        sf_path = sf.name
        command = ["open_jtalk", "-m", htsvoice_path, "-x", mecab_dict_path, "-ow", sf_path, tf_path]
        subprocess.run(command)
        command = [sound_player, sf_path]
        subprocess.run(command)


def search_word(arg: str):
    print(arg)
    if arg in positives:
        speak_word(word + "!")
    elif arg in negatives:
        speak_word(word + "?")


def make_word_list(pos_file: Path, neg_file: Path) -> (list, list):
    pos_list = []
    neg_list = []

    with pos_file.open(mode='r') as pf:
        for row in pf:
            pos_list.append(row.strip())
    with neg_file.open(mode='r') as nf:
        for row in nf:
            neg_list.append(row.strip())

    return pos_list, neg_list


host = "127.0.0.1"
port = 10500
htsvoice_path = "/usr/local/Cellar/open-jtalk/1.10_1/voice/mei/mei_normal.htsvoice"
mecab_dict_path = "/usr/local/Cellar/open-jtalk/1.10_1/dic"
sound_player = "afplay"

if __name__ == '__main__':
    args = sys.argv

    if len(args) < 4:
        print("python3 voice_response.py <launcher.sh> <positive words> <negative words>")
        exit(0)

    launcher_path = Path(args[1])
    pos_path = Path(args[2])
    neg_path = Path(args[3])

    positives, negatives = make_word_list(pos_path, neg_path)

    process = subprocess.Popen([launcher_path.absolute()], stdout=subprocess.PIPE,
                               cwd=launcher_path.parent)
    process_id = process.stdout.read()
    time.sleep(5)
    this_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    this_socket.connect((host, port))

    std_arg = ""
    while True:
        std_arg = str(this_socket.recv(1024).decode("utf-8"))
        arg_split = std_arg.split('\n')
        for line in arg_split:
            index = line.find("WORD")
            if index != -1:
                word = line[index + 6:line.find('"', index + 6)]
                search_word(word)
        time.sleep(0.1)
