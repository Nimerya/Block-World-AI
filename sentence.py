import nltk


grammar = r"""
                LENGTH: {<IN><NN><CD>}
                BLOCK: {<DT><JJ><NN><NN.?><LENGTH>?}
                POS: {<VBZ><IN>}
                OBJECT: {<DT><NN>}
                ASSERTION: {<BLOCK><POS><BLOCK|OBJECT>}
                QUERY: {<VBZ><BLOCK><IN><BLOCK|OBJECT><.>}
                COMMAND: {<VB.?><BLOCK><IN><BLOCK|OBJECT>}
           """

# class that represents the blocks


class Block:
    # constructor with the default values
    def __init__(self):
        self.color = "black"
        self.name = None
        self.length = 1

    # redefinition of the equal, not equal, has methods to better operate with sets
    def __eq__(self, other):
        return self.name == other.name

    def __ne__(self, other):
        return self.name != other.name

    def __hash__(self):
        return hash(str(self.name))


class Object:
    def __init__(self):
        self.name = None


class Sentence:

    def __init__(self, text):
        self.text = text
        self.tokens = self.tokenize()
        self.tagged = self.tag()
        self.chunks = self.chunk()
        self.query = self.is_query()
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
        print("query: {}".format(self.query))
        print("assertion: {}".format(self.assertion))
        print("command: {}".format(self.command))
        # self.print_blocks()
        # self.print_objects()
        if debug:
            self.draw()

    def translate(self, processed_blocks):
        out = []
        if self.assertion:
            for block in self.blocks:
                if block not in processed_blocks:
                    block_fact = "block({}, {}, {}).".format(block.name, block.color, block.length).lower()
                    out.append(block_fact)
            if len(self.blocks) == 2:
                positional_fact = "on({}, {}, 0).".format(self.blocks[0].name, self.blocks[1].name).lower()
            else:
                positional_fact = "on({}, {}, 0).".format(self.blocks[0].name, self.objects[0].name).lower()
            out.append(positional_fact)
        elif self.command:
            if len(self.blocks) == 2:
                goal = "on({}, {}, T),".format(self.blocks[0].name.lower(), self.blocks[1].name.lower())
            else:
                goal = "on({}, {}, T),".format(self.blocks[0].name.lower(), self.objects[0].name.lower())
            out.append(goal)
            return out
        # self.query
        else:
            if len(self.blocks) == 2:
                query = "on({}, {}, _)".format(self.blocks[0].name, self.blocks[1].name).lower()
            else:
                query = "on({}, {}, _)".format(self.blocks[0].name, self.objects[0].name).lower()
            out.append(query)
            return out
        return out

    def is_query(self):
        for subtree in self.chunks.subtrees():
            if subtree.label() == "QUERY":
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
                    if leaf[1] == "CD":
                        b.length = leaf[0]
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
            print("block name: {}; color: {}; length: {}".format(i.name, i.color, i.length))

    def print_objects(self):
        for i in self.objects:
            print("object name: {}".format(i.name))

    @staticmethod
    def help():
        nltk.help.upenn_tagset()



