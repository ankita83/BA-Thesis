class QueryNode:
    pass

class Conjunction(QueryNode):
    def __init__(self, conjuncts):
        self._conjuncts = conjuncts

    def __len__(self):
        return len(self._conjuncts)

    def __str__(self):
        conj_str = map(lambda c: str(c), self._conjuncts)
        return " & ".join(filter(None,conj_str))

class Token(QueryNode):
    def __init__(self, variable, attributes = Conjunction([])):
        self._variable = variable
        self._attributes = attributes

    def __str__(self):
        if len(self._attributes) == 0:
            return "#{}".format(self._variable)

        return "#{}:[{}]".format(self._variable, self._attributes)

class AttributeValue(QueryNode):
    def __init__(self, attribute, value):
        self._attribute = attribute
        self._value = value

    def __str__(self):
        return '{}="{}"'.format(self._attribute, self._value)

class DepRel(QueryNode):
    def __init__(self, head, dep, rel = None):
        self._head = head
        self._dep = dep
        self._rel = rel

    def __str__(self):
        if self._rel:
            return "{} >{} {}".format(self._head, self._rel, self._dep)
        else:
            if self._head:
                if self._dep:
                    return "{} > {}".format(self._head, self._dep)
                else:
                    return "{}".format(self._head)
            else:
                return "{}".format(self._dep)

example1 = Conjunction([
    DepRel(
        Token("T4", Conjunction([
            AttributeValue("word", "saw"),
            AttributeValue("pos", "VERB"),
        ])),
        AttributeValue("pos", "NOUN"),"dobj"
    ),
    DepRel(Token("T4"),AttributeValue("pos", "NOUN"), "nsubj")
])

if __name__ == "__main__":
    print(example1)
