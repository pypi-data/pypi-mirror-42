from antlr4 import *


from monitors.parser.ExtRegExpLexer import ExtRegExpLexer
from monitors.parser.ExtRegExpParser import ExtRegExpParser
from monitors.parser.ExtRegExpVisitor import ExtRegExpVisitor

import intervals

class BaseMonitor:
    def union(self):
        pass

    def cascade(self, now, state, left, right, lower):
        if left and right:
            return (state & intervals.closed(self.time, intervals.inf)) | intervals.closed(self.time + lower, intervals.inf)
        elif not left and right:
            return intervals.closed(self.time + lower, intervals.inf)
        elif left and not right:
            return (state & intervals.closed(self.time, intervals.inf))
        else:
            return intervals.empty()

    def update_timed_since(self, now, state, left, right, lower, upper):
        if left and right:
            return (state & intervals.closed(self.time, intervals.inf)) | intervals.closed(self.time + lower, self.time + upper)
        elif not left and right:
            return intervals.closed(self.time + lower, self.time + upper)
        elif left and not right:
            return (state & intervals.closed(self.time, intervals.inf))
        else:
            return intervals.empty()

    def output_timed(self, state):
        return self.time in state

def monitor(pattern, **kwargs):
    "Compile an extended regular expression"

    lexer = ExtRegExpLexer(InputStream(pattern))
    stream = CommonTokenStream(lexer)
    parser = ExtRegExpParser(stream)
    tree = parser.expr()

    # lisp_tree_str = tree.toStringTree(recog=parser)
    # print(lisp_tree_str)

    # Annotate the syntax tree with positions, nullable values, and output positions 
    annotator = RegExpAnnotator()
    annotator.visit(tree)

    builder = RegExpBuilder()
    builder.build(tree)

    if 'classname' in kwargs:
        classname = kwargs['classname']
    else:
        classname = builder.name

    statements = []
    statements += ["import intervals"]
    statements += ["from monitors.mtl import BaseMonitor"]
    statements += [""]
    statements += ["class {classname}(BaseMonitor): ".format(classname=classname)]
    statements += [""]
    statements += ["\tstates = [{}]".format(", ".join([str(init) for init in builder.initialization]))]
    statements += ["\tprev_states = [{}]".format(", ".join([str(init) for init in builder.initialization]))]
    statements += [""]
    statements += ["\ttime = -1"]
    statements += [""]
    statements += ["\tdef update(self, **kwargs):"]
    statements += [""]
    statements += ["\t\tself.time = self.time + 1"]
    statements += [""]
    statements += ["\t\tself.prev_states = self.states.copy()"]
    statements += [""]
    statements += ["\t\t{}".format(statement) for statement in builder.statements]
    statements += [""]
    statements += ["\t\treturn {}".format(builder.output)]
    statements += [""]
    statements += ["\tdef output(self):"]
    statements += ["\t\treturn {}".format(builder.output)]
    
    source = '\n'.join(statements)

    if ('print_source_code' in kwargs) and kwargs['print_source_code']:
        print(source)

    code = compile(source, "<string>", "exec")

    exec(code, kwargs)

    return kwargs[classname]()


class RegExpBuilder(ExtRegExpVisitor):

    def __init__(self):
        super().__init__()
        self.name = "Monitor"
        self.statements = list()
        self.variables = set([])

    def build(self, tree, trigger_init=set([0])):

        # Start anywhere
        self.statements.append("self.states[0] = False")

        self.walk(tree, trigger_init)

        self.output = ' or '.join(['self.states[{}]'.format(i) for i in tree.output])

        # Zeroth state should be True initially
        self.initialization = [True]
        self.initialization.extend([False] * (len(self.statements) -1 ))

        return self.initialization, self.statements, self.output

    def walk(self, tree, trigger=set([0])):
        tree.trigger = trigger
        self.visit(tree)

    def visitTrue(self, ctx:ExtRegExpParser.TrueContext):
        trig_cond = " or ".join(['self.prev_states[{}]'.format(i) for i in ctx.trigger])
        self.statements.append("self.states[{}] = {};".format(ctx.position, trig_cond))

    def visitAtomic(self, ctx:ExtRegExpParser.AtomicContext):
        trig_cond = " or ".join(['self.prev_states[{}]'.format(i) for i in ctx.trigger])
        self.statements.append("self.states[{}] = {} and ({});".format(ctx.position, ctx.child.callname, trig_cond))

    def visitNegAtomic(self, ctx:ExtRegExpParser.NegAtomicContext):
        trig_cond = " or ".join(['self.prev_states[{}]'.format(i) for i in ctx.trigger])
        self.statements.append("self.states[{}] = not {} and ({});".format(ctx.position, ctx.child.callname, trig_cond))

    def visitUnion(self, ctx:ExtRegExpParser.UnionContext):
        self.walk(ctx.left, ctx.trigger)
        self.walk(ctx.right, ctx.trigger)

    # Visit a parse tree produced by ExtRegExpParser#Concat.
    def visitConcatenation(self, ctx:ExtRegExpParser.ConcatenationContext):

        self.walk(ctx.left, ctx.trigger)

        if ctx.left.nullable:
            self.walk(ctx.right, ctx.left.output | ctx.trigger)
        else:
            self.walk(ctx.right, ctx.left.output)

    # Visit a parse tree produced by ExtRegExpParser#Star.
    def visitStar(self, ctx:ExtRegExpParser.StarContext):
        self.walk(ctx.child, ctx.child.output | ctx.trigger)

    # Visit a parse tree produced by ExtRegExpParser#Grouping.
    def visitGrouping(self, ctx:ExtRegExpParser.GroupingContext):
        self.walk(ctx.child, ctx.trigger)

    # Visit a parse tree produced by ExtRegExpParser#Question.
    def visitQuestion(self, ctx:ExtRegExpParser.QuestionContext):
        self.walk(ctx.child, ctx.child.output | ctx.trigger)

    # Visit a parse tree produced by ExtRegExpParser#Plus.
    def visitPlus(self, ctx:ExtRegExpParser.PlusContext):
        self.walk(ctx.child, ctx.child.output | ctx.trigger)


class RegExpAnnotator(ExtRegExpVisitor):

    def __init__(self):
        super().__init__()
        self.num = 1
        self.variables = set()

        self.name = None
        self.statements = list()

    def visitTrue(self, ctx:ExtRegExpParser.TrueContext):

        ctx.nullable = False
        ctx.output = set([self.num])
        ctx.position = self.num
        ctx.callname = "True"
        self.num = self.num + 1 

        return self.num, ctx.nullable, ctx.output

    def visitProp(self, ctx:ExtRegExpParser.PropContext):

        ctx.nullable = False
        ctx.output = set([self.num])
        ctx.position = self.num
        ctx.callname = "kwargs['{}']".format(ctx.name.text)
        self.num = self.num + 1 

        return self.num, ctx.nullable, ctx.output

    def visitPred(self, ctx:ExtRegExpParser.PredContext):
        name = ctx.name.text
        nargs = ["kwargs['{}']".format(arg) for arg in ctx.args.getText().split(',')]

        ctx.callname = "{name}({params})".format(name=name, params=','.join(nargs))

        ctx.nullable = False
        ctx.output = set([self.num])
        ctx.position = self.num

        self.num = self.num + 1 

        return self.num, ctx.nullable, ctx.output

    def visitAtomic(self, ctx:ExtRegExpParser.AtomicContext):

        self.visit(ctx.child)

        ctx.nullable = ctx.child.nullable
        ctx.output = ctx.child.output
        ctx.position = ctx.child.position

        return self.num, ctx.nullable, ctx.output

    def visitNegAtomic(self, ctx:ExtRegExpParser.NegAtomicContext):

        self.visit(ctx.child)

        ctx.nullable = ctx.child.nullable
        ctx.output = ctx.child.output
        ctx.position = ctx.child.position

        return self.num, ctx.nullable, ctx.output

    def visitUnion(self, ctx:ExtRegExpParser.UnionContext):
        self.visit(ctx.left)
        self.visit(ctx.right)

        ctx.nullable = ctx.left.nullable or ctx.right.nullable
        ctx.output = ctx.left.output | ctx.right.output

        return self.num, ctx.nullable, ctx.output

    # Visit a parse tree produced by ExtRegExpParser#Concat.
    def visitConcatenation(self, ctx:ExtRegExpParser.ConcatenationContext):

        self.visit(ctx.left)
        self.visit(ctx.right)

        ctx.nullable = ctx.left.nullable and ctx.right.nullable
        ctx.output = ctx.left.output | ctx.right.output if ctx.right.nullable else ctx.right.output

        return self.num, ctx.nullable, ctx.output

    # Visit a parse tree produced by ExtRegExpParser#Star.
    def visitStar(self, ctx:ExtRegExpParser.StarContext):

        self.visit(ctx.child)

        ctx.nullable = True
        ctx.output = ctx.child.output

        return self.num, ctx.nullable, ctx.output

    # Visit a parse tree produced by ExtRegExpParser#Grouping.
    def visitGrouping(self, ctx:ExtRegExpParser.GroupingContext):

        self.visit(ctx.child)

        ctx.nullable = ctx.child.nullable
        ctx.output = ctx.child.output

        return self.num, ctx.nullable, ctx.output

    # Visit a parse tree produced by ExtRegExpParser#Question.
    def visitQuestion(self, ctx:ExtRegExpParser.QuestionContext):

        self.visit(ctx.child)

        ctx.nullable = True
        ctx.output = ctx.child.output

        return self.num, ctx.nullable, ctx.output

    # Visit a parse tree produced by ExtRegExpParser#Plus.
    def visitPlus(self, ctx:ExtRegExpParser.PlusContext):

        self.visit(ctx.child)

        ctx.nullable = ctx.child.nullable 
        ctx.output = ctx.child.output

        return self.num, ctx.nullable, ctx.output