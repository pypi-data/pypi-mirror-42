# Generated from ExtRegExp.g4 by ANTLR 4.7.1
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .ExtRegExpParser import ExtRegExpParser
else:
    from ExtRegExpParser import ExtRegExpParser

# This class defines a complete generic visitor for a parse tree produced by ExtRegExpParser.

class ExtRegExpVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by ExtRegExpParser#Intersection.
    def visitIntersection(self, ctx:ExtRegExpParser.IntersectionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ExtRegExpParser#Restriction.
    def visitRestriction(self, ctx:ExtRegExpParser.RestrictionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ExtRegExpParser#Concatenation.
    def visitConcatenation(self, ctx:ExtRegExpParser.ConcatenationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ExtRegExpParser#Star.
    def visitStar(self, ctx:ExtRegExpParser.StarContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ExtRegExpParser#True.
    def visitTrue(self, ctx:ExtRegExpParser.TrueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ExtRegExpParser#Atomic.
    def visitAtomic(self, ctx:ExtRegExpParser.AtomicContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ExtRegExpParser#Grouping.
    def visitGrouping(self, ctx:ExtRegExpParser.GroupingContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ExtRegExpParser#Question.
    def visitQuestion(self, ctx:ExtRegExpParser.QuestionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ExtRegExpParser#Plus.
    def visitPlus(self, ctx:ExtRegExpParser.PlusContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ExtRegExpParser#Union.
    def visitUnion(self, ctx:ExtRegExpParser.UnionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ExtRegExpParser#NegAtomic.
    def visitNegAtomic(self, ctx:ExtRegExpParser.NegAtomicContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ExtRegExpParser#Prop.
    def visitProp(self, ctx:ExtRegExpParser.PropContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ExtRegExpParser#Pred.
    def visitPred(self, ctx:ExtRegExpParser.PredContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ExtRegExpParser#idlist.
    def visitIdlist(self, ctx:ExtRegExpParser.IdlistContext):
        return self.visitChildren(ctx)



del ExtRegExpParser