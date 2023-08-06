# Generated from ExtRegExp.g4 by ANTLR 4.7.1
# encoding: utf-8
from antlr4 import *
from io import StringIO
from typing.io import TextIO
import sys

def serializedATN():
    with StringIO() as buf:
        buf.write("\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\3\23")
        buf.write(">\4\2\t\2\4\3\t\3\4\4\t\4\3\2\3\2\3\2\3\2\3\2\3\2\3\2")
        buf.write("\3\2\3\2\5\2\22\n\2\3\2\3\2\3\2\3\2\3\2\3\2\3\2\3\2\3")
        buf.write("\2\3\2\3\2\3\2\3\2\3\2\3\2\3\2\3\2\3\2\3\2\3\2\3\2\7\2")
        buf.write(")\n\2\f\2\16\2,\13\2\3\3\3\3\3\3\3\3\3\3\3\3\5\3\64\n")
        buf.write("\3\3\4\3\4\3\4\7\49\n\4\f\4\16\4<\13\4\3\4\2\3\2\5\2\4")
        buf.write("\6\2\2\2F\2\21\3\2\2\2\4\63\3\2\2\2\6\65\3\2\2\2\b\t\b")
        buf.write("\2\1\2\t\22\7\3\2\2\n\22\5\4\3\2\13\f\7\4\2\2\f\22\5\4")
        buf.write("\3\2\r\16\7\16\2\2\16\17\5\2\2\2\17\20\7\17\2\2\20\22")
        buf.write("\3\2\2\2\21\b\3\2\2\2\21\n\3\2\2\2\21\13\3\2\2\2\21\r")
        buf.write("\3\2\2\2\22*\3\2\2\2\23\24\f\6\2\2\24\25\7\13\2\2\25)")
        buf.write("\5\2\2\7\26\27\f\5\2\2\27\30\7\f\2\2\30)\5\2\2\6\31\32")
        buf.write("\f\4\2\2\32\33\7\r\2\2\33)\5\2\2\5\34\35\f\n\2\2\35)\7")
        buf.write("\5\2\2\36\37\f\t\2\2\37)\7\6\2\2 !\f\b\2\2!)\7\7\2\2\"")
        buf.write("#\f\7\2\2#$\7\b\2\2$%\7\22\2\2%&\7\t\2\2&\'\7\22\2\2\'")
        buf.write(")\7\n\2\2(\23\3\2\2\2(\26\3\2\2\2(\31\3\2\2\2(\34\3\2")
        buf.write("\2\2(\36\3\2\2\2( \3\2\2\2(\"\3\2\2\2),\3\2\2\2*(\3\2")
        buf.write("\2\2*+\3\2\2\2+\3\3\2\2\2,*\3\2\2\2-\64\7\21\2\2./\7\21")
        buf.write("\2\2/\60\7\16\2\2\60\61\5\6\4\2\61\62\7\17\2\2\62\64\3")
        buf.write("\2\2\2\63-\3\2\2\2\63.\3\2\2\2\64\5\3\2\2\2\65:\7\21\2")
        buf.write("\2\66\67\7\20\2\2\679\7\21\2\28\66\3\2\2\29<\3\2\2\2:")
        buf.write("8\3\2\2\2:;\3\2\2\2;\7\3\2\2\2<:\3\2\2\2\7\21(*\63:")
        return buf.getvalue()


class ExtRegExpParser ( Parser ):

    grammarFileName = "ExtRegExp.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "'True'", "'!'", "'*'", "'+'", "'?'", 
                     "'['", "':'", "']'", "';'", "'&'", "'|'", "'('", "')'", 
                     "','" ]

    symbolicNames = [ "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "NAME", "NUMBER", 
                      "WS" ]

    RULE_expr = 0
    RULE_atom = 1
    RULE_idlist = 2

    ruleNames =  [ "expr", "atom", "idlist" ]

    EOF = Token.EOF
    T__0=1
    T__1=2
    T__2=3
    T__3=4
    T__4=5
    T__5=6
    T__6=7
    T__7=8
    T__8=9
    T__9=10
    T__10=11
    T__11=12
    T__12=13
    T__13=14
    NAME=15
    NUMBER=16
    WS=17

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.7.1")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None



    class ExprContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return ExtRegExpParser.RULE_expr

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)


    class IntersectionContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a ExtRegExpParser.ExprContext
            super().__init__(parser)
            self.left = None # ExprContext
            self.right = None # ExprContext
            self.copyFrom(ctx)

        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(ExtRegExpParser.ExprContext)
            else:
                return self.getTypedRuleContext(ExtRegExpParser.ExprContext,i)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterIntersection" ):
                listener.enterIntersection(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitIntersection" ):
                listener.exitIntersection(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitIntersection" ):
                return visitor.visitIntersection(self)
            else:
                return visitor.visitChildren(self)


    class RestrictionContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a ExtRegExpParser.ExprContext
            super().__init__(parser)
            self.child = None # ExprContext
            self.l = None # Token
            self.u = None # Token
            self.copyFrom(ctx)

        def expr(self):
            return self.getTypedRuleContext(ExtRegExpParser.ExprContext,0)

        def NUMBER(self, i:int=None):
            if i is None:
                return self.getTokens(ExtRegExpParser.NUMBER)
            else:
                return self.getToken(ExtRegExpParser.NUMBER, i)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterRestriction" ):
                listener.enterRestriction(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitRestriction" ):
                listener.exitRestriction(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitRestriction" ):
                return visitor.visitRestriction(self)
            else:
                return visitor.visitChildren(self)


    class ConcatenationContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a ExtRegExpParser.ExprContext
            super().__init__(parser)
            self.left = None # ExprContext
            self.right = None # ExprContext
            self.copyFrom(ctx)

        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(ExtRegExpParser.ExprContext)
            else:
                return self.getTypedRuleContext(ExtRegExpParser.ExprContext,i)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterConcatenation" ):
                listener.enterConcatenation(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitConcatenation" ):
                listener.exitConcatenation(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitConcatenation" ):
                return visitor.visitConcatenation(self)
            else:
                return visitor.visitChildren(self)


    class StarContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a ExtRegExpParser.ExprContext
            super().__init__(parser)
            self.child = None # ExprContext
            self.copyFrom(ctx)

        def expr(self):
            return self.getTypedRuleContext(ExtRegExpParser.ExprContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterStar" ):
                listener.enterStar(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitStar" ):
                listener.exitStar(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitStar" ):
                return visitor.visitStar(self)
            else:
                return visitor.visitChildren(self)


    class TrueContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a ExtRegExpParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterTrue" ):
                listener.enterTrue(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitTrue" ):
                listener.exitTrue(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitTrue" ):
                return visitor.visitTrue(self)
            else:
                return visitor.visitChildren(self)


    class AtomicContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a ExtRegExpParser.ExprContext
            super().__init__(parser)
            self.child = None # AtomContext
            self.copyFrom(ctx)

        def atom(self):
            return self.getTypedRuleContext(ExtRegExpParser.AtomContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAtomic" ):
                listener.enterAtomic(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAtomic" ):
                listener.exitAtomic(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAtomic" ):
                return visitor.visitAtomic(self)
            else:
                return visitor.visitChildren(self)


    class GroupingContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a ExtRegExpParser.ExprContext
            super().__init__(parser)
            self.child = None # ExprContext
            self.copyFrom(ctx)

        def expr(self):
            return self.getTypedRuleContext(ExtRegExpParser.ExprContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterGrouping" ):
                listener.enterGrouping(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitGrouping" ):
                listener.exitGrouping(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitGrouping" ):
                return visitor.visitGrouping(self)
            else:
                return visitor.visitChildren(self)


    class QuestionContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a ExtRegExpParser.ExprContext
            super().__init__(parser)
            self.child = None # ExprContext
            self.copyFrom(ctx)

        def expr(self):
            return self.getTypedRuleContext(ExtRegExpParser.ExprContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterQuestion" ):
                listener.enterQuestion(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitQuestion" ):
                listener.exitQuestion(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitQuestion" ):
                return visitor.visitQuestion(self)
            else:
                return visitor.visitChildren(self)


    class PlusContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a ExtRegExpParser.ExprContext
            super().__init__(parser)
            self.child = None # ExprContext
            self.copyFrom(ctx)

        def expr(self):
            return self.getTypedRuleContext(ExtRegExpParser.ExprContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPlus" ):
                listener.enterPlus(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPlus" ):
                listener.exitPlus(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitPlus" ):
                return visitor.visitPlus(self)
            else:
                return visitor.visitChildren(self)


    class UnionContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a ExtRegExpParser.ExprContext
            super().__init__(parser)
            self.left = None # ExprContext
            self.right = None # ExprContext
            self.copyFrom(ctx)

        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(ExtRegExpParser.ExprContext)
            else:
                return self.getTypedRuleContext(ExtRegExpParser.ExprContext,i)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterUnion" ):
                listener.enterUnion(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitUnion" ):
                listener.exitUnion(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitUnion" ):
                return visitor.visitUnion(self)
            else:
                return visitor.visitChildren(self)


    class NegAtomicContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a ExtRegExpParser.ExprContext
            super().__init__(parser)
            self.child = None # AtomContext
            self.copyFrom(ctx)

        def atom(self):
            return self.getTypedRuleContext(ExtRegExpParser.AtomContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterNegAtomic" ):
                listener.enterNegAtomic(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitNegAtomic" ):
                listener.exitNegAtomic(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitNegAtomic" ):
                return visitor.visitNegAtomic(self)
            else:
                return visitor.visitChildren(self)



    def expr(self, _p:int=0):
        _parentctx = self._ctx
        _parentState = self.state
        localctx = ExtRegExpParser.ExprContext(self, self._ctx, _parentState)
        _prevctx = localctx
        _startState = 0
        self.enterRecursionRule(localctx, 0, self.RULE_expr, _p)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 15
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [ExtRegExpParser.T__0]:
                localctx = ExtRegExpParser.TrueContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx

                self.state = 7
                self.match(ExtRegExpParser.T__0)
                pass
            elif token in [ExtRegExpParser.NAME]:
                localctx = ExtRegExpParser.AtomicContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 8
                localctx.child = self.atom()
                pass
            elif token in [ExtRegExpParser.T__1]:
                localctx = ExtRegExpParser.NegAtomicContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 9
                self.match(ExtRegExpParser.T__1)
                self.state = 10
                localctx.child = self.atom()
                pass
            elif token in [ExtRegExpParser.T__11]:
                localctx = ExtRegExpParser.GroupingContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 11
                self.match(ExtRegExpParser.T__11)
                self.state = 12
                localctx.child = self.expr(0)
                self.state = 13
                self.match(ExtRegExpParser.T__12)
                pass
            else:
                raise NoViableAltException(self)

            self._ctx.stop = self._input.LT(-1)
            self.state = 40
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,2,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    self.state = 38
                    self._errHandler.sync(self)
                    la_ = self._interp.adaptivePredict(self._input,1,self._ctx)
                    if la_ == 1:
                        localctx = ExtRegExpParser.ConcatenationContext(self, ExtRegExpParser.ExprContext(self, _parentctx, _parentState))
                        localctx.left = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 17
                        if not self.precpred(self._ctx, 4):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 4)")
                        self.state = 18
                        self.match(ExtRegExpParser.T__8)
                        self.state = 19
                        localctx.right = self.expr(5)
                        pass

                    elif la_ == 2:
                        localctx = ExtRegExpParser.IntersectionContext(self, ExtRegExpParser.ExprContext(self, _parentctx, _parentState))
                        localctx.left = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 20
                        if not self.precpred(self._ctx, 3):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 3)")
                        self.state = 21
                        self.match(ExtRegExpParser.T__9)
                        self.state = 22
                        localctx.right = self.expr(4)
                        pass

                    elif la_ == 3:
                        localctx = ExtRegExpParser.UnionContext(self, ExtRegExpParser.ExprContext(self, _parentctx, _parentState))
                        localctx.left = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 23
                        if not self.precpred(self._ctx, 2):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 2)")
                        self.state = 24
                        self.match(ExtRegExpParser.T__10)
                        self.state = 25
                        localctx.right = self.expr(3)
                        pass

                    elif la_ == 4:
                        localctx = ExtRegExpParser.StarContext(self, ExtRegExpParser.ExprContext(self, _parentctx, _parentState))
                        localctx.child = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 26
                        if not self.precpred(self._ctx, 8):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 8)")
                        self.state = 27
                        self.match(ExtRegExpParser.T__2)
                        pass

                    elif la_ == 5:
                        localctx = ExtRegExpParser.PlusContext(self, ExtRegExpParser.ExprContext(self, _parentctx, _parentState))
                        localctx.child = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 28
                        if not self.precpred(self._ctx, 7):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 7)")
                        self.state = 29
                        self.match(ExtRegExpParser.T__3)
                        pass

                    elif la_ == 6:
                        localctx = ExtRegExpParser.QuestionContext(self, ExtRegExpParser.ExprContext(self, _parentctx, _parentState))
                        localctx.child = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 30
                        if not self.precpred(self._ctx, 6):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 6)")
                        self.state = 31
                        self.match(ExtRegExpParser.T__4)
                        pass

                    elif la_ == 7:
                        localctx = ExtRegExpParser.RestrictionContext(self, ExtRegExpParser.ExprContext(self, _parentctx, _parentState))
                        localctx.child = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 32
                        if not self.precpred(self._ctx, 5):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 5)")
                        self.state = 33
                        self.match(ExtRegExpParser.T__5)
                        self.state = 34
                        localctx.l = self.match(ExtRegExpParser.NUMBER)
                        self.state = 35
                        self.match(ExtRegExpParser.T__6)
                        self.state = 36
                        localctx.u = self.match(ExtRegExpParser.NUMBER)
                        self.state = 37
                        self.match(ExtRegExpParser.T__7)
                        pass

             
                self.state = 42
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,2,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.unrollRecursionContexts(_parentctx)
        return localctx

    class AtomContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return ExtRegExpParser.RULE_atom

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)



    class PropContext(AtomContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a ExtRegExpParser.AtomContext
            super().__init__(parser)
            self.name = None # Token
            self.copyFrom(ctx)

        def NAME(self):
            return self.getToken(ExtRegExpParser.NAME, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterProp" ):
                listener.enterProp(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitProp" ):
                listener.exitProp(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitProp" ):
                return visitor.visitProp(self)
            else:
                return visitor.visitChildren(self)


    class PredContext(AtomContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a ExtRegExpParser.AtomContext
            super().__init__(parser)
            self.name = None # Token
            self.args = None # IdlistContext
            self.copyFrom(ctx)

        def NAME(self):
            return self.getToken(ExtRegExpParser.NAME, 0)
        def idlist(self):
            return self.getTypedRuleContext(ExtRegExpParser.IdlistContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPred" ):
                listener.enterPred(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPred" ):
                listener.exitPred(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitPred" ):
                return visitor.visitPred(self)
            else:
                return visitor.visitChildren(self)



    def atom(self):

        localctx = ExtRegExpParser.AtomContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_atom)
        try:
            self.state = 49
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,3,self._ctx)
            if la_ == 1:
                localctx = ExtRegExpParser.PropContext(self, localctx)
                self.enterOuterAlt(localctx, 1)
                self.state = 43
                localctx.name = self.match(ExtRegExpParser.NAME)
                pass

            elif la_ == 2:
                localctx = ExtRegExpParser.PredContext(self, localctx)
                self.enterOuterAlt(localctx, 2)
                self.state = 44
                localctx.name = self.match(ExtRegExpParser.NAME)
                self.state = 45
                self.match(ExtRegExpParser.T__11)
                self.state = 46
                localctx.args = self.idlist()
                self.state = 47
                self.match(ExtRegExpParser.T__12)
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class IdlistContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser
            self.param = None # Token

        def NAME(self, i:int=None):
            if i is None:
                return self.getTokens(ExtRegExpParser.NAME)
            else:
                return self.getToken(ExtRegExpParser.NAME, i)

        def getRuleIndex(self):
            return ExtRegExpParser.RULE_idlist

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterIdlist" ):
                listener.enterIdlist(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitIdlist" ):
                listener.exitIdlist(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitIdlist" ):
                return visitor.visitIdlist(self)
            else:
                return visitor.visitChildren(self)




    def idlist(self):

        localctx = ExtRegExpParser.IdlistContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_idlist)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 51
            localctx.param = self.match(ExtRegExpParser.NAME)
            self.state = 56
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==ExtRegExpParser.T__13:
                self.state = 52
                self.match(ExtRegExpParser.T__13)
                self.state = 53
                localctx.param = self.match(ExtRegExpParser.NAME)
                self.state = 58
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx



    def sempred(self, localctx:RuleContext, ruleIndex:int, predIndex:int):
        if self._predicates == None:
            self._predicates = dict()
        self._predicates[0] = self.expr_sempred
        pred = self._predicates.get(ruleIndex, None)
        if pred is None:
            raise Exception("No predicate with index:" + str(ruleIndex))
        else:
            return pred(localctx, predIndex)

    def expr_sempred(self, localctx:ExprContext, predIndex:int):
            if predIndex == 0:
                return self.precpred(self._ctx, 4)
         

            if predIndex == 1:
                return self.precpred(self._ctx, 3)
         

            if predIndex == 2:
                return self.precpred(self._ctx, 2)
         

            if predIndex == 3:
                return self.precpred(self._ctx, 8)
         

            if predIndex == 4:
                return self.precpred(self._ctx, 7)
         

            if predIndex == 5:
                return self.precpred(self._ctx, 6)
         

            if predIndex == 6:
                return self.precpred(self._ctx, 5)
         




