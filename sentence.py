import nltk

command_verbs = ["put", "move"]
grammar = r"""
                BLOCK: {<DT>?<JJ><NN><NNP>}
                OBJECT: {<DT>?<NN>}
                POS: {<VBZ><IN>}
                ASSERTION: {<BLOCK><POS><OBJECT|BLOCK>}
                QUESTION: {<VBZ><BLOCK><IN><OBJECT|BLOCK><.>}
                COMMAND: {<VB.?><BLOCK><IN><OBJECT|BLOCK>}
           """

# question: {verb_at_start<.*>*question_mark}
# assertion: {object<VBR><RP><DT>?object}


class Block:
    def __init__(self):
        self.color = None
        self.name = None


class Object:
    def __init__(self):
        self.name = None

class Sentence:

    def __init__(self, text):
        self.text = text
        self.tokens = self.tokenize()
        self.tagged = self.tag()
        self.chunks = self.chunk()
        self.question = self.is_question()
        self.assertion = self.is_assertion()
        self.command = self.is_command()
        self.blocks = self.get_blocks()
        self.objects = self.get_objects()

    def tokenize(self):
        return nltk.word_tokenize(self.text)

    def tag(self):
        return nltk.pos_tag(self.tokens)

    def extract_entities(self):
        return nltk.chunk.ne_chunk(self.tagged)

    def chunk(self):
        cp = nltk.RegexpParser(grammar)
        result = cp.parse(self.tagged)
        return result

    def draw(self):
        self.chunks.draw()

    def info(self, debug=False):
        print("\ntext: {}".format(self.text))
        print("tagged tokens: {}".format(self.tagged))
        print("chunks: {}".format(self.chunks))
        print("question: {}".format(self.question))
        print("assertion: {}".format(self.assertion))
        print("command: {}".format(self.command))
        self.print_blocks()
        self.print_objects()
        if debug:
            self.draw()

    def translate(self):
        out = []
        if self.assertion:
            for block in self.blocks:
                # TODO
                out.append("")
        elif self.command:
            # TODO
        # self.query
        else:
            # TODO
        return out

    def is_question(self):
        for subtree in self.chunks.subtrees():
            if subtree.label() == "QUESTION":
                return True
        return False

    def is_assertion(self):
        for subtree in self.chunks.subtrees():
            if subtree.label() == "ASSERTION":
                return True
        return False

    def is_command(self):
        for subtree in self.chunks.subtrees():
            if subtree.label() == "COMMAND":
                return True
        return False

    def get_blocks(self):
        blocks = []
        for subtree in self.chunks.subtrees():
            if subtree.label() == "BLOCK":
                b = Block()
                for leaf in subtree.leaves():
                    if leaf[1] == "JJ":
                        b.color = leaf[0]
                    if leaf[1] == "NNP":
                        b.name = leaf[0]
                blocks.append(b)
        return blocks

    def get_objects(self):
        objects = []
        for subtree in self.chunks.subtrees():
            if subtree.label() == "OBJECT":
                o = Object()
                for leaf in subtree.leaves():
                    if leaf[1] == "NN":
                        o.name = leaf[0]
                objects.append(o)
        return objects

    def print_blocks(self):
        for i in self.blocks:
            print("block name: {}; color: {}".format(i.name, i.color))

    def print_objects(self):
        for i in self.objects:
            print("object name: {}".format(i.name))

    @staticmethod
    def help():
        nltk.help.upenn_tagset()



