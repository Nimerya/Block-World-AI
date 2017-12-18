import datetime
import subprocess
import shlex
from sentence import Sentence as S

now = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")


def main():
    lp_file = open("files/instance_{}".format(now), "w")
    lp_file.write("#include \"_block_world_base_engine.lp\". \n")
    while True:
        text = input("Insert a phrase: ")
        sentence = S(text)
        sentence.info()
        statements = sentence.translate()
        for item in statements:
            lp_file.write("{}{}".format(item, "\n"))
            print("added: {}".format(item))
        if not sentence.assertion:
            break
    lp_file.close()
    run_command("clingo -t 4 {}".format(lp_file))


def run_command(command):
    out_file = open("files/out_{}".format(now), "w")

    process = subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE)
    while True:
        output = process.stdout.readline()
        if output == '' and process.poll() is not None:
            break
        if output:
            print(output.strip())
            out_file.write(output.strip())

    rc = process.poll()
    return rc


if __name__ == "__main__":
    main()
