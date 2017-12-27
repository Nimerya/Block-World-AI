import datetime
import subprocess
import shlex
from sentence import Sentence as S

now = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")


def main():
    # set that will contains the already processed blocks
    processed_blocks = set()
    # file in which wthe generated rules will be stored
    lp_file = open("files/instance_{}.lp".format(now), "w")
    # initialize the goal string
    goal = "goal(T) :- time(T),"
    # optimization statement
    opt = "number_of_moveop(M):- M=#count{X,Y,T: moveop(X,Y,T)}.\n#minimize{M: number_of_moveop(M)}.\n"
    # cycle
    print("starting insertion loop...")
    print("end the insertion with either a QUERY or by writing \"done\" after you have provided the goals (if any)")
    while True:
        # read the input
        print("-------------------------------------")
        text = input("Insert a phrase: ")
        # if the user writes "done" than the solver is launched
        if text == "done":
            lp_file.write("time(0..{}).\n".format(len(processed_blocks)*2))
            # write the final goal and the show directives
            lp_file.write("{}.\n".format(goal[:-1]))
            # write the final goal and the show directives
            lp_file.write("{}\n#show moveop/3.\n#show goal.\n".format(opt))
            # add in the instance file the include of the main engine of the solver
            lp_file.write("#include \"_block_world_base_engine.lp\".\n")
            break
        # create an object sentence from the read text
        sentence = S(text)
        # print information about the sentence
        sentence.info()
        # translate the sentence to ASP
        statements = sentence.translate(processed_blocks)
        # cycle through the blocks captured by the parser
        for item in sentence.blocks:
            # add them to the list of processed blocks
            processed_blocks.add(item)
        # if the sentence is an assertion
        if sentence.assertion:
            # cycle through the items returned by the translator
            for item in statements:
                # write the items to the ASP file
                lp_file.write("{}{}".format(item, "\n"))
                print("added to planner: {}".format(item))
        # if the sentence is a command -> add the translated rules to the final goal
        elif sentence.command:
            print("added to goal: {}".format(statements[0]))
            goal += statements[0]
        # if the sentence is a query we don't need the engine to plan, but only the facts, so
        # write the translated query and run the solver
        else:
            query = "query(yes):- {}. \nquery(no):- not query(yes).\n#show query/1".format(statements[0])
            lp_file.write("{}.{}".format(query, "\n"))
            break
    # close the instance file
    lp_file.close()
    print("running engine...\n")
    # run the solver
    command = "clingo {}".format("files/instance_{}.lp".format(now))
    print("command: {}".format(command))
    run_command(command)


# function that runs shell commands and reads the output
def run_command(command):
    out_file = open("files/out_{}.txt".format(now), "w")

    process = subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE)
    while True:
        output = process.stdout.readline()
        if output == '' and process.poll() is not None:
            break
        if output:
            print(output.strip().decode("utf-8"))
            out_file.write(output.strip().decode("utf-8"))

    rc = process.poll()
    return rc


# run main function
if __name__ == "__main__":
    main()
