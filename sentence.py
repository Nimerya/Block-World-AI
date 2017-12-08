import nltk

command_verbs = ["put", "move"]
grammar = r"""
                BLOCK: {<DT>?<JJ><NN><NNP>}
                OBJECT: {<DT>?<NN>}
                ASSERTION: {<BLOCK><VBZ><IN><OBJECT|BLOCK>}
                QUESTION: {<VBZ><BLOCK><IN><OBJECT|BLOCK><.>}
                COMMAND: {<VB.?><BLOCK><IN><OBJECT|BLOCK>}
           """

# question: {verb_at_start<.*>*question_mark}
# assertion: {object<VBR><RP><DT>?object}


class Sentence:

    def __init__(self, text):
        self.text = text
        self.tokens = self.tokenize()
        self.tagged = self.tag()
        self.chunks = self.chunk()
        self.question = self.is_question()
        self.assertion = self.is_assertion()
        self.command = self.is_command()

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
        if debug:
            self.draw()

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

    @staticmethod
    def help():
        nltk.help.upenn_tagset()