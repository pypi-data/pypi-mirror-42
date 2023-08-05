# Generated from /Users/aleksandrrudakov/dev/zmei/generator/zmei_generator/parser/gen/grammar/ZmeiLangParser.g4 by ANTLR 4.7.2
# encoding: utf-8
from antlr4 import *
from io import StringIO
from typing.io import TextIO
import sys


def serializedATN():
    with StringIO() as buf:
        buf.write("\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\3\u00a1")
        buf.write("\u09c6\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7\t\7")
        buf.write("\4\b\t\b\4\t\t\t\4\n\t\n\4\13\t\13\4\f\t\f\4\r\t\r\4\16")
        buf.write("\t\16\4\17\t\17\4\20\t\20\4\21\t\21\4\22\t\22\4\23\t\23")
        buf.write("\4\24\t\24\4\25\t\25\4\26\t\26\4\27\t\27\4\30\t\30\4\31")
        buf.write("\t\31\4\32\t\32\4\33\t\33\4\34\t\34\4\35\t\35\4\36\t\36")
        buf.write("\4\37\t\37\4 \t \4!\t!\4\"\t\"\4#\t#\4$\t$\4%\t%\4&\t")
        buf.write("&\4\'\t\'\4(\t(\4)\t)\4*\t*\4+\t+\4,\t,\4-\t-\4.\t.\4")
        buf.write("/\t/\4\60\t\60\4\61\t\61\4\62\t\62\4\63\t\63\4\64\t\64")
        buf.write("\4\65\t\65\4\66\t\66\4\67\t\67\48\t8\49\t9\4:\t:\4;\t")
        buf.write(";\4<\t<\4=\t=\4>\t>\4?\t?\4@\t@\4A\tA\4B\tB\4C\tC\4D\t")
        buf.write("D\4E\tE\4F\tF\4G\tG\4H\tH\4I\tI\4J\tJ\4K\tK\4L\tL\4M\t")
        buf.write("M\4N\tN\4O\tO\4P\tP\4Q\tQ\4R\tR\4S\tS\4T\tT\4U\tU\4V\t")
        buf.write("V\4W\tW\4X\tX\4Y\tY\4Z\tZ\4[\t[\4\\\t\\\4]\t]\4^\t^\4")
        buf.write("_\t_\4`\t`\4a\ta\4b\tb\4c\tc\4d\td\4e\te\4f\tf\4g\tg\4")
        buf.write("h\th\4i\ti\4j\tj\4k\tk\4l\tl\4m\tm\4n\tn\4o\to\4p\tp\4")
        buf.write("q\tq\4r\tr\4s\ts\4t\tt\4u\tu\4v\tv\4w\tw\4x\tx\4y\ty\4")
        buf.write("z\tz\4{\t{\4|\t|\4}\t}\4~\t~\4\177\t\177\4\u0080\t\u0080")
        buf.write("\4\u0081\t\u0081\4\u0082\t\u0082\4\u0083\t\u0083\4\u0084")
        buf.write("\t\u0084\4\u0085\t\u0085\4\u0086\t\u0086\4\u0087\t\u0087")
        buf.write("\4\u0088\t\u0088\4\u0089\t\u0089\4\u008a\t\u008a\4\u008b")
        buf.write("\t\u008b\4\u008c\t\u008c\4\u008d\t\u008d\4\u008e\t\u008e")
        buf.write("\4\u008f\t\u008f\4\u0090\t\u0090\4\u0091\t\u0091\4\u0092")
        buf.write("\t\u0092\4\u0093\t\u0093\4\u0094\t\u0094\4\u0095\t\u0095")
        buf.write("\4\u0096\t\u0096\4\u0097\t\u0097\4\u0098\t\u0098\4\u0099")
        buf.write("\t\u0099\4\u009a\t\u009a\4\u009b\t\u009b\4\u009c\t\u009c")
        buf.write("\4\u009d\t\u009d\4\u009e\t\u009e\4\u009f\t\u009f\4\u00a0")
        buf.write("\t\u00a0\4\u00a1\t\u00a1\4\u00a2\t\u00a2\4\u00a3\t\u00a3")
        buf.write("\4\u00a4\t\u00a4\4\u00a5\t\u00a5\4\u00a6\t\u00a6\4\u00a7")
        buf.write("\t\u00a7\4\u00a8\t\u00a8\4\u00a9\t\u00a9\4\u00aa\t\u00aa")
        buf.write("\4\u00ab\t\u00ab\4\u00ac\t\u00ac\4\u00ad\t\u00ad\4\u00ae")
        buf.write("\t\u00ae\4\u00af\t\u00af\4\u00b0\t\u00b0\4\u00b1\t\u00b1")
        buf.write("\4\u00b2\t\u00b2\4\u00b3\t\u00b3\4\u00b4\t\u00b4\4\u00b5")
        buf.write("\t\u00b5\4\u00b6\t\u00b6\4\u00b7\t\u00b7\4\u00b8\t\u00b8")
        buf.write("\4\u00b9\t\u00b9\4\u00ba\t\u00ba\4\u00bb\t\u00bb\4\u00bc")
        buf.write("\t\u00bc\4\u00bd\t\u00bd\4\u00be\t\u00be\4\u00bf\t\u00bf")
        buf.write("\4\u00c0\t\u00c0\4\u00c1\t\u00c1\4\u00c2\t\u00c2\4\u00c3")
        buf.write("\t\u00c3\4\u00c4\t\u00c4\4\u00c5\t\u00c5\4\u00c6\t\u00c6")
        buf.write("\4\u00c7\t\u00c7\4\u00c8\t\u00c8\4\u00c9\t\u00c9\4\u00ca")
        buf.write("\t\u00ca\4\u00cb\t\u00cb\4\u00cc\t\u00cc\4\u00cd\t\u00cd")
        buf.write("\4\u00ce\t\u00ce\4\u00cf\t\u00cf\4\u00d0\t\u00d0\4\u00d1")
        buf.write("\t\u00d1\4\u00d2\t\u00d2\4\u00d3\t\u00d3\4\u00d4\t\u00d4")
        buf.write("\4\u00d5\t\u00d5\4\u00d6\t\u00d6\4\u00d7\t\u00d7\4\u00d8")
        buf.write("\t\u00d8\4\u00d9\t\u00d9\4\u00da\t\u00da\4\u00db\t\u00db")
        buf.write("\4\u00dc\t\u00dc\4\u00dd\t\u00dd\4\u00de\t\u00de\4\u00df")
        buf.write("\t\u00df\4\u00e0\t\u00e0\4\u00e1\t\u00e1\4\u00e2\t\u00e2")
        buf.write("\4\u00e3\t\u00e3\4\u00e4\t\u00e4\4\u00e5\t\u00e5\4\u00e6")
        buf.write("\t\u00e6\4\u00e7\t\u00e7\4\u00e8\t\u00e8\4\u00e9\t\u00e9")
        buf.write("\4\u00ea\t\u00ea\4\u00eb\t\u00eb\4\u00ec\t\u00ec\4\u00ed")
        buf.write("\t\u00ed\4\u00ee\t\u00ee\4\u00ef\t\u00ef\4\u00f0\t\u00f0")
        buf.write("\4\u00f1\t\u00f1\4\u00f2\t\u00f2\4\u00f3\t\u00f3\4\u00f4")
        buf.write("\t\u00f4\4\u00f5\t\u00f5\4\u00f6\t\u00f6\4\u00f7\t\u00f7")
        buf.write("\4\u00f8\t\u00f8\4\u00f9\t\u00f9\4\u00fa\t\u00fa\4\u00fb")
        buf.write("\t\u00fb\4\u00fc\t\u00fc\4\u00fd\t\u00fd\4\u00fe\t\u00fe")
        buf.write("\4\u00ff\t\u00ff\4\u0100\t\u0100\4\u0101\t\u0101\4\u0102")
        buf.write("\t\u0102\4\u0103\t\u0103\4\u0104\t\u0104\4\u0105\t\u0105")
        buf.write("\4\u0106\t\u0106\4\u0107\t\u0107\4\u0108\t\u0108\4\u0109")
        buf.write("\t\u0109\4\u010a\t\u010a\4\u010b\t\u010b\4\u010c\t\u010c")
        buf.write("\4\u010d\t\u010d\4\u010e\t\u010e\4\u010f\t\u010f\4\u0110")
        buf.write("\t\u0110\4\u0111\t\u0111\4\u0112\t\u0112\4\u0113\t\u0113")
        buf.write("\4\u0114\t\u0114\4\u0115\t\u0115\4\u0116\t\u0116\4\u0117")
        buf.write("\t\u0117\3\2\7\2\u0230\n\2\f\2\16\2\u0233\13\2\3\2\7\2")
        buf.write("\u0236\n\2\f\2\16\2\u0239\13\2\3\2\7\2\u023c\n\2\f\2\16")
        buf.write("\2\u023f\13\2\3\2\5\2\u0242\n\2\3\2\6\2\u0245\n\2\r\2")
        buf.write("\16\2\u0246\5\2\u0249\n\2\3\2\7\2\u024c\n\2\f\2\16\2\u024f")
        buf.write("\13\2\3\2\5\2\u0252\n\2\3\2\6\2\u0255\n\2\r\2\16\2\u0256")
        buf.write("\5\2\u0259\n\2\3\2\7\2\u025c\n\2\f\2\16\2\u025f\13\2\3")
        buf.write("\2\3\2\3\3\6\3\u0264\n\3\r\3\16\3\u0265\3\4\6\4\u0269")
        buf.write("\n\4\r\4\16\4\u026a\3\5\3\5\3\6\3\6\3\7\3\7\5\7\u0273")
        buf.write("\n\7\3\7\3\7\3\7\6\7\u0278\n\7\r\7\16\7\u0279\3\b\5\b")
        buf.write("\u027d\n\b\3\b\3\b\3\t\3\t\3\t\7\t\u0284\n\t\f\t\16\t")
        buf.write("\u0287\13\t\3\n\3\n\3\n\5\n\u028c\n\n\3\n\5\n\u028f\n")
        buf.write("\n\3\13\3\13\3\f\3\f\3\r\3\r\3\16\3\16\3\17\3\17\3\17")
        buf.write("\7\17\u029c\n\17\f\17\16\17\u029f\13\17\3\20\3\20\3\20")
        buf.write("\3\20\5\20\u02a5\n\20\3\20\3\20\3\21\5\21\u02aa\n\21\3")
        buf.write("\21\3\21\3\21\3\21\7\21\u02b0\n\21\f\21\16\21\u02b3\13")
        buf.write("\21\3\21\3\21\3\21\5\21\u02b8\n\21\3\21\7\21\u02bb\n\21")
        buf.write("\f\21\16\21\u02be\13\21\5\21\u02c0\n\21\3\22\5\22\u02c3")
        buf.write("\n\22\3\22\3\22\5\22\u02c7\n\22\3\23\3\23\3\23\3\23\3")
        buf.write("\24\3\24\5\24\u02cf\n\24\3\25\3\25\3\25\3\25\3\26\3\26")
        buf.write("\3\27\3\27\3\27\3\27\3\27\3\27\3\27\3\27\3\27\3\27\5\27")
        buf.write("\u02e1\n\27\3\30\3\30\3\30\3\30\3\30\5\30\u02e8\n\30\3")
        buf.write("\31\3\31\3\32\3\32\3\32\5\32\u02ef\n\32\3\33\3\33\3\33")
        buf.write("\5\33\u02f4\n\33\3\34\3\34\3\34\5\34\u02f9\n\34\3\35\3")
        buf.write("\35\3\35\5\35\u02fe\n\35\3\36\3\36\3\36\7\36\u0303\n\36")
        buf.write("\f\36\16\36\u0306\13\36\3\36\5\36\u0309\n\36\3\36\7\36")
        buf.write("\u030c\n\36\f\36\16\36\u030f\13\36\3\36\6\36\u0312\n\36")
        buf.write("\r\36\16\36\u0313\3\36\7\36\u0317\n\36\f\36\16\36\u031a")
        buf.write("\13\36\3\36\3\36\3\37\3\37\3 \3 \3 \7 \u0323\n \f \16")
        buf.write(" \u0326\13 \3 \5 \u0329\n \3 \7 \u032c\n \f \16 \u032f")
        buf.write("\13 \3 \3 \5 \u0333\n \7 \u0335\n \f \16 \u0338\13 \3")
        buf.write(" \7 \u033b\n \f \16 \u033e\13 \3 \3 \3!\3!\3!\7!\u0345")
        buf.write("\n!\f!\16!\u0348\13!\3!\3!\3!\7!\u034d\n!\f!\16!\u0350")
        buf.write("\13!\5!\u0352\n!\3!\7!\u0355\n!\f!\16!\u0358\13!\3!\3")
        buf.write("!\3\"\7\"\u035d\n\"\f\"\16\"\u0360\13\"\3\"\3\"\3\"\7")
        buf.write("\"\u0365\n\"\f\"\16\"\u0368\13\"\3\"\3\"\5\"\u036c\n\"")
        buf.write("\7\"\u036e\n\"\f\"\16\"\u0371\13\"\3\"\7\"\u0374\n\"\f")
        buf.write("\"\16\"\u0377\13\"\3\"\5\"\u037a\n\"\3#\3#\3$\3$\7$\u0380")
        buf.write("\n$\f$\16$\u0383\13$\3$\3$\7$\u0387\n$\f$\16$\u038a\13")
        buf.write("$\3$\3$\3$\7$\u038f\n$\f$\16$\u0392\13$\3$\3$\3$\7$\u0397")
        buf.write("\n$\f$\16$\u039a\13$\3$\3$\5$\u039e\n$\7$\u03a0\n$\f$")
        buf.write("\16$\u03a3\13$\5$\u03a5\n$\3$\7$\u03a8\n$\f$\16$\u03ab")
        buf.write("\13$\3$\3$\7$\u03af\n$\f$\16$\u03b2\13$\3%\3%\3%\3&\3")
        buf.write("&\3&\3&\6&\u03bb\n&\r&\16&\u03bc\3\'\3\'\3\'\3\'\6\'\u03c3")
        buf.write("\n\'\r\'\16\'\u03c4\3(\3(\3(\3(\6(\u03cb\n(\r(\16(\u03cc")
        buf.write("\3)\7)\u03d0\n)\f)\16)\u03d3\13)\3)\3)\3)\3)\3*\3*\3+")
        buf.write("\3+\3+\3+\5+\u03df\n+\3,\3,\3,\3,\3-\3-\3.\3.\3.\3.\3")
        buf.write(".\3.\3.\5.\u03ee\n.\3.\3.\3/\3/\3\60\3\60\3\60\5\60\u03f7")
        buf.write("\n\60\3\61\3\61\3\61\3\61\3\61\3\62\3\62\3\62\7\62\u0401")
        buf.write("\n\62\f\62\16\62\u0404\13\62\3\63\3\63\5\63\u0408\n\63")
        buf.write("\3\63\7\63\u040b\n\63\f\63\16\63\u040e\13\63\3\63\7\63")
        buf.write("\u0411\n\63\f\63\16\63\u0414\13\63\3\63\7\63\u0417\n\63")
        buf.write("\f\63\16\63\u041a\13\63\3\63\7\63\u041d\n\63\f\63\16\63")
        buf.write("\u0420\13\63\3\63\7\63\u0423\n\63\f\63\16\63\u0426\13")
        buf.write("\63\3\64\3\64\3\64\6\64\u042b\n\64\r\64\16\64\u042c\3")
        buf.write("\64\5\64\u0430\n\64\3\65\3\65\5\65\u0434\n\65\3\65\3\65")
        buf.write("\5\65\u0438\n\65\3\65\3\65\3\65\3\66\3\66\3\66\3\66\6")
        buf.write("\66\u0441\n\66\r\66\16\66\u0442\3\67\3\67\3\67\3\67\5")
        buf.write("\67\u0449\n\67\38\38\38\58\u044e\n8\39\39\39\39\39\59")
        buf.write("\u0455\n9\3:\3:\3;\7;\u045a\n;\f;\16;\u045d\13;\3;\3;")
        buf.write("\5;\u0461\n;\3;\5;\u0464\n;\3;\5;\u0467\n;\3;\6;\u046a")
        buf.write("\n;\r;\16;\u046b\3;\5;\u046f\n;\3<\3<\5<\u0473\n<\3<\3")
        buf.write("<\3<\5<\u0478\n<\3<\3<\3<\5<\u047d\n<\3=\3=\3>\5>\u0482")
        buf.write("\n>\3>\3>\3?\3?\3?\3@\3@\3A\3A\3A\3B\3B\3C\3C\3D\6D\u0493")
        buf.write("\nD\rD\16D\u0494\3D\3D\5D\u0499\nD\3E\3E\3E\3F\3F\3F\3")
        buf.write("G\3G\3H\3H\3I\3I\3I\3I\3I\3I\3I\3I\3I\3I\3I\3I\3I\3I\3")
        buf.write("I\3I\3I\3I\5I\u04b7\nI\3J\3J\3K\3K\3L\3L\3M\3M\3N\3N\3")
        buf.write("O\3O\3P\3P\3Q\3Q\3R\3R\3S\3S\3T\3T\3U\3U\3V\3V\3V\3V\3")
        buf.write("V\5V\u04d6\nV\3V\3V\5V\u04da\nV\3W\3W\3X\3X\3X\3X\3X\7")
        buf.write("X\u04e3\nX\fX\16X\u04e6\13X\3Y\5Y\u04e9\nY\3Y\3Y\3Z\3")
        buf.write("Z\3Z\5Z\u04f0\nZ\3[\3[\3[\3\\\3\\\3\\\3\\\3\\\5\\\u04fa")
        buf.write("\n\\\3]\3]\3]\3]\3]\7]\u0501\n]\f]\16]\u0504\13]\3^\5")
        buf.write("^\u0507\n^\3^\3^\3_\3_\3_\5_\u050e\n_\3`\3`\3`\3a\3a\3")
        buf.write("a\3a\3a\3b\3b\3b\7b\u051b\nb\fb\16b\u051e\13b\3c\3c\3")
        buf.write("d\3d\3d\3d\3d\5d\u0527\nd\3e\3e\3f\3f\3f\3f\3f\5f\u0530")
        buf.write("\nf\3g\3g\3h\3h\3h\7h\u0537\nh\fh\16h\u053a\13h\3i\3i")
        buf.write("\3i\3i\3j\3j\3k\3k\3k\3l\7l\u0546\nl\fl\16l\u0549\13l")
        buf.write("\3m\3m\3m\3n\3n\3n\5n\u0551\nn\3n\3n\5n\u0555\nn\3n\5")
        buf.write("n\u0558\nn\3n\3n\3o\3o\3p\3p\3q\3q\3r\3r\3s\3s\3s\3s\3")
        buf.write("t\3t\3t\3t\3t\3t\3t\3t\3t\3t\3t\3t\3t\3t\3t\5t\u0577\n")
        buf.write("t\3u\3u\3u\3u\3u\3u\3u\3u\3u\3u\3u\3u\3u\3u\7u\u0587\n")
        buf.write("u\fu\16u\u058a\13u\3u\7u\u058d\nu\fu\16u\u0590\13u\3u")
        buf.write("\5u\u0593\nu\3u\7u\u0596\nu\fu\16u\u0599\13u\3v\3v\3v")
        buf.write("\7v\u059e\nv\fv\16v\u05a1\13v\3v\3v\3v\7v\u05a6\nv\fv")
        buf.write("\16v\u05a9\13v\3v\7v\u05ac\nv\fv\16v\u05af\13v\3w\3w\3")
        buf.write("w\3w\3w\7w\u05b6\nw\fw\16w\u05b9\13w\3x\3x\3y\3y\3z\3")
        buf.write("z\3z\3z\3z\7z\u05c4\nz\fz\16z\u05c7\13z\3{\3{\3{\3{\3")
        buf.write("{\3{\3{\7{\u05d0\n{\f{\16{\u05d3\13{\3{\5{\u05d6\n{\3")
        buf.write("|\3|\3}\3}\3}\3}\3~\3~\3\177\3\177\3\177\3\177\3\u0080")
        buf.write("\3\u0080\3\u0080\3\u0080\3\u0081\3\u0081\3\u0081\3\u0081")
        buf.write("\3\u0081\7\u0081\u05ed\n\u0081\f\u0081\16\u0081\u05f0")
        buf.write("\13\u0081\3\u0082\3\u0082\5\u0082\u05f4\n\u0082\3\u0082")
        buf.write("\3\u0082\3\u0082\3\u0082\3\u0083\3\u0083\3\u0084\3\u0084")
        buf.write("\3\u0085\3\u0085\3\u0085\3\u0085\7\u0085\u0602\n\u0085")
        buf.write("\f\u0085\16\u0085\u0605\13\u0085\3\u0086\3\u0086\3\u0086")
        buf.write("\3\u0086\7\u0086\u060b\n\u0086\f\u0086\16\u0086\u060e")
        buf.write("\13\u0086\3\u0087\3\u0087\3\u0087\3\u0087\7\u0087\u0614")
        buf.write("\n\u0087\f\u0087\16\u0087\u0617\13\u0087\3\u0088\3\u0088")
        buf.write("\3\u0088\3\u0088\7\u0088\u061d\n\u0088\f\u0088\16\u0088")
        buf.write("\u0620\13\u0088\3\u0089\3\u0089\3\u0089\3\u0089\7\u0089")
        buf.write("\u0626\n\u0089\f\u0089\16\u0089\u0629\13\u0089\3\u008a")
        buf.write("\3\u008a\3\u008a\3\u008a\7\u008a\u062f\n\u008a\f\u008a")
        buf.write("\16\u008a\u0632\13\u008a\3\u008b\3\u008b\3\u008b\3\u008b")
        buf.write("\3\u008b\3\u008b\7\u008b\u063a\n\u008b\f\u008b\16\u008b")
        buf.write("\u063d\13\u008b\5\u008b\u063f\n\u008b\3\u008b\3\u008b")
        buf.write("\5\u008b\u0643\n\u008b\3\u008c\3\u008c\3\u008d\3\u008d")
        buf.write("\3\u008e\3\u008e\3\u008e\5\u008e\u064c\n\u008e\3\u008e")
        buf.write("\3\u008e\3\u008e\3\u008e\5\u008e\u0652\n\u008e\3\u008f")
        buf.write("\3\u008f\3\u008f\3\u008f\7\u008f\u0658\n\u008f\f\u008f")
        buf.write("\16\u008f\u065b\13\u008f\3\u0090\3\u0090\3\u0090\3\u0090")
        buf.write("\3\u0090\3\u0090\3\u0090\3\u0090\3\u0090\3\u0090\3\u0090")
        buf.write("\3\u0090\7\u0090\u0669\n\u0090\f\u0090\16\u0090\u066c")
        buf.write("\13\u0090\3\u0091\3\u0091\3\u0092\3\u0092\3\u0092\3\u0092")
        buf.write("\7\u0092\u0674\n\u0092\f\u0092\16\u0092\u0677\13\u0092")
        buf.write("\3\u0093\3\u0093\3\u0093\7\u0093\u067c\n\u0093\f\u0093")
        buf.write("\16\u0093\u067f\13\u0093\3\u0094\3\u0094\5\u0094\u0683")
        buf.write("\n\u0094\3\u0094\3\u0094\7\u0094\u0687\n\u0094\f\u0094")
        buf.write("\16\u0094\u068a\13\u0094\3\u0095\3\u0095\5\u0095\u068e")
        buf.write("\n\u0095\3\u0095\3\u0095\7\u0095\u0692\n\u0095\f\u0095")
        buf.write("\16\u0095\u0695\13\u0095\3\u0096\3\u0096\5\u0096\u0699")
        buf.write("\n\u0096\3\u0096\3\u0096\7\u0096\u069d\n\u0096\f\u0096")
        buf.write("\16\u0096\u06a0\13\u0096\3\u0097\3\u0097\3\u0097\3\u0097")
        buf.write("\7\u0097\u06a6\n\u0097\f\u0097\16\u0097\u06a9\13\u0097")
        buf.write("\3\u0098\3\u0098\3\u0098\3\u0098\7\u0098\u06af\n\u0098")
        buf.write("\f\u0098\16\u0098\u06b2\13\u0098\3\u0099\3\u0099\3\u0099")
        buf.write("\3\u0099\5\u0099\u06b8\n\u0099\3\u0099\7\u0099\u06bb\n")
        buf.write("\u0099\f\u0099\16\u0099\u06be\13\u0099\3\u009a\3\u009a")
        buf.write("\3\u009b\3\u009b\3\u009b\3\u009b\3\u009b\7\u009b\u06c7")
        buf.write("\n\u009b\f\u009b\16\u009b\u06ca\13\u009b\3\u009b\3\u009b")
        buf.write("\3\u009c\3\u009c\3\u009c\3\u009c\5\u009c\u06d2\n\u009c")
        buf.write("\3\u009d\3\u009d\3\u009e\3\u009e\3\u009f\3\u009f\3\u00a0")
        buf.write("\3\u00a0\3\u00a0\3\u00a0\7\u00a0\u06de\n\u00a0\f\u00a0")
        buf.write("\16\u00a0\u06e1\13\u00a0\3\u00a1\3\u00a1\3\u00a1\3\u00a1")
        buf.write("\5\u00a1\u06e7\n\u00a1\3\u00a2\3\u00a2\3\u00a3\3\u00a3")
        buf.write("\3\u00a4\3\u00a4\3\u00a4\3\u00a4\3\u00a4\6\u00a4\u06f2")
        buf.write("\n\u00a4\r\u00a4\16\u00a4\u06f3\3\u00a5\3\u00a5\3\u00a5")
        buf.write("\3\u00a5\3\u00a5\3\u00a6\3\u00a6\3\u00a7\3\u00a7\3\u00a7")
        buf.write("\3\u00a7\3\u00a7\3\u00a8\3\u00a8\3\u00a8\7\u00a8\u0705")
        buf.write("\n\u00a8\f\u00a8\16\u00a8\u0708\13\u00a8\3\u00a9\3\u00a9")
        buf.write("\3\u00a9\3\u00aa\3\u00aa\3\u00aa\3\u00ab\3\u00ab\3\u00ab")
        buf.write("\3\u00ab\3\u00ab\5\u00ab\u0715\n\u00ab\3\u00ac\3\u00ac")
        buf.write("\3\u00ad\3\u00ad\3\u00ad\3\u00ad\3\u00ad\3\u00ae\3\u00ae")
        buf.write("\3\u00ae\3\u00ae\3\u00ae\3\u00af\3\u00af\3\u00b0\3\u00b0")
        buf.write("\3\u00b0\3\u00b1\3\u00b1\3\u00b1\3\u00b2\3\u00b2\3\u00b2")
        buf.write("\3\u00b3\3\u00b3\3\u00b3\3\u00b4\3\u00b4\3\u00b4\3\u00b4")
        buf.write("\3\u00b4\3\u00b5\3\u00b5\3\u00b6\3\u00b6\7\u00b6\u073a")
        buf.write("\n\u00b6\f\u00b6\16\u00b6\u073d\13\u00b6\3\u00b6\3\u00b6")
        buf.write("\7\u00b6\u0741\n\u00b6\f\u00b6\16\u00b6\u0744\13\u00b6")
        buf.write("\3\u00b7\3\u00b7\5\u00b7\u0748\n\u00b7\3\u00b7\3\u00b7")
        buf.write("\5\u00b7\u074c\n\u00b7\3\u00b7\3\u00b7\5\u00b7\u0750\n")
        buf.write("\u00b7\3\u00b7\3\u00b7\5\u00b7\u0754\n\u00b7\5\u00b7\u0756")
        buf.write("\n\u00b7\3\u00b7\3\u00b7\5\u00b7\u075a\n\u00b7\3\u00b8")
        buf.write("\3\u00b8\3\u00b8\5\u00b8\u075f\n\u00b8\3\u00b8\3\u00b8")
        buf.write("\3\u00b8\3\u00b8\3\u00b9\3\u00b9\3\u00b9\3\u00ba\3\u00ba")
        buf.write("\3\u00bb\3\u00bb\5\u00bb\u076c\n\u00bb\3\u00bc\3\u00bc")
        buf.write("\3\u00bc\7\u00bc\u0771\n\u00bc\f\u00bc\16\u00bc\u0774")
        buf.write("\13\u00bc\3\u00bd\3\u00bd\3\u00bd\3\u00bd\3\u00bd\6\u00bd")
        buf.write("\u077b\n\u00bd\r\u00bd\16\u00bd\u077c\3\u00be\5\u00be")
        buf.write("\u0780\n\u00be\3\u00be\3\u00be\3\u00bf\3\u00bf\3\u00bf")
        buf.write("\6\u00bf\u0787\n\u00bf\r\u00bf\16\u00bf\u0788\3\u00c0")
        buf.write("\3\u00c0\3\u00c0\3\u00c0\3\u00c1\3\u00c1\5\u00c1\u0791")
        buf.write("\n\u00c1\3\u00c2\3\u00c2\3\u00c2\6\u00c2\u0796\n\u00c2")
        buf.write("\r\u00c2\16\u00c2\u0797\3\u00c2\5\u00c2\u079b\n\u00c2")
        buf.write("\5\u00c2\u079d\n\u00c2\3\u00c3\3\u00c3\3\u00c4\7\u00c4")
        buf.write("\u07a2\n\u00c4\f\u00c4\16\u00c4\u07a5\13\u00c4\3\u00c4")
        buf.write("\7\u00c4\u07a8\n\u00c4\f\u00c4\16\u00c4\u07ab\13\u00c4")
        buf.write("\3\u00c4\5\u00c4\u07ae\n\u00c4\3\u00c4\7\u00c4\u07b1\n")
        buf.write("\u00c4\f\u00c4\16\u00c4\u07b4\13\u00c4\3\u00c4\7\u00c4")
        buf.write("\u07b7\n\u00c4\f\u00c4\16\u00c4\u07ba\13\u00c4\3\u00c5")
        buf.write("\3\u00c5\3\u00c6\3\u00c6\3\u00c6\3\u00c6\6\u00c6\u07c2")
        buf.write("\n\u00c6\r\u00c6\16\u00c6\u07c3\3\u00c6\5\u00c6\u07c7")
        buf.write("\n\u00c6\3\u00c7\3\u00c7\3\u00c8\3\u00c8\3\u00c9\3\u00c9")
        buf.write("\3\u00c9\5\u00c9\u07d0\n\u00c9\3\u00c9\3\u00c9\5\u00c9")
        buf.write("\u07d4\n\u00c9\3\u00c9\6\u00c9\u07d7\n\u00c9\r\u00c9\16")
        buf.write("\u00c9\u07d8\3\u00c9\5\u00c9\u07dc\n\u00c9\3\u00ca\3\u00ca")
        buf.write("\3\u00cb\3\u00cb\3\u00cb\7\u00cb\u07e3\n\u00cb\f\u00cb")
        buf.write("\16\u00cb\u07e6\13\u00cb\3\u00cc\5\u00cc\u07e9\n\u00cc")
        buf.write("\3\u00cc\3\u00cc\3\u00cd\3\u00cd\3\u00cd\3\u00cd\3\u00cd")
        buf.write("\3\u00cd\3\u00cd\3\u00cd\3\u00cd\3\u00cd\3\u00cd\3\u00cd")
        buf.write("\3\u00cd\3\u00cd\3\u00cd\3\u00cd\3\u00cd\5\u00cd\u07fe")
        buf.write("\n\u00cd\3\u00ce\3\u00ce\3\u00ce\3\u00ce\6\u00ce\u0804")
        buf.write("\n\u00ce\r\u00ce\16\u00ce\u0805\3\u00ce\3\u00ce\3\u00cf")
        buf.write("\3\u00cf\5\u00cf\u080c\n\u00cf\3\u00cf\5\u00cf\u080f\n")
        buf.write("\u00cf\3\u00cf\5\u00cf\u0812\n\u00cf\3\u00cf\5\u00cf\u0815")
        buf.write("\n\u00cf\3\u00d0\3\u00d0\5\u00d0\u0819\n\u00d0\3\u00d1")
        buf.write("\3\u00d1\3\u00d2\3\u00d2\3\u00d2\3\u00d2\3\u00d2\3\u00d2")
        buf.write("\7\u00d2\u0823\n\u00d2\f\u00d2\16\u00d2\u0826\13\u00d2")
        buf.write("\5\u00d2\u0828\n\u00d2\3\u00d3\3\u00d3\3\u00d4\3\u00d4")
        buf.write("\3\u00d4\5\u00d4\u082f\n\u00d4\3\u00d4\3\u00d4\5\u00d4")
        buf.write("\u0833\n\u00d4\3\u00d4\5\u00d4\u0836\n\u00d4\3\u00d5\3")
        buf.write("\u00d5\3\u00d6\3\u00d6\3\u00d7\3\u00d7\3\u00d7\3\u00d7")
        buf.write("\3\u00d8\3\u00d8\3\u00d8\5\u00d8\u0843\n\u00d8\3\u00d8")
        buf.write("\3\u00d8\3\u00d9\3\u00d9\3\u00da\3\u00da\3\u00da\5\u00da")
        buf.write("\u084c\n\u00da\3\u00da\3\u00da\3\u00db\3\u00db\3\u00dc")
        buf.write("\3\u00dc\3\u00dc\3\u00dd\3\u00dd\3\u00dd\3\u00de\3\u00de")
        buf.write("\5\u00de\u085a\n\u00de\3\u00de\3\u00de\7\u00de\u085e\n")
        buf.write("\u00de\f\u00de\16\u00de\u0861\13\u00de\3\u00de\3\u00de")
        buf.write("\5\u00de\u0865\n\u00de\3\u00de\3\u00de\3\u00de\3\u00de")
        buf.write("\3\u00de\3\u00de\3\u00de\3\u00de\3\u00de\3\u00de\3\u00de")
        buf.write("\3\u00de\3\u00de\3\u00de\3\u00de\7\u00de\u0876\n\u00de")
        buf.write("\f\u00de\16\u00de\u0879\13\u00de\3\u00de\7\u00de\u087c")
        buf.write("\n\u00de\f\u00de\16\u00de\u087f\13\u00de\3\u00de\3\u00de")
        buf.write("\5\u00de\u0883\n\u00de\3\u00de\7\u00de\u0886\n\u00de\f")
        buf.write("\u00de\16\u00de\u0889\13\u00de\3\u00de\7\u00de\u088c\n")
        buf.write("\u00de\f\u00de\16\u00de\u088f\13\u00de\3\u00de\7\u00de")
        buf.write("\u0892\n\u00de\f\u00de\16\u00de\u0895\13\u00de\3\u00de")
        buf.write("\3\u00de\3\u00df\3\u00df\7\u00df\u089b\n\u00df\f\u00df")
        buf.write("\16\u00df\u089e\13\u00df\3\u00df\3\u00df\7\u00df\u08a2")
        buf.write("\n\u00df\f\u00df\16\u00df\u08a5\13\u00df\3\u00df\3\u00df")
        buf.write("\7\u00df\u08a9\n\u00df\f\u00df\16\u00df\u08ac\13\u00df")
        buf.write("\3\u00df\3\u00df\7\u00df\u08b0\n\u00df\f\u00df\16\u00df")
        buf.write("\u08b3\13\u00df\3\u00e0\3\u00e0\3\u00e1\3\u00e1\3\u00e1")
        buf.write("\3\u00e1\5\u00e1\u08bb\n\u00e1\3\u00e1\3\u00e1\3\u00e1")
        buf.write("\3\u00e1\3\u00e2\3\u00e2\3\u00e3\3\u00e3\3\u00e3\3\u00e3")
        buf.write("\5\u00e3\u08c7\n\u00e3\3\u00e3\3\u00e3\3\u00e3\3\u00e3")
        buf.write("\3\u00e4\3\u00e4\3\u00e5\3\u00e5\5\u00e5\u08d1\n\u00e5")
        buf.write("\3\u00e6\3\u00e6\3\u00e7\3\u00e7\3\u00e7\3\u00e7\3\u00e8")
        buf.write("\3\u00e8\3\u00e8\3\u00e8\3\u00e9\3\u00e9\3\u00ea\3\u00ea")
        buf.write("\3\u00ea\3\u00ea\3\u00eb\3\u00eb\3\u00ec\3\u00ec\3\u00ec")
        buf.write("\3\u00ec\3\u00ed\3\u00ed\3\u00ed\3\u00ed\5\u00ed\u08ed")
        buf.write("\n\u00ed\3\u00ee\3\u00ee\3\u00ee\3\u00ee\5\u00ee\u08f3")
        buf.write("\n\u00ee\3\u00ef\3\u00ef\3\u00ef\3\u00ef\3\u00f0\3\u00f0")
        buf.write("\3\u00f0\3\u00f0\3\u00f1\3\u00f1\3\u00f1\3\u00f1\3\u00f2")
        buf.write("\3\u00f2\3\u00f2\7\u00f2\u0904\n\u00f2\f\u00f2\16\u00f2")
        buf.write("\u0907\13\u00f2\3\u00f3\3\u00f3\3\u00f4\3\u00f4\3\u00f4")
        buf.write("\3\u00f4\3\u00f5\3\u00f5\3\u00f5\3\u00f5\3\u00f6\3\u00f6")
        buf.write("\3\u00f7\3\u00f7\3\u00f7\3\u00f7\3\u00f8\3\u00f8\3\u00f9")
        buf.write("\3\u00f9\3\u00f9\7\u00f9\u091e\n\u00f9\f\u00f9\16\u00f9")
        buf.write("\u0921\13\u00f9\3\u00fa\3\u00fa\5\u00fa\u0925\n\u00fa")
        buf.write("\3\u00fb\3\u00fb\5\u00fb\u0929\n\u00fb\3\u00fb\5\u00fb")
        buf.write("\u092c\n\u00fb\3\u00fc\3\u00fc\3\u00fd\3\u00fd\3\u00fd")
        buf.write("\3\u00fd\3\u00fe\3\u00fe\3\u00fe\7\u00fe\u0937\n\u00fe")
        buf.write("\f\u00fe\16\u00fe\u093a\13\u00fe\3\u00ff\3\u00ff\3\u0100")
        buf.write("\3\u0100\5\u0100\u0940\n\u0100\3\u0100\5\u0100\u0943\n")
        buf.write("\u0100\3\u0101\3\u0101\5\u0101\u0947\n\u0101\3\u0102\3")
        buf.write("\u0102\5\u0102\u094b\n\u0102\3\u0103\3\u0103\3\u0103\3")
        buf.write("\u0104\3\u0104\3\u0104\3\u0105\3\u0105\3\u0105\3\u0106")
        buf.write("\3\u0106\3\u0106\3\u0106\3\u0106\7\u0106\u095b\n\u0106")
        buf.write("\f\u0106\16\u0106\u095e\13\u0106\3\u0106\6\u0106\u0961")
        buf.write("\n\u0106\r\u0106\16\u0106\u0962\3\u0106\7\u0106\u0966")
        buf.write("\n\u0106\f\u0106\16\u0106\u0969\13\u0106\3\u0106\3\u0106")
        buf.write("\3\u0107\3\u0107\3\u0108\5\u0108\u0970\n\u0108\3\u0108")
        buf.write("\7\u0108\u0973\n\u0108\f\u0108\16\u0108\u0976\13\u0108")
        buf.write("\3\u0108\5\u0108\u0979\n\u0108\3\u0108\3\u0108\3\u0108")
        buf.write("\5\u0108\u097e\n\u0108\3\u0108\7\u0108\u0981\n\u0108\f")
        buf.write("\u0108\16\u0108\u0984\13\u0108\3\u0109\3\u0109\3\u0109")
        buf.write("\5\u0109\u0989\n\u0109\3\u010a\3\u010a\3\u010b\3\u010b")
        buf.write("\3\u010b\3\u010b\7\u010b\u0991\n\u010b\f\u010b\16\u010b")
        buf.write("\u0994\13\u010b\3\u010b\3\u010b\3\u010c\3\u010c\3\u010c")
        buf.write("\3\u010c\3\u010d\3\u010d\3\u010e\3\u010e\3\u010e\5\u010e")
        buf.write("\u09a1\n\u010e\3\u010f\3\u010f\3\u0110\3\u0110\3\u0110")
        buf.write("\3\u0110\3\u0110\3\u0111\3\u0111\3\u0111\5\u0111\u09ad")
        buf.write("\n\u0111\3\u0111\3\u0111\3\u0112\3\u0112\3\u0112\5\u0112")
        buf.write("\u09b4\n\u0112\3\u0113\3\u0113\3\u0113\3\u0114\3\u0114")
        buf.write("\3\u0115\3\u0115\5\u0115\u09bd\n\u0115\3\u0116\3\u0116")
        buf.write("\3\u0116\3\u0116\3\u0116\3\u0117\3\u0117\3\u0117\2\2\u0118")
        buf.write("\2\4\6\b\n\f\16\20\22\24\26\30\32\34\36 \"$&(*,.\60\62")
        buf.write("\64\668:<>@BDFHJLNPRTVXZ\\^`bdfhjlnprtvxz|~\u0080\u0082")
        buf.write("\u0084\u0086\u0088\u008a\u008c\u008e\u0090\u0092\u0094")
        buf.write("\u0096\u0098\u009a\u009c\u009e\u00a0\u00a2\u00a4\u00a6")
        buf.write("\u00a8\u00aa\u00ac\u00ae\u00b0\u00b2\u00b4\u00b6\u00b8")
        buf.write("\u00ba\u00bc\u00be\u00c0\u00c2\u00c4\u00c6\u00c8\u00ca")
        buf.write("\u00cc\u00ce\u00d0\u00d2\u00d4\u00d6\u00d8\u00da\u00dc")
        buf.write("\u00de\u00e0\u00e2\u00e4\u00e6\u00e8\u00ea\u00ec\u00ee")
        buf.write("\u00f0\u00f2\u00f4\u00f6\u00f8\u00fa\u00fc\u00fe\u0100")
        buf.write("\u0102\u0104\u0106\u0108\u010a\u010c\u010e\u0110\u0112")
        buf.write("\u0114\u0116\u0118\u011a\u011c\u011e\u0120\u0122\u0124")
        buf.write("\u0126\u0128\u012a\u012c\u012e\u0130\u0132\u0134\u0136")
        buf.write("\u0138\u013a\u013c\u013e\u0140\u0142\u0144\u0146\u0148")
        buf.write("\u014a\u014c\u014e\u0150\u0152\u0154\u0156\u0158\u015a")
        buf.write("\u015c\u015e\u0160\u0162\u0164\u0166\u0168\u016a\u016c")
        buf.write("\u016e\u0170\u0172\u0174\u0176\u0178\u017a\u017c\u017e")
        buf.write("\u0180\u0182\u0184\u0186\u0188\u018a\u018c\u018e\u0190")
        buf.write("\u0192\u0194\u0196\u0198\u019a\u019c\u019e\u01a0\u01a2")
        buf.write("\u01a4\u01a6\u01a8\u01aa\u01ac\u01ae\u01b0\u01b2\u01b4")
        buf.write("\u01b6\u01b8\u01ba\u01bc\u01be\u01c0\u01c2\u01c4\u01c6")
        buf.write("\u01c8\u01ca\u01cc\u01ce\u01d0\u01d2\u01d4\u01d6\u01d8")
        buf.write("\u01da\u01dc\u01de\u01e0\u01e2\u01e4\u01e6\u01e8\u01ea")
        buf.write("\u01ec\u01ee\u01f0\u01f2\u01f4\u01f6\u01f8\u01fa\u01fc")
        buf.write("\u01fe\u0200\u0202\u0204\u0206\u0208\u020a\u020c\u020e")
        buf.write("\u0210\u0212\u0214\u0216\u0218\u021a\u021c\u021e\u0220")
        buf.write("\u0222\u0224\u0226\u0228\u022a\u022c\2\23\4\2,wyy\3\2")
        buf.write("\u0092\u0093\4\2\u008b\u008b\u0090\u0090\3\2\u0092\u0092")
        buf.write("\3\2\u0099\u009a\3\2\u008b\u0090\4\2zz\u0084\u0084\5\2")
        buf.write("88::==\3\2BD\4\2\u008e\u008e\u0090\u0090\3\2`b\3\2,.\4")
        buf.write("\2\u0086\u0086\u0090\u0090\4\2\u0088\u0088\u008c\u008c")
        buf.write("\3\2\r\17\3\2WY\4\2WZnn\2\u0a26\2\u0231\3\2\2\2\4\u0263")
        buf.write("\3\2\2\2\6\u0268\3\2\2\2\b\u026c\3\2\2\2\n\u026e\3\2\2")
        buf.write("\2\f\u0272\3\2\2\2\16\u027c\3\2\2\2\20\u0280\3\2\2\2\22")
        buf.write("\u028e\3\2\2\2\24\u0290\3\2\2\2\26\u0292\3\2\2\2\30\u0294")
        buf.write("\3\2\2\2\32\u0296\3\2\2\2\34\u0298\3\2\2\2\36\u02a0\3")
        buf.write("\2\2\2 \u02bf\3\2\2\2\"\u02c2\3\2\2\2$\u02c8\3\2\2\2&")
        buf.write("\u02ce\3\2\2\2(\u02d0\3\2\2\2*\u02d4\3\2\2\2,\u02e0\3")
        buf.write("\2\2\2.\u02e2\3\2\2\2\60\u02e9\3\2\2\2\62\u02eb\3\2\2")
        buf.write("\2\64\u02f0\3\2\2\2\66\u02f5\3\2\2\28\u02fa\3\2\2\2:\u02ff")
        buf.write("\3\2\2\2<\u031d\3\2\2\2>\u031f\3\2\2\2@\u0341\3\2\2\2")
        buf.write("B\u035e\3\2\2\2D\u037b\3\2\2\2F\u037d\3\2\2\2H\u03b3\3")
        buf.write("\2\2\2J\u03ba\3\2\2\2L\u03c2\3\2\2\2N\u03ca\3\2\2\2P\u03d1")
        buf.write("\3\2\2\2R\u03d8\3\2\2\2T\u03de\3\2\2\2V\u03e0\3\2\2\2")
        buf.write("X\u03e4\3\2\2\2Z\u03e6\3\2\2\2\\\u03f1\3\2\2\2^\u03f6")
        buf.write("\3\2\2\2`\u03f8\3\2\2\2b\u03fd\3\2\2\2d\u0405\3\2\2\2")
        buf.write("f\u0427\3\2\2\2h\u0431\3\2\2\2j\u043c\3\2\2\2l\u0444\3")
        buf.write("\2\2\2n\u044d\3\2\2\2p\u044f\3\2\2\2r\u0456\3\2\2\2t\u045b")
        buf.write("\3\2\2\2v\u047c\3\2\2\2x\u047e\3\2\2\2z\u0481\3\2\2\2")
        buf.write("|\u0485\3\2\2\2~\u0488\3\2\2\2\u0080\u048a\3\2\2\2\u0082")
        buf.write("\u048d\3\2\2\2\u0084\u048f\3\2\2\2\u0086\u0498\3\2\2\2")
        buf.write("\u0088\u049a\3\2\2\2\u008a\u049d\3\2\2\2\u008c\u04a0\3")
        buf.write("\2\2\2\u008e\u04a2\3\2\2\2\u0090\u04b6\3\2\2\2\u0092\u04b8")
        buf.write("\3\2\2\2\u0094\u04ba\3\2\2\2\u0096\u04bc\3\2\2\2\u0098")
        buf.write("\u04be\3\2\2\2\u009a\u04c0\3\2\2\2\u009c\u04c2\3\2\2\2")
        buf.write("\u009e\u04c4\3\2\2\2\u00a0\u04c6\3\2\2\2\u00a2\u04c8\3")
        buf.write("\2\2\2\u00a4\u04ca\3\2\2\2\u00a6\u04cc\3\2\2\2\u00a8\u04ce")
        buf.write("\3\2\2\2\u00aa\u04d0\3\2\2\2\u00ac\u04db\3\2\2\2\u00ae")
        buf.write("\u04dd\3\2\2\2\u00b0\u04e8\3\2\2\2\u00b2\u04ef\3\2\2\2")
        buf.write("\u00b4\u04f1\3\2\2\2\u00b6\u04f4\3\2\2\2\u00b8\u04fb\3")
        buf.write("\2\2\2\u00ba\u0506\3\2\2\2\u00bc\u050d\3\2\2\2\u00be\u050f")
        buf.write("\3\2\2\2\u00c0\u0512\3\2\2\2\u00c2\u0517\3\2\2\2\u00c4")
        buf.write("\u051f\3\2\2\2\u00c6\u0521\3\2\2\2\u00c8\u0528\3\2\2\2")
        buf.write("\u00ca\u052a\3\2\2\2\u00cc\u0531\3\2\2\2\u00ce\u0533\3")
        buf.write("\2\2\2\u00d0\u053b\3\2\2\2\u00d2\u053f\3\2\2\2\u00d4\u0541")
        buf.write("\3\2\2\2\u00d6\u0547\3\2\2\2\u00d8\u054a\3\2\2\2\u00da")
        buf.write("\u054d\3\2\2\2\u00dc\u055b\3\2\2\2\u00de\u055d\3\2\2\2")
        buf.write("\u00e0\u055f\3\2\2\2\u00e2\u0561\3\2\2\2\u00e4\u0563\3")
        buf.write("\2\2\2\u00e6\u0576\3\2\2\2\u00e8\u0578\3\2\2\2\u00ea\u059a")
        buf.write("\3\2\2\2\u00ec\u05b0\3\2\2\2\u00ee\u05ba\3\2\2\2\u00f0")
        buf.write("\u05bc\3\2\2\2\u00f2\u05be\3\2\2\2\u00f4\u05c8\3\2\2\2")
        buf.write("\u00f6\u05d7\3\2\2\2\u00f8\u05d9\3\2\2\2\u00fa\u05dd\3")
        buf.write("\2\2\2\u00fc\u05df\3\2\2\2\u00fe\u05e3\3\2\2\2\u0100\u05e7")
        buf.write("\3\2\2\2\u0102\u05f1\3\2\2\2\u0104\u05f9\3\2\2\2\u0106")
        buf.write("\u05fb\3\2\2\2\u0108\u05fd\3\2\2\2\u010a\u0606\3\2\2\2")
        buf.write("\u010c\u060f\3\2\2\2\u010e\u0618\3\2\2\2\u0110\u0621\3")
        buf.write("\2\2\2\u0112\u062a\3\2\2\2\u0114\u0633\3\2\2\2\u0116\u0644")
        buf.write("\3\2\2\2\u0118\u0646\3\2\2\2\u011a\u0648\3\2\2\2\u011c")
        buf.write("\u0653\3\2\2\2\u011e\u066a\3\2\2\2\u0120\u066d\3\2\2\2")
        buf.write("\u0122\u066f\3\2\2\2\u0124\u0678\3\2\2\2\u0126\u0680\3")
        buf.write("\2\2\2\u0128\u068b\3\2\2\2\u012a\u0696\3\2\2\2\u012c\u06a1")
        buf.write("\3\2\2\2\u012e\u06aa\3\2\2\2\u0130\u06b3\3\2\2\2\u0132")
        buf.write("\u06bf\3\2\2\2\u0134\u06c1\3\2\2\2\u0136\u06cd\3\2\2\2")
        buf.write("\u0138\u06d3\3\2\2\2\u013a\u06d5\3\2\2\2\u013c\u06d7\3")
        buf.write("\2\2\2\u013e\u06d9\3\2\2\2\u0140\u06e2\3\2\2\2\u0142\u06e8")
        buf.write("\3\2\2\2\u0144\u06ea\3\2\2\2\u0146\u06ec\3\2\2\2\u0148")
        buf.write("\u06f5\3\2\2\2\u014a\u06fa\3\2\2\2\u014c\u06fc\3\2\2\2")
        buf.write("\u014e\u0701\3\2\2\2\u0150\u0709\3\2\2\2\u0152\u070c\3")
        buf.write("\2\2\2\u0154\u070f\3\2\2\2\u0156\u0716\3\2\2\2\u0158\u0718")
        buf.write("\3\2\2\2\u015a\u071d\3\2\2\2\u015c\u0722\3\2\2\2\u015e")
        buf.write("\u0724\3\2\2\2\u0160\u0727\3\2\2\2\u0162\u072a\3\2\2\2")
        buf.write("\u0164\u072d\3\2\2\2\u0166\u0730\3\2\2\2\u0168\u0735\3")
        buf.write("\2\2\2\u016a\u0737\3\2\2\2\u016c\u0745\3\2\2\2\u016e\u075e")
        buf.write("\3\2\2\2\u0170\u0764\3\2\2\2\u0172\u0767\3\2\2\2\u0174")
        buf.write("\u076b\3\2\2\2\u0176\u076d\3\2\2\2\u0178\u077a\3\2\2\2")
        buf.write("\u017a\u077f\3\2\2\2\u017c\u0786\3\2\2\2\u017e\u078a\3")
        buf.write("\2\2\2\u0180\u0790\3\2\2\2\u0182\u079c\3\2\2\2\u0184\u079e")
        buf.write("\3\2\2\2\u0186\u07a3\3\2\2\2\u0188\u07bb\3\2\2\2\u018a")
        buf.write("\u07bd\3\2\2\2\u018c\u07c8\3\2\2\2\u018e\u07ca\3\2\2\2")
        buf.write("\u0190\u07cc\3\2\2\2\u0192\u07dd\3\2\2\2\u0194\u07df\3")
        buf.write("\2\2\2\u0196\u07e8\3\2\2\2\u0198\u07fd\3\2\2\2\u019a\u07ff")
        buf.write("\3\2\2\2\u019c\u0809\3\2\2\2\u019e\u0818\3\2\2\2\u01a0")
        buf.write("\u081a\3\2\2\2\u01a2\u081c\3\2\2\2\u01a4\u0829\3\2\2\2")
        buf.write("\u01a6\u082b\3\2\2\2\u01a8\u0837\3\2\2\2\u01aa\u0839\3")
        buf.write("\2\2\2\u01ac\u083b\3\2\2\2\u01ae\u083f\3\2\2\2\u01b0\u0846")
        buf.write("\3\2\2\2\u01b2\u0848\3\2\2\2\u01b4\u084f\3\2\2\2\u01b6")
        buf.write("\u0851\3\2\2\2\u01b8\u0854\3\2\2\2\u01ba\u0859\3\2\2\2")
        buf.write("\u01bc\u0898\3\2\2\2\u01be\u08b4\3\2\2\2\u01c0\u08ba\3")
        buf.write("\2\2\2\u01c2\u08c0\3\2\2\2\u01c4\u08c6\3\2\2\2\u01c6\u08cc")
        buf.write("\3\2\2\2\u01c8\u08d0\3\2\2\2\u01ca\u08d2\3\2\2\2\u01cc")
        buf.write("\u08d4\3\2\2\2\u01ce\u08d8\3\2\2\2\u01d0\u08dc\3\2\2\2")
        buf.write("\u01d2\u08de\3\2\2\2\u01d4\u08e2\3\2\2\2\u01d6\u08e4\3")
        buf.write("\2\2\2\u01d8\u08e8\3\2\2\2\u01da\u08ee\3\2\2\2\u01dc\u08f4")
        buf.write("\3\2\2\2\u01de\u08f8\3\2\2\2\u01e0\u08fc\3\2\2\2\u01e2")
        buf.write("\u0900\3\2\2\2\u01e4\u0908\3\2\2\2\u01e6\u090a\3\2\2\2")
        buf.write("\u01e8\u090e\3\2\2\2\u01ea\u0912\3\2\2\2\u01ec\u0914\3")
        buf.write("\2\2\2\u01ee\u0918\3\2\2\2\u01f0\u091a\3\2\2\2\u01f2\u0922")
        buf.write("\3\2\2\2\u01f4\u092b\3\2\2\2\u01f6\u092d\3\2\2\2\u01f8")
        buf.write("\u092f\3\2\2\2\u01fa\u0933\3\2\2\2\u01fc\u093b\3\2\2\2")
        buf.write("\u01fe\u0942\3\2\2\2\u0200\u0944\3\2\2\2\u0202\u0948\3")
        buf.write("\2\2\2\u0204\u094c\3\2\2\2\u0206\u094f\3\2\2\2\u0208\u0952")
        buf.write("\3\2\2\2\u020a\u0955\3\2\2\2\u020c\u096c\3\2\2\2\u020e")
        buf.write("\u096f\3\2\2\2\u0210\u0985\3\2\2\2\u0212\u098a\3\2\2\2")
        buf.write("\u0214\u098c\3\2\2\2\u0216\u0997\3\2\2\2\u0218\u099b\3")
        buf.write("\2\2\2\u021a\u09a0\3\2\2\2\u021c\u09a2\3\2\2\2\u021e\u09a4")
        buf.write("\3\2\2\2\u0220\u09ac\3\2\2\2\u0222\u09b3\3\2\2\2\u0224")
        buf.write("\u09b5\3\2\2\2\u0226\u09b8\3\2\2\2\u0228\u09ba\3\2\2\2")
        buf.write("\u022a\u09be\3\2\2\2\u022c\u09c3\3\2\2\2\u022e\u0230\7")
        buf.write("x\2\2\u022f\u022e\3\2\2\2\u0230\u0233\3\2\2\2\u0231\u022f")
        buf.write("\3\2\2\2\u0231\u0232\3\2\2\2\u0232\u0237\3\2\2\2\u0233")
        buf.write("\u0231\3\2\2\2\u0234\u0236\5,\27\2\u0235\u0234\3\2\2\2")
        buf.write("\u0236\u0239\3\2\2\2\u0237\u0235\3\2\2\2\u0237\u0238\3")
        buf.write("\2\2\2\u0238\u023d\3\2\2\2\u0239\u0237\3\2\2\2\u023a\u023c")
        buf.write("\7x\2\2\u023b\u023a\3\2\2\2\u023c\u023f\3\2\2\2\u023d")
        buf.write("\u023b\3\2\2\2\u023d\u023e\3\2\2\2\u023e\u0248\3\2\2\2")
        buf.write("\u023f\u023d\3\2\2\2\u0240\u0242\5\4\3\2\u0241\u0240\3")
        buf.write("\2\2\2\u0241\u0242\3\2\2\2\u0242\u0244\3\2\2\2\u0243\u0245")
        buf.write("\5\u016a\u00b6\2\u0244\u0243\3\2\2\2\u0245\u0246\3\2\2")
        buf.write("\2\u0246\u0244\3\2\2\2\u0246\u0247\3\2\2\2\u0247\u0249")
        buf.write("\3\2\2\2\u0248\u0241\3\2\2\2\u0248\u0249\3\2\2\2\u0249")
        buf.write("\u024d\3\2\2\2\u024a\u024c\7x\2\2\u024b\u024a\3\2\2\2")
        buf.write("\u024c\u024f\3\2\2\2\u024d\u024b\3\2\2\2\u024d\u024e\3")
        buf.write("\2\2\2\u024e\u0258\3\2\2\2\u024f\u024d\3\2\2\2\u0250\u0252")
        buf.write("\5\6\4\2\u0251\u0250\3\2\2\2\u0251\u0252\3\2\2\2\u0252")
        buf.write("\u0254\3\2\2\2\u0253\u0255\5d\63\2\u0254\u0253\3\2\2\2")
        buf.write("\u0255\u0256\3\2\2\2\u0256\u0254\3\2\2\2\u0256\u0257\3")
        buf.write("\2\2\2\u0257\u0259\3\2\2\2\u0258\u0251\3\2\2\2\u0258\u0259")
        buf.write("\3\2\2\2\u0259\u025d\3\2\2\2\u025a\u025c\7x\2\2\u025b")
        buf.write("\u025a\3\2\2\2\u025c\u025f\3\2\2\2\u025d\u025b\3\2\2\2")
        buf.write("\u025d\u025e\3\2\2\2\u025e\u0260\3\2\2\2\u025f\u025d\3")
        buf.write("\2\2\2\u0260\u0261\7\2\2\3\u0261\3\3\2\2\2\u0262\u0264")
        buf.write("\5\b\5\2\u0263\u0262\3\2\2\2\u0264\u0265\3\2\2\2\u0265")
        buf.write("\u0263\3\2\2\2\u0265\u0266\3\2\2\2\u0266\5\3\2\2\2\u0267")
        buf.write("\u0269\5\n\6\2\u0268\u0267\3\2\2\2\u0269\u026a\3\2\2\2")
        buf.write("\u026a\u0268\3\2\2\2\u026a\u026b\3\2\2\2\u026b\7\3\2\2")
        buf.write("\2\u026c\u026d\5\f\7\2\u026d\t\3\2\2\2\u026e\u026f\5\f")
        buf.write("\7\2\u026f\13\3\2\2\2\u0270\u0271\7\\\2\2\u0271\u0273")
        buf.write("\5\16\b\2\u0272\u0270\3\2\2\2\u0272\u0273\3\2\2\2\u0273")
        buf.write("\u0274\3\2\2\2\u0274\u0275\7t\2\2\u0275\u0277\5\20\t\2")
        buf.write("\u0276\u0278\7x\2\2\u0277\u0276\3\2\2\2\u0278\u0279\3")
        buf.write("\2\2\2\u0279\u0277\3\2\2\2\u0279\u027a\3\2\2\2\u027a\r")
        buf.write("\3\2\2\2\u027b\u027d\7\u0088\2\2\u027c\u027b\3\2\2\2\u027c")
        buf.write("\u027d\3\2\2\2\u027d\u027e\3\2\2\2\u027e\u027f\5\34\17")
        buf.write("\2\u027f\17\3\2\2\2\u0280\u0285\5\22\n\2\u0281\u0282\7")
        buf.write("\u0087\2\2\u0282\u0284\5\22\n\2\u0283\u0281\3\2\2\2\u0284")
        buf.write("\u0287\3\2\2\2\u0285\u0283\3\2\2\2\u0285\u0286\3\2\2\2")
        buf.write("\u0286\21\3\2\2\2\u0287\u0285\3\2\2\2\u0288\u028b\5\24")
        buf.write("\13\2\u0289\u028a\7u\2\2\u028a\u028c\5\26\f\2\u028b\u0289")
        buf.write("\3\2\2\2\u028b\u028c\3\2\2\2\u028c\u028f\3\2\2\2\u028d")
        buf.write("\u028f\5\30\r\2\u028e\u0288\3\2\2\2\u028e\u028d\3\2\2")
        buf.write("\2\u028f\23\3\2\2\2\u0290\u0291\5\34\17\2\u0291\25\3\2")
        buf.write("\2\2\u0292\u0293\5\32\16\2\u0293\27\3\2\2\2\u0294\u0295")
        buf.write("\7\u008f\2\2\u0295\31\3\2\2\2\u0296\u0297\t\2\2\2\u0297")
        buf.write("\33\3\2\2\2\u0298\u029d\5\32\16\2\u0299\u029a\7\u0088")
        buf.write("\2\2\u029a\u029c\5\32\16\2\u029b\u0299\3\2\2\2\u029c\u029f")
        buf.write("\3\2\2\2\u029d\u029b\3\2\2\2\u029d\u029e\3\2\2\2\u029e")
        buf.write("\35\3\2\2\2\u029f\u029d\3\2\2\2\u02a0\u02a4\7\u0089\2")
        buf.write("\2\u02a1\u02a2\5\32\16\2\u02a2\u02a3\7\u0088\2\2\u02a3")
        buf.write("\u02a5\3\2\2\2\u02a4\u02a1\3\2\2\2\u02a4\u02a5\3\2\2\2")
        buf.write("\u02a5\u02a6\3\2\2\2\u02a6\u02a7\5\32\16\2\u02a7\37\3")
        buf.write("\2\2\2\u02a8\u02aa\7\u0088\2\2\u02a9\u02a8\3\2\2\2\u02a9")
        buf.write("\u02aa\3\2\2\2\u02aa\u02ab\3\2\2\2\u02ab\u02b1\7\u008f")
        buf.write("\2\2\u02ac\u02ad\7\u0087\2\2\u02ad\u02ae\7\177\2\2\u02ae")
        buf.write("\u02b0\5\"\22\2\u02af\u02ac\3\2\2\2\u02b0\u02b3\3\2\2")
        buf.write("\2\u02b1\u02af\3\2\2\2\u02b1\u02b2\3\2\2\2\u02b2\u02c0")
        buf.write("\3\2\2\2\u02b3\u02b1\3\2\2\2\u02b4\u02bc\5\32\16\2\u02b5")
        buf.write("\u02b7\7\u0087\2\2\u02b6\u02b8\7\177\2\2\u02b7\u02b6\3")
        buf.write("\2\2\2\u02b7\u02b8\3\2\2\2\u02b8\u02b9\3\2\2\2\u02b9\u02bb")
        buf.write("\5\"\22\2\u02ba\u02b5\3\2\2\2\u02bb\u02be\3\2\2\2\u02bc")
        buf.write("\u02ba\3\2\2\2\u02bc\u02bd\3\2\2\2\u02bd\u02c0\3\2\2\2")
        buf.write("\u02be\u02bc\3\2\2\2\u02bf\u02a9\3\2\2\2\u02bf\u02b4\3")
        buf.write("\2\2\2\u02c0!\3\2\2\2\u02c1\u02c3\7\u008f\2\2\u02c2\u02c1")
        buf.write("\3\2\2\2\u02c2\u02c3\3\2\2\2\u02c3\u02c4\3\2\2\2\u02c4")
        buf.write("\u02c6\5\32\16\2\u02c5\u02c7\7\u008f\2\2\u02c6\u02c5\3")
        buf.write("\2\2\2\u02c6\u02c7\3\2\2\2\u02c7#\3\2\2\2\u02c8\u02c9")
        buf.write("\7\u0082\2\2\u02c9\u02ca\7v\2\2\u02ca\u02cb\7\u0083\2")
        buf.write("\2\u02cb%\3\2\2\2\u02cc\u02cf\5*\26\2\u02cd\u02cf\5(\25")
        buf.write("\2\u02ce\u02cc\3\2\2\2\u02ce\u02cd\3\2\2\2\u02cf\'\3\2")
        buf.write("\2\2\u02d0\u02d1\7\u0099\2\2\u02d1\u02d2\7\u009d\2\2\u02d2")
        buf.write("\u02d3\7x\2\2\u02d3)\3\2\2\2\u02d4\u02d5\7\u009b\2\2\u02d5")
        buf.write("+\3\2\2\2\u02d6\u02e1\5.\30\2\u02d7\u02e1\5\62\32\2\u02d8")
        buf.write("\u02e1\5\64\33\2\u02d9\u02e1\5\66\34\2\u02da\u02e1\58")
        buf.write("\35\2\u02db\u02e1\5:\36\2\u02dc\u02e1\5V,\2\u02dd\u02e1")
        buf.write("\5Z.\2\u02de\u02e1\5`\61\2\u02df\u02e1\7x\2\2\u02e0\u02d6")
        buf.write("\3\2\2\2\u02e0\u02d7\3\2\2\2\u02e0\u02d8\3\2\2\2\u02e0")
        buf.write("\u02d9\3\2\2\2\u02e0\u02da\3\2\2\2\u02e0\u02db\3\2\2\2")
        buf.write("\u02e0\u02dc\3\2\2\2\u02e0\u02dd\3\2\2\2\u02e0\u02de\3")
        buf.write("\2\2\2\u02e0\u02df\3\2\2\2\u02e1-\3\2\2\2\u02e2\u02e7")
        buf.write("\7\4\2\2\u02e3\u02e4\7\u0080\2\2\u02e4\u02e5\5\60\31\2")
        buf.write("\u02e5\u02e6\7\u0081\2\2\u02e6\u02e8\3\2\2\2\u02e7\u02e3")
        buf.write("\3\2\2\2\u02e7\u02e8\3\2\2\2\u02e8/\3\2\2\2\u02e9\u02ea")
        buf.write("\t\3\2\2\u02ea\61\3\2\2\2\u02eb\u02ee\7\5\2\2\u02ec\u02ed")
        buf.write("\7\u0080\2\2\u02ed\u02ef\7\u0081\2\2\u02ee\u02ec\3\2\2")
        buf.write("\2\u02ee\u02ef\3\2\2\2\u02ef\63\3\2\2\2\u02f0\u02f3\7")
        buf.write("\7\2\2\u02f1\u02f2\7\u0080\2\2\u02f2\u02f4\7\u0081\2\2")
        buf.write("\u02f3\u02f1\3\2\2\2\u02f3\u02f4\3\2\2\2\u02f4\65\3\2")
        buf.write("\2\2\u02f5\u02f8\7\b\2\2\u02f6\u02f7\7\u0080\2\2\u02f7")
        buf.write("\u02f9\7\u0081\2\2\u02f8\u02f6\3\2\2\2\u02f8\u02f9\3\2")
        buf.write("\2\2\u02f9\67\3\2\2\2\u02fa\u02fd\7\13\2\2\u02fb\u02fc")
        buf.write("\7\u0080\2\2\u02fc\u02fe\7\u0081\2\2\u02fd\u02fb\3\2\2")
        buf.write("\2\u02fd\u02fe\3\2\2\2\u02fe9\3\2\2\2\u02ff\u0300\7\f")
        buf.write("\2\2\u0300\u0304\7\u0080\2\2\u0301\u0303\7x\2\2\u0302")
        buf.write("\u0301\3\2\2\2\u0303\u0306\3\2\2\2\u0304\u0302\3\2\2\2")
        buf.write("\u0304\u0305\3\2\2\2\u0305\u0308\3\2\2\2\u0306\u0304\3")
        buf.write("\2\2\2\u0307\u0309\5<\37\2\u0308\u0307\3\2\2\2\u0308\u0309")
        buf.write("\3\2\2\2\u0309\u030d\3\2\2\2\u030a\u030c\7x\2\2\u030b")
        buf.write("\u030a\3\2\2\2\u030c\u030f\3\2\2\2\u030d\u030b\3\2\2\2")
        buf.write("\u030d\u030e\3\2\2\2\u030e\u0311\3\2\2\2\u030f\u030d\3")
        buf.write("\2\2\2\u0310\u0312\5F$\2\u0311\u0310\3\2\2\2\u0312\u0313")
        buf.write("\3\2\2\2\u0313\u0311\3\2\2\2\u0313\u0314\3\2\2\2\u0314")
        buf.write("\u0318\3\2\2\2\u0315\u0317\7x\2\2\u0316\u0315\3\2\2\2")
        buf.write("\u0317\u031a\3\2\2\2\u0318\u0316\3\2\2\2\u0318\u0319\3")
        buf.write("\2\2\2\u0319\u031b\3\2\2\2\u031a\u0318\3\2\2\2\u031b\u031c")
        buf.write("\7\u0081\2\2\u031c;\3\2\2\2\u031d\u031e\5> \2\u031e=\3")
        buf.write("\2\2\2\u031f\u0320\7J\2\2\u0320\u0324\7\u0080\2\2\u0321")
        buf.write("\u0323\7x\2\2\u0322\u0321\3\2\2\2\u0323\u0326\3\2\2\2")
        buf.write("\u0324\u0322\3\2\2\2\u0324\u0325\3\2\2\2\u0325\u0328\3")
        buf.write("\2\2\2\u0326\u0324\3\2\2\2\u0327\u0329\5@!\2\u0328\u0327")
        buf.write("\3\2\2\2\u0328\u0329\3\2\2\2\u0329\u032d\3\2\2\2\u032a")
        buf.write("\u032c\7x\2\2\u032b\u032a\3\2\2\2\u032c\u032f\3\2\2\2")
        buf.write("\u032d\u032b\3\2\2\2\u032d\u032e\3\2\2\2\u032e\u0336\3")
        buf.write("\2\2\2\u032f\u032d\3\2\2\2\u0330\u0332\5P)\2\u0331\u0333")
        buf.write("\7\u0087\2\2\u0332\u0331\3\2\2\2\u0332\u0333\3\2\2\2\u0333")
        buf.write("\u0335\3\2\2\2\u0334\u0330\3\2\2\2\u0335\u0338\3\2\2\2")
        buf.write("\u0336\u0334\3\2\2\2\u0336\u0337\3\2\2\2\u0337\u033c\3")
        buf.write("\2\2\2\u0338\u0336\3\2\2\2\u0339\u033b\7x\2\2\u033a\u0339")
        buf.write("\3\2\2\2\u033b\u033e\3\2\2\2\u033c\u033a\3\2\2\2\u033c")
        buf.write("\u033d\3\2\2\2\u033d\u033f\3\2\2\2\u033e\u033c\3\2\2\2")
        buf.write("\u033f\u0340\7\u0081\2\2\u0340?\3\2\2\2\u0341\u0342\7")
        buf.write("I\2\2\u0342\u0346\7\u0080\2\2\u0343\u0345\7x\2\2\u0344")
        buf.write("\u0343\3\2\2\2\u0345\u0348\3\2\2\2\u0346\u0344\3\2\2\2")
        buf.write("\u0346\u0347\3\2\2\2\u0347\u0351\3\2\2\2\u0348\u0346\3")
        buf.write("\2\2\2\u0349\u034e\5B\"\2\u034a\u034b\7\u0087\2\2\u034b")
        buf.write("\u034d\5B\"\2\u034c\u034a\3\2\2\2\u034d\u0350\3\2\2\2")
        buf.write("\u034e\u034c\3\2\2\2\u034e\u034f\3\2\2\2\u034f\u0352\3")
        buf.write("\2\2\2\u0350\u034e\3\2\2\2\u0351\u0349\3\2\2\2\u0351\u0352")
        buf.write("\3\2\2\2\u0352\u0356\3\2\2\2\u0353\u0355\7x\2\2\u0354")
        buf.write("\u0353\3\2\2\2\u0355\u0358\3\2\2\2\u0356\u0354\3\2\2\2")
        buf.write("\u0356\u0357\3\2\2\2\u0357\u0359\3\2\2\2\u0358\u0356\3")
        buf.write("\2\2\2\u0359\u035a\7\u0081\2\2\u035aA\3\2\2\2\u035b\u035d")
        buf.write("\7x\2\2\u035c\u035b\3\2\2\2\u035d\u0360\3\2\2\2\u035e")
        buf.write("\u035c\3\2\2\2\u035e\u035f\3\2\2\2\u035f\u0361\3\2\2\2")
        buf.write("\u0360\u035e\3\2\2\2\u0361\u0379\5D#\2\u0362\u0366\7\u0080")
        buf.write("\2\2\u0363\u0365\7x\2\2\u0364\u0363\3\2\2\2\u0365\u0368")
        buf.write("\3\2\2\2\u0366\u0364\3\2\2\2\u0366\u0367\3\2\2\2\u0367")
        buf.write("\u036f\3\2\2\2\u0368\u0366\3\2\2\2\u0369\u036b\5P)\2\u036a")
        buf.write("\u036c\7\u0087\2\2\u036b\u036a\3\2\2\2\u036b\u036c\3\2")
        buf.write("\2\2\u036c\u036e\3\2\2\2\u036d\u0369\3\2\2\2\u036e\u0371")
        buf.write("\3\2\2\2\u036f\u036d\3\2\2\2\u036f\u0370\3\2\2\2\u0370")
        buf.write("\u0375\3\2\2\2\u0371\u036f\3\2\2\2\u0372\u0374\7x\2\2")
        buf.write("\u0373\u0372\3\2\2\2\u0374\u0377\3\2\2\2\u0375\u0373\3")
        buf.write("\2\2\2\u0375\u0376\3\2\2\2\u0376\u0378\3\2\2\2\u0377\u0375")
        buf.write("\3\2\2\2\u0378\u037a\7\u0081\2\2\u0379\u0362\3\2\2\2\u0379")
        buf.write("\u037a\3\2\2\2\u037aC\3\2\2\2\u037b\u037c\5\32\16\2\u037c")
        buf.write("E\3\2\2\2\u037d\u0381\5J&\2\u037e\u0380\7x\2\2\u037f\u037e")
        buf.write("\3\2\2\2\u0380\u0383\3\2\2\2\u0381\u037f\3\2\2\2\u0381")
        buf.write("\u0382\3\2\2\2\u0382\u0384\3\2\2\2\u0383\u0381\3\2\2\2")
        buf.write("\u0384\u0388\5H%\2\u0385\u0387\7x\2\2\u0386\u0385\3\2")
        buf.write("\2\2\u0387\u038a\3\2\2\2\u0388\u0386\3\2\2\2\u0388\u0389")
        buf.write("\3\2\2\2\u0389\u038b\3\2\2\2\u038a\u0388\3\2\2\2\u038b")
        buf.write("\u038c\5L\'\2\u038c\u0390\7\u0080\2\2\u038d\u038f\7x\2")
        buf.write("\2\u038e\u038d\3\2\2\2\u038f\u0392\3\2\2\2\u0390\u038e")
        buf.write("\3\2\2\2\u0390\u0391\3\2\2\2\u0391\u0393\3\2\2\2\u0392")
        buf.write("\u0390\3\2\2\2\u0393\u03a4\5N(\2\u0394\u0398\7~\2\2\u0395")
        buf.write("\u0397\7x\2\2\u0396\u0395\3\2\2\2\u0397\u039a\3\2\2\2")
        buf.write("\u0398\u0396\3\2\2\2\u0398\u0399\3\2\2\2\u0399\u03a1\3")
        buf.write("\2\2\2\u039a\u0398\3\2\2\2\u039b\u039d\5P)\2\u039c\u039e")
        buf.write("\7\u0087\2\2\u039d\u039c\3\2\2\2\u039d\u039e\3\2\2\2\u039e")
        buf.write("\u03a0\3\2\2\2\u039f\u039b\3\2\2\2\u03a0\u03a3\3\2\2\2")
        buf.write("\u03a1\u039f\3\2\2\2\u03a1\u03a2\3\2\2\2\u03a2\u03a5\3")
        buf.write("\2\2\2\u03a3\u03a1\3\2\2\2\u03a4\u0394\3\2\2\2\u03a4\u03a5")
        buf.write("\3\2\2\2\u03a5\u03a9\3\2\2\2\u03a6\u03a8\7x\2\2\u03a7")
        buf.write("\u03a6\3\2\2\2\u03a8\u03ab\3\2\2\2\u03a9\u03a7\3\2\2\2")
        buf.write("\u03a9\u03aa\3\2\2\2\u03aa\u03ac\3\2\2\2\u03ab\u03a9\3")
        buf.write("\2\2\2\u03ac\u03b0\7\u0081\2\2\u03ad\u03af\7x\2\2\u03ae")
        buf.write("\u03ad\3\2\2\2\u03af\u03b2\3\2\2\2\u03b0\u03ae\3\2\2\2")
        buf.write("\u03b0\u03b1\3\2\2\2\u03b1G\3\2\2\2\u03b2\u03b0\3\2\2")
        buf.write("\2\u03b3\u03b4\t\4\2\2\u03b4\u03b5\7}\2\2\u03b5I\3\2\2")
        buf.write("\2\u03b6\u03bb\5\32\16\2\u03b7\u03bb\7\u0086\2\2\u03b8")
        buf.write("\u03bb\7\u008f\2\2\u03b9\u03bb\7\u008a\2\2\u03ba\u03b6")
        buf.write("\3\2\2\2\u03ba\u03b7\3\2\2\2\u03ba\u03b8\3\2\2\2\u03ba")
        buf.write("\u03b9\3\2\2\2\u03bb\u03bc\3\2\2\2\u03bc\u03ba\3\2\2\2")
        buf.write("\u03bc\u03bd\3\2\2\2\u03bdK\3\2\2\2\u03be\u03c3\5\32\16")
        buf.write("\2\u03bf\u03c3\7\u0086\2\2\u03c0\u03c3\7\u008a\2\2\u03c1")
        buf.write("\u03c3\7\u008f\2\2\u03c2\u03be\3\2\2\2\u03c2\u03bf\3\2")
        buf.write("\2\2\u03c2\u03c0\3\2\2\2\u03c2\u03c1\3\2\2\2\u03c3\u03c4")
        buf.write("\3\2\2\2\u03c4\u03c2\3\2\2\2\u03c4\u03c5\3\2\2\2\u03c5")
        buf.write("M\3\2\2\2\u03c6\u03cb\5\32\16\2\u03c7\u03cb\7\u0086\2")
        buf.write("\2\u03c8\u03cb\7\u008f\2\2\u03c9\u03cb\7\u0088\2\2\u03ca")
        buf.write("\u03c6\3\2\2\2\u03ca\u03c7\3\2\2\2\u03ca\u03c8\3\2\2\2")
        buf.write("\u03ca\u03c9\3\2\2\2\u03cb\u03cc\3\2\2\2\u03cc\u03ca\3")
        buf.write("\2\2\2\u03cc\u03cd\3\2\2\2\u03cdO\3\2\2\2\u03ce\u03d0")
        buf.write("\7x\2\2\u03cf\u03ce\3\2\2\2\u03d0\u03d3\3\2\2\2\u03d1")
        buf.write("\u03cf\3\2\2\2\u03d1\u03d2\3\2\2\2\u03d2\u03d4\3\2\2\2")
        buf.write("\u03d3\u03d1\3\2\2\2\u03d4\u03d5\5R*\2\u03d5\u03d6\7\u008b")
        buf.write("\2\2\u03d6\u03d7\5T+\2\u03d7Q\3\2\2\2\u03d8\u03d9\5\32")
        buf.write("\16\2\u03d9S\3\2\2\2\u03da\u03df\7\u0092\2\2\u03db\u03df")
        buf.write("\7\u0093\2\2\u03dc\u03df\7z\2\2\u03dd\u03df\5\32\16\2")
        buf.write("\u03de\u03da\3\2\2\2\u03de\u03db\3\2\2\2\u03de\u03dc\3")
        buf.write("\2\2\2\u03de\u03dd\3\2\2\2\u03dfU\3\2\2\2\u03e0\u03e1")
        buf.write("\7\22\2\2\u03e1\u03e2\5X-\2\u03e2\u03e3\5&\24\2\u03e3")
        buf.write("W\3\2\2\2\u03e4\u03e5\t\5\2\2\u03e5Y\3\2\2\2\u03e6\u03e7")
        buf.write("\7\20\2\2\u03e7\u03e8\7\u0080\2\2\u03e8\u03ed\5^\60\2")
        buf.write("\u03e9\u03ea\7\u0087\2\2\u03ea\u03eb\7G\2\2\u03eb\u03ec")
        buf.write("\7\u008b\2\2\u03ec\u03ee\5\\/\2\u03ed\u03e9\3\2\2\2\u03ed")
        buf.write("\u03ee\3\2\2\2\u03ee\u03ef\3\2\2\2\u03ef\u03f0\7\u0081")
        buf.write("\2\2\u03f0[\3\2\2\2\u03f1\u03f2\7w\2\2\u03f2]\3\2\2\2")
        buf.write("\u03f3\u03f7\5\32\16\2\u03f4\u03f7\7\u0092\2\2\u03f5\u03f7")
        buf.write("\7\u0093\2\2\u03f6\u03f3\3\2\2\2\u03f6\u03f4\3\2\2\2\u03f6")
        buf.write("\u03f5\3\2\2\2\u03f7_\3\2\2\2\u03f8\u03f9\7+\2\2\u03f9")
        buf.write("\u03fa\7\u0080\2\2\u03fa\u03fb\5b\62\2\u03fb\u03fc\7\u0081")
        buf.write("\2\2\u03fca\3\2\2\2\u03fd\u0402\7y\2\2\u03fe\u03ff\7\u0087")
        buf.write("\2\2\u03ff\u0401\7y\2\2\u0400\u03fe\3\2\2\2\u0401\u0404")
        buf.write("\3\2\2\2\u0402\u0400\3\2\2\2\u0402\u0403\3\2\2\2\u0403")
        buf.write("c\3\2\2\2\u0404\u0402\3\2\2\2\u0405\u0407\5h\65\2\u0406")
        buf.write("\u0408\5f\64\2\u0407\u0406\3\2\2\2\u0407\u0408\3\2\2\2")
        buf.write("\u0408\u040c\3\2\2\2\u0409\u040b\7x\2\2\u040a\u0409\3")
        buf.write("\2\2\2\u040b\u040e\3\2\2\2\u040c\u040a\3\2\2\2\u040c\u040d")
        buf.write("\3\2\2\2\u040d\u0412\3\2\2\2\u040e\u040c\3\2\2\2\u040f")
        buf.write("\u0411\5t;\2\u0410\u040f\3\2\2\2\u0411\u0414\3\2\2\2\u0412")
        buf.write("\u0410\3\2\2\2\u0412\u0413\3\2\2\2\u0413\u0418\3\2\2\2")
        buf.write("\u0414\u0412\3\2\2\2\u0415\u0417\7x\2\2\u0416\u0415\3")
        buf.write("\2\2\2\u0417\u041a\3\2\2\2\u0418\u0416\3\2\2\2\u0418\u0419")
        buf.write("\3\2\2\2\u0419\u041e\3\2\2\2\u041a\u0418\3\2\2\2\u041b")
        buf.write("\u041d\5\u00e6t\2\u041c\u041b\3\2\2\2\u041d\u0420\3\2")
        buf.write("\2\2\u041e\u041c\3\2\2\2\u041e\u041f\3\2\2\2\u041f\u0424")
        buf.write("\3\2\2\2\u0420\u041e\3\2\2\2\u0421\u0423\7x\2\2\u0422")
        buf.write("\u0421\3\2\2\2\u0423\u0426\3\2\2\2\u0424\u0422\3\2\2\2")
        buf.write("\u0424\u0425\3\2\2\2\u0425e\3\2\2\2\u0426\u0424\3\2\2")
        buf.write("\2\u0427\u0428\7\u008b\2\2\u0428\u042f\t\3\2\2\u0429\u042b")
        buf.write("\7x\2\2\u042a\u0429\3\2\2\2\u042b\u042c\3\2\2\2\u042c")
        buf.write("\u042a\3\2\2\2\u042c\u042d\3\2\2\2\u042d\u0430\3\2\2\2")
        buf.write("\u042e\u0430\7\2\2\3\u042f\u042a\3\2\2\2\u042f\u042e\3")
        buf.write("\2\2\2\u0430g\3\2\2\2\u0431\u0433\7\u0089\2\2\u0432\u0434")
        buf.write("\5p9\2\u0433\u0432\3\2\2\2\u0433\u0434\3\2\2\2\u0434\u0435")
        buf.write("\3\2\2\2\u0435\u0437\5r:\2\u0436\u0438\5l\67\2\u0437\u0436")
        buf.write("\3\2\2\2\u0437\u0438\3\2\2\2\u0438\u0439\3\2\2\2\u0439")
        buf.write("\u043a\5j\66\2\u043a\u043b\7x\2\2\u043bi\3\2\2\2\u043c")
        buf.write("\u043d\7x\2\2\u043d\u043e\7\u0086\2\2\u043e\u0440\7\u0086")
        buf.write("\2\2\u043f\u0441\7\u0086\2\2\u0440\u043f\3\2\2\2\u0441")
        buf.write("\u0442\3\2\2\2\u0442\u0440\3\2\2\2\u0442\u0443\3\2\2\2")
        buf.write("\u0443k\3\2\2\2\u0444\u0445\7~\2\2\u0445\u0448\5n8\2\u0446")
        buf.write("\u0447\7\u008a\2\2\u0447\u0449\5n8\2\u0448\u0446\3\2\2")
        buf.write("\2\u0448\u0449\3\2\2\2\u0449m\3\2\2\2\u044a\u044e\5\32")
        buf.write("\16\2\u044b\u044e\7\u0092\2\2\u044c\u044e\7\u0093\2\2")
        buf.write("\u044d\u044a\3\2\2\2\u044d\u044b\3\2\2\2\u044d\u044c\3")
        buf.write("\2\2\2\u044eo\3\2\2\2\u044f\u0454\5\32\16\2\u0450\u0451")
        buf.write("\7\u0086\2\2\u0451\u0455\7}\2\2\u0452\u0453\7\u0090\2")
        buf.write("\2\u0453\u0455\7}\2\2\u0454\u0450\3\2\2\2\u0454\u0452")
        buf.write("\3\2\2\2\u0455q\3\2\2\2\u0456\u0457\5\32\16\2\u0457s\3")
        buf.write("\2\2\2\u0458\u045a\5\u008eH\2\u0459\u0458\3\2\2\2\u045a")
        buf.write("\u045d\3\2\2\2\u045b\u0459\3\2\2\2\u045b\u045c\3\2\2\2")
        buf.write("\u045c\u045e\3\2\2\2\u045d\u045b\3\2\2\2\u045e\u0460\5")
        buf.write("\u008cG\2\u045f\u0461\5v<\2\u0460\u045f\3\2\2\2\u0460")
        buf.write("\u0461\3\2\2\2\u0461\u0463\3\2\2\2\u0462\u0464\5\u008a")
        buf.write("F\2\u0463\u0462\3\2\2\2\u0463\u0464\3\2\2\2\u0464\u0466")
        buf.write("\3\2\2\2\u0465\u0467\5\u0088E\2\u0466\u0465\3\2\2\2\u0466")
        buf.write("\u0467\3\2\2\2\u0467\u046e\3\2\2\2\u0468\u046a\7x\2\2")
        buf.write("\u0469\u0468\3\2\2\2\u046a\u046b\3\2\2\2\u046b\u0469\3")
        buf.write("\2\2\2\u046b\u046c\3\2\2\2\u046c\u046f\3\2\2\2\u046d\u046f")
        buf.write("\7\2\2\3\u046e\u0469\3\2\2\2\u046e\u046d\3\2\2\2\u046f")
        buf.write("u\3\2\2\2\u0470\u0472\7~\2\2\u0471\u0473\5x=\2\u0472\u0471")
        buf.write("\3\2\2\2\u0472\u0473\3\2\2\2\u0473\u047d\3\2\2\2\u0474")
        buf.write("\u0475\7~\2\2\u0475\u0477\5\u0090I\2\u0476\u0478\5z>\2")
        buf.write("\u0477\u0476\3\2\2\2\u0477\u0478\3\2\2\2\u0478\u047d\3")
        buf.write("\2\2\2\u0479\u047a\7~\2\2\u047a\u047d\5~@\2\u047b\u047d")
        buf.write("\5\u0080A\2\u047c\u0470\3\2\2\2\u047c\u0474\3\2\2\2\u047c")
        buf.write("\u0479\3\2\2\2\u047c\u047b\3\2\2\2\u047dw\3\2\2\2\u047e")
        buf.write("\u047f\5*\26\2\u047fy\3\2\2\2\u0480\u0482\5|?\2\u0481")
        buf.write("\u0480\3\2\2\2\u0481\u0482\3\2\2\2\u0482\u0483\3\2\2\2")
        buf.write("\u0483\u0484\5*\26\2\u0484{\3\2\2\2\u0485\u0486\7\u0088")
        buf.write("\2\2\u0486\u0487\7\u0088\2\2\u0487}\3\2\2\2\u0488\u0489")
        buf.write("\5\32\16\2\u0489\177\3\2\2\2\u048a\u048b\5\u0082B\2\u048b")
        buf.write("\u048c\5\u0084C\2\u048c\u0081\3\2\2\2\u048d\u048e\t\6")
        buf.write("\2\2\u048e\u0083\3\2\2\2\u048f\u0490\7\u009d\2\2\u0490")
        buf.write("\u0085\3\2\2\2\u0491\u0493\5\32\16\2\u0492\u0491\3\2\2")
        buf.write("\2\u0493\u0494\3\2\2\2\u0494\u0492\3\2\2\2\u0494\u0495")
        buf.write("\3\2\2\2\u0495\u0499\3\2\2\2\u0496\u0499\7\u0092\2\2\u0497")
        buf.write("\u0499\7\u0093\2\2\u0498\u0492\3\2\2\2\u0498\u0496\3\2")
        buf.write("\2\2\u0498\u0497\3\2\2\2\u0499\u0087\3\2\2\2\u049a\u049b")
        buf.write("\7\u0084\2\2\u049b\u049c\5\u0086D\2\u049c\u0089\3\2\2")
        buf.write("\2\u049d\u049e\7\u008a\2\2\u049e\u049f\5\u0086D\2\u049f")
        buf.write("\u008b\3\2\2\2\u04a0\u04a1\5\32\16\2\u04a1\u008d\3\2\2")
        buf.write("\2\u04a2\u04a3\t\7\2\2\u04a3\u008f\3\2\2\2\u04a4\u04b7")
        buf.write("\5\u0092J\2\u04a5\u04b7\5\u0096L\2\u04a6\u04b7\5\u0094")
        buf.write("K\2\u04a7\u04b7\5\u0098M\2\u04a8\u04b7\5\u009aN\2\u04a9")
        buf.write("\u04b7\5\u009cO\2\u04aa\u04b7\5\u009eP\2\u04ab\u04b7\5")
        buf.write("\u00a0Q\2\u04ac\u04b7\5\u00a2R\2\u04ad\u04b7\5\u00aaV")
        buf.write("\2\u04ae\u04b7\5\u00b6\\\2\u04af\u04b7\5\u00c0a\2\u04b0")
        buf.write("\u04b7\5\u00c6d\2\u04b1\u04b7\5\u00dan\2\u04b2\u04b7\5")
        buf.write("\u00caf\2\u04b3\u04b7\5\u00a4S\2\u04b4\u04b7\5\u00a6T")
        buf.write("\2\u04b5\u04b7\5\u00a8U\2\u04b6\u04a4\3\2\2\2\u04b6\u04a5")
        buf.write("\3\2\2\2\u04b6\u04a6\3\2\2\2\u04b6\u04a7\3\2\2\2\u04b6")
        buf.write("\u04a8\3\2\2\2\u04b6\u04a9\3\2\2\2\u04b6\u04aa\3\2\2\2")
        buf.write("\u04b6\u04ab\3\2\2\2\u04b6\u04ac\3\2\2\2\u04b6\u04ad\3")
        buf.write("\2\2\2\u04b6\u04ae\3\2\2\2\u04b6\u04af\3\2\2\2\u04b6\u04b0")
        buf.write("\3\2\2\2\u04b6\u04b1\3\2\2\2\u04b6\u04b2\3\2\2\2\u04b6")
        buf.write("\u04b3\3\2\2\2\u04b6\u04b4\3\2\2\2\u04b6\u04b5\3\2\2\2")
        buf.write("\u04b7\u0091\3\2\2\2\u04b8\u04b9\7/\2\2\u04b9\u0093\3")
        buf.write("\2\2\2\u04ba\u04bb\7\60\2\2\u04bb\u0095\3\2\2\2\u04bc")
        buf.write("\u04bd\7\61\2\2\u04bd\u0097\3\2\2\2\u04be\u04bf\7\62\2")
        buf.write("\2\u04bf\u0099\3\2\2\2\u04c0\u04c1\7\63\2\2\u04c1\u009b")
        buf.write("\3\2\2\2\u04c2\u04c3\7\64\2\2\u04c3\u009d\3\2\2\2\u04c4")
        buf.write("\u04c5\7\65\2\2\u04c5\u009f\3\2\2\2\u04c6\u04c7\7\66\2")
        buf.write("\2\u04c7\u00a1\3\2\2\2\u04c8\u04c9\7\67\2\2\u04c9\u00a3")
        buf.write("\3\2\2\2\u04ca\u04cb\79\2\2\u04cb\u00a5\3\2\2\2\u04cc")
        buf.write("\u04cd\7;\2\2\u04cd\u00a7\3\2\2\2\u04ce\u04cf\7<\2\2\u04cf")
        buf.write("\u00a9\3\2\2\2\u04d0\u04d9\7>\2\2\u04d1\u04d2\7\u0080")
        buf.write("\2\2\u04d2\u04d5\5\u00acW\2\u04d3\u04d4\7\u0087\2\2\u04d4")
        buf.write("\u04d6\5\u00aeX\2\u04d5\u04d3\3\2\2\2\u04d5\u04d6\3\2")
        buf.write("\2\2\u04d6\u04d7\3\2\2\2\u04d7\u04d8\7\u0081\2\2\u04d8")
        buf.write("\u04da\3\2\2\2\u04d9\u04d1\3\2\2\2\u04d9\u04da\3\2\2\2")
        buf.write("\u04da\u00ab\3\2\2\2\u04db\u04dc\t\b\2\2\u04dc\u00ad\3")
        buf.write("\2\2\2\u04dd\u04de\7E\2\2\u04de\u04df\7\u008b\2\2\u04df")
        buf.write("\u04e4\5\u00b0Y\2\u04e0\u04e1\7\u0087\2\2\u04e1\u04e3")
        buf.write("\5\u00b0Y\2\u04e2\u04e0\3\2\2\2\u04e3\u04e6\3\2\2\2\u04e4")
        buf.write("\u04e2\3\2\2\2\u04e4\u04e5\3\2\2\2\u04e5\u00af\3\2\2\2")
        buf.write("\u04e6\u04e4\3\2\2\2\u04e7\u04e9\5\u00b4[\2\u04e8\u04e7")
        buf.write("\3\2\2\2\u04e8\u04e9\3\2\2\2\u04e9\u04ea\3\2\2\2\u04ea")
        buf.write("\u04eb\5\u00b2Z\2\u04eb\u00b1\3\2\2\2\u04ec\u04f0\5\32")
        buf.write("\16\2\u04ed\u04f0\7\u0092\2\2\u04ee\u04f0\7\u0093\2\2")
        buf.write("\u04ef\u04ec\3\2\2\2\u04ef\u04ed\3\2\2\2\u04ef\u04ee\3")
        buf.write("\2\2\2\u04f0\u00b3\3\2\2\2\u04f1\u04f2\5\32\16\2\u04f2")
        buf.write("\u04f3\7~\2\2\u04f3\u00b5\3\2\2\2\u04f4\u04f9\7?\2\2\u04f5")
        buf.write("\u04f6\7\u0080\2\2\u04f6\u04f7\5\u00b8]\2\u04f7\u04f8")
        buf.write("\7\u0081\2\2\u04f8\u04fa\3\2\2\2\u04f9\u04f5\3\2\2\2\u04f9")
        buf.write("\u04fa\3\2\2\2\u04fa\u00b7\3\2\2\2\u04fb\u04fc\7E\2\2")
        buf.write("\u04fc\u04fd\7\u008b\2\2\u04fd\u0502\5\u00ba^\2\u04fe")
        buf.write("\u04ff\7\u0087\2\2\u04ff\u0501\5\u00ba^\2\u0500\u04fe")
        buf.write("\3\2\2\2\u0501\u0504\3\2\2\2\u0502\u0500\3\2\2\2\u0502")
        buf.write("\u0503\3\2\2\2\u0503\u00b9\3\2\2\2\u0504\u0502\3\2\2\2")
        buf.write("\u0505\u0507\5\u00be`\2\u0506\u0505\3\2\2\2\u0506\u0507")
        buf.write("\3\2\2\2\u0507\u0508\3\2\2\2\u0508\u0509\5\u00bc_\2\u0509")
        buf.write("\u00bb\3\2\2\2\u050a\u050e\5\32\16\2\u050b\u050e\7\u0092")
        buf.write("\2\2\u050c\u050e\7\u0093\2\2\u050d\u050a\3\2\2\2\u050d")
        buf.write("\u050b\3\2\2\2\u050d\u050c\3\2\2\2\u050e\u00bd\3\2\2\2")
        buf.write("\u050f\u0510\7z\2\2\u0510\u0511\7~\2\2\u0511\u00bf\3\2")
        buf.write("\2\2\u0512\u0513\7@\2\2\u0513\u0514\7\u0080\2\2\u0514")
        buf.write("\u0515\5\u00c2b\2\u0515\u0516\7\u0081\2\2\u0516\u00c1")
        buf.write("\3\2\2\2\u0517\u051c\5\u00c4c\2\u0518\u0519\7\u0087\2")
        buf.write("\2\u0519\u051b\5\u00c4c\2\u051a\u0518\3\2\2\2\u051b\u051e")
        buf.write("\3\2\2\2\u051c\u051a\3\2\2\2\u051c\u051d\3\2\2\2\u051d")
        buf.write("\u00c3\3\2\2\2\u051e\u051c\3\2\2\2\u051f\u0520\5\32\16")
        buf.write("\2\u0520\u00c5\3\2\2\2\u0521\u0526\7A\2\2\u0522\u0523")
        buf.write("\7\u0080\2\2\u0523\u0524\5\u00c8e\2\u0524\u0525\7\u0081")
        buf.write("\2\2\u0525\u0527\3\2\2\2\u0526\u0522\3\2\2\2\u0526\u0527")
        buf.write("\3\2\2\2\u0527\u00c7\3\2\2\2\u0528\u0529\7w\2\2\u0529")
        buf.write("\u00c9\3\2\2\2\u052a\u052f\5\u00ccg\2\u052b\u052c\7\u0080")
        buf.write("\2\2\u052c\u052d\5\u00ceh\2\u052d\u052e\7\u0081\2\2\u052e")
        buf.write("\u0530\3\2\2\2\u052f\u052b\3\2\2\2\u052f\u0530\3\2\2\2")
        buf.write("\u0530\u00cb\3\2\2\2\u0531\u0532\t\t\2\2\u0532\u00cd\3")
        buf.write("\2\2\2\u0533\u0538\5\u00d0i\2\u0534\u0535\7\u0087\2\2")
        buf.write("\u0535\u0537\5\u00d0i\2\u0536\u0534\3\2\2\2\u0537\u053a")
        buf.write("\3\2\2\2\u0538\u0536\3\2\2\2\u0538\u0539\3\2\2\2\u0539")
        buf.write("\u00cf\3\2\2\2\u053a\u0538\3\2\2\2\u053b\u053c\5\u00d4")
        buf.write("k\2\u053c\u053d\5\u00d2j\2\u053d\u053e\5\u00d6l\2\u053e")
        buf.write("\u00d1\3\2\2\2\u053f\u0540\7{\2\2\u0540\u00d3\3\2\2\2")
        buf.write("\u0541\u0542\5\32\16\2\u0542\u0543\7\u008b\2\2\u0543\u00d5")
        buf.write("\3\2\2\2\u0544\u0546\5\u00d8m\2\u0545\u0544\3\2\2\2\u0546")
        buf.write("\u0549\3\2\2\2\u0547\u0545\3\2\2\2\u0547\u0548\3\2\2\2")
        buf.write("\u0548\u00d7\3\2\2\2\u0549\u0547\3\2\2\2\u054a\u054b\7")
        buf.write("\u0091\2\2\u054b\u054c\5\32\16\2\u054c\u00d9\3\2\2\2\u054d")
        buf.write("\u054e\5\u00dco\2\u054e\u0550\7\u0080\2\2\u054f\u0551")
        buf.write("\5\u00dep\2\u0550\u054f\3\2\2\2\u0550\u0551\3\2\2\2\u0551")
        buf.write("\u0554\3\2\2\2\u0552\u0555\5\u00e0q\2\u0553\u0555\5\u00e2")
        buf.write("r\2\u0554\u0552\3\2\2\2\u0554\u0553\3\2\2\2\u0555\u0557")
        buf.write("\3\2\2\2\u0556\u0558\5\u00e4s\2\u0557\u0556\3\2\2\2\u0557")
        buf.write("\u0558\3\2\2\2\u0558\u0559\3\2\2\2\u0559\u055a\7\u0081")
        buf.write("\2\2\u055a\u00db\3\2\2\2\u055b\u055c\t\n\2\2\u055c\u00dd")
        buf.write("\3\2\2\2\u055d\u055e\t\13\2\2\u055e\u00df\3\2\2\2\u055f")
        buf.write("\u0560\5\36\20\2\u0560\u00e1\3\2\2\2\u0561\u0562\5\34")
        buf.write("\17\2\u0562\u00e3\3\2\2\2\u0563\u0564\7\u0086\2\2\u0564")
        buf.write("\u0565\7}\2\2\u0565\u0566\5\32\16\2\u0566\u00e5\3\2\2")
        buf.write("\2\u0567\u0577\5\u00e8u\2\u0568\u0577\5\u0114\u008b\2")
        buf.write("\u0569\u0577\5\u011a\u008e\2\u056a\u0577\5\u014c\u00a7")
        buf.write("\2\u056b\u0577\5\u0150\u00a9\2\u056c\u0577\5\u0152\u00aa")
        buf.write("\2\u056d\u0577\5\u0154\u00ab\2\u056e\u0577\5\u0158\u00ad")
        buf.write("\2\u056f\u0577\5\u015a\u00ae\2\u0570\u0577\5\u015e\u00b0")
        buf.write("\2\u0571\u0577\5\u0160\u00b1\2\u0572\u0577\5\u0162\u00b2")
        buf.write("\2\u0573\u0577\5\u0164\u00b3\2\u0574\u0577\5\u0166\u00b4")
        buf.write("\2\u0575\u0577\7x\2\2\u0576\u0567\3\2\2\2\u0576\u0568")
        buf.write("\3\2\2\2\u0576\u0569\3\2\2\2\u0576\u056a\3\2\2\2\u0576")
        buf.write("\u056b\3\2\2\2\u0576\u056c\3\2\2\2\u0576\u056d\3\2\2\2")
        buf.write("\u0576\u056e\3\2\2\2\u0576\u056f\3\2\2\2\u0576\u0570\3")
        buf.write("\2\2\2\u0576\u0571\3\2\2\2\u0576\u0572\3\2\2\2\u0576\u0573")
        buf.write("\3\2\2\2\u0576\u0574\3\2\2\2\u0576\u0575\3\2\2\2\u0577")
        buf.write("\u00e7\3\2\2\2\u0578\u0592\7\3\2\2\u0579\u0588\7\u0080")
        buf.write("\2\2\u057a\u0587\5\u0108\u0085\2\u057b\u0587\5\u010a\u0086")
        buf.write("\2\u057c\u0587\5\u010c\u0087\2\u057d\u0587\5\u010e\u0088")
        buf.write("\2\u057e\u0587\5\u0110\u0089\2\u057f\u0587\5\u0112\u008a")
        buf.write("\2\u0580\u0587\5\u0100\u0081\2\u0581\u0587\5\u00f2z\2")
        buf.write("\u0582\u0587\5\u00ecw\2\u0583\u0587\5\u00eav\2\u0584\u0587")
        buf.write("\7x\2\2\u0585\u0587\7\u0087\2\2\u0586\u057a\3\2\2\2\u0586")
        buf.write("\u057b\3\2\2\2\u0586\u057c\3\2\2\2\u0586\u057d\3\2\2\2")
        buf.write("\u0586\u057e\3\2\2\2\u0586\u057f\3\2\2\2\u0586\u0580\3")
        buf.write("\2\2\2\u0586\u0581\3\2\2\2\u0586\u0582\3\2\2\2\u0586\u0583")
        buf.write("\3\2\2\2\u0586\u0584\3\2\2\2\u0586\u0585\3\2\2\2\u0587")
        buf.write("\u058a\3\2\2\2\u0588\u0586\3\2\2\2\u0588\u0589\3\2\2\2")
        buf.write("\u0589\u058e\3\2\2\2\u058a\u0588\3\2\2\2\u058b\u058d\7")
        buf.write("x\2\2\u058c\u058b\3\2\2\2\u058d\u0590\3\2\2\2\u058e\u058c")
        buf.write("\3\2\2\2\u058e\u058f\3\2\2\2\u058f\u0591\3\2\2\2\u0590")
        buf.write("\u058e\3\2\2\2\u0591\u0593\7\u0081\2\2\u0592\u0579\3\2")
        buf.write("\2\2\u0592\u0593\3\2\2\2\u0593\u0597\3\2\2\2\u0594\u0596")
        buf.write("\7x\2\2\u0595\u0594\3\2\2\2\u0596\u0599\3\2\2\2\u0597")
        buf.write("\u0595\3\2\2\2\u0597\u0598\3\2\2\2\u0598\u00e9\3\2\2\2")
        buf.write("\u0599\u0597\3\2\2\2\u059a\u059b\7_\2\2\u059b\u059f\7")
        buf.write("~\2\2\u059c\u059e\7x\2\2\u059d\u059c\3\2\2\2\u059e\u05a1")
        buf.write("\3\2\2\2\u059f\u059d\3\2\2\2\u059f\u05a0\3\2\2\2\u05a0")
        buf.write("\u05a2\3\2\2\2\u05a1\u059f\3\2\2\2\u05a2\u05ad\5\u00f0")
        buf.write("y\2\u05a3\u05a7\7\u0087\2\2\u05a4\u05a6\7x\2\2\u05a5\u05a4")
        buf.write("\3\2\2\2\u05a6\u05a9\3\2\2\2\u05a7\u05a5\3\2\2\2\u05a7")
        buf.write("\u05a8\3\2\2\2\u05a8\u05aa\3\2\2\2\u05a9\u05a7\3\2\2\2")
        buf.write("\u05aa\u05ac\5\u00f0y\2\u05ab\u05a3\3\2\2\2\u05ac\u05af")
        buf.write("\3\2\2\2\u05ad\u05ab\3\2\2\2\u05ad\u05ae\3\2\2\2\u05ae")
        buf.write("\u00eb\3\2\2\2\u05af\u05ad\3\2\2\2\u05b0\u05b1\7^\2\2")
        buf.write("\u05b1\u05b2\7~\2\2\u05b2\u05b7\5\u00eex\2\u05b3\u05b4")
        buf.write("\7\u0087\2\2\u05b4\u05b6\5\u00eex\2\u05b5\u05b3\3\2\2")
        buf.write("\2\u05b6\u05b9\3\2\2\2\u05b7\u05b5\3\2\2\2\u05b7\u05b8")
        buf.write("\3\2\2\2\u05b8\u00ed\3\2\2\2\u05b9\u05b7\3\2\2\2\u05ba")
        buf.write("\u05bb\t\3\2\2\u05bb\u00ef\3\2\2\2\u05bc\u05bd\t\3\2\2")
        buf.write("\u05bd\u00f1\3\2\2\2\u05be\u05bf\7c\2\2\u05bf\u05c0\7")
        buf.write("~\2\2\u05c0\u05c5\5\u00f4{\2\u05c1\u05c2\7\u0087\2\2\u05c2")
        buf.write("\u05c4\5\u00f4{\2\u05c3\u05c1\3\2\2\2\u05c4\u05c7\3\2")
        buf.write("\2\2\u05c5\u05c3\3\2\2\2\u05c5\u05c6\3\2\2\2\u05c6\u00f3")
        buf.write("\3\2\2\2\u05c7\u05c5\3\2\2\2\u05c8\u05d5\5\u00f6|\2\u05c9")
        buf.write("\u05d1\7\u0080\2\2\u05ca\u05d0\5\u00f8}\2\u05cb\u05d0")
        buf.write("\5\u00fc\177\2\u05cc\u05d0\5\u00fe\u0080\2\u05cd\u05d0")
        buf.write("\7x\2\2\u05ce\u05d0\7\u0087\2\2\u05cf\u05ca\3\2\2\2\u05cf")
        buf.write("\u05cb\3\2\2\2\u05cf\u05cc\3\2\2\2\u05cf\u05cd\3\2\2\2")
        buf.write("\u05cf\u05ce\3\2\2\2\u05d0\u05d3\3\2\2\2\u05d1\u05cf\3")
        buf.write("\2\2\2\u05d1\u05d2\3\2\2\2\u05d2\u05d4\3\2\2\2\u05d3\u05d1")
        buf.write("\3\2\2\2\u05d4\u05d6\7\u0081\2\2\u05d5\u05c9\3\2\2\2\u05d5")
        buf.write("\u05d6\3\2\2\2\u05d6\u00f5\3\2\2\2\u05d7\u05d8\5\32\16")
        buf.write("\2\u05d8\u00f7\3\2\2\2\u05d9\u05da\7d\2\2\u05da\u05db")
        buf.write("\7~\2\2\u05db\u05dc\5\u00fa~\2\u05dc\u00f9\3\2\2\2\u05dd")
        buf.write("\u05de\t\f\2\2\u05de\u00fb\3\2\2\2\u05df\u05e0\7l\2\2")
        buf.write("\u05e0\u05e1\7~\2\2\u05e1\u05e2\7z\2\2\u05e2\u00fd\3\2")
        buf.write("\2\2\u05e3\u05e4\7s\2\2\u05e4\u05e5\7~\2\2\u05e5\u05e6")
        buf.write("\5 \21\2\u05e6\u00ff\3\2\2\2\u05e7\u05e8\7m\2\2\u05e8")
        buf.write("\u05e9\7~\2\2\u05e9\u05ee\5\u0102\u0082\2\u05ea\u05eb")
        buf.write("\7\u0087\2\2\u05eb\u05ed\5\u0102\u0082\2\u05ec\u05ea\3")
        buf.write("\2\2\2\u05ed\u05f0\3\2\2\2\u05ee\u05ec\3\2\2\2\u05ee\u05ef")
        buf.write("\3\2\2\2\u05ef\u0101\3\2\2\2\u05f0\u05ee\3\2\2\2\u05f1")
        buf.write("\u05f3\5\u0104\u0083\2\u05f2\u05f4\5\u0106\u0084\2\u05f3")
        buf.write("\u05f2\3\2\2\2\u05f3\u05f4\3\2\2\2\u05f4\u05f5\3\2\2\2")
        buf.write("\u05f5\u05f6\7\u0080\2\2\u05f6\u05f7\5 \21\2\u05f7\u05f8")
        buf.write("\7\u0081\2\2\u05f8\u0103\3\2\2\2\u05f9\u05fa\5\32\16\2")
        buf.write("\u05fa\u0105\3\2\2\2\u05fb\u05fc\t\3\2\2\u05fc\u0107\3")
        buf.write("\2\2\2\u05fd\u05fe\7n\2\2\u05fe\u05ff\7~\2\2\u05ff\u0603")
        buf.write("\5 \21\2\u0600\u0602\7x\2\2\u0601\u0600\3\2\2\2\u0602")
        buf.write("\u0605\3\2\2\2\u0603\u0601\3\2\2\2\u0603\u0604\3\2\2\2")
        buf.write("\u0604\u0109\3\2\2\2\u0605\u0603\3\2\2\2\u0606\u0607\7")
        buf.write("o\2\2\u0607\u0608\7~\2\2\u0608\u060c\5 \21\2\u0609\u060b")
        buf.write("\7x\2\2\u060a\u0609\3\2\2\2\u060b\u060e\3\2\2\2\u060c")
        buf.write("\u060a\3\2\2\2\u060c\u060d\3\2\2\2\u060d\u010b\3\2\2\2")
        buf.write("\u060e\u060c\3\2\2\2\u060f\u0610\7p\2\2\u0610\u0611\7")
        buf.write("~\2\2\u0611\u0615\5 \21\2\u0612\u0614\7x\2\2\u0613\u0612")
        buf.write("\3\2\2\2\u0614\u0617\3\2\2\2\u0615\u0613\3\2\2\2\u0615")
        buf.write("\u0616\3\2\2\2\u0616\u010d\3\2\2\2\u0617\u0615\3\2\2\2")
        buf.write("\u0618\u0619\7q\2\2\u0619\u061a\7~\2\2\u061a\u061e\5 ")
        buf.write("\21\2\u061b\u061d\7x\2\2\u061c\u061b\3\2\2\2\u061d\u0620")
        buf.write("\3\2\2\2\u061e\u061c\3\2\2\2\u061e\u061f\3\2\2\2\u061f")
        buf.write("\u010f\3\2\2\2\u0620\u061e\3\2\2\2\u0621\u0622\7r\2\2")
        buf.write("\u0622\u0623\7~\2\2\u0623\u0627\5 \21\2\u0624\u0626\7")
        buf.write("x\2\2\u0625\u0624\3\2\2\2\u0626\u0629\3\2\2\2\u0627\u0625")
        buf.write("\3\2\2\2\u0627\u0628\3\2\2\2\u0628\u0111\3\2\2\2\u0629")
        buf.write("\u0627\3\2\2\2\u062a\u062b\7s\2\2\u062b\u062c\7~\2\2\u062c")
        buf.write("\u0630\5 \21\2\u062d\u062f\7x\2\2\u062e\u062d\3\2\2\2")
        buf.write("\u062f\u0632\3\2\2\2\u0630\u062e\3\2\2\2\u0630\u0631\3")
        buf.write("\2\2\2\u0631\u0113\3\2\2\2\u0632\u0630\3\2\2\2\u0633\u0642")
        buf.write("\7\t\2\2\u0634\u063e\7\u0080\2\2\u0635\u063f\5\u0116\u008c")
        buf.write("\2\u0636\u063b\5\u0118\u008d\2\u0637\u0638\7\u0087\2\2")
        buf.write("\u0638\u063a\5\u0118\u008d\2\u0639\u0637\3\2\2\2\u063a")
        buf.write("\u063d\3\2\2\2\u063b\u0639\3\2\2\2\u063b\u063c\3\2\2\2")
        buf.write("\u063c\u063f\3\2\2\2\u063d\u063b\3\2\2\2\u063e\u0635\3")
        buf.write("\2\2\2\u063e\u0636\3\2\2\2\u063f\u0640\3\2\2\2\u0640\u0641")
        buf.write("\7\u0081\2\2\u0641\u0643\3\2\2\2\u0642\u0634\3\2\2\2\u0642")
        buf.write("\u0643\3\2\2\2\u0643\u0115\3\2\2\2\u0644\u0645\7\u008f")
        buf.write("\2\2\u0645\u0117\3\2\2\2\u0646\u0647\5\32\16\2\u0647\u0119")
        buf.write("\3\2\2\2\u0648\u064b\7\n\2\2\u0649\u064a\7\u0088\2\2\u064a")
        buf.write("\u064c\5\u0120\u0091\2\u064b\u0649\3\2\2\2\u064b\u064c")
        buf.write("\3\2\2\2\u064c\u0651\3\2\2\2\u064d\u064e\7\u0080\2\2\u064e")
        buf.write("\u064f\5\u011c\u008f\2\u064f\u0650\7\u0081\2\2\u0650\u0652")
        buf.write("\3\2\2\2\u0651\u064d\3\2\2\2\u0651\u0652\3\2\2\2\u0652")
        buf.write("\u011b\3\2\2\2\u0653\u0659\5\u011e\u0090\2\u0654\u0658")
        buf.write("\5\u0146\u00a4\2\u0655\u0658\7x\2\2\u0656\u0658\7\u0087")
        buf.write("\2\2\u0657\u0654\3\2\2\2\u0657\u0655\3\2\2\2\u0657\u0656")
        buf.write("\3\2\2\2\u0658\u065b\3\2\2\2\u0659\u0657\3\2\2\2\u0659")
        buf.write("\u065a\3\2\2\2\u065a\u011d\3\2\2\2\u065b\u0659\3\2\2\2")
        buf.write("\u065c\u0669\5\u0130\u0099\2\u065d\u0669\5\u0122\u0092")
        buf.write("\2\u065e\u0669\5\u0134\u009b\2\u065f\u0669\5\u0124\u0093")
        buf.write("\2\u0660\u0669\5\u0126\u0094\2\u0661\u0669\5\u0128\u0095")
        buf.write("\2\u0662\u0669\5\u012a\u0096\2\u0663\u0669\5\u012c\u0097")
        buf.write("\2\u0664\u0669\5\u012e\u0098\2\u0665\u0669\5\u013e\u00a0")
        buf.write("\2\u0666\u0669\7x\2\2\u0667\u0669\7\u0087\2\2\u0668\u065c")
        buf.write("\3\2\2\2\u0668\u065d\3\2\2\2\u0668\u065e\3\2\2\2\u0668")
        buf.write("\u065f\3\2\2\2\u0668\u0660\3\2\2\2\u0668\u0661\3\2\2\2")
        buf.write("\u0668\u0662\3\2\2\2\u0668\u0663\3\2\2\2\u0668\u0664\3")
        buf.write("\2\2\2\u0668\u0665\3\2\2\2\u0668\u0666\3\2\2\2\u0668\u0667")
        buf.write("\3\2\2\2\u0669\u066c\3\2\2\2\u066a\u0668\3\2\2\2\u066a")
        buf.write("\u066b\3\2\2\2\u066b\u011f\3\2\2\2\u066c\u066a\3\2\2\2")
        buf.write("\u066d\u066e\5\32\16\2\u066e\u0121\3\2\2\2\u066f\u0670")
        buf.write("\7k\2\2\u0670\u0671\7~\2\2\u0671\u0675\7w\2\2\u0672\u0674")
        buf.write("\7x\2\2\u0673\u0672\3\2\2\2\u0674\u0677\3\2\2\2\u0675")
        buf.write("\u0673\3\2\2\2\u0675\u0676\3\2\2\2\u0676\u0123\3\2\2\2")
        buf.write("\u0677\u0675\3\2\2\2\u0678\u0679\7h\2\2\u0679\u067d\5")
        buf.write("&\24\2\u067a\u067c\7x\2\2\u067b\u067a\3\2\2\2\u067c\u067f")
        buf.write("\3\2\2\2\u067d\u067b\3\2\2\2\u067d\u067e\3\2\2\2\u067e")
        buf.write("\u0125\3\2\2\2\u067f\u067d\3\2\2\2\u0680\u0682\7g\2\2")
        buf.write("\u0681\u0683\7~\2\2\u0682\u0681\3\2\2\2\u0682\u0683\3")
        buf.write("\2\2\2\u0683\u0684\3\2\2\2\u0684\u0688\5&\24\2\u0685\u0687")
        buf.write("\7x\2\2\u0686\u0685\3\2\2\2\u0687\u068a\3\2\2\2\u0688")
        buf.write("\u0686\3\2\2\2\u0688\u0689\3\2\2\2\u0689\u0127\3\2\2\2")
        buf.write("\u068a\u0688\3\2\2\2\u068b\u068d\7M\2\2\u068c\u068e\7")
        buf.write("~\2\2\u068d\u068c\3\2\2\2\u068d\u068e\3\2\2\2\u068e\u068f")
        buf.write("\3\2\2\2\u068f\u0693\5&\24\2\u0690\u0692\7x\2\2\u0691")
        buf.write("\u0690\3\2\2\2\u0692\u0695\3\2\2\2\u0693\u0691\3\2\2\2")
        buf.write("\u0693\u0694\3\2\2\2\u0694\u0129\3\2\2\2\u0695\u0693\3")
        buf.write("\2\2\2\u0696\u0698\7L\2\2\u0697\u0699\7~\2\2\u0698\u0697")
        buf.write("\3\2\2\2\u0698\u0699\3\2\2\2\u0699\u069a\3\2\2\2\u069a")
        buf.write("\u069e\5&\24\2\u069b\u069d\7x\2\2\u069c\u069b\3\2\2\2")
        buf.write("\u069d\u06a0\3\2\2\2\u069e\u069c\3\2\2\2\u069e\u069f\3")
        buf.write("\2\2\2\u069f\u012b\3\2\2\2\u06a0\u069e\3\2\2\2\u06a1\u06a2")
        buf.write("\7o\2\2\u06a2\u06a3\7~\2\2\u06a3\u06a7\5 \21\2\u06a4\u06a6")
        buf.write("\7x\2\2\u06a5\u06a4\3\2\2\2\u06a6\u06a9\3\2\2\2\u06a7")
        buf.write("\u06a5\3\2\2\2\u06a7\u06a8\3\2\2\2\u06a8\u012d\3\2\2\2")
        buf.write("\u06a9\u06a7\3\2\2\2\u06aa\u06ab\7e\2\2\u06ab\u06ac\7")
        buf.write("~\2\2\u06ac\u06b0\5\32\16\2\u06ad\u06af\7x\2\2\u06ae\u06ad")
        buf.write("\3\2\2\2\u06af\u06b2\3\2\2\2\u06b0\u06ae\3\2\2\2\u06b0")
        buf.write("\u06b1\3\2\2\2\u06b1\u012f\3\2\2\2\u06b2\u06b0\3\2\2\2")
        buf.write("\u06b3\u06b4\7s\2\2\u06b4\u06b5\7~\2\2\u06b5\u06b7\5 ")
        buf.write("\21\2\u06b6\u06b8\5\u0132\u009a\2\u06b7\u06b6\3\2\2\2")
        buf.write("\u06b7\u06b8\3\2\2\2\u06b8\u06bc\3\2\2\2\u06b9\u06bb\7")
        buf.write("x\2\2\u06ba\u06b9\3\2\2\2\u06bb\u06be\3\2\2\2\u06bc\u06ba")
        buf.write("\3\2\2\2\u06bc\u06bd\3\2\2\2\u06bd\u0131\3\2\2\2\u06be")
        buf.write("\u06bc\3\2\2\2\u06bf\u06c0\5$\23\2\u06c0\u0133\3\2\2\2")
        buf.write("\u06c1\u06c2\7i\2\2\u06c2\u06c3\7\u0080\2\2\u06c3\u06c8")
        buf.write("\5\u0136\u009c\2\u06c4\u06c5\7\u0087\2\2\u06c5\u06c7\5")
        buf.write("\u0136\u009c\2\u06c6\u06c4\3\2\2\2\u06c7\u06ca\3\2\2\2")
        buf.write("\u06c8\u06c6\3\2\2\2\u06c8\u06c9\3\2\2\2\u06c9\u06cb\3")
        buf.write("\2\2\2\u06ca\u06c8\3\2\2\2\u06cb\u06cc\7\u0081\2\2\u06cc")
        buf.write("\u0135\3\2\2\2\u06cd\u06d1\5\u0138\u009d\2\u06ce\u06cf")
        buf.write("\7~\2\2\u06cf\u06d2\5\u013a\u009e\2\u06d0\u06d2\5\u013c")
        buf.write("\u009f\2\u06d1\u06ce\3\2\2\2\u06d1\u06d0\3\2\2\2\u06d1")
        buf.write("\u06d2\3\2\2\2\u06d2\u0137\3\2\2\2\u06d3\u06d4\t\r\2\2")
        buf.write("\u06d4\u0139\3\2\2\2\u06d5\u06d6\5\36\20\2\u06d6\u013b")
        buf.write("\3\2\2\2\u06d7\u06d8\5\34\17\2\u06d8\u013d\3\2\2\2\u06d9")
        buf.write("\u06da\7f\2\2\u06da\u06db\7~\2\2\u06db\u06df\5\u0140\u00a1")
        buf.write("\2\u06dc\u06de\7x\2\2\u06dd\u06dc\3\2\2\2\u06de\u06e1")
        buf.write("\3\2\2\2\u06df\u06dd\3\2\2\2\u06df\u06e0\3\2\2\2\u06e0")
        buf.write("\u013f\3\2\2\2\u06e1\u06df\3\2\2\2\u06e2\u06e3\7j\2\2")
        buf.write("\u06e3\u06e6\5\u0142\u00a2\2\u06e4\u06e5\7u\2\2\u06e5")
        buf.write("\u06e7\5\u0144\u00a3\2\u06e6\u06e4\3\2\2\2\u06e6\u06e7")
        buf.write("\3\2\2\2\u06e7\u0141\3\2\2\2\u06e8\u06e9\5\32\16\2\u06e9")
        buf.write("\u0143\3\2\2\2\u06ea\u06eb\5\32\16\2\u06eb\u0145\3\2\2")
        buf.write("\2\u06ec\u06ed\7c\2\2\u06ed\u06f1\7~\2\2\u06ee\u06f2\5")
        buf.write("\u0148\u00a5\2\u06ef\u06f2\7\u0087\2\2\u06f0\u06f2\7x")
        buf.write("\2\2\u06f1\u06ee\3\2\2\2\u06f1\u06ef\3\2\2\2\u06f1\u06f0")
        buf.write("\3\2\2\2\u06f2\u06f3\3\2\2\2\u06f3\u06f1\3\2\2\2\u06f3")
        buf.write("\u06f4\3\2\2\2\u06f4\u0147\3\2\2\2\u06f5\u06f6\5\u014a")
        buf.write("\u00a6\2\u06f6\u06f7\7\u0080\2\2\u06f7\u06f8\5\u011c\u008f")
        buf.write("\2\u06f8\u06f9\7\u0081\2\2\u06f9\u0149\3\2\2\2\u06fa\u06fb")
        buf.write("\5\32\16\2\u06fb\u014b\3\2\2\2\u06fc\u06fd\7)\2\2\u06fd")
        buf.write("\u06fe\7\u0080\2\2\u06fe\u06ff\5\u014e\u00a8\2\u06ff\u0700")
        buf.write("\7\u0081\2\2\u0700\u014d\3\2\2\2\u0701\u0706\5\32\16\2")
        buf.write("\u0702\u0703\7\u0087\2\2\u0703\u0705\5\32\16\2\u0704\u0702")
        buf.write("\3\2\2\2\u0705\u0708\3\2\2\2\u0706\u0704\3\2\2\2\u0706")
        buf.write("\u0707\3\2\2\2\u0707\u014f\3\2\2\2\u0708\u0706\3\2\2\2")
        buf.write("\u0709\u070a\7(\2\2\u070a\u070b\5&\24\2\u070b\u0151\3")
        buf.write("\2\2\2\u070c\u070d\7%\2\2\u070d\u070e\5&\24\2\u070e\u0153")
        buf.write("\3\2\2\2\u070f\u0714\7 \2\2\u0710\u0711\7\u0080\2\2\u0711")
        buf.write("\u0712\5\u0156\u00ac\2\u0712\u0713\7\u0081\2\2\u0713\u0715")
        buf.write("\3\2\2\2\u0714\u0710\3\2\2\2\u0714\u0715\3\2\2\2\u0715")
        buf.write("\u0155\3\2\2\2\u0716\u0717\7]\2\2\u0717\u0157\3\2\2\2")
        buf.write("\u0718\u0719\7\"\2\2\u0719\u071a\7\u0080\2\2\u071a\u071b")
        buf.write("\5\34\17\2\u071b\u071c\7\u0081\2\2\u071c\u0159\3\2\2\2")
        buf.write("\u071d\u071e\7!\2\2\u071e\u071f\7\u0080\2\2\u071f\u0720")
        buf.write("\5\u015c\u00af\2\u0720\u0721\7\u0081\2\2\u0721\u015b\3")
        buf.write("\2\2\2\u0722\u0723\5\32\16\2\u0723\u015d\3\2\2\2\u0724")
        buf.write("\u0725\7#\2\2\u0725\u0726\5&\24\2\u0726\u015f\3\2\2\2")
        buf.write("\u0727\u0728\7&\2\2\u0728\u0729\5&\24\2\u0729\u0161\3")
        buf.write("\2\2\2\u072a\u072b\7\'\2\2\u072b\u072c\5&\24\2\u072c\u0163")
        buf.write("\3\2\2\2\u072d\u072e\7$\2\2\u072e\u072f\5&\24\2\u072f")
        buf.write("\u0165\3\2\2\2\u0730\u0731\7*\2\2\u0731\u0732\7\u0080")
        buf.write("\2\2\u0732\u0733\5\u0168\u00b5\2\u0733\u0734\7\u0081\2")
        buf.write("\2\u0734\u0167\3\2\2\2\u0735\u0736\5\32\16\2\u0736\u0169")
        buf.write("\3\2\2\2\u0737\u073b\5\u016c\u00b7\2\u0738\u073a\7x\2")
        buf.write("\2\u0739\u0738\3\2\2\2\u073a\u073d\3\2\2\2\u073b\u0739")
        buf.write("\3\2\2\2\u073b\u073c\3\2\2\2\u073c\u073e\3\2\2\2\u073d")
        buf.write("\u073b\3\2\2\2\u073e\u0742\5\u0186\u00c4\2\u073f\u0741")
        buf.write("\7x\2\2\u0740\u073f\3\2\2\2\u0741\u0744\3\2\2\2\u0742")
        buf.write("\u0740\3\2\2\2\u0742\u0743\3\2\2\2\u0743\u016b\3\2\2\2")
        buf.write("\u0744\u0742\3\2\2\2\u0745\u0747\7\u0082\2\2\u0746\u0748")
        buf.write("\5\u016e\u00b8\2\u0747\u0746\3\2\2\2\u0747\u0748\3\2\2")
        buf.write("\2\u0748\u0749\3\2\2\2\u0749\u074b\5\u0184\u00c3\2\u074a")
        buf.write("\u074c\5\u0170\u00b9\2\u074b\u074a\3\2\2\2\u074b\u074c")
        buf.write("\3\2\2\2\u074c\u0755\3\2\2\2\u074d\u074f\7~\2\2\u074e")
        buf.write("\u0750\5\u017a\u00be\2\u074f\u074e\3\2\2\2\u074f\u0750")
        buf.write("\3\2\2\2\u0750\u0753\3\2\2\2\u0751\u0752\7~\2\2\u0752")
        buf.write("\u0754\5\u0174\u00bb\2\u0753\u0751\3\2\2\2\u0753\u0754")
        buf.write("\3\2\2\2\u0754\u0756\3\2\2\2\u0755\u074d\3\2\2\2\u0755")
        buf.write("\u0756\3\2\2\2\u0756\u0757\3\2\2\2\u0757\u0759\7\u0083")
        buf.write("\2\2\u0758\u075a\7x\2\2\u0759\u0758\3\2\2\2\u0759\u075a")
        buf.write("\3\2\2\2\u075a\u016d\3\2\2\2\u075b\u075c\5\32\16\2\u075c")
        buf.write("\u075d\7\u0088\2\2\u075d\u075f\3\2\2\2\u075e\u075b\3\2")
        buf.write("\2\2\u075e\u075f\3\2\2\2\u075f\u0760\3\2\2\2\u0760\u0761")
        buf.write("\5\32\16\2\u0761\u0762\t\16\2\2\u0762\u0763\7}\2\2\u0763")
        buf.write("\u016f\3\2\2\2\u0764\u0765\7u\2\2\u0765\u0766\5\u0172")
        buf.write("\u00ba\2\u0766\u0171\3\2\2\2\u0767\u0768\5\32\16\2\u0768")
        buf.write("\u0173\3\2\2\2\u0769\u076c\5\u0176\u00bc\2\u076a\u076c")
        buf.write("\5&\24\2\u076b\u0769\3\2\2\2\u076b\u076a\3\2\2\2\u076c")
        buf.write("\u0175\3\2\2\2\u076d\u0772\5\u0178\u00bd\2\u076e\u076f")
        buf.write("\7\u008a\2\2\u076f\u0771\5\u0178\u00bd\2\u0770\u076e\3")
        buf.write("\2\2\2\u0771\u0774\3\2\2\2\u0772\u0770\3\2\2\2\u0772\u0773")
        buf.write("\3\2\2\2\u0773\u0177\3\2\2\2\u0774\u0772\3\2\2\2\u0775")
        buf.write("\u077b\5\32\16\2\u0776\u077b\7z\2\2\u0777\u077b\7\u0086")
        buf.write("\2\2\u0778\u077b\7\u0085\2\2\u0779\u077b\7\u0088\2\2\u077a")
        buf.write("\u0775\3\2\2\2\u077a\u0776\3\2\2\2\u077a\u0777\3\2\2\2")
        buf.write("\u077a\u0778\3\2\2\2\u077a\u0779\3\2\2\2\u077b\u077c\3")
        buf.write("\2\2\2\u077c\u077a\3\2\2\2\u077c\u077d\3\2\2\2\u077d\u0179")
        buf.write("\3\2\2\2\u077e\u0780\t\17\2\2\u077f\u077e\3\2\2\2\u077f")
        buf.write("\u0780\3\2\2\2\u0780\u0781\3\2\2\2\u0781\u0782\5\u0182")
        buf.write("\u00c2\2\u0782\u017b\3\2\2\2\u0783\u0787\5\32\16\2\u0784")
        buf.write("\u0787\7\u0086\2\2\u0785\u0787\7z\2\2\u0786\u0783\3\2")
        buf.write("\2\2\u0786\u0784\3\2\2\2\u0786\u0785\3\2\2\2\u0787\u0788")
        buf.write("\3\2\2\2\u0788\u0786\3\2\2\2\u0788\u0789\3\2\2\2\u0789")
        buf.write("\u017d\3\2\2\2\u078a\u078b\7|\2\2\u078b\u078c\5\32\16")
        buf.write("\2\u078c\u078d\7}\2\2\u078d\u017f\3\2\2\2\u078e\u0791")
        buf.write("\5\u017c\u00bf\2\u078f\u0791\5\u017e\u00c0\2\u0790\u078e")
        buf.write("\3\2\2\2\u0790\u078f\3\2\2\2\u0791\u0181\3\2\2\2\u0792")
        buf.write("\u079d\7\u008a\2\2\u0793\u0794\7\u008a\2\2\u0794\u0796")
        buf.write("\5\u0180\u00c1\2\u0795\u0793\3\2\2\2\u0796\u0797\3\2\2")
        buf.write("\2\u0797\u0795\3\2\2\2\u0797\u0798\3\2\2\2\u0798\u079a")
        buf.write("\3\2\2\2\u0799\u079b\7\u008a\2\2\u079a\u0799\3\2\2\2\u079a")
        buf.write("\u079b\3\2\2\2\u079b\u079d\3\2\2\2\u079c\u0792\3\2\2\2")
        buf.write("\u079c\u0795\3\2\2\2\u079d\u0183\3\2\2\2\u079e\u079f\5")
        buf.write("\32\16\2\u079f\u0185\3\2\2\2\u07a0\u07a2\5\u018a\u00c6")
        buf.write("\2\u07a1\u07a0\3\2\2\2\u07a2\u07a5\3\2\2\2\u07a3\u07a1")
        buf.write("\3\2\2\2\u07a3\u07a4\3\2\2\2\u07a4\u07a9\3\2\2\2\u07a5")
        buf.write("\u07a3\3\2\2\2\u07a6\u07a8\5\u0190\u00c9\2\u07a7\u07a6")
        buf.write("\3\2\2\2\u07a8\u07ab\3\2\2\2\u07a9\u07a7\3\2\2\2\u07a9")
        buf.write("\u07aa\3\2\2\2\u07aa\u07ad\3\2\2\2\u07ab\u07a9\3\2\2\2")
        buf.write("\u07ac\u07ae\5\u0188\u00c5\2\u07ad\u07ac\3\2\2\2\u07ad")
        buf.write("\u07ae\3\2\2\2\u07ae\u07b2\3\2\2\2\u07af\u07b1\7x\2\2")
        buf.write("\u07b0\u07af\3\2\2\2\u07b1\u07b4\3\2\2\2\u07b2\u07b0\3")
        buf.write("\2\2\2\u07b2\u07b3\3\2\2\2\u07b3\u07b8\3\2\2\2\u07b4\u07b2")
        buf.write("\3\2\2\2\u07b5\u07b7\5\u0198\u00cd\2\u07b6\u07b5\3\2\2")
        buf.write("\2\u07b7\u07ba\3\2\2\2\u07b8\u07b6\3\2\2\2\u07b8\u07b9")
        buf.write("\3\2\2\2\u07b9\u0187\3\2\2\2\u07ba\u07b8\3\2\2\2\u07bb")
        buf.write("\u07bc\5&\24\2\u07bc\u0189\3\2\2\2\u07bd\u07be\5\u018c")
        buf.write("\u00c7\2\u07be\u07bf\7\u0099\2\2\u07bf\u07c6\5\u018e\u00c8")
        buf.write("\2\u07c0\u07c2\7x\2\2\u07c1\u07c0\3\2\2\2\u07c2\u07c3")
        buf.write("\3\2\2\2\u07c3\u07c1\3\2\2\2\u07c3\u07c4\3\2\2\2\u07c4")
        buf.write("\u07c7\3\2\2\2\u07c5\u07c7\7\2\2\3\u07c6\u07c1\3\2\2\2")
        buf.write("\u07c6\u07c5\3\2\2\2\u07c7\u018b\3\2\2\2\u07c8\u07c9\5")
        buf.write("\32\16\2\u07c9\u018d\3\2\2\2\u07ca\u07cb\7\u009d\2\2\u07cb")
        buf.write("\u018f\3\2\2\2\u07cc\u07cd\5\u0192\u00ca\2\u07cd\u07cf")
        buf.write("\7\u0080\2\2\u07ce\u07d0\5\u0194\u00cb\2\u07cf\u07ce\3")
        buf.write("\2\2\2\u07cf\u07d0\3\2\2\2\u07d0\u07d1\3\2\2\2\u07d1\u07d3")
        buf.write("\7\u0081\2\2\u07d2\u07d4\5*\26\2\u07d3\u07d2\3\2\2\2\u07d3")
        buf.write("\u07d4\3\2\2\2\u07d4\u07db\3\2\2\2\u07d5\u07d7\7x\2\2")
        buf.write("\u07d6\u07d5\3\2\2\2\u07d7\u07d8\3\2\2\2\u07d8\u07d6\3")
        buf.write("\2\2\2\u07d8\u07d9\3\2\2\2\u07d9\u07dc\3\2\2\2\u07da\u07dc")
        buf.write("\7\2\2\3\u07db\u07d6\3\2\2\2\u07db\u07da\3\2\2\2\u07dc")
        buf.write("\u0191\3\2\2\2\u07dd\u07de\5\32\16\2\u07de\u0193\3\2\2")
        buf.write("\2\u07df\u07e4\5\u0196\u00cc\2\u07e0\u07e1\7\u0087\2\2")
        buf.write("\u07e1\u07e3\5\u0196\u00cc\2\u07e2\u07e0\3\2\2\2\u07e3")
        buf.write("\u07e6\3\2\2\2\u07e4\u07e2\3\2\2\2\u07e4\u07e5\3\2\2\2")
        buf.write("\u07e5\u0195\3\2\2\2\u07e6\u07e4\3\2\2\2\u07e7\u07e9\7")
        buf.write("\u0088\2\2\u07e8\u07e7\3\2\2\2\u07e8\u07e9\3\2\2\2\u07e9")
        buf.write("\u07ea\3\2\2\2\u07ea\u07eb\5\32\16\2\u07eb\u0197\3\2\2")
        buf.write("\2\u07ec\u07fe\5\u019a\u00ce\2\u07ed\u07fe\5\u01a6\u00d4")
        buf.write("\2\u07ee\u07fe\5\u01ae\u00d8\2\u07ef\u07fe\5\u01b2\u00da")
        buf.write("\2\u07f0\u07fe\5\u01b6\u00dc\2\u07f1\u07fe\5\u0200\u0101")
        buf.write("\2\u07f2\u07fe\5\u0202\u0102\2\u07f3\u07fe\5\u0204\u0103")
        buf.write("\2\u07f4\u07fe\5\u0206\u0104\2\u07f5\u07fe\5\u01b8\u00dd")
        buf.write("\2\u07f6\u07fe\5\u0208\u0105\2\u07f7\u07fe\5\u020a\u0106")
        buf.write("\2\u07f8\u07fe\5\u0224\u0113\2\u07f9\u07fe\5\u0226\u0114")
        buf.write("\2\u07fa\u07fe\5\u0228\u0115\2\u07fb\u07fe\5\u022a\u0116")
        buf.write("\2\u07fc\u07fe\7x\2\2\u07fd\u07ec\3\2\2\2\u07fd\u07ed")
        buf.write("\3\2\2\2\u07fd\u07ee\3\2\2\2\u07fd\u07ef\3\2\2\2\u07fd")
        buf.write("\u07f0\3\2\2\2\u07fd\u07f1\3\2\2\2\u07fd\u07f2\3\2\2\2")
        buf.write("\u07fd\u07f3\3\2\2\2\u07fd\u07f4\3\2\2\2\u07fd\u07f5\3")
        buf.write("\2\2\2\u07fd\u07f6\3\2\2\2\u07fd\u07f7\3\2\2\2\u07fd\u07f8")
        buf.write("\3\2\2\2\u07fd\u07f9\3\2\2\2\u07fd\u07fa\3\2\2\2\u07fd")
        buf.write("\u07fb\3\2\2\2\u07fd\u07fc\3\2\2\2\u07fe\u0199\3\2\2\2")
        buf.write("\u07ff\u0800\7\6\2\2\u0800\u0803\7\u0080\2\2\u0801\u0804")
        buf.write("\5\u019c\u00cf\2\u0802\u0804\7x\2\2\u0803\u0801\3\2\2")
        buf.write("\2\u0803\u0802\3\2\2\2\u0804\u0805\3\2\2\2\u0805\u0803")
        buf.write("\3\2\2\2\u0805\u0806\3\2\2\2\u0806\u0807\3\2\2\2\u0807")
        buf.write("\u0808\7\u0081\2\2\u0808\u019b\3\2\2\2\u0809\u080b\5\u019e")
        buf.write("\u00d0\2\u080a\u080c\5\u01a0\u00d1\2\u080b\u080a\3\2\2")
        buf.write("\2\u080b\u080c\3\2\2\2\u080c\u080e\3\2\2\2\u080d\u080f")
        buf.write("\5\u01a2\u00d2\2\u080e\u080d\3\2\2\2\u080e\u080f\3\2\2")
        buf.write("\2\u080f\u0811\3\2\2\2\u0810\u0812\7\u0087\2\2\u0811\u0810")
        buf.write("\3\2\2\2\u0811\u0812\3\2\2\2\u0812\u0814\3\2\2\2\u0813")
        buf.write("\u0815\7x\2\2\u0814\u0813\3\2\2\2\u0814\u0815\3\2\2\2")
        buf.write("\u0815\u019d\3\2\2\2\u0816\u0819\5\36\20\2\u0817\u0819")
        buf.write("\5\34\17\2\u0818\u0816\3\2\2\2\u0818\u0817\3\2\2\2\u0819")
        buf.write("\u019f\3\2\2\2\u081a\u081b\5*\26\2\u081b\u01a1\3\2\2\2")
        buf.write("\u081c\u081d\7\u008b\2\2\u081d\u0827\7}\2\2\u081e\u0828")
        buf.write("\7\u008f\2\2\u081f\u0824\5\u01a4\u00d3\2\u0820\u0821\7")
        buf.write("\u0087\2\2\u0821\u0823\5\u01a4\u00d3\2\u0822\u0820\3\2")
        buf.write("\2\2\u0823\u0826\3\2\2\2\u0824\u0822\3\2\2\2\u0824\u0825")
        buf.write("\3\2\2\2\u0825\u0828\3\2\2\2\u0826\u0824\3\2\2\2\u0827")
        buf.write("\u081e\3\2\2\2\u0827\u081f\3\2\2\2\u0828\u01a3\3\2\2\2")
        buf.write("\u0829\u082a\5\32\16\2\u082a\u01a5\3\2\2\2\u082b\u082e")
        buf.write("\5\u01a8\u00d5\2\u082c\u082d\7\u0088\2\2\u082d\u082f\5")
        buf.write("\u01aa\u00d6\2\u082e\u082c\3\2\2\2\u082e\u082f\3\2\2\2")
        buf.write("\u082f\u0835\3\2\2\2\u0830\u0832\7\u0080\2\2\u0831\u0833")
        buf.write("\5\u01ac\u00d7\2\u0832\u0831\3\2\2\2\u0832\u0833\3\2\2")
        buf.write("\2\u0833\u0834\3\2\2\2\u0834\u0836\7\u0081\2\2\u0835\u0830")
        buf.write("\3\2\2\2\u0835\u0836\3\2\2\2\u0836\u01a7\3\2\2\2\u0837")
        buf.write("\u0838\t\20\2\2\u0838\u01a9\3\2\2\2\u0839\u083a\5\32\16")
        buf.write("\2\u083a\u01ab\3\2\2\2\u083b\u083c\7K\2\2\u083c\u083d")
        buf.write("\7~\2\2\u083d\u083e\7w\2\2\u083e\u01ad\3\2\2\2\u083f\u0842")
        buf.write("\7\37\2\2\u0840\u0841\7\u0088\2\2\u0841\u0843\5\u01b0")
        buf.write("\u00d9\2\u0842\u0840\3\2\2\2\u0842\u0843\3\2\2\2\u0843")
        buf.write("\u0844\3\2\2\2\u0844\u0845\5*\26\2\u0845\u01af\3\2\2\2")
        buf.write("\u0846\u0847\5\32\16\2\u0847\u01b1\3\2\2\2\u0848\u084b")
        buf.write("\7\36\2\2\u0849\u084a\7\u0088\2\2\u084a\u084c\5\u01b4")
        buf.write("\u00db\2\u084b\u0849\3\2\2\2\u084b\u084c\3\2\2\2\u084c")
        buf.write("\u084d\3\2\2\2\u084d\u084e\5*\26\2\u084e\u01b3\3\2\2\2")
        buf.write("\u084f\u0850\5\32\16\2\u0850\u01b5\3\2\2\2\u0851\u0852")
        buf.write("\7\30\2\2\u0852\u0853\5\u01ba\u00de\2\u0853\u01b7\3\2")
        buf.write("\2\2\u0854\u0855\7\25\2\2\u0855\u0856\5\u01ba\u00de\2")
        buf.write("\u0856\u01b9\3\2\2\2\u0857\u0858\7\u0088\2\2\u0858\u085a")
        buf.write("\5\u01be\u00e0\2\u0859\u0857\3\2\2\2\u0859\u085a\3\2\2")
        buf.write("\2\u085a\u085b\3\2\2\2\u085b\u085f\7\u0080\2\2\u085c\u085e")
        buf.write("\7x\2\2\u085d\u085c\3\2\2\2\u085e\u0861\3\2\2\2\u085f")
        buf.write("\u085d\3\2\2\2\u085f\u0860\3\2\2\2\u0860\u0862\3\2\2\2")
        buf.write("\u0861\u085f\3\2\2\2\u0862\u0864\5\u01c8\u00e5\2\u0863")
        buf.write("\u0865\5\u01ca\u00e6\2\u0864\u0863\3\2\2\2\u0864\u0865")
        buf.write("\3\2\2\2\u0865\u0877\3\2\2\2\u0866\u0876\5\u01cc\u00e7")
        buf.write("\2\u0867\u0876\5\u01e0\u00f1\2\u0868\u0876\5\u01e6\u00f4")
        buf.write("\2\u0869\u0876\5\u01f8\u00fd\2\u086a\u0876\5\u01de\u00f0")
        buf.write("\2\u086b\u0876\5\u01d6\u00ec\2\u086c\u0876\5\u01dc\u00ef")
        buf.write("\2\u086d\u0876\5\u01d8\u00ed\2\u086e\u0876\5\u01da\u00ee")
        buf.write("\2\u086f\u0876\5\u01ce\u00e8\2\u0870\u0876\5\u01d2\u00ea")
        buf.write("\2\u0871\u0876\5\u01e8\u00f5\2\u0872\u0876\5\u01ec\u00f7")
        buf.write("\2\u0873\u0876\7x\2\2\u0874\u0876\7\u0087\2\2\u0875\u0866")
        buf.write("\3\2\2\2\u0875\u0867\3\2\2\2\u0875\u0868\3\2\2\2\u0875")
        buf.write("\u0869\3\2\2\2\u0875\u086a\3\2\2\2\u0875\u086b\3\2\2\2")
        buf.write("\u0875\u086c\3\2\2\2\u0875\u086d\3\2\2\2\u0875\u086e\3")
        buf.write("\2\2\2\u0875\u086f\3\2\2\2\u0875\u0870\3\2\2\2\u0875\u0871")
        buf.write("\3\2\2\2\u0875\u0872\3\2\2\2\u0875\u0873\3\2\2\2\u0875")
        buf.write("\u0874\3\2\2\2\u0876\u0879\3\2\2\2\u0877\u0875\3\2\2\2")
        buf.write("\u0877\u0878\3\2\2\2\u0878\u087d\3\2\2\2\u0879\u0877\3")
        buf.write("\2\2\2\u087a\u087c\7x\2\2\u087b\u087a\3\2\2\2\u087c\u087f")
        buf.write("\3\2\2\2\u087d\u087b\3\2\2\2\u087d\u087e\3\2\2\2\u087e")
        buf.write("\u0882\3\2\2\2\u087f\u087d\3\2\2\2\u0880\u0883\5\u01c0")
        buf.write("\u00e1\2\u0881\u0883\5\u01c4\u00e3\2\u0882\u0880\3\2\2")
        buf.write("\2\u0882\u0881\3\2\2\2\u0882\u0883\3\2\2\2\u0883\u0887")
        buf.write("\3\2\2\2\u0884\u0886\7x\2\2\u0885\u0884\3\2\2\2\u0886")
        buf.write("\u0889\3\2\2\2\u0887\u0885\3\2\2\2\u0887\u0888\3\2\2\2")
        buf.write("\u0888\u088d\3\2\2\2\u0889\u0887\3\2\2\2\u088a\u088c\5")
        buf.write("\u01bc\u00df\2\u088b\u088a\3\2\2\2\u088c\u088f\3\2\2\2")
        buf.write("\u088d\u088b\3\2\2\2\u088d\u088e\3\2\2\2\u088e\u0893\3")
        buf.write("\2\2\2\u088f\u088d\3\2\2\2\u0890\u0892\7x\2\2\u0891\u0890")
        buf.write("\3\2\2\2\u0892\u0895\3\2\2\2\u0893\u0891\3\2\2\2\u0893")
        buf.write("\u0894\3\2\2\2\u0894\u0896\3\2\2\2\u0895\u0893\3\2\2\2")
        buf.write("\u0896\u0897\7\u0081\2\2\u0897\u01bb\3\2\2\2\u0898\u089c")
        buf.write("\5\u01e4\u00f3\2\u0899\u089b\7x\2\2\u089a\u0899\3\2\2")
        buf.write("\2\u089b\u089e\3\2\2\2\u089c\u089a\3\2\2\2\u089c\u089d")
        buf.write("\3\2\2\2\u089d\u089f\3\2\2\2\u089e\u089c\3\2\2\2\u089f")
        buf.write("\u08a3\7\u0080\2\2\u08a0\u08a2\7x\2\2\u08a1\u08a0\3\2")
        buf.write("\2\2\u08a2\u08a5\3\2\2\2\u08a3\u08a1\3\2\2\2\u08a3\u08a4")
        buf.write("\3\2\2\2\u08a4\u08a6\3\2\2\2\u08a5\u08a3\3\2\2\2\u08a6")
        buf.write("\u08aa\5\u0186\u00c4\2\u08a7\u08a9\7x\2\2\u08a8\u08a7")
        buf.write("\3\2\2\2\u08a9\u08ac\3\2\2\2\u08aa\u08a8\3\2\2\2\u08aa")
        buf.write("\u08ab\3\2\2\2\u08ab\u08ad\3\2\2\2\u08ac\u08aa\3\2\2\2")
        buf.write("\u08ad\u08b1\7\u0081\2\2\u08ae\u08b0\7x\2\2\u08af\u08ae")
        buf.write("\3\2\2\2\u08b0\u08b3\3\2\2\2\u08b1\u08af\3\2\2\2\u08b1")
        buf.write("\u08b2\3\2\2\2\u08b2\u01bd\3\2\2\2\u08b3\u08b1\3\2\2\2")
        buf.write("\u08b4\u08b5\5\32\16\2\u08b5\u01bf\3\2\2\2\u08b6\u08b7")
        buf.write("\7\u0080\2\2\u08b7\u08b8\5\u01c2\u00e2\2\u08b8\u08b9\7")
        buf.write("\u0081\2\2\u08b9\u08bb\3\2\2\2\u08ba\u08b6\3\2\2\2\u08ba")
        buf.write("\u08bb\3\2\2\2\u08bb\u08bc\3\2\2\2\u08bc\u08bd\7\u008b")
        buf.write("\2\2\u08bd\u08be\7}\2\2\u08be\u08bf\5*\26\2\u08bf\u01c1")
        buf.write("\3\2\2\2\u08c0\u08c1\t\21\2\2\u08c1\u01c3\3\2\2\2\u08c2")
        buf.write("\u08c3\7\u0080\2\2\u08c3\u08c4\5\u01c2\u00e2\2\u08c4\u08c5")
        buf.write("\7\u0081\2\2\u08c5\u08c7\3\2\2\2\u08c6\u08c2\3\2\2\2\u08c6")
        buf.write("\u08c7\3\2\2\2\u08c7\u08c8\3\2\2\2\u08c8\u08c9\7\u008b")
        buf.write("\2\2\u08c9\u08ca\7}\2\2\u08ca\u08cb\5\u01c6\u00e4\2\u08cb")
        buf.write("\u01c5\3\2\2\2\u08cc\u08cd\t\3\2\2\u08cd\u01c7\3\2\2\2")
        buf.write("\u08ce\u08d1\5\36\20\2\u08cf\u08d1\5\34\17\2\u08d0\u08ce")
        buf.write("\3\2\2\2\u08d0\u08cf\3\2\2\2\u08d1\u01c9\3\2\2\2\u08d2")
        buf.write("\u08d3\5*\26\2\u08d3\u01cb\3\2\2\2\u08d4\u08d5\7F\2\2")
        buf.write("\u08d5\u08d6\7~\2\2\u08d6\u08d7\5\32\16\2\u08d7\u01cd")
        buf.write("\3\2\2\2\u08d8\u08d9\7P\2\2\u08d9\u08da\7~\2\2\u08da\u08db")
        buf.write("\5\u01d0\u00e9\2\u08db\u01cf\3\2\2\2\u08dc\u08dd\t\3\2")
        buf.write("\2\u08dd\u01d1\3\2\2\2\u08de\u08df\7O\2\2\u08df\u08e0")
        buf.write("\7~\2\2\u08e0\u08e1\5\u01d4\u00eb\2\u08e1\u01d3\3\2\2")
        buf.write("\2\u08e2\u08e3\t\3\2\2\u08e3\u01d5\3\2\2\2\u08e4\u08e5")
        buf.write("\7T\2\2\u08e5\u08e6\7~\2\2\u08e6\u08e7\5\32\16\2\u08e7")
        buf.write("\u01d7\3\2\2\2\u08e8\u08ec\7R\2\2\u08e9\u08ed\5(\25\2")
        buf.write("\u08ea\u08eb\7~\2\2\u08eb\u08ed\5*\26\2\u08ec\u08e9\3")
        buf.write("\2\2\2\u08ec\u08ea\3\2\2\2\u08ed\u01d9\3\2\2\2\u08ee\u08f2")
        buf.write("\7Q\2\2\u08ef\u08f3\5(\25\2\u08f0\u08f1\7~\2\2\u08f1\u08f3")
        buf.write("\5*\26\2\u08f2\u08ef\3\2\2\2\u08f2\u08f0\3\2\2\2\u08f3")
        buf.write("\u01db\3\2\2\2\u08f4\u08f5\7S\2\2\u08f5\u08f6\7~\2\2\u08f6")
        buf.write("\u08f7\5\32\16\2\u08f7\u01dd\3\2\2\2\u08f8\u08f9\7U\2")
        buf.write("\2\u08f9\u08fa\7~\2\2\u08fa\u08fb\5\32\16\2\u08fb\u01df")
        buf.write("\3\2\2\2\u08fc\u08fd\7[\2\2\u08fd\u08fe\7~\2\2\u08fe\u08ff")
        buf.write("\5\u01e2\u00f2\2\u08ff\u01e1\3\2\2\2\u0900\u0905\5\u01e4")
        buf.write("\u00f3\2\u0901\u0902\7\u0087\2\2\u0902\u0904\5\u01e4\u00f3")
        buf.write("\2\u0903\u0901\3\2\2\2\u0904\u0907\3\2\2\2\u0905\u0903")
        buf.write("\3\2\2\2\u0905\u0906\3\2\2\2\u0906\u01e3\3\2\2\2\u0907")
        buf.write("\u0905\3\2\2\2\u0908\u0909\t\22\2\2\u0909\u01e5\3\2\2")
        buf.write("\2\u090a\u090b\7s\2\2\u090b\u090c\7~\2\2\u090c\u090d\5")
        buf.write("\u01f0\u00f9\2\u090d\u01e7\3\2\2\2\u090e\u090f\7n\2\2")
        buf.write("\u090f\u0910\7~\2\2\u0910\u0911\5\u01ea\u00f6\2\u0911")
        buf.write("\u01e9\3\2\2\2\u0912\u0913\t\f\2\2\u0913\u01eb\3\2\2\2")
        buf.write("\u0914\u0915\7H\2\2\u0915\u0916\7~\2\2\u0916\u0917\5\u01ee")
        buf.write("\u00f8\2\u0917\u01ed\3\2\2\2\u0918\u0919\7w\2\2\u0919")
        buf.write("\u01ef\3\2\2\2\u091a\u091f\5\u01f2\u00fa\2\u091b\u091c")
        buf.write("\7\u0087\2\2\u091c\u091e\5\u01f2\u00fa\2\u091d\u091b\3")
        buf.write("\2\2\2\u091e\u0921\3\2\2\2\u091f\u091d\3\2\2\2\u091f\u0920")
        buf.write("\3\2\2\2\u0920\u01f1\3\2\2\2\u0921\u091f\3\2\2\2\u0922")
        buf.write("\u0924\5\u01f4\u00fb\2\u0923\u0925\5\u01f6\u00fc\2\u0924")
        buf.write("\u0923\3\2\2\2\u0924\u0925\3\2\2\2\u0925\u01f3\3\2\2\2")
        buf.write("\u0926\u092c\7\u008f\2\2\u0927\u0929\7\177\2\2\u0928\u0927")
        buf.write("\3\2\2\2\u0928\u0929\3\2\2\2\u0929\u092a\3\2\2\2\u092a")
        buf.write("\u092c\5\32\16\2\u092b\u0926\3\2\2\2\u092b\u0928\3\2\2")
        buf.write("\2\u092c\u01f5\3\2\2\2\u092d\u092e\5*\26\2\u092e\u01f7")
        buf.write("\3\2\2\2\u092f\u0930\7V\2\2\u0930\u0931\7~\2\2\u0931\u0932")
        buf.write("\5\u01fa\u00fe\2\u0932\u01f9\3\2\2\2\u0933\u0938\5\u01fc")
        buf.write("\u00ff\2\u0934\u0935\7\u0087\2\2\u0935\u0937\5\u01fc\u00ff")
        buf.write("\2\u0936\u0934\3\2\2\2\u0937\u093a\3\2\2\2\u0938\u0936")
        buf.write("\3\2\2\2\u0938\u0939\3\2\2\2\u0939\u01fb\3\2\2\2\u093a")
        buf.write("\u0938\3\2\2\2\u093b\u093c\5\u01fe\u0100\2\u093c\u01fd")
        buf.write("\3\2\2\2\u093d\u0943\7\u008f\2\2\u093e\u0940\7\177\2\2")
        buf.write("\u093f\u093e\3\2\2\2\u093f\u0940\3\2\2\2\u0940\u0941\3")
        buf.write("\2\2\2\u0941\u0943\5\32\16\2\u0942\u093d\3\2\2\2\u0942")
        buf.write("\u093f\3\2\2\2\u0943\u01ff\3\2\2\2\u0944\u0946\7\33\2")
        buf.write("\2\u0945\u0947\5*\26\2\u0946\u0945\3\2\2\2\u0946\u0947")
        buf.write("\3\2\2\2\u0947\u0201\3\2\2\2\u0948\u094a\7\35\2\2\u0949")
        buf.write("\u094b\5*\26\2\u094a\u0949\3\2\2\2\u094a\u094b\3\2\2\2")
        buf.write("\u094b\u0203\3\2\2\2\u094c\u094d\7\32\2\2\u094d\u094e")
        buf.write("\5\u01ba\u00de\2\u094e\u0205\3\2\2\2\u094f\u0950\7\31")
        buf.write("\2\2\u0950\u0951\5\u01ba\u00de\2\u0951\u0207\3\2\2\2\u0952")
        buf.write("\u0953\7\27\2\2\u0953\u0954\5\u01ba\u00de\2\u0954\u0209")
        buf.write("\3\2\2\2\u0955\u0956\7\24\2\2\u0956\u0957\7\u0088\2\2")
        buf.write("\u0957\u0958\5\u020c\u0107\2\u0958\u095c\7\u0080\2\2\u0959")
        buf.write("\u095b\7x\2\2\u095a\u0959\3\2\2\2\u095b\u095e\3\2\2\2")
        buf.write("\u095c\u095a\3\2\2\2\u095c\u095d\3\2\2\2\u095d\u0960\3")
        buf.write("\2\2\2\u095e\u095c\3\2\2\2\u095f\u0961\5\u020e\u0108\2")
        buf.write("\u0960\u095f\3\2\2\2\u0961\u0962\3\2\2\2\u0962\u0960\3")
        buf.write("\2\2\2\u0962\u0963\3\2\2\2\u0963\u0967\3\2\2\2\u0964\u0966")
        buf.write("\7x\2\2\u0965\u0964\3\2\2\2\u0966\u0969\3\2\2\2\u0967")
        buf.write("\u0965\3\2\2\2\u0967\u0968\3\2\2\2\u0968\u096a\3\2\2\2")
        buf.write("\u0969\u0967\3\2\2\2\u096a\u096b\7\u0081\2\2\u096b\u020b")
        buf.write("\3\2\2\2\u096c\u096d\5\32\16\2\u096d\u020d\3\2\2\2\u096e")
        buf.write("\u0970\7\u0087\2\2\u096f\u096e\3\2\2\2\u096f\u0970\3\2")
        buf.write("\2\2\u0970\u0974\3\2\2\2\u0971\u0973\7x\2\2\u0972\u0971")
        buf.write("\3\2\2\2\u0973\u0976\3\2\2\2\u0974\u0972\3\2\2\2\u0974")
        buf.write("\u0975\3\2\2\2\u0975\u0978\3\2\2\2\u0976\u0974\3\2\2\2")
        buf.write("\u0977\u0979\5\u0214\u010b\2\u0978\u0977\3\2\2\2\u0978")
        buf.write("\u0979\3\2\2\2\u0979\u097a\3\2\2\2\u097a\u097d\5\u0222")
        buf.write("\u0112\2\u097b\u097e\5\u0212\u010a\2\u097c\u097e\5\u0210")
        buf.write("\u0109\2\u097d\u097b\3\2\2\2\u097d\u097c\3\2\2\2\u097e")
        buf.write("\u0982\3\2\2\2\u097f\u0981\7x\2\2\u0980\u097f\3\2\2\2")
        buf.write("\u0981\u0984\3\2\2\2\u0982\u0980\3\2\2\2\u0982\u0983\3")
        buf.write("\2\2\2\u0983\u020f\3\2\2\2\u0984\u0982\3\2\2\2\u0985\u0988")
        buf.write("\7~\2\2\u0986\u0989\5\u021e\u0110\2\u0987\u0989\5\u021c")
        buf.write("\u010f\2\u0988\u0986\3\2\2\2\u0988\u0987\3\2\2\2\u0989")
        buf.write("\u0211\3\2\2\2\u098a\u098b\5(\25\2\u098b\u0213\3\2\2\2")
        buf.write("\u098c\u098d\7\u0082\2\2\u098d\u0992\5\u0216\u010c\2\u098e")
        buf.write("\u098f\7\u0087\2\2\u098f\u0991\5\u0216\u010c\2\u0990\u098e")
        buf.write("\3\2\2\2\u0991\u0994\3\2\2\2\u0992\u0990\3\2\2\2\u0992")
        buf.write("\u0993\3\2\2\2\u0993\u0995\3\2\2\2\u0994\u0992\3\2\2\2")
        buf.write("\u0995\u0996\7\u0083\2\2\u0996\u0215\3\2\2\2\u0997\u0998")
        buf.write("\5\u0218\u010d\2\u0998\u0999\7\u008b\2\2\u0999\u099a\5")
        buf.write("\u021a\u010e\2\u099a\u0217\3\2\2\2\u099b\u099c\5\32\16")
        buf.write("\2\u099c\u0219\3\2\2\2\u099d\u09a1\7\u0092\2\2\u099e\u09a1")
        buf.write("\7\u0093\2\2\u099f\u09a1\5\32\16\2\u09a0\u099d\3\2\2\2")
        buf.write("\u09a0\u099e\3\2\2\2\u09a0\u099f\3\2\2\2\u09a1\u021b\3")
        buf.write("\2\2\2\u09a2\u09a3\t\3\2\2\u09a3\u021d\3\2\2\2\u09a4\u09a5")
        buf.write("\7N\2\2\u09a5\u09a6\7\u0080\2\2\u09a6\u09a7\5\u0220\u0111")
        buf.write("\2\u09a7\u09a8\7\u0081\2\2\u09a8\u021f\3\2\2\2\u09a9\u09aa")
        buf.write("\5\32\16\2\u09aa\u09ab\7\u0088\2\2\u09ab\u09ad\3\2\2\2")
        buf.write("\u09ac\u09a9\3\2\2\2\u09ac\u09ad\3\2\2\2\u09ad\u09ae\3")
        buf.write("\2\2\2\u09ae\u09af\5\32\16\2\u09af\u0221\3\2\2\2\u09b0")
        buf.write("\u09b4\7\u0092\2\2\u09b1\u09b4\7\u0093\2\2\u09b2\u09b4")
        buf.write("\5\32\16\2\u09b3\u09b0\3\2\2\2\u09b3\u09b1\3\2\2\2\u09b3")
        buf.write("\u09b2\3\2\2\2\u09b4\u0223\3\2\2\2\u09b5\u09b6\7\26\2")
        buf.write("\2\u09b6\u09b7\5\u01ba\u00de\2\u09b7\u0225\3\2\2\2\u09b8")
        buf.write("\u09b9\7\21\2\2\u09b9\u0227\3\2\2\2\u09ba\u09bc\7\23\2")
        buf.write("\2\u09bb\u09bd\5*\26\2\u09bc\u09bb\3\2\2\2\u09bc\u09bd")
        buf.write("\3\2\2\2\u09bd\u0229\3\2\2\2\u09be\u09bf\7\34\2\2\u09bf")
        buf.write("\u09c0\7\u0080\2\2\u09c0\u09c1\5\u022c\u0117\2\u09c1\u09c2")
        buf.write("\7\u0081\2\2\u09c2\u022b\3\2\2\2\u09c3\u09c4\7z\2\2\u09c4")
        buf.write("\u022d\3\2\2\2\u0108\u0231\u0237\u023d\u0241\u0246\u0248")
        buf.write("\u024d\u0251\u0256\u0258\u025d\u0265\u026a\u0272\u0279")
        buf.write("\u027c\u0285\u028b\u028e\u029d\u02a4\u02a9\u02b1\u02b7")
        buf.write("\u02bc\u02bf\u02c2\u02c6\u02ce\u02e0\u02e7\u02ee\u02f3")
        buf.write("\u02f8\u02fd\u0304\u0308\u030d\u0313\u0318\u0324\u0328")
        buf.write("\u032d\u0332\u0336\u033c\u0346\u034e\u0351\u0356\u035e")
        buf.write("\u0366\u036b\u036f\u0375\u0379\u0381\u0388\u0390\u0398")
        buf.write("\u039d\u03a1\u03a4\u03a9\u03b0\u03ba\u03bc\u03c2\u03c4")
        buf.write("\u03ca\u03cc\u03d1\u03de\u03ed\u03f6\u0402\u0407\u040c")
        buf.write("\u0412\u0418\u041e\u0424\u042c\u042f\u0433\u0437\u0442")
        buf.write("\u0448\u044d\u0454\u045b\u0460\u0463\u0466\u046b\u046e")
        buf.write("\u0472\u0477\u047c\u0481\u0494\u0498\u04b6\u04d5\u04d9")
        buf.write("\u04e4\u04e8\u04ef\u04f9\u0502\u0506\u050d\u051c\u0526")
        buf.write("\u052f\u0538\u0547\u0550\u0554\u0557\u0576\u0586\u0588")
        buf.write("\u058e\u0592\u0597\u059f\u05a7\u05ad\u05b7\u05c5\u05cf")
        buf.write("\u05d1\u05d5\u05ee\u05f3\u0603\u060c\u0615\u061e\u0627")
        buf.write("\u0630\u063b\u063e\u0642\u064b\u0651\u0657\u0659\u0668")
        buf.write("\u066a\u0675\u067d\u0682\u0688\u068d\u0693\u0698\u069e")
        buf.write("\u06a7\u06b0\u06b7\u06bc\u06c8\u06d1\u06df\u06e6\u06f1")
        buf.write("\u06f3\u0706\u0714\u073b\u0742\u0747\u074b\u074f\u0753")
        buf.write("\u0755\u0759\u075e\u076b\u0772\u077a\u077c\u077f\u0786")
        buf.write("\u0788\u0790\u0797\u079a\u079c\u07a3\u07a9\u07ad\u07b2")
        buf.write("\u07b8\u07c3\u07c6\u07cf\u07d3\u07d8\u07db\u07e4\u07e8")
        buf.write("\u07fd\u0803\u0805\u080b\u080e\u0811\u0814\u0818\u0824")
        buf.write("\u0827\u082e\u0832\u0835\u0842\u084b\u0859\u085f\u0864")
        buf.write("\u0875\u0877\u087d\u0882\u0887\u088d\u0893\u089c\u08a3")
        buf.write("\u08aa\u08b1\u08ba\u08c6\u08d0\u08ec\u08f2\u0905\u091f")
        buf.write("\u0924\u0928\u092b\u0938\u093f\u0942\u0946\u094a\u095c")
        buf.write("\u0962\u0967\u096f\u0974\u0978\u097d\u0982\u0988\u0992")
        buf.write("\u09a0\u09ac\u09b3\u09bc")
        return buf.getvalue()


class ZmeiLangParser ( Parser ):

    grammarFileName = "ZmeiLangParser.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "'@admin'", "'@suit'", "'@celery'", "'@stream'", 
                     "'@channels'", "'@docker'", "'@api'", "'@rest'", "'@filer'", 
                     "'@gitlab'", "'@react'", "'@react_client'", "'@react_server'", 
                     "'@theme'", "'@@'", "'@file'", "'@get'", "'@menu'", 
                     "'@crud'", "'@crud_detail'", "'@crud_list'", "'@crud_delete'", 
                     "'@crud_edit'", "'@crud_create'", "'@post'", "'@error'", 
                     "'@auth'", "'@markdown'", "'@html'", "'@tree'", "'@date_tree'", 
                     "'@mixin'", "'@m2m_changed'", "'@post_delete'", "'@pre_delete'", 
                     "'@post_save'", "'@pre_save'", "'@clean'", "'@order'", 
                     "'@sortable'", "'@langs'", "'basic'", "'session'", 
                     "'token'", "'text'", "'html'", "'html_media'", "'float'", 
                     "'decimal'", "'date'", "'datetime'", "'create_time'", 
                     "'update_time'", "'image'", "'file'", "'filer_image'", 
                     "'filer_file'", "'filer_folder'", "'filer_image_folder'", 
                     "'str'", "'int'", "'slug'", "'bool'", "'one'", "'one2one'", 
                     "'many'", "'choices'", "'theme'", "'install'", "'header'", 
                     "'services'", "'selenium_pytest'", "'child'", "'filter_out'", 
                     "'filter_in'", "'page'", "'link_suffix'", "'url_prefix'", 
                     "'can_edit'", "'object_expr'", "'block'", "'item_name'", 
                     "'pk_param'", "'list_fields'", "'delete'", "'edit'", 
                     "'create'", "'detail'", "'skip'", "'from'", "'+polymorphic_list'", 
                     "'css'", "'js'", "'tabular'", "'stacked'", "'polymorphic'", 
                     "'inline'", "'type'", "'user_field'", "'annotate'", 
                     "'on_create'", "'query'", "'auth'", "'count'", "'i18n'", 
                     "'extension'", "'tabs'", "'list'", "'read_only'", "'list_editable'", 
                     "'list_filter'", "'list_search'", "'fields'", "'import'", 
                     "'as'", "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "<INVALID>", "<INVALID>", "'<'", "'>'", "':'", "'^'", 
                     "'('", "')'", "'['", "']'", "'?'", "'_'", "'-'", "','", 
                     "'.'", "'#'", "'/'", "'='", "'$'", "'&'", "'!'", "'*'", 
                     "'~'", "'|'", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "<INVALID>", "<INVALID>", "' '", "<INVALID>", "<INVALID>", 
                     "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "<INVALID>", "';'", "<INVALID>", "'\n'" ]

    symbolicNames = [ "<INVALID>", "AN_ADMIN", "AN_SUIT", "AN_CELERY", "AN_STREAM", 
                      "AN_CHANNELS", "AN_DOCKER", "AN_API", "AN_REST", "AN_FILER", 
                      "AN_GITLAB", "AN_REACT", "AN_REACT_CLIENT", "AN_REACT_SERVER", 
                      "AN_THEME", "AN_PRIORITY", "AN_FILE", "AN_GET", "AN_MENU", 
                      "AN_CRUD", "AN_CRUD_DETAIL", "AN_CRUD_LIST", "AN_CRUD_DELETE", 
                      "AN_CRUD_EDIT", "AN_CRUD_CREATE", "AN_POST", "AN_ERROR", 
                      "AN_AUTH", "AN_MARKDOWN", "AN_HTML", "AN_TREE", "AN_DATE_TREE", 
                      "AN_MIXIN", "AN_M2M_CHANGED", "AN_POST_DELETE", "AN_PRE_DELETE", 
                      "AN_POST_SAVE", "AN_PRE_SAVE", "AN_CLEAN", "AN_ORDER", 
                      "AN_SORTABLE", "AN_LANGS", "KW_AUTH_TYPE_BASIC", "KW_AUTH_TYPE_SESSION", 
                      "KW_AUTH_TYPE_TOKEN", "COL_FIELD_TYPE_LONGTEXT", "COL_FIELD_TYPE_HTML", 
                      "COL_FIELD_TYPE_HTML_MEDIA", "COL_FIELD_TYPE_FLOAT", 
                      "COL_FIELD_TYPE_DECIMAL", "COL_FIELD_TYPE_DATE", "COL_FIELD_TYPE_DATETIME", 
                      "COL_FIELD_TYPE_CREATE_TIME", "COL_FIELD_TYPE_UPDATE_TIME", 
                      "COL_FIELD_TYPE_IMAGE", "COL_FIELD_TYPE_FILE", "COL_FIELD_TYPE_FILER_IMAGE", 
                      "COL_FIELD_TYPE_FILER_FILE", "COL_FIELD_TYPE_FILER_FOLDER", 
                      "COL_FIELD_TYPE_FILER_IMAGE_FOLDER", "COL_FIELD_TYPE_TEXT", 
                      "COL_FIELD_TYPE_INT", "COL_FIELD_TYPE_SLUG", "COL_FIELD_TYPE_BOOL", 
                      "COL_FIELD_TYPE_ONE", "COL_FIELD_TYPE_ONE2ONE", "COL_FIELD_TYPE_MANY", 
                      "COL_FIELD_CHOICES", "KW_THEME", "KW_INSTALL", "KW_HEADER", 
                      "KW_SERVICES", "KW_SELENIUM_PYTEST", "KW_CHILD", "KW_FILTER_OUT", 
                      "KW_FILTER_IN", "KW_PAGE", "KW_LINK_SUFFIX", "KW_URL_PREFIX", 
                      "KW_CAN_EDIT", "KW_OBJECT_EXPR", "KW_BLOCK", "KW_ITEM_NAME", 
                      "KW_PK_PARAM", "KW_LIST_FIELDS", "KW_DELETE", "KW_EDIT", 
                      "KW_CREATE", "KW_DETAIL", "KW_SKIP", "KW_FROM", "KW_POLY_LIST", 
                      "KW_CSS", "KW_JS", "KW_INLINE_TYPE_TABULAR", "KW_INLINE_TYPE_STACKED", 
                      "KW_INLINE_TYPE_POLYMORPHIC", "KW_INLINE", "KW_TYPE", 
                      "KW_USER_FIELD", "KW_ANNOTATE", "KW_ON_CREATE", "KW_QUERY", 
                      "KW_AUTH", "KW_COUNT", "KW_I18N", "KW_EXTENSION", 
                      "KW_TABS", "KW_LIST", "KW_READ_ONLY", "KW_LIST_EDITABLE", 
                      "KW_LIST_FILTER", "KW_LIST_SEARCH", "KW_FIELDS", "KW_IMPORT", 
                      "KW_AS", "WRITE_MODE", "BOOL", "NL", "ID", "DIGIT", 
                      "SIZE2D", "LT", "GT", "COLON", "EXCLUDE", "BRACE_OPEN", 
                      "BRACE_CLOSE", "SQ_BRACE_OPEN", "SQ_BRACE_CLOSE", 
                      "QUESTION_MARK", "UNDERSCORE", "DASH", "COMA", "DOT", 
                      "HASH", "SLASH", "EQUALS", "DOLLAR", "AMP", "EXCLAM", 
                      "STAR", "APPROX", "PIPE", "STRING_DQ", "STRING_SQ", 
                      "COMMENT_LINE", "COMMENT_BLOCK", "UNICODE", "WS", 
                      "COL_FIELD_CALCULATED", "ASSIGN", "ASSIGN_STATIC", 
                      "CODE_BLOCK", "ERRCHAR", "PYTHON_CODE", "PYTHON_LINE_ERRCHAR", 
                      "PYTHON_LINE_END", "PYTHON_EXPR_ERRCHAR", "PYTHON_LINE_NL" ]

    RULE_col_file = 0
    RULE_page_imports = 1
    RULE_model_imports = 2
    RULE_page_import_statement = 3
    RULE_model_import_statement = 4
    RULE_import_statement = 5
    RULE_import_source = 6
    RULE_import_list = 7
    RULE_import_item = 8
    RULE_import_item_name = 9
    RULE_import_item_alias = 10
    RULE_import_item_all = 11
    RULE_id_or_kw = 12
    RULE_classname = 13
    RULE_model_ref = 14
    RULE_field_list_expr = 15
    RULE_field_list_expr_field = 16
    RULE_write_mode_expr = 17
    RULE_python_code = 18
    RULE_code_line = 19
    RULE_code_block = 20
    RULE_cs_annotation = 21
    RULE_an_suit = 22
    RULE_an_suit_app_name = 23
    RULE_an_celery = 24
    RULE_an_channels = 25
    RULE_an_docker = 26
    RULE_an_filer = 27
    RULE_an_gitlab = 28
    RULE_an_gitlab_test_declaration = 29
    RULE_an_gitlab_test_declaration_selenium_pytest = 30
    RULE_an_gitlab_test_services = 31
    RULE_an_gitlab_test_service = 32
    RULE_an_gitlab_test_service_name = 33
    RULE_an_gitlab_branch_declaration = 34
    RULE_an_gitlab_branch_deploy_type = 35
    RULE_an_gitlab_branch_name = 36
    RULE_an_gitlab_deployment_name = 37
    RULE_an_gitlab_deployment_host = 38
    RULE_an_gitlab_deployment_variable = 39
    RULE_an_gitlab_deployment_variable_name = 40
    RULE_an_gitlab_deployment_variable_value = 41
    RULE_an_file = 42
    RULE_an_file_name = 43
    RULE_an_theme = 44
    RULE_an_theme_install = 45
    RULE_an_theme_name = 46
    RULE_an_langs = 47
    RULE_an_langs_list = 48
    RULE_col = 49
    RULE_col_str_expr = 50
    RULE_col_header = 51
    RULE_col_header_line_separator = 52
    RULE_col_verbose_name = 53
    RULE_verbose_name_part = 54
    RULE_col_base_name = 55
    RULE_col_name = 56
    RULE_col_field = 57
    RULE_col_field_expr_or_def = 58
    RULE_col_field_custom = 59
    RULE_col_field_extend = 60
    RULE_col_field_extend_append = 61
    RULE_wrong_field_type = 62
    RULE_col_field_expr = 63
    RULE_col_field_expr_marker = 64
    RULE_col_feild_expr_code = 65
    RULE_string_or_quoted = 66
    RULE_col_field_help_text = 67
    RULE_col_field_verbose_name = 68
    RULE_col_field_name = 69
    RULE_col_modifier = 70
    RULE_col_field_def = 71
    RULE_field_longtext = 72
    RULE_field_html = 73
    RULE_field_html_media = 74
    RULE_field_float = 75
    RULE_field_decimal = 76
    RULE_field_date = 77
    RULE_field_datetime = 78
    RULE_field_create_time = 79
    RULE_field_update_time = 80
    RULE_field_file = 81
    RULE_field_filer_file = 82
    RULE_field_filer_folder = 83
    RULE_field_text = 84
    RULE_field_text_size = 85
    RULE_field_text_choices = 86
    RULE_field_text_choice = 87
    RULE_field_text_choice_val = 88
    RULE_field_text_choice_key = 89
    RULE_field_int = 90
    RULE_field_int_choices = 91
    RULE_field_int_choice = 92
    RULE_field_int_choice_val = 93
    RULE_field_int_choice_key = 94
    RULE_field_slug = 95
    RULE_field_slug_ref_field = 96
    RULE_field_slug_ref_field_id = 97
    RULE_field_bool = 98
    RULE_field_bool_default = 99
    RULE_field_image = 100
    RULE_filer_image_type = 101
    RULE_field_image_sizes = 102
    RULE_field_image_size = 103
    RULE_field_image_size_dimensions = 104
    RULE_field_image_size_name = 105
    RULE_field_image_filters = 106
    RULE_field_image_filter = 107
    RULE_field_relation = 108
    RULE_field_relation_type = 109
    RULE_field_relation_cascade_marker = 110
    RULE_field_relation_target_ref = 111
    RULE_field_relation_target_class = 112
    RULE_field_relation_related_name = 113
    RULE_model_annotation = 114
    RULE_an_admin = 115
    RULE_an_admin_js = 116
    RULE_an_admin_css = 117
    RULE_an_admin_css_file_name = 118
    RULE_an_admin_js_file_name = 119
    RULE_an_admin_inlines = 120
    RULE_an_admin_inline = 121
    RULE_inline_name = 122
    RULE_inline_type = 123
    RULE_inline_type_name = 124
    RULE_inline_extension = 125
    RULE_inline_fields = 126
    RULE_an_admin_tabs = 127
    RULE_an_admin_tab = 128
    RULE_tab_name = 129
    RULE_tab_verbose_name = 130
    RULE_an_admin_list = 131
    RULE_an_admin_read_only = 132
    RULE_an_admin_list_editable = 133
    RULE_an_admin_list_filter = 134
    RULE_an_admin_list_search = 135
    RULE_an_admin_fields = 136
    RULE_an_api = 137
    RULE_an_api_all = 138
    RULE_an_api_name = 139
    RULE_an_rest = 140
    RULE_an_rest_config = 141
    RULE_an_rest_main_part = 142
    RULE_an_rest_descriptor = 143
    RULE_an_rest_i18n = 144
    RULE_an_rest_query = 145
    RULE_an_rest_on_create = 146
    RULE_an_rest_filter_in = 147
    RULE_an_rest_filter_out = 148
    RULE_an_rest_read_only = 149
    RULE_an_rest_user_field = 150
    RULE_an_rest_fields = 151
    RULE_an_rest_fields_write_mode = 152
    RULE_an_rest_auth = 153
    RULE_an_rest_auth_type = 154
    RULE_an_rest_auth_type_name = 155
    RULE_an_rest_auth_token_model = 156
    RULE_an_rest_auth_token_class = 157
    RULE_an_rest_annotate = 158
    RULE_an_rest_annotate_count = 159
    RULE_an_rest_annotate_count_field = 160
    RULE_an_rest_annotate_count_alias = 161
    RULE_an_rest_inline = 162
    RULE_an_rest_inline_decl = 163
    RULE_an_rest_inline_name = 164
    RULE_an_order = 165
    RULE_an_order_fields = 166
    RULE_an_clean = 167
    RULE_an_pre_delete = 168
    RULE_an_tree = 169
    RULE_an_tree_poly = 170
    RULE_an_mixin = 171
    RULE_an_date_tree = 172
    RULE_an_date_tree_field = 173
    RULE_an_m2m_changed = 174
    RULE_an_post_save = 175
    RULE_an_pre_save = 176
    RULE_an_post_delete = 177
    RULE_an_sortable = 178
    RULE_an_sortable_field_name = 179
    RULE_page = 180
    RULE_page_header = 181
    RULE_page_base = 182
    RULE_page_alias = 183
    RULE_page_alias_name = 184
    RULE_page_template = 185
    RULE_template_name = 186
    RULE_file_name_part = 187
    RULE_page_url = 188
    RULE_url_part = 189
    RULE_url_param = 190
    RULE_url_segment = 191
    RULE_url_segments = 192
    RULE_page_name = 193
    RULE_page_body = 194
    RULE_page_code = 195
    RULE_page_field = 196
    RULE_page_field_name = 197
    RULE_page_field_code = 198
    RULE_page_function = 199
    RULE_page_function_name = 200
    RULE_page_function_args = 201
    RULE_page_function_arg = 202
    RULE_page_annotation = 203
    RULE_an_stream = 204
    RULE_an_stream_model = 205
    RULE_an_stream_target_model = 206
    RULE_an_stream_target_filter = 207
    RULE_an_stream_field_list = 208
    RULE_an_stream_field_name = 209
    RULE_an_react = 210
    RULE_an_react_type = 211
    RULE_an_react_descriptor = 212
    RULE_an_react_child = 213
    RULE_an_html = 214
    RULE_an_html_descriptor = 215
    RULE_an_markdown = 216
    RULE_an_markdown_descriptor = 217
    RULE_an_crud_delete = 218
    RULE_an_crud = 219
    RULE_an_crud_params = 220
    RULE_an_crud_page_override = 221
    RULE_an_crud_descriptor = 222
    RULE_an_crud_next_page = 223
    RULE_an_crud_next_page_event_name = 224
    RULE_an_crud_next_page_url = 225
    RULE_an_crud_next_page_url_val = 226
    RULE_an_crud_target_model = 227
    RULE_an_crud_target_filter = 228
    RULE_an_crud_theme = 229
    RULE_an_crud_url_prefix = 230
    RULE_an_crud_url_prefix_val = 231
    RULE_an_crud_link_suffix = 232
    RULE_an_crud_link_suffix_val = 233
    RULE_an_crud_item_name = 234
    RULE_an_crud_object_expr = 235
    RULE_an_crud_can_edit = 236
    RULE_an_crud_block = 237
    RULE_an_crud_pk_param = 238
    RULE_an_crud_skip = 239
    RULE_an_crud_skip_values = 240
    RULE_an_crud_view_name = 241
    RULE_an_crud_fields = 242
    RULE_an_crud_list_type = 243
    RULE_an_crud_list_type_var = 244
    RULE_an_crud_header = 245
    RULE_an_crud_header_enabled = 246
    RULE_an_crud_fields_expr = 247
    RULE_an_crud_field = 248
    RULE_an_crud_field_spec = 249
    RULE_an_crud_field_filter = 250
    RULE_an_crud_list_fields = 251
    RULE_an_crud_list_fields_expr = 252
    RULE_an_crud_list_field = 253
    RULE_an_crud_list_field_spec = 254
    RULE_an_post = 255
    RULE_an_auth = 256
    RULE_an_crud_create = 257
    RULE_an_crud_edit = 258
    RULE_an_crud_list = 259
    RULE_an_menu = 260
    RULE_an_menu_descriptor = 261
    RULE_an_menu_item = 262
    RULE_an_menu_target = 263
    RULE_an_menu_item_code = 264
    RULE_an_menu_item_args = 265
    RULE_an_menu_item_arg = 266
    RULE_an_menu_item_arg_key = 267
    RULE_an_menu_item_arg_val = 268
    RULE_an_menu_item_url = 269
    RULE_an_menu_item_page = 270
    RULE_an_menu_item_page_ref = 271
    RULE_an_menu_label = 272
    RULE_an_crud_detail = 273
    RULE_an_priority_marker = 274
    RULE_an_get = 275
    RULE_an_error = 276
    RULE_an_error_code = 277

    ruleNames =  [ "col_file", "page_imports", "model_imports", "page_import_statement", 
                   "model_import_statement", "import_statement", "import_source", 
                   "import_list", "import_item", "import_item_name", "import_item_alias", 
                   "import_item_all", "id_or_kw", "classname", "model_ref", 
                   "field_list_expr", "field_list_expr_field", "write_mode_expr", 
                   "python_code", "code_line", "code_block", "cs_annotation", 
                   "an_suit", "an_suit_app_name", "an_celery", "an_channels", 
                   "an_docker", "an_filer", "an_gitlab", "an_gitlab_test_declaration", 
                   "an_gitlab_test_declaration_selenium_pytest", "an_gitlab_test_services", 
                   "an_gitlab_test_service", "an_gitlab_test_service_name", 
                   "an_gitlab_branch_declaration", "an_gitlab_branch_deploy_type", 
                   "an_gitlab_branch_name", "an_gitlab_deployment_name", 
                   "an_gitlab_deployment_host", "an_gitlab_deployment_variable", 
                   "an_gitlab_deployment_variable_name", "an_gitlab_deployment_variable_value", 
                   "an_file", "an_file_name", "an_theme", "an_theme_install", 
                   "an_theme_name", "an_langs", "an_langs_list", "col", 
                   "col_str_expr", "col_header", "col_header_line_separator", 
                   "col_verbose_name", "verbose_name_part", "col_base_name", 
                   "col_name", "col_field", "col_field_expr_or_def", "col_field_custom", 
                   "col_field_extend", "col_field_extend_append", "wrong_field_type", 
                   "col_field_expr", "col_field_expr_marker", "col_feild_expr_code", 
                   "string_or_quoted", "col_field_help_text", "col_field_verbose_name", 
                   "col_field_name", "col_modifier", "col_field_def", "field_longtext", 
                   "field_html", "field_html_media", "field_float", "field_decimal", 
                   "field_date", "field_datetime", "field_create_time", 
                   "field_update_time", "field_file", "field_filer_file", 
                   "field_filer_folder", "field_text", "field_text_size", 
                   "field_text_choices", "field_text_choice", "field_text_choice_val", 
                   "field_text_choice_key", "field_int", "field_int_choices", 
                   "field_int_choice", "field_int_choice_val", "field_int_choice_key", 
                   "field_slug", "field_slug_ref_field", "field_slug_ref_field_id", 
                   "field_bool", "field_bool_default", "field_image", "filer_image_type", 
                   "field_image_sizes", "field_image_size", "field_image_size_dimensions", 
                   "field_image_size_name", "field_image_filters", "field_image_filter", 
                   "field_relation", "field_relation_type", "field_relation_cascade_marker", 
                   "field_relation_target_ref", "field_relation_target_class", 
                   "field_relation_related_name", "model_annotation", "an_admin", 
                   "an_admin_js", "an_admin_css", "an_admin_css_file_name", 
                   "an_admin_js_file_name", "an_admin_inlines", "an_admin_inline", 
                   "inline_name", "inline_type", "inline_type_name", "inline_extension", 
                   "inline_fields", "an_admin_tabs", "an_admin_tab", "tab_name", 
                   "tab_verbose_name", "an_admin_list", "an_admin_read_only", 
                   "an_admin_list_editable", "an_admin_list_filter", "an_admin_list_search", 
                   "an_admin_fields", "an_api", "an_api_all", "an_api_name", 
                   "an_rest", "an_rest_config", "an_rest_main_part", "an_rest_descriptor", 
                   "an_rest_i18n", "an_rest_query", "an_rest_on_create", 
                   "an_rest_filter_in", "an_rest_filter_out", "an_rest_read_only", 
                   "an_rest_user_field", "an_rest_fields", "an_rest_fields_write_mode", 
                   "an_rest_auth", "an_rest_auth_type", "an_rest_auth_type_name", 
                   "an_rest_auth_token_model", "an_rest_auth_token_class", 
                   "an_rest_annotate", "an_rest_annotate_count", "an_rest_annotate_count_field", 
                   "an_rest_annotate_count_alias", "an_rest_inline", "an_rest_inline_decl", 
                   "an_rest_inline_name", "an_order", "an_order_fields", 
                   "an_clean", "an_pre_delete", "an_tree", "an_tree_poly", 
                   "an_mixin", "an_date_tree", "an_date_tree_field", "an_m2m_changed", 
                   "an_post_save", "an_pre_save", "an_post_delete", "an_sortable", 
                   "an_sortable_field_name", "page", "page_header", "page_base", 
                   "page_alias", "page_alias_name", "page_template", "template_name", 
                   "file_name_part", "page_url", "url_part", "url_param", 
                   "url_segment", "url_segments", "page_name", "page_body", 
                   "page_code", "page_field", "page_field_name", "page_field_code", 
                   "page_function", "page_function_name", "page_function_args", 
                   "page_function_arg", "page_annotation", "an_stream", 
                   "an_stream_model", "an_stream_target_model", "an_stream_target_filter", 
                   "an_stream_field_list", "an_stream_field_name", "an_react", 
                   "an_react_type", "an_react_descriptor", "an_react_child", 
                   "an_html", "an_html_descriptor", "an_markdown", "an_markdown_descriptor", 
                   "an_crud_delete", "an_crud", "an_crud_params", "an_crud_page_override", 
                   "an_crud_descriptor", "an_crud_next_page", "an_crud_next_page_event_name", 
                   "an_crud_next_page_url", "an_crud_next_page_url_val", 
                   "an_crud_target_model", "an_crud_target_filter", "an_crud_theme", 
                   "an_crud_url_prefix", "an_crud_url_prefix_val", "an_crud_link_suffix", 
                   "an_crud_link_suffix_val", "an_crud_item_name", "an_crud_object_expr", 
                   "an_crud_can_edit", "an_crud_block", "an_crud_pk_param", 
                   "an_crud_skip", "an_crud_skip_values", "an_crud_view_name", 
                   "an_crud_fields", "an_crud_list_type", "an_crud_list_type_var", 
                   "an_crud_header", "an_crud_header_enabled", "an_crud_fields_expr", 
                   "an_crud_field", "an_crud_field_spec", "an_crud_field_filter", 
                   "an_crud_list_fields", "an_crud_list_fields_expr", "an_crud_list_field", 
                   "an_crud_list_field_spec", "an_post", "an_auth", "an_crud_create", 
                   "an_crud_edit", "an_crud_list", "an_menu", "an_menu_descriptor", 
                   "an_menu_item", "an_menu_target", "an_menu_item_code", 
                   "an_menu_item_args", "an_menu_item_arg", "an_menu_item_arg_key", 
                   "an_menu_item_arg_val", "an_menu_item_url", "an_menu_item_page", 
                   "an_menu_item_page_ref", "an_menu_label", "an_crud_detail", 
                   "an_priority_marker", "an_get", "an_error", "an_error_code" ]

    EOF = Token.EOF
    AN_ADMIN=1
    AN_SUIT=2
    AN_CELERY=3
    AN_STREAM=4
    AN_CHANNELS=5
    AN_DOCKER=6
    AN_API=7
    AN_REST=8
    AN_FILER=9
    AN_GITLAB=10
    AN_REACT=11
    AN_REACT_CLIENT=12
    AN_REACT_SERVER=13
    AN_THEME=14
    AN_PRIORITY=15
    AN_FILE=16
    AN_GET=17
    AN_MENU=18
    AN_CRUD=19
    AN_CRUD_DETAIL=20
    AN_CRUD_LIST=21
    AN_CRUD_DELETE=22
    AN_CRUD_EDIT=23
    AN_CRUD_CREATE=24
    AN_POST=25
    AN_ERROR=26
    AN_AUTH=27
    AN_MARKDOWN=28
    AN_HTML=29
    AN_TREE=30
    AN_DATE_TREE=31
    AN_MIXIN=32
    AN_M2M_CHANGED=33
    AN_POST_DELETE=34
    AN_PRE_DELETE=35
    AN_POST_SAVE=36
    AN_PRE_SAVE=37
    AN_CLEAN=38
    AN_ORDER=39
    AN_SORTABLE=40
    AN_LANGS=41
    KW_AUTH_TYPE_BASIC=42
    KW_AUTH_TYPE_SESSION=43
    KW_AUTH_TYPE_TOKEN=44
    COL_FIELD_TYPE_LONGTEXT=45
    COL_FIELD_TYPE_HTML=46
    COL_FIELD_TYPE_HTML_MEDIA=47
    COL_FIELD_TYPE_FLOAT=48
    COL_FIELD_TYPE_DECIMAL=49
    COL_FIELD_TYPE_DATE=50
    COL_FIELD_TYPE_DATETIME=51
    COL_FIELD_TYPE_CREATE_TIME=52
    COL_FIELD_TYPE_UPDATE_TIME=53
    COL_FIELD_TYPE_IMAGE=54
    COL_FIELD_TYPE_FILE=55
    COL_FIELD_TYPE_FILER_IMAGE=56
    COL_FIELD_TYPE_FILER_FILE=57
    COL_FIELD_TYPE_FILER_FOLDER=58
    COL_FIELD_TYPE_FILER_IMAGE_FOLDER=59
    COL_FIELD_TYPE_TEXT=60
    COL_FIELD_TYPE_INT=61
    COL_FIELD_TYPE_SLUG=62
    COL_FIELD_TYPE_BOOL=63
    COL_FIELD_TYPE_ONE=64
    COL_FIELD_TYPE_ONE2ONE=65
    COL_FIELD_TYPE_MANY=66
    COL_FIELD_CHOICES=67
    KW_THEME=68
    KW_INSTALL=69
    KW_HEADER=70
    KW_SERVICES=71
    KW_SELENIUM_PYTEST=72
    KW_CHILD=73
    KW_FILTER_OUT=74
    KW_FILTER_IN=75
    KW_PAGE=76
    KW_LINK_SUFFIX=77
    KW_URL_PREFIX=78
    KW_CAN_EDIT=79
    KW_OBJECT_EXPR=80
    KW_BLOCK=81
    KW_ITEM_NAME=82
    KW_PK_PARAM=83
    KW_LIST_FIELDS=84
    KW_DELETE=85
    KW_EDIT=86
    KW_CREATE=87
    KW_DETAIL=88
    KW_SKIP=89
    KW_FROM=90
    KW_POLY_LIST=91
    KW_CSS=92
    KW_JS=93
    KW_INLINE_TYPE_TABULAR=94
    KW_INLINE_TYPE_STACKED=95
    KW_INLINE_TYPE_POLYMORPHIC=96
    KW_INLINE=97
    KW_TYPE=98
    KW_USER_FIELD=99
    KW_ANNOTATE=100
    KW_ON_CREATE=101
    KW_QUERY=102
    KW_AUTH=103
    KW_COUNT=104
    KW_I18N=105
    KW_EXTENSION=106
    KW_TABS=107
    KW_LIST=108
    KW_READ_ONLY=109
    KW_LIST_EDITABLE=110
    KW_LIST_FILTER=111
    KW_LIST_SEARCH=112
    KW_FIELDS=113
    KW_IMPORT=114
    KW_AS=115
    WRITE_MODE=116
    BOOL=117
    NL=118
    ID=119
    DIGIT=120
    SIZE2D=121
    LT=122
    GT=123
    COLON=124
    EXCLUDE=125
    BRACE_OPEN=126
    BRACE_CLOSE=127
    SQ_BRACE_OPEN=128
    SQ_BRACE_CLOSE=129
    QUESTION_MARK=130
    UNDERSCORE=131
    DASH=132
    COMA=133
    DOT=134
    HASH=135
    SLASH=136
    EQUALS=137
    DOLLAR=138
    AMP=139
    EXCLAM=140
    STAR=141
    APPROX=142
    PIPE=143
    STRING_DQ=144
    STRING_SQ=145
    COMMENT_LINE=146
    COMMENT_BLOCK=147
    UNICODE=148
    WS=149
    COL_FIELD_CALCULATED=150
    ASSIGN=151
    ASSIGN_STATIC=152
    CODE_BLOCK=153
    ERRCHAR=154
    PYTHON_CODE=155
    PYTHON_LINE_ERRCHAR=156
    PYTHON_LINE_END=157
    PYTHON_EXPR_ERRCHAR=158
    PYTHON_LINE_NL=159

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.7.2")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class Col_fileContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def EOF(self):
            return self.getToken(ZmeiLangParser.EOF, 0)

        def NL(self, i:int=None):
            if i is None:
                return self.getTokens(ZmeiLangParser.NL)
            else:
                return self.getToken(ZmeiLangParser.NL, i)

        def cs_annotation(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(ZmeiLangParser.Cs_annotationContext)
            else:
                return self.getTypedRuleContext(ZmeiLangParser.Cs_annotationContext,i)


        def page_imports(self):
            return self.getTypedRuleContext(ZmeiLangParser.Page_importsContext,0)


        def page(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(ZmeiLangParser.PageContext)
            else:
                return self.getTypedRuleContext(ZmeiLangParser.PageContext,i)


        def model_imports(self):
            return self.getTypedRuleContext(ZmeiLangParser.Model_importsContext,0)


        def col(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(ZmeiLangParser.ColContext)
            else:
                return self.getTypedRuleContext(ZmeiLangParser.ColContext,i)


        def getRuleIndex(self):
            return ZmeiLangParser.RULE_col_file

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterCol_file" ):
                listener.enterCol_file(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitCol_file" ):
                listener.exitCol_file(self)




    def col_file(self):

        localctx = ZmeiLangParser.Col_fileContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_col_file)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 559
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,0,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 556
                    self.match(ZmeiLangParser.NL) 
                self.state = 561
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,0,self._ctx)

            self.state = 565
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,1,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 562
                    self.cs_annotation() 
                self.state = 567
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,1,self._ctx)

            self.state = 571
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,2,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 568
                    self.match(ZmeiLangParser.NL) 
                self.state = 573
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,2,self._ctx)

            self.state = 582
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,5,self._ctx)
            if la_ == 1:
                self.state = 575
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==ZmeiLangParser.KW_FROM or _la==ZmeiLangParser.KW_IMPORT:
                    self.state = 574
                    self.page_imports()


                self.state = 578 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while True:
                    self.state = 577
                    self.page()
                    self.state = 580 
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    if not (_la==ZmeiLangParser.SQ_BRACE_OPEN):
                        break



            self.state = 587
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,6,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 584
                    self.match(ZmeiLangParser.NL) 
                self.state = 589
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,6,self._ctx)

            self.state = 598
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if ((((_la - 90)) & ~0x3f) == 0 and ((1 << (_la - 90)) & ((1 << (ZmeiLangParser.KW_FROM - 90)) | (1 << (ZmeiLangParser.KW_IMPORT - 90)) | (1 << (ZmeiLangParser.HASH - 90)))) != 0):
                self.state = 591
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==ZmeiLangParser.KW_FROM or _la==ZmeiLangParser.KW_IMPORT:
                    self.state = 590
                    self.model_imports()


                self.state = 594 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while True:
                    self.state = 593
                    self.col()
                    self.state = 596 
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    if not (_la==ZmeiLangParser.HASH):
                        break



            self.state = 603
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==ZmeiLangParser.NL:
                self.state = 600
                self.match(ZmeiLangParser.NL)
                self.state = 605
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 606
            self.match(ZmeiLangParser.EOF)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Page_importsContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def page_import_statement(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(ZmeiLangParser.Page_import_statementContext)
            else:
                return self.getTypedRuleContext(ZmeiLangParser.Page_import_statementContext,i)


        def getRuleIndex(self):
            return ZmeiLangParser.RULE_page_imports

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPage_imports" ):
                listener.enterPage_imports(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPage_imports" ):
                listener.exitPage_imports(self)




    def page_imports(self):

        localctx = ZmeiLangParser.Page_importsContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_page_imports)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 609 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 608
                self.page_import_statement()
                self.state = 611 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not (_la==ZmeiLangParser.KW_FROM or _la==ZmeiLangParser.KW_IMPORT):
                    break

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Model_importsContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def model_import_statement(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(ZmeiLangParser.Model_import_statementContext)
            else:
                return self.getTypedRuleContext(ZmeiLangParser.Model_import_statementContext,i)


        def getRuleIndex(self):
            return ZmeiLangParser.RULE_model_imports

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterModel_imports" ):
                listener.enterModel_imports(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitModel_imports" ):
                listener.exitModel_imports(self)




    def model_imports(self):

        localctx = ZmeiLangParser.Model_importsContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_model_imports)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 614 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 613
                self.model_import_statement()
                self.state = 616 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not (_la==ZmeiLangParser.KW_FROM or _la==ZmeiLangParser.KW_IMPORT):
                    break

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Page_import_statementContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def import_statement(self):
            return self.getTypedRuleContext(ZmeiLangParser.Import_statementContext,0)


        def getRuleIndex(self):
            return ZmeiLangParser.RULE_page_import_statement

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPage_import_statement" ):
                listener.enterPage_import_statement(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPage_import_statement" ):
                listener.exitPage_import_statement(self)




    def page_import_statement(self):

        localctx = ZmeiLangParser.Page_import_statementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_page_import_statement)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 618
            self.import_statement()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Model_import_statementContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def import_statement(self):
            return self.getTypedRuleContext(ZmeiLangParser.Import_statementContext,0)


        def getRuleIndex(self):
            return ZmeiLangParser.RULE_model_import_statement

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterModel_import_statement" ):
                listener.enterModel_import_statement(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitModel_import_statement" ):
                listener.exitModel_import_statement(self)




    def model_import_statement(self):

        localctx = ZmeiLangParser.Model_import_statementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_model_import_statement)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 620
            self.import_statement()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Import_statementContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def KW_IMPORT(self):
            return self.getToken(ZmeiLangParser.KW_IMPORT, 0)

        def import_list(self):
            return self.getTypedRuleContext(ZmeiLangParser.Import_listContext,0)


        def KW_FROM(self):
            return self.getToken(ZmeiLangParser.KW_FROM, 0)

        def import_source(self):
            return self.getTypedRuleContext(ZmeiLangParser.Import_sourceContext,0)


        def NL(self, i:int=None):
            if i is None:
                return self.getTokens(ZmeiLangParser.NL)
            else:
                return self.getToken(ZmeiLangParser.NL, i)

        def getRuleIndex(self):
            return ZmeiLangParser.RULE_import_statement

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterImport_statement" ):
                listener.enterImport_statement(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitImport_statement" ):
                listener.exitImport_statement(self)




    def import_statement(self):

        localctx = ZmeiLangParser.Import_statementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 10, self.RULE_import_statement)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 624
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==ZmeiLangParser.KW_FROM:
                self.state = 622
                self.match(ZmeiLangParser.KW_FROM)
                self.state = 623
                self.import_source()


            self.state = 626
            self.match(ZmeiLangParser.KW_IMPORT)
            self.state = 627
            self.import_list()
            self.state = 629 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 628
                self.match(ZmeiLangParser.NL)
                self.state = 631 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not (_la==ZmeiLangParser.NL):
                    break

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Import_sourceContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def classname(self):
            return self.getTypedRuleContext(ZmeiLangParser.ClassnameContext,0)


        def DOT(self):
            return self.getToken(ZmeiLangParser.DOT, 0)

        def getRuleIndex(self):
            return ZmeiLangParser.RULE_import_source

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterImport_source" ):
                listener.enterImport_source(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitImport_source" ):
                listener.exitImport_source(self)




    def import_source(self):

        localctx = ZmeiLangParser.Import_sourceContext(self, self._ctx, self.state)
        self.enterRule(localctx, 12, self.RULE_import_source)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 634
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==ZmeiLangParser.DOT:
                self.state = 633
                self.match(ZmeiLangParser.DOT)


            self.state = 636
            self.classname()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Import_listContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def import_item(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(ZmeiLangParser.Import_itemContext)
            else:
                return self.getTypedRuleContext(ZmeiLangParser.Import_itemContext,i)


        def COMA(self, i:int=None):
            if i is None:
                return self.getTokens(ZmeiLangParser.COMA)
            else:
                return self.getToken(ZmeiLangParser.COMA, i)

        def getRuleIndex(self):
            return ZmeiLangParser.RULE_import_list

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterImport_list" ):
                listener.enterImport_list(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitImport_list" ):
                listener.exitImport_list(self)




    def import_list(self):

        localctx = ZmeiLangParser.Import_listContext(self, self._ctx, self.state)
        self.enterRule(localctx, 14, self.RULE_import_list)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 638
            self.import_item()
            self.state = 643
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==ZmeiLangParser.COMA:
                self.state = 639
                self.match(ZmeiLangParser.COMA)
                self.state = 640
                self.import_item()
                self.state = 645
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Import_itemContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def import_item_name(self):
            return self.getTypedRuleContext(ZmeiLangParser.Import_item_nameContext,0)


        def KW_AS(self):
            return self.getToken(ZmeiLangParser.KW_AS, 0)

        def import_item_alias(self):
            return self.getTypedRuleContext(ZmeiLangParser.Import_item_aliasContext,0)


        def import_item_all(self):
            return self.getTypedRuleContext(ZmeiLangParser.Import_item_allContext,0)


        def getRuleIndex(self):
            return ZmeiLangParser.RULE_import_item

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterImport_item" ):
                listener.enterImport_item(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitImport_item" ):
                listener.exitImport_item(self)




    def import_item(self):

        localctx = ZmeiLangParser.Import_itemContext(self, self._ctx, self.state)
        self.enterRule(localctx, 16, self.RULE_import_item)
        self._la = 0 # Token type
        try:
            self.state = 652
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [ZmeiLangParser.KW_AUTH_TYPE_BASIC, ZmeiLangParser.KW_AUTH_TYPE_SESSION, ZmeiLangParser.KW_AUTH_TYPE_TOKEN, ZmeiLangParser.COL_FIELD_TYPE_LONGTEXT, ZmeiLangParser.COL_FIELD_TYPE_HTML, ZmeiLangParser.COL_FIELD_TYPE_HTML_MEDIA, ZmeiLangParser.COL_FIELD_TYPE_FLOAT, ZmeiLangParser.COL_FIELD_TYPE_DECIMAL, ZmeiLangParser.COL_FIELD_TYPE_DATE, ZmeiLangParser.COL_FIELD_TYPE_DATETIME, ZmeiLangParser.COL_FIELD_TYPE_CREATE_TIME, ZmeiLangParser.COL_FIELD_TYPE_UPDATE_TIME, ZmeiLangParser.COL_FIELD_TYPE_IMAGE, ZmeiLangParser.COL_FIELD_TYPE_FILE, ZmeiLangParser.COL_FIELD_TYPE_FILER_IMAGE, ZmeiLangParser.COL_FIELD_TYPE_FILER_FILE, ZmeiLangParser.COL_FIELD_TYPE_FILER_FOLDER, ZmeiLangParser.COL_FIELD_TYPE_FILER_IMAGE_FOLDER, ZmeiLangParser.COL_FIELD_TYPE_TEXT, ZmeiLangParser.COL_FIELD_TYPE_INT, ZmeiLangParser.COL_FIELD_TYPE_SLUG, ZmeiLangParser.COL_FIELD_TYPE_BOOL, ZmeiLangParser.COL_FIELD_TYPE_ONE, ZmeiLangParser.COL_FIELD_TYPE_ONE2ONE, ZmeiLangParser.COL_FIELD_TYPE_MANY, ZmeiLangParser.COL_FIELD_CHOICES, ZmeiLangParser.KW_THEME, ZmeiLangParser.KW_INSTALL, ZmeiLangParser.KW_HEADER, ZmeiLangParser.KW_SERVICES, ZmeiLangParser.KW_SELENIUM_PYTEST, ZmeiLangParser.KW_CHILD, ZmeiLangParser.KW_FILTER_OUT, ZmeiLangParser.KW_FILTER_IN, ZmeiLangParser.KW_PAGE, ZmeiLangParser.KW_LINK_SUFFIX, ZmeiLangParser.KW_URL_PREFIX, ZmeiLangParser.KW_CAN_EDIT, ZmeiLangParser.KW_OBJECT_EXPR, ZmeiLangParser.KW_BLOCK, ZmeiLangParser.KW_ITEM_NAME, ZmeiLangParser.KW_PK_PARAM, ZmeiLangParser.KW_LIST_FIELDS, ZmeiLangParser.KW_DELETE, ZmeiLangParser.KW_EDIT, ZmeiLangParser.KW_CREATE, ZmeiLangParser.KW_DETAIL, ZmeiLangParser.KW_SKIP, ZmeiLangParser.KW_FROM, ZmeiLangParser.KW_POLY_LIST, ZmeiLangParser.KW_CSS, ZmeiLangParser.KW_JS, ZmeiLangParser.KW_INLINE_TYPE_TABULAR, ZmeiLangParser.KW_INLINE_TYPE_STACKED, ZmeiLangParser.KW_INLINE_TYPE_POLYMORPHIC, ZmeiLangParser.KW_INLINE, ZmeiLangParser.KW_TYPE, ZmeiLangParser.KW_USER_FIELD, ZmeiLangParser.KW_ANNOTATE, ZmeiLangParser.KW_ON_CREATE, ZmeiLangParser.KW_QUERY, ZmeiLangParser.KW_AUTH, ZmeiLangParser.KW_COUNT, ZmeiLangParser.KW_I18N, ZmeiLangParser.KW_EXTENSION, ZmeiLangParser.KW_TABS, ZmeiLangParser.KW_LIST, ZmeiLangParser.KW_READ_ONLY, ZmeiLangParser.KW_LIST_EDITABLE, ZmeiLangParser.KW_LIST_FILTER, ZmeiLangParser.KW_LIST_SEARCH, ZmeiLangParser.KW_FIELDS, ZmeiLangParser.KW_IMPORT, ZmeiLangParser.KW_AS, ZmeiLangParser.WRITE_MODE, ZmeiLangParser.BOOL, ZmeiLangParser.ID]:
                self.enterOuterAlt(localctx, 1)
                self.state = 646
                self.import_item_name()
                self.state = 649
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==ZmeiLangParser.KW_AS:
                    self.state = 647
                    self.match(ZmeiLangParser.KW_AS)
                    self.state = 648
                    self.import_item_alias()


                pass
            elif token in [ZmeiLangParser.STAR]:
                self.enterOuterAlt(localctx, 2)
                self.state = 651
                self.import_item_all()
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Import_item_nameContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def classname(self):
            return self.getTypedRuleContext(ZmeiLangParser.ClassnameContext,0)


        def getRuleIndex(self):
            return ZmeiLangParser.RULE_import_item_name

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterImport_item_name" ):
                listener.enterImport_item_name(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitImport_item_name" ):
                listener.exitImport_item_name(self)




    def import_item_name(self):

        localctx = ZmeiLangParser.Import_item_nameContext(self, self._ctx, self.state)
        self.enterRule(localctx, 18, self.RULE_import_item_name)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 654
            self.classname()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Import_item_aliasContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def id_or_kw(self):
            return self.getTypedRuleContext(ZmeiLangParser.Id_or_kwContext,0)


        def getRuleIndex(self):
            return ZmeiLangParser.RULE_import_item_alias

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterImport_item_alias" ):
                listener.enterImport_item_alias(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitImport_item_alias" ):
                listener.exitImport_item_alias(self)




    def import_item_alias(self):

        localctx = ZmeiLangParser.Import_item_aliasContext(self, self._ctx, self.state)
        self.enterRule(localctx, 20, self.RULE_import_item_alias)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 656
            self.id_or_kw()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Import_item_allContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def STAR(self):
            return self.getToken(ZmeiLangParser.STAR, 0)

        def getRuleIndex(self):
            return ZmeiLangParser.RULE_import_item_all

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterImport_item_all" ):
                listener.enterImport_item_all(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitImport_item_all" ):
                listener.exitImport_item_all(self)




    def import_item_all(self):

        localctx = ZmeiLangParser.Import_item_allContext(self, self._ctx, self.state)
        self.enterRule(localctx, 22, self.RULE_import_item_all)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 658
            self.match(ZmeiLangParser.STAR)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Id_or_kwContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ID(self):
            return self.getToken(ZmeiLangParser.ID, 0)

        def BOOL(self):
            return self.getToken(ZmeiLangParser.BOOL, 0)

        def WRITE_MODE(self):
            return self.getToken(ZmeiLangParser.WRITE_MODE, 0)

        def KW_AUTH_TYPE_BASIC(self):
            return self.getToken(ZmeiLangParser.KW_AUTH_TYPE_BASIC, 0)

        def KW_AUTH_TYPE_SESSION(self):
            return self.getToken(ZmeiLangParser.KW_AUTH_TYPE_SESSION, 0)

        def KW_AUTH_TYPE_TOKEN(self):
            return self.getToken(ZmeiLangParser.KW_AUTH_TYPE_TOKEN, 0)

        def COL_FIELD_TYPE_LONGTEXT(self):
            return self.getToken(ZmeiLangParser.COL_FIELD_TYPE_LONGTEXT, 0)

        def COL_FIELD_TYPE_HTML(self):
            return self.getToken(ZmeiLangParser.COL_FIELD_TYPE_HTML, 0)

        def COL_FIELD_TYPE_HTML_MEDIA(self):
            return self.getToken(ZmeiLangParser.COL_FIELD_TYPE_HTML_MEDIA, 0)

        def COL_FIELD_TYPE_FLOAT(self):
            return self.getToken(ZmeiLangParser.COL_FIELD_TYPE_FLOAT, 0)

        def COL_FIELD_TYPE_DECIMAL(self):
            return self.getToken(ZmeiLangParser.COL_FIELD_TYPE_DECIMAL, 0)

        def COL_FIELD_TYPE_DATE(self):
            return self.getToken(ZmeiLangParser.COL_FIELD_TYPE_DATE, 0)

        def COL_FIELD_TYPE_DATETIME(self):
            return self.getToken(ZmeiLangParser.COL_FIELD_TYPE_DATETIME, 0)

        def COL_FIELD_TYPE_CREATE_TIME(self):
            return self.getToken(ZmeiLangParser.COL_FIELD_TYPE_CREATE_TIME, 0)

        def COL_FIELD_TYPE_UPDATE_TIME(self):
            return self.getToken(ZmeiLangParser.COL_FIELD_TYPE_UPDATE_TIME, 0)

        def COL_FIELD_TYPE_IMAGE(self):
            return self.getToken(ZmeiLangParser.COL_FIELD_TYPE_IMAGE, 0)

        def COL_FIELD_TYPE_FILE(self):
            return self.getToken(ZmeiLangParser.COL_FIELD_TYPE_FILE, 0)

        def COL_FIELD_TYPE_FILER_IMAGE(self):
            return self.getToken(ZmeiLangParser.COL_FIELD_TYPE_FILER_IMAGE, 0)

        def COL_FIELD_TYPE_FILER_FILE(self):
            return self.getToken(ZmeiLangParser.COL_FIELD_TYPE_FILER_FILE, 0)

        def COL_FIELD_TYPE_FILER_FOLDER(self):
            return self.getToken(ZmeiLangParser.COL_FIELD_TYPE_FILER_FOLDER, 0)

        def COL_FIELD_TYPE_FILER_IMAGE_FOLDER(self):
            return self.getToken(ZmeiLangParser.COL_FIELD_TYPE_FILER_IMAGE_FOLDER, 0)

        def COL_FIELD_TYPE_TEXT(self):
            return self.getToken(ZmeiLangParser.COL_FIELD_TYPE_TEXT, 0)

        def COL_FIELD_TYPE_INT(self):
            return self.getToken(ZmeiLangParser.COL_FIELD_TYPE_INT, 0)

        def COL_FIELD_TYPE_SLUG(self):
            return self.getToken(ZmeiLangParser.COL_FIELD_TYPE_SLUG, 0)

        def COL_FIELD_TYPE_BOOL(self):
            return self.getToken(ZmeiLangParser.COL_FIELD_TYPE_BOOL, 0)

        def COL_FIELD_TYPE_ONE(self):
            return self.getToken(ZmeiLangParser.COL_FIELD_TYPE_ONE, 0)

        def COL_FIELD_TYPE_ONE2ONE(self):
            return self.getToken(ZmeiLangParser.COL_FIELD_TYPE_ONE2ONE, 0)

        def COL_FIELD_TYPE_MANY(self):
            return self.getToken(ZmeiLangParser.COL_FIELD_TYPE_MANY, 0)

        def COL_FIELD_CHOICES(self):
            return self.getToken(ZmeiLangParser.COL_FIELD_CHOICES, 0)

        def KW_THEME(self):
            return self.getToken(ZmeiLangParser.KW_THEME, 0)

        def KW_INSTALL(self):
            return self.getToken(ZmeiLangParser.KW_INSTALL, 0)

        def KW_HEADER(self):
            return self.getToken(ZmeiLangParser.KW_HEADER, 0)

        def KW_SERVICES(self):
            return self.getToken(ZmeiLangParser.KW_SERVICES, 0)

        def KW_SELENIUM_PYTEST(self):
            return self.getToken(ZmeiLangParser.KW_SELENIUM_PYTEST, 0)

        def KW_CHILD(self):
            return self.getToken(ZmeiLangParser.KW_CHILD, 0)

        def KW_FILTER_OUT(self):
            return self.getToken(ZmeiLangParser.KW_FILTER_OUT, 0)

        def KW_FILTER_IN(self):
            return self.getToken(ZmeiLangParser.KW_FILTER_IN, 0)

        def KW_PAGE(self):
            return self.getToken(ZmeiLangParser.KW_PAGE, 0)

        def KW_LINK_SUFFIX(self):
            return self.getToken(ZmeiLangParser.KW_LINK_SUFFIX, 0)

        def KW_URL_PREFIX(self):
            return self.getToken(ZmeiLangParser.KW_URL_PREFIX, 0)

        def KW_CAN_EDIT(self):
            return self.getToken(ZmeiLangParser.KW_CAN_EDIT, 0)

        def KW_OBJECT_EXPR(self):
            return self.getToken(ZmeiLangParser.KW_OBJECT_EXPR, 0)

        def KW_BLOCK(self):
            return self.getToken(ZmeiLangParser.KW_BLOCK, 0)

        def KW_ITEM_NAME(self):
            return self.getToken(ZmeiLangParser.KW_ITEM_NAME, 0)

        def KW_PK_PARAM(self):
            return self.getToken(ZmeiLangParser.KW_PK_PARAM, 0)

        def KW_LIST_FIELDS(self):
            return self.getToken(ZmeiLangParser.KW_LIST_FIELDS, 0)

        def KW_DELETE(self):
            return self.getToken(ZmeiLangParser.KW_DELETE, 0)

        def KW_EDIT(self):
            return self.getToken(ZmeiLangParser.KW_EDIT, 0)

        def KW_CREATE(self):
            return self.getToken(ZmeiLangParser.KW_CREATE, 0)

        def KW_DETAIL(self):
            return self.getToken(ZmeiLangParser.KW_DETAIL, 0)

        def KW_SKIP(self):
            return self.getToken(ZmeiLangParser.KW_SKIP, 0)

        def KW_FROM(self):
            return self.getToken(ZmeiLangParser.KW_FROM, 0)

        def KW_POLY_LIST(self):
            return self.getToken(ZmeiLangParser.KW_POLY_LIST, 0)

        def KW_CSS(self):
            return self.getToken(ZmeiLangParser.KW_CSS, 0)

        def KW_JS(self):
            return self.getToken(ZmeiLangParser.KW_JS, 0)

        def KW_INLINE_TYPE_TABULAR(self):
            return self.getToken(ZmeiLangParser.KW_INLINE_TYPE_TABULAR, 0)

        def KW_INLINE_TYPE_STACKED(self):
            return self.getToken(ZmeiLangParser.KW_INLINE_TYPE_STACKED, 0)

        def KW_INLINE_TYPE_POLYMORPHIC(self):
            return self.getToken(ZmeiLangParser.KW_INLINE_TYPE_POLYMORPHIC, 0)

        def KW_INLINE(self):
            return self.getToken(ZmeiLangParser.KW_INLINE, 0)

        def KW_TYPE(self):
            return self.getToken(ZmeiLangParser.KW_TYPE, 0)

        def KW_USER_FIELD(self):
            return self.getToken(ZmeiLangParser.KW_USER_FIELD, 0)

        def KW_ANNOTATE(self):
            return self.getToken(ZmeiLangParser.KW_ANNOTATE, 0)

        def KW_ON_CREATE(self):
            return self.getToken(ZmeiLangParser.KW_ON_CREATE, 0)

        def KW_QUERY(self):
            return self.getToken(ZmeiLangParser.KW_QUERY, 0)

        def KW_AUTH(self):
            return self.getToken(ZmeiLangParser.KW_AUTH, 0)

        def KW_COUNT(self):
            return self.getToken(ZmeiLangParser.KW_COUNT, 0)

        def KW_I18N(self):
            return self.getToken(ZmeiLangParser.KW_I18N, 0)

        def KW_EXTENSION(self):
            return self.getToken(ZmeiLangParser.KW_EXTENSION, 0)

        def KW_TABS(self):
            return self.getToken(ZmeiLangParser.KW_TABS, 0)

        def KW_LIST(self):
            return self.getToken(ZmeiLangParser.KW_LIST, 0)

        def KW_READ_ONLY(self):
            return self.getToken(ZmeiLangParser.KW_READ_ONLY, 0)

        def KW_LIST_EDITABLE(self):
            return self.getToken(ZmeiLangParser.KW_LIST_EDITABLE, 0)

        def KW_LIST_FILTER(self):
            return self.getToken(ZmeiLangParser.KW_LIST_FILTER, 0)

        def KW_LIST_SEARCH(self):
            return self.getToken(ZmeiLangParser.KW_LIST_SEARCH, 0)

        def KW_FIELDS(self):
            return self.getToken(ZmeiLangParser.KW_FIELDS, 0)

        def KW_IMPORT(self):
            return self.getToken(ZmeiLangParser.KW_IMPORT, 0)

        def KW_AS(self):
            return self.getToken(ZmeiLangParser.KW_AS, 0)

        def getRuleIndex(self):
            return ZmeiLangParser.RULE_id_or_kw

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterId_or_kw" ):
                listener.enterId_or_kw(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitId_or_kw" ):
                listener.exitId_or_kw(self)




    def id_or_kw(self):

        localctx = ZmeiLangParser.Id_or_kwContext(self, self._ctx, self.state)
        self.enterRule(localctx, 24, self.RULE_id_or_kw)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 660
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << ZmeiLangParser.KW_AUTH_TYPE_BASIC) | (1 << ZmeiLangParser.KW_AUTH_TYPE_SESSION) | (1 << ZmeiLangParser.KW_AUTH_TYPE_TOKEN) | (1 << ZmeiLangParser.COL_FIELD_TYPE_LONGTEXT) | (1 << ZmeiLangParser.COL_FIELD_TYPE_HTML) | (1 << ZmeiLangParser.COL_FIELD_TYPE_HTML_MEDIA) | (1 << ZmeiLangParser.COL_FIELD_TYPE_FLOAT) | (1 << ZmeiLangParser.COL_FIELD_TYPE_DECIMAL) | (1 << ZmeiLangParser.COL_FIELD_TYPE_DATE) | (1 << ZmeiLangParser.COL_FIELD_TYPE_DATETIME) | (1 << ZmeiLangParser.COL_FIELD_TYPE_CREATE_TIME) | (1 << ZmeiLangParser.COL_FIELD_TYPE_UPDATE_TIME) | (1 << ZmeiLangParser.COL_FIELD_TYPE_IMAGE) | (1 << ZmeiLangParser.COL_FIELD_TYPE_FILE) | (1 << ZmeiLangParser.COL_FIELD_TYPE_FILER_IMAGE) | (1 << ZmeiLangParser.COL_FIELD_TYPE_FILER_FILE) | (1 << ZmeiLangParser.COL_FIELD_TYPE_FILER_FOLDER) | (1 << ZmeiLangParser.COL_FIELD_TYPE_FILER_IMAGE_FOLDER) | (1 << ZmeiLangParser.COL_FIELD_TYPE_TEXT) | (1 << ZmeiLangParser.COL_FIELD_TYPE_INT) | (1 << ZmeiLangParser.COL_FIELD_TYPE_SLUG) | (1 << ZmeiLangParser.COL_FIELD_TYPE_BOOL))) != 0) or ((((_la - 64)) & ~0x3f) == 0 and ((1 << (_la - 64)) & ((1 << (ZmeiLangParser.COL_FIELD_TYPE_ONE - 64)) | (1 << (ZmeiLangParser.COL_FIELD_TYPE_ONE2ONE - 64)) | (1 << (ZmeiLangParser.COL_FIELD_TYPE_MANY - 64)) | (1 << (ZmeiLangParser.COL_FIELD_CHOICES - 64)) | (1 << (ZmeiLangParser.KW_THEME - 64)) | (1 << (ZmeiLangParser.KW_INSTALL - 64)) | (1 << (ZmeiLangParser.KW_HEADER - 64)) | (1 << (ZmeiLangParser.KW_SERVICES - 64)) | (1 << (ZmeiLangParser.KW_SELENIUM_PYTEST - 64)) | (1 << (ZmeiLangParser.KW_CHILD - 64)) | (1 << (ZmeiLangParser.KW_FILTER_OUT - 64)) | (1 << (ZmeiLangParser.KW_FILTER_IN - 64)) | (1 << (ZmeiLangParser.KW_PAGE - 64)) | (1 << (ZmeiLangParser.KW_LINK_SUFFIX - 64)) | (1 << (ZmeiLangParser.KW_URL_PREFIX - 64)) | (1 << (ZmeiLangParser.KW_CAN_EDIT - 64)) | (1 << (ZmeiLangParser.KW_OBJECT_EXPR - 64)) | (1 << (ZmeiLangParser.KW_BLOCK - 64)) | (1 << (ZmeiLangParser.KW_ITEM_NAME - 64)) | (1 << (ZmeiLangParser.KW_PK_PARAM - 64)) | (1 << (ZmeiLangParser.KW_LIST_FIELDS - 64)) | (1 << (ZmeiLangParser.KW_DELETE - 64)) | (1 << (ZmeiLangParser.KW_EDIT - 64)) | (1 << (ZmeiLangParser.KW_CREATE - 64)) | (1 << (ZmeiLangParser.KW_DETAIL - 64)) | (1 << (ZmeiLangParser.KW_SKIP - 64)) | (1 << (ZmeiLangParser.KW_FROM - 64)) | (1 << (ZmeiLangParser.KW_POLY_LIST - 64)) | (1 << (ZmeiLangParser.KW_CSS - 64)) | (1 << (ZmeiLangParser.KW_JS - 64)) | (1 << (ZmeiLangParser.KW_INLINE_TYPE_TABULAR - 64)) | (1 << (ZmeiLangParser.KW_INLINE_TYPE_STACKED - 64)) | (1 << (ZmeiLangParser.KW_INLINE_TYPE_POLYMORPHIC - 64)) | (1 << (ZmeiLangParser.KW_INLINE - 64)) | (1 << (ZmeiLangParser.KW_TYPE - 64)) | (1 << (ZmeiLangParser.KW_USER_FIELD - 64)) | (1 << (ZmeiLangParser.KW_ANNOTATE - 64)) | (1 << (ZmeiLangParser.KW_ON_CREATE - 64)) | (1 << (ZmeiLangParser.KW_QUERY - 64)) | (1 << (ZmeiLangParser.KW_AUTH - 64)) | (1 << (ZmeiLangParser.KW_COUNT - 64)) | (1 << (ZmeiLangParser.KW_I18N - 64)) | (1 << (ZmeiLangParser.KW_EXTENSION - 64)) | (1 << (ZmeiLangParser.KW_TABS - 64)) | (1 << (ZmeiLangParser.KW_LIST - 64)) | (1 << (ZmeiLangParser.KW_READ_ONLY - 64)) | (1 << (ZmeiLangParser.KW_LIST_EDITABLE - 64)) | (1 << (ZmeiLangParser.KW_LIST_FILTER - 64)) | (1 << (ZmeiLangParser.KW_LIST_SEARCH - 64)) | (1 << (ZmeiLangParser.KW_FIELDS - 64)) | (1 << (ZmeiLangParser.KW_IMPORT - 64)) | (1 << (ZmeiLangParser.KW_AS - 64)) | (1 << (ZmeiLangParser.WRITE_MODE - 64)) | (1 << (ZmeiLangParser.BOOL - 64)) | (1 << (ZmeiLangParser.ID - 64)))) != 0)):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ClassnameContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def id_or_kw(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(ZmeiLangParser.Id_or_kwContext)
            else:
                return self.getTypedRuleContext(ZmeiLangParser.Id_or_kwContext,i)


        def DOT(self, i:int=None):
            if i is None:
                return self.getTokens(ZmeiLangParser.DOT)
            else:
                return self.getToken(ZmeiLangParser.DOT, i)

        def getRuleIndex(self):
            return ZmeiLangParser.RULE_classname

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterClassname" ):
                listener.enterClassname(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitClassname" ):
                listener.exitClassname(self)




    def classname(self):

        localctx = ZmeiLangParser.ClassnameContext(self, self._ctx, self.state)
        self.enterRule(localctx, 26, self.RULE_classname)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 662
            self.id_or_kw()
            self.state = 667
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==ZmeiLangParser.DOT:
                self.state = 663
                self.match(ZmeiLangParser.DOT)
                self.state = 664
                self.id_or_kw()
                self.state = 669
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Model_refContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def HASH(self):
            return self.getToken(ZmeiLangParser.HASH, 0)

        def id_or_kw(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(ZmeiLangParser.Id_or_kwContext)
            else:
                return self.getTypedRuleContext(ZmeiLangParser.Id_or_kwContext,i)


        def DOT(self):
            return self.getToken(ZmeiLangParser.DOT, 0)

        def getRuleIndex(self):
            return ZmeiLangParser.RULE_model_ref

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterModel_ref" ):
                listener.enterModel_ref(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitModel_ref" ):
                listener.exitModel_ref(self)




    def model_ref(self):

        localctx = ZmeiLangParser.Model_refContext(self, self._ctx, self.state)
        self.enterRule(localctx, 28, self.RULE_model_ref)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 670
            self.match(ZmeiLangParser.HASH)
            self.state = 674
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,20,self._ctx)
            if la_ == 1:
                self.state = 671
                self.id_or_kw()
                self.state = 672
                self.match(ZmeiLangParser.DOT)


            self.state = 676
            self.id_or_kw()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Field_list_exprContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def STAR(self):
            return self.getToken(ZmeiLangParser.STAR, 0)

        def DOT(self):
            return self.getToken(ZmeiLangParser.DOT, 0)

        def COMA(self, i:int=None):
            if i is None:
                return self.getTokens(ZmeiLangParser.COMA)
            else:
                return self.getToken(ZmeiLangParser.COMA, i)

        def EXCLUDE(self, i:int=None):
            if i is None:
                return self.getTokens(ZmeiLangParser.EXCLUDE)
            else:
                return self.getToken(ZmeiLangParser.EXCLUDE, i)

        def field_list_expr_field(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(ZmeiLangParser.Field_list_expr_fieldContext)
            else:
                return self.getTypedRuleContext(ZmeiLangParser.Field_list_expr_fieldContext,i)


        def id_or_kw(self):
            return self.getTypedRuleContext(ZmeiLangParser.Id_or_kwContext,0)


        def getRuleIndex(self):
            return ZmeiLangParser.RULE_field_list_expr

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterField_list_expr" ):
                listener.enterField_list_expr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitField_list_expr" ):
                listener.exitField_list_expr(self)




    def field_list_expr(self):

        localctx = ZmeiLangParser.Field_list_exprContext(self, self._ctx, self.state)
        self.enterRule(localctx, 30, self.RULE_field_list_expr)
        self._la = 0 # Token type
        try:
            self.state = 701
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [ZmeiLangParser.DOT, ZmeiLangParser.STAR]:
                self.enterOuterAlt(localctx, 1)
                self.state = 679
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==ZmeiLangParser.DOT:
                    self.state = 678
                    self.match(ZmeiLangParser.DOT)


                self.state = 681
                self.match(ZmeiLangParser.STAR)
                self.state = 687
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,22,self._ctx)
                while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                    if _alt==1:
                        self.state = 682
                        self.match(ZmeiLangParser.COMA)
                        self.state = 683
                        self.match(ZmeiLangParser.EXCLUDE)
                        self.state = 684
                        self.field_list_expr_field() 
                    self.state = 689
                    self._errHandler.sync(self)
                    _alt = self._interp.adaptivePredict(self._input,22,self._ctx)

                pass
            elif token in [ZmeiLangParser.KW_AUTH_TYPE_BASIC, ZmeiLangParser.KW_AUTH_TYPE_SESSION, ZmeiLangParser.KW_AUTH_TYPE_TOKEN, ZmeiLangParser.COL_FIELD_TYPE_LONGTEXT, ZmeiLangParser.COL_FIELD_TYPE_HTML, ZmeiLangParser.COL_FIELD_TYPE_HTML_MEDIA, ZmeiLangParser.COL_FIELD_TYPE_FLOAT, ZmeiLangParser.COL_FIELD_TYPE_DECIMAL, ZmeiLangParser.COL_FIELD_TYPE_DATE, ZmeiLangParser.COL_FIELD_TYPE_DATETIME, ZmeiLangParser.COL_FIELD_TYPE_CREATE_TIME, ZmeiLangParser.COL_FIELD_TYPE_UPDATE_TIME, ZmeiLangParser.COL_FIELD_TYPE_IMAGE, ZmeiLangParser.COL_FIELD_TYPE_FILE, ZmeiLangParser.COL_FIELD_TYPE_FILER_IMAGE, ZmeiLangParser.COL_FIELD_TYPE_FILER_FILE, ZmeiLangParser.COL_FIELD_TYPE_FILER_FOLDER, ZmeiLangParser.COL_FIELD_TYPE_FILER_IMAGE_FOLDER, ZmeiLangParser.COL_FIELD_TYPE_TEXT, ZmeiLangParser.COL_FIELD_TYPE_INT, ZmeiLangParser.COL_FIELD_TYPE_SLUG, ZmeiLangParser.COL_FIELD_TYPE_BOOL, ZmeiLangParser.COL_FIELD_TYPE_ONE, ZmeiLangParser.COL_FIELD_TYPE_ONE2ONE, ZmeiLangParser.COL_FIELD_TYPE_MANY, ZmeiLangParser.COL_FIELD_CHOICES, ZmeiLangParser.KW_THEME, ZmeiLangParser.KW_INSTALL, ZmeiLangParser.KW_HEADER, ZmeiLangParser.KW_SERVICES, ZmeiLangParser.KW_SELENIUM_PYTEST, ZmeiLangParser.KW_CHILD, ZmeiLangParser.KW_FILTER_OUT, ZmeiLangParser.KW_FILTER_IN, ZmeiLangParser.KW_PAGE, ZmeiLangParser.KW_LINK_SUFFIX, ZmeiLangParser.KW_URL_PREFIX, ZmeiLangParser.KW_CAN_EDIT, ZmeiLangParser.KW_OBJECT_EXPR, ZmeiLangParser.KW_BLOCK, ZmeiLangParser.KW_ITEM_NAME, ZmeiLangParser.KW_PK_PARAM, ZmeiLangParser.KW_LIST_FIELDS, ZmeiLangParser.KW_DELETE, ZmeiLangParser.KW_EDIT, ZmeiLangParser.KW_CREATE, ZmeiLangParser.KW_DETAIL, ZmeiLangParser.KW_SKIP, ZmeiLangParser.KW_FROM, ZmeiLangParser.KW_POLY_LIST, ZmeiLangParser.KW_CSS, ZmeiLangParser.KW_JS, ZmeiLangParser.KW_INLINE_TYPE_TABULAR, ZmeiLangParser.KW_INLINE_TYPE_STACKED, ZmeiLangParser.KW_INLINE_TYPE_POLYMORPHIC, ZmeiLangParser.KW_INLINE, ZmeiLangParser.KW_TYPE, ZmeiLangParser.KW_USER_FIELD, ZmeiLangParser.KW_ANNOTATE, ZmeiLangParser.KW_ON_CREATE, ZmeiLangParser.KW_QUERY, ZmeiLangParser.KW_AUTH, ZmeiLangParser.KW_COUNT, ZmeiLangParser.KW_I18N, ZmeiLangParser.KW_EXTENSION, ZmeiLangParser.KW_TABS, ZmeiLangParser.KW_LIST, ZmeiLangParser.KW_READ_ONLY, ZmeiLangParser.KW_LIST_EDITABLE, ZmeiLangParser.KW_LIST_FILTER, ZmeiLangParser.KW_LIST_SEARCH, ZmeiLangParser.KW_FIELDS, ZmeiLangParser.KW_IMPORT, ZmeiLangParser.KW_AS, ZmeiLangParser.WRITE_MODE, ZmeiLangParser.BOOL, ZmeiLangParser.ID]:
                self.enterOuterAlt(localctx, 2)
                self.state = 690
                self.id_or_kw()
                self.state = 698
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,24,self._ctx)
                while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                    if _alt==1:
                        self.state = 691
                        self.match(ZmeiLangParser.COMA)
                        self.state = 693
                        self._errHandler.sync(self)
                        _la = self._input.LA(1)
                        if _la==ZmeiLangParser.EXCLUDE:
                            self.state = 692
                            self.match(ZmeiLangParser.EXCLUDE)


                        self.state = 695
                        self.field_list_expr_field() 
                    self.state = 700
                    self._errHandler.sync(self)
                    _alt = self._interp.adaptivePredict(self._input,24,self._ctx)

                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Field_list_expr_fieldContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def id_or_kw(self):
            return self.getTypedRuleContext(ZmeiLangParser.Id_or_kwContext,0)


        def STAR(self, i:int=None):
            if i is None:
                return self.getTokens(ZmeiLangParser.STAR)
            else:
                return self.getToken(ZmeiLangParser.STAR, i)

        def getRuleIndex(self):
            return ZmeiLangParser.RULE_field_list_expr_field

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterField_list_expr_field" ):
                listener.enterField_list_expr_field(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitField_list_expr_field" ):
                listener.exitField_list_expr_field(self)




    def field_list_expr_field(self):

        localctx = ZmeiLangParser.Field_list_expr_fieldContext(self, self._ctx, self.state)
        self.enterRule(localctx, 32, self.RULE_field_list_expr_field)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 704
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==ZmeiLangParser.STAR:
                self.state = 703
                self.match(ZmeiLangParser.STAR)


            self.state = 706
            self.id_or_kw()
            self.state = 708
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==ZmeiLangParser.STAR:
                self.state = 707
                self.match(ZmeiLangParser.STAR)


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Write_mode_exprContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def SQ_BRACE_OPEN(self):
            return self.getToken(ZmeiLangParser.SQ_BRACE_OPEN, 0)

        def WRITE_MODE(self):
            return self.getToken(ZmeiLangParser.WRITE_MODE, 0)

        def SQ_BRACE_CLOSE(self):
            return self.getToken(ZmeiLangParser.SQ_BRACE_CLOSE, 0)

        def getRuleIndex(self):
            return ZmeiLangParser.RULE_write_mode_expr

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterWrite_mode_expr" ):
                listener.enterWrite_mode_expr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitWrite_mode_expr" ):
                listener.exitWrite_mode_expr(self)




    def write_mode_expr(self):

        localctx = ZmeiLangParser.Write_mode_exprContext(self, self._ctx, self.state)
        self.enterRule(localctx, 34, self.RULE_write_mode_expr)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 710
            self.match(ZmeiLangParser.SQ_BRACE_OPEN)
            self.state = 711
            self.match(ZmeiLangParser.WRITE_MODE)
            self.state = 712
            self.match(ZmeiLangParser.SQ_BRACE_CLOSE)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Python_codeContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def code_block(self):
            return self.getTypedRuleContext(ZmeiLangParser.Code_blockContext,0)


        def code_line(self):
            return self.getTypedRuleContext(ZmeiLangParser.Code_lineContext,0)


        def getRuleIndex(self):
            return ZmeiLangParser.RULE_python_code

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPython_code" ):
                listener.enterPython_code(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPython_code" ):
                listener.exitPython_code(self)




    def python_code(self):

        localctx = ZmeiLangParser.Python_codeContext(self, self._ctx, self.state)
        self.enterRule(localctx, 36, self.RULE_python_code)
        try:
            self.state = 716
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [ZmeiLangParser.CODE_BLOCK]:
                self.enterOuterAlt(localctx, 1)
                self.state = 714
                self.code_block()
                pass
            elif token in [ZmeiLangParser.ASSIGN]:
                self.enterOuterAlt(localctx, 2)
                self.state = 715
                self.code_line()
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Code_lineContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ASSIGN(self):
            return self.getToken(ZmeiLangParser.ASSIGN, 0)

        def PYTHON_CODE(self):
            return self.getToken(ZmeiLangParser.PYTHON_CODE, 0)

        def NL(self):
            return self.getToken(ZmeiLangParser.NL, 0)

        def getRuleIndex(self):
            return ZmeiLangParser.RULE_code_line

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterCode_line" ):
                listener.enterCode_line(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitCode_line" ):
                listener.exitCode_line(self)




    def code_line(self):

        localctx = ZmeiLangParser.Code_lineContext(self, self._ctx, self.state)
        self.enterRule(localctx, 38, self.RULE_code_line)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 718
            self.match(ZmeiLangParser.ASSIGN)
            self.state = 719
            self.match(ZmeiLangParser.PYTHON_CODE)
            self.state = 720
            self.match(ZmeiLangParser.NL)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Code_blockContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def CODE_BLOCK(self):
            return self.getToken(ZmeiLangParser.CODE_BLOCK, 0)

        def getRuleIndex(self):
            return ZmeiLangParser.RULE_code_block

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterCode_block" ):
                listener.enterCode_block(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitCode_block" ):
                listener.exitCode_block(self)




    def code_block(self):

        localctx = ZmeiLangParser.Code_blockContext(self, self._ctx, self.state)
        self.enterRule(localctx, 40, self.RULE_code_block)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 722
            self.match(ZmeiLangParser.CODE_BLOCK)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Cs_annotationContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def an_suit(self):
            return self.getTypedRuleContext(ZmeiLangParser.An_suitContext,0)


        def an_celery(self):
            return self.getTypedRuleContext(ZmeiLangParser.An_celeryContext,0)


        def an_channels(self):
            return self.getTypedRuleContext(ZmeiLangParser.An_channelsContext,0)


        def an_docker(self):
            return self.getTypedRuleContext(ZmeiLangParser.An_dockerContext,0)


        def an_filer(self):
            return self.getTypedRuleContext(ZmeiLangParser.An_filerContext,0)


        def an_gitlab(self):
            return self.getTypedRuleContext(ZmeiLangParser.An_gitlabContext,0)


        def an_file(self):
            return self.getTypedRuleContext(ZmeiLangParser.An_fileContext,0)


        def an_theme(self):
            return self.getTypedRuleContext(ZmeiLangParser.An_themeContext,0)


        def an_langs(self):
            return self.getTypedRuleContext(ZmeiLangParser.An_langsContext,0)


        def NL(self):
            return self.getToken(ZmeiLangParser.NL, 0)

        def getRuleIndex(self):
            return ZmeiLangParser.RULE_cs_annotation

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterCs_annotation" ):
                listener.enterCs_annotation(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitCs_annotation" ):
                listener.exitCs_annotation(self)




    def cs_annotation(self):

        localctx = ZmeiLangParser.Cs_annotationContext(self, self._ctx, self.state)
        self.enterRule(localctx, 42, self.RULE_cs_annotation)
        try:
            self.state = 734
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [ZmeiLangParser.AN_SUIT]:
                self.enterOuterAlt(localctx, 1)
                self.state = 724
                self.an_suit()
                pass
            elif token in [ZmeiLangParser.AN_CELERY]:
                self.enterOuterAlt(localctx, 2)
                self.state = 725
                self.an_celery()
                pass
            elif token in [ZmeiLangParser.AN_CHANNELS]:
                self.enterOuterAlt(localctx, 3)
                self.state = 726
                self.an_channels()
                pass
            elif token in [ZmeiLangParser.AN_DOCKER]:
                self.enterOuterAlt(localctx, 4)
                self.state = 727
                self.an_docker()
                pass
            elif token in [ZmeiLangParser.AN_FILER]:
                self.enterOuterAlt(localctx, 5)
                self.state = 728
                self.an_filer()
                pass
            elif token in [ZmeiLangParser.AN_GITLAB]:
                self.enterOuterAlt(localctx, 6)
                self.state = 729
                self.an_gitlab()
                pass
            elif token in [ZmeiLangParser.AN_FILE]:
                self.enterOuterAlt(localctx, 7)
                self.state = 730
                self.an_file()
                pass
            elif token in [ZmeiLangParser.AN_THEME]:
                self.enterOuterAlt(localctx, 8)
                self.state = 731
                self.an_theme()
                pass
            elif token in [ZmeiLangParser.AN_LANGS]:
                self.enterOuterAlt(localctx, 9)
                self.state = 732
                self.an_langs()
                pass
            elif token in [ZmeiLangParser.NL]:
                self.enterOuterAlt(localctx, 10)
                self.state = 733
                self.match(ZmeiLangParser.NL)
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class An_suitContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def AN_SUIT(self):
            return self.getToken(ZmeiLangParser.AN_SUIT, 0)

        def BRACE_OPEN(self):
            return self.getToken(ZmeiLangParser.BRACE_OPEN, 0)

        def an_suit_app_name(self):
            return self.getTypedRuleContext(ZmeiLangParser.An_suit_app_nameContext,0)


        def BRACE_CLOSE(self):
            return self.getToken(ZmeiLangParser.BRACE_CLOSE, 0)

        def getRuleIndex(self):
            return ZmeiLangParser.RULE_an_suit

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAn_suit" ):
                listener.enterAn_suit(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAn_suit" ):
                listener.exitAn_suit(self)




    def an_suit(self):

        localctx = ZmeiLangParser.An_suitContext(self, self._ctx, self.state)
        self.enterRule(localctx, 44, self.RULE_an_suit)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 736
            self.match(ZmeiLangParser.AN_SUIT)
            self.state = 741
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==ZmeiLangParser.BRACE_OPEN:
                self.state = 737
                self.match(ZmeiLangParser.BRACE_OPEN)
                self.state = 738
                self.an_suit_app_name()
                self.state = 739
                self.match(ZmeiLangParser.BRACE_CLOSE)


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class An_suit_app_nameContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def STRING_DQ(self):
            return self.getToken(ZmeiLangParser.STRING_DQ, 0)

        def STRING_SQ(self):
            return self.getToken(ZmeiLangParser.STRING_SQ, 0)

        def getRuleIndex(self):
            return ZmeiLangParser.RULE_an_suit_app_name

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAn_suit_app_name" ):
                listener.enterAn_suit_app_name(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAn_suit_app_name" ):
                listener.exitAn_suit_app_name(self)




    def an_suit_app_name(self):

        localctx = ZmeiLangParser.An_suit_app_nameContext(self, self._ctx, self.state)
        self.enterRule(localctx, 46, self.RULE_an_suit_app_name)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 743
            _la = self._input.LA(1)
            if not(_la==ZmeiLangParser.STRING_DQ or _la==ZmeiLangParser.STRING_SQ):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class An_celeryContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def AN_CELERY(self):
            return self.getToken(ZmeiLangParser.AN_CELERY, 0)

        def BRACE_OPEN(self):
            return self.getToken(ZmeiLangParser.BRACE_OPEN, 0)

        def BRACE_CLOSE(self):
            return self.getToken(ZmeiLangParser.BRACE_CLOSE, 0)

        def getRuleIndex(self):
            return ZmeiLangParser.RULE_an_celery

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAn_celery" ):
                listener.enterAn_celery(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAn_celery" ):
                listener.exitAn_celery(self)




    def an_celery(self):

        localctx = ZmeiLangParser.An_celeryContext(self, self._ctx, self.state)
        self.enterRule(localctx, 48, self.RULE_an_celery)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 745
            self.match(ZmeiLangParser.AN_CELERY)
            self.state = 748
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==ZmeiLangParser.BRACE_OPEN:
                self.state = 746
                self.match(ZmeiLangParser.BRACE_OPEN)
                self.state = 747
                self.match(ZmeiLangParser.BRACE_CLOSE)


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class An_channelsContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def AN_CHANNELS(self):
            return self.getToken(ZmeiLangParser.AN_CHANNELS, 0)

        def BRACE_OPEN(self):
            return self.getToken(ZmeiLangParser.BRACE_OPEN, 0)

        def BRACE_CLOSE(self):
            return self.getToken(ZmeiLangParser.BRACE_CLOSE, 0)

        def getRuleIndex(self):
            return ZmeiLangParser.RULE_an_channels

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAn_channels" ):
                listener.enterAn_channels(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAn_channels" ):
                listener.exitAn_channels(self)




    def an_channels(self):

        localctx = ZmeiLangParser.An_channelsContext(self, self._ctx, self.state)
        self.enterRule(localctx, 50, self.RULE_an_channels)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 750
            self.match(ZmeiLangParser.AN_CHANNELS)
            self.state = 753
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==ZmeiLangParser.BRACE_OPEN:
                self.state = 751
                self.match(ZmeiLangParser.BRACE_OPEN)
                self.state = 752
                self.match(ZmeiLangParser.BRACE_CLOSE)


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class An_dockerContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def AN_DOCKER(self):
            return self.getToken(ZmeiLangParser.AN_DOCKER, 0)

        def BRACE_OPEN(self):
            return self.getToken(ZmeiLangParser.BRACE_OPEN, 0)

        def BRACE_CLOSE(self):
            return self.getToken(ZmeiLangParser.BRACE_CLOSE, 0)

        def getRuleIndex(self):
            return ZmeiLangParser.RULE_an_docker

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAn_docker" ):
                listener.enterAn_docker(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAn_docker" ):
                listener.exitAn_docker(self)




    def an_docker(self):

        localctx = ZmeiLangParser.An_dockerContext(self, self._ctx, self.state)
        self.enterRule(localctx, 52, self.RULE_an_docker)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 755
            self.match(ZmeiLangParser.AN_DOCKER)
            self.state = 758
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==ZmeiLangParser.BRACE_OPEN:
                self.state = 756
                self.match(ZmeiLangParser.BRACE_OPEN)
                self.state = 757
                self.match(ZmeiLangParser.BRACE_CLOSE)


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class An_filerContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def AN_FILER(self):
            return self.getToken(ZmeiLangParser.AN_FILER, 0)

        def BRACE_OPEN(self):
            return self.getToken(ZmeiLangParser.BRACE_OPEN, 0)

        def BRACE_CLOSE(self):
            return self.getToken(ZmeiLangParser.BRACE_CLOSE, 0)

        def getRuleIndex(self):
            return ZmeiLangParser.RULE_an_filer

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAn_filer" ):
                listener.enterAn_filer(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAn_filer" ):
                listener.exitAn_filer(self)




    def an_filer(self):

        localctx = ZmeiLangParser.An_filerContext(self, self._ctx, self.state)
        self.enterRule(localctx, 54, self.RULE_an_filer)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 760
            self.match(ZmeiLangParser.AN_FILER)
            self.state = 763
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==ZmeiLangParser.BRACE_OPEN:
                self.state = 761
                self.match(ZmeiLangParser.BRACE_OPEN)
                self.state = 762
                self.match(ZmeiLangParser.BRACE_CLOSE)


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class An_gitlabContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def AN_GITLAB(self):
            return self.getToken(ZmeiLangParser.AN_GITLAB, 0)

        def BRACE_OPEN(self):
            return self.getToken(ZmeiLangParser.BRACE_OPEN, 0)

        def BRACE_CLOSE(self):
            return self.getToken(ZmeiLangParser.BRACE_CLOSE, 0)

        def NL(self, i:int=None):
            if i is None:
                return self.getTokens(ZmeiLangParser.NL)
            else:
                return self.getToken(ZmeiLangParser.NL, i)

        def an_gitlab_test_declaration(self):
            return self.getTypedRuleContext(ZmeiLangParser.An_gitlab_test_declarationContext,0)


        def an_gitlab_branch_declaration(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(ZmeiLangParser.An_gitlab_branch_declarationContext)
            else:
                return self.getTypedRuleContext(ZmeiLangParser.An_gitlab_branch_declarationContext,i)


        def getRuleIndex(self):
            return ZmeiLangParser.RULE_an_gitlab

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAn_gitlab" ):
                listener.enterAn_gitlab(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAn_gitlab" ):
                listener.exitAn_gitlab(self)




    def an_gitlab(self):

        localctx = ZmeiLangParser.An_gitlabContext(self, self._ctx, self.state)
        self.enterRule(localctx, 56, self.RULE_an_gitlab)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 765
            self.match(ZmeiLangParser.AN_GITLAB)
            self.state = 766
            self.match(ZmeiLangParser.BRACE_OPEN)
            self.state = 770
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,35,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 767
                    self.match(ZmeiLangParser.NL) 
                self.state = 772
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,35,self._ctx)

            self.state = 774
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,36,self._ctx)
            if la_ == 1:
                self.state = 773
                self.an_gitlab_test_declaration()


            self.state = 779
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==ZmeiLangParser.NL:
                self.state = 776
                self.match(ZmeiLangParser.NL)
                self.state = 781
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 783 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 782
                self.an_gitlab_branch_declaration()
                self.state = 785 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not (((((_la - 42)) & ~0x3f) == 0 and ((1 << (_la - 42)) & ((1 << (ZmeiLangParser.KW_AUTH_TYPE_BASIC - 42)) | (1 << (ZmeiLangParser.KW_AUTH_TYPE_SESSION - 42)) | (1 << (ZmeiLangParser.KW_AUTH_TYPE_TOKEN - 42)) | (1 << (ZmeiLangParser.COL_FIELD_TYPE_LONGTEXT - 42)) | (1 << (ZmeiLangParser.COL_FIELD_TYPE_HTML - 42)) | (1 << (ZmeiLangParser.COL_FIELD_TYPE_HTML_MEDIA - 42)) | (1 << (ZmeiLangParser.COL_FIELD_TYPE_FLOAT - 42)) | (1 << (ZmeiLangParser.COL_FIELD_TYPE_DECIMAL - 42)) | (1 << (ZmeiLangParser.COL_FIELD_TYPE_DATE - 42)) | (1 << (ZmeiLangParser.COL_FIELD_TYPE_DATETIME - 42)) | (1 << (ZmeiLangParser.COL_FIELD_TYPE_CREATE_TIME - 42)) | (1 << (ZmeiLangParser.COL_FIELD_TYPE_UPDATE_TIME - 42)) | (1 << (ZmeiLangParser.COL_FIELD_TYPE_IMAGE - 42)) | (1 << (ZmeiLangParser.COL_FIELD_TYPE_FILE - 42)) | (1 << (ZmeiLangParser.COL_FIELD_TYPE_FILER_IMAGE - 42)) | (1 << (ZmeiLangParser.COL_FIELD_TYPE_FILER_FILE - 42)) | (1 << (ZmeiLangParser.COL_FIELD_TYPE_FILER_FOLDER - 42)) | (1 << (ZmeiLangParser.COL_FIELD_TYPE_FILER_IMAGE_FOLDER - 42)) | (1 << (ZmeiLangParser.COL_FIELD_TYPE_TEXT - 42)) | (1 << (ZmeiLangParser.COL_FIELD_TYPE_INT - 42)) | (1 << (ZmeiLangParser.COL_FIELD_TYPE_SLUG - 42)) | (1 << (ZmeiLangParser.COL_FIELD_TYPE_BOOL - 42)) | (1 << (ZmeiLangParser.COL_FIELD_TYPE_ONE - 42)) | (1 << (ZmeiLangParser.COL_FIELD_TYPE_ONE2ONE - 42)) | (1 << (ZmeiLangParser.COL_FIELD_TYPE_MANY - 42)) | (1 << (ZmeiLangParser.COL_FIELD_CHOICES - 42)) | (1 << (ZmeiLangParser.KW_THEME - 42)) | (1 << (ZmeiLangParser.KW_INSTALL - 42)) | (1 << (ZmeiLangParser.KW_HEADER - 42)) | (1 << (ZmeiLangParser.KW_SERVICES - 42)) | (1 << (ZmeiLangParser.KW_SELENIUM_PYTEST - 42)) | (1 << (ZmeiLangParser.KW_CHILD - 42)) | (1 << (ZmeiLangParser.KW_FILTER_OUT - 42)) | (1 << (ZmeiLangParser.KW_FILTER_IN - 42)) | (1 << (ZmeiLangParser.KW_PAGE - 42)) | (1 << (ZmeiLangParser.KW_LINK_SUFFIX - 42)) | (1 << (ZmeiLangParser.KW_URL_PREFIX - 42)) | (1 << (ZmeiLangParser.KW_CAN_EDIT - 42)) | (1 << (ZmeiLangParser.KW_OBJECT_EXPR - 42)) | (1 << (ZmeiLangParser.KW_BLOCK - 42)) | (1 << (ZmeiLangParser.KW_ITEM_NAME - 42)) | (1 << (ZmeiLangParser.KW_PK_PARAM - 42)) | (1 << (ZmeiLangParser.KW_LIST_FIELDS - 42)) | (1 << (ZmeiLangParser.KW_DELETE - 42)) | (1 << (ZmeiLangParser.KW_EDIT - 42)) | (1 << (ZmeiLangParser.KW_CREATE - 42)) | (1 << (ZmeiLangParser.KW_DETAIL - 42)) | (1 << (ZmeiLangParser.KW_SKIP - 42)) | (1 << (ZmeiLangParser.KW_FROM - 42)) | (1 << (ZmeiLangParser.KW_POLY_LIST - 42)) | (1 << (ZmeiLangParser.KW_CSS - 42)) | (1 << (ZmeiLangParser.KW_JS - 42)) | (1 << (ZmeiLangParser.KW_INLINE_TYPE_TABULAR - 42)) | (1 << (ZmeiLangParser.KW_INLINE_TYPE_STACKED - 42)) | (1 << (ZmeiLangParser.KW_INLINE_TYPE_POLYMORPHIC - 42)) | (1 << (ZmeiLangParser.KW_INLINE - 42)) | (1 << (ZmeiLangParser.KW_TYPE - 42)) | (1 << (ZmeiLangParser.KW_USER_FIELD - 42)) | (1 << (ZmeiLangParser.KW_ANNOTATE - 42)) | (1 << (ZmeiLangParser.KW_ON_CREATE - 42)) | (1 << (ZmeiLangParser.KW_QUERY - 42)) | (1 << (ZmeiLangParser.KW_AUTH - 42)) | (1 << (ZmeiLangParser.KW_COUNT - 42)) | (1 << (ZmeiLangParser.KW_I18N - 42)))) != 0) or ((((_la - 106)) & ~0x3f) == 0 and ((1 << (_la - 106)) & ((1 << (ZmeiLangParser.KW_EXTENSION - 106)) | (1 << (ZmeiLangParser.KW_TABS - 106)) | (1 << (ZmeiLangParser.KW_LIST - 106)) | (1 << (ZmeiLangParser.KW_READ_ONLY - 106)) | (1 << (ZmeiLangParser.KW_LIST_EDITABLE - 106)) | (1 << (ZmeiLangParser.KW_LIST_FILTER - 106)) | (1 << (ZmeiLangParser.KW_LIST_SEARCH - 106)) | (1 << (ZmeiLangParser.KW_FIELDS - 106)) | (1 << (ZmeiLangParser.KW_IMPORT - 106)) | (1 << (ZmeiLangParser.KW_AS - 106)) | (1 << (ZmeiLangParser.WRITE_MODE - 106)) | (1 << (ZmeiLangParser.BOOL - 106)) | (1 << (ZmeiLangParser.ID - 106)) | (1 << (ZmeiLangParser.DASH - 106)) | (1 << (ZmeiLangParser.SLASH - 106)) | (1 << (ZmeiLangParser.STAR - 106)))) != 0)):
                    break

            self.state = 790
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==ZmeiLangParser.NL:
                self.state = 787
                self.match(ZmeiLangParser.NL)
                self.state = 792
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 793
            self.match(ZmeiLangParser.BRACE_CLOSE)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class An_gitlab_test_declarationContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def an_gitlab_test_declaration_selenium_pytest(self):
            return self.getTypedRuleContext(ZmeiLangParser.An_gitlab_test_declaration_selenium_pytestContext,0)


        def getRuleIndex(self):
            return ZmeiLangParser.RULE_an_gitlab_test_declaration

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAn_gitlab_test_declaration" ):
                listener.enterAn_gitlab_test_declaration(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAn_gitlab_test_declaration" ):
                listener.exitAn_gitlab_test_declaration(self)




    def an_gitlab_test_declaration(self):

        localctx = ZmeiLangParser.An_gitlab_test_declarationContext(self, self._ctx, self.state)
        self.enterRule(localctx, 58, self.RULE_an_gitlab_test_declaration)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 795
            self.an_gitlab_test_declaration_selenium_pytest()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class An_gitlab_test_declaration_selenium_pytestContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def KW_SELENIUM_PYTEST(self):
            return self.getToken(ZmeiLangParser.KW_SELENIUM_PYTEST, 0)

        def BRACE_OPEN(self):
            return self.getToken(ZmeiLangParser.BRACE_OPEN, 0)

        def BRACE_CLOSE(self):
            return self.getToken(ZmeiLangParser.BRACE_CLOSE, 0)

        def NL(self, i:int=None):
            if i is None:
                return self.getTokens(ZmeiLangParser.NL)
            else:
                return self.getToken(ZmeiLangParser.NL, i)

        def an_gitlab_test_services(self):
            return self.getTypedRuleContext(ZmeiLangParser.An_gitlab_test_servicesContext,0)


        def an_gitlab_deployment_variable(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(ZmeiLangParser.An_gitlab_deployment_variableContext)
            else:
                return self.getTypedRuleContext(ZmeiLangParser.An_gitlab_deployment_variableContext,i)


        def COMA(self, i:int=None):
            if i is None:
                return self.getTokens(ZmeiLangParser.COMA)
            else:
                return self.getToken(ZmeiLangParser.COMA, i)

        def getRuleIndex(self):
            return ZmeiLangParser.RULE_an_gitlab_test_declaration_selenium_pytest

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAn_gitlab_test_declaration_selenium_pytest" ):
                listener.enterAn_gitlab_test_declaration_selenium_pytest(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAn_gitlab_test_declaration_selenium_pytest" ):
                listener.exitAn_gitlab_test_declaration_selenium_pytest(self)




    def an_gitlab_test_declaration_selenium_pytest(self):

        localctx = ZmeiLangParser.An_gitlab_test_declaration_selenium_pytestContext(self, self._ctx, self.state)
        self.enterRule(localctx, 60, self.RULE_an_gitlab_test_declaration_selenium_pytest)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 797
            self.match(ZmeiLangParser.KW_SELENIUM_PYTEST)
            self.state = 798
            self.match(ZmeiLangParser.BRACE_OPEN)
            self.state = 802
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,40,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 799
                    self.match(ZmeiLangParser.NL) 
                self.state = 804
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,40,self._ctx)

            self.state = 806
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,41,self._ctx)
            if la_ == 1:
                self.state = 805
                self.an_gitlab_test_services()


            self.state = 811
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,42,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 808
                    self.match(ZmeiLangParser.NL) 
                self.state = 813
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,42,self._ctx)

            self.state = 820
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,44,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 814
                    self.an_gitlab_deployment_variable()
                    self.state = 816
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    if _la==ZmeiLangParser.COMA:
                        self.state = 815
                        self.match(ZmeiLangParser.COMA)

             
                self.state = 822
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,44,self._ctx)

            self.state = 826
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==ZmeiLangParser.NL:
                self.state = 823
                self.match(ZmeiLangParser.NL)
                self.state = 828
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 829
            self.match(ZmeiLangParser.BRACE_CLOSE)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class An_gitlab_test_servicesContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def KW_SERVICES(self):
            return self.getToken(ZmeiLangParser.KW_SERVICES, 0)

        def BRACE_OPEN(self):
            return self.getToken(ZmeiLangParser.BRACE_OPEN, 0)

        def BRACE_CLOSE(self):
            return self.getToken(ZmeiLangParser.BRACE_CLOSE, 0)

        def NL(self, i:int=None):
            if i is None:
                return self.getTokens(ZmeiLangParser.NL)
            else:
                return self.getToken(ZmeiLangParser.NL, i)

        def an_gitlab_test_service(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(ZmeiLangParser.An_gitlab_test_serviceContext)
            else:
                return self.getTypedRuleContext(ZmeiLangParser.An_gitlab_test_serviceContext,i)


        def COMA(self, i:int=None):
            if i is None:
                return self.getTokens(ZmeiLangParser.COMA)
            else:
                return self.getToken(ZmeiLangParser.COMA, i)

        def getRuleIndex(self):
            return ZmeiLangParser.RULE_an_gitlab_test_services

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAn_gitlab_test_services" ):
                listener.enterAn_gitlab_test_services(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAn_gitlab_test_services" ):
                listener.exitAn_gitlab_test_services(self)




    def an_gitlab_test_services(self):

        localctx = ZmeiLangParser.An_gitlab_test_servicesContext(self, self._ctx, self.state)
        self.enterRule(localctx, 62, self.RULE_an_gitlab_test_services)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 831
            self.match(ZmeiLangParser.KW_SERVICES)
            self.state = 832
            self.match(ZmeiLangParser.BRACE_OPEN)
            self.state = 836
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,46,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 833
                    self.match(ZmeiLangParser.NL) 
                self.state = 838
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,46,self._ctx)

            self.state = 847
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,48,self._ctx)
            if la_ == 1:
                self.state = 839
                self.an_gitlab_test_service()
                self.state = 844
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la==ZmeiLangParser.COMA:
                    self.state = 840
                    self.match(ZmeiLangParser.COMA)
                    self.state = 841
                    self.an_gitlab_test_service()
                    self.state = 846
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)



            self.state = 852
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==ZmeiLangParser.NL:
                self.state = 849
                self.match(ZmeiLangParser.NL)
                self.state = 854
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 855
            self.match(ZmeiLangParser.BRACE_CLOSE)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class An_gitlab_test_serviceContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def an_gitlab_test_service_name(self):
            return self.getTypedRuleContext(ZmeiLangParser.An_gitlab_test_service_nameContext,0)


        def NL(self, i:int=None):
            if i is None:
                return self.getTokens(ZmeiLangParser.NL)
            else:
                return self.getToken(ZmeiLangParser.NL, i)

        def BRACE_OPEN(self):
            return self.getToken(ZmeiLangParser.BRACE_OPEN, 0)

        def BRACE_CLOSE(self):
            return self.getToken(ZmeiLangParser.BRACE_CLOSE, 0)

        def an_gitlab_deployment_variable(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(ZmeiLangParser.An_gitlab_deployment_variableContext)
            else:
                return self.getTypedRuleContext(ZmeiLangParser.An_gitlab_deployment_variableContext,i)


        def COMA(self, i:int=None):
            if i is None:
                return self.getTokens(ZmeiLangParser.COMA)
            else:
                return self.getToken(ZmeiLangParser.COMA, i)

        def getRuleIndex(self):
            return ZmeiLangParser.RULE_an_gitlab_test_service

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAn_gitlab_test_service" ):
                listener.enterAn_gitlab_test_service(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAn_gitlab_test_service" ):
                listener.exitAn_gitlab_test_service(self)




    def an_gitlab_test_service(self):

        localctx = ZmeiLangParser.An_gitlab_test_serviceContext(self, self._ctx, self.state)
        self.enterRule(localctx, 64, self.RULE_an_gitlab_test_service)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 860
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==ZmeiLangParser.NL:
                self.state = 857
                self.match(ZmeiLangParser.NL)
                self.state = 862
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 863
            self.an_gitlab_test_service_name()
            self.state = 887
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==ZmeiLangParser.BRACE_OPEN:
                self.state = 864
                self.match(ZmeiLangParser.BRACE_OPEN)
                self.state = 868
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,51,self._ctx)
                while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                    if _alt==1:
                        self.state = 865
                        self.match(ZmeiLangParser.NL) 
                    self.state = 870
                    self._errHandler.sync(self)
                    _alt = self._interp.adaptivePredict(self._input,51,self._ctx)

                self.state = 877
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,53,self._ctx)
                while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                    if _alt==1:
                        self.state = 871
                        self.an_gitlab_deployment_variable()
                        self.state = 873
                        self._errHandler.sync(self)
                        _la = self._input.LA(1)
                        if _la==ZmeiLangParser.COMA:
                            self.state = 872
                            self.match(ZmeiLangParser.COMA)

                 
                    self.state = 879
                    self._errHandler.sync(self)
                    _alt = self._interp.adaptivePredict(self._input,53,self._ctx)

                self.state = 883
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la==ZmeiLangParser.NL:
                    self.state = 880
                    self.match(ZmeiLangParser.NL)
                    self.state = 885
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                self.state = 886
                self.match(ZmeiLangParser.BRACE_CLOSE)


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class An_gitlab_test_service_nameContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def id_or_kw(self):
            return self.getTypedRuleContext(ZmeiLangParser.Id_or_kwContext,0)


        def getRuleIndex(self):
            return ZmeiLangParser.RULE_an_gitlab_test_service_name

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAn_gitlab_test_service_name" ):
                listener.enterAn_gitlab_test_service_name(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAn_gitlab_test_service_name" ):
                listener.exitAn_gitlab_test_service_name(self)




    def an_gitlab_test_service_name(self):

        localctx = ZmeiLangParser.An_gitlab_test_service_nameContext(self, self._ctx, self.state)
        self.enterRule(localctx, 66, self.RULE_an_gitlab_test_service_name)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 889
            self.id_or_kw()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class An_gitlab_branch_declarationContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def an_gitlab_branch_name(self):
            return self.getTypedRuleContext(ZmeiLangParser.An_gitlab_branch_nameContext,0)


        def an_gitlab_branch_deploy_type(self):
            return self.getTypedRuleContext(ZmeiLangParser.An_gitlab_branch_deploy_typeContext,0)


        def an_gitlab_deployment_name(self):
            return self.getTypedRuleContext(ZmeiLangParser.An_gitlab_deployment_nameContext,0)


        def BRACE_OPEN(self):
            return self.getToken(ZmeiLangParser.BRACE_OPEN, 0)

        def an_gitlab_deployment_host(self):
            return self.getTypedRuleContext(ZmeiLangParser.An_gitlab_deployment_hostContext,0)


        def BRACE_CLOSE(self):
            return self.getToken(ZmeiLangParser.BRACE_CLOSE, 0)

        def NL(self, i:int=None):
            if i is None:
                return self.getTokens(ZmeiLangParser.NL)
            else:
                return self.getToken(ZmeiLangParser.NL, i)

        def COLON(self):
            return self.getToken(ZmeiLangParser.COLON, 0)

        def an_gitlab_deployment_variable(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(ZmeiLangParser.An_gitlab_deployment_variableContext)
            else:
                return self.getTypedRuleContext(ZmeiLangParser.An_gitlab_deployment_variableContext,i)


        def COMA(self, i:int=None):
            if i is None:
                return self.getTokens(ZmeiLangParser.COMA)
            else:
                return self.getToken(ZmeiLangParser.COMA, i)

        def getRuleIndex(self):
            return ZmeiLangParser.RULE_an_gitlab_branch_declaration

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAn_gitlab_branch_declaration" ):
                listener.enterAn_gitlab_branch_declaration(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAn_gitlab_branch_declaration" ):
                listener.exitAn_gitlab_branch_declaration(self)




    def an_gitlab_branch_declaration(self):

        localctx = ZmeiLangParser.An_gitlab_branch_declarationContext(self, self._ctx, self.state)
        self.enterRule(localctx, 68, self.RULE_an_gitlab_branch_declaration)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 891
            self.an_gitlab_branch_name()
            self.state = 895
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==ZmeiLangParser.NL:
                self.state = 892
                self.match(ZmeiLangParser.NL)
                self.state = 897
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 898
            self.an_gitlab_branch_deploy_type()
            self.state = 902
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==ZmeiLangParser.NL:
                self.state = 899
                self.match(ZmeiLangParser.NL)
                self.state = 904
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 905
            self.an_gitlab_deployment_name()
            self.state = 906
            self.match(ZmeiLangParser.BRACE_OPEN)
            self.state = 910
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==ZmeiLangParser.NL:
                self.state = 907
                self.match(ZmeiLangParser.NL)
                self.state = 912
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 913
            self.an_gitlab_deployment_host()
            self.state = 930
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==ZmeiLangParser.COLON:
                self.state = 914
                self.match(ZmeiLangParser.COLON)
                self.state = 918
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,59,self._ctx)
                while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                    if _alt==1:
                        self.state = 915
                        self.match(ZmeiLangParser.NL) 
                    self.state = 920
                    self._errHandler.sync(self)
                    _alt = self._interp.adaptivePredict(self._input,59,self._ctx)

                self.state = 927
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,61,self._ctx)
                while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                    if _alt==1:
                        self.state = 921
                        self.an_gitlab_deployment_variable()
                        self.state = 923
                        self._errHandler.sync(self)
                        _la = self._input.LA(1)
                        if _la==ZmeiLangParser.COMA:
                            self.state = 922
                            self.match(ZmeiLangParser.COMA)

                 
                    self.state = 929
                    self._errHandler.sync(self)
                    _alt = self._interp.adaptivePredict(self._input,61,self._ctx)



            self.state = 935
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==ZmeiLangParser.NL:
                self.state = 932
                self.match(ZmeiLangParser.NL)
                self.state = 937
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 938
            self.match(ZmeiLangParser.BRACE_CLOSE)
            self.state = 942
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,64,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 939
                    self.match(ZmeiLangParser.NL) 
                self.state = 944
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,64,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class An_gitlab_branch_deploy_typeContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def GT(self):
            return self.getToken(ZmeiLangParser.GT, 0)

        def EQUALS(self):
            return self.getToken(ZmeiLangParser.EQUALS, 0)

        def APPROX(self):
            return self.getToken(ZmeiLangParser.APPROX, 0)

        def getRuleIndex(self):
            return ZmeiLangParser.RULE_an_gitlab_branch_deploy_type

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAn_gitlab_branch_deploy_type" ):
                listener.enterAn_gitlab_branch_deploy_type(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAn_gitlab_branch_deploy_type" ):
                listener.exitAn_gitlab_branch_deploy_type(self)




    def an_gitlab_branch_deploy_type(self):

        localctx = ZmeiLangParser.An_gitlab_branch_deploy_typeContext(self, self._ctx, self.state)
        self.enterRule(localctx, 70, self.RULE_an_gitlab_branch_deploy_type)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 945
            _la = self._input.LA(1)
            if not(_la==ZmeiLangParser.EQUALS or _la==ZmeiLangParser.APPROX):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
            self.state = 946
            self.match(ZmeiLangParser.GT)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class An_gitlab_branch_nameContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def id_or_kw(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(ZmeiLangParser.Id_or_kwContext)
            else:
                return self.getTypedRuleContext(ZmeiLangParser.Id_or_kwContext,i)


        def DASH(self, i:int=None):
            if i is None:
                return self.getTokens(ZmeiLangParser.DASH)
            else:
                return self.getToken(ZmeiLangParser.DASH, i)

        def STAR(self, i:int=None):
            if i is None:
                return self.getTokens(ZmeiLangParser.STAR)
            else:
                return self.getToken(ZmeiLangParser.STAR, i)

        def SLASH(self, i:int=None):
            if i is None:
                return self.getTokens(ZmeiLangParser.SLASH)
            else:
                return self.getToken(ZmeiLangParser.SLASH, i)

        def getRuleIndex(self):
            return ZmeiLangParser.RULE_an_gitlab_branch_name

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAn_gitlab_branch_name" ):
                listener.enterAn_gitlab_branch_name(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAn_gitlab_branch_name" ):
                listener.exitAn_gitlab_branch_name(self)




    def an_gitlab_branch_name(self):

        localctx = ZmeiLangParser.An_gitlab_branch_nameContext(self, self._ctx, self.state)
        self.enterRule(localctx, 72, self.RULE_an_gitlab_branch_name)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 952 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 952
                self._errHandler.sync(self)
                token = self._input.LA(1)
                if token in [ZmeiLangParser.KW_AUTH_TYPE_BASIC, ZmeiLangParser.KW_AUTH_TYPE_SESSION, ZmeiLangParser.KW_AUTH_TYPE_TOKEN, ZmeiLangParser.COL_FIELD_TYPE_LONGTEXT, ZmeiLangParser.COL_FIELD_TYPE_HTML, ZmeiLangParser.COL_FIELD_TYPE_HTML_MEDIA, ZmeiLangParser.COL_FIELD_TYPE_FLOAT, ZmeiLangParser.COL_FIELD_TYPE_DECIMAL, ZmeiLangParser.COL_FIELD_TYPE_DATE, ZmeiLangParser.COL_FIELD_TYPE_DATETIME, ZmeiLangParser.COL_FIELD_TYPE_CREATE_TIME, ZmeiLangParser.COL_FIELD_TYPE_UPDATE_TIME, ZmeiLangParser.COL_FIELD_TYPE_IMAGE, ZmeiLangParser.COL_FIELD_TYPE_FILE, ZmeiLangParser.COL_FIELD_TYPE_FILER_IMAGE, ZmeiLangParser.COL_FIELD_TYPE_FILER_FILE, ZmeiLangParser.COL_FIELD_TYPE_FILER_FOLDER, ZmeiLangParser.COL_FIELD_TYPE_FILER_IMAGE_FOLDER, ZmeiLangParser.COL_FIELD_TYPE_TEXT, ZmeiLangParser.COL_FIELD_TYPE_INT, ZmeiLangParser.COL_FIELD_TYPE_SLUG, ZmeiLangParser.COL_FIELD_TYPE_BOOL, ZmeiLangParser.COL_FIELD_TYPE_ONE, ZmeiLangParser.COL_FIELD_TYPE_ONE2ONE, ZmeiLangParser.COL_FIELD_TYPE_MANY, ZmeiLangParser.COL_FIELD_CHOICES, ZmeiLangParser.KW_THEME, ZmeiLangParser.KW_INSTALL, ZmeiLangParser.KW_HEADER, ZmeiLangParser.KW_SERVICES, ZmeiLangParser.KW_SELENIUM_PYTEST, ZmeiLangParser.KW_CHILD, ZmeiLangParser.KW_FILTER_OUT, ZmeiLangParser.KW_FILTER_IN, ZmeiLangParser.KW_PAGE, ZmeiLangParser.KW_LINK_SUFFIX, ZmeiLangParser.KW_URL_PREFIX, ZmeiLangParser.KW_CAN_EDIT, ZmeiLangParser.KW_OBJECT_EXPR, ZmeiLangParser.KW_BLOCK, ZmeiLangParser.KW_ITEM_NAME, ZmeiLangParser.KW_PK_PARAM, ZmeiLangParser.KW_LIST_FIELDS, ZmeiLangParser.KW_DELETE, ZmeiLangParser.KW_EDIT, ZmeiLangParser.KW_CREATE, ZmeiLangParser.KW_DETAIL, ZmeiLangParser.KW_SKIP, ZmeiLangParser.KW_FROM, ZmeiLangParser.KW_POLY_LIST, ZmeiLangParser.KW_CSS, ZmeiLangParser.KW_JS, ZmeiLangParser.KW_INLINE_TYPE_TABULAR, ZmeiLangParser.KW_INLINE_TYPE_STACKED, ZmeiLangParser.KW_INLINE_TYPE_POLYMORPHIC, ZmeiLangParser.KW_INLINE, ZmeiLangParser.KW_TYPE, ZmeiLangParser.KW_USER_FIELD, ZmeiLangParser.KW_ANNOTATE, ZmeiLangParser.KW_ON_CREATE, ZmeiLangParser.KW_QUERY, ZmeiLangParser.KW_AUTH, ZmeiLangParser.KW_COUNT, ZmeiLangParser.KW_I18N, ZmeiLangParser.KW_EXTENSION, ZmeiLangParser.KW_TABS, ZmeiLangParser.KW_LIST, ZmeiLangParser.KW_READ_ONLY, ZmeiLangParser.KW_LIST_EDITABLE, ZmeiLangParser.KW_LIST_FILTER, ZmeiLangParser.KW_LIST_SEARCH, ZmeiLangParser.KW_FIELDS, ZmeiLangParser.KW_IMPORT, ZmeiLangParser.KW_AS, ZmeiLangParser.WRITE_MODE, ZmeiLangParser.BOOL, ZmeiLangParser.ID]:
                    self.state = 948
                    self.id_or_kw()
                    pass
                elif token in [ZmeiLangParser.DASH]:
                    self.state = 949
                    self.match(ZmeiLangParser.DASH)
                    pass
                elif token in [ZmeiLangParser.STAR]:
                    self.state = 950
                    self.match(ZmeiLangParser.STAR)
                    pass
                elif token in [ZmeiLangParser.SLASH]:
                    self.state = 951
                    self.match(ZmeiLangParser.SLASH)
                    pass
                else:
                    raise NoViableAltException(self)

                self.state = 954 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not (((((_la - 42)) & ~0x3f) == 0 and ((1 << (_la - 42)) & ((1 << (ZmeiLangParser.KW_AUTH_TYPE_BASIC - 42)) | (1 << (ZmeiLangParser.KW_AUTH_TYPE_SESSION - 42)) | (1 << (ZmeiLangParser.KW_AUTH_TYPE_TOKEN - 42)) | (1 << (ZmeiLangParser.COL_FIELD_TYPE_LONGTEXT - 42)) | (1 << (ZmeiLangParser.COL_FIELD_TYPE_HTML - 42)) | (1 << (ZmeiLangParser.COL_FIELD_TYPE_HTML_MEDIA - 42)) | (1 << (ZmeiLangParser.COL_FIELD_TYPE_FLOAT - 42)) | (1 << (ZmeiLangParser.COL_FIELD_TYPE_DECIMAL - 42)) | (1 << (ZmeiLangParser.COL_FIELD_TYPE_DATE - 42)) | (1 << (ZmeiLangParser.COL_FIELD_TYPE_DATETIME - 42)) | (1 << (ZmeiLangParser.COL_FIELD_TYPE_CREATE_TIME - 42)) | (1 << (ZmeiLangParser.COL_FIELD_TYPE_UPDATE_TIME - 42)) | (1 << (ZmeiLangParser.COL_FIELD_TYPE_IMAGE - 42)) | (1 << (ZmeiLangParser.COL_FIELD_TYPE_FILE - 42)) | (1 << (ZmeiLangParser.COL_FIELD_TYPE_FILER_IMAGE - 42)) | (1 << (ZmeiLangParser.COL_FIELD_TYPE_FILER_FILE - 42)) | (1 << (ZmeiLangParser.COL_FIELD_TYPE_FILER_FOLDER - 42)) | (1 << (ZmeiLangParser.COL_FIELD_TYPE_FILER_IMAGE_FOLDER - 42)) | (1 << (ZmeiLangParser.COL_FIELD_TYPE_TEXT - 42)) | (1 << (ZmeiLangParser.COL_FIELD_TYPE_INT - 42)) | (1 << (ZmeiLangParser.COL_FIELD_TYPE_SLUG - 42)) | (1 << (ZmeiLangParser.COL_FIELD_TYPE_BOOL - 42)) | (1 << (ZmeiLangParser.COL_FIELD_TYPE_ONE - 42)) | (1 << (ZmeiLangParser.COL_FIELD_TYPE_ONE2ONE - 42)) | (1 << (ZmeiLangParser.COL_FIELD_TYPE_MANY - 42)) | (1 << (ZmeiLangParser.COL_FIELD_CHOICES - 42)) | (1 << (ZmeiLangParser.KW_THEME - 42)) | (1 << (ZmeiLangParser.KW_INSTALL - 42)) | (1 << (ZmeiLangParser.KW_HEADER - 42)) | (1 << (ZmeiLangParser.KW_SERVICES - 42)) | (1 << (ZmeiLangParser.KW_SELENIUM_PYTEST - 42)) | (1 << (ZmeiLangParser.KW_CHILD - 42)) | (1 << (ZmeiLangParser.KW_FILTER_OUT - 42)) | (1 << (ZmeiLangParser.KW_FILTER_IN - 42)) | (1 << (ZmeiLangParser.KW_PAGE - 42)) | (1 << (ZmeiLangParser.KW_LINK_SUFFIX - 42)) | (1 << (ZmeiLangParser.KW_URL_PREFIX - 42)) | (1 << (ZmeiLangParser.KW_CAN_EDIT - 42)) | (1 << (ZmeiLangParser.KW_OBJECT_EXPR - 42)) | (1 << (ZmeiLangParser.KW_BLOCK - 42)) | (1 << (ZmeiLangParser.KW_ITEM_NAME - 42)) | (1 << (ZmeiLangParser.KW_PK_PARAM - 42)) | (1 << (ZmeiLangParser.KW_LIST_FIELDS - 42)) | (1 << (ZmeiLangParser.KW_DELETE - 42)) | (1 << (ZmeiLangParser.KW_EDIT - 42)) | (1 << (ZmeiLangParser.KW_CREATE - 42)) | (1 << (ZmeiLangParser.KW_DETAIL - 42)) | (1 << (ZmeiLangParser.KW_SKIP - 42)) | (1 << (ZmeiLangParser.KW_FROM - 42)) | (1 << (ZmeiLangParser.KW_POLY_LIST - 42)) | (1 << (ZmeiLangParser.KW_CSS - 42)) | (1 << (ZmeiLangParser.KW_JS - 42)) | (1 << (ZmeiLangParser.KW_INLINE_TYPE_TABULAR - 42)) | (1 << (ZmeiLangParser.KW_INLINE_TYPE_STACKED - 42)) | (1 << (ZmeiLangParser.KW_INLINE_TYPE_POLYMORPHIC - 42)) | (1 << (ZmeiLangParser.KW_INLINE - 42)) | (1 << (ZmeiLangParser.KW_TYPE - 42)) | (1 << (ZmeiLangParser.KW_USER_FIELD - 42)) | (1 << (ZmeiLangParser.KW_ANNOTATE - 42)) | (1 << (ZmeiLangParser.KW_ON_CREATE - 42)) | (1 << (ZmeiLangParser.KW_QUERY - 42)) | (1 << (ZmeiLangParser.KW_AUTH - 42)) | (1 << (ZmeiLangParser.KW_COUNT - 42)) | (1 << (ZmeiLangParser.KW_I18N - 42)))) != 0) or ((((_la - 106)) & ~0x3f) == 0 and ((1 << (_la - 106)) & ((1 << (ZmeiLangParser.KW_EXTENSION - 106)) | (1 << (ZmeiLangParser.KW_TABS - 106)) | (1 << (ZmeiLangParser.KW_LIST - 106)) | (1 << (ZmeiLangParser.KW_READ_ONLY - 106)) | (1 << (ZmeiLangParser.KW_LIST_EDITABLE - 106)) | (1 << (ZmeiLangParser.KW_LIST_FILTER - 106)) | (1 << (ZmeiLangParser.KW_LIST_SEARCH - 106)) | (1 << (ZmeiLangParser.KW_FIELDS - 106)) | (1 << (ZmeiLangParser.KW_IMPORT - 106)) | (1 << (ZmeiLangParser.KW_AS - 106)) | (1 << (ZmeiLangParser.WRITE_MODE - 106)) | (1 << (ZmeiLangParser.BOOL - 106)) | (1 << (ZmeiLangParser.ID - 106)) | (1 << (ZmeiLangParser.DASH - 106)) | (1 << (ZmeiLangParser.SLASH - 106)) | (1 << (ZmeiLangParser.STAR - 106)))) != 0)):
                    break

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class An_gitlab_deployment_nameContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def id_or_kw(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(ZmeiLangParser.Id_or_kwContext)
            else:
                return self.getTypedRuleContext(ZmeiLangParser.Id_or_kwContext,i)


        def DASH(self, i:int=None):
            if i is None:
                return self.getTokens(ZmeiLangParser.DASH)
            else:
                return self.getToken(ZmeiLangParser.DASH, i)

        def SLASH(self, i:int=None):
            if i is None:
                return self.getTokens(ZmeiLangParser.SLASH)
            else:
                return self.getToken(ZmeiLangParser.SLASH, i)

        def STAR(self, i:int=None):
            if i is None:
                return self.getTokens(ZmeiLangParser.STAR)
            else:
                return self.getToken(ZmeiLangParser.STAR, i)

        def getRuleIndex(self):
            return ZmeiLangParser.RULE_an_gitlab_deployment_name

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAn_gitlab_deployment_name" ):
                listener.enterAn_gitlab_deployment_name(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAn_gitlab_deployment_name" ):
                listener.exitAn_gitlab_deployment_name(self)




    def an_gitlab_deployment_name(self):

        localctx = ZmeiLangParser.An_gitlab_deployment_nameContext(self, self._ctx, self.state)
        self.enterRule(localctx, 74, self.RULE_an_gitlab_deployment_name)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 960 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 960
                self._errHandler.sync(self)
                token = self._input.LA(1)
                if token in [ZmeiLangParser.KW_AUTH_TYPE_BASIC, ZmeiLangParser.KW_AUTH_TYPE_SESSION, ZmeiLangParser.KW_AUTH_TYPE_TOKEN, ZmeiLangParser.COL_FIELD_TYPE_LONGTEXT, ZmeiLangParser.COL_FIELD_TYPE_HTML, ZmeiLangParser.COL_FIELD_TYPE_HTML_MEDIA, ZmeiLangParser.COL_FIELD_TYPE_FLOAT, ZmeiLangParser.COL_FIELD_TYPE_DECIMAL, ZmeiLangParser.COL_FIELD_TYPE_DATE, ZmeiLangParser.COL_FIELD_TYPE_DATETIME, ZmeiLangParser.COL_FIELD_TYPE_CREATE_TIME, ZmeiLangParser.COL_FIELD_TYPE_UPDATE_TIME, ZmeiLangParser.COL_FIELD_TYPE_IMAGE, ZmeiLangParser.COL_FIELD_TYPE_FILE, ZmeiLangParser.COL_FIELD_TYPE_FILER_IMAGE, ZmeiLangParser.COL_FIELD_TYPE_FILER_FILE, ZmeiLangParser.COL_FIELD_TYPE_FILER_FOLDER, ZmeiLangParser.COL_FIELD_TYPE_FILER_IMAGE_FOLDER, ZmeiLangParser.COL_FIELD_TYPE_TEXT, ZmeiLangParser.COL_FIELD_TYPE_INT, ZmeiLangParser.COL_FIELD_TYPE_SLUG, ZmeiLangParser.COL_FIELD_TYPE_BOOL, ZmeiLangParser.COL_FIELD_TYPE_ONE, ZmeiLangParser.COL_FIELD_TYPE_ONE2ONE, ZmeiLangParser.COL_FIELD_TYPE_MANY, ZmeiLangParser.COL_FIELD_CHOICES, ZmeiLangParser.KW_THEME, ZmeiLangParser.KW_INSTALL, ZmeiLangParser.KW_HEADER, ZmeiLangParser.KW_SERVICES, ZmeiLangParser.KW_SELENIUM_PYTEST, ZmeiLangParser.KW_CHILD, ZmeiLangParser.KW_FILTER_OUT, ZmeiLangParser.KW_FILTER_IN, ZmeiLangParser.KW_PAGE, ZmeiLangParser.KW_LINK_SUFFIX, ZmeiLangParser.KW_URL_PREFIX, ZmeiLangParser.KW_CAN_EDIT, ZmeiLangParser.KW_OBJECT_EXPR, ZmeiLangParser.KW_BLOCK, ZmeiLangParser.KW_ITEM_NAME, ZmeiLangParser.KW_PK_PARAM, ZmeiLangParser.KW_LIST_FIELDS, ZmeiLangParser.KW_DELETE, ZmeiLangParser.KW_EDIT, ZmeiLangParser.KW_CREATE, ZmeiLangParser.KW_DETAIL, ZmeiLangParser.KW_SKIP, ZmeiLangParser.KW_FROM, ZmeiLangParser.KW_POLY_LIST, ZmeiLangParser.KW_CSS, ZmeiLangParser.KW_JS, ZmeiLangParser.KW_INLINE_TYPE_TABULAR, ZmeiLangParser.KW_INLINE_TYPE_STACKED, ZmeiLangParser.KW_INLINE_TYPE_POLYMORPHIC, ZmeiLangParser.KW_INLINE, ZmeiLangParser.KW_TYPE, ZmeiLangParser.KW_USER_FIELD, ZmeiLangParser.KW_ANNOTATE, ZmeiLangParser.KW_ON_CREATE, ZmeiLangParser.KW_QUERY, ZmeiLangParser.KW_AUTH, ZmeiLangParser.KW_COUNT, ZmeiLangParser.KW_I18N, ZmeiLangParser.KW_EXTENSION, ZmeiLangParser.KW_TABS, ZmeiLangParser.KW_LIST, ZmeiLangParser.KW_READ_ONLY, ZmeiLangParser.KW_LIST_EDITABLE, ZmeiLangParser.KW_LIST_FILTER, ZmeiLangParser.KW_LIST_SEARCH, ZmeiLangParser.KW_FIELDS, ZmeiLangParser.KW_IMPORT, ZmeiLangParser.KW_AS, ZmeiLangParser.WRITE_MODE, ZmeiLangParser.BOOL, ZmeiLangParser.ID]:
                    self.state = 956
                    self.id_or_kw()
                    pass
                elif token in [ZmeiLangParser.DASH]:
                    self.state = 957
                    self.match(ZmeiLangParser.DASH)
                    pass
                elif token in [ZmeiLangParser.SLASH]:
                    self.state = 958
                    self.match(ZmeiLangParser.SLASH)
                    pass
                elif token in [ZmeiLangParser.STAR]:
                    self.state = 959
                    self.match(ZmeiLangParser.STAR)
                    pass
                else:
                    raise NoViableAltException(self)

                self.state = 962 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not (((((_la - 42)) & ~0x3f) == 0 and ((1 << (_la - 42)) & ((1 << (ZmeiLangParser.KW_AUTH_TYPE_BASIC - 42)) | (1 << (ZmeiLangParser.KW_AUTH_TYPE_SESSION - 42)) | (1 << (ZmeiLangParser.KW_AUTH_TYPE_TOKEN - 42)) | (1 << (ZmeiLangParser.COL_FIELD_TYPE_LONGTEXT - 42)) | (1 << (ZmeiLangParser.COL_FIELD_TYPE_HTML - 42)) | (1 << (ZmeiLangParser.COL_FIELD_TYPE_HTML_MEDIA - 42)) | (1 << (ZmeiLangParser.COL_FIELD_TYPE_FLOAT - 42)) | (1 << (ZmeiLangParser.COL_FIELD_TYPE_DECIMAL - 42)) | (1 << (ZmeiLangParser.COL_FIELD_TYPE_DATE - 42)) | (1 << (ZmeiLangParser.COL_FIELD_TYPE_DATETIME - 42)) | (1 << (ZmeiLangParser.COL_FIELD_TYPE_CREATE_TIME - 42)) | (1 << (ZmeiLangParser.COL_FIELD_TYPE_UPDATE_TIME - 42)) | (1 << (ZmeiLangParser.COL_FIELD_TYPE_IMAGE - 42)) | (1 << (ZmeiLangParser.COL_FIELD_TYPE_FILE - 42)) | (1 << (ZmeiLangParser.COL_FIELD_TYPE_FILER_IMAGE - 42)) | (1 << (ZmeiLangParser.COL_FIELD_TYPE_FILER_FILE - 42)) | (1 << (ZmeiLangParser.COL_FIELD_TYPE_FILER_FOLDER - 42)) | (1 << (ZmeiLangParser.COL_FIELD_TYPE_FILER_IMAGE_FOLDER - 42)) | (1 << (ZmeiLangParser.COL_FIELD_TYPE_TEXT - 42)) | (1 << (ZmeiLangParser.COL_FIELD_TYPE_INT - 42)) | (1 << (ZmeiLangParser.COL_FIELD_TYPE_SLUG - 42)) | (1 << (ZmeiLangParser.COL_FIELD_TYPE_BOOL - 42)) | (1 << (ZmeiLangParser.COL_FIELD_TYPE_ONE - 42)) | (1 << (ZmeiLangParser.COL_FIELD_TYPE_ONE2ONE - 42)) | (1 << (ZmeiLangParser.COL_FIELD_TYPE_MANY - 42)) | (1 << (ZmeiLangParser.COL_FIELD_CHOICES - 42)) | (1 << (ZmeiLangParser.KW_THEME - 42)) | (1 << (ZmeiLangParser.KW_INSTALL - 42)) | (1 << (ZmeiLangParser.KW_HEADER - 42)) | (1 << (ZmeiLangParser.KW_SERVICES - 42)) | (1 << (ZmeiLangParser.KW_SELENIUM_PYTEST - 42)) | (1 << (ZmeiLangParser.KW_CHILD - 42)) | (1 << (ZmeiLangParser.KW_FILTER_OUT - 42)) | (1 << (ZmeiLangParser.KW_FILTER_IN - 42)) | (1 << (ZmeiLangParser.KW_PAGE - 42)) | (1 << (ZmeiLangParser.KW_LINK_SUFFIX - 42)) | (1 << (ZmeiLangParser.KW_URL_PREFIX - 42)) | (1 << (ZmeiLangParser.KW_CAN_EDIT - 42)) | (1 << (ZmeiLangParser.KW_OBJECT_EXPR - 42)) | (1 << (ZmeiLangParser.KW_BLOCK - 42)) | (1 << (ZmeiLangParser.KW_ITEM_NAME - 42)) | (1 << (ZmeiLangParser.KW_PK_PARAM - 42)) | (1 << (ZmeiLangParser.KW_LIST_FIELDS - 42)) | (1 << (ZmeiLangParser.KW_DELETE - 42)) | (1 << (ZmeiLangParser.KW_EDIT - 42)) | (1 << (ZmeiLangParser.KW_CREATE - 42)) | (1 << (ZmeiLangParser.KW_DETAIL - 42)) | (1 << (ZmeiLangParser.KW_SKIP - 42)) | (1 << (ZmeiLangParser.KW_FROM - 42)) | (1 << (ZmeiLangParser.KW_POLY_LIST - 42)) | (1 << (ZmeiLangParser.KW_CSS - 42)) | (1 << (ZmeiLangParser.KW_JS - 42)) | (1 << (ZmeiLangParser.KW_INLINE_TYPE_TABULAR - 42)) | (1 << (ZmeiLangParser.KW_INLINE_TYPE_STACKED - 42)) | (1 << (ZmeiLangParser.KW_INLINE_TYPE_POLYMORPHIC - 42)) | (1 << (ZmeiLangParser.KW_INLINE - 42)) | (1 << (ZmeiLangParser.KW_TYPE - 42)) | (1 << (ZmeiLangParser.KW_USER_FIELD - 42)) | (1 << (ZmeiLangParser.KW_ANNOTATE - 42)) | (1 << (ZmeiLangParser.KW_ON_CREATE - 42)) | (1 << (ZmeiLangParser.KW_QUERY - 42)) | (1 << (ZmeiLangParser.KW_AUTH - 42)) | (1 << (ZmeiLangParser.KW_COUNT - 42)) | (1 << (ZmeiLangParser.KW_I18N - 42)))) != 0) or ((((_la - 106)) & ~0x3f) == 0 and ((1 << (_la - 106)) & ((1 << (ZmeiLangParser.KW_EXTENSION - 106)) | (1 << (ZmeiLangParser.KW_TABS - 106)) | (1 << (ZmeiLangParser.KW_LIST - 106)) | (1 << (ZmeiLangParser.KW_READ_ONLY - 106)) | (1 << (ZmeiLangParser.KW_LIST_EDITABLE - 106)) | (1 << (ZmeiLangParser.KW_LIST_FILTER - 106)) | (1 << (ZmeiLangParser.KW_LIST_SEARCH - 106)) | (1 << (ZmeiLangParser.KW_FIELDS - 106)) | (1 << (ZmeiLangParser.KW_IMPORT - 106)) | (1 << (ZmeiLangParser.KW_AS - 106)) | (1 << (ZmeiLangParser.WRITE_MODE - 106)) | (1 << (ZmeiLangParser.BOOL - 106)) | (1 << (ZmeiLangParser.ID - 106)) | (1 << (ZmeiLangParser.DASH - 106)) | (1 << (ZmeiLangParser.SLASH - 106)) | (1 << (ZmeiLangParser.STAR - 106)))) != 0)):
                    break

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class An_gitlab_deployment_hostContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def id_or_kw(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(ZmeiLangParser.Id_or_kwContext)
            else:
                return self.getTypedRuleContext(ZmeiLangParser.Id_or_kwContext,i)


        def DASH(self, i:int=None):
            if i is None:
                return self.getTokens(ZmeiLangParser.DASH)
            else:
                return self.getToken(ZmeiLangParser.DASH, i)

        def STAR(self, i:int=None):
            if i is None:
                return self.getTokens(ZmeiLangParser.STAR)
            else:
                return self.getToken(ZmeiLangParser.STAR, i)

        def DOT(self, i:int=None):
            if i is None:
                return self.getTokens(ZmeiLangParser.DOT)
            else:
                return self.getToken(ZmeiLangParser.DOT, i)

        def getRuleIndex(self):
            return ZmeiLangParser.RULE_an_gitlab_deployment_host

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAn_gitlab_deployment_host" ):
                listener.enterAn_gitlab_deployment_host(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAn_gitlab_deployment_host" ):
                listener.exitAn_gitlab_deployment_host(self)




    def an_gitlab_deployment_host(self):

        localctx = ZmeiLangParser.An_gitlab_deployment_hostContext(self, self._ctx, self.state)
        self.enterRule(localctx, 76, self.RULE_an_gitlab_deployment_host)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 968 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 968
                self._errHandler.sync(self)
                token = self._input.LA(1)
                if token in [ZmeiLangParser.KW_AUTH_TYPE_BASIC, ZmeiLangParser.KW_AUTH_TYPE_SESSION, ZmeiLangParser.KW_AUTH_TYPE_TOKEN, ZmeiLangParser.COL_FIELD_TYPE_LONGTEXT, ZmeiLangParser.COL_FIELD_TYPE_HTML, ZmeiLangParser.COL_FIELD_TYPE_HTML_MEDIA, ZmeiLangParser.COL_FIELD_TYPE_FLOAT, ZmeiLangParser.COL_FIELD_TYPE_DECIMAL, ZmeiLangParser.COL_FIELD_TYPE_DATE, ZmeiLangParser.COL_FIELD_TYPE_DATETIME, ZmeiLangParser.COL_FIELD_TYPE_CREATE_TIME, ZmeiLangParser.COL_FIELD_TYPE_UPDATE_TIME, ZmeiLangParser.COL_FIELD_TYPE_IMAGE, ZmeiLangParser.COL_FIELD_TYPE_FILE, ZmeiLangParser.COL_FIELD_TYPE_FILER_IMAGE, ZmeiLangParser.COL_FIELD_TYPE_FILER_FILE, ZmeiLangParser.COL_FIELD_TYPE_FILER_FOLDER, ZmeiLangParser.COL_FIELD_TYPE_FILER_IMAGE_FOLDER, ZmeiLangParser.COL_FIELD_TYPE_TEXT, ZmeiLangParser.COL_FIELD_TYPE_INT, ZmeiLangParser.COL_FIELD_TYPE_SLUG, ZmeiLangParser.COL_FIELD_TYPE_BOOL, ZmeiLangParser.COL_FIELD_TYPE_ONE, ZmeiLangParser.COL_FIELD_TYPE_ONE2ONE, ZmeiLangParser.COL_FIELD_TYPE_MANY, ZmeiLangParser.COL_FIELD_CHOICES, ZmeiLangParser.KW_THEME, ZmeiLangParser.KW_INSTALL, ZmeiLangParser.KW_HEADER, ZmeiLangParser.KW_SERVICES, ZmeiLangParser.KW_SELENIUM_PYTEST, ZmeiLangParser.KW_CHILD, ZmeiLangParser.KW_FILTER_OUT, ZmeiLangParser.KW_FILTER_IN, ZmeiLangParser.KW_PAGE, ZmeiLangParser.KW_LINK_SUFFIX, ZmeiLangParser.KW_URL_PREFIX, ZmeiLangParser.KW_CAN_EDIT, ZmeiLangParser.KW_OBJECT_EXPR, ZmeiLangParser.KW_BLOCK, ZmeiLangParser.KW_ITEM_NAME, ZmeiLangParser.KW_PK_PARAM, ZmeiLangParser.KW_LIST_FIELDS, ZmeiLangParser.KW_DELETE, ZmeiLangParser.KW_EDIT, ZmeiLangParser.KW_CREATE, ZmeiLangParser.KW_DETAIL, ZmeiLangParser.KW_SKIP, ZmeiLangParser.KW_FROM, ZmeiLangParser.KW_POLY_LIST, ZmeiLangParser.KW_CSS, ZmeiLangParser.KW_JS, ZmeiLangParser.KW_INLINE_TYPE_TABULAR, ZmeiLangParser.KW_INLINE_TYPE_STACKED, ZmeiLangParser.KW_INLINE_TYPE_POLYMORPHIC, ZmeiLangParser.KW_INLINE, ZmeiLangParser.KW_TYPE, ZmeiLangParser.KW_USER_FIELD, ZmeiLangParser.KW_ANNOTATE, ZmeiLangParser.KW_ON_CREATE, ZmeiLangParser.KW_QUERY, ZmeiLangParser.KW_AUTH, ZmeiLangParser.KW_COUNT, ZmeiLangParser.KW_I18N, ZmeiLangParser.KW_EXTENSION, ZmeiLangParser.KW_TABS, ZmeiLangParser.KW_LIST, ZmeiLangParser.KW_READ_ONLY, ZmeiLangParser.KW_LIST_EDITABLE, ZmeiLangParser.KW_LIST_FILTER, ZmeiLangParser.KW_LIST_SEARCH, ZmeiLangParser.KW_FIELDS, ZmeiLangParser.KW_IMPORT, ZmeiLangParser.KW_AS, ZmeiLangParser.WRITE_MODE, ZmeiLangParser.BOOL, ZmeiLangParser.ID]:
                    self.state = 964
                    self.id_or_kw()
                    pass
                elif token in [ZmeiLangParser.DASH]:
                    self.state = 965
                    self.match(ZmeiLangParser.DASH)
                    pass
                elif token in [ZmeiLangParser.STAR]:
                    self.state = 966
                    self.match(ZmeiLangParser.STAR)
                    pass
                elif token in [ZmeiLangParser.DOT]:
                    self.state = 967
                    self.match(ZmeiLangParser.DOT)
                    pass
                else:
                    raise NoViableAltException(self)

                self.state = 970 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not (((((_la - 42)) & ~0x3f) == 0 and ((1 << (_la - 42)) & ((1 << (ZmeiLangParser.KW_AUTH_TYPE_BASIC - 42)) | (1 << (ZmeiLangParser.KW_AUTH_TYPE_SESSION - 42)) | (1 << (ZmeiLangParser.KW_AUTH_TYPE_TOKEN - 42)) | (1 << (ZmeiLangParser.COL_FIELD_TYPE_LONGTEXT - 42)) | (1 << (ZmeiLangParser.COL_FIELD_TYPE_HTML - 42)) | (1 << (ZmeiLangParser.COL_FIELD_TYPE_HTML_MEDIA - 42)) | (1 << (ZmeiLangParser.COL_FIELD_TYPE_FLOAT - 42)) | (1 << (ZmeiLangParser.COL_FIELD_TYPE_DECIMAL - 42)) | (1 << (ZmeiLangParser.COL_FIELD_TYPE_DATE - 42)) | (1 << (ZmeiLangParser.COL_FIELD_TYPE_DATETIME - 42)) | (1 << (ZmeiLangParser.COL_FIELD_TYPE_CREATE_TIME - 42)) | (1 << (ZmeiLangParser.COL_FIELD_TYPE_UPDATE_TIME - 42)) | (1 << (ZmeiLangParser.COL_FIELD_TYPE_IMAGE - 42)) | (1 << (ZmeiLangParser.COL_FIELD_TYPE_FILE - 42)) | (1 << (ZmeiLangParser.COL_FIELD_TYPE_FILER_IMAGE - 42)) | (1 << (ZmeiLangParser.COL_FIELD_TYPE_FILER_FILE - 42)) | (1 << (ZmeiLangParser.COL_FIELD_TYPE_FILER_FOLDER - 42)) | (1 << (ZmeiLangParser.COL_FIELD_TYPE_FILER_IMAGE_FOLDER - 42)) | (1 << (ZmeiLangParser.COL_FIELD_TYPE_TEXT - 42)) | (1 << (ZmeiLangParser.COL_FIELD_TYPE_INT - 42)) | (1 << (ZmeiLangParser.COL_FIELD_TYPE_SLUG - 42)) | (1 << (ZmeiLangParser.COL_FIELD_TYPE_BOOL - 42)) | (1 << (ZmeiLangParser.COL_FIELD_TYPE_ONE - 42)) | (1 << (ZmeiLangParser.COL_FIELD_TYPE_ONE2ONE - 42)) | (1 << (ZmeiLangParser.COL_FIELD_TYPE_MANY - 42)) | (1 << (ZmeiLangParser.COL_FIELD_CHOICES - 42)) | (1 << (ZmeiLangParser.KW_THEME - 42)) | (1 << (ZmeiLangParser.KW_INSTALL - 42)) | (1 << (ZmeiLangParser.KW_HEADER - 42)) | (1 << (ZmeiLangParser.KW_SERVICES - 42)) | (1 << (ZmeiLangParser.KW_SELENIUM_PYTEST - 42)) | (1 << (ZmeiLangParser.KW_CHILD - 42)) | (1 << (ZmeiLangParser.KW_FILTER_OUT - 42)) | (1 << (ZmeiLangParser.KW_FILTER_IN - 42)) | (1 << (ZmeiLangParser.KW_PAGE - 42)) | (1 << (ZmeiLangParser.KW_LINK_SUFFIX - 42)) | (1 << (ZmeiLangParser.KW_URL_PREFIX - 42)) | (1 << (ZmeiLangParser.KW_CAN_EDIT - 42)) | (1 << (ZmeiLangParser.KW_OBJECT_EXPR - 42)) | (1 << (ZmeiLangParser.KW_BLOCK - 42)) | (1 << (ZmeiLangParser.KW_ITEM_NAME - 42)) | (1 << (ZmeiLangParser.KW_PK_PARAM - 42)) | (1 << (ZmeiLangParser.KW_LIST_FIELDS - 42)) | (1 << (ZmeiLangParser.KW_DELETE - 42)) | (1 << (ZmeiLangParser.KW_EDIT - 42)) | (1 << (ZmeiLangParser.KW_CREATE - 42)) | (1 << (ZmeiLangParser.KW_DETAIL - 42)) | (1 << (ZmeiLangParser.KW_SKIP - 42)) | (1 << (ZmeiLangParser.KW_FROM - 42)) | (1 << (ZmeiLangParser.KW_POLY_LIST - 42)) | (1 << (ZmeiLangParser.KW_CSS - 42)) | (1 << (ZmeiLangParser.KW_JS - 42)) | (1 << (ZmeiLangParser.KW_INLINE_TYPE_TABULAR - 42)) | (1 << (ZmeiLangParser.KW_INLINE_TYPE_STACKED - 42)) | (1 << (ZmeiLangParser.KW_INLINE_TYPE_POLYMORPHIC - 42)) | (1 << (ZmeiLangParser.KW_INLINE - 42)) | (1 << (ZmeiLangParser.KW_TYPE - 42)) | (1 << (ZmeiLangParser.KW_USER_FIELD - 42)) | (1 << (ZmeiLangParser.KW_ANNOTATE - 42)) | (1 << (ZmeiLangParser.KW_ON_CREATE - 42)) | (1 << (ZmeiLangParser.KW_QUERY - 42)) | (1 << (ZmeiLangParser.KW_AUTH - 42)) | (1 << (ZmeiLangParser.KW_COUNT - 42)) | (1 << (ZmeiLangParser.KW_I18N - 42)))) != 0) or ((((_la - 106)) & ~0x3f) == 0 and ((1 << (_la - 106)) & ((1 << (ZmeiLangParser.KW_EXTENSION - 106)) | (1 << (ZmeiLangParser.KW_TABS - 106)) | (1 << (ZmeiLangParser.KW_LIST - 106)) | (1 << (ZmeiLangParser.KW_READ_ONLY - 106)) | (1 << (ZmeiLangParser.KW_LIST_EDITABLE - 106)) | (1 << (ZmeiLangParser.KW_LIST_FILTER - 106)) | (1 << (ZmeiLangParser.KW_LIST_SEARCH - 106)) | (1 << (ZmeiLangParser.KW_FIELDS - 106)) | (1 << (ZmeiLangParser.KW_IMPORT - 106)) | (1 << (ZmeiLangParser.KW_AS - 106)) | (1 << (ZmeiLangParser.WRITE_MODE - 106)) | (1 << (ZmeiLangParser.BOOL - 106)) | (1 << (ZmeiLangParser.ID - 106)) | (1 << (ZmeiLangParser.DASH - 106)) | (1 << (ZmeiLangParser.DOT - 106)) | (1 << (ZmeiLangParser.STAR - 106)))) != 0)):
                    break

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class An_gitlab_deployment_variableContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def an_gitlab_deployment_variable_name(self):
            return self.getTypedRuleContext(ZmeiLangParser.An_gitlab_deployment_variable_nameContext,0)


        def EQUALS(self):
            return self.getToken(ZmeiLangParser.EQUALS, 0)

        def an_gitlab_deployment_variable_value(self):
            return self.getTypedRuleContext(ZmeiLangParser.An_gitlab_deployment_variable_valueContext,0)


        def NL(self, i:int=None):
            if i is None:
                return self.getTokens(ZmeiLangParser.NL)
            else:
                return self.getToken(ZmeiLangParser.NL, i)

        def getRuleIndex(self):
            return ZmeiLangParser.RULE_an_gitlab_deployment_variable

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAn_gitlab_deployment_variable" ):
                listener.enterAn_gitlab_deployment_variable(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAn_gitlab_deployment_variable" ):
                listener.exitAn_gitlab_deployment_variable(self)




    def an_gitlab_deployment_variable(self):

        localctx = ZmeiLangParser.An_gitlab_deployment_variableContext(self, self._ctx, self.state)
        self.enterRule(localctx, 78, self.RULE_an_gitlab_deployment_variable)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 975
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==ZmeiLangParser.NL:
                self.state = 972
                self.match(ZmeiLangParser.NL)
                self.state = 977
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 978
            self.an_gitlab_deployment_variable_name()
            self.state = 979
            self.match(ZmeiLangParser.EQUALS)
            self.state = 980
            self.an_gitlab_deployment_variable_value()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class An_gitlab_deployment_variable_nameContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def id_or_kw(self):
            return self.getTypedRuleContext(ZmeiLangParser.Id_or_kwContext,0)


        def getRuleIndex(self):
            return ZmeiLangParser.RULE_an_gitlab_deployment_variable_name

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAn_gitlab_deployment_variable_name" ):
                listener.enterAn_gitlab_deployment_variable_name(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAn_gitlab_deployment_variable_name" ):
                listener.exitAn_gitlab_deployment_variable_name(self)




    def an_gitlab_deployment_variable_name(self):

        localctx = ZmeiLangParser.An_gitlab_deployment_variable_nameContext(self, self._ctx, self.state)
        self.enterRule(localctx, 80, self.RULE_an_gitlab_deployment_variable_name)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 982
            self.id_or_kw()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class An_gitlab_deployment_variable_valueContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def STRING_DQ(self):
            return self.getToken(ZmeiLangParser.STRING_DQ, 0)

        def STRING_SQ(self):
            return self.getToken(ZmeiLangParser.STRING_SQ, 0)

        def DIGIT(self):
            return self.getToken(ZmeiLangParser.DIGIT, 0)

        def id_or_kw(self):
            return self.getTypedRuleContext(ZmeiLangParser.Id_or_kwContext,0)


        def getRuleIndex(self):
            return ZmeiLangParser.RULE_an_gitlab_deployment_variable_value

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAn_gitlab_deployment_variable_value" ):
                listener.enterAn_gitlab_deployment_variable_value(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAn_gitlab_deployment_variable_value" ):
                listener.exitAn_gitlab_deployment_variable_value(self)




    def an_gitlab_deployment_variable_value(self):

        localctx = ZmeiLangParser.An_gitlab_deployment_variable_valueContext(self, self._ctx, self.state)
        self.enterRule(localctx, 82, self.RULE_an_gitlab_deployment_variable_value)
        try:
            self.state = 988
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [ZmeiLangParser.STRING_DQ]:
                self.enterOuterAlt(localctx, 1)
                self.state = 984
                self.match(ZmeiLangParser.STRING_DQ)
                pass
            elif token in [ZmeiLangParser.STRING_SQ]:
                self.enterOuterAlt(localctx, 2)
                self.state = 985
                self.match(ZmeiLangParser.STRING_SQ)
                pass
            elif token in [ZmeiLangParser.DIGIT]:
                self.enterOuterAlt(localctx, 3)
                self.state = 986
                self.match(ZmeiLangParser.DIGIT)
                pass
            elif token in [ZmeiLangParser.KW_AUTH_TYPE_BASIC, ZmeiLangParser.KW_AUTH_TYPE_SESSION, ZmeiLangParser.KW_AUTH_TYPE_TOKEN, ZmeiLangParser.COL_FIELD_TYPE_LONGTEXT, ZmeiLangParser.COL_FIELD_TYPE_HTML, ZmeiLangParser.COL_FIELD_TYPE_HTML_MEDIA, ZmeiLangParser.COL_FIELD_TYPE_FLOAT, ZmeiLangParser.COL_FIELD_TYPE_DECIMAL, ZmeiLangParser.COL_FIELD_TYPE_DATE, ZmeiLangParser.COL_FIELD_TYPE_DATETIME, ZmeiLangParser.COL_FIELD_TYPE_CREATE_TIME, ZmeiLangParser.COL_FIELD_TYPE_UPDATE_TIME, ZmeiLangParser.COL_FIELD_TYPE_IMAGE, ZmeiLangParser.COL_FIELD_TYPE_FILE, ZmeiLangParser.COL_FIELD_TYPE_FILER_IMAGE, ZmeiLangParser.COL_FIELD_TYPE_FILER_FILE, ZmeiLangParser.COL_FIELD_TYPE_FILER_FOLDER, ZmeiLangParser.COL_FIELD_TYPE_FILER_IMAGE_FOLDER, ZmeiLangParser.COL_FIELD_TYPE_TEXT, ZmeiLangParser.COL_FIELD_TYPE_INT, ZmeiLangParser.COL_FIELD_TYPE_SLUG, ZmeiLangParser.COL_FIELD_TYPE_BOOL, ZmeiLangParser.COL_FIELD_TYPE_ONE, ZmeiLangParser.COL_FIELD_TYPE_ONE2ONE, ZmeiLangParser.COL_FIELD_TYPE_MANY, ZmeiLangParser.COL_FIELD_CHOICES, ZmeiLangParser.KW_THEME, ZmeiLangParser.KW_INSTALL, ZmeiLangParser.KW_HEADER, ZmeiLangParser.KW_SERVICES, ZmeiLangParser.KW_SELENIUM_PYTEST, ZmeiLangParser.KW_CHILD, ZmeiLangParser.KW_FILTER_OUT, ZmeiLangParser.KW_FILTER_IN, ZmeiLangParser.KW_PAGE, ZmeiLangParser.KW_LINK_SUFFIX, ZmeiLangParser.KW_URL_PREFIX, ZmeiLangParser.KW_CAN_EDIT, ZmeiLangParser.KW_OBJECT_EXPR, ZmeiLangParser.KW_BLOCK, ZmeiLangParser.KW_ITEM_NAME, ZmeiLangParser.KW_PK_PARAM, ZmeiLangParser.KW_LIST_FIELDS, ZmeiLangParser.KW_DELETE, ZmeiLangParser.KW_EDIT, ZmeiLangParser.KW_CREATE, ZmeiLangParser.KW_DETAIL, ZmeiLangParser.KW_SKIP, ZmeiLangParser.KW_FROM, ZmeiLangParser.KW_POLY_LIST, ZmeiLangParser.KW_CSS, ZmeiLangParser.KW_JS, ZmeiLangParser.KW_INLINE_TYPE_TABULAR, ZmeiLangParser.KW_INLINE_TYPE_STACKED, ZmeiLangParser.KW_INLINE_TYPE_POLYMORPHIC, ZmeiLangParser.KW_INLINE, ZmeiLangParser.KW_TYPE, ZmeiLangParser.KW_USER_FIELD, ZmeiLangParser.KW_ANNOTATE, ZmeiLangParser.KW_ON_CREATE, ZmeiLangParser.KW_QUERY, ZmeiLangParser.KW_AUTH, ZmeiLangParser.KW_COUNT, ZmeiLangParser.KW_I18N, ZmeiLangParser.KW_EXTENSION, ZmeiLangParser.KW_TABS, ZmeiLangParser.KW_LIST, ZmeiLangParser.KW_READ_ONLY, ZmeiLangParser.KW_LIST_EDITABLE, ZmeiLangParser.KW_LIST_FILTER, ZmeiLangParser.KW_LIST_SEARCH, ZmeiLangParser.KW_FIELDS, ZmeiLangParser.KW_IMPORT, ZmeiLangParser.KW_AS, ZmeiLangParser.WRITE_MODE, ZmeiLangParser.BOOL, ZmeiLangParser.ID]:
                self.enterOuterAlt(localctx, 4)
                self.state = 987
                self.id_or_kw()
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class An_fileContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def AN_FILE(self):
            return self.getToken(ZmeiLangParser.AN_FILE, 0)

        def an_file_name(self):
            return self.getTypedRuleContext(ZmeiLangParser.An_file_nameContext,0)


        def python_code(self):
            return self.getTypedRuleContext(ZmeiLangParser.Python_codeContext,0)


        def getRuleIndex(self):
            return ZmeiLangParser.RULE_an_file

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAn_file" ):
                listener.enterAn_file(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAn_file" ):
                listener.exitAn_file(self)




    def an_file(self):

        localctx = ZmeiLangParser.An_fileContext(self, self._ctx, self.state)
        self.enterRule(localctx, 84, self.RULE_an_file)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 990
            self.match(ZmeiLangParser.AN_FILE)
            self.state = 991
            self.an_file_name()
            self.state = 992
            self.python_code()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class An_file_nameContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def STRING_DQ(self):
            return self.getToken(ZmeiLangParser.STRING_DQ, 0)

        def getRuleIndex(self):
            return ZmeiLangParser.RULE_an_file_name

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAn_file_name" ):
                listener.enterAn_file_name(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAn_file_name" ):
                listener.exitAn_file_name(self)




    def an_file_name(self):

        localctx = ZmeiLangParser.An_file_nameContext(self, self._ctx, self.state)
        self.enterRule(localctx, 86, self.RULE_an_file_name)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 994
            _la = self._input.LA(1)
            if not(_la==ZmeiLangParser.STRING_DQ):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class An_themeContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def AN_THEME(self):
            return self.getToken(ZmeiLangParser.AN_THEME, 0)

        def BRACE_OPEN(self):
            return self.getToken(ZmeiLangParser.BRACE_OPEN, 0)

        def an_theme_name(self):
            return self.getTypedRuleContext(ZmeiLangParser.An_theme_nameContext,0)


        def BRACE_CLOSE(self):
            return self.getToken(ZmeiLangParser.BRACE_CLOSE, 0)

        def COMA(self):
            return self.getToken(ZmeiLangParser.COMA, 0)

        def KW_INSTALL(self):
            return self.getToken(ZmeiLangParser.KW_INSTALL, 0)

        def EQUALS(self):
            return self.getToken(ZmeiLangParser.EQUALS, 0)

        def an_theme_install(self):
            return self.getTypedRuleContext(ZmeiLangParser.An_theme_installContext,0)


        def getRuleIndex(self):
            return ZmeiLangParser.RULE_an_theme

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAn_theme" ):
                listener.enterAn_theme(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAn_theme" ):
                listener.exitAn_theme(self)




    def an_theme(self):

        localctx = ZmeiLangParser.An_themeContext(self, self._ctx, self.state)
        self.enterRule(localctx, 88, self.RULE_an_theme)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 996
            self.match(ZmeiLangParser.AN_THEME)
            self.state = 997
            self.match(ZmeiLangParser.BRACE_OPEN)
            self.state = 998
            self.an_theme_name()
            self.state = 1003
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==ZmeiLangParser.COMA:
                self.state = 999
                self.match(ZmeiLangParser.COMA)
                self.state = 1000
                self.match(ZmeiLangParser.KW_INSTALL)
                self.state = 1001
                self.match(ZmeiLangParser.EQUALS)
                self.state = 1002
                self.an_theme_install()


            self.state = 1005
            self.match(ZmeiLangParser.BRACE_CLOSE)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class An_theme_installContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def BOOL(self):
            return self.getToken(ZmeiLangParser.BOOL, 0)

        def getRuleIndex(self):
            return ZmeiLangParser.RULE_an_theme_install

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAn_theme_install" ):
                listener.enterAn_theme_install(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAn_theme_install" ):
                listener.exitAn_theme_install(self)




    def an_theme_install(self):

        localctx = ZmeiLangParser.An_theme_installContext(self, self._ctx, self.state)
        self.enterRule(localctx, 90, self.RULE_an_theme_install)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1007
            self.match(ZmeiLangParser.BOOL)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class An_theme_nameContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def id_or_kw(self):
            return self.getTypedRuleContext(ZmeiLangParser.Id_or_kwContext,0)


        def STRING_DQ(self):
            return self.getToken(ZmeiLangParser.STRING_DQ, 0)

        def STRING_SQ(self):
            return self.getToken(ZmeiLangParser.STRING_SQ, 0)

        def getRuleIndex(self):
            return ZmeiLangParser.RULE_an_theme_name

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAn_theme_name" ):
                listener.enterAn_theme_name(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAn_theme_name" ):
                listener.exitAn_theme_name(self)




    def an_theme_name(self):

        localctx = ZmeiLangParser.An_theme_nameContext(self, self._ctx, self.state)
        self.enterRule(localctx, 92, self.RULE_an_theme_name)
        try:
            self.state = 1012
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [ZmeiLangParser.KW_AUTH_TYPE_BASIC, ZmeiLangParser.KW_AUTH_TYPE_SESSION, ZmeiLangParser.KW_AUTH_TYPE_TOKEN, ZmeiLangParser.COL_FIELD_TYPE_LONGTEXT, ZmeiLangParser.COL_FIELD_TYPE_HTML, ZmeiLangParser.COL_FIELD_TYPE_HTML_MEDIA, ZmeiLangParser.COL_FIELD_TYPE_FLOAT, ZmeiLangParser.COL_FIELD_TYPE_DECIMAL, ZmeiLangParser.COL_FIELD_TYPE_DATE, ZmeiLangParser.COL_FIELD_TYPE_DATETIME, ZmeiLangParser.COL_FIELD_TYPE_CREATE_TIME, ZmeiLangParser.COL_FIELD_TYPE_UPDATE_TIME, ZmeiLangParser.COL_FIELD_TYPE_IMAGE, ZmeiLangParser.COL_FIELD_TYPE_FILE, ZmeiLangParser.COL_FIELD_TYPE_FILER_IMAGE, ZmeiLangParser.COL_FIELD_TYPE_FILER_FILE, ZmeiLangParser.COL_FIELD_TYPE_FILER_FOLDER, ZmeiLangParser.COL_FIELD_TYPE_FILER_IMAGE_FOLDER, ZmeiLangParser.COL_FIELD_TYPE_TEXT, ZmeiLangParser.COL_FIELD_TYPE_INT, ZmeiLangParser.COL_FIELD_TYPE_SLUG, ZmeiLangParser.COL_FIELD_TYPE_BOOL, ZmeiLangParser.COL_FIELD_TYPE_ONE, ZmeiLangParser.COL_FIELD_TYPE_ONE2ONE, ZmeiLangParser.COL_FIELD_TYPE_MANY, ZmeiLangParser.COL_FIELD_CHOICES, ZmeiLangParser.KW_THEME, ZmeiLangParser.KW_INSTALL, ZmeiLangParser.KW_HEADER, ZmeiLangParser.KW_SERVICES, ZmeiLangParser.KW_SELENIUM_PYTEST, ZmeiLangParser.KW_CHILD, ZmeiLangParser.KW_FILTER_OUT, ZmeiLangParser.KW_FILTER_IN, ZmeiLangParser.KW_PAGE, ZmeiLangParser.KW_LINK_SUFFIX, ZmeiLangParser.KW_URL_PREFIX, ZmeiLangParser.KW_CAN_EDIT, ZmeiLangParser.KW_OBJECT_EXPR, ZmeiLangParser.KW_BLOCK, ZmeiLangParser.KW_ITEM_NAME, ZmeiLangParser.KW_PK_PARAM, ZmeiLangParser.KW_LIST_FIELDS, ZmeiLangParser.KW_DELETE, ZmeiLangParser.KW_EDIT, ZmeiLangParser.KW_CREATE, ZmeiLangParser.KW_DETAIL, ZmeiLangParser.KW_SKIP, ZmeiLangParser.KW_FROM, ZmeiLangParser.KW_POLY_LIST, ZmeiLangParser.KW_CSS, ZmeiLangParser.KW_JS, ZmeiLangParser.KW_INLINE_TYPE_TABULAR, ZmeiLangParser.KW_INLINE_TYPE_STACKED, ZmeiLangParser.KW_INLINE_TYPE_POLYMORPHIC, ZmeiLangParser.KW_INLINE, ZmeiLangParser.KW_TYPE, ZmeiLangParser.KW_USER_FIELD, ZmeiLangParser.KW_ANNOTATE, ZmeiLangParser.KW_ON_CREATE, ZmeiLangParser.KW_QUERY, ZmeiLangParser.KW_AUTH, ZmeiLangParser.KW_COUNT, ZmeiLangParser.KW_I18N, ZmeiLangParser.KW_EXTENSION, ZmeiLangParser.KW_TABS, ZmeiLangParser.KW_LIST, ZmeiLangParser.KW_READ_ONLY, ZmeiLangParser.KW_LIST_EDITABLE, ZmeiLangParser.KW_LIST_FILTER, ZmeiLangParser.KW_LIST_SEARCH, ZmeiLangParser.KW_FIELDS, ZmeiLangParser.KW_IMPORT, ZmeiLangParser.KW_AS, ZmeiLangParser.WRITE_MODE, ZmeiLangParser.BOOL, ZmeiLangParser.ID]:
                self.enterOuterAlt(localctx, 1)
                self.state = 1009
                self.id_or_kw()
                pass
            elif token in [ZmeiLangParser.STRING_DQ]:
                self.enterOuterAlt(localctx, 2)
                self.state = 1010
                self.match(ZmeiLangParser.STRING_DQ)
                pass
            elif token in [ZmeiLangParser.STRING_SQ]:
                self.enterOuterAlt(localctx, 3)
                self.state = 1011
                self.match(ZmeiLangParser.STRING_SQ)
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class An_langsContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def AN_LANGS(self):
            return self.getToken(ZmeiLangParser.AN_LANGS, 0)

        def BRACE_OPEN(self):
            return self.getToken(ZmeiLangParser.BRACE_OPEN, 0)

        def an_langs_list(self):
            return self.getTypedRuleContext(ZmeiLangParser.An_langs_listContext,0)


        def BRACE_CLOSE(self):
            return self.getToken(ZmeiLangParser.BRACE_CLOSE, 0)

        def getRuleIndex(self):
            return ZmeiLangParser.RULE_an_langs

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAn_langs" ):
                listener.enterAn_langs(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAn_langs" ):
                listener.exitAn_langs(self)




    def an_langs(self):

        localctx = ZmeiLangParser.An_langsContext(self, self._ctx, self.state)
        self.enterRule(localctx, 94, self.RULE_an_langs)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1014
            self.match(ZmeiLangParser.AN_LANGS)
            self.state = 1015
            self.match(ZmeiLangParser.BRACE_OPEN)
            self.state = 1016
            self.an_langs_list()
            self.state = 1017
            self.match(ZmeiLangParser.BRACE_CLOSE)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class An_langs_listContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ID(self, i:int=None):
            if i is None:
                return self.getTokens(ZmeiLangParser.ID)
            else:
                return self.getToken(ZmeiLangParser.ID, i)

        def COMA(self, i:int=None):
            if i is None:
                return self.getTokens(ZmeiLangParser.COMA)
            else:
                return self.getToken(ZmeiLangParser.COMA, i)

        def getRuleIndex(self):
            return ZmeiLangParser.RULE_an_langs_list

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAn_langs_list" ):
                listener.enterAn_langs_list(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAn_langs_list" ):
                listener.exitAn_langs_list(self)




    def an_langs_list(self):

        localctx = ZmeiLangParser.An_langs_listContext(self, self._ctx, self.state)
        self.enterRule(localctx, 96, self.RULE_an_langs_list)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1019
            self.match(ZmeiLangParser.ID)
            self.state = 1024
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==ZmeiLangParser.COMA:
                self.state = 1020
                self.match(ZmeiLangParser.COMA)
                self.state = 1021
                self.match(ZmeiLangParser.ID)
                self.state = 1026
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ColContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def col_header(self):
            return self.getTypedRuleContext(ZmeiLangParser.Col_headerContext,0)


        def col_str_expr(self):
            return self.getTypedRuleContext(ZmeiLangParser.Col_str_exprContext,0)


        def NL(self, i:int=None):
            if i is None:
                return self.getTokens(ZmeiLangParser.NL)
            else:
                return self.getToken(ZmeiLangParser.NL, i)

        def col_field(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(ZmeiLangParser.Col_fieldContext)
            else:
                return self.getTypedRuleContext(ZmeiLangParser.Col_fieldContext,i)


        def model_annotation(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(ZmeiLangParser.Model_annotationContext)
            else:
                return self.getTypedRuleContext(ZmeiLangParser.Model_annotationContext,i)


        def getRuleIndex(self):
            return ZmeiLangParser.RULE_col

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterCol" ):
                listener.enterCol(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitCol" ):
                listener.exitCol(self)




    def col(self):

        localctx = ZmeiLangParser.ColContext(self, self._ctx, self.state)
        self.enterRule(localctx, 98, self.RULE_col)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1027
            self.col_header()
            self.state = 1029
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,76,self._ctx)
            if la_ == 1:
                self.state = 1028
                self.col_str_expr()


            self.state = 1034
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,77,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 1031
                    self.match(ZmeiLangParser.NL) 
                self.state = 1036
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,77,self._ctx)

            self.state = 1040
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while ((((_la - 42)) & ~0x3f) == 0 and ((1 << (_la - 42)) & ((1 << (ZmeiLangParser.KW_AUTH_TYPE_BASIC - 42)) | (1 << (ZmeiLangParser.KW_AUTH_TYPE_SESSION - 42)) | (1 << (ZmeiLangParser.KW_AUTH_TYPE_TOKEN - 42)) | (1 << (ZmeiLangParser.COL_FIELD_TYPE_LONGTEXT - 42)) | (1 << (ZmeiLangParser.COL_FIELD_TYPE_HTML - 42)) | (1 << (ZmeiLangParser.COL_FIELD_TYPE_HTML_MEDIA - 42)) | (1 << (ZmeiLangParser.COL_FIELD_TYPE_FLOAT - 42)) | (1 << (ZmeiLangParser.COL_FIELD_TYPE_DECIMAL - 42)) | (1 << (ZmeiLangParser.COL_FIELD_TYPE_DATE - 42)) | (1 << (ZmeiLangParser.COL_FIELD_TYPE_DATETIME - 42)) | (1 << (ZmeiLangParser.COL_FIELD_TYPE_CREATE_TIME - 42)) | (1 << (ZmeiLangParser.COL_FIELD_TYPE_UPDATE_TIME - 42)) | (1 << (ZmeiLangParser.COL_FIELD_TYPE_IMAGE - 42)) | (1 << (ZmeiLangParser.COL_FIELD_TYPE_FILE - 42)) | (1 << (ZmeiLangParser.COL_FIELD_TYPE_FILER_IMAGE - 42)) | (1 << (ZmeiLangParser.COL_FIELD_TYPE_FILER_FILE - 42)) | (1 << (ZmeiLangParser.COL_FIELD_TYPE_FILER_FOLDER - 42)) | (1 << (ZmeiLangParser.COL_FIELD_TYPE_FILER_IMAGE_FOLDER - 42)) | (1 << (ZmeiLangParser.COL_FIELD_TYPE_TEXT - 42)) | (1 << (ZmeiLangParser.COL_FIELD_TYPE_INT - 42)) | (1 << (ZmeiLangParser.COL_FIELD_TYPE_SLUG - 42)) | (1 << (ZmeiLangParser.COL_FIELD_TYPE_BOOL - 42)) | (1 << (ZmeiLangParser.COL_FIELD_TYPE_ONE - 42)) | (1 << (ZmeiLangParser.COL_FIELD_TYPE_ONE2ONE - 42)) | (1 << (ZmeiLangParser.COL_FIELD_TYPE_MANY - 42)) | (1 << (ZmeiLangParser.COL_FIELD_CHOICES - 42)) | (1 << (ZmeiLangParser.KW_THEME - 42)) | (1 << (ZmeiLangParser.KW_INSTALL - 42)) | (1 << (ZmeiLangParser.KW_HEADER - 42)) | (1 << (ZmeiLangParser.KW_SERVICES - 42)) | (1 << (ZmeiLangParser.KW_SELENIUM_PYTEST - 42)) | (1 << (ZmeiLangParser.KW_CHILD - 42)) | (1 << (ZmeiLangParser.KW_FILTER_OUT - 42)) | (1 << (ZmeiLangParser.KW_FILTER_IN - 42)) | (1 << (ZmeiLangParser.KW_PAGE - 42)) | (1 << (ZmeiLangParser.KW_LINK_SUFFIX - 42)) | (1 << (ZmeiLangParser.KW_URL_PREFIX - 42)) | (1 << (ZmeiLangParser.KW_CAN_EDIT - 42)) | (1 << (ZmeiLangParser.KW_OBJECT_EXPR - 42)) | (1 << (ZmeiLangParser.KW_BLOCK - 42)) | (1 << (ZmeiLangParser.KW_ITEM_NAME - 42)) | (1 << (ZmeiLangParser.KW_PK_PARAM - 42)) | (1 << (ZmeiLangParser.KW_LIST_FIELDS - 42)) | (1 << (ZmeiLangParser.KW_DELETE - 42)) | (1 << (ZmeiLangParser.KW_EDIT - 42)) | (1 << (ZmeiLangParser.KW_CREATE - 42)) | (1 << (ZmeiLangParser.KW_DETAIL - 42)) | (1 << (ZmeiLangParser.KW_SKIP - 42)) | (1 << (ZmeiLangParser.KW_FROM - 42)) | (1 << (ZmeiLangParser.KW_POLY_LIST - 42)) | (1 << (ZmeiLangParser.KW_CSS - 42)) | (1 << (ZmeiLangParser.KW_JS - 42)) | (1 << (ZmeiLangParser.KW_INLINE_TYPE_TABULAR - 42)) | (1 << (ZmeiLangParser.KW_INLINE_TYPE_STACKED - 42)) | (1 << (ZmeiLangParser.KW_INLINE_TYPE_POLYMORPHIC - 42)) | (1 << (ZmeiLangParser.KW_INLINE - 42)) | (1 << (ZmeiLangParser.KW_TYPE - 42)) | (1 << (ZmeiLangParser.KW_USER_FIELD - 42)) | (1 << (ZmeiLangParser.KW_ANNOTATE - 42)) | (1 << (ZmeiLangParser.KW_ON_CREATE - 42)) | (1 << (ZmeiLangParser.KW_QUERY - 42)) | (1 << (ZmeiLangParser.KW_AUTH - 42)) | (1 << (ZmeiLangParser.KW_COUNT - 42)) | (1 << (ZmeiLangParser.KW_I18N - 42)))) != 0) or ((((_la - 106)) & ~0x3f) == 0 and ((1 << (_la - 106)) & ((1 << (ZmeiLangParser.KW_EXTENSION - 106)) | (1 << (ZmeiLangParser.KW_TABS - 106)) | (1 << (ZmeiLangParser.KW_LIST - 106)) | (1 << (ZmeiLangParser.KW_READ_ONLY - 106)) | (1 << (ZmeiLangParser.KW_LIST_EDITABLE - 106)) | (1 << (ZmeiLangParser.KW_LIST_FILTER - 106)) | (1 << (ZmeiLangParser.KW_LIST_SEARCH - 106)) | (1 << (ZmeiLangParser.KW_FIELDS - 106)) | (1 << (ZmeiLangParser.KW_IMPORT - 106)) | (1 << (ZmeiLangParser.KW_AS - 106)) | (1 << (ZmeiLangParser.WRITE_MODE - 106)) | (1 << (ZmeiLangParser.BOOL - 106)) | (1 << (ZmeiLangParser.ID - 106)) | (1 << (ZmeiLangParser.EQUALS - 106)) | (1 << (ZmeiLangParser.DOLLAR - 106)) | (1 << (ZmeiLangParser.AMP - 106)) | (1 << (ZmeiLangParser.EXCLAM - 106)) | (1 << (ZmeiLangParser.STAR - 106)) | (1 << (ZmeiLangParser.APPROX - 106)))) != 0):
                self.state = 1037
                self.col_field()
                self.state = 1042
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 1046
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,79,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 1043
                    self.match(ZmeiLangParser.NL) 
                self.state = 1048
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,79,self._ctx)

            self.state = 1052
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,80,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 1049
                    self.model_annotation() 
                self.state = 1054
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,80,self._ctx)

            self.state = 1058
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,81,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 1055
                    self.match(ZmeiLangParser.NL) 
                self.state = 1060
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,81,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Col_str_exprContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def EQUALS(self):
            return self.getToken(ZmeiLangParser.EQUALS, 0)

        def STRING_DQ(self):
            return self.getToken(ZmeiLangParser.STRING_DQ, 0)

        def STRING_SQ(self):
            return self.getToken(ZmeiLangParser.STRING_SQ, 0)

        def EOF(self):
            return self.getToken(ZmeiLangParser.EOF, 0)

        def NL(self, i:int=None):
            if i is None:
                return self.getTokens(ZmeiLangParser.NL)
            else:
                return self.getToken(ZmeiLangParser.NL, i)

        def getRuleIndex(self):
            return ZmeiLangParser.RULE_col_str_expr

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterCol_str_expr" ):
                listener.enterCol_str_expr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitCol_str_expr" ):
                listener.exitCol_str_expr(self)




    def col_str_expr(self):

        localctx = ZmeiLangParser.Col_str_exprContext(self, self._ctx, self.state)
        self.enterRule(localctx, 100, self.RULE_col_str_expr)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1061
            self.match(ZmeiLangParser.EQUALS)
            self.state = 1062
            _la = self._input.LA(1)
            if not(_la==ZmeiLangParser.STRING_DQ or _la==ZmeiLangParser.STRING_SQ):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
            self.state = 1069
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [ZmeiLangParser.NL]:
                self.state = 1064 
                self._errHandler.sync(self)
                _alt = 1
                while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                    if _alt == 1:
                        self.state = 1063
                        self.match(ZmeiLangParser.NL)

                    else:
                        raise NoViableAltException(self)
                    self.state = 1066 
                    self._errHandler.sync(self)
                    _alt = self._interp.adaptivePredict(self._input,82,self._ctx)

                pass
            elif token in [ZmeiLangParser.EOF]:
                self.state = 1068
                self.match(ZmeiLangParser.EOF)
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Col_headerContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def HASH(self):
            return self.getToken(ZmeiLangParser.HASH, 0)

        def col_name(self):
            return self.getTypedRuleContext(ZmeiLangParser.Col_nameContext,0)


        def col_header_line_separator(self):
            return self.getTypedRuleContext(ZmeiLangParser.Col_header_line_separatorContext,0)


        def NL(self):
            return self.getToken(ZmeiLangParser.NL, 0)

        def col_base_name(self):
            return self.getTypedRuleContext(ZmeiLangParser.Col_base_nameContext,0)


        def col_verbose_name(self):
            return self.getTypedRuleContext(ZmeiLangParser.Col_verbose_nameContext,0)


        def getRuleIndex(self):
            return ZmeiLangParser.RULE_col_header

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterCol_header" ):
                listener.enterCol_header(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitCol_header" ):
                listener.exitCol_header(self)




    def col_header(self):

        localctx = ZmeiLangParser.Col_headerContext(self, self._ctx, self.state)
        self.enterRule(localctx, 102, self.RULE_col_header)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1071
            self.match(ZmeiLangParser.HASH)
            self.state = 1073
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,84,self._ctx)
            if la_ == 1:
                self.state = 1072
                self.col_base_name()


            self.state = 1075
            self.col_name()
            self.state = 1077
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==ZmeiLangParser.COLON:
                self.state = 1076
                self.col_verbose_name()


            self.state = 1079
            self.col_header_line_separator()
            self.state = 1080
            self.match(ZmeiLangParser.NL)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Col_header_line_separatorContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def NL(self):
            return self.getToken(ZmeiLangParser.NL, 0)

        def DASH(self, i:int=None):
            if i is None:
                return self.getTokens(ZmeiLangParser.DASH)
            else:
                return self.getToken(ZmeiLangParser.DASH, i)

        def getRuleIndex(self):
            return ZmeiLangParser.RULE_col_header_line_separator

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterCol_header_line_separator" ):
                listener.enterCol_header_line_separator(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitCol_header_line_separator" ):
                listener.exitCol_header_line_separator(self)




    def col_header_line_separator(self):

        localctx = ZmeiLangParser.Col_header_line_separatorContext(self, self._ctx, self.state)
        self.enterRule(localctx, 104, self.RULE_col_header_line_separator)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1082
            self.match(ZmeiLangParser.NL)
            self.state = 1083
            self.match(ZmeiLangParser.DASH)
            self.state = 1084
            self.match(ZmeiLangParser.DASH)
            self.state = 1086 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 1085
                self.match(ZmeiLangParser.DASH)
                self.state = 1088 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not (_la==ZmeiLangParser.DASH):
                    break

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Col_verbose_nameContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def COLON(self):
            return self.getToken(ZmeiLangParser.COLON, 0)

        def verbose_name_part(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(ZmeiLangParser.Verbose_name_partContext)
            else:
                return self.getTypedRuleContext(ZmeiLangParser.Verbose_name_partContext,i)


        def SLASH(self):
            return self.getToken(ZmeiLangParser.SLASH, 0)

        def getRuleIndex(self):
            return ZmeiLangParser.RULE_col_verbose_name

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterCol_verbose_name" ):
                listener.enterCol_verbose_name(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitCol_verbose_name" ):
                listener.exitCol_verbose_name(self)




    def col_verbose_name(self):

        localctx = ZmeiLangParser.Col_verbose_nameContext(self, self._ctx, self.state)
        self.enterRule(localctx, 106, self.RULE_col_verbose_name)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1090
            self.match(ZmeiLangParser.COLON)
            self.state = 1091
            self.verbose_name_part()
            self.state = 1094
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==ZmeiLangParser.SLASH:
                self.state = 1092
                self.match(ZmeiLangParser.SLASH)
                self.state = 1093
                self.verbose_name_part()


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Verbose_name_partContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def id_or_kw(self):
            return self.getTypedRuleContext(ZmeiLangParser.Id_or_kwContext,0)


        def STRING_DQ(self):
            return self.getToken(ZmeiLangParser.STRING_DQ, 0)

        def STRING_SQ(self):
            return self.getToken(ZmeiLangParser.STRING_SQ, 0)

        def getRuleIndex(self):
            return ZmeiLangParser.RULE_verbose_name_part

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterVerbose_name_part" ):
                listener.enterVerbose_name_part(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitVerbose_name_part" ):
                listener.exitVerbose_name_part(self)




    def verbose_name_part(self):

        localctx = ZmeiLangParser.Verbose_name_partContext(self, self._ctx, self.state)
        self.enterRule(localctx, 108, self.RULE_verbose_name_part)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1099
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [ZmeiLangParser.KW_AUTH_TYPE_BASIC, ZmeiLangParser.KW_AUTH_TYPE_SESSION, ZmeiLangParser.KW_AUTH_TYPE_TOKEN, ZmeiLangParser.COL_FIELD_TYPE_LONGTEXT, ZmeiLangParser.COL_FIELD_TYPE_HTML, ZmeiLangParser.COL_FIELD_TYPE_HTML_MEDIA, ZmeiLangParser.COL_FIELD_TYPE_FLOAT, ZmeiLangParser.COL_FIELD_TYPE_DECIMAL, ZmeiLangParser.COL_FIELD_TYPE_DATE, ZmeiLangParser.COL_FIELD_TYPE_DATETIME, ZmeiLangParser.COL_FIELD_TYPE_CREATE_TIME, ZmeiLangParser.COL_FIELD_TYPE_UPDATE_TIME, ZmeiLangParser.COL_FIELD_TYPE_IMAGE, ZmeiLangParser.COL_FIELD_TYPE_FILE, ZmeiLangParser.COL_FIELD_TYPE_FILER_IMAGE, ZmeiLangParser.COL_FIELD_TYPE_FILER_FILE, ZmeiLangParser.COL_FIELD_TYPE_FILER_FOLDER, ZmeiLangParser.COL_FIELD_TYPE_FILER_IMAGE_FOLDER, ZmeiLangParser.COL_FIELD_TYPE_TEXT, ZmeiLangParser.COL_FIELD_TYPE_INT, ZmeiLangParser.COL_FIELD_TYPE_SLUG, ZmeiLangParser.COL_FIELD_TYPE_BOOL, ZmeiLangParser.COL_FIELD_TYPE_ONE, ZmeiLangParser.COL_FIELD_TYPE_ONE2ONE, ZmeiLangParser.COL_FIELD_TYPE_MANY, ZmeiLangParser.COL_FIELD_CHOICES, ZmeiLangParser.KW_THEME, ZmeiLangParser.KW_INSTALL, ZmeiLangParser.KW_HEADER, ZmeiLangParser.KW_SERVICES, ZmeiLangParser.KW_SELENIUM_PYTEST, ZmeiLangParser.KW_CHILD, ZmeiLangParser.KW_FILTER_OUT, ZmeiLangParser.KW_FILTER_IN, ZmeiLangParser.KW_PAGE, ZmeiLangParser.KW_LINK_SUFFIX, ZmeiLangParser.KW_URL_PREFIX, ZmeiLangParser.KW_CAN_EDIT, ZmeiLangParser.KW_OBJECT_EXPR, ZmeiLangParser.KW_BLOCK, ZmeiLangParser.KW_ITEM_NAME, ZmeiLangParser.KW_PK_PARAM, ZmeiLangParser.KW_LIST_FIELDS, ZmeiLangParser.KW_DELETE, ZmeiLangParser.KW_EDIT, ZmeiLangParser.KW_CREATE, ZmeiLangParser.KW_DETAIL, ZmeiLangParser.KW_SKIP, ZmeiLangParser.KW_FROM, ZmeiLangParser.KW_POLY_LIST, ZmeiLangParser.KW_CSS, ZmeiLangParser.KW_JS, ZmeiLangParser.KW_INLINE_TYPE_TABULAR, ZmeiLangParser.KW_INLINE_TYPE_STACKED, ZmeiLangParser.KW_INLINE_TYPE_POLYMORPHIC, ZmeiLangParser.KW_INLINE, ZmeiLangParser.KW_TYPE, ZmeiLangParser.KW_USER_FIELD, ZmeiLangParser.KW_ANNOTATE, ZmeiLangParser.KW_ON_CREATE, ZmeiLangParser.KW_QUERY, ZmeiLangParser.KW_AUTH, ZmeiLangParser.KW_COUNT, ZmeiLangParser.KW_I18N, ZmeiLangParser.KW_EXTENSION, ZmeiLangParser.KW_TABS, ZmeiLangParser.KW_LIST, ZmeiLangParser.KW_READ_ONLY, ZmeiLangParser.KW_LIST_EDITABLE, ZmeiLangParser.KW_LIST_FILTER, ZmeiLangParser.KW_LIST_SEARCH, ZmeiLangParser.KW_FIELDS, ZmeiLangParser.KW_IMPORT, ZmeiLangParser.KW_AS, ZmeiLangParser.WRITE_MODE, ZmeiLangParser.BOOL, ZmeiLangParser.ID]:
                self.state = 1096
                self.id_or_kw()
                pass
            elif token in [ZmeiLangParser.STRING_DQ]:
                self.state = 1097
                self.match(ZmeiLangParser.STRING_DQ)
                pass
            elif token in [ZmeiLangParser.STRING_SQ]:
                self.state = 1098
                self.match(ZmeiLangParser.STRING_SQ)
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Col_base_nameContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def id_or_kw(self):
            return self.getTypedRuleContext(ZmeiLangParser.Id_or_kwContext,0)


        def DASH(self):
            return self.getToken(ZmeiLangParser.DASH, 0)

        def GT(self):
            return self.getToken(ZmeiLangParser.GT, 0)

        def APPROX(self):
            return self.getToken(ZmeiLangParser.APPROX, 0)

        def getRuleIndex(self):
            return ZmeiLangParser.RULE_col_base_name

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterCol_base_name" ):
                listener.enterCol_base_name(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitCol_base_name" ):
                listener.exitCol_base_name(self)




    def col_base_name(self):

        localctx = ZmeiLangParser.Col_base_nameContext(self, self._ctx, self.state)
        self.enterRule(localctx, 110, self.RULE_col_base_name)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1101
            self.id_or_kw()
            self.state = 1106
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [ZmeiLangParser.DASH]:
                self.state = 1102
                self.match(ZmeiLangParser.DASH)
                self.state = 1103
                self.match(ZmeiLangParser.GT)
                pass
            elif token in [ZmeiLangParser.APPROX]:
                self.state = 1104
                self.match(ZmeiLangParser.APPROX)
                self.state = 1105
                self.match(ZmeiLangParser.GT)
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Col_nameContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def id_or_kw(self):
            return self.getTypedRuleContext(ZmeiLangParser.Id_or_kwContext,0)


        def getRuleIndex(self):
            return ZmeiLangParser.RULE_col_name

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterCol_name" ):
                listener.enterCol_name(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitCol_name" ):
                listener.exitCol_name(self)




    def col_name(self):

        localctx = ZmeiLangParser.Col_nameContext(self, self._ctx, self.state)
        self.enterRule(localctx, 112, self.RULE_col_name)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1108
            self.id_or_kw()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Col_fieldContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def col_field_name(self):
            return self.getTypedRuleContext(ZmeiLangParser.Col_field_nameContext,0)


        def EOF(self):
            return self.getToken(ZmeiLangParser.EOF, 0)

        def col_modifier(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(ZmeiLangParser.Col_modifierContext)
            else:
                return self.getTypedRuleContext(ZmeiLangParser.Col_modifierContext,i)


        def col_field_expr_or_def(self):
            return self.getTypedRuleContext(ZmeiLangParser.Col_field_expr_or_defContext,0)


        def col_field_verbose_name(self):
            return self.getTypedRuleContext(ZmeiLangParser.Col_field_verbose_nameContext,0)


        def col_field_help_text(self):
            return self.getTypedRuleContext(ZmeiLangParser.Col_field_help_textContext,0)


        def NL(self, i:int=None):
            if i is None:
                return self.getTokens(ZmeiLangParser.NL)
            else:
                return self.getToken(ZmeiLangParser.NL, i)

        def getRuleIndex(self):
            return ZmeiLangParser.RULE_col_field

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterCol_field" ):
                listener.enterCol_field(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitCol_field" ):
                listener.exitCol_field(self)




    def col_field(self):

        localctx = ZmeiLangParser.Col_fieldContext(self, self._ctx, self.state)
        self.enterRule(localctx, 114, self.RULE_col_field)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1113
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while ((((_la - 137)) & ~0x3f) == 0 and ((1 << (_la - 137)) & ((1 << (ZmeiLangParser.EQUALS - 137)) | (1 << (ZmeiLangParser.DOLLAR - 137)) | (1 << (ZmeiLangParser.AMP - 137)) | (1 << (ZmeiLangParser.EXCLAM - 137)) | (1 << (ZmeiLangParser.STAR - 137)) | (1 << (ZmeiLangParser.APPROX - 137)))) != 0):
                self.state = 1110
                self.col_modifier()
                self.state = 1115
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 1116
            self.col_field_name()
            self.state = 1118
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if ((((_la - 124)) & ~0x3f) == 0 and ((1 << (_la - 124)) & ((1 << (ZmeiLangParser.COLON - 124)) | (1 << (ZmeiLangParser.ASSIGN - 124)) | (1 << (ZmeiLangParser.ASSIGN_STATIC - 124)))) != 0):
                self.state = 1117
                self.col_field_expr_or_def()


            self.state = 1121
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==ZmeiLangParser.SLASH:
                self.state = 1120
                self.col_field_verbose_name()


            self.state = 1124
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==ZmeiLangParser.QUESTION_MARK:
                self.state = 1123
                self.col_field_help_text()


            self.state = 1132
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [ZmeiLangParser.NL]:
                self.state = 1127 
                self._errHandler.sync(self)
                _alt = 1
                while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                    if _alt == 1:
                        self.state = 1126
                        self.match(ZmeiLangParser.NL)

                    else:
                        raise NoViableAltException(self)
                    self.state = 1129 
                    self._errHandler.sync(self)
                    _alt = self._interp.adaptivePredict(self._input,94,self._ctx)

                pass
            elif token in [ZmeiLangParser.EOF]:
                self.state = 1131
                self.match(ZmeiLangParser.EOF)
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Col_field_expr_or_defContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def col_field_expr(self):
            return self.getTypedRuleContext(ZmeiLangParser.Col_field_exprContext,0)


        def COLON(self):
            return self.getToken(ZmeiLangParser.COLON, 0)

        def col_field_def(self):
            return self.getTypedRuleContext(ZmeiLangParser.Col_field_defContext,0)


        def wrong_field_type(self):
            return self.getTypedRuleContext(ZmeiLangParser.Wrong_field_typeContext,0)


        def col_field_custom(self):
            return self.getTypedRuleContext(ZmeiLangParser.Col_field_customContext,0)


        def col_field_extend(self):
            return self.getTypedRuleContext(ZmeiLangParser.Col_field_extendContext,0)


        def getRuleIndex(self):
            return ZmeiLangParser.RULE_col_field_expr_or_def

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterCol_field_expr_or_def" ):
                listener.enterCol_field_expr_or_def(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitCol_field_expr_or_def" ):
                listener.exitCol_field_expr_or_def(self)




    def col_field_expr_or_def(self):

        localctx = ZmeiLangParser.Col_field_expr_or_defContext(self, self._ctx, self.state)
        self.enterRule(localctx, 116, self.RULE_col_field_expr_or_def)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1146
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,98,self._ctx)
            if la_ == 1:
                self.state = 1134
                self.match(ZmeiLangParser.COLON)
                self.state = 1136
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==ZmeiLangParser.CODE_BLOCK:
                    self.state = 1135
                    self.col_field_custom()


                pass

            elif la_ == 2:
                self.state = 1138
                self.match(ZmeiLangParser.COLON)
                self.state = 1139
                self.col_field_def()
                self.state = 1141
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==ZmeiLangParser.DOT or _la==ZmeiLangParser.CODE_BLOCK:
                    self.state = 1140
                    self.col_field_extend()


                pass

            elif la_ == 3:
                self.state = 1143
                self.match(ZmeiLangParser.COLON)
                self.state = 1144
                self.wrong_field_type()
                pass

            elif la_ == 4:
                self.state = 1145
                self.col_field_expr()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Col_field_customContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def code_block(self):
            return self.getTypedRuleContext(ZmeiLangParser.Code_blockContext,0)


        def getRuleIndex(self):
            return ZmeiLangParser.RULE_col_field_custom

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterCol_field_custom" ):
                listener.enterCol_field_custom(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitCol_field_custom" ):
                listener.exitCol_field_custom(self)




    def col_field_custom(self):

        localctx = ZmeiLangParser.Col_field_customContext(self, self._ctx, self.state)
        self.enterRule(localctx, 118, self.RULE_col_field_custom)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1148
            self.code_block()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Col_field_extendContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def code_block(self):
            return self.getTypedRuleContext(ZmeiLangParser.Code_blockContext,0)


        def col_field_extend_append(self):
            return self.getTypedRuleContext(ZmeiLangParser.Col_field_extend_appendContext,0)


        def getRuleIndex(self):
            return ZmeiLangParser.RULE_col_field_extend

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterCol_field_extend" ):
                listener.enterCol_field_extend(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitCol_field_extend" ):
                listener.exitCol_field_extend(self)




    def col_field_extend(self):

        localctx = ZmeiLangParser.Col_field_extendContext(self, self._ctx, self.state)
        self.enterRule(localctx, 120, self.RULE_col_field_extend)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1151
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==ZmeiLangParser.DOT:
                self.state = 1150
                self.col_field_extend_append()


            self.state = 1153
            self.code_block()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Col_field_extend_appendContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def DOT(self, i:int=None):
            if i is None:
                return self.getTokens(ZmeiLangParser.DOT)
            else:
                return self.getToken(ZmeiLangParser.DOT, i)

        def getRuleIndex(self):
            return ZmeiLangParser.RULE_col_field_extend_append

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterCol_field_extend_append" ):
                listener.enterCol_field_extend_append(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitCol_field_extend_append" ):
                listener.exitCol_field_extend_append(self)




    def col_field_extend_append(self):

        localctx = ZmeiLangParser.Col_field_extend_appendContext(self, self._ctx, self.state)
        self.enterRule(localctx, 122, self.RULE_col_field_extend_append)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1155
            self.match(ZmeiLangParser.DOT)
            self.state = 1156
            self.match(ZmeiLangParser.DOT)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Wrong_field_typeContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def id_or_kw(self):
            return self.getTypedRuleContext(ZmeiLangParser.Id_or_kwContext,0)


        def getRuleIndex(self):
            return ZmeiLangParser.RULE_wrong_field_type

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterWrong_field_type" ):
                listener.enterWrong_field_type(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitWrong_field_type" ):
                listener.exitWrong_field_type(self)




    def wrong_field_type(self):

        localctx = ZmeiLangParser.Wrong_field_typeContext(self, self._ctx, self.state)
        self.enterRule(localctx, 124, self.RULE_wrong_field_type)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1158
            self.id_or_kw()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Col_field_exprContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def col_field_expr_marker(self):
            return self.getTypedRuleContext(ZmeiLangParser.Col_field_expr_markerContext,0)


        def col_feild_expr_code(self):
            return self.getTypedRuleContext(ZmeiLangParser.Col_feild_expr_codeContext,0)


        def getRuleIndex(self):
            return ZmeiLangParser.RULE_col_field_expr

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterCol_field_expr" ):
                listener.enterCol_field_expr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitCol_field_expr" ):
                listener.exitCol_field_expr(self)




    def col_field_expr(self):

        localctx = ZmeiLangParser.Col_field_exprContext(self, self._ctx, self.state)
        self.enterRule(localctx, 126, self.RULE_col_field_expr)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1160
            self.col_field_expr_marker()
            self.state = 1161
            self.col_feild_expr_code()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Col_field_expr_markerContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ASSIGN(self):
            return self.getToken(ZmeiLangParser.ASSIGN, 0)

        def ASSIGN_STATIC(self):
            return self.getToken(ZmeiLangParser.ASSIGN_STATIC, 0)

        def getRuleIndex(self):
            return ZmeiLangParser.RULE_col_field_expr_marker

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterCol_field_expr_marker" ):
                listener.enterCol_field_expr_marker(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitCol_field_expr_marker" ):
                listener.exitCol_field_expr_marker(self)




    def col_field_expr_marker(self):

        localctx = ZmeiLangParser.Col_field_expr_markerContext(self, self._ctx, self.state)
        self.enterRule(localctx, 128, self.RULE_col_field_expr_marker)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1163
            _la = self._input.LA(1)
            if not(_la==ZmeiLangParser.ASSIGN or _la==ZmeiLangParser.ASSIGN_STATIC):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Col_feild_expr_codeContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def PYTHON_CODE(self):
            return self.getToken(ZmeiLangParser.PYTHON_CODE, 0)

        def getRuleIndex(self):
            return ZmeiLangParser.RULE_col_feild_expr_code

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterCol_feild_expr_code" ):
                listener.enterCol_feild_expr_code(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitCol_feild_expr_code" ):
                listener.exitCol_feild_expr_code(self)




    def col_feild_expr_code(self):

        localctx = ZmeiLangParser.Col_feild_expr_codeContext(self, self._ctx, self.state)
        self.enterRule(localctx, 130, self.RULE_col_feild_expr_code)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1165
            self.match(ZmeiLangParser.PYTHON_CODE)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class String_or_quotedContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def STRING_DQ(self):
            return self.getToken(ZmeiLangParser.STRING_DQ, 0)

        def STRING_SQ(self):
            return self.getToken(ZmeiLangParser.STRING_SQ, 0)

        def id_or_kw(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(ZmeiLangParser.Id_or_kwContext)
            else:
                return self.getTypedRuleContext(ZmeiLangParser.Id_or_kwContext,i)


        def getRuleIndex(self):
            return ZmeiLangParser.RULE_string_or_quoted

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterString_or_quoted" ):
                listener.enterString_or_quoted(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitString_or_quoted" ):
                listener.exitString_or_quoted(self)




    def string_or_quoted(self):

        localctx = ZmeiLangParser.String_or_quotedContext(self, self._ctx, self.state)
        self.enterRule(localctx, 132, self.RULE_string_or_quoted)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1174
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [ZmeiLangParser.KW_AUTH_TYPE_BASIC, ZmeiLangParser.KW_AUTH_TYPE_SESSION, ZmeiLangParser.KW_AUTH_TYPE_TOKEN, ZmeiLangParser.COL_FIELD_TYPE_LONGTEXT, ZmeiLangParser.COL_FIELD_TYPE_HTML, ZmeiLangParser.COL_FIELD_TYPE_HTML_MEDIA, ZmeiLangParser.COL_FIELD_TYPE_FLOAT, ZmeiLangParser.COL_FIELD_TYPE_DECIMAL, ZmeiLangParser.COL_FIELD_TYPE_DATE, ZmeiLangParser.COL_FIELD_TYPE_DATETIME, ZmeiLangParser.COL_FIELD_TYPE_CREATE_TIME, ZmeiLangParser.COL_FIELD_TYPE_UPDATE_TIME, ZmeiLangParser.COL_FIELD_TYPE_IMAGE, ZmeiLangParser.COL_FIELD_TYPE_FILE, ZmeiLangParser.COL_FIELD_TYPE_FILER_IMAGE, ZmeiLangParser.COL_FIELD_TYPE_FILER_FILE, ZmeiLangParser.COL_FIELD_TYPE_FILER_FOLDER, ZmeiLangParser.COL_FIELD_TYPE_FILER_IMAGE_FOLDER, ZmeiLangParser.COL_FIELD_TYPE_TEXT, ZmeiLangParser.COL_FIELD_TYPE_INT, ZmeiLangParser.COL_FIELD_TYPE_SLUG, ZmeiLangParser.COL_FIELD_TYPE_BOOL, ZmeiLangParser.COL_FIELD_TYPE_ONE, ZmeiLangParser.COL_FIELD_TYPE_ONE2ONE, ZmeiLangParser.COL_FIELD_TYPE_MANY, ZmeiLangParser.COL_FIELD_CHOICES, ZmeiLangParser.KW_THEME, ZmeiLangParser.KW_INSTALL, ZmeiLangParser.KW_HEADER, ZmeiLangParser.KW_SERVICES, ZmeiLangParser.KW_SELENIUM_PYTEST, ZmeiLangParser.KW_CHILD, ZmeiLangParser.KW_FILTER_OUT, ZmeiLangParser.KW_FILTER_IN, ZmeiLangParser.KW_PAGE, ZmeiLangParser.KW_LINK_SUFFIX, ZmeiLangParser.KW_URL_PREFIX, ZmeiLangParser.KW_CAN_EDIT, ZmeiLangParser.KW_OBJECT_EXPR, ZmeiLangParser.KW_BLOCK, ZmeiLangParser.KW_ITEM_NAME, ZmeiLangParser.KW_PK_PARAM, ZmeiLangParser.KW_LIST_FIELDS, ZmeiLangParser.KW_DELETE, ZmeiLangParser.KW_EDIT, ZmeiLangParser.KW_CREATE, ZmeiLangParser.KW_DETAIL, ZmeiLangParser.KW_SKIP, ZmeiLangParser.KW_FROM, ZmeiLangParser.KW_POLY_LIST, ZmeiLangParser.KW_CSS, ZmeiLangParser.KW_JS, ZmeiLangParser.KW_INLINE_TYPE_TABULAR, ZmeiLangParser.KW_INLINE_TYPE_STACKED, ZmeiLangParser.KW_INLINE_TYPE_POLYMORPHIC, ZmeiLangParser.KW_INLINE, ZmeiLangParser.KW_TYPE, ZmeiLangParser.KW_USER_FIELD, ZmeiLangParser.KW_ANNOTATE, ZmeiLangParser.KW_ON_CREATE, ZmeiLangParser.KW_QUERY, ZmeiLangParser.KW_AUTH, ZmeiLangParser.KW_COUNT, ZmeiLangParser.KW_I18N, ZmeiLangParser.KW_EXTENSION, ZmeiLangParser.KW_TABS, ZmeiLangParser.KW_LIST, ZmeiLangParser.KW_READ_ONLY, ZmeiLangParser.KW_LIST_EDITABLE, ZmeiLangParser.KW_LIST_FILTER, ZmeiLangParser.KW_LIST_SEARCH, ZmeiLangParser.KW_FIELDS, ZmeiLangParser.KW_IMPORT, ZmeiLangParser.KW_AS, ZmeiLangParser.WRITE_MODE, ZmeiLangParser.BOOL, ZmeiLangParser.ID]:
                self.state = 1168 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while True:
                    self.state = 1167
                    self.id_or_kw()
                    self.state = 1170 
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    if not ((((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << ZmeiLangParser.KW_AUTH_TYPE_BASIC) | (1 << ZmeiLangParser.KW_AUTH_TYPE_SESSION) | (1 << ZmeiLangParser.KW_AUTH_TYPE_TOKEN) | (1 << ZmeiLangParser.COL_FIELD_TYPE_LONGTEXT) | (1 << ZmeiLangParser.COL_FIELD_TYPE_HTML) | (1 << ZmeiLangParser.COL_FIELD_TYPE_HTML_MEDIA) | (1 << ZmeiLangParser.COL_FIELD_TYPE_FLOAT) | (1 << ZmeiLangParser.COL_FIELD_TYPE_DECIMAL) | (1 << ZmeiLangParser.COL_FIELD_TYPE_DATE) | (1 << ZmeiLangParser.COL_FIELD_TYPE_DATETIME) | (1 << ZmeiLangParser.COL_FIELD_TYPE_CREATE_TIME) | (1 << ZmeiLangParser.COL_FIELD_TYPE_UPDATE_TIME) | (1 << ZmeiLangParser.COL_FIELD_TYPE_IMAGE) | (1 << ZmeiLangParser.COL_FIELD_TYPE_FILE) | (1 << ZmeiLangParser.COL_FIELD_TYPE_FILER_IMAGE) | (1 << ZmeiLangParser.COL_FIELD_TYPE_FILER_FILE) | (1 << ZmeiLangParser.COL_FIELD_TYPE_FILER_FOLDER) | (1 << ZmeiLangParser.COL_FIELD_TYPE_FILER_IMAGE_FOLDER) | (1 << ZmeiLangParser.COL_FIELD_TYPE_TEXT) | (1 << ZmeiLangParser.COL_FIELD_TYPE_INT) | (1 << ZmeiLangParser.COL_FIELD_TYPE_SLUG) | (1 << ZmeiLangParser.COL_FIELD_TYPE_BOOL))) != 0) or ((((_la - 64)) & ~0x3f) == 0 and ((1 << (_la - 64)) & ((1 << (ZmeiLangParser.COL_FIELD_TYPE_ONE - 64)) | (1 << (ZmeiLangParser.COL_FIELD_TYPE_ONE2ONE - 64)) | (1 << (ZmeiLangParser.COL_FIELD_TYPE_MANY - 64)) | (1 << (ZmeiLangParser.COL_FIELD_CHOICES - 64)) | (1 << (ZmeiLangParser.KW_THEME - 64)) | (1 << (ZmeiLangParser.KW_INSTALL - 64)) | (1 << (ZmeiLangParser.KW_HEADER - 64)) | (1 << (ZmeiLangParser.KW_SERVICES - 64)) | (1 << (ZmeiLangParser.KW_SELENIUM_PYTEST - 64)) | (1 << (ZmeiLangParser.KW_CHILD - 64)) | (1 << (ZmeiLangParser.KW_FILTER_OUT - 64)) | (1 << (ZmeiLangParser.KW_FILTER_IN - 64)) | (1 << (ZmeiLangParser.KW_PAGE - 64)) | (1 << (ZmeiLangParser.KW_LINK_SUFFIX - 64)) | (1 << (ZmeiLangParser.KW_URL_PREFIX - 64)) | (1 << (ZmeiLangParser.KW_CAN_EDIT - 64)) | (1 << (ZmeiLangParser.KW_OBJECT_EXPR - 64)) | (1 << (ZmeiLangParser.KW_BLOCK - 64)) | (1 << (ZmeiLangParser.KW_ITEM_NAME - 64)) | (1 << (ZmeiLangParser.KW_PK_PARAM - 64)) | (1 << (ZmeiLangParser.KW_LIST_FIELDS - 64)) | (1 << (ZmeiLangParser.KW_DELETE - 64)) | (1 << (ZmeiLangParser.KW_EDIT - 64)) | (1 << (ZmeiLangParser.KW_CREATE - 64)) | (1 << (ZmeiLangParser.KW_DETAIL - 64)) | (1 << (ZmeiLangParser.KW_SKIP - 64)) | (1 << (ZmeiLangParser.KW_FROM - 64)) | (1 << (ZmeiLangParser.KW_POLY_LIST - 64)) | (1 << (ZmeiLangParser.KW_CSS - 64)) | (1 << (ZmeiLangParser.KW_JS - 64)) | (1 << (ZmeiLangParser.KW_INLINE_TYPE_TABULAR - 64)) | (1 << (ZmeiLangParser.KW_INLINE_TYPE_STACKED - 64)) | (1 << (ZmeiLangParser.KW_INLINE_TYPE_POLYMORPHIC - 64)) | (1 << (ZmeiLangParser.KW_INLINE - 64)) | (1 << (ZmeiLangParser.KW_TYPE - 64)) | (1 << (ZmeiLangParser.KW_USER_FIELD - 64)) | (1 << (ZmeiLangParser.KW_ANNOTATE - 64)) | (1 << (ZmeiLangParser.KW_ON_CREATE - 64)) | (1 << (ZmeiLangParser.KW_QUERY - 64)) | (1 << (ZmeiLangParser.KW_AUTH - 64)) | (1 << (ZmeiLangParser.KW_COUNT - 64)) | (1 << (ZmeiLangParser.KW_I18N - 64)) | (1 << (ZmeiLangParser.KW_EXTENSION - 64)) | (1 << (ZmeiLangParser.KW_TABS - 64)) | (1 << (ZmeiLangParser.KW_LIST - 64)) | (1 << (ZmeiLangParser.KW_READ_ONLY - 64)) | (1 << (ZmeiLangParser.KW_LIST_EDITABLE - 64)) | (1 << (ZmeiLangParser.KW_LIST_FILTER - 64)) | (1 << (ZmeiLangParser.KW_LIST_SEARCH - 64)) | (1 << (ZmeiLangParser.KW_FIELDS - 64)) | (1 << (ZmeiLangParser.KW_IMPORT - 64)) | (1 << (ZmeiLangParser.KW_AS - 64)) | (1 << (ZmeiLangParser.WRITE_MODE - 64)) | (1 << (ZmeiLangParser.BOOL - 64)) | (1 << (ZmeiLangParser.ID - 64)))) != 0)):
                        break

                pass
            elif token in [ZmeiLangParser.STRING_DQ]:
                self.state = 1172
                self.match(ZmeiLangParser.STRING_DQ)
                pass
            elif token in [ZmeiLangParser.STRING_SQ]:
                self.state = 1173
                self.match(ZmeiLangParser.STRING_SQ)
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Col_field_help_textContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def QUESTION_MARK(self):
            return self.getToken(ZmeiLangParser.QUESTION_MARK, 0)

        def string_or_quoted(self):
            return self.getTypedRuleContext(ZmeiLangParser.String_or_quotedContext,0)


        def getRuleIndex(self):
            return ZmeiLangParser.RULE_col_field_help_text

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterCol_field_help_text" ):
                listener.enterCol_field_help_text(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitCol_field_help_text" ):
                listener.exitCol_field_help_text(self)




    def col_field_help_text(self):

        localctx = ZmeiLangParser.Col_field_help_textContext(self, self._ctx, self.state)
        self.enterRule(localctx, 134, self.RULE_col_field_help_text)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1176
            self.match(ZmeiLangParser.QUESTION_MARK)
            self.state = 1177
            self.string_or_quoted()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Col_field_verbose_nameContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def SLASH(self):
            return self.getToken(ZmeiLangParser.SLASH, 0)

        def string_or_quoted(self):
            return self.getTypedRuleContext(ZmeiLangParser.String_or_quotedContext,0)


        def getRuleIndex(self):
            return ZmeiLangParser.RULE_col_field_verbose_name

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterCol_field_verbose_name" ):
                listener.enterCol_field_verbose_name(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitCol_field_verbose_name" ):
                listener.exitCol_field_verbose_name(self)




    def col_field_verbose_name(self):

        localctx = ZmeiLangParser.Col_field_verbose_nameContext(self, self._ctx, self.state)
        self.enterRule(localctx, 136, self.RULE_col_field_verbose_name)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1179
            self.match(ZmeiLangParser.SLASH)
            self.state = 1180
            self.string_or_quoted()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Col_field_nameContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def id_or_kw(self):
            return self.getTypedRuleContext(ZmeiLangParser.Id_or_kwContext,0)


        def getRuleIndex(self):
            return ZmeiLangParser.RULE_col_field_name

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterCol_field_name" ):
                listener.enterCol_field_name(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitCol_field_name" ):
                listener.exitCol_field_name(self)




    def col_field_name(self):

        localctx = ZmeiLangParser.Col_field_nameContext(self, self._ctx, self.state)
        self.enterRule(localctx, 138, self.RULE_col_field_name)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1182
            self.id_or_kw()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Col_modifierContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def EQUALS(self):
            return self.getToken(ZmeiLangParser.EQUALS, 0)

        def DOLLAR(self):
            return self.getToken(ZmeiLangParser.DOLLAR, 0)

        def AMP(self):
            return self.getToken(ZmeiLangParser.AMP, 0)

        def EXCLAM(self):
            return self.getToken(ZmeiLangParser.EXCLAM, 0)

        def STAR(self):
            return self.getToken(ZmeiLangParser.STAR, 0)

        def APPROX(self):
            return self.getToken(ZmeiLangParser.APPROX, 0)

        def getRuleIndex(self):
            return ZmeiLangParser.RULE_col_modifier

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterCol_modifier" ):
                listener.enterCol_modifier(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitCol_modifier" ):
                listener.exitCol_modifier(self)




    def col_modifier(self):

        localctx = ZmeiLangParser.Col_modifierContext(self, self._ctx, self.state)
        self.enterRule(localctx, 140, self.RULE_col_modifier)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1184
            _la = self._input.LA(1)
            if not(((((_la - 137)) & ~0x3f) == 0 and ((1 << (_la - 137)) & ((1 << (ZmeiLangParser.EQUALS - 137)) | (1 << (ZmeiLangParser.DOLLAR - 137)) | (1 << (ZmeiLangParser.AMP - 137)) | (1 << (ZmeiLangParser.EXCLAM - 137)) | (1 << (ZmeiLangParser.STAR - 137)) | (1 << (ZmeiLangParser.APPROX - 137)))) != 0)):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Col_field_defContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def field_longtext(self):
            return self.getTypedRuleContext(ZmeiLangParser.Field_longtextContext,0)


        def field_html_media(self):
            return self.getTypedRuleContext(ZmeiLangParser.Field_html_mediaContext,0)


        def field_html(self):
            return self.getTypedRuleContext(ZmeiLangParser.Field_htmlContext,0)


        def field_float(self):
            return self.getTypedRuleContext(ZmeiLangParser.Field_floatContext,0)


        def field_decimal(self):
            return self.getTypedRuleContext(ZmeiLangParser.Field_decimalContext,0)


        def field_date(self):
            return self.getTypedRuleContext(ZmeiLangParser.Field_dateContext,0)


        def field_datetime(self):
            return self.getTypedRuleContext(ZmeiLangParser.Field_datetimeContext,0)


        def field_create_time(self):
            return self.getTypedRuleContext(ZmeiLangParser.Field_create_timeContext,0)


        def field_update_time(self):
            return self.getTypedRuleContext(ZmeiLangParser.Field_update_timeContext,0)


        def field_text(self):
            return self.getTypedRuleContext(ZmeiLangParser.Field_textContext,0)


        def field_int(self):
            return self.getTypedRuleContext(ZmeiLangParser.Field_intContext,0)


        def field_slug(self):
            return self.getTypedRuleContext(ZmeiLangParser.Field_slugContext,0)


        def field_bool(self):
            return self.getTypedRuleContext(ZmeiLangParser.Field_boolContext,0)


        def field_relation(self):
            return self.getTypedRuleContext(ZmeiLangParser.Field_relationContext,0)


        def field_image(self):
            return self.getTypedRuleContext(ZmeiLangParser.Field_imageContext,0)


        def field_file(self):
            return self.getTypedRuleContext(ZmeiLangParser.Field_fileContext,0)


        def field_filer_file(self):
            return self.getTypedRuleContext(ZmeiLangParser.Field_filer_fileContext,0)


        def field_filer_folder(self):
            return self.getTypedRuleContext(ZmeiLangParser.Field_filer_folderContext,0)


        def getRuleIndex(self):
            return ZmeiLangParser.RULE_col_field_def

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterCol_field_def" ):
                listener.enterCol_field_def(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitCol_field_def" ):
                listener.exitCol_field_def(self)




    def col_field_def(self):

        localctx = ZmeiLangParser.Col_field_defContext(self, self._ctx, self.state)
        self.enterRule(localctx, 142, self.RULE_col_field_def)
        try:
            self.state = 1204
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [ZmeiLangParser.COL_FIELD_TYPE_LONGTEXT]:
                self.enterOuterAlt(localctx, 1)
                self.state = 1186
                self.field_longtext()
                pass
            elif token in [ZmeiLangParser.COL_FIELD_TYPE_HTML_MEDIA]:
                self.enterOuterAlt(localctx, 2)
                self.state = 1187
                self.field_html_media()
                pass
            elif token in [ZmeiLangParser.COL_FIELD_TYPE_HTML]:
                self.enterOuterAlt(localctx, 3)
                self.state = 1188
                self.field_html()
                pass
            elif token in [ZmeiLangParser.COL_FIELD_TYPE_FLOAT]:
                self.enterOuterAlt(localctx, 4)
                self.state = 1189
                self.field_float()
                pass
            elif token in [ZmeiLangParser.COL_FIELD_TYPE_DECIMAL]:
                self.enterOuterAlt(localctx, 5)
                self.state = 1190
                self.field_decimal()
                pass
            elif token in [ZmeiLangParser.COL_FIELD_TYPE_DATE]:
                self.enterOuterAlt(localctx, 6)
                self.state = 1191
                self.field_date()
                pass
            elif token in [ZmeiLangParser.COL_FIELD_TYPE_DATETIME]:
                self.enterOuterAlt(localctx, 7)
                self.state = 1192
                self.field_datetime()
                pass
            elif token in [ZmeiLangParser.COL_FIELD_TYPE_CREATE_TIME]:
                self.enterOuterAlt(localctx, 8)
                self.state = 1193
                self.field_create_time()
                pass
            elif token in [ZmeiLangParser.COL_FIELD_TYPE_UPDATE_TIME]:
                self.enterOuterAlt(localctx, 9)
                self.state = 1194
                self.field_update_time()
                pass
            elif token in [ZmeiLangParser.COL_FIELD_TYPE_TEXT]:
                self.enterOuterAlt(localctx, 10)
                self.state = 1195
                self.field_text()
                pass
            elif token in [ZmeiLangParser.COL_FIELD_TYPE_INT]:
                self.enterOuterAlt(localctx, 11)
                self.state = 1196
                self.field_int()
                pass
            elif token in [ZmeiLangParser.COL_FIELD_TYPE_SLUG]:
                self.enterOuterAlt(localctx, 12)
                self.state = 1197
                self.field_slug()
                pass
            elif token in [ZmeiLangParser.COL_FIELD_TYPE_BOOL]:
                self.enterOuterAlt(localctx, 13)
                self.state = 1198
                self.field_bool()
                pass
            elif token in [ZmeiLangParser.COL_FIELD_TYPE_ONE, ZmeiLangParser.COL_FIELD_TYPE_ONE2ONE, ZmeiLangParser.COL_FIELD_TYPE_MANY]:
                self.enterOuterAlt(localctx, 14)
                self.state = 1199
                self.field_relation()
                pass
            elif token in [ZmeiLangParser.COL_FIELD_TYPE_IMAGE, ZmeiLangParser.COL_FIELD_TYPE_FILER_IMAGE, ZmeiLangParser.COL_FIELD_TYPE_FILER_IMAGE_FOLDER]:
                self.enterOuterAlt(localctx, 15)
                self.state = 1200
                self.field_image()
                pass
            elif token in [ZmeiLangParser.COL_FIELD_TYPE_FILE]:
                self.enterOuterAlt(localctx, 16)
                self.state = 1201
                self.field_file()
                pass
            elif token in [ZmeiLangParser.COL_FIELD_TYPE_FILER_FILE]:
                self.enterOuterAlt(localctx, 17)
                self.state = 1202
                self.field_filer_file()
                pass
            elif token in [ZmeiLangParser.COL_FIELD_TYPE_FILER_FOLDER]:
                self.enterOuterAlt(localctx, 18)
                self.state = 1203
                self.field_filer_folder()
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Field_longtextContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def COL_FIELD_TYPE_LONGTEXT(self):
            return self.getToken(ZmeiLangParser.COL_FIELD_TYPE_LONGTEXT, 0)

        def getRuleIndex(self):
            return ZmeiLangParser.RULE_field_longtext

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterField_longtext" ):
                listener.enterField_longtext(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitField_longtext" ):
                listener.exitField_longtext(self)




    def field_longtext(self):

        localctx = ZmeiLangParser.Field_longtextContext(self, self._ctx, self.state)
        self.enterRule(localctx, 144, self.RULE_field_longtext)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1206
            self.match(ZmeiLangParser.COL_FIELD_TYPE_LONGTEXT)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Field_htmlContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def COL_FIELD_TYPE_HTML(self):
            return self.getToken(ZmeiLangParser.COL_FIELD_TYPE_HTML, 0)

        def getRuleIndex(self):
            return ZmeiLangParser.RULE_field_html

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterField_html" ):
                listener.enterField_html(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitField_html" ):
                listener.exitField_html(self)




    def field_html(self):

        localctx = ZmeiLangParser.Field_htmlContext(self, self._ctx, self.state)
        self.enterRule(localctx, 146, self.RULE_field_html)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1208
            self.match(ZmeiLangParser.COL_FIELD_TYPE_HTML)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Field_html_mediaContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def COL_FIELD_TYPE_HTML_MEDIA(self):
            return self.getToken(ZmeiLangParser.COL_FIELD_TYPE_HTML_MEDIA, 0)

        def getRuleIndex(self):
            return ZmeiLangParser.RULE_field_html_media

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterField_html_media" ):
                listener.enterField_html_media(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitField_html_media" ):
                listener.exitField_html_media(self)




    def field_html_media(self):

        localctx = ZmeiLangParser.Field_html_mediaContext(self, self._ctx, self.state)
        self.enterRule(localctx, 148, self.RULE_field_html_media)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1210
            self.match(ZmeiLangParser.COL_FIELD_TYPE_HTML_MEDIA)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Field_floatContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def COL_FIELD_TYPE_FLOAT(self):
            return self.getToken(ZmeiLangParser.COL_FIELD_TYPE_FLOAT, 0)

        def getRuleIndex(self):
            return ZmeiLangParser.RULE_field_float

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterField_float" ):
                listener.enterField_float(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitField_float" ):
                listener.exitField_float(self)




    def field_float(self):

        localctx = ZmeiLangParser.Field_floatContext(self, self._ctx, self.state)
        self.enterRule(localctx, 150, self.RULE_field_float)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1212
            self.match(ZmeiLangParser.COL_FIELD_TYPE_FLOAT)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Field_decimalContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def COL_FIELD_TYPE_DECIMAL(self):
            return self.getToken(ZmeiLangParser.COL_FIELD_TYPE_DECIMAL, 0)

        def getRuleIndex(self):
            return ZmeiLangParser.RULE_field_decimal

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterField_decimal" ):
                listener.enterField_decimal(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitField_decimal" ):
                listener.exitField_decimal(self)




    def field_decimal(self):

        localctx = ZmeiLangParser.Field_decimalContext(self, self._ctx, self.state)
        self.enterRule(localctx, 152, self.RULE_field_decimal)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1214
            self.match(ZmeiLangParser.COL_FIELD_TYPE_DECIMAL)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Field_dateContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def COL_FIELD_TYPE_DATE(self):
            return self.getToken(ZmeiLangParser.COL_FIELD_TYPE_DATE, 0)

        def getRuleIndex(self):
            return ZmeiLangParser.RULE_field_date

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterField_date" ):
                listener.enterField_date(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitField_date" ):
                listener.exitField_date(self)




    def field_date(self):

        localctx = ZmeiLangParser.Field_dateContext(self, self._ctx, self.state)
        self.enterRule(localctx, 154, self.RULE_field_date)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1216
            self.match(ZmeiLangParser.COL_FIELD_TYPE_DATE)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Field_datetimeContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def COL_FIELD_TYPE_DATETIME(self):
            return self.getToken(ZmeiLangParser.COL_FIELD_TYPE_DATETIME, 0)

        def getRuleIndex(self):
            return ZmeiLangParser.RULE_field_datetime

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterField_datetime" ):
                listener.enterField_datetime(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitField_datetime" ):
                listener.exitField_datetime(self)




    def field_datetime(self):

        localctx = ZmeiLangParser.Field_datetimeContext(self, self._ctx, self.state)
        self.enterRule(localctx, 156, self.RULE_field_datetime)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1218
            self.match(ZmeiLangParser.COL_FIELD_TYPE_DATETIME)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Field_create_timeContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def COL_FIELD_TYPE_CREATE_TIME(self):
            return self.getToken(ZmeiLangParser.COL_FIELD_TYPE_CREATE_TIME, 0)

        def getRuleIndex(self):
            return ZmeiLangParser.RULE_field_create_time

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterField_create_time" ):
                listener.enterField_create_time(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitField_create_time" ):
                listener.exitField_create_time(self)




    def field_create_time(self):

        localctx = ZmeiLangParser.Field_create_timeContext(self, self._ctx, self.state)
        self.enterRule(localctx, 158, self.RULE_field_create_time)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1220
            self.match(ZmeiLangParser.COL_FIELD_TYPE_CREATE_TIME)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Field_update_timeContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def COL_FIELD_TYPE_UPDATE_TIME(self):
            return self.getToken(ZmeiLangParser.COL_FIELD_TYPE_UPDATE_TIME, 0)

        def getRuleIndex(self):
            return ZmeiLangParser.RULE_field_update_time

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterField_update_time" ):
                listener.enterField_update_time(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitField_update_time" ):
                listener.exitField_update_time(self)




    def field_update_time(self):

        localctx = ZmeiLangParser.Field_update_timeContext(self, self._ctx, self.state)
        self.enterRule(localctx, 160, self.RULE_field_update_time)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1222
            self.match(ZmeiLangParser.COL_FIELD_TYPE_UPDATE_TIME)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Field_fileContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def COL_FIELD_TYPE_FILE(self):
            return self.getToken(ZmeiLangParser.COL_FIELD_TYPE_FILE, 0)

        def getRuleIndex(self):
            return ZmeiLangParser.RULE_field_file

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterField_file" ):
                listener.enterField_file(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitField_file" ):
                listener.exitField_file(self)




    def field_file(self):

        localctx = ZmeiLangParser.Field_fileContext(self, self._ctx, self.state)
        self.enterRule(localctx, 162, self.RULE_field_file)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1224
            self.match(ZmeiLangParser.COL_FIELD_TYPE_FILE)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Field_filer_fileContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def COL_FIELD_TYPE_FILER_FILE(self):
            return self.getToken(ZmeiLangParser.COL_FIELD_TYPE_FILER_FILE, 0)

        def getRuleIndex(self):
            return ZmeiLangParser.RULE_field_filer_file

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterField_filer_file" ):
                listener.enterField_filer_file(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitField_filer_file" ):
                listener.exitField_filer_file(self)




    def field_filer_file(self):

        localctx = ZmeiLangParser.Field_filer_fileContext(self, self._ctx, self.state)
        self.enterRule(localctx, 164, self.RULE_field_filer_file)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1226
            self.match(ZmeiLangParser.COL_FIELD_TYPE_FILER_FILE)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Field_filer_folderContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def COL_FIELD_TYPE_FILER_FOLDER(self):
            return self.getToken(ZmeiLangParser.COL_FIELD_TYPE_FILER_FOLDER, 0)

        def getRuleIndex(self):
            return ZmeiLangParser.RULE_field_filer_folder

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterField_filer_folder" ):
                listener.enterField_filer_folder(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitField_filer_folder" ):
                listener.exitField_filer_folder(self)




    def field_filer_folder(self):

        localctx = ZmeiLangParser.Field_filer_folderContext(self, self._ctx, self.state)
        self.enterRule(localctx, 166, self.RULE_field_filer_folder)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1228
            self.match(ZmeiLangParser.COL_FIELD_TYPE_FILER_FOLDER)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Field_textContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def COL_FIELD_TYPE_TEXT(self):
            return self.getToken(ZmeiLangParser.COL_FIELD_TYPE_TEXT, 0)

        def BRACE_OPEN(self):
            return self.getToken(ZmeiLangParser.BRACE_OPEN, 0)

        def field_text_size(self):
            return self.getTypedRuleContext(ZmeiLangParser.Field_text_sizeContext,0)


        def BRACE_CLOSE(self):
            return self.getToken(ZmeiLangParser.BRACE_CLOSE, 0)

        def COMA(self):
            return self.getToken(ZmeiLangParser.COMA, 0)

        def field_text_choices(self):
            return self.getTypedRuleContext(ZmeiLangParser.Field_text_choicesContext,0)


        def getRuleIndex(self):
            return ZmeiLangParser.RULE_field_text

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterField_text" ):
                listener.enterField_text(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitField_text" ):
                listener.exitField_text(self)




    def field_text(self):

        localctx = ZmeiLangParser.Field_textContext(self, self._ctx, self.state)
        self.enterRule(localctx, 168, self.RULE_field_text)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1230
            self.match(ZmeiLangParser.COL_FIELD_TYPE_TEXT)
            self.state = 1239
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==ZmeiLangParser.BRACE_OPEN:
                self.state = 1231
                self.match(ZmeiLangParser.BRACE_OPEN)
                self.state = 1232
                self.field_text_size()
                self.state = 1235
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==ZmeiLangParser.COMA:
                    self.state = 1233
                    self.match(ZmeiLangParser.COMA)
                    self.state = 1234
                    self.field_text_choices()


                self.state = 1237
                self.match(ZmeiLangParser.BRACE_CLOSE)


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Field_text_sizeContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def DIGIT(self):
            return self.getToken(ZmeiLangParser.DIGIT, 0)

        def QUESTION_MARK(self):
            return self.getToken(ZmeiLangParser.QUESTION_MARK, 0)

        def getRuleIndex(self):
            return ZmeiLangParser.RULE_field_text_size

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterField_text_size" ):
                listener.enterField_text_size(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitField_text_size" ):
                listener.exitField_text_size(self)




    def field_text_size(self):

        localctx = ZmeiLangParser.Field_text_sizeContext(self, self._ctx, self.state)
        self.enterRule(localctx, 170, self.RULE_field_text_size)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1241
            _la = self._input.LA(1)
            if not(_la==ZmeiLangParser.DIGIT or _la==ZmeiLangParser.QUESTION_MARK):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Field_text_choicesContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def COL_FIELD_CHOICES(self):
            return self.getToken(ZmeiLangParser.COL_FIELD_CHOICES, 0)

        def EQUALS(self):
            return self.getToken(ZmeiLangParser.EQUALS, 0)

        def field_text_choice(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(ZmeiLangParser.Field_text_choiceContext)
            else:
                return self.getTypedRuleContext(ZmeiLangParser.Field_text_choiceContext,i)


        def COMA(self, i:int=None):
            if i is None:
                return self.getTokens(ZmeiLangParser.COMA)
            else:
                return self.getToken(ZmeiLangParser.COMA, i)

        def getRuleIndex(self):
            return ZmeiLangParser.RULE_field_text_choices

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterField_text_choices" ):
                listener.enterField_text_choices(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitField_text_choices" ):
                listener.exitField_text_choices(self)




    def field_text_choices(self):

        localctx = ZmeiLangParser.Field_text_choicesContext(self, self._ctx, self.state)
        self.enterRule(localctx, 172, self.RULE_field_text_choices)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1243
            self.match(ZmeiLangParser.COL_FIELD_CHOICES)
            self.state = 1244
            self.match(ZmeiLangParser.EQUALS)
            self.state = 1245
            self.field_text_choice()
            self.state = 1250
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==ZmeiLangParser.COMA:
                self.state = 1246
                self.match(ZmeiLangParser.COMA)
                self.state = 1247
                self.field_text_choice()
                self.state = 1252
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Field_text_choiceContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def field_text_choice_val(self):
            return self.getTypedRuleContext(ZmeiLangParser.Field_text_choice_valContext,0)


        def field_text_choice_key(self):
            return self.getTypedRuleContext(ZmeiLangParser.Field_text_choice_keyContext,0)


        def getRuleIndex(self):
            return ZmeiLangParser.RULE_field_text_choice

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterField_text_choice" ):
                listener.enterField_text_choice(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitField_text_choice" ):
                listener.exitField_text_choice(self)




    def field_text_choice(self):

        localctx = ZmeiLangParser.Field_text_choiceContext(self, self._ctx, self.state)
        self.enterRule(localctx, 174, self.RULE_field_text_choice)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1254
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,106,self._ctx)
            if la_ == 1:
                self.state = 1253
                self.field_text_choice_key()


            self.state = 1256
            self.field_text_choice_val()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Field_text_choice_valContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def id_or_kw(self):
            return self.getTypedRuleContext(ZmeiLangParser.Id_or_kwContext,0)


        def STRING_DQ(self):
            return self.getToken(ZmeiLangParser.STRING_DQ, 0)

        def STRING_SQ(self):
            return self.getToken(ZmeiLangParser.STRING_SQ, 0)

        def getRuleIndex(self):
            return ZmeiLangParser.RULE_field_text_choice_val

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterField_text_choice_val" ):
                listener.enterField_text_choice_val(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitField_text_choice_val" ):
                listener.exitField_text_choice_val(self)




    def field_text_choice_val(self):

        localctx = ZmeiLangParser.Field_text_choice_valContext(self, self._ctx, self.state)
        self.enterRule(localctx, 176, self.RULE_field_text_choice_val)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1261
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [ZmeiLangParser.KW_AUTH_TYPE_BASIC, ZmeiLangParser.KW_AUTH_TYPE_SESSION, ZmeiLangParser.KW_AUTH_TYPE_TOKEN, ZmeiLangParser.COL_FIELD_TYPE_LONGTEXT, ZmeiLangParser.COL_FIELD_TYPE_HTML, ZmeiLangParser.COL_FIELD_TYPE_HTML_MEDIA, ZmeiLangParser.COL_FIELD_TYPE_FLOAT, ZmeiLangParser.COL_FIELD_TYPE_DECIMAL, ZmeiLangParser.COL_FIELD_TYPE_DATE, ZmeiLangParser.COL_FIELD_TYPE_DATETIME, ZmeiLangParser.COL_FIELD_TYPE_CREATE_TIME, ZmeiLangParser.COL_FIELD_TYPE_UPDATE_TIME, ZmeiLangParser.COL_FIELD_TYPE_IMAGE, ZmeiLangParser.COL_FIELD_TYPE_FILE, ZmeiLangParser.COL_FIELD_TYPE_FILER_IMAGE, ZmeiLangParser.COL_FIELD_TYPE_FILER_FILE, ZmeiLangParser.COL_FIELD_TYPE_FILER_FOLDER, ZmeiLangParser.COL_FIELD_TYPE_FILER_IMAGE_FOLDER, ZmeiLangParser.COL_FIELD_TYPE_TEXT, ZmeiLangParser.COL_FIELD_TYPE_INT, ZmeiLangParser.COL_FIELD_TYPE_SLUG, ZmeiLangParser.COL_FIELD_TYPE_BOOL, ZmeiLangParser.COL_FIELD_TYPE_ONE, ZmeiLangParser.COL_FIELD_TYPE_ONE2ONE, ZmeiLangParser.COL_FIELD_TYPE_MANY, ZmeiLangParser.COL_FIELD_CHOICES, ZmeiLangParser.KW_THEME, ZmeiLangParser.KW_INSTALL, ZmeiLangParser.KW_HEADER, ZmeiLangParser.KW_SERVICES, ZmeiLangParser.KW_SELENIUM_PYTEST, ZmeiLangParser.KW_CHILD, ZmeiLangParser.KW_FILTER_OUT, ZmeiLangParser.KW_FILTER_IN, ZmeiLangParser.KW_PAGE, ZmeiLangParser.KW_LINK_SUFFIX, ZmeiLangParser.KW_URL_PREFIX, ZmeiLangParser.KW_CAN_EDIT, ZmeiLangParser.KW_OBJECT_EXPR, ZmeiLangParser.KW_BLOCK, ZmeiLangParser.KW_ITEM_NAME, ZmeiLangParser.KW_PK_PARAM, ZmeiLangParser.KW_LIST_FIELDS, ZmeiLangParser.KW_DELETE, ZmeiLangParser.KW_EDIT, ZmeiLangParser.KW_CREATE, ZmeiLangParser.KW_DETAIL, ZmeiLangParser.KW_SKIP, ZmeiLangParser.KW_FROM, ZmeiLangParser.KW_POLY_LIST, ZmeiLangParser.KW_CSS, ZmeiLangParser.KW_JS, ZmeiLangParser.KW_INLINE_TYPE_TABULAR, ZmeiLangParser.KW_INLINE_TYPE_STACKED, ZmeiLangParser.KW_INLINE_TYPE_POLYMORPHIC, ZmeiLangParser.KW_INLINE, ZmeiLangParser.KW_TYPE, ZmeiLangParser.KW_USER_FIELD, ZmeiLangParser.KW_ANNOTATE, ZmeiLangParser.KW_ON_CREATE, ZmeiLangParser.KW_QUERY, ZmeiLangParser.KW_AUTH, ZmeiLangParser.KW_COUNT, ZmeiLangParser.KW_I18N, ZmeiLangParser.KW_EXTENSION, ZmeiLangParser.KW_TABS, ZmeiLangParser.KW_LIST, ZmeiLangParser.KW_READ_ONLY, ZmeiLangParser.KW_LIST_EDITABLE, ZmeiLangParser.KW_LIST_FILTER, ZmeiLangParser.KW_LIST_SEARCH, ZmeiLangParser.KW_FIELDS, ZmeiLangParser.KW_IMPORT, ZmeiLangParser.KW_AS, ZmeiLangParser.WRITE_MODE, ZmeiLangParser.BOOL, ZmeiLangParser.ID]:
                self.state = 1258
                self.id_or_kw()
                pass
            elif token in [ZmeiLangParser.STRING_DQ]:
                self.state = 1259
                self.match(ZmeiLangParser.STRING_DQ)
                pass
            elif token in [ZmeiLangParser.STRING_SQ]:
                self.state = 1260
                self.match(ZmeiLangParser.STRING_SQ)
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Field_text_choice_keyContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def id_or_kw(self):
            return self.getTypedRuleContext(ZmeiLangParser.Id_or_kwContext,0)


        def COLON(self):
            return self.getToken(ZmeiLangParser.COLON, 0)

        def getRuleIndex(self):
            return ZmeiLangParser.RULE_field_text_choice_key

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterField_text_choice_key" ):
                listener.enterField_text_choice_key(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitField_text_choice_key" ):
                listener.exitField_text_choice_key(self)




    def field_text_choice_key(self):

        localctx = ZmeiLangParser.Field_text_choice_keyContext(self, self._ctx, self.state)
        self.enterRule(localctx, 178, self.RULE_field_text_choice_key)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1263
            self.id_or_kw()
            self.state = 1264
            self.match(ZmeiLangParser.COLON)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Field_intContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def COL_FIELD_TYPE_INT(self):
            return self.getToken(ZmeiLangParser.COL_FIELD_TYPE_INT, 0)

        def BRACE_OPEN(self):
            return self.getToken(ZmeiLangParser.BRACE_OPEN, 0)

        def field_int_choices(self):
            return self.getTypedRuleContext(ZmeiLangParser.Field_int_choicesContext,0)


        def BRACE_CLOSE(self):
            return self.getToken(ZmeiLangParser.BRACE_CLOSE, 0)

        def getRuleIndex(self):
            return ZmeiLangParser.RULE_field_int

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterField_int" ):
                listener.enterField_int(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitField_int" ):
                listener.exitField_int(self)




    def field_int(self):

        localctx = ZmeiLangParser.Field_intContext(self, self._ctx, self.state)
        self.enterRule(localctx, 180, self.RULE_field_int)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1266
            self.match(ZmeiLangParser.COL_FIELD_TYPE_INT)
            self.state = 1271
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==ZmeiLangParser.BRACE_OPEN:
                self.state = 1267
                self.match(ZmeiLangParser.BRACE_OPEN)
                self.state = 1268
                self.field_int_choices()
                self.state = 1269
                self.match(ZmeiLangParser.BRACE_CLOSE)


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Field_int_choicesContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def COL_FIELD_CHOICES(self):
            return self.getToken(ZmeiLangParser.COL_FIELD_CHOICES, 0)

        def EQUALS(self):
            return self.getToken(ZmeiLangParser.EQUALS, 0)

        def field_int_choice(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(ZmeiLangParser.Field_int_choiceContext)
            else:
                return self.getTypedRuleContext(ZmeiLangParser.Field_int_choiceContext,i)


        def COMA(self, i:int=None):
            if i is None:
                return self.getTokens(ZmeiLangParser.COMA)
            else:
                return self.getToken(ZmeiLangParser.COMA, i)

        def getRuleIndex(self):
            return ZmeiLangParser.RULE_field_int_choices

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterField_int_choices" ):
                listener.enterField_int_choices(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitField_int_choices" ):
                listener.exitField_int_choices(self)




    def field_int_choices(self):

        localctx = ZmeiLangParser.Field_int_choicesContext(self, self._ctx, self.state)
        self.enterRule(localctx, 182, self.RULE_field_int_choices)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1273
            self.match(ZmeiLangParser.COL_FIELD_CHOICES)
            self.state = 1274
            self.match(ZmeiLangParser.EQUALS)
            self.state = 1275
            self.field_int_choice()
            self.state = 1280
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==ZmeiLangParser.COMA:
                self.state = 1276
                self.match(ZmeiLangParser.COMA)
                self.state = 1277
                self.field_int_choice()
                self.state = 1282
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Field_int_choiceContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def field_int_choice_val(self):
            return self.getTypedRuleContext(ZmeiLangParser.Field_int_choice_valContext,0)


        def field_int_choice_key(self):
            return self.getTypedRuleContext(ZmeiLangParser.Field_int_choice_keyContext,0)


        def getRuleIndex(self):
            return ZmeiLangParser.RULE_field_int_choice

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterField_int_choice" ):
                listener.enterField_int_choice(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitField_int_choice" ):
                listener.exitField_int_choice(self)




    def field_int_choice(self):

        localctx = ZmeiLangParser.Field_int_choiceContext(self, self._ctx, self.state)
        self.enterRule(localctx, 184, self.RULE_field_int_choice)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1284
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==ZmeiLangParser.DIGIT:
                self.state = 1283
                self.field_int_choice_key()


            self.state = 1286
            self.field_int_choice_val()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Field_int_choice_valContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def id_or_kw(self):
            return self.getTypedRuleContext(ZmeiLangParser.Id_or_kwContext,0)


        def STRING_DQ(self):
            return self.getToken(ZmeiLangParser.STRING_DQ, 0)

        def STRING_SQ(self):
            return self.getToken(ZmeiLangParser.STRING_SQ, 0)

        def getRuleIndex(self):
            return ZmeiLangParser.RULE_field_int_choice_val

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterField_int_choice_val" ):
                listener.enterField_int_choice_val(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitField_int_choice_val" ):
                listener.exitField_int_choice_val(self)




    def field_int_choice_val(self):

        localctx = ZmeiLangParser.Field_int_choice_valContext(self, self._ctx, self.state)
        self.enterRule(localctx, 186, self.RULE_field_int_choice_val)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1291
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [ZmeiLangParser.KW_AUTH_TYPE_BASIC, ZmeiLangParser.KW_AUTH_TYPE_SESSION, ZmeiLangParser.KW_AUTH_TYPE_TOKEN, ZmeiLangParser.COL_FIELD_TYPE_LONGTEXT, ZmeiLangParser.COL_FIELD_TYPE_HTML, ZmeiLangParser.COL_FIELD_TYPE_HTML_MEDIA, ZmeiLangParser.COL_FIELD_TYPE_FLOAT, ZmeiLangParser.COL_FIELD_TYPE_DECIMAL, ZmeiLangParser.COL_FIELD_TYPE_DATE, ZmeiLangParser.COL_FIELD_TYPE_DATETIME, ZmeiLangParser.COL_FIELD_TYPE_CREATE_TIME, ZmeiLangParser.COL_FIELD_TYPE_UPDATE_TIME, ZmeiLangParser.COL_FIELD_TYPE_IMAGE, ZmeiLangParser.COL_FIELD_TYPE_FILE, ZmeiLangParser.COL_FIELD_TYPE_FILER_IMAGE, ZmeiLangParser.COL_FIELD_TYPE_FILER_FILE, ZmeiLangParser.COL_FIELD_TYPE_FILER_FOLDER, ZmeiLangParser.COL_FIELD_TYPE_FILER_IMAGE_FOLDER, ZmeiLangParser.COL_FIELD_TYPE_TEXT, ZmeiLangParser.COL_FIELD_TYPE_INT, ZmeiLangParser.COL_FIELD_TYPE_SLUG, ZmeiLangParser.COL_FIELD_TYPE_BOOL, ZmeiLangParser.COL_FIELD_TYPE_ONE, ZmeiLangParser.COL_FIELD_TYPE_ONE2ONE, ZmeiLangParser.COL_FIELD_TYPE_MANY, ZmeiLangParser.COL_FIELD_CHOICES, ZmeiLangParser.KW_THEME, ZmeiLangParser.KW_INSTALL, ZmeiLangParser.KW_HEADER, ZmeiLangParser.KW_SERVICES, ZmeiLangParser.KW_SELENIUM_PYTEST, ZmeiLangParser.KW_CHILD, ZmeiLangParser.KW_FILTER_OUT, ZmeiLangParser.KW_FILTER_IN, ZmeiLangParser.KW_PAGE, ZmeiLangParser.KW_LINK_SUFFIX, ZmeiLangParser.KW_URL_PREFIX, ZmeiLangParser.KW_CAN_EDIT, ZmeiLangParser.KW_OBJECT_EXPR, ZmeiLangParser.KW_BLOCK, ZmeiLangParser.KW_ITEM_NAME, ZmeiLangParser.KW_PK_PARAM, ZmeiLangParser.KW_LIST_FIELDS, ZmeiLangParser.KW_DELETE, ZmeiLangParser.KW_EDIT, ZmeiLangParser.KW_CREATE, ZmeiLangParser.KW_DETAIL, ZmeiLangParser.KW_SKIP, ZmeiLangParser.KW_FROM, ZmeiLangParser.KW_POLY_LIST, ZmeiLangParser.KW_CSS, ZmeiLangParser.KW_JS, ZmeiLangParser.KW_INLINE_TYPE_TABULAR, ZmeiLangParser.KW_INLINE_TYPE_STACKED, ZmeiLangParser.KW_INLINE_TYPE_POLYMORPHIC, ZmeiLangParser.KW_INLINE, ZmeiLangParser.KW_TYPE, ZmeiLangParser.KW_USER_FIELD, ZmeiLangParser.KW_ANNOTATE, ZmeiLangParser.KW_ON_CREATE, ZmeiLangParser.KW_QUERY, ZmeiLangParser.KW_AUTH, ZmeiLangParser.KW_COUNT, ZmeiLangParser.KW_I18N, ZmeiLangParser.KW_EXTENSION, ZmeiLangParser.KW_TABS, ZmeiLangParser.KW_LIST, ZmeiLangParser.KW_READ_ONLY, ZmeiLangParser.KW_LIST_EDITABLE, ZmeiLangParser.KW_LIST_FILTER, ZmeiLangParser.KW_LIST_SEARCH, ZmeiLangParser.KW_FIELDS, ZmeiLangParser.KW_IMPORT, ZmeiLangParser.KW_AS, ZmeiLangParser.WRITE_MODE, ZmeiLangParser.BOOL, ZmeiLangParser.ID]:
                self.state = 1288
                self.id_or_kw()
                pass
            elif token in [ZmeiLangParser.STRING_DQ]:
                self.state = 1289
                self.match(ZmeiLangParser.STRING_DQ)
                pass
            elif token in [ZmeiLangParser.STRING_SQ]:
                self.state = 1290
                self.match(ZmeiLangParser.STRING_SQ)
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Field_int_choice_keyContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def DIGIT(self):
            return self.getToken(ZmeiLangParser.DIGIT, 0)

        def COLON(self):
            return self.getToken(ZmeiLangParser.COLON, 0)

        def getRuleIndex(self):
            return ZmeiLangParser.RULE_field_int_choice_key

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterField_int_choice_key" ):
                listener.enterField_int_choice_key(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitField_int_choice_key" ):
                listener.exitField_int_choice_key(self)




    def field_int_choice_key(self):

        localctx = ZmeiLangParser.Field_int_choice_keyContext(self, self._ctx, self.state)
        self.enterRule(localctx, 188, self.RULE_field_int_choice_key)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1293
            self.match(ZmeiLangParser.DIGIT)
            self.state = 1294
            self.match(ZmeiLangParser.COLON)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Field_slugContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def COL_FIELD_TYPE_SLUG(self):
            return self.getToken(ZmeiLangParser.COL_FIELD_TYPE_SLUG, 0)

        def BRACE_OPEN(self):
            return self.getToken(ZmeiLangParser.BRACE_OPEN, 0)

        def field_slug_ref_field(self):
            return self.getTypedRuleContext(ZmeiLangParser.Field_slug_ref_fieldContext,0)


        def BRACE_CLOSE(self):
            return self.getToken(ZmeiLangParser.BRACE_CLOSE, 0)

        def getRuleIndex(self):
            return ZmeiLangParser.RULE_field_slug

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterField_slug" ):
                listener.enterField_slug(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitField_slug" ):
                listener.exitField_slug(self)




    def field_slug(self):

        localctx = ZmeiLangParser.Field_slugContext(self, self._ctx, self.state)
        self.enterRule(localctx, 190, self.RULE_field_slug)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1296
            self.match(ZmeiLangParser.COL_FIELD_TYPE_SLUG)
            self.state = 1297
            self.match(ZmeiLangParser.BRACE_OPEN)
            self.state = 1298
            self.field_slug_ref_field()
            self.state = 1299
            self.match(ZmeiLangParser.BRACE_CLOSE)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Field_slug_ref_fieldContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def field_slug_ref_field_id(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(ZmeiLangParser.Field_slug_ref_field_idContext)
            else:
                return self.getTypedRuleContext(ZmeiLangParser.Field_slug_ref_field_idContext,i)


        def COMA(self, i:int=None):
            if i is None:
                return self.getTokens(ZmeiLangParser.COMA)
            else:
                return self.getToken(ZmeiLangParser.COMA, i)

        def getRuleIndex(self):
            return ZmeiLangParser.RULE_field_slug_ref_field

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterField_slug_ref_field" ):
                listener.enterField_slug_ref_field(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitField_slug_ref_field" ):
                listener.exitField_slug_ref_field(self)




    def field_slug_ref_field(self):

        localctx = ZmeiLangParser.Field_slug_ref_fieldContext(self, self._ctx, self.state)
        self.enterRule(localctx, 192, self.RULE_field_slug_ref_field)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1301
            self.field_slug_ref_field_id()
            self.state = 1306
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==ZmeiLangParser.COMA:
                self.state = 1302
                self.match(ZmeiLangParser.COMA)
                self.state = 1303
                self.field_slug_ref_field_id()
                self.state = 1308
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Field_slug_ref_field_idContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def id_or_kw(self):
            return self.getTypedRuleContext(ZmeiLangParser.Id_or_kwContext,0)


        def getRuleIndex(self):
            return ZmeiLangParser.RULE_field_slug_ref_field_id

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterField_slug_ref_field_id" ):
                listener.enterField_slug_ref_field_id(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitField_slug_ref_field_id" ):
                listener.exitField_slug_ref_field_id(self)




    def field_slug_ref_field_id(self):

        localctx = ZmeiLangParser.Field_slug_ref_field_idContext(self, self._ctx, self.state)
        self.enterRule(localctx, 194, self.RULE_field_slug_ref_field_id)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1309
            self.id_or_kw()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Field_boolContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def COL_FIELD_TYPE_BOOL(self):
            return self.getToken(ZmeiLangParser.COL_FIELD_TYPE_BOOL, 0)

        def BRACE_OPEN(self):
            return self.getToken(ZmeiLangParser.BRACE_OPEN, 0)

        def field_bool_default(self):
            return self.getTypedRuleContext(ZmeiLangParser.Field_bool_defaultContext,0)


        def BRACE_CLOSE(self):
            return self.getToken(ZmeiLangParser.BRACE_CLOSE, 0)

        def getRuleIndex(self):
            return ZmeiLangParser.RULE_field_bool

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterField_bool" ):
                listener.enterField_bool(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitField_bool" ):
                listener.exitField_bool(self)




    def field_bool(self):

        localctx = ZmeiLangParser.Field_boolContext(self, self._ctx, self.state)
        self.enterRule(localctx, 196, self.RULE_field_bool)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1311
            self.match(ZmeiLangParser.COL_FIELD_TYPE_BOOL)
            self.state = 1316
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==ZmeiLangParser.BRACE_OPEN:
                self.state = 1312
                self.match(ZmeiLangParser.BRACE_OPEN)
                self.state = 1313
                self.field_bool_default()
                self.state = 1314
                self.match(ZmeiLangParser.BRACE_CLOSE)


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Field_bool_defaultContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def BOOL(self):
            return self.getToken(ZmeiLangParser.BOOL, 0)

        def getRuleIndex(self):
            return ZmeiLangParser.RULE_field_bool_default

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterField_bool_default" ):
                listener.enterField_bool_default(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitField_bool_default" ):
                listener.exitField_bool_default(self)




    def field_bool_default(self):

        localctx = ZmeiLangParser.Field_bool_defaultContext(self, self._ctx, self.state)
        self.enterRule(localctx, 198, self.RULE_field_bool_default)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1318
            self.match(ZmeiLangParser.BOOL)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Field_imageContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def filer_image_type(self):
            return self.getTypedRuleContext(ZmeiLangParser.Filer_image_typeContext,0)


        def BRACE_OPEN(self):
            return self.getToken(ZmeiLangParser.BRACE_OPEN, 0)

        def field_image_sizes(self):
            return self.getTypedRuleContext(ZmeiLangParser.Field_image_sizesContext,0)


        def BRACE_CLOSE(self):
            return self.getToken(ZmeiLangParser.BRACE_CLOSE, 0)

        def getRuleIndex(self):
            return ZmeiLangParser.RULE_field_image

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterField_image" ):
                listener.enterField_image(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitField_image" ):
                listener.exitField_image(self)




    def field_image(self):

        localctx = ZmeiLangParser.Field_imageContext(self, self._ctx, self.state)
        self.enterRule(localctx, 200, self.RULE_field_image)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1320
            self.filer_image_type()
            self.state = 1325
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==ZmeiLangParser.BRACE_OPEN:
                self.state = 1321
                self.match(ZmeiLangParser.BRACE_OPEN)
                self.state = 1322
                self.field_image_sizes()
                self.state = 1323
                self.match(ZmeiLangParser.BRACE_CLOSE)


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Filer_image_typeContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def COL_FIELD_TYPE_IMAGE(self):
            return self.getToken(ZmeiLangParser.COL_FIELD_TYPE_IMAGE, 0)

        def COL_FIELD_TYPE_FILER_IMAGE(self):
            return self.getToken(ZmeiLangParser.COL_FIELD_TYPE_FILER_IMAGE, 0)

        def COL_FIELD_TYPE_FILER_IMAGE_FOLDER(self):
            return self.getToken(ZmeiLangParser.COL_FIELD_TYPE_FILER_IMAGE_FOLDER, 0)

        def getRuleIndex(self):
            return ZmeiLangParser.RULE_filer_image_type

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterFiler_image_type" ):
                listener.enterFiler_image_type(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitFiler_image_type" ):
                listener.exitFiler_image_type(self)




    def filer_image_type(self):

        localctx = ZmeiLangParser.Filer_image_typeContext(self, self._ctx, self.state)
        self.enterRule(localctx, 202, self.RULE_filer_image_type)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1327
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << ZmeiLangParser.COL_FIELD_TYPE_IMAGE) | (1 << ZmeiLangParser.COL_FIELD_TYPE_FILER_IMAGE) | (1 << ZmeiLangParser.COL_FIELD_TYPE_FILER_IMAGE_FOLDER))) != 0)):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Field_image_sizesContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def field_image_size(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(ZmeiLangParser.Field_image_sizeContext)
            else:
                return self.getTypedRuleContext(ZmeiLangParser.Field_image_sizeContext,i)


        def COMA(self, i:int=None):
            if i is None:
                return self.getTokens(ZmeiLangParser.COMA)
            else:
                return self.getToken(ZmeiLangParser.COMA, i)

        def getRuleIndex(self):
            return ZmeiLangParser.RULE_field_image_sizes

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterField_image_sizes" ):
                listener.enterField_image_sizes(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitField_image_sizes" ):
                listener.exitField_image_sizes(self)




    def field_image_sizes(self):

        localctx = ZmeiLangParser.Field_image_sizesContext(self, self._ctx, self.state)
        self.enterRule(localctx, 204, self.RULE_field_image_sizes)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1329
            self.field_image_size()
            self.state = 1334
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==ZmeiLangParser.COMA:
                self.state = 1330
                self.match(ZmeiLangParser.COMA)
                self.state = 1331
                self.field_image_size()
                self.state = 1336
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Field_image_sizeContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def field_image_size_name(self):
            return self.getTypedRuleContext(ZmeiLangParser.Field_image_size_nameContext,0)


        def field_image_size_dimensions(self):
            return self.getTypedRuleContext(ZmeiLangParser.Field_image_size_dimensionsContext,0)


        def field_image_filters(self):
            return self.getTypedRuleContext(ZmeiLangParser.Field_image_filtersContext,0)


        def getRuleIndex(self):
            return ZmeiLangParser.RULE_field_image_size

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterField_image_size" ):
                listener.enterField_image_size(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitField_image_size" ):
                listener.exitField_image_size(self)




    def field_image_size(self):

        localctx = ZmeiLangParser.Field_image_sizeContext(self, self._ctx, self.state)
        self.enterRule(localctx, 206, self.RULE_field_image_size)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1337
            self.field_image_size_name()
            self.state = 1338
            self.field_image_size_dimensions()
            self.state = 1339
            self.field_image_filters()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Field_image_size_dimensionsContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def SIZE2D(self):
            return self.getToken(ZmeiLangParser.SIZE2D, 0)

        def getRuleIndex(self):
            return ZmeiLangParser.RULE_field_image_size_dimensions

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterField_image_size_dimensions" ):
                listener.enterField_image_size_dimensions(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitField_image_size_dimensions" ):
                listener.exitField_image_size_dimensions(self)




    def field_image_size_dimensions(self):

        localctx = ZmeiLangParser.Field_image_size_dimensionsContext(self, self._ctx, self.state)
        self.enterRule(localctx, 208, self.RULE_field_image_size_dimensions)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1341
            self.match(ZmeiLangParser.SIZE2D)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Field_image_size_nameContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def id_or_kw(self):
            return self.getTypedRuleContext(ZmeiLangParser.Id_or_kwContext,0)


        def EQUALS(self):
            return self.getToken(ZmeiLangParser.EQUALS, 0)

        def getRuleIndex(self):
            return ZmeiLangParser.RULE_field_image_size_name

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterField_image_size_name" ):
                listener.enterField_image_size_name(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitField_image_size_name" ):
                listener.exitField_image_size_name(self)




    def field_image_size_name(self):

        localctx = ZmeiLangParser.Field_image_size_nameContext(self, self._ctx, self.state)
        self.enterRule(localctx, 210, self.RULE_field_image_size_name)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1343
            self.id_or_kw()
            self.state = 1344
            self.match(ZmeiLangParser.EQUALS)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Field_image_filtersContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def field_image_filter(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(ZmeiLangParser.Field_image_filterContext)
            else:
                return self.getTypedRuleContext(ZmeiLangParser.Field_image_filterContext,i)


        def getRuleIndex(self):
            return ZmeiLangParser.RULE_field_image_filters

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterField_image_filters" ):
                listener.enterField_image_filters(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitField_image_filters" ):
                listener.exitField_image_filters(self)




    def field_image_filters(self):

        localctx = ZmeiLangParser.Field_image_filtersContext(self, self._ctx, self.state)
        self.enterRule(localctx, 212, self.RULE_field_image_filters)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1349
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==ZmeiLangParser.PIPE:
                self.state = 1346
                self.field_image_filter()
                self.state = 1351
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Field_image_filterContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def PIPE(self):
            return self.getToken(ZmeiLangParser.PIPE, 0)

        def id_or_kw(self):
            return self.getTypedRuleContext(ZmeiLangParser.Id_or_kwContext,0)


        def getRuleIndex(self):
            return ZmeiLangParser.RULE_field_image_filter

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterField_image_filter" ):
                listener.enterField_image_filter(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitField_image_filter" ):
                listener.exitField_image_filter(self)




    def field_image_filter(self):

        localctx = ZmeiLangParser.Field_image_filterContext(self, self._ctx, self.state)
        self.enterRule(localctx, 214, self.RULE_field_image_filter)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1352
            self.match(ZmeiLangParser.PIPE)
            self.state = 1353
            self.id_or_kw()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Field_relationContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def field_relation_type(self):
            return self.getTypedRuleContext(ZmeiLangParser.Field_relation_typeContext,0)


        def BRACE_OPEN(self):
            return self.getToken(ZmeiLangParser.BRACE_OPEN, 0)

        def BRACE_CLOSE(self):
            return self.getToken(ZmeiLangParser.BRACE_CLOSE, 0)

        def field_relation_target_ref(self):
            return self.getTypedRuleContext(ZmeiLangParser.Field_relation_target_refContext,0)


        def field_relation_target_class(self):
            return self.getTypedRuleContext(ZmeiLangParser.Field_relation_target_classContext,0)


        def field_relation_cascade_marker(self):
            return self.getTypedRuleContext(ZmeiLangParser.Field_relation_cascade_markerContext,0)


        def field_relation_related_name(self):
            return self.getTypedRuleContext(ZmeiLangParser.Field_relation_related_nameContext,0)


        def getRuleIndex(self):
            return ZmeiLangParser.RULE_field_relation

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterField_relation" ):
                listener.enterField_relation(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitField_relation" ):
                listener.exitField_relation(self)




    def field_relation(self):

        localctx = ZmeiLangParser.Field_relationContext(self, self._ctx, self.state)
        self.enterRule(localctx, 216, self.RULE_field_relation)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1355
            self.field_relation_type()
            self.state = 1356
            self.match(ZmeiLangParser.BRACE_OPEN)
            self.state = 1358
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==ZmeiLangParser.EXCLAM or _la==ZmeiLangParser.APPROX:
                self.state = 1357
                self.field_relation_cascade_marker()


            self.state = 1362
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [ZmeiLangParser.HASH]:
                self.state = 1360
                self.field_relation_target_ref()
                pass
            elif token in [ZmeiLangParser.KW_AUTH_TYPE_BASIC, ZmeiLangParser.KW_AUTH_TYPE_SESSION, ZmeiLangParser.KW_AUTH_TYPE_TOKEN, ZmeiLangParser.COL_FIELD_TYPE_LONGTEXT, ZmeiLangParser.COL_FIELD_TYPE_HTML, ZmeiLangParser.COL_FIELD_TYPE_HTML_MEDIA, ZmeiLangParser.COL_FIELD_TYPE_FLOAT, ZmeiLangParser.COL_FIELD_TYPE_DECIMAL, ZmeiLangParser.COL_FIELD_TYPE_DATE, ZmeiLangParser.COL_FIELD_TYPE_DATETIME, ZmeiLangParser.COL_FIELD_TYPE_CREATE_TIME, ZmeiLangParser.COL_FIELD_TYPE_UPDATE_TIME, ZmeiLangParser.COL_FIELD_TYPE_IMAGE, ZmeiLangParser.COL_FIELD_TYPE_FILE, ZmeiLangParser.COL_FIELD_TYPE_FILER_IMAGE, ZmeiLangParser.COL_FIELD_TYPE_FILER_FILE, ZmeiLangParser.COL_FIELD_TYPE_FILER_FOLDER, ZmeiLangParser.COL_FIELD_TYPE_FILER_IMAGE_FOLDER, ZmeiLangParser.COL_FIELD_TYPE_TEXT, ZmeiLangParser.COL_FIELD_TYPE_INT, ZmeiLangParser.COL_FIELD_TYPE_SLUG, ZmeiLangParser.COL_FIELD_TYPE_BOOL, ZmeiLangParser.COL_FIELD_TYPE_ONE, ZmeiLangParser.COL_FIELD_TYPE_ONE2ONE, ZmeiLangParser.COL_FIELD_TYPE_MANY, ZmeiLangParser.COL_FIELD_CHOICES, ZmeiLangParser.KW_THEME, ZmeiLangParser.KW_INSTALL, ZmeiLangParser.KW_HEADER, ZmeiLangParser.KW_SERVICES, ZmeiLangParser.KW_SELENIUM_PYTEST, ZmeiLangParser.KW_CHILD, ZmeiLangParser.KW_FILTER_OUT, ZmeiLangParser.KW_FILTER_IN, ZmeiLangParser.KW_PAGE, ZmeiLangParser.KW_LINK_SUFFIX, ZmeiLangParser.KW_URL_PREFIX, ZmeiLangParser.KW_CAN_EDIT, ZmeiLangParser.KW_OBJECT_EXPR, ZmeiLangParser.KW_BLOCK, ZmeiLangParser.KW_ITEM_NAME, ZmeiLangParser.KW_PK_PARAM, ZmeiLangParser.KW_LIST_FIELDS, ZmeiLangParser.KW_DELETE, ZmeiLangParser.KW_EDIT, ZmeiLangParser.KW_CREATE, ZmeiLangParser.KW_DETAIL, ZmeiLangParser.KW_SKIP, ZmeiLangParser.KW_FROM, ZmeiLangParser.KW_POLY_LIST, ZmeiLangParser.KW_CSS, ZmeiLangParser.KW_JS, ZmeiLangParser.KW_INLINE_TYPE_TABULAR, ZmeiLangParser.KW_INLINE_TYPE_STACKED, ZmeiLangParser.KW_INLINE_TYPE_POLYMORPHIC, ZmeiLangParser.KW_INLINE, ZmeiLangParser.KW_TYPE, ZmeiLangParser.KW_USER_FIELD, ZmeiLangParser.KW_ANNOTATE, ZmeiLangParser.KW_ON_CREATE, ZmeiLangParser.KW_QUERY, ZmeiLangParser.KW_AUTH, ZmeiLangParser.KW_COUNT, ZmeiLangParser.KW_I18N, ZmeiLangParser.KW_EXTENSION, ZmeiLangParser.KW_TABS, ZmeiLangParser.KW_LIST, ZmeiLangParser.KW_READ_ONLY, ZmeiLangParser.KW_LIST_EDITABLE, ZmeiLangParser.KW_LIST_FILTER, ZmeiLangParser.KW_LIST_SEARCH, ZmeiLangParser.KW_FIELDS, ZmeiLangParser.KW_IMPORT, ZmeiLangParser.KW_AS, ZmeiLangParser.WRITE_MODE, ZmeiLangParser.BOOL, ZmeiLangParser.ID]:
                self.state = 1361
                self.field_relation_target_class()
                pass
            else:
                raise NoViableAltException(self)

            self.state = 1365
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==ZmeiLangParser.DASH:
                self.state = 1364
                self.field_relation_related_name()


            self.state = 1367
            self.match(ZmeiLangParser.BRACE_CLOSE)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Field_relation_typeContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def COL_FIELD_TYPE_ONE(self):
            return self.getToken(ZmeiLangParser.COL_FIELD_TYPE_ONE, 0)

        def COL_FIELD_TYPE_ONE2ONE(self):
            return self.getToken(ZmeiLangParser.COL_FIELD_TYPE_ONE2ONE, 0)

        def COL_FIELD_TYPE_MANY(self):
            return self.getToken(ZmeiLangParser.COL_FIELD_TYPE_MANY, 0)

        def getRuleIndex(self):
            return ZmeiLangParser.RULE_field_relation_type

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterField_relation_type" ):
                listener.enterField_relation_type(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitField_relation_type" ):
                listener.exitField_relation_type(self)




    def field_relation_type(self):

        localctx = ZmeiLangParser.Field_relation_typeContext(self, self._ctx, self.state)
        self.enterRule(localctx, 218, self.RULE_field_relation_type)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1369
            _la = self._input.LA(1)
            if not(((((_la - 64)) & ~0x3f) == 0 and ((1 << (_la - 64)) & ((1 << (ZmeiLangParser.COL_FIELD_TYPE_ONE - 64)) | (1 << (ZmeiLangParser.COL_FIELD_TYPE_ONE2ONE - 64)) | (1 << (ZmeiLangParser.COL_FIELD_TYPE_MANY - 64)))) != 0)):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Field_relation_cascade_markerContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def APPROX(self):
            return self.getToken(ZmeiLangParser.APPROX, 0)

        def EXCLAM(self):
            return self.getToken(ZmeiLangParser.EXCLAM, 0)

        def getRuleIndex(self):
            return ZmeiLangParser.RULE_field_relation_cascade_marker

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterField_relation_cascade_marker" ):
                listener.enterField_relation_cascade_marker(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitField_relation_cascade_marker" ):
                listener.exitField_relation_cascade_marker(self)




    def field_relation_cascade_marker(self):

        localctx = ZmeiLangParser.Field_relation_cascade_markerContext(self, self._ctx, self.state)
        self.enterRule(localctx, 220, self.RULE_field_relation_cascade_marker)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1371
            _la = self._input.LA(1)
            if not(_la==ZmeiLangParser.EXCLAM or _la==ZmeiLangParser.APPROX):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Field_relation_target_refContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def model_ref(self):
            return self.getTypedRuleContext(ZmeiLangParser.Model_refContext,0)


        def getRuleIndex(self):
            return ZmeiLangParser.RULE_field_relation_target_ref

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterField_relation_target_ref" ):
                listener.enterField_relation_target_ref(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitField_relation_target_ref" ):
                listener.exitField_relation_target_ref(self)




    def field_relation_target_ref(self):

        localctx = ZmeiLangParser.Field_relation_target_refContext(self, self._ctx, self.state)
        self.enterRule(localctx, 222, self.RULE_field_relation_target_ref)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1373
            self.model_ref()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Field_relation_target_classContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def classname(self):
            return self.getTypedRuleContext(ZmeiLangParser.ClassnameContext,0)


        def getRuleIndex(self):
            return ZmeiLangParser.RULE_field_relation_target_class

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterField_relation_target_class" ):
                listener.enterField_relation_target_class(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitField_relation_target_class" ):
                listener.exitField_relation_target_class(self)




    def field_relation_target_class(self):

        localctx = ZmeiLangParser.Field_relation_target_classContext(self, self._ctx, self.state)
        self.enterRule(localctx, 224, self.RULE_field_relation_target_class)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1375
            self.classname()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Field_relation_related_nameContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def DASH(self):
            return self.getToken(ZmeiLangParser.DASH, 0)

        def GT(self):
            return self.getToken(ZmeiLangParser.GT, 0)

        def id_or_kw(self):
            return self.getTypedRuleContext(ZmeiLangParser.Id_or_kwContext,0)


        def getRuleIndex(self):
            return ZmeiLangParser.RULE_field_relation_related_name

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterField_relation_related_name" ):
                listener.enterField_relation_related_name(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitField_relation_related_name" ):
                listener.exitField_relation_related_name(self)




    def field_relation_related_name(self):

        localctx = ZmeiLangParser.Field_relation_related_nameContext(self, self._ctx, self.state)
        self.enterRule(localctx, 226, self.RULE_field_relation_related_name)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1377
            self.match(ZmeiLangParser.DASH)
            self.state = 1378
            self.match(ZmeiLangParser.GT)
            self.state = 1379
            self.id_or_kw()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Model_annotationContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def an_admin(self):
            return self.getTypedRuleContext(ZmeiLangParser.An_adminContext,0)


        def an_api(self):
            return self.getTypedRuleContext(ZmeiLangParser.An_apiContext,0)


        def an_rest(self):
            return self.getTypedRuleContext(ZmeiLangParser.An_restContext,0)


        def an_order(self):
            return self.getTypedRuleContext(ZmeiLangParser.An_orderContext,0)


        def an_clean(self):
            return self.getTypedRuleContext(ZmeiLangParser.An_cleanContext,0)


        def an_pre_delete(self):
            return self.getTypedRuleContext(ZmeiLangParser.An_pre_deleteContext,0)


        def an_tree(self):
            return self.getTypedRuleContext(ZmeiLangParser.An_treeContext,0)


        def an_mixin(self):
            return self.getTypedRuleContext(ZmeiLangParser.An_mixinContext,0)


        def an_date_tree(self):
            return self.getTypedRuleContext(ZmeiLangParser.An_date_treeContext,0)


        def an_m2m_changed(self):
            return self.getTypedRuleContext(ZmeiLangParser.An_m2m_changedContext,0)


        def an_post_save(self):
            return self.getTypedRuleContext(ZmeiLangParser.An_post_saveContext,0)


        def an_pre_save(self):
            return self.getTypedRuleContext(ZmeiLangParser.An_pre_saveContext,0)


        def an_post_delete(self):
            return self.getTypedRuleContext(ZmeiLangParser.An_post_deleteContext,0)


        def an_sortable(self):
            return self.getTypedRuleContext(ZmeiLangParser.An_sortableContext,0)


        def NL(self):
            return self.getToken(ZmeiLangParser.NL, 0)

        def getRuleIndex(self):
            return ZmeiLangParser.RULE_model_annotation

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterModel_annotation" ):
                listener.enterModel_annotation(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitModel_annotation" ):
                listener.exitModel_annotation(self)




    def model_annotation(self):

        localctx = ZmeiLangParser.Model_annotationContext(self, self._ctx, self.state)
        self.enterRule(localctx, 228, self.RULE_model_annotation)
        try:
            self.state = 1396
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [ZmeiLangParser.AN_ADMIN]:
                self.enterOuterAlt(localctx, 1)
                self.state = 1381
                self.an_admin()
                pass
            elif token in [ZmeiLangParser.AN_API]:
                self.enterOuterAlt(localctx, 2)
                self.state = 1382
                self.an_api()
                pass
            elif token in [ZmeiLangParser.AN_REST]:
                self.enterOuterAlt(localctx, 3)
                self.state = 1383
                self.an_rest()
                pass
            elif token in [ZmeiLangParser.AN_ORDER]:
                self.enterOuterAlt(localctx, 4)
                self.state = 1384
                self.an_order()
                pass
            elif token in [ZmeiLangParser.AN_CLEAN]:
                self.enterOuterAlt(localctx, 5)
                self.state = 1385
                self.an_clean()
                pass
            elif token in [ZmeiLangParser.AN_PRE_DELETE]:
                self.enterOuterAlt(localctx, 6)
                self.state = 1386
                self.an_pre_delete()
                pass
            elif token in [ZmeiLangParser.AN_TREE]:
                self.enterOuterAlt(localctx, 7)
                self.state = 1387
                self.an_tree()
                pass
            elif token in [ZmeiLangParser.AN_MIXIN]:
                self.enterOuterAlt(localctx, 8)
                self.state = 1388
                self.an_mixin()
                pass
            elif token in [ZmeiLangParser.AN_DATE_TREE]:
                self.enterOuterAlt(localctx, 9)
                self.state = 1389
                self.an_date_tree()
                pass
            elif token in [ZmeiLangParser.AN_M2M_CHANGED]:
                self.enterOuterAlt(localctx, 10)
                self.state = 1390
                self.an_m2m_changed()
                pass
            elif token in [ZmeiLangParser.AN_POST_SAVE]:
                self.enterOuterAlt(localctx, 11)
                self.state = 1391
                self.an_post_save()
                pass
            elif token in [ZmeiLangParser.AN_PRE_SAVE]:
                self.enterOuterAlt(localctx, 12)
                self.state = 1392
                self.an_pre_save()
                pass
            elif token in [ZmeiLangParser.AN_POST_DELETE]:
                self.enterOuterAlt(localctx, 13)
                self.state = 1393
                self.an_post_delete()
                pass
            elif token in [ZmeiLangParser.AN_SORTABLE]:
                self.enterOuterAlt(localctx, 14)
                self.state = 1394
                self.an_sortable()
                pass
            elif token in [ZmeiLangParser.NL]:
                self.enterOuterAlt(localctx, 15)
                self.state = 1395
                self.match(ZmeiLangParser.NL)
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class An_adminContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def AN_ADMIN(self):
            return self.getToken(ZmeiLangParser.AN_ADMIN, 0)

        def BRACE_OPEN(self):
            return self.getToken(ZmeiLangParser.BRACE_OPEN, 0)

        def BRACE_CLOSE(self):
            return self.getToken(ZmeiLangParser.BRACE_CLOSE, 0)

        def NL(self, i:int=None):
            if i is None:
                return self.getTokens(ZmeiLangParser.NL)
            else:
                return self.getToken(ZmeiLangParser.NL, i)

        def an_admin_list(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(ZmeiLangParser.An_admin_listContext)
            else:
                return self.getTypedRuleContext(ZmeiLangParser.An_admin_listContext,i)


        def an_admin_read_only(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(ZmeiLangParser.An_admin_read_onlyContext)
            else:
                return self.getTypedRuleContext(ZmeiLangParser.An_admin_read_onlyContext,i)


        def an_admin_list_editable(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(ZmeiLangParser.An_admin_list_editableContext)
            else:
                return self.getTypedRuleContext(ZmeiLangParser.An_admin_list_editableContext,i)


        def an_admin_list_filter(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(ZmeiLangParser.An_admin_list_filterContext)
            else:
                return self.getTypedRuleContext(ZmeiLangParser.An_admin_list_filterContext,i)


        def an_admin_list_search(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(ZmeiLangParser.An_admin_list_searchContext)
            else:
                return self.getTypedRuleContext(ZmeiLangParser.An_admin_list_searchContext,i)


        def an_admin_fields(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(ZmeiLangParser.An_admin_fieldsContext)
            else:
                return self.getTypedRuleContext(ZmeiLangParser.An_admin_fieldsContext,i)


        def an_admin_tabs(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(ZmeiLangParser.An_admin_tabsContext)
            else:
                return self.getTypedRuleContext(ZmeiLangParser.An_admin_tabsContext,i)


        def an_admin_inlines(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(ZmeiLangParser.An_admin_inlinesContext)
            else:
                return self.getTypedRuleContext(ZmeiLangParser.An_admin_inlinesContext,i)


        def an_admin_css(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(ZmeiLangParser.An_admin_cssContext)
            else:
                return self.getTypedRuleContext(ZmeiLangParser.An_admin_cssContext,i)


        def an_admin_js(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(ZmeiLangParser.An_admin_jsContext)
            else:
                return self.getTypedRuleContext(ZmeiLangParser.An_admin_jsContext,i)


        def COMA(self, i:int=None):
            if i is None:
                return self.getTokens(ZmeiLangParser.COMA)
            else:
                return self.getToken(ZmeiLangParser.COMA, i)

        def getRuleIndex(self):
            return ZmeiLangParser.RULE_an_admin

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAn_admin" ):
                listener.enterAn_admin(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAn_admin" ):
                listener.exitAn_admin(self)




    def an_admin(self):

        localctx = ZmeiLangParser.An_adminContext(self, self._ctx, self.state)
        self.enterRule(localctx, 230, self.RULE_an_admin)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1398
            self.match(ZmeiLangParser.AN_ADMIN)
            self.state = 1424
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==ZmeiLangParser.BRACE_OPEN:
                self.state = 1399
                self.match(ZmeiLangParser.BRACE_OPEN)
                self.state = 1414
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,122,self._ctx)
                while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                    if _alt==1:
                        self.state = 1412
                        self._errHandler.sync(self)
                        token = self._input.LA(1)
                        if token in [ZmeiLangParser.KW_LIST]:
                            self.state = 1400
                            self.an_admin_list()
                            pass
                        elif token in [ZmeiLangParser.KW_READ_ONLY]:
                            self.state = 1401
                            self.an_admin_read_only()
                            pass
                        elif token in [ZmeiLangParser.KW_LIST_EDITABLE]:
                            self.state = 1402
                            self.an_admin_list_editable()
                            pass
                        elif token in [ZmeiLangParser.KW_LIST_FILTER]:
                            self.state = 1403
                            self.an_admin_list_filter()
                            pass
                        elif token in [ZmeiLangParser.KW_LIST_SEARCH]:
                            self.state = 1404
                            self.an_admin_list_search()
                            pass
                        elif token in [ZmeiLangParser.KW_FIELDS]:
                            self.state = 1405
                            self.an_admin_fields()
                            pass
                        elif token in [ZmeiLangParser.KW_TABS]:
                            self.state = 1406
                            self.an_admin_tabs()
                            pass
                        elif token in [ZmeiLangParser.KW_INLINE]:
                            self.state = 1407
                            self.an_admin_inlines()
                            pass
                        elif token in [ZmeiLangParser.KW_CSS]:
                            self.state = 1408
                            self.an_admin_css()
                            pass
                        elif token in [ZmeiLangParser.KW_JS]:
                            self.state = 1409
                            self.an_admin_js()
                            pass
                        elif token in [ZmeiLangParser.NL]:
                            self.state = 1410
                            self.match(ZmeiLangParser.NL)
                            pass
                        elif token in [ZmeiLangParser.COMA]:
                            self.state = 1411
                            self.match(ZmeiLangParser.COMA)
                            pass
                        else:
                            raise NoViableAltException(self)
                 
                    self.state = 1416
                    self._errHandler.sync(self)
                    _alt = self._interp.adaptivePredict(self._input,122,self._ctx)

                self.state = 1420
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la==ZmeiLangParser.NL:
                    self.state = 1417
                    self.match(ZmeiLangParser.NL)
                    self.state = 1422
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                self.state = 1423
                self.match(ZmeiLangParser.BRACE_CLOSE)


            self.state = 1429
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,125,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 1426
                    self.match(ZmeiLangParser.NL) 
                self.state = 1431
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,125,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class An_admin_jsContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def KW_JS(self):
            return self.getToken(ZmeiLangParser.KW_JS, 0)

        def COLON(self):
            return self.getToken(ZmeiLangParser.COLON, 0)

        def an_admin_js_file_name(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(ZmeiLangParser.An_admin_js_file_nameContext)
            else:
                return self.getTypedRuleContext(ZmeiLangParser.An_admin_js_file_nameContext,i)


        def NL(self, i:int=None):
            if i is None:
                return self.getTokens(ZmeiLangParser.NL)
            else:
                return self.getToken(ZmeiLangParser.NL, i)

        def COMA(self, i:int=None):
            if i is None:
                return self.getTokens(ZmeiLangParser.COMA)
            else:
                return self.getToken(ZmeiLangParser.COMA, i)

        def getRuleIndex(self):
            return ZmeiLangParser.RULE_an_admin_js

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAn_admin_js" ):
                listener.enterAn_admin_js(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAn_admin_js" ):
                listener.exitAn_admin_js(self)




    def an_admin_js(self):

        localctx = ZmeiLangParser.An_admin_jsContext(self, self._ctx, self.state)
        self.enterRule(localctx, 232, self.RULE_an_admin_js)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1432
            self.match(ZmeiLangParser.KW_JS)
            self.state = 1433
            self.match(ZmeiLangParser.COLON)
            self.state = 1437
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==ZmeiLangParser.NL:
                self.state = 1434
                self.match(ZmeiLangParser.NL)
                self.state = 1439
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 1440
            self.an_admin_js_file_name()
            self.state = 1451
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,128,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 1441
                    self.match(ZmeiLangParser.COMA)
                    self.state = 1445
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    while _la==ZmeiLangParser.NL:
                        self.state = 1442
                        self.match(ZmeiLangParser.NL)
                        self.state = 1447
                        self._errHandler.sync(self)
                        _la = self._input.LA(1)

                    self.state = 1448
                    self.an_admin_js_file_name() 
                self.state = 1453
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,128,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class An_admin_cssContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def KW_CSS(self):
            return self.getToken(ZmeiLangParser.KW_CSS, 0)

        def COLON(self):
            return self.getToken(ZmeiLangParser.COLON, 0)

        def an_admin_css_file_name(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(ZmeiLangParser.An_admin_css_file_nameContext)
            else:
                return self.getTypedRuleContext(ZmeiLangParser.An_admin_css_file_nameContext,i)


        def COMA(self, i:int=None):
            if i is None:
                return self.getTokens(ZmeiLangParser.COMA)
            else:
                return self.getToken(ZmeiLangParser.COMA, i)

        def getRuleIndex(self):
            return ZmeiLangParser.RULE_an_admin_css

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAn_admin_css" ):
                listener.enterAn_admin_css(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAn_admin_css" ):
                listener.exitAn_admin_css(self)




    def an_admin_css(self):

        localctx = ZmeiLangParser.An_admin_cssContext(self, self._ctx, self.state)
        self.enterRule(localctx, 234, self.RULE_an_admin_css)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1454
            self.match(ZmeiLangParser.KW_CSS)
            self.state = 1455
            self.match(ZmeiLangParser.COLON)
            self.state = 1456
            self.an_admin_css_file_name()
            self.state = 1461
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,129,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 1457
                    self.match(ZmeiLangParser.COMA)
                    self.state = 1458
                    self.an_admin_css_file_name() 
                self.state = 1463
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,129,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class An_admin_css_file_nameContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def STRING_DQ(self):
            return self.getToken(ZmeiLangParser.STRING_DQ, 0)

        def STRING_SQ(self):
            return self.getToken(ZmeiLangParser.STRING_SQ, 0)

        def getRuleIndex(self):
            return ZmeiLangParser.RULE_an_admin_css_file_name

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAn_admin_css_file_name" ):
                listener.enterAn_admin_css_file_name(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAn_admin_css_file_name" ):
                listener.exitAn_admin_css_file_name(self)




    def an_admin_css_file_name(self):

        localctx = ZmeiLangParser.An_admin_css_file_nameContext(self, self._ctx, self.state)
        self.enterRule(localctx, 236, self.RULE_an_admin_css_file_name)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1464
            _la = self._input.LA(1)
            if not(_la==ZmeiLangParser.STRING_DQ or _la==ZmeiLangParser.STRING_SQ):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class An_admin_js_file_nameContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def STRING_DQ(self):
            return self.getToken(ZmeiLangParser.STRING_DQ, 0)

        def STRING_SQ(self):
            return self.getToken(ZmeiLangParser.STRING_SQ, 0)

        def getRuleIndex(self):
            return ZmeiLangParser.RULE_an_admin_js_file_name

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAn_admin_js_file_name" ):
                listener.enterAn_admin_js_file_name(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAn_admin_js_file_name" ):
                listener.exitAn_admin_js_file_name(self)




    def an_admin_js_file_name(self):

        localctx = ZmeiLangParser.An_admin_js_file_nameContext(self, self._ctx, self.state)
        self.enterRule(localctx, 238, self.RULE_an_admin_js_file_name)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1466
            _la = self._input.LA(1)
            if not(_la==ZmeiLangParser.STRING_DQ or _la==ZmeiLangParser.STRING_SQ):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class An_admin_inlinesContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def KW_INLINE(self):
            return self.getToken(ZmeiLangParser.KW_INLINE, 0)

        def COLON(self):
            return self.getToken(ZmeiLangParser.COLON, 0)

        def an_admin_inline(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(ZmeiLangParser.An_admin_inlineContext)
            else:
                return self.getTypedRuleContext(ZmeiLangParser.An_admin_inlineContext,i)


        def COMA(self, i:int=None):
            if i is None:
                return self.getTokens(ZmeiLangParser.COMA)
            else:
                return self.getToken(ZmeiLangParser.COMA, i)

        def getRuleIndex(self):
            return ZmeiLangParser.RULE_an_admin_inlines

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAn_admin_inlines" ):
                listener.enterAn_admin_inlines(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAn_admin_inlines" ):
                listener.exitAn_admin_inlines(self)




    def an_admin_inlines(self):

        localctx = ZmeiLangParser.An_admin_inlinesContext(self, self._ctx, self.state)
        self.enterRule(localctx, 240, self.RULE_an_admin_inlines)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1468
            self.match(ZmeiLangParser.KW_INLINE)
            self.state = 1469
            self.match(ZmeiLangParser.COLON)
            self.state = 1470
            self.an_admin_inline()
            self.state = 1475
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,130,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 1471
                    self.match(ZmeiLangParser.COMA)
                    self.state = 1472
                    self.an_admin_inline() 
                self.state = 1477
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,130,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class An_admin_inlineContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def inline_name(self):
            return self.getTypedRuleContext(ZmeiLangParser.Inline_nameContext,0)


        def BRACE_OPEN(self):
            return self.getToken(ZmeiLangParser.BRACE_OPEN, 0)

        def BRACE_CLOSE(self):
            return self.getToken(ZmeiLangParser.BRACE_CLOSE, 0)

        def inline_type(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(ZmeiLangParser.Inline_typeContext)
            else:
                return self.getTypedRuleContext(ZmeiLangParser.Inline_typeContext,i)


        def inline_extension(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(ZmeiLangParser.Inline_extensionContext)
            else:
                return self.getTypedRuleContext(ZmeiLangParser.Inline_extensionContext,i)


        def inline_fields(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(ZmeiLangParser.Inline_fieldsContext)
            else:
                return self.getTypedRuleContext(ZmeiLangParser.Inline_fieldsContext,i)


        def NL(self, i:int=None):
            if i is None:
                return self.getTokens(ZmeiLangParser.NL)
            else:
                return self.getToken(ZmeiLangParser.NL, i)

        def COMA(self, i:int=None):
            if i is None:
                return self.getTokens(ZmeiLangParser.COMA)
            else:
                return self.getToken(ZmeiLangParser.COMA, i)

        def getRuleIndex(self):
            return ZmeiLangParser.RULE_an_admin_inline

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAn_admin_inline" ):
                listener.enterAn_admin_inline(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAn_admin_inline" ):
                listener.exitAn_admin_inline(self)




    def an_admin_inline(self):

        localctx = ZmeiLangParser.An_admin_inlineContext(self, self._ctx, self.state)
        self.enterRule(localctx, 242, self.RULE_an_admin_inline)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1478
            self.inline_name()
            self.state = 1491
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==ZmeiLangParser.BRACE_OPEN:
                self.state = 1479
                self.match(ZmeiLangParser.BRACE_OPEN)
                self.state = 1487
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while ((((_la - 98)) & ~0x3f) == 0 and ((1 << (_la - 98)) & ((1 << (ZmeiLangParser.KW_TYPE - 98)) | (1 << (ZmeiLangParser.KW_EXTENSION - 98)) | (1 << (ZmeiLangParser.KW_FIELDS - 98)) | (1 << (ZmeiLangParser.NL - 98)) | (1 << (ZmeiLangParser.COMA - 98)))) != 0):
                    self.state = 1485
                    self._errHandler.sync(self)
                    token = self._input.LA(1)
                    if token in [ZmeiLangParser.KW_TYPE]:
                        self.state = 1480
                        self.inline_type()
                        pass
                    elif token in [ZmeiLangParser.KW_EXTENSION]:
                        self.state = 1481
                        self.inline_extension()
                        pass
                    elif token in [ZmeiLangParser.KW_FIELDS]:
                        self.state = 1482
                        self.inline_fields()
                        pass
                    elif token in [ZmeiLangParser.NL]:
                        self.state = 1483
                        self.match(ZmeiLangParser.NL)
                        pass
                    elif token in [ZmeiLangParser.COMA]:
                        self.state = 1484
                        self.match(ZmeiLangParser.COMA)
                        pass
                    else:
                        raise NoViableAltException(self)

                    self.state = 1489
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                self.state = 1490
                self.match(ZmeiLangParser.BRACE_CLOSE)


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Inline_nameContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def id_or_kw(self):
            return self.getTypedRuleContext(ZmeiLangParser.Id_or_kwContext,0)


        def getRuleIndex(self):
            return ZmeiLangParser.RULE_inline_name

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterInline_name" ):
                listener.enterInline_name(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitInline_name" ):
                listener.exitInline_name(self)




    def inline_name(self):

        localctx = ZmeiLangParser.Inline_nameContext(self, self._ctx, self.state)
        self.enterRule(localctx, 244, self.RULE_inline_name)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1493
            self.id_or_kw()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Inline_typeContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def KW_TYPE(self):
            return self.getToken(ZmeiLangParser.KW_TYPE, 0)

        def COLON(self):
            return self.getToken(ZmeiLangParser.COLON, 0)

        def inline_type_name(self):
            return self.getTypedRuleContext(ZmeiLangParser.Inline_type_nameContext,0)


        def getRuleIndex(self):
            return ZmeiLangParser.RULE_inline_type

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterInline_type" ):
                listener.enterInline_type(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitInline_type" ):
                listener.exitInline_type(self)




    def inline_type(self):

        localctx = ZmeiLangParser.Inline_typeContext(self, self._ctx, self.state)
        self.enterRule(localctx, 246, self.RULE_inline_type)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1495
            self.match(ZmeiLangParser.KW_TYPE)
            self.state = 1496
            self.match(ZmeiLangParser.COLON)
            self.state = 1497
            self.inline_type_name()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Inline_type_nameContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def KW_INLINE_TYPE_TABULAR(self):
            return self.getToken(ZmeiLangParser.KW_INLINE_TYPE_TABULAR, 0)

        def KW_INLINE_TYPE_STACKED(self):
            return self.getToken(ZmeiLangParser.KW_INLINE_TYPE_STACKED, 0)

        def KW_INLINE_TYPE_POLYMORPHIC(self):
            return self.getToken(ZmeiLangParser.KW_INLINE_TYPE_POLYMORPHIC, 0)

        def getRuleIndex(self):
            return ZmeiLangParser.RULE_inline_type_name

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterInline_type_name" ):
                listener.enterInline_type_name(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitInline_type_name" ):
                listener.exitInline_type_name(self)




    def inline_type_name(self):

        localctx = ZmeiLangParser.Inline_type_nameContext(self, self._ctx, self.state)
        self.enterRule(localctx, 248, self.RULE_inline_type_name)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1499
            _la = self._input.LA(1)
            if not(((((_la - 94)) & ~0x3f) == 0 and ((1 << (_la - 94)) & ((1 << (ZmeiLangParser.KW_INLINE_TYPE_TABULAR - 94)) | (1 << (ZmeiLangParser.KW_INLINE_TYPE_STACKED - 94)) | (1 << (ZmeiLangParser.KW_INLINE_TYPE_POLYMORPHIC - 94)))) != 0)):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Inline_extensionContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def KW_EXTENSION(self):
            return self.getToken(ZmeiLangParser.KW_EXTENSION, 0)

        def COLON(self):
            return self.getToken(ZmeiLangParser.COLON, 0)

        def DIGIT(self):
            return self.getToken(ZmeiLangParser.DIGIT, 0)

        def getRuleIndex(self):
            return ZmeiLangParser.RULE_inline_extension

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterInline_extension" ):
                listener.enterInline_extension(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitInline_extension" ):
                listener.exitInline_extension(self)




    def inline_extension(self):

        localctx = ZmeiLangParser.Inline_extensionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 250, self.RULE_inline_extension)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1501
            self.match(ZmeiLangParser.KW_EXTENSION)
            self.state = 1502
            self.match(ZmeiLangParser.COLON)
            self.state = 1503
            self.match(ZmeiLangParser.DIGIT)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Inline_fieldsContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def KW_FIELDS(self):
            return self.getToken(ZmeiLangParser.KW_FIELDS, 0)

        def COLON(self):
            return self.getToken(ZmeiLangParser.COLON, 0)

        def field_list_expr(self):
            return self.getTypedRuleContext(ZmeiLangParser.Field_list_exprContext,0)


        def getRuleIndex(self):
            return ZmeiLangParser.RULE_inline_fields

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterInline_fields" ):
                listener.enterInline_fields(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitInline_fields" ):
                listener.exitInline_fields(self)




    def inline_fields(self):

        localctx = ZmeiLangParser.Inline_fieldsContext(self, self._ctx, self.state)
        self.enterRule(localctx, 252, self.RULE_inline_fields)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1505
            self.match(ZmeiLangParser.KW_FIELDS)
            self.state = 1506
            self.match(ZmeiLangParser.COLON)
            self.state = 1507
            self.field_list_expr()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class An_admin_tabsContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def KW_TABS(self):
            return self.getToken(ZmeiLangParser.KW_TABS, 0)

        def COLON(self):
            return self.getToken(ZmeiLangParser.COLON, 0)

        def an_admin_tab(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(ZmeiLangParser.An_admin_tabContext)
            else:
                return self.getTypedRuleContext(ZmeiLangParser.An_admin_tabContext,i)


        def COMA(self, i:int=None):
            if i is None:
                return self.getTokens(ZmeiLangParser.COMA)
            else:
                return self.getToken(ZmeiLangParser.COMA, i)

        def getRuleIndex(self):
            return ZmeiLangParser.RULE_an_admin_tabs

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAn_admin_tabs" ):
                listener.enterAn_admin_tabs(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAn_admin_tabs" ):
                listener.exitAn_admin_tabs(self)




    def an_admin_tabs(self):

        localctx = ZmeiLangParser.An_admin_tabsContext(self, self._ctx, self.state)
        self.enterRule(localctx, 254, self.RULE_an_admin_tabs)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1509
            self.match(ZmeiLangParser.KW_TABS)
            self.state = 1510
            self.match(ZmeiLangParser.COLON)
            self.state = 1511
            self.an_admin_tab()
            self.state = 1516
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,134,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 1512
                    self.match(ZmeiLangParser.COMA)
                    self.state = 1513
                    self.an_admin_tab() 
                self.state = 1518
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,134,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class An_admin_tabContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def tab_name(self):
            return self.getTypedRuleContext(ZmeiLangParser.Tab_nameContext,0)


        def BRACE_OPEN(self):
            return self.getToken(ZmeiLangParser.BRACE_OPEN, 0)

        def field_list_expr(self):
            return self.getTypedRuleContext(ZmeiLangParser.Field_list_exprContext,0)


        def BRACE_CLOSE(self):
            return self.getToken(ZmeiLangParser.BRACE_CLOSE, 0)

        def tab_verbose_name(self):
            return self.getTypedRuleContext(ZmeiLangParser.Tab_verbose_nameContext,0)


        def getRuleIndex(self):
            return ZmeiLangParser.RULE_an_admin_tab

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAn_admin_tab" ):
                listener.enterAn_admin_tab(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAn_admin_tab" ):
                listener.exitAn_admin_tab(self)




    def an_admin_tab(self):

        localctx = ZmeiLangParser.An_admin_tabContext(self, self._ctx, self.state)
        self.enterRule(localctx, 256, self.RULE_an_admin_tab)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1519
            self.tab_name()
            self.state = 1521
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==ZmeiLangParser.STRING_DQ or _la==ZmeiLangParser.STRING_SQ:
                self.state = 1520
                self.tab_verbose_name()


            self.state = 1523
            self.match(ZmeiLangParser.BRACE_OPEN)
            self.state = 1524
            self.field_list_expr()
            self.state = 1525
            self.match(ZmeiLangParser.BRACE_CLOSE)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Tab_nameContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def id_or_kw(self):
            return self.getTypedRuleContext(ZmeiLangParser.Id_or_kwContext,0)


        def getRuleIndex(self):
            return ZmeiLangParser.RULE_tab_name

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterTab_name" ):
                listener.enterTab_name(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitTab_name" ):
                listener.exitTab_name(self)




    def tab_name(self):

        localctx = ZmeiLangParser.Tab_nameContext(self, self._ctx, self.state)
        self.enterRule(localctx, 258, self.RULE_tab_name)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1527
            self.id_or_kw()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Tab_verbose_nameContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def STRING_DQ(self):
            return self.getToken(ZmeiLangParser.STRING_DQ, 0)

        def STRING_SQ(self):
            return self.getToken(ZmeiLangParser.STRING_SQ, 0)

        def getRuleIndex(self):
            return ZmeiLangParser.RULE_tab_verbose_name

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterTab_verbose_name" ):
                listener.enterTab_verbose_name(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitTab_verbose_name" ):
                listener.exitTab_verbose_name(self)




    def tab_verbose_name(self):

        localctx = ZmeiLangParser.Tab_verbose_nameContext(self, self._ctx, self.state)
        self.enterRule(localctx, 260, self.RULE_tab_verbose_name)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1529
            _la = self._input.LA(1)
            if not(_la==ZmeiLangParser.STRING_DQ or _la==ZmeiLangParser.STRING_SQ):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class An_admin_listContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def KW_LIST(self):
            return self.getToken(ZmeiLangParser.KW_LIST, 0)

        def COLON(self):
            return self.getToken(ZmeiLangParser.COLON, 0)

        def field_list_expr(self):
            return self.getTypedRuleContext(ZmeiLangParser.Field_list_exprContext,0)


        def NL(self, i:int=None):
            if i is None:
                return self.getTokens(ZmeiLangParser.NL)
            else:
                return self.getToken(ZmeiLangParser.NL, i)

        def getRuleIndex(self):
            return ZmeiLangParser.RULE_an_admin_list

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAn_admin_list" ):
                listener.enterAn_admin_list(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAn_admin_list" ):
                listener.exitAn_admin_list(self)




    def an_admin_list(self):

        localctx = ZmeiLangParser.An_admin_listContext(self, self._ctx, self.state)
        self.enterRule(localctx, 262, self.RULE_an_admin_list)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1531
            self.match(ZmeiLangParser.KW_LIST)
            self.state = 1532
            self.match(ZmeiLangParser.COLON)
            self.state = 1533
            self.field_list_expr()
            self.state = 1537
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,136,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 1534
                    self.match(ZmeiLangParser.NL) 
                self.state = 1539
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,136,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class An_admin_read_onlyContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def KW_READ_ONLY(self):
            return self.getToken(ZmeiLangParser.KW_READ_ONLY, 0)

        def COLON(self):
            return self.getToken(ZmeiLangParser.COLON, 0)

        def field_list_expr(self):
            return self.getTypedRuleContext(ZmeiLangParser.Field_list_exprContext,0)


        def NL(self, i:int=None):
            if i is None:
                return self.getTokens(ZmeiLangParser.NL)
            else:
                return self.getToken(ZmeiLangParser.NL, i)

        def getRuleIndex(self):
            return ZmeiLangParser.RULE_an_admin_read_only

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAn_admin_read_only" ):
                listener.enterAn_admin_read_only(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAn_admin_read_only" ):
                listener.exitAn_admin_read_only(self)




    def an_admin_read_only(self):

        localctx = ZmeiLangParser.An_admin_read_onlyContext(self, self._ctx, self.state)
        self.enterRule(localctx, 264, self.RULE_an_admin_read_only)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1540
            self.match(ZmeiLangParser.KW_READ_ONLY)
            self.state = 1541
            self.match(ZmeiLangParser.COLON)
            self.state = 1542
            self.field_list_expr()
            self.state = 1546
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,137,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 1543
                    self.match(ZmeiLangParser.NL) 
                self.state = 1548
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,137,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class An_admin_list_editableContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def KW_LIST_EDITABLE(self):
            return self.getToken(ZmeiLangParser.KW_LIST_EDITABLE, 0)

        def COLON(self):
            return self.getToken(ZmeiLangParser.COLON, 0)

        def field_list_expr(self):
            return self.getTypedRuleContext(ZmeiLangParser.Field_list_exprContext,0)


        def NL(self, i:int=None):
            if i is None:
                return self.getTokens(ZmeiLangParser.NL)
            else:
                return self.getToken(ZmeiLangParser.NL, i)

        def getRuleIndex(self):
            return ZmeiLangParser.RULE_an_admin_list_editable

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAn_admin_list_editable" ):
                listener.enterAn_admin_list_editable(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAn_admin_list_editable" ):
                listener.exitAn_admin_list_editable(self)




    def an_admin_list_editable(self):

        localctx = ZmeiLangParser.An_admin_list_editableContext(self, self._ctx, self.state)
        self.enterRule(localctx, 266, self.RULE_an_admin_list_editable)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1549
            self.match(ZmeiLangParser.KW_LIST_EDITABLE)
            self.state = 1550
            self.match(ZmeiLangParser.COLON)
            self.state = 1551
            self.field_list_expr()
            self.state = 1555
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,138,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 1552
                    self.match(ZmeiLangParser.NL) 
                self.state = 1557
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,138,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class An_admin_list_filterContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def KW_LIST_FILTER(self):
            return self.getToken(ZmeiLangParser.KW_LIST_FILTER, 0)

        def COLON(self):
            return self.getToken(ZmeiLangParser.COLON, 0)

        def field_list_expr(self):
            return self.getTypedRuleContext(ZmeiLangParser.Field_list_exprContext,0)


        def NL(self, i:int=None):
            if i is None:
                return self.getTokens(ZmeiLangParser.NL)
            else:
                return self.getToken(ZmeiLangParser.NL, i)

        def getRuleIndex(self):
            return ZmeiLangParser.RULE_an_admin_list_filter

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAn_admin_list_filter" ):
                listener.enterAn_admin_list_filter(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAn_admin_list_filter" ):
                listener.exitAn_admin_list_filter(self)




    def an_admin_list_filter(self):

        localctx = ZmeiLangParser.An_admin_list_filterContext(self, self._ctx, self.state)
        self.enterRule(localctx, 268, self.RULE_an_admin_list_filter)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1558
            self.match(ZmeiLangParser.KW_LIST_FILTER)
            self.state = 1559
            self.match(ZmeiLangParser.COLON)
            self.state = 1560
            self.field_list_expr()
            self.state = 1564
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,139,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 1561
                    self.match(ZmeiLangParser.NL) 
                self.state = 1566
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,139,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class An_admin_list_searchContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def KW_LIST_SEARCH(self):
            return self.getToken(ZmeiLangParser.KW_LIST_SEARCH, 0)

        def COLON(self):
            return self.getToken(ZmeiLangParser.COLON, 0)

        def field_list_expr(self):
            return self.getTypedRuleContext(ZmeiLangParser.Field_list_exprContext,0)


        def NL(self, i:int=None):
            if i is None:
                return self.getTokens(ZmeiLangParser.NL)
            else:
                return self.getToken(ZmeiLangParser.NL, i)

        def getRuleIndex(self):
            return ZmeiLangParser.RULE_an_admin_list_search

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAn_admin_list_search" ):
                listener.enterAn_admin_list_search(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAn_admin_list_search" ):
                listener.exitAn_admin_list_search(self)




    def an_admin_list_search(self):

        localctx = ZmeiLangParser.An_admin_list_searchContext(self, self._ctx, self.state)
        self.enterRule(localctx, 270, self.RULE_an_admin_list_search)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1567
            self.match(ZmeiLangParser.KW_LIST_SEARCH)
            self.state = 1568
            self.match(ZmeiLangParser.COLON)
            self.state = 1569
            self.field_list_expr()
            self.state = 1573
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,140,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 1570
                    self.match(ZmeiLangParser.NL) 
                self.state = 1575
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,140,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class An_admin_fieldsContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def KW_FIELDS(self):
            return self.getToken(ZmeiLangParser.KW_FIELDS, 0)

        def COLON(self):
            return self.getToken(ZmeiLangParser.COLON, 0)

        def field_list_expr(self):
            return self.getTypedRuleContext(ZmeiLangParser.Field_list_exprContext,0)


        def NL(self, i:int=None):
            if i is None:
                return self.getTokens(ZmeiLangParser.NL)
            else:
                return self.getToken(ZmeiLangParser.NL, i)

        def getRuleIndex(self):
            return ZmeiLangParser.RULE_an_admin_fields

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAn_admin_fields" ):
                listener.enterAn_admin_fields(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAn_admin_fields" ):
                listener.exitAn_admin_fields(self)




    def an_admin_fields(self):

        localctx = ZmeiLangParser.An_admin_fieldsContext(self, self._ctx, self.state)
        self.enterRule(localctx, 272, self.RULE_an_admin_fields)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1576
            self.match(ZmeiLangParser.KW_FIELDS)
            self.state = 1577
            self.match(ZmeiLangParser.COLON)
            self.state = 1578
            self.field_list_expr()
            self.state = 1582
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,141,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 1579
                    self.match(ZmeiLangParser.NL) 
                self.state = 1584
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,141,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class An_apiContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def AN_API(self):
            return self.getToken(ZmeiLangParser.AN_API, 0)

        def BRACE_OPEN(self):
            return self.getToken(ZmeiLangParser.BRACE_OPEN, 0)

        def BRACE_CLOSE(self):
            return self.getToken(ZmeiLangParser.BRACE_CLOSE, 0)

        def an_api_all(self):
            return self.getTypedRuleContext(ZmeiLangParser.An_api_allContext,0)


        def an_api_name(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(ZmeiLangParser.An_api_nameContext)
            else:
                return self.getTypedRuleContext(ZmeiLangParser.An_api_nameContext,i)


        def COMA(self, i:int=None):
            if i is None:
                return self.getTokens(ZmeiLangParser.COMA)
            else:
                return self.getToken(ZmeiLangParser.COMA, i)

        def getRuleIndex(self):
            return ZmeiLangParser.RULE_an_api

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAn_api" ):
                listener.enterAn_api(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAn_api" ):
                listener.exitAn_api(self)




    def an_api(self):

        localctx = ZmeiLangParser.An_apiContext(self, self._ctx, self.state)
        self.enterRule(localctx, 274, self.RULE_an_api)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1585
            self.match(ZmeiLangParser.AN_API)
            self.state = 1600
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==ZmeiLangParser.BRACE_OPEN:
                self.state = 1586
                self.match(ZmeiLangParser.BRACE_OPEN)
                self.state = 1596
                self._errHandler.sync(self)
                token = self._input.LA(1)
                if token in [ZmeiLangParser.STAR]:
                    self.state = 1587
                    self.an_api_all()
                    pass
                elif token in [ZmeiLangParser.KW_AUTH_TYPE_BASIC, ZmeiLangParser.KW_AUTH_TYPE_SESSION, ZmeiLangParser.KW_AUTH_TYPE_TOKEN, ZmeiLangParser.COL_FIELD_TYPE_LONGTEXT, ZmeiLangParser.COL_FIELD_TYPE_HTML, ZmeiLangParser.COL_FIELD_TYPE_HTML_MEDIA, ZmeiLangParser.COL_FIELD_TYPE_FLOAT, ZmeiLangParser.COL_FIELD_TYPE_DECIMAL, ZmeiLangParser.COL_FIELD_TYPE_DATE, ZmeiLangParser.COL_FIELD_TYPE_DATETIME, ZmeiLangParser.COL_FIELD_TYPE_CREATE_TIME, ZmeiLangParser.COL_FIELD_TYPE_UPDATE_TIME, ZmeiLangParser.COL_FIELD_TYPE_IMAGE, ZmeiLangParser.COL_FIELD_TYPE_FILE, ZmeiLangParser.COL_FIELD_TYPE_FILER_IMAGE, ZmeiLangParser.COL_FIELD_TYPE_FILER_FILE, ZmeiLangParser.COL_FIELD_TYPE_FILER_FOLDER, ZmeiLangParser.COL_FIELD_TYPE_FILER_IMAGE_FOLDER, ZmeiLangParser.COL_FIELD_TYPE_TEXT, ZmeiLangParser.COL_FIELD_TYPE_INT, ZmeiLangParser.COL_FIELD_TYPE_SLUG, ZmeiLangParser.COL_FIELD_TYPE_BOOL, ZmeiLangParser.COL_FIELD_TYPE_ONE, ZmeiLangParser.COL_FIELD_TYPE_ONE2ONE, ZmeiLangParser.COL_FIELD_TYPE_MANY, ZmeiLangParser.COL_FIELD_CHOICES, ZmeiLangParser.KW_THEME, ZmeiLangParser.KW_INSTALL, ZmeiLangParser.KW_HEADER, ZmeiLangParser.KW_SERVICES, ZmeiLangParser.KW_SELENIUM_PYTEST, ZmeiLangParser.KW_CHILD, ZmeiLangParser.KW_FILTER_OUT, ZmeiLangParser.KW_FILTER_IN, ZmeiLangParser.KW_PAGE, ZmeiLangParser.KW_LINK_SUFFIX, ZmeiLangParser.KW_URL_PREFIX, ZmeiLangParser.KW_CAN_EDIT, ZmeiLangParser.KW_OBJECT_EXPR, ZmeiLangParser.KW_BLOCK, ZmeiLangParser.KW_ITEM_NAME, ZmeiLangParser.KW_PK_PARAM, ZmeiLangParser.KW_LIST_FIELDS, ZmeiLangParser.KW_DELETE, ZmeiLangParser.KW_EDIT, ZmeiLangParser.KW_CREATE, ZmeiLangParser.KW_DETAIL, ZmeiLangParser.KW_SKIP, ZmeiLangParser.KW_FROM, ZmeiLangParser.KW_POLY_LIST, ZmeiLangParser.KW_CSS, ZmeiLangParser.KW_JS, ZmeiLangParser.KW_INLINE_TYPE_TABULAR, ZmeiLangParser.KW_INLINE_TYPE_STACKED, ZmeiLangParser.KW_INLINE_TYPE_POLYMORPHIC, ZmeiLangParser.KW_INLINE, ZmeiLangParser.KW_TYPE, ZmeiLangParser.KW_USER_FIELD, ZmeiLangParser.KW_ANNOTATE, ZmeiLangParser.KW_ON_CREATE, ZmeiLangParser.KW_QUERY, ZmeiLangParser.KW_AUTH, ZmeiLangParser.KW_COUNT, ZmeiLangParser.KW_I18N, ZmeiLangParser.KW_EXTENSION, ZmeiLangParser.KW_TABS, ZmeiLangParser.KW_LIST, ZmeiLangParser.KW_READ_ONLY, ZmeiLangParser.KW_LIST_EDITABLE, ZmeiLangParser.KW_LIST_FILTER, ZmeiLangParser.KW_LIST_SEARCH, ZmeiLangParser.KW_FIELDS, ZmeiLangParser.KW_IMPORT, ZmeiLangParser.KW_AS, ZmeiLangParser.WRITE_MODE, ZmeiLangParser.BOOL, ZmeiLangParser.ID]:
                    self.state = 1588
                    self.an_api_name()
                    self.state = 1593
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    while _la==ZmeiLangParser.COMA:
                        self.state = 1589
                        self.match(ZmeiLangParser.COMA)
                        self.state = 1590
                        self.an_api_name()
                        self.state = 1595
                        self._errHandler.sync(self)
                        _la = self._input.LA(1)

                    pass
                else:
                    raise NoViableAltException(self)

                self.state = 1598
                self.match(ZmeiLangParser.BRACE_CLOSE)


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class An_api_allContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def STAR(self):
            return self.getToken(ZmeiLangParser.STAR, 0)

        def getRuleIndex(self):
            return ZmeiLangParser.RULE_an_api_all

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAn_api_all" ):
                listener.enterAn_api_all(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAn_api_all" ):
                listener.exitAn_api_all(self)




    def an_api_all(self):

        localctx = ZmeiLangParser.An_api_allContext(self, self._ctx, self.state)
        self.enterRule(localctx, 276, self.RULE_an_api_all)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1602
            self.match(ZmeiLangParser.STAR)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class An_api_nameContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def id_or_kw(self):
            return self.getTypedRuleContext(ZmeiLangParser.Id_or_kwContext,0)


        def getRuleIndex(self):
            return ZmeiLangParser.RULE_an_api_name

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAn_api_name" ):
                listener.enterAn_api_name(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAn_api_name" ):
                listener.exitAn_api_name(self)




    def an_api_name(self):

        localctx = ZmeiLangParser.An_api_nameContext(self, self._ctx, self.state)
        self.enterRule(localctx, 278, self.RULE_an_api_name)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1604
            self.id_or_kw()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class An_restContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def AN_REST(self):
            return self.getToken(ZmeiLangParser.AN_REST, 0)

        def DOT(self):
            return self.getToken(ZmeiLangParser.DOT, 0)

        def an_rest_descriptor(self):
            return self.getTypedRuleContext(ZmeiLangParser.An_rest_descriptorContext,0)


        def BRACE_OPEN(self):
            return self.getToken(ZmeiLangParser.BRACE_OPEN, 0)

        def an_rest_config(self):
            return self.getTypedRuleContext(ZmeiLangParser.An_rest_configContext,0)


        def BRACE_CLOSE(self):
            return self.getToken(ZmeiLangParser.BRACE_CLOSE, 0)

        def getRuleIndex(self):
            return ZmeiLangParser.RULE_an_rest

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAn_rest" ):
                listener.enterAn_rest(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAn_rest" ):
                listener.exitAn_rest(self)




    def an_rest(self):

        localctx = ZmeiLangParser.An_restContext(self, self._ctx, self.state)
        self.enterRule(localctx, 280, self.RULE_an_rest)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1606
            self.match(ZmeiLangParser.AN_REST)
            self.state = 1609
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==ZmeiLangParser.DOT:
                self.state = 1607
                self.match(ZmeiLangParser.DOT)
                self.state = 1608
                self.an_rest_descriptor()


            self.state = 1615
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==ZmeiLangParser.BRACE_OPEN:
                self.state = 1611
                self.match(ZmeiLangParser.BRACE_OPEN)
                self.state = 1612
                self.an_rest_config()
                self.state = 1613
                self.match(ZmeiLangParser.BRACE_CLOSE)


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class An_rest_configContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def an_rest_main_part(self):
            return self.getTypedRuleContext(ZmeiLangParser.An_rest_main_partContext,0)


        def an_rest_inline(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(ZmeiLangParser.An_rest_inlineContext)
            else:
                return self.getTypedRuleContext(ZmeiLangParser.An_rest_inlineContext,i)


        def NL(self, i:int=None):
            if i is None:
                return self.getTokens(ZmeiLangParser.NL)
            else:
                return self.getToken(ZmeiLangParser.NL, i)

        def COMA(self, i:int=None):
            if i is None:
                return self.getTokens(ZmeiLangParser.COMA)
            else:
                return self.getToken(ZmeiLangParser.COMA, i)

        def getRuleIndex(self):
            return ZmeiLangParser.RULE_an_rest_config

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAn_rest_config" ):
                listener.enterAn_rest_config(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAn_rest_config" ):
                listener.exitAn_rest_config(self)




    def an_rest_config(self):

        localctx = ZmeiLangParser.An_rest_configContext(self, self._ctx, self.state)
        self.enterRule(localctx, 282, self.RULE_an_rest_config)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1617
            self.an_rest_main_part()
            self.state = 1623
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while ((((_la - 97)) & ~0x3f) == 0 and ((1 << (_la - 97)) & ((1 << (ZmeiLangParser.KW_INLINE - 97)) | (1 << (ZmeiLangParser.NL - 97)) | (1 << (ZmeiLangParser.COMA - 97)))) != 0):
                self.state = 1621
                self._errHandler.sync(self)
                token = self._input.LA(1)
                if token in [ZmeiLangParser.KW_INLINE]:
                    self.state = 1618
                    self.an_rest_inline()
                    pass
                elif token in [ZmeiLangParser.NL]:
                    self.state = 1619
                    self.match(ZmeiLangParser.NL)
                    pass
                elif token in [ZmeiLangParser.COMA]:
                    self.state = 1620
                    self.match(ZmeiLangParser.COMA)
                    pass
                else:
                    raise NoViableAltException(self)

                self.state = 1625
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class An_rest_main_partContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def an_rest_fields(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(ZmeiLangParser.An_rest_fieldsContext)
            else:
                return self.getTypedRuleContext(ZmeiLangParser.An_rest_fieldsContext,i)


        def an_rest_i18n(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(ZmeiLangParser.An_rest_i18nContext)
            else:
                return self.getTypedRuleContext(ZmeiLangParser.An_rest_i18nContext,i)


        def an_rest_auth(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(ZmeiLangParser.An_rest_authContext)
            else:
                return self.getTypedRuleContext(ZmeiLangParser.An_rest_authContext,i)


        def an_rest_query(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(ZmeiLangParser.An_rest_queryContext)
            else:
                return self.getTypedRuleContext(ZmeiLangParser.An_rest_queryContext,i)


        def an_rest_on_create(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(ZmeiLangParser.An_rest_on_createContext)
            else:
                return self.getTypedRuleContext(ZmeiLangParser.An_rest_on_createContext,i)


        def an_rest_filter_in(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(ZmeiLangParser.An_rest_filter_inContext)
            else:
                return self.getTypedRuleContext(ZmeiLangParser.An_rest_filter_inContext,i)


        def an_rest_filter_out(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(ZmeiLangParser.An_rest_filter_outContext)
            else:
                return self.getTypedRuleContext(ZmeiLangParser.An_rest_filter_outContext,i)


        def an_rest_read_only(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(ZmeiLangParser.An_rest_read_onlyContext)
            else:
                return self.getTypedRuleContext(ZmeiLangParser.An_rest_read_onlyContext,i)


        def an_rest_user_field(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(ZmeiLangParser.An_rest_user_fieldContext)
            else:
                return self.getTypedRuleContext(ZmeiLangParser.An_rest_user_fieldContext,i)


        def an_rest_annotate(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(ZmeiLangParser.An_rest_annotateContext)
            else:
                return self.getTypedRuleContext(ZmeiLangParser.An_rest_annotateContext,i)


        def NL(self, i:int=None):
            if i is None:
                return self.getTokens(ZmeiLangParser.NL)
            else:
                return self.getToken(ZmeiLangParser.NL, i)

        def COMA(self, i:int=None):
            if i is None:
                return self.getTokens(ZmeiLangParser.COMA)
            else:
                return self.getToken(ZmeiLangParser.COMA, i)

        def getRuleIndex(self):
            return ZmeiLangParser.RULE_an_rest_main_part

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAn_rest_main_part" ):
                listener.enterAn_rest_main_part(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAn_rest_main_part" ):
                listener.exitAn_rest_main_part(self)




    def an_rest_main_part(self):

        localctx = ZmeiLangParser.An_rest_main_partContext(self, self._ctx, self.state)
        self.enterRule(localctx, 284, self.RULE_an_rest_main_part)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1640
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,150,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 1638
                    self._errHandler.sync(self)
                    token = self._input.LA(1)
                    if token in [ZmeiLangParser.KW_FIELDS]:
                        self.state = 1626
                        self.an_rest_fields()
                        pass
                    elif token in [ZmeiLangParser.KW_I18N]:
                        self.state = 1627
                        self.an_rest_i18n()
                        pass
                    elif token in [ZmeiLangParser.KW_AUTH]:
                        self.state = 1628
                        self.an_rest_auth()
                        pass
                    elif token in [ZmeiLangParser.KW_QUERY]:
                        self.state = 1629
                        self.an_rest_query()
                        pass
                    elif token in [ZmeiLangParser.KW_ON_CREATE]:
                        self.state = 1630
                        self.an_rest_on_create()
                        pass
                    elif token in [ZmeiLangParser.KW_FILTER_IN]:
                        self.state = 1631
                        self.an_rest_filter_in()
                        pass
                    elif token in [ZmeiLangParser.KW_FILTER_OUT]:
                        self.state = 1632
                        self.an_rest_filter_out()
                        pass
                    elif token in [ZmeiLangParser.KW_READ_ONLY]:
                        self.state = 1633
                        self.an_rest_read_only()
                        pass
                    elif token in [ZmeiLangParser.KW_USER_FIELD]:
                        self.state = 1634
                        self.an_rest_user_field()
                        pass
                    elif token in [ZmeiLangParser.KW_ANNOTATE]:
                        self.state = 1635
                        self.an_rest_annotate()
                        pass
                    elif token in [ZmeiLangParser.NL]:
                        self.state = 1636
                        self.match(ZmeiLangParser.NL)
                        pass
                    elif token in [ZmeiLangParser.COMA]:
                        self.state = 1637
                        self.match(ZmeiLangParser.COMA)
                        pass
                    else:
                        raise NoViableAltException(self)
             
                self.state = 1642
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,150,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class An_rest_descriptorContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def id_or_kw(self):
            return self.getTypedRuleContext(ZmeiLangParser.Id_or_kwContext,0)


        def getRuleIndex(self):
            return ZmeiLangParser.RULE_an_rest_descriptor

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAn_rest_descriptor" ):
                listener.enterAn_rest_descriptor(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAn_rest_descriptor" ):
                listener.exitAn_rest_descriptor(self)




    def an_rest_descriptor(self):

        localctx = ZmeiLangParser.An_rest_descriptorContext(self, self._ctx, self.state)
        self.enterRule(localctx, 286, self.RULE_an_rest_descriptor)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1643
            self.id_or_kw()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class An_rest_i18nContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def KW_I18N(self):
            return self.getToken(ZmeiLangParser.KW_I18N, 0)

        def COLON(self):
            return self.getToken(ZmeiLangParser.COLON, 0)

        def BOOL(self):
            return self.getToken(ZmeiLangParser.BOOL, 0)

        def NL(self, i:int=None):
            if i is None:
                return self.getTokens(ZmeiLangParser.NL)
            else:
                return self.getToken(ZmeiLangParser.NL, i)

        def getRuleIndex(self):
            return ZmeiLangParser.RULE_an_rest_i18n

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAn_rest_i18n" ):
                listener.enterAn_rest_i18n(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAn_rest_i18n" ):
                listener.exitAn_rest_i18n(self)




    def an_rest_i18n(self):

        localctx = ZmeiLangParser.An_rest_i18nContext(self, self._ctx, self.state)
        self.enterRule(localctx, 288, self.RULE_an_rest_i18n)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1645
            self.match(ZmeiLangParser.KW_I18N)
            self.state = 1646
            self.match(ZmeiLangParser.COLON)
            self.state = 1647
            self.match(ZmeiLangParser.BOOL)
            self.state = 1651
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,151,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 1648
                    self.match(ZmeiLangParser.NL) 
                self.state = 1653
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,151,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class An_rest_queryContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def KW_QUERY(self):
            return self.getToken(ZmeiLangParser.KW_QUERY, 0)

        def python_code(self):
            return self.getTypedRuleContext(ZmeiLangParser.Python_codeContext,0)


        def NL(self, i:int=None):
            if i is None:
                return self.getTokens(ZmeiLangParser.NL)
            else:
                return self.getToken(ZmeiLangParser.NL, i)

        def getRuleIndex(self):
            return ZmeiLangParser.RULE_an_rest_query

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAn_rest_query" ):
                listener.enterAn_rest_query(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAn_rest_query" ):
                listener.exitAn_rest_query(self)




    def an_rest_query(self):

        localctx = ZmeiLangParser.An_rest_queryContext(self, self._ctx, self.state)
        self.enterRule(localctx, 290, self.RULE_an_rest_query)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1654
            self.match(ZmeiLangParser.KW_QUERY)
            self.state = 1655
            self.python_code()
            self.state = 1659
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,152,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 1656
                    self.match(ZmeiLangParser.NL) 
                self.state = 1661
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,152,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class An_rest_on_createContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def KW_ON_CREATE(self):
            return self.getToken(ZmeiLangParser.KW_ON_CREATE, 0)

        def python_code(self):
            return self.getTypedRuleContext(ZmeiLangParser.Python_codeContext,0)


        def COLON(self):
            return self.getToken(ZmeiLangParser.COLON, 0)

        def NL(self, i:int=None):
            if i is None:
                return self.getTokens(ZmeiLangParser.NL)
            else:
                return self.getToken(ZmeiLangParser.NL, i)

        def getRuleIndex(self):
            return ZmeiLangParser.RULE_an_rest_on_create

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAn_rest_on_create" ):
                listener.enterAn_rest_on_create(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAn_rest_on_create" ):
                listener.exitAn_rest_on_create(self)




    def an_rest_on_create(self):

        localctx = ZmeiLangParser.An_rest_on_createContext(self, self._ctx, self.state)
        self.enterRule(localctx, 292, self.RULE_an_rest_on_create)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1662
            self.match(ZmeiLangParser.KW_ON_CREATE)
            self.state = 1664
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==ZmeiLangParser.COLON:
                self.state = 1663
                self.match(ZmeiLangParser.COLON)


            self.state = 1666
            self.python_code()
            self.state = 1670
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,154,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 1667
                    self.match(ZmeiLangParser.NL) 
                self.state = 1672
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,154,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class An_rest_filter_inContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def KW_FILTER_IN(self):
            return self.getToken(ZmeiLangParser.KW_FILTER_IN, 0)

        def python_code(self):
            return self.getTypedRuleContext(ZmeiLangParser.Python_codeContext,0)


        def COLON(self):
            return self.getToken(ZmeiLangParser.COLON, 0)

        def NL(self, i:int=None):
            if i is None:
                return self.getTokens(ZmeiLangParser.NL)
            else:
                return self.getToken(ZmeiLangParser.NL, i)

        def getRuleIndex(self):
            return ZmeiLangParser.RULE_an_rest_filter_in

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAn_rest_filter_in" ):
                listener.enterAn_rest_filter_in(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAn_rest_filter_in" ):
                listener.exitAn_rest_filter_in(self)




    def an_rest_filter_in(self):

        localctx = ZmeiLangParser.An_rest_filter_inContext(self, self._ctx, self.state)
        self.enterRule(localctx, 294, self.RULE_an_rest_filter_in)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1673
            self.match(ZmeiLangParser.KW_FILTER_IN)
            self.state = 1675
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==ZmeiLangParser.COLON:
                self.state = 1674
                self.match(ZmeiLangParser.COLON)


            self.state = 1677
            self.python_code()
            self.state = 1681
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,156,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 1678
                    self.match(ZmeiLangParser.NL) 
                self.state = 1683
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,156,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class An_rest_filter_outContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def KW_FILTER_OUT(self):
            return self.getToken(ZmeiLangParser.KW_FILTER_OUT, 0)

        def python_code(self):
            return self.getTypedRuleContext(ZmeiLangParser.Python_codeContext,0)


        def COLON(self):
            return self.getToken(ZmeiLangParser.COLON, 0)

        def NL(self, i:int=None):
            if i is None:
                return self.getTokens(ZmeiLangParser.NL)
            else:
                return self.getToken(ZmeiLangParser.NL, i)

        def getRuleIndex(self):
            return ZmeiLangParser.RULE_an_rest_filter_out

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAn_rest_filter_out" ):
                listener.enterAn_rest_filter_out(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAn_rest_filter_out" ):
                listener.exitAn_rest_filter_out(self)




    def an_rest_filter_out(self):

        localctx = ZmeiLangParser.An_rest_filter_outContext(self, self._ctx, self.state)
        self.enterRule(localctx, 296, self.RULE_an_rest_filter_out)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1684
            self.match(ZmeiLangParser.KW_FILTER_OUT)
            self.state = 1686
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==ZmeiLangParser.COLON:
                self.state = 1685
                self.match(ZmeiLangParser.COLON)


            self.state = 1688
            self.python_code()
            self.state = 1692
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,158,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 1689
                    self.match(ZmeiLangParser.NL) 
                self.state = 1694
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,158,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class An_rest_read_onlyContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def KW_READ_ONLY(self):
            return self.getToken(ZmeiLangParser.KW_READ_ONLY, 0)

        def COLON(self):
            return self.getToken(ZmeiLangParser.COLON, 0)

        def field_list_expr(self):
            return self.getTypedRuleContext(ZmeiLangParser.Field_list_exprContext,0)


        def NL(self, i:int=None):
            if i is None:
                return self.getTokens(ZmeiLangParser.NL)
            else:
                return self.getToken(ZmeiLangParser.NL, i)

        def getRuleIndex(self):
            return ZmeiLangParser.RULE_an_rest_read_only

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAn_rest_read_only" ):
                listener.enterAn_rest_read_only(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAn_rest_read_only" ):
                listener.exitAn_rest_read_only(self)




    def an_rest_read_only(self):

        localctx = ZmeiLangParser.An_rest_read_onlyContext(self, self._ctx, self.state)
        self.enterRule(localctx, 298, self.RULE_an_rest_read_only)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1695
            self.match(ZmeiLangParser.KW_READ_ONLY)
            self.state = 1696
            self.match(ZmeiLangParser.COLON)
            self.state = 1697
            self.field_list_expr()
            self.state = 1701
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,159,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 1698
                    self.match(ZmeiLangParser.NL) 
                self.state = 1703
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,159,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class An_rest_user_fieldContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def KW_USER_FIELD(self):
            return self.getToken(ZmeiLangParser.KW_USER_FIELD, 0)

        def COLON(self):
            return self.getToken(ZmeiLangParser.COLON, 0)

        def id_or_kw(self):
            return self.getTypedRuleContext(ZmeiLangParser.Id_or_kwContext,0)


        def NL(self, i:int=None):
            if i is None:
                return self.getTokens(ZmeiLangParser.NL)
            else:
                return self.getToken(ZmeiLangParser.NL, i)

        def getRuleIndex(self):
            return ZmeiLangParser.RULE_an_rest_user_field

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAn_rest_user_field" ):
                listener.enterAn_rest_user_field(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAn_rest_user_field" ):
                listener.exitAn_rest_user_field(self)




    def an_rest_user_field(self):

        localctx = ZmeiLangParser.An_rest_user_fieldContext(self, self._ctx, self.state)
        self.enterRule(localctx, 300, self.RULE_an_rest_user_field)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1704
            self.match(ZmeiLangParser.KW_USER_FIELD)
            self.state = 1705
            self.match(ZmeiLangParser.COLON)
            self.state = 1706
            self.id_or_kw()
            self.state = 1710
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,160,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 1707
                    self.match(ZmeiLangParser.NL) 
                self.state = 1712
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,160,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class An_rest_fieldsContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def KW_FIELDS(self):
            return self.getToken(ZmeiLangParser.KW_FIELDS, 0)

        def COLON(self):
            return self.getToken(ZmeiLangParser.COLON, 0)

        def field_list_expr(self):
            return self.getTypedRuleContext(ZmeiLangParser.Field_list_exprContext,0)


        def an_rest_fields_write_mode(self):
            return self.getTypedRuleContext(ZmeiLangParser.An_rest_fields_write_modeContext,0)


        def NL(self, i:int=None):
            if i is None:
                return self.getTokens(ZmeiLangParser.NL)
            else:
                return self.getToken(ZmeiLangParser.NL, i)

        def getRuleIndex(self):
            return ZmeiLangParser.RULE_an_rest_fields

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAn_rest_fields" ):
                listener.enterAn_rest_fields(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAn_rest_fields" ):
                listener.exitAn_rest_fields(self)




    def an_rest_fields(self):

        localctx = ZmeiLangParser.An_rest_fieldsContext(self, self._ctx, self.state)
        self.enterRule(localctx, 302, self.RULE_an_rest_fields)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1713
            self.match(ZmeiLangParser.KW_FIELDS)
            self.state = 1714
            self.match(ZmeiLangParser.COLON)
            self.state = 1715
            self.field_list_expr()
            self.state = 1717
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==ZmeiLangParser.SQ_BRACE_OPEN:
                self.state = 1716
                self.an_rest_fields_write_mode()


            self.state = 1722
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,162,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 1719
                    self.match(ZmeiLangParser.NL) 
                self.state = 1724
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,162,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class An_rest_fields_write_modeContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def write_mode_expr(self):
            return self.getTypedRuleContext(ZmeiLangParser.Write_mode_exprContext,0)


        def getRuleIndex(self):
            return ZmeiLangParser.RULE_an_rest_fields_write_mode

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAn_rest_fields_write_mode" ):
                listener.enterAn_rest_fields_write_mode(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAn_rest_fields_write_mode" ):
                listener.exitAn_rest_fields_write_mode(self)




    def an_rest_fields_write_mode(self):

        localctx = ZmeiLangParser.An_rest_fields_write_modeContext(self, self._ctx, self.state)
        self.enterRule(localctx, 304, self.RULE_an_rest_fields_write_mode)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1725
            self.write_mode_expr()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class An_rest_authContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def KW_AUTH(self):
            return self.getToken(ZmeiLangParser.KW_AUTH, 0)

        def BRACE_OPEN(self):
            return self.getToken(ZmeiLangParser.BRACE_OPEN, 0)

        def an_rest_auth_type(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(ZmeiLangParser.An_rest_auth_typeContext)
            else:
                return self.getTypedRuleContext(ZmeiLangParser.An_rest_auth_typeContext,i)


        def BRACE_CLOSE(self):
            return self.getToken(ZmeiLangParser.BRACE_CLOSE, 0)

        def COMA(self, i:int=None):
            if i is None:
                return self.getTokens(ZmeiLangParser.COMA)
            else:
                return self.getToken(ZmeiLangParser.COMA, i)

        def getRuleIndex(self):
            return ZmeiLangParser.RULE_an_rest_auth

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAn_rest_auth" ):
                listener.enterAn_rest_auth(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAn_rest_auth" ):
                listener.exitAn_rest_auth(self)




    def an_rest_auth(self):

        localctx = ZmeiLangParser.An_rest_authContext(self, self._ctx, self.state)
        self.enterRule(localctx, 306, self.RULE_an_rest_auth)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1727
            self.match(ZmeiLangParser.KW_AUTH)
            self.state = 1728
            self.match(ZmeiLangParser.BRACE_OPEN)
            self.state = 1729
            self.an_rest_auth_type()
            self.state = 1734
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==ZmeiLangParser.COMA:
                self.state = 1730
                self.match(ZmeiLangParser.COMA)
                self.state = 1731
                self.an_rest_auth_type()
                self.state = 1736
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 1737
            self.match(ZmeiLangParser.BRACE_CLOSE)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class An_rest_auth_typeContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def an_rest_auth_type_name(self):
            return self.getTypedRuleContext(ZmeiLangParser.An_rest_auth_type_nameContext,0)


        def COLON(self):
            return self.getToken(ZmeiLangParser.COLON, 0)

        def an_rest_auth_token_model(self):
            return self.getTypedRuleContext(ZmeiLangParser.An_rest_auth_token_modelContext,0)


        def an_rest_auth_token_class(self):
            return self.getTypedRuleContext(ZmeiLangParser.An_rest_auth_token_classContext,0)


        def getRuleIndex(self):
            return ZmeiLangParser.RULE_an_rest_auth_type

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAn_rest_auth_type" ):
                listener.enterAn_rest_auth_type(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAn_rest_auth_type" ):
                listener.exitAn_rest_auth_type(self)




    def an_rest_auth_type(self):

        localctx = ZmeiLangParser.An_rest_auth_typeContext(self, self._ctx, self.state)
        self.enterRule(localctx, 308, self.RULE_an_rest_auth_type)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1739
            self.an_rest_auth_type_name()
            self.state = 1743
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [ZmeiLangParser.COLON]:
                self.state = 1740
                self.match(ZmeiLangParser.COLON)
                self.state = 1741
                self.an_rest_auth_token_model()
                pass
            elif token in [ZmeiLangParser.KW_AUTH_TYPE_BASIC, ZmeiLangParser.KW_AUTH_TYPE_SESSION, ZmeiLangParser.KW_AUTH_TYPE_TOKEN, ZmeiLangParser.COL_FIELD_TYPE_LONGTEXT, ZmeiLangParser.COL_FIELD_TYPE_HTML, ZmeiLangParser.COL_FIELD_TYPE_HTML_MEDIA, ZmeiLangParser.COL_FIELD_TYPE_FLOAT, ZmeiLangParser.COL_FIELD_TYPE_DECIMAL, ZmeiLangParser.COL_FIELD_TYPE_DATE, ZmeiLangParser.COL_FIELD_TYPE_DATETIME, ZmeiLangParser.COL_FIELD_TYPE_CREATE_TIME, ZmeiLangParser.COL_FIELD_TYPE_UPDATE_TIME, ZmeiLangParser.COL_FIELD_TYPE_IMAGE, ZmeiLangParser.COL_FIELD_TYPE_FILE, ZmeiLangParser.COL_FIELD_TYPE_FILER_IMAGE, ZmeiLangParser.COL_FIELD_TYPE_FILER_FILE, ZmeiLangParser.COL_FIELD_TYPE_FILER_FOLDER, ZmeiLangParser.COL_FIELD_TYPE_FILER_IMAGE_FOLDER, ZmeiLangParser.COL_FIELD_TYPE_TEXT, ZmeiLangParser.COL_FIELD_TYPE_INT, ZmeiLangParser.COL_FIELD_TYPE_SLUG, ZmeiLangParser.COL_FIELD_TYPE_BOOL, ZmeiLangParser.COL_FIELD_TYPE_ONE, ZmeiLangParser.COL_FIELD_TYPE_ONE2ONE, ZmeiLangParser.COL_FIELD_TYPE_MANY, ZmeiLangParser.COL_FIELD_CHOICES, ZmeiLangParser.KW_THEME, ZmeiLangParser.KW_INSTALL, ZmeiLangParser.KW_HEADER, ZmeiLangParser.KW_SERVICES, ZmeiLangParser.KW_SELENIUM_PYTEST, ZmeiLangParser.KW_CHILD, ZmeiLangParser.KW_FILTER_OUT, ZmeiLangParser.KW_FILTER_IN, ZmeiLangParser.KW_PAGE, ZmeiLangParser.KW_LINK_SUFFIX, ZmeiLangParser.KW_URL_PREFIX, ZmeiLangParser.KW_CAN_EDIT, ZmeiLangParser.KW_OBJECT_EXPR, ZmeiLangParser.KW_BLOCK, ZmeiLangParser.KW_ITEM_NAME, ZmeiLangParser.KW_PK_PARAM, ZmeiLangParser.KW_LIST_FIELDS, ZmeiLangParser.KW_DELETE, ZmeiLangParser.KW_EDIT, ZmeiLangParser.KW_CREATE, ZmeiLangParser.KW_DETAIL, ZmeiLangParser.KW_SKIP, ZmeiLangParser.KW_FROM, ZmeiLangParser.KW_POLY_LIST, ZmeiLangParser.KW_CSS, ZmeiLangParser.KW_JS, ZmeiLangParser.KW_INLINE_TYPE_TABULAR, ZmeiLangParser.KW_INLINE_TYPE_STACKED, ZmeiLangParser.KW_INLINE_TYPE_POLYMORPHIC, ZmeiLangParser.KW_INLINE, ZmeiLangParser.KW_TYPE, ZmeiLangParser.KW_USER_FIELD, ZmeiLangParser.KW_ANNOTATE, ZmeiLangParser.KW_ON_CREATE, ZmeiLangParser.KW_QUERY, ZmeiLangParser.KW_AUTH, ZmeiLangParser.KW_COUNT, ZmeiLangParser.KW_I18N, ZmeiLangParser.KW_EXTENSION, ZmeiLangParser.KW_TABS, ZmeiLangParser.KW_LIST, ZmeiLangParser.KW_READ_ONLY, ZmeiLangParser.KW_LIST_EDITABLE, ZmeiLangParser.KW_LIST_FILTER, ZmeiLangParser.KW_LIST_SEARCH, ZmeiLangParser.KW_FIELDS, ZmeiLangParser.KW_IMPORT, ZmeiLangParser.KW_AS, ZmeiLangParser.WRITE_MODE, ZmeiLangParser.BOOL, ZmeiLangParser.ID]:
                self.state = 1742
                self.an_rest_auth_token_class()
                pass
            elif token in [ZmeiLangParser.BRACE_CLOSE, ZmeiLangParser.COMA]:
                pass
            else:
                pass
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class An_rest_auth_type_nameContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def KW_AUTH_TYPE_BASIC(self):
            return self.getToken(ZmeiLangParser.KW_AUTH_TYPE_BASIC, 0)

        def KW_AUTH_TYPE_SESSION(self):
            return self.getToken(ZmeiLangParser.KW_AUTH_TYPE_SESSION, 0)

        def KW_AUTH_TYPE_TOKEN(self):
            return self.getToken(ZmeiLangParser.KW_AUTH_TYPE_TOKEN, 0)

        def getRuleIndex(self):
            return ZmeiLangParser.RULE_an_rest_auth_type_name

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAn_rest_auth_type_name" ):
                listener.enterAn_rest_auth_type_name(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAn_rest_auth_type_name" ):
                listener.exitAn_rest_auth_type_name(self)




    def an_rest_auth_type_name(self):

        localctx = ZmeiLangParser.An_rest_auth_type_nameContext(self, self._ctx, self.state)
        self.enterRule(localctx, 310, self.RULE_an_rest_auth_type_name)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1745
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << ZmeiLangParser.KW_AUTH_TYPE_BASIC) | (1 << ZmeiLangParser.KW_AUTH_TYPE_SESSION) | (1 << ZmeiLangParser.KW_AUTH_TYPE_TOKEN))) != 0)):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class An_rest_auth_token_modelContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def model_ref(self):
            return self.getTypedRuleContext(ZmeiLangParser.Model_refContext,0)


        def getRuleIndex(self):
            return ZmeiLangParser.RULE_an_rest_auth_token_model

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAn_rest_auth_token_model" ):
                listener.enterAn_rest_auth_token_model(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAn_rest_auth_token_model" ):
                listener.exitAn_rest_auth_token_model(self)




    def an_rest_auth_token_model(self):

        localctx = ZmeiLangParser.An_rest_auth_token_modelContext(self, self._ctx, self.state)
        self.enterRule(localctx, 312, self.RULE_an_rest_auth_token_model)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1747
            self.model_ref()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class An_rest_auth_token_classContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def classname(self):
            return self.getTypedRuleContext(ZmeiLangParser.ClassnameContext,0)


        def getRuleIndex(self):
            return ZmeiLangParser.RULE_an_rest_auth_token_class

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAn_rest_auth_token_class" ):
                listener.enterAn_rest_auth_token_class(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAn_rest_auth_token_class" ):
                listener.exitAn_rest_auth_token_class(self)




    def an_rest_auth_token_class(self):

        localctx = ZmeiLangParser.An_rest_auth_token_classContext(self, self._ctx, self.state)
        self.enterRule(localctx, 314, self.RULE_an_rest_auth_token_class)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1749
            self.classname()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class An_rest_annotateContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def KW_ANNOTATE(self):
            return self.getToken(ZmeiLangParser.KW_ANNOTATE, 0)

        def COLON(self):
            return self.getToken(ZmeiLangParser.COLON, 0)

        def an_rest_annotate_count(self):
            return self.getTypedRuleContext(ZmeiLangParser.An_rest_annotate_countContext,0)


        def NL(self, i:int=None):
            if i is None:
                return self.getTokens(ZmeiLangParser.NL)
            else:
                return self.getToken(ZmeiLangParser.NL, i)

        def getRuleIndex(self):
            return ZmeiLangParser.RULE_an_rest_annotate

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAn_rest_annotate" ):
                listener.enterAn_rest_annotate(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAn_rest_annotate" ):
                listener.exitAn_rest_annotate(self)




    def an_rest_annotate(self):

        localctx = ZmeiLangParser.An_rest_annotateContext(self, self._ctx, self.state)
        self.enterRule(localctx, 316, self.RULE_an_rest_annotate)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1751
            self.match(ZmeiLangParser.KW_ANNOTATE)
            self.state = 1752
            self.match(ZmeiLangParser.COLON)
            self.state = 1753
            self.an_rest_annotate_count()
            self.state = 1757
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,165,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 1754
                    self.match(ZmeiLangParser.NL) 
                self.state = 1759
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,165,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class An_rest_annotate_countContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def KW_COUNT(self):
            return self.getToken(ZmeiLangParser.KW_COUNT, 0)

        def an_rest_annotate_count_field(self):
            return self.getTypedRuleContext(ZmeiLangParser.An_rest_annotate_count_fieldContext,0)


        def KW_AS(self):
            return self.getToken(ZmeiLangParser.KW_AS, 0)

        def an_rest_annotate_count_alias(self):
            return self.getTypedRuleContext(ZmeiLangParser.An_rest_annotate_count_aliasContext,0)


        def getRuleIndex(self):
            return ZmeiLangParser.RULE_an_rest_annotate_count

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAn_rest_annotate_count" ):
                listener.enterAn_rest_annotate_count(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAn_rest_annotate_count" ):
                listener.exitAn_rest_annotate_count(self)




    def an_rest_annotate_count(self):

        localctx = ZmeiLangParser.An_rest_annotate_countContext(self, self._ctx, self.state)
        self.enterRule(localctx, 318, self.RULE_an_rest_annotate_count)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1760
            self.match(ZmeiLangParser.KW_COUNT)
            self.state = 1761
            self.an_rest_annotate_count_field()
            self.state = 1764
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==ZmeiLangParser.KW_AS:
                self.state = 1762
                self.match(ZmeiLangParser.KW_AS)
                self.state = 1763
                self.an_rest_annotate_count_alias()


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class An_rest_annotate_count_fieldContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def id_or_kw(self):
            return self.getTypedRuleContext(ZmeiLangParser.Id_or_kwContext,0)


        def getRuleIndex(self):
            return ZmeiLangParser.RULE_an_rest_annotate_count_field

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAn_rest_annotate_count_field" ):
                listener.enterAn_rest_annotate_count_field(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAn_rest_annotate_count_field" ):
                listener.exitAn_rest_annotate_count_field(self)




    def an_rest_annotate_count_field(self):

        localctx = ZmeiLangParser.An_rest_annotate_count_fieldContext(self, self._ctx, self.state)
        self.enterRule(localctx, 320, self.RULE_an_rest_annotate_count_field)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1766
            self.id_or_kw()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class An_rest_annotate_count_aliasContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def id_or_kw(self):
            return self.getTypedRuleContext(ZmeiLangParser.Id_or_kwContext,0)


        def getRuleIndex(self):
            return ZmeiLangParser.RULE_an_rest_annotate_count_alias

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAn_rest_annotate_count_alias" ):
                listener.enterAn_rest_annotate_count_alias(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAn_rest_annotate_count_alias" ):
                listener.exitAn_rest_annotate_count_alias(self)




    def an_rest_annotate_count_alias(self):

        localctx = ZmeiLangParser.An_rest_annotate_count_aliasContext(self, self._ctx, self.state)
        self.enterRule(localctx, 322, self.RULE_an_rest_annotate_count_alias)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1768
            self.id_or_kw()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class An_rest_inlineContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def KW_INLINE(self):
            return self.getToken(ZmeiLangParser.KW_INLINE, 0)

        def COLON(self):
            return self.getToken(ZmeiLangParser.COLON, 0)

        def an_rest_inline_decl(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(ZmeiLangParser.An_rest_inline_declContext)
            else:
                return self.getTypedRuleContext(ZmeiLangParser.An_rest_inline_declContext,i)


        def COMA(self, i:int=None):
            if i is None:
                return self.getTokens(ZmeiLangParser.COMA)
            else:
                return self.getToken(ZmeiLangParser.COMA, i)

        def NL(self, i:int=None):
            if i is None:
                return self.getTokens(ZmeiLangParser.NL)
            else:
                return self.getToken(ZmeiLangParser.NL, i)

        def getRuleIndex(self):
            return ZmeiLangParser.RULE_an_rest_inline

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAn_rest_inline" ):
                listener.enterAn_rest_inline(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAn_rest_inline" ):
                listener.exitAn_rest_inline(self)




    def an_rest_inline(self):

        localctx = ZmeiLangParser.An_rest_inlineContext(self, self._ctx, self.state)
        self.enterRule(localctx, 324, self.RULE_an_rest_inline)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1770
            self.match(ZmeiLangParser.KW_INLINE)
            self.state = 1771
            self.match(ZmeiLangParser.COLON)
            self.state = 1775 
            self._errHandler.sync(self)
            _alt = 1
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt == 1:
                    self.state = 1775
                    self._errHandler.sync(self)
                    token = self._input.LA(1)
                    if token in [ZmeiLangParser.KW_AUTH_TYPE_BASIC, ZmeiLangParser.KW_AUTH_TYPE_SESSION, ZmeiLangParser.KW_AUTH_TYPE_TOKEN, ZmeiLangParser.COL_FIELD_TYPE_LONGTEXT, ZmeiLangParser.COL_FIELD_TYPE_HTML, ZmeiLangParser.COL_FIELD_TYPE_HTML_MEDIA, ZmeiLangParser.COL_FIELD_TYPE_FLOAT, ZmeiLangParser.COL_FIELD_TYPE_DECIMAL, ZmeiLangParser.COL_FIELD_TYPE_DATE, ZmeiLangParser.COL_FIELD_TYPE_DATETIME, ZmeiLangParser.COL_FIELD_TYPE_CREATE_TIME, ZmeiLangParser.COL_FIELD_TYPE_UPDATE_TIME, ZmeiLangParser.COL_FIELD_TYPE_IMAGE, ZmeiLangParser.COL_FIELD_TYPE_FILE, ZmeiLangParser.COL_FIELD_TYPE_FILER_IMAGE, ZmeiLangParser.COL_FIELD_TYPE_FILER_FILE, ZmeiLangParser.COL_FIELD_TYPE_FILER_FOLDER, ZmeiLangParser.COL_FIELD_TYPE_FILER_IMAGE_FOLDER, ZmeiLangParser.COL_FIELD_TYPE_TEXT, ZmeiLangParser.COL_FIELD_TYPE_INT, ZmeiLangParser.COL_FIELD_TYPE_SLUG, ZmeiLangParser.COL_FIELD_TYPE_BOOL, ZmeiLangParser.COL_FIELD_TYPE_ONE, ZmeiLangParser.COL_FIELD_TYPE_ONE2ONE, ZmeiLangParser.COL_FIELD_TYPE_MANY, ZmeiLangParser.COL_FIELD_CHOICES, ZmeiLangParser.KW_THEME, ZmeiLangParser.KW_INSTALL, ZmeiLangParser.KW_HEADER, ZmeiLangParser.KW_SERVICES, ZmeiLangParser.KW_SELENIUM_PYTEST, ZmeiLangParser.KW_CHILD, ZmeiLangParser.KW_FILTER_OUT, ZmeiLangParser.KW_FILTER_IN, ZmeiLangParser.KW_PAGE, ZmeiLangParser.KW_LINK_SUFFIX, ZmeiLangParser.KW_URL_PREFIX, ZmeiLangParser.KW_CAN_EDIT, ZmeiLangParser.KW_OBJECT_EXPR, ZmeiLangParser.KW_BLOCK, ZmeiLangParser.KW_ITEM_NAME, ZmeiLangParser.KW_PK_PARAM, ZmeiLangParser.KW_LIST_FIELDS, ZmeiLangParser.KW_DELETE, ZmeiLangParser.KW_EDIT, ZmeiLangParser.KW_CREATE, ZmeiLangParser.KW_DETAIL, ZmeiLangParser.KW_SKIP, ZmeiLangParser.KW_FROM, ZmeiLangParser.KW_POLY_LIST, ZmeiLangParser.KW_CSS, ZmeiLangParser.KW_JS, ZmeiLangParser.KW_INLINE_TYPE_TABULAR, ZmeiLangParser.KW_INLINE_TYPE_STACKED, ZmeiLangParser.KW_INLINE_TYPE_POLYMORPHIC, ZmeiLangParser.KW_INLINE, ZmeiLangParser.KW_TYPE, ZmeiLangParser.KW_USER_FIELD, ZmeiLangParser.KW_ANNOTATE, ZmeiLangParser.KW_ON_CREATE, ZmeiLangParser.KW_QUERY, ZmeiLangParser.KW_AUTH, ZmeiLangParser.KW_COUNT, ZmeiLangParser.KW_I18N, ZmeiLangParser.KW_EXTENSION, ZmeiLangParser.KW_TABS, ZmeiLangParser.KW_LIST, ZmeiLangParser.KW_READ_ONLY, ZmeiLangParser.KW_LIST_EDITABLE, ZmeiLangParser.KW_LIST_FILTER, ZmeiLangParser.KW_LIST_SEARCH, ZmeiLangParser.KW_FIELDS, ZmeiLangParser.KW_IMPORT, ZmeiLangParser.KW_AS, ZmeiLangParser.WRITE_MODE, ZmeiLangParser.BOOL, ZmeiLangParser.ID]:
                        self.state = 1772
                        self.an_rest_inline_decl()
                        pass
                    elif token in [ZmeiLangParser.COMA]:
                        self.state = 1773
                        self.match(ZmeiLangParser.COMA)
                        pass
                    elif token in [ZmeiLangParser.NL]:
                        self.state = 1774
                        self.match(ZmeiLangParser.NL)
                        pass
                    else:
                        raise NoViableAltException(self)


                else:
                    raise NoViableAltException(self)
                self.state = 1777 
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,168,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class An_rest_inline_declContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def an_rest_inline_name(self):
            return self.getTypedRuleContext(ZmeiLangParser.An_rest_inline_nameContext,0)


        def BRACE_OPEN(self):
            return self.getToken(ZmeiLangParser.BRACE_OPEN, 0)

        def an_rest_config(self):
            return self.getTypedRuleContext(ZmeiLangParser.An_rest_configContext,0)


        def BRACE_CLOSE(self):
            return self.getToken(ZmeiLangParser.BRACE_CLOSE, 0)

        def getRuleIndex(self):
            return ZmeiLangParser.RULE_an_rest_inline_decl

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAn_rest_inline_decl" ):
                listener.enterAn_rest_inline_decl(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAn_rest_inline_decl" ):
                listener.exitAn_rest_inline_decl(self)




    def an_rest_inline_decl(self):

        localctx = ZmeiLangParser.An_rest_inline_declContext(self, self._ctx, self.state)
        self.enterRule(localctx, 326, self.RULE_an_rest_inline_decl)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1779
            self.an_rest_inline_name()
            self.state = 1780
            self.match(ZmeiLangParser.BRACE_OPEN)
            self.state = 1781
            self.an_rest_config()
            self.state = 1782
            self.match(ZmeiLangParser.BRACE_CLOSE)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class An_rest_inline_nameContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def id_or_kw(self):
            return self.getTypedRuleContext(ZmeiLangParser.Id_or_kwContext,0)


        def getRuleIndex(self):
            return ZmeiLangParser.RULE_an_rest_inline_name

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAn_rest_inline_name" ):
                listener.enterAn_rest_inline_name(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAn_rest_inline_name" ):
                listener.exitAn_rest_inline_name(self)




    def an_rest_inline_name(self):

        localctx = ZmeiLangParser.An_rest_inline_nameContext(self, self._ctx, self.state)
        self.enterRule(localctx, 328, self.RULE_an_rest_inline_name)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1784
            self.id_or_kw()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class An_orderContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def AN_ORDER(self):
            return self.getToken(ZmeiLangParser.AN_ORDER, 0)

        def BRACE_OPEN(self):
            return self.getToken(ZmeiLangParser.BRACE_OPEN, 0)

        def an_order_fields(self):
            return self.getTypedRuleContext(ZmeiLangParser.An_order_fieldsContext,0)


        def BRACE_CLOSE(self):
            return self.getToken(ZmeiLangParser.BRACE_CLOSE, 0)

        def getRuleIndex(self):
            return ZmeiLangParser.RULE_an_order

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAn_order" ):
                listener.enterAn_order(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAn_order" ):
                listener.exitAn_order(self)




    def an_order(self):

        localctx = ZmeiLangParser.An_orderContext(self, self._ctx, self.state)
        self.enterRule(localctx, 330, self.RULE_an_order)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1786
            self.match(ZmeiLangParser.AN_ORDER)
            self.state = 1787
            self.match(ZmeiLangParser.BRACE_OPEN)
            self.state = 1788
            self.an_order_fields()
            self.state = 1789
            self.match(ZmeiLangParser.BRACE_CLOSE)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class An_order_fieldsContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def id_or_kw(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(ZmeiLangParser.Id_or_kwContext)
            else:
                return self.getTypedRuleContext(ZmeiLangParser.Id_or_kwContext,i)


        def COMA(self, i:int=None):
            if i is None:
                return self.getTokens(ZmeiLangParser.COMA)
            else:
                return self.getToken(ZmeiLangParser.COMA, i)

        def getRuleIndex(self):
            return ZmeiLangParser.RULE_an_order_fields

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAn_order_fields" ):
                listener.enterAn_order_fields(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAn_order_fields" ):
                listener.exitAn_order_fields(self)




    def an_order_fields(self):

        localctx = ZmeiLangParser.An_order_fieldsContext(self, self._ctx, self.state)
        self.enterRule(localctx, 332, self.RULE_an_order_fields)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1791
            self.id_or_kw()
            self.state = 1796
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==ZmeiLangParser.COMA:
                self.state = 1792
                self.match(ZmeiLangParser.COMA)
                self.state = 1793
                self.id_or_kw()
                self.state = 1798
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class An_cleanContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def AN_CLEAN(self):
            return self.getToken(ZmeiLangParser.AN_CLEAN, 0)

        def python_code(self):
            return self.getTypedRuleContext(ZmeiLangParser.Python_codeContext,0)


        def getRuleIndex(self):
            return ZmeiLangParser.RULE_an_clean

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAn_clean" ):
                listener.enterAn_clean(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAn_clean" ):
                listener.exitAn_clean(self)




    def an_clean(self):

        localctx = ZmeiLangParser.An_cleanContext(self, self._ctx, self.state)
        self.enterRule(localctx, 334, self.RULE_an_clean)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1799
            self.match(ZmeiLangParser.AN_CLEAN)
            self.state = 1800
            self.python_code()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class An_pre_deleteContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def AN_PRE_DELETE(self):
            return self.getToken(ZmeiLangParser.AN_PRE_DELETE, 0)

        def python_code(self):
            return self.getTypedRuleContext(ZmeiLangParser.Python_codeContext,0)


        def getRuleIndex(self):
            return ZmeiLangParser.RULE_an_pre_delete

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAn_pre_delete" ):
                listener.enterAn_pre_delete(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAn_pre_delete" ):
                listener.exitAn_pre_delete(self)




    def an_pre_delete(self):

        localctx = ZmeiLangParser.An_pre_deleteContext(self, self._ctx, self.state)
        self.enterRule(localctx, 336, self.RULE_an_pre_delete)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1802
            self.match(ZmeiLangParser.AN_PRE_DELETE)
            self.state = 1803
            self.python_code()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class An_treeContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def AN_TREE(self):
            return self.getToken(ZmeiLangParser.AN_TREE, 0)

        def BRACE_OPEN(self):
            return self.getToken(ZmeiLangParser.BRACE_OPEN, 0)

        def an_tree_poly(self):
            return self.getTypedRuleContext(ZmeiLangParser.An_tree_polyContext,0)


        def BRACE_CLOSE(self):
            return self.getToken(ZmeiLangParser.BRACE_CLOSE, 0)

        def getRuleIndex(self):
            return ZmeiLangParser.RULE_an_tree

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAn_tree" ):
                listener.enterAn_tree(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAn_tree" ):
                listener.exitAn_tree(self)




    def an_tree(self):

        localctx = ZmeiLangParser.An_treeContext(self, self._ctx, self.state)
        self.enterRule(localctx, 338, self.RULE_an_tree)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1805
            self.match(ZmeiLangParser.AN_TREE)
            self.state = 1810
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==ZmeiLangParser.BRACE_OPEN:
                self.state = 1806
                self.match(ZmeiLangParser.BRACE_OPEN)
                self.state = 1807
                self.an_tree_poly()
                self.state = 1808
                self.match(ZmeiLangParser.BRACE_CLOSE)


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class An_tree_polyContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def KW_POLY_LIST(self):
            return self.getToken(ZmeiLangParser.KW_POLY_LIST, 0)

        def getRuleIndex(self):
            return ZmeiLangParser.RULE_an_tree_poly

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAn_tree_poly" ):
                listener.enterAn_tree_poly(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAn_tree_poly" ):
                listener.exitAn_tree_poly(self)




    def an_tree_poly(self):

        localctx = ZmeiLangParser.An_tree_polyContext(self, self._ctx, self.state)
        self.enterRule(localctx, 340, self.RULE_an_tree_poly)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1812
            self.match(ZmeiLangParser.KW_POLY_LIST)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class An_mixinContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def AN_MIXIN(self):
            return self.getToken(ZmeiLangParser.AN_MIXIN, 0)

        def BRACE_OPEN(self):
            return self.getToken(ZmeiLangParser.BRACE_OPEN, 0)

        def classname(self):
            return self.getTypedRuleContext(ZmeiLangParser.ClassnameContext,0)


        def BRACE_CLOSE(self):
            return self.getToken(ZmeiLangParser.BRACE_CLOSE, 0)

        def getRuleIndex(self):
            return ZmeiLangParser.RULE_an_mixin

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAn_mixin" ):
                listener.enterAn_mixin(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAn_mixin" ):
                listener.exitAn_mixin(self)




    def an_mixin(self):

        localctx = ZmeiLangParser.An_mixinContext(self, self._ctx, self.state)
        self.enterRule(localctx, 342, self.RULE_an_mixin)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1814
            self.match(ZmeiLangParser.AN_MIXIN)

            self.state = 1815
            self.match(ZmeiLangParser.BRACE_OPEN)
            self.state = 1816
            self.classname()
            self.state = 1817
            self.match(ZmeiLangParser.BRACE_CLOSE)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class An_date_treeContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def AN_DATE_TREE(self):
            return self.getToken(ZmeiLangParser.AN_DATE_TREE, 0)

        def BRACE_OPEN(self):
            return self.getToken(ZmeiLangParser.BRACE_OPEN, 0)

        def an_date_tree_field(self):
            return self.getTypedRuleContext(ZmeiLangParser.An_date_tree_fieldContext,0)


        def BRACE_CLOSE(self):
            return self.getToken(ZmeiLangParser.BRACE_CLOSE, 0)

        def getRuleIndex(self):
            return ZmeiLangParser.RULE_an_date_tree

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAn_date_tree" ):
                listener.enterAn_date_tree(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAn_date_tree" ):
                listener.exitAn_date_tree(self)




    def an_date_tree(self):

        localctx = ZmeiLangParser.An_date_treeContext(self, self._ctx, self.state)
        self.enterRule(localctx, 344, self.RULE_an_date_tree)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1819
            self.match(ZmeiLangParser.AN_DATE_TREE)

            self.state = 1820
            self.match(ZmeiLangParser.BRACE_OPEN)
            self.state = 1821
            self.an_date_tree_field()
            self.state = 1822
            self.match(ZmeiLangParser.BRACE_CLOSE)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class An_date_tree_fieldContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def id_or_kw(self):
            return self.getTypedRuleContext(ZmeiLangParser.Id_or_kwContext,0)


        def getRuleIndex(self):
            return ZmeiLangParser.RULE_an_date_tree_field

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAn_date_tree_field" ):
                listener.enterAn_date_tree_field(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAn_date_tree_field" ):
                listener.exitAn_date_tree_field(self)




    def an_date_tree_field(self):

        localctx = ZmeiLangParser.An_date_tree_fieldContext(self, self._ctx, self.state)
        self.enterRule(localctx, 346, self.RULE_an_date_tree_field)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1824
            self.id_or_kw()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class An_m2m_changedContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def AN_M2M_CHANGED(self):
            return self.getToken(ZmeiLangParser.AN_M2M_CHANGED, 0)

        def python_code(self):
            return self.getTypedRuleContext(ZmeiLangParser.Python_codeContext,0)


        def getRuleIndex(self):
            return ZmeiLangParser.RULE_an_m2m_changed

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAn_m2m_changed" ):
                listener.enterAn_m2m_changed(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAn_m2m_changed" ):
                listener.exitAn_m2m_changed(self)




    def an_m2m_changed(self):

        localctx = ZmeiLangParser.An_m2m_changedContext(self, self._ctx, self.state)
        self.enterRule(localctx, 348, self.RULE_an_m2m_changed)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1826
            self.match(ZmeiLangParser.AN_M2M_CHANGED)
            self.state = 1827
            self.python_code()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class An_post_saveContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def AN_POST_SAVE(self):
            return self.getToken(ZmeiLangParser.AN_POST_SAVE, 0)

        def python_code(self):
            return self.getTypedRuleContext(ZmeiLangParser.Python_codeContext,0)


        def getRuleIndex(self):
            return ZmeiLangParser.RULE_an_post_save

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAn_post_save" ):
                listener.enterAn_post_save(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAn_post_save" ):
                listener.exitAn_post_save(self)




    def an_post_save(self):

        localctx = ZmeiLangParser.An_post_saveContext(self, self._ctx, self.state)
        self.enterRule(localctx, 350, self.RULE_an_post_save)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1829
            self.match(ZmeiLangParser.AN_POST_SAVE)
            self.state = 1830
            self.python_code()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class An_pre_saveContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def AN_PRE_SAVE(self):
            return self.getToken(ZmeiLangParser.AN_PRE_SAVE, 0)

        def python_code(self):
            return self.getTypedRuleContext(ZmeiLangParser.Python_codeContext,0)


        def getRuleIndex(self):
            return ZmeiLangParser.RULE_an_pre_save

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAn_pre_save" ):
                listener.enterAn_pre_save(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAn_pre_save" ):
                listener.exitAn_pre_save(self)




    def an_pre_save(self):

        localctx = ZmeiLangParser.An_pre_saveContext(self, self._ctx, self.state)
        self.enterRule(localctx, 352, self.RULE_an_pre_save)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1832
            self.match(ZmeiLangParser.AN_PRE_SAVE)
            self.state = 1833
            self.python_code()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class An_post_deleteContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def AN_POST_DELETE(self):
            return self.getToken(ZmeiLangParser.AN_POST_DELETE, 0)

        def python_code(self):
            return self.getTypedRuleContext(ZmeiLangParser.Python_codeContext,0)


        def getRuleIndex(self):
            return ZmeiLangParser.RULE_an_post_delete

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAn_post_delete" ):
                listener.enterAn_post_delete(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAn_post_delete" ):
                listener.exitAn_post_delete(self)




    def an_post_delete(self):

        localctx = ZmeiLangParser.An_post_deleteContext(self, self._ctx, self.state)
        self.enterRule(localctx, 354, self.RULE_an_post_delete)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1835
            self.match(ZmeiLangParser.AN_POST_DELETE)
            self.state = 1836
            self.python_code()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class An_sortableContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def AN_SORTABLE(self):
            return self.getToken(ZmeiLangParser.AN_SORTABLE, 0)

        def BRACE_OPEN(self):
            return self.getToken(ZmeiLangParser.BRACE_OPEN, 0)

        def an_sortable_field_name(self):
            return self.getTypedRuleContext(ZmeiLangParser.An_sortable_field_nameContext,0)


        def BRACE_CLOSE(self):
            return self.getToken(ZmeiLangParser.BRACE_CLOSE, 0)

        def getRuleIndex(self):
            return ZmeiLangParser.RULE_an_sortable

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAn_sortable" ):
                listener.enterAn_sortable(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAn_sortable" ):
                listener.exitAn_sortable(self)




    def an_sortable(self):

        localctx = ZmeiLangParser.An_sortableContext(self, self._ctx, self.state)
        self.enterRule(localctx, 356, self.RULE_an_sortable)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1838
            self.match(ZmeiLangParser.AN_SORTABLE)
            self.state = 1839
            self.match(ZmeiLangParser.BRACE_OPEN)
            self.state = 1840
            self.an_sortable_field_name()
            self.state = 1841
            self.match(ZmeiLangParser.BRACE_CLOSE)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class An_sortable_field_nameContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def id_or_kw(self):
            return self.getTypedRuleContext(ZmeiLangParser.Id_or_kwContext,0)


        def getRuleIndex(self):
            return ZmeiLangParser.RULE_an_sortable_field_name

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAn_sortable_field_name" ):
                listener.enterAn_sortable_field_name(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAn_sortable_field_name" ):
                listener.exitAn_sortable_field_name(self)




    def an_sortable_field_name(self):

        localctx = ZmeiLangParser.An_sortable_field_nameContext(self, self._ctx, self.state)
        self.enterRule(localctx, 358, self.RULE_an_sortable_field_name)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1843
            self.id_or_kw()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class PageContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def page_header(self):
            return self.getTypedRuleContext(ZmeiLangParser.Page_headerContext,0)


        def page_body(self):
            return self.getTypedRuleContext(ZmeiLangParser.Page_bodyContext,0)


        def NL(self, i:int=None):
            if i is None:
                return self.getTokens(ZmeiLangParser.NL)
            else:
                return self.getToken(ZmeiLangParser.NL, i)

        def getRuleIndex(self):
            return ZmeiLangParser.RULE_page

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPage" ):
                listener.enterPage(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPage" ):
                listener.exitPage(self)




    def page(self):

        localctx = ZmeiLangParser.PageContext(self, self._ctx, self.state)
        self.enterRule(localctx, 360, self.RULE_page)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1845
            self.page_header()
            self.state = 1849
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,171,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 1846
                    self.match(ZmeiLangParser.NL) 
                self.state = 1851
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,171,self._ctx)

            self.state = 1852
            self.page_body()
            self.state = 1856
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,172,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 1853
                    self.match(ZmeiLangParser.NL) 
                self.state = 1858
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,172,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Page_headerContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def SQ_BRACE_OPEN(self):
            return self.getToken(ZmeiLangParser.SQ_BRACE_OPEN, 0)

        def page_name(self):
            return self.getTypedRuleContext(ZmeiLangParser.Page_nameContext,0)


        def SQ_BRACE_CLOSE(self):
            return self.getToken(ZmeiLangParser.SQ_BRACE_CLOSE, 0)

        def page_base(self):
            return self.getTypedRuleContext(ZmeiLangParser.Page_baseContext,0)


        def page_alias(self):
            return self.getTypedRuleContext(ZmeiLangParser.Page_aliasContext,0)


        def COLON(self, i:int=None):
            if i is None:
                return self.getTokens(ZmeiLangParser.COLON)
            else:
                return self.getToken(ZmeiLangParser.COLON, i)

        def NL(self):
            return self.getToken(ZmeiLangParser.NL, 0)

        def page_url(self):
            return self.getTypedRuleContext(ZmeiLangParser.Page_urlContext,0)


        def page_template(self):
            return self.getTypedRuleContext(ZmeiLangParser.Page_templateContext,0)


        def getRuleIndex(self):
            return ZmeiLangParser.RULE_page_header

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPage_header" ):
                listener.enterPage_header(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPage_header" ):
                listener.exitPage_header(self)




    def page_header(self):

        localctx = ZmeiLangParser.Page_headerContext(self, self._ctx, self.state)
        self.enterRule(localctx, 362, self.RULE_page_header)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1859
            self.match(ZmeiLangParser.SQ_BRACE_OPEN)
            self.state = 1861
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,173,self._ctx)
            if la_ == 1:
                self.state = 1860
                self.page_base()


            self.state = 1863
            self.page_name()
            self.state = 1865
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==ZmeiLangParser.KW_AS:
                self.state = 1864
                self.page_alias()


            self.state = 1875
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==ZmeiLangParser.COLON:
                self.state = 1867
                self.match(ZmeiLangParser.COLON)
                self.state = 1869
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if ((((_la - 134)) & ~0x3f) == 0 and ((1 << (_la - 134)) & ((1 << (ZmeiLangParser.DOT - 134)) | (1 << (ZmeiLangParser.SLASH - 134)) | (1 << (ZmeiLangParser.DOLLAR - 134)))) != 0):
                    self.state = 1868
                    self.page_url()


                self.state = 1873
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==ZmeiLangParser.COLON:
                    self.state = 1871
                    self.match(ZmeiLangParser.COLON)
                    self.state = 1872
                    self.page_template()




            self.state = 1877
            self.match(ZmeiLangParser.SQ_BRACE_CLOSE)
            self.state = 1879
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,178,self._ctx)
            if la_ == 1:
                self.state = 1878
                self.match(ZmeiLangParser.NL)


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Page_baseContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def id_or_kw(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(ZmeiLangParser.Id_or_kwContext)
            else:
                return self.getTypedRuleContext(ZmeiLangParser.Id_or_kwContext,i)


        def GT(self):
            return self.getToken(ZmeiLangParser.GT, 0)

        def DASH(self):
            return self.getToken(ZmeiLangParser.DASH, 0)

        def APPROX(self):
            return self.getToken(ZmeiLangParser.APPROX, 0)

        def DOT(self):
            return self.getToken(ZmeiLangParser.DOT, 0)

        def getRuleIndex(self):
            return ZmeiLangParser.RULE_page_base

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPage_base" ):
                listener.enterPage_base(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPage_base" ):
                listener.exitPage_base(self)




    def page_base(self):

        localctx = ZmeiLangParser.Page_baseContext(self, self._ctx, self.state)
        self.enterRule(localctx, 364, self.RULE_page_base)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1884
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,179,self._ctx)
            if la_ == 1:
                self.state = 1881
                self.id_or_kw()
                self.state = 1882
                self.match(ZmeiLangParser.DOT)


            self.state = 1886
            self.id_or_kw()
            self.state = 1887
            _la = self._input.LA(1)
            if not(_la==ZmeiLangParser.DASH or _la==ZmeiLangParser.APPROX):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
            self.state = 1888
            self.match(ZmeiLangParser.GT)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Page_aliasContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def KW_AS(self):
            return self.getToken(ZmeiLangParser.KW_AS, 0)

        def page_alias_name(self):
            return self.getTypedRuleContext(ZmeiLangParser.Page_alias_nameContext,0)


        def getRuleIndex(self):
            return ZmeiLangParser.RULE_page_alias

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPage_alias" ):
                listener.enterPage_alias(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPage_alias" ):
                listener.exitPage_alias(self)




    def page_alias(self):

        localctx = ZmeiLangParser.Page_aliasContext(self, self._ctx, self.state)
        self.enterRule(localctx, 366, self.RULE_page_alias)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1890
            self.match(ZmeiLangParser.KW_AS)
            self.state = 1891
            self.page_alias_name()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Page_alias_nameContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def id_or_kw(self):
            return self.getTypedRuleContext(ZmeiLangParser.Id_or_kwContext,0)


        def getRuleIndex(self):
            return ZmeiLangParser.RULE_page_alias_name

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPage_alias_name" ):
                listener.enterPage_alias_name(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPage_alias_name" ):
                listener.exitPage_alias_name(self)




    def page_alias_name(self):

        localctx = ZmeiLangParser.Page_alias_nameContext(self, self._ctx, self.state)
        self.enterRule(localctx, 368, self.RULE_page_alias_name)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1893
            self.id_or_kw()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Page_templateContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def template_name(self):
            return self.getTypedRuleContext(ZmeiLangParser.Template_nameContext,0)


        def python_code(self):
            return self.getTypedRuleContext(ZmeiLangParser.Python_codeContext,0)


        def getRuleIndex(self):
            return ZmeiLangParser.RULE_page_template

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPage_template" ):
                listener.enterPage_template(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPage_template" ):
                listener.exitPage_template(self)




    def page_template(self):

        localctx = ZmeiLangParser.Page_templateContext(self, self._ctx, self.state)
        self.enterRule(localctx, 370, self.RULE_page_template)
        try:
            self.state = 1897
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [ZmeiLangParser.KW_AUTH_TYPE_BASIC, ZmeiLangParser.KW_AUTH_TYPE_SESSION, ZmeiLangParser.KW_AUTH_TYPE_TOKEN, ZmeiLangParser.COL_FIELD_TYPE_LONGTEXT, ZmeiLangParser.COL_FIELD_TYPE_HTML, ZmeiLangParser.COL_FIELD_TYPE_HTML_MEDIA, ZmeiLangParser.COL_FIELD_TYPE_FLOAT, ZmeiLangParser.COL_FIELD_TYPE_DECIMAL, ZmeiLangParser.COL_FIELD_TYPE_DATE, ZmeiLangParser.COL_FIELD_TYPE_DATETIME, ZmeiLangParser.COL_FIELD_TYPE_CREATE_TIME, ZmeiLangParser.COL_FIELD_TYPE_UPDATE_TIME, ZmeiLangParser.COL_FIELD_TYPE_IMAGE, ZmeiLangParser.COL_FIELD_TYPE_FILE, ZmeiLangParser.COL_FIELD_TYPE_FILER_IMAGE, ZmeiLangParser.COL_FIELD_TYPE_FILER_FILE, ZmeiLangParser.COL_FIELD_TYPE_FILER_FOLDER, ZmeiLangParser.COL_FIELD_TYPE_FILER_IMAGE_FOLDER, ZmeiLangParser.COL_FIELD_TYPE_TEXT, ZmeiLangParser.COL_FIELD_TYPE_INT, ZmeiLangParser.COL_FIELD_TYPE_SLUG, ZmeiLangParser.COL_FIELD_TYPE_BOOL, ZmeiLangParser.COL_FIELD_TYPE_ONE, ZmeiLangParser.COL_FIELD_TYPE_ONE2ONE, ZmeiLangParser.COL_FIELD_TYPE_MANY, ZmeiLangParser.COL_FIELD_CHOICES, ZmeiLangParser.KW_THEME, ZmeiLangParser.KW_INSTALL, ZmeiLangParser.KW_HEADER, ZmeiLangParser.KW_SERVICES, ZmeiLangParser.KW_SELENIUM_PYTEST, ZmeiLangParser.KW_CHILD, ZmeiLangParser.KW_FILTER_OUT, ZmeiLangParser.KW_FILTER_IN, ZmeiLangParser.KW_PAGE, ZmeiLangParser.KW_LINK_SUFFIX, ZmeiLangParser.KW_URL_PREFIX, ZmeiLangParser.KW_CAN_EDIT, ZmeiLangParser.KW_OBJECT_EXPR, ZmeiLangParser.KW_BLOCK, ZmeiLangParser.KW_ITEM_NAME, ZmeiLangParser.KW_PK_PARAM, ZmeiLangParser.KW_LIST_FIELDS, ZmeiLangParser.KW_DELETE, ZmeiLangParser.KW_EDIT, ZmeiLangParser.KW_CREATE, ZmeiLangParser.KW_DETAIL, ZmeiLangParser.KW_SKIP, ZmeiLangParser.KW_FROM, ZmeiLangParser.KW_POLY_LIST, ZmeiLangParser.KW_CSS, ZmeiLangParser.KW_JS, ZmeiLangParser.KW_INLINE_TYPE_TABULAR, ZmeiLangParser.KW_INLINE_TYPE_STACKED, ZmeiLangParser.KW_INLINE_TYPE_POLYMORPHIC, ZmeiLangParser.KW_INLINE, ZmeiLangParser.KW_TYPE, ZmeiLangParser.KW_USER_FIELD, ZmeiLangParser.KW_ANNOTATE, ZmeiLangParser.KW_ON_CREATE, ZmeiLangParser.KW_QUERY, ZmeiLangParser.KW_AUTH, ZmeiLangParser.KW_COUNT, ZmeiLangParser.KW_I18N, ZmeiLangParser.KW_EXTENSION, ZmeiLangParser.KW_TABS, ZmeiLangParser.KW_LIST, ZmeiLangParser.KW_READ_ONLY, ZmeiLangParser.KW_LIST_EDITABLE, ZmeiLangParser.KW_LIST_FILTER, ZmeiLangParser.KW_LIST_SEARCH, ZmeiLangParser.KW_FIELDS, ZmeiLangParser.KW_IMPORT, ZmeiLangParser.KW_AS, ZmeiLangParser.WRITE_MODE, ZmeiLangParser.BOOL, ZmeiLangParser.ID, ZmeiLangParser.DIGIT, ZmeiLangParser.UNDERSCORE, ZmeiLangParser.DASH, ZmeiLangParser.DOT]:
                self.enterOuterAlt(localctx, 1)
                self.state = 1895
                self.template_name()
                pass
            elif token in [ZmeiLangParser.ASSIGN, ZmeiLangParser.CODE_BLOCK]:
                self.enterOuterAlt(localctx, 2)
                self.state = 1896
                self.python_code()
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Template_nameContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def file_name_part(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(ZmeiLangParser.File_name_partContext)
            else:
                return self.getTypedRuleContext(ZmeiLangParser.File_name_partContext,i)


        def SLASH(self, i:int=None):
            if i is None:
                return self.getTokens(ZmeiLangParser.SLASH)
            else:
                return self.getToken(ZmeiLangParser.SLASH, i)

        def getRuleIndex(self):
            return ZmeiLangParser.RULE_template_name

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterTemplate_name" ):
                listener.enterTemplate_name(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitTemplate_name" ):
                listener.exitTemplate_name(self)




    def template_name(self):

        localctx = ZmeiLangParser.Template_nameContext(self, self._ctx, self.state)
        self.enterRule(localctx, 372, self.RULE_template_name)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1899
            self.file_name_part()
            self.state = 1904
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==ZmeiLangParser.SLASH:
                self.state = 1900
                self.match(ZmeiLangParser.SLASH)
                self.state = 1901
                self.file_name_part()
                self.state = 1906
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class File_name_partContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def id_or_kw(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(ZmeiLangParser.Id_or_kwContext)
            else:
                return self.getTypedRuleContext(ZmeiLangParser.Id_or_kwContext,i)


        def DIGIT(self, i:int=None):
            if i is None:
                return self.getTokens(ZmeiLangParser.DIGIT)
            else:
                return self.getToken(ZmeiLangParser.DIGIT, i)

        def DASH(self, i:int=None):
            if i is None:
                return self.getTokens(ZmeiLangParser.DASH)
            else:
                return self.getToken(ZmeiLangParser.DASH, i)

        def UNDERSCORE(self, i:int=None):
            if i is None:
                return self.getTokens(ZmeiLangParser.UNDERSCORE)
            else:
                return self.getToken(ZmeiLangParser.UNDERSCORE, i)

        def DOT(self, i:int=None):
            if i is None:
                return self.getTokens(ZmeiLangParser.DOT)
            else:
                return self.getToken(ZmeiLangParser.DOT, i)

        def getRuleIndex(self):
            return ZmeiLangParser.RULE_file_name_part

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterFile_name_part" ):
                listener.enterFile_name_part(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitFile_name_part" ):
                listener.exitFile_name_part(self)




    def file_name_part(self):

        localctx = ZmeiLangParser.File_name_partContext(self, self._ctx, self.state)
        self.enterRule(localctx, 374, self.RULE_file_name_part)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1912 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 1912
                self._errHandler.sync(self)
                token = self._input.LA(1)
                if token in [ZmeiLangParser.KW_AUTH_TYPE_BASIC, ZmeiLangParser.KW_AUTH_TYPE_SESSION, ZmeiLangParser.KW_AUTH_TYPE_TOKEN, ZmeiLangParser.COL_FIELD_TYPE_LONGTEXT, ZmeiLangParser.COL_FIELD_TYPE_HTML, ZmeiLangParser.COL_FIELD_TYPE_HTML_MEDIA, ZmeiLangParser.COL_FIELD_TYPE_FLOAT, ZmeiLangParser.COL_FIELD_TYPE_DECIMAL, ZmeiLangParser.COL_FIELD_TYPE_DATE, ZmeiLangParser.COL_FIELD_TYPE_DATETIME, ZmeiLangParser.COL_FIELD_TYPE_CREATE_TIME, ZmeiLangParser.COL_FIELD_TYPE_UPDATE_TIME, ZmeiLangParser.COL_FIELD_TYPE_IMAGE, ZmeiLangParser.COL_FIELD_TYPE_FILE, ZmeiLangParser.COL_FIELD_TYPE_FILER_IMAGE, ZmeiLangParser.COL_FIELD_TYPE_FILER_FILE, ZmeiLangParser.COL_FIELD_TYPE_FILER_FOLDER, ZmeiLangParser.COL_FIELD_TYPE_FILER_IMAGE_FOLDER, ZmeiLangParser.COL_FIELD_TYPE_TEXT, ZmeiLangParser.COL_FIELD_TYPE_INT, ZmeiLangParser.COL_FIELD_TYPE_SLUG, ZmeiLangParser.COL_FIELD_TYPE_BOOL, ZmeiLangParser.COL_FIELD_TYPE_ONE, ZmeiLangParser.COL_FIELD_TYPE_ONE2ONE, ZmeiLangParser.COL_FIELD_TYPE_MANY, ZmeiLangParser.COL_FIELD_CHOICES, ZmeiLangParser.KW_THEME, ZmeiLangParser.KW_INSTALL, ZmeiLangParser.KW_HEADER, ZmeiLangParser.KW_SERVICES, ZmeiLangParser.KW_SELENIUM_PYTEST, ZmeiLangParser.KW_CHILD, ZmeiLangParser.KW_FILTER_OUT, ZmeiLangParser.KW_FILTER_IN, ZmeiLangParser.KW_PAGE, ZmeiLangParser.KW_LINK_SUFFIX, ZmeiLangParser.KW_URL_PREFIX, ZmeiLangParser.KW_CAN_EDIT, ZmeiLangParser.KW_OBJECT_EXPR, ZmeiLangParser.KW_BLOCK, ZmeiLangParser.KW_ITEM_NAME, ZmeiLangParser.KW_PK_PARAM, ZmeiLangParser.KW_LIST_FIELDS, ZmeiLangParser.KW_DELETE, ZmeiLangParser.KW_EDIT, ZmeiLangParser.KW_CREATE, ZmeiLangParser.KW_DETAIL, ZmeiLangParser.KW_SKIP, ZmeiLangParser.KW_FROM, ZmeiLangParser.KW_POLY_LIST, ZmeiLangParser.KW_CSS, ZmeiLangParser.KW_JS, ZmeiLangParser.KW_INLINE_TYPE_TABULAR, ZmeiLangParser.KW_INLINE_TYPE_STACKED, ZmeiLangParser.KW_INLINE_TYPE_POLYMORPHIC, ZmeiLangParser.KW_INLINE, ZmeiLangParser.KW_TYPE, ZmeiLangParser.KW_USER_FIELD, ZmeiLangParser.KW_ANNOTATE, ZmeiLangParser.KW_ON_CREATE, ZmeiLangParser.KW_QUERY, ZmeiLangParser.KW_AUTH, ZmeiLangParser.KW_COUNT, ZmeiLangParser.KW_I18N, ZmeiLangParser.KW_EXTENSION, ZmeiLangParser.KW_TABS, ZmeiLangParser.KW_LIST, ZmeiLangParser.KW_READ_ONLY, ZmeiLangParser.KW_LIST_EDITABLE, ZmeiLangParser.KW_LIST_FILTER, ZmeiLangParser.KW_LIST_SEARCH, ZmeiLangParser.KW_FIELDS, ZmeiLangParser.KW_IMPORT, ZmeiLangParser.KW_AS, ZmeiLangParser.WRITE_MODE, ZmeiLangParser.BOOL, ZmeiLangParser.ID]:
                    self.state = 1907
                    self.id_or_kw()
                    pass
                elif token in [ZmeiLangParser.DIGIT]:
                    self.state = 1908
                    self.match(ZmeiLangParser.DIGIT)
                    pass
                elif token in [ZmeiLangParser.DASH]:
                    self.state = 1909
                    self.match(ZmeiLangParser.DASH)
                    pass
                elif token in [ZmeiLangParser.UNDERSCORE]:
                    self.state = 1910
                    self.match(ZmeiLangParser.UNDERSCORE)
                    pass
                elif token in [ZmeiLangParser.DOT]:
                    self.state = 1911
                    self.match(ZmeiLangParser.DOT)
                    pass
                else:
                    raise NoViableAltException(self)

                self.state = 1914 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not (((((_la - 42)) & ~0x3f) == 0 and ((1 << (_la - 42)) & ((1 << (ZmeiLangParser.KW_AUTH_TYPE_BASIC - 42)) | (1 << (ZmeiLangParser.KW_AUTH_TYPE_SESSION - 42)) | (1 << (ZmeiLangParser.KW_AUTH_TYPE_TOKEN - 42)) | (1 << (ZmeiLangParser.COL_FIELD_TYPE_LONGTEXT - 42)) | (1 << (ZmeiLangParser.COL_FIELD_TYPE_HTML - 42)) | (1 << (ZmeiLangParser.COL_FIELD_TYPE_HTML_MEDIA - 42)) | (1 << (ZmeiLangParser.COL_FIELD_TYPE_FLOAT - 42)) | (1 << (ZmeiLangParser.COL_FIELD_TYPE_DECIMAL - 42)) | (1 << (ZmeiLangParser.COL_FIELD_TYPE_DATE - 42)) | (1 << (ZmeiLangParser.COL_FIELD_TYPE_DATETIME - 42)) | (1 << (ZmeiLangParser.COL_FIELD_TYPE_CREATE_TIME - 42)) | (1 << (ZmeiLangParser.COL_FIELD_TYPE_UPDATE_TIME - 42)) | (1 << (ZmeiLangParser.COL_FIELD_TYPE_IMAGE - 42)) | (1 << (ZmeiLangParser.COL_FIELD_TYPE_FILE - 42)) | (1 << (ZmeiLangParser.COL_FIELD_TYPE_FILER_IMAGE - 42)) | (1 << (ZmeiLangParser.COL_FIELD_TYPE_FILER_FILE - 42)) | (1 << (ZmeiLangParser.COL_FIELD_TYPE_FILER_FOLDER - 42)) | (1 << (ZmeiLangParser.COL_FIELD_TYPE_FILER_IMAGE_FOLDER - 42)) | (1 << (ZmeiLangParser.COL_FIELD_TYPE_TEXT - 42)) | (1 << (ZmeiLangParser.COL_FIELD_TYPE_INT - 42)) | (1 << (ZmeiLangParser.COL_FIELD_TYPE_SLUG - 42)) | (1 << (ZmeiLangParser.COL_FIELD_TYPE_BOOL - 42)) | (1 << (ZmeiLangParser.COL_FIELD_TYPE_ONE - 42)) | (1 << (ZmeiLangParser.COL_FIELD_TYPE_ONE2ONE - 42)) | (1 << (ZmeiLangParser.COL_FIELD_TYPE_MANY - 42)) | (1 << (ZmeiLangParser.COL_FIELD_CHOICES - 42)) | (1 << (ZmeiLangParser.KW_THEME - 42)) | (1 << (ZmeiLangParser.KW_INSTALL - 42)) | (1 << (ZmeiLangParser.KW_HEADER - 42)) | (1 << (ZmeiLangParser.KW_SERVICES - 42)) | (1 << (ZmeiLangParser.KW_SELENIUM_PYTEST - 42)) | (1 << (ZmeiLangParser.KW_CHILD - 42)) | (1 << (ZmeiLangParser.KW_FILTER_OUT - 42)) | (1 << (ZmeiLangParser.KW_FILTER_IN - 42)) | (1 << (ZmeiLangParser.KW_PAGE - 42)) | (1 << (ZmeiLangParser.KW_LINK_SUFFIX - 42)) | (1 << (ZmeiLangParser.KW_URL_PREFIX - 42)) | (1 << (ZmeiLangParser.KW_CAN_EDIT - 42)) | (1 << (ZmeiLangParser.KW_OBJECT_EXPR - 42)) | (1 << (ZmeiLangParser.KW_BLOCK - 42)) | (1 << (ZmeiLangParser.KW_ITEM_NAME - 42)) | (1 << (ZmeiLangParser.KW_PK_PARAM - 42)) | (1 << (ZmeiLangParser.KW_LIST_FIELDS - 42)) | (1 << (ZmeiLangParser.KW_DELETE - 42)) | (1 << (ZmeiLangParser.KW_EDIT - 42)) | (1 << (ZmeiLangParser.KW_CREATE - 42)) | (1 << (ZmeiLangParser.KW_DETAIL - 42)) | (1 << (ZmeiLangParser.KW_SKIP - 42)) | (1 << (ZmeiLangParser.KW_FROM - 42)) | (1 << (ZmeiLangParser.KW_POLY_LIST - 42)) | (1 << (ZmeiLangParser.KW_CSS - 42)) | (1 << (ZmeiLangParser.KW_JS - 42)) | (1 << (ZmeiLangParser.KW_INLINE_TYPE_TABULAR - 42)) | (1 << (ZmeiLangParser.KW_INLINE_TYPE_STACKED - 42)) | (1 << (ZmeiLangParser.KW_INLINE_TYPE_POLYMORPHIC - 42)) | (1 << (ZmeiLangParser.KW_INLINE - 42)) | (1 << (ZmeiLangParser.KW_TYPE - 42)) | (1 << (ZmeiLangParser.KW_USER_FIELD - 42)) | (1 << (ZmeiLangParser.KW_ANNOTATE - 42)) | (1 << (ZmeiLangParser.KW_ON_CREATE - 42)) | (1 << (ZmeiLangParser.KW_QUERY - 42)) | (1 << (ZmeiLangParser.KW_AUTH - 42)) | (1 << (ZmeiLangParser.KW_COUNT - 42)) | (1 << (ZmeiLangParser.KW_I18N - 42)))) != 0) or ((((_la - 106)) & ~0x3f) == 0 and ((1 << (_la - 106)) & ((1 << (ZmeiLangParser.KW_EXTENSION - 106)) | (1 << (ZmeiLangParser.KW_TABS - 106)) | (1 << (ZmeiLangParser.KW_LIST - 106)) | (1 << (ZmeiLangParser.KW_READ_ONLY - 106)) | (1 << (ZmeiLangParser.KW_LIST_EDITABLE - 106)) | (1 << (ZmeiLangParser.KW_LIST_FILTER - 106)) | (1 << (ZmeiLangParser.KW_LIST_SEARCH - 106)) | (1 << (ZmeiLangParser.KW_FIELDS - 106)) | (1 << (ZmeiLangParser.KW_IMPORT - 106)) | (1 << (ZmeiLangParser.KW_AS - 106)) | (1 << (ZmeiLangParser.WRITE_MODE - 106)) | (1 << (ZmeiLangParser.BOOL - 106)) | (1 << (ZmeiLangParser.ID - 106)) | (1 << (ZmeiLangParser.DIGIT - 106)) | (1 << (ZmeiLangParser.UNDERSCORE - 106)) | (1 << (ZmeiLangParser.DASH - 106)) | (1 << (ZmeiLangParser.DOT - 106)))) != 0)):
                    break

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Page_urlContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def url_segments(self):
            return self.getTypedRuleContext(ZmeiLangParser.Url_segmentsContext,0)


        def DOT(self):
            return self.getToken(ZmeiLangParser.DOT, 0)

        def DOLLAR(self):
            return self.getToken(ZmeiLangParser.DOLLAR, 0)

        def getRuleIndex(self):
            return ZmeiLangParser.RULE_page_url

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPage_url" ):
                listener.enterPage_url(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPage_url" ):
                listener.exitPage_url(self)




    def page_url(self):

        localctx = ZmeiLangParser.Page_urlContext(self, self._ctx, self.state)
        self.enterRule(localctx, 376, self.RULE_page_url)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1917
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==ZmeiLangParser.DOT or _la==ZmeiLangParser.DOLLAR:
                self.state = 1916
                _la = self._input.LA(1)
                if not(_la==ZmeiLangParser.DOT or _la==ZmeiLangParser.DOLLAR):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()


            self.state = 1919
            self.url_segments()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Url_partContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def id_or_kw(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(ZmeiLangParser.Id_or_kwContext)
            else:
                return self.getTypedRuleContext(ZmeiLangParser.Id_or_kwContext,i)


        def DASH(self, i:int=None):
            if i is None:
                return self.getTokens(ZmeiLangParser.DASH)
            else:
                return self.getToken(ZmeiLangParser.DASH, i)

        def DIGIT(self, i:int=None):
            if i is None:
                return self.getTokens(ZmeiLangParser.DIGIT)
            else:
                return self.getToken(ZmeiLangParser.DIGIT, i)

        def getRuleIndex(self):
            return ZmeiLangParser.RULE_url_part

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterUrl_part" ):
                listener.enterUrl_part(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitUrl_part" ):
                listener.exitUrl_part(self)




    def url_part(self):

        localctx = ZmeiLangParser.Url_partContext(self, self._ctx, self.state)
        self.enterRule(localctx, 378, self.RULE_url_part)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1924 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 1924
                self._errHandler.sync(self)
                token = self._input.LA(1)
                if token in [ZmeiLangParser.KW_AUTH_TYPE_BASIC, ZmeiLangParser.KW_AUTH_TYPE_SESSION, ZmeiLangParser.KW_AUTH_TYPE_TOKEN, ZmeiLangParser.COL_FIELD_TYPE_LONGTEXT, ZmeiLangParser.COL_FIELD_TYPE_HTML, ZmeiLangParser.COL_FIELD_TYPE_HTML_MEDIA, ZmeiLangParser.COL_FIELD_TYPE_FLOAT, ZmeiLangParser.COL_FIELD_TYPE_DECIMAL, ZmeiLangParser.COL_FIELD_TYPE_DATE, ZmeiLangParser.COL_FIELD_TYPE_DATETIME, ZmeiLangParser.COL_FIELD_TYPE_CREATE_TIME, ZmeiLangParser.COL_FIELD_TYPE_UPDATE_TIME, ZmeiLangParser.COL_FIELD_TYPE_IMAGE, ZmeiLangParser.COL_FIELD_TYPE_FILE, ZmeiLangParser.COL_FIELD_TYPE_FILER_IMAGE, ZmeiLangParser.COL_FIELD_TYPE_FILER_FILE, ZmeiLangParser.COL_FIELD_TYPE_FILER_FOLDER, ZmeiLangParser.COL_FIELD_TYPE_FILER_IMAGE_FOLDER, ZmeiLangParser.COL_FIELD_TYPE_TEXT, ZmeiLangParser.COL_FIELD_TYPE_INT, ZmeiLangParser.COL_FIELD_TYPE_SLUG, ZmeiLangParser.COL_FIELD_TYPE_BOOL, ZmeiLangParser.COL_FIELD_TYPE_ONE, ZmeiLangParser.COL_FIELD_TYPE_ONE2ONE, ZmeiLangParser.COL_FIELD_TYPE_MANY, ZmeiLangParser.COL_FIELD_CHOICES, ZmeiLangParser.KW_THEME, ZmeiLangParser.KW_INSTALL, ZmeiLangParser.KW_HEADER, ZmeiLangParser.KW_SERVICES, ZmeiLangParser.KW_SELENIUM_PYTEST, ZmeiLangParser.KW_CHILD, ZmeiLangParser.KW_FILTER_OUT, ZmeiLangParser.KW_FILTER_IN, ZmeiLangParser.KW_PAGE, ZmeiLangParser.KW_LINK_SUFFIX, ZmeiLangParser.KW_URL_PREFIX, ZmeiLangParser.KW_CAN_EDIT, ZmeiLangParser.KW_OBJECT_EXPR, ZmeiLangParser.KW_BLOCK, ZmeiLangParser.KW_ITEM_NAME, ZmeiLangParser.KW_PK_PARAM, ZmeiLangParser.KW_LIST_FIELDS, ZmeiLangParser.KW_DELETE, ZmeiLangParser.KW_EDIT, ZmeiLangParser.KW_CREATE, ZmeiLangParser.KW_DETAIL, ZmeiLangParser.KW_SKIP, ZmeiLangParser.KW_FROM, ZmeiLangParser.KW_POLY_LIST, ZmeiLangParser.KW_CSS, ZmeiLangParser.KW_JS, ZmeiLangParser.KW_INLINE_TYPE_TABULAR, ZmeiLangParser.KW_INLINE_TYPE_STACKED, ZmeiLangParser.KW_INLINE_TYPE_POLYMORPHIC, ZmeiLangParser.KW_INLINE, ZmeiLangParser.KW_TYPE, ZmeiLangParser.KW_USER_FIELD, ZmeiLangParser.KW_ANNOTATE, ZmeiLangParser.KW_ON_CREATE, ZmeiLangParser.KW_QUERY, ZmeiLangParser.KW_AUTH, ZmeiLangParser.KW_COUNT, ZmeiLangParser.KW_I18N, ZmeiLangParser.KW_EXTENSION, ZmeiLangParser.KW_TABS, ZmeiLangParser.KW_LIST, ZmeiLangParser.KW_READ_ONLY, ZmeiLangParser.KW_LIST_EDITABLE, ZmeiLangParser.KW_LIST_FILTER, ZmeiLangParser.KW_LIST_SEARCH, ZmeiLangParser.KW_FIELDS, ZmeiLangParser.KW_IMPORT, ZmeiLangParser.KW_AS, ZmeiLangParser.WRITE_MODE, ZmeiLangParser.BOOL, ZmeiLangParser.ID]:
                    self.state = 1921
                    self.id_or_kw()
                    pass
                elif token in [ZmeiLangParser.DASH]:
                    self.state = 1922
                    self.match(ZmeiLangParser.DASH)
                    pass
                elif token in [ZmeiLangParser.DIGIT]:
                    self.state = 1923
                    self.match(ZmeiLangParser.DIGIT)
                    pass
                else:
                    raise NoViableAltException(self)

                self.state = 1926 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not (((((_la - 42)) & ~0x3f) == 0 and ((1 << (_la - 42)) & ((1 << (ZmeiLangParser.KW_AUTH_TYPE_BASIC - 42)) | (1 << (ZmeiLangParser.KW_AUTH_TYPE_SESSION - 42)) | (1 << (ZmeiLangParser.KW_AUTH_TYPE_TOKEN - 42)) | (1 << (ZmeiLangParser.COL_FIELD_TYPE_LONGTEXT - 42)) | (1 << (ZmeiLangParser.COL_FIELD_TYPE_HTML - 42)) | (1 << (ZmeiLangParser.COL_FIELD_TYPE_HTML_MEDIA - 42)) | (1 << (ZmeiLangParser.COL_FIELD_TYPE_FLOAT - 42)) | (1 << (ZmeiLangParser.COL_FIELD_TYPE_DECIMAL - 42)) | (1 << (ZmeiLangParser.COL_FIELD_TYPE_DATE - 42)) | (1 << (ZmeiLangParser.COL_FIELD_TYPE_DATETIME - 42)) | (1 << (ZmeiLangParser.COL_FIELD_TYPE_CREATE_TIME - 42)) | (1 << (ZmeiLangParser.COL_FIELD_TYPE_UPDATE_TIME - 42)) | (1 << (ZmeiLangParser.COL_FIELD_TYPE_IMAGE - 42)) | (1 << (ZmeiLangParser.COL_FIELD_TYPE_FILE - 42)) | (1 << (ZmeiLangParser.COL_FIELD_TYPE_FILER_IMAGE - 42)) | (1 << (ZmeiLangParser.COL_FIELD_TYPE_FILER_FILE - 42)) | (1 << (ZmeiLangParser.COL_FIELD_TYPE_FILER_FOLDER - 42)) | (1 << (ZmeiLangParser.COL_FIELD_TYPE_FILER_IMAGE_FOLDER - 42)) | (1 << (ZmeiLangParser.COL_FIELD_TYPE_TEXT - 42)) | (1 << (ZmeiLangParser.COL_FIELD_TYPE_INT - 42)) | (1 << (ZmeiLangParser.COL_FIELD_TYPE_SLUG - 42)) | (1 << (ZmeiLangParser.COL_FIELD_TYPE_BOOL - 42)) | (1 << (ZmeiLangParser.COL_FIELD_TYPE_ONE - 42)) | (1 << (ZmeiLangParser.COL_FIELD_TYPE_ONE2ONE - 42)) | (1 << (ZmeiLangParser.COL_FIELD_TYPE_MANY - 42)) | (1 << (ZmeiLangParser.COL_FIELD_CHOICES - 42)) | (1 << (ZmeiLangParser.KW_THEME - 42)) | (1 << (ZmeiLangParser.KW_INSTALL - 42)) | (1 << (ZmeiLangParser.KW_HEADER - 42)) | (1 << (ZmeiLangParser.KW_SERVICES - 42)) | (1 << (ZmeiLangParser.KW_SELENIUM_PYTEST - 42)) | (1 << (ZmeiLangParser.KW_CHILD - 42)) | (1 << (ZmeiLangParser.KW_FILTER_OUT - 42)) | (1 << (ZmeiLangParser.KW_FILTER_IN - 42)) | (1 << (ZmeiLangParser.KW_PAGE - 42)) | (1 << (ZmeiLangParser.KW_LINK_SUFFIX - 42)) | (1 << (ZmeiLangParser.KW_URL_PREFIX - 42)) | (1 << (ZmeiLangParser.KW_CAN_EDIT - 42)) | (1 << (ZmeiLangParser.KW_OBJECT_EXPR - 42)) | (1 << (ZmeiLangParser.KW_BLOCK - 42)) | (1 << (ZmeiLangParser.KW_ITEM_NAME - 42)) | (1 << (ZmeiLangParser.KW_PK_PARAM - 42)) | (1 << (ZmeiLangParser.KW_LIST_FIELDS - 42)) | (1 << (ZmeiLangParser.KW_DELETE - 42)) | (1 << (ZmeiLangParser.KW_EDIT - 42)) | (1 << (ZmeiLangParser.KW_CREATE - 42)) | (1 << (ZmeiLangParser.KW_DETAIL - 42)) | (1 << (ZmeiLangParser.KW_SKIP - 42)) | (1 << (ZmeiLangParser.KW_FROM - 42)) | (1 << (ZmeiLangParser.KW_POLY_LIST - 42)) | (1 << (ZmeiLangParser.KW_CSS - 42)) | (1 << (ZmeiLangParser.KW_JS - 42)) | (1 << (ZmeiLangParser.KW_INLINE_TYPE_TABULAR - 42)) | (1 << (ZmeiLangParser.KW_INLINE_TYPE_STACKED - 42)) | (1 << (ZmeiLangParser.KW_INLINE_TYPE_POLYMORPHIC - 42)) | (1 << (ZmeiLangParser.KW_INLINE - 42)) | (1 << (ZmeiLangParser.KW_TYPE - 42)) | (1 << (ZmeiLangParser.KW_USER_FIELD - 42)) | (1 << (ZmeiLangParser.KW_ANNOTATE - 42)) | (1 << (ZmeiLangParser.KW_ON_CREATE - 42)) | (1 << (ZmeiLangParser.KW_QUERY - 42)) | (1 << (ZmeiLangParser.KW_AUTH - 42)) | (1 << (ZmeiLangParser.KW_COUNT - 42)) | (1 << (ZmeiLangParser.KW_I18N - 42)))) != 0) or ((((_la - 106)) & ~0x3f) == 0 and ((1 << (_la - 106)) & ((1 << (ZmeiLangParser.KW_EXTENSION - 106)) | (1 << (ZmeiLangParser.KW_TABS - 106)) | (1 << (ZmeiLangParser.KW_LIST - 106)) | (1 << (ZmeiLangParser.KW_READ_ONLY - 106)) | (1 << (ZmeiLangParser.KW_LIST_EDITABLE - 106)) | (1 << (ZmeiLangParser.KW_LIST_FILTER - 106)) | (1 << (ZmeiLangParser.KW_LIST_SEARCH - 106)) | (1 << (ZmeiLangParser.KW_FIELDS - 106)) | (1 << (ZmeiLangParser.KW_IMPORT - 106)) | (1 << (ZmeiLangParser.KW_AS - 106)) | (1 << (ZmeiLangParser.WRITE_MODE - 106)) | (1 << (ZmeiLangParser.BOOL - 106)) | (1 << (ZmeiLangParser.ID - 106)) | (1 << (ZmeiLangParser.DIGIT - 106)) | (1 << (ZmeiLangParser.DASH - 106)))) != 0)):
                    break

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Url_paramContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def LT(self):
            return self.getToken(ZmeiLangParser.LT, 0)

        def id_or_kw(self):
            return self.getTypedRuleContext(ZmeiLangParser.Id_or_kwContext,0)


        def GT(self):
            return self.getToken(ZmeiLangParser.GT, 0)

        def getRuleIndex(self):
            return ZmeiLangParser.RULE_url_param

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterUrl_param" ):
                listener.enterUrl_param(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitUrl_param" ):
                listener.exitUrl_param(self)




    def url_param(self):

        localctx = ZmeiLangParser.Url_paramContext(self, self._ctx, self.state)
        self.enterRule(localctx, 380, self.RULE_url_param)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1928
            self.match(ZmeiLangParser.LT)
            self.state = 1929
            self.id_or_kw()
            self.state = 1930
            self.match(ZmeiLangParser.GT)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Url_segmentContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def url_part(self):
            return self.getTypedRuleContext(ZmeiLangParser.Url_partContext,0)


        def url_param(self):
            return self.getTypedRuleContext(ZmeiLangParser.Url_paramContext,0)


        def getRuleIndex(self):
            return ZmeiLangParser.RULE_url_segment

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterUrl_segment" ):
                listener.enterUrl_segment(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitUrl_segment" ):
                listener.exitUrl_segment(self)




    def url_segment(self):

        localctx = ZmeiLangParser.Url_segmentContext(self, self._ctx, self.state)
        self.enterRule(localctx, 382, self.RULE_url_segment)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1934
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [ZmeiLangParser.KW_AUTH_TYPE_BASIC, ZmeiLangParser.KW_AUTH_TYPE_SESSION, ZmeiLangParser.KW_AUTH_TYPE_TOKEN, ZmeiLangParser.COL_FIELD_TYPE_LONGTEXT, ZmeiLangParser.COL_FIELD_TYPE_HTML, ZmeiLangParser.COL_FIELD_TYPE_HTML_MEDIA, ZmeiLangParser.COL_FIELD_TYPE_FLOAT, ZmeiLangParser.COL_FIELD_TYPE_DECIMAL, ZmeiLangParser.COL_FIELD_TYPE_DATE, ZmeiLangParser.COL_FIELD_TYPE_DATETIME, ZmeiLangParser.COL_FIELD_TYPE_CREATE_TIME, ZmeiLangParser.COL_FIELD_TYPE_UPDATE_TIME, ZmeiLangParser.COL_FIELD_TYPE_IMAGE, ZmeiLangParser.COL_FIELD_TYPE_FILE, ZmeiLangParser.COL_FIELD_TYPE_FILER_IMAGE, ZmeiLangParser.COL_FIELD_TYPE_FILER_FILE, ZmeiLangParser.COL_FIELD_TYPE_FILER_FOLDER, ZmeiLangParser.COL_FIELD_TYPE_FILER_IMAGE_FOLDER, ZmeiLangParser.COL_FIELD_TYPE_TEXT, ZmeiLangParser.COL_FIELD_TYPE_INT, ZmeiLangParser.COL_FIELD_TYPE_SLUG, ZmeiLangParser.COL_FIELD_TYPE_BOOL, ZmeiLangParser.COL_FIELD_TYPE_ONE, ZmeiLangParser.COL_FIELD_TYPE_ONE2ONE, ZmeiLangParser.COL_FIELD_TYPE_MANY, ZmeiLangParser.COL_FIELD_CHOICES, ZmeiLangParser.KW_THEME, ZmeiLangParser.KW_INSTALL, ZmeiLangParser.KW_HEADER, ZmeiLangParser.KW_SERVICES, ZmeiLangParser.KW_SELENIUM_PYTEST, ZmeiLangParser.KW_CHILD, ZmeiLangParser.KW_FILTER_OUT, ZmeiLangParser.KW_FILTER_IN, ZmeiLangParser.KW_PAGE, ZmeiLangParser.KW_LINK_SUFFIX, ZmeiLangParser.KW_URL_PREFIX, ZmeiLangParser.KW_CAN_EDIT, ZmeiLangParser.KW_OBJECT_EXPR, ZmeiLangParser.KW_BLOCK, ZmeiLangParser.KW_ITEM_NAME, ZmeiLangParser.KW_PK_PARAM, ZmeiLangParser.KW_LIST_FIELDS, ZmeiLangParser.KW_DELETE, ZmeiLangParser.KW_EDIT, ZmeiLangParser.KW_CREATE, ZmeiLangParser.KW_DETAIL, ZmeiLangParser.KW_SKIP, ZmeiLangParser.KW_FROM, ZmeiLangParser.KW_POLY_LIST, ZmeiLangParser.KW_CSS, ZmeiLangParser.KW_JS, ZmeiLangParser.KW_INLINE_TYPE_TABULAR, ZmeiLangParser.KW_INLINE_TYPE_STACKED, ZmeiLangParser.KW_INLINE_TYPE_POLYMORPHIC, ZmeiLangParser.KW_INLINE, ZmeiLangParser.KW_TYPE, ZmeiLangParser.KW_USER_FIELD, ZmeiLangParser.KW_ANNOTATE, ZmeiLangParser.KW_ON_CREATE, ZmeiLangParser.KW_QUERY, ZmeiLangParser.KW_AUTH, ZmeiLangParser.KW_COUNT, ZmeiLangParser.KW_I18N, ZmeiLangParser.KW_EXTENSION, ZmeiLangParser.KW_TABS, ZmeiLangParser.KW_LIST, ZmeiLangParser.KW_READ_ONLY, ZmeiLangParser.KW_LIST_EDITABLE, ZmeiLangParser.KW_LIST_FILTER, ZmeiLangParser.KW_LIST_SEARCH, ZmeiLangParser.KW_FIELDS, ZmeiLangParser.KW_IMPORT, ZmeiLangParser.KW_AS, ZmeiLangParser.WRITE_MODE, ZmeiLangParser.BOOL, ZmeiLangParser.ID, ZmeiLangParser.DIGIT, ZmeiLangParser.DASH]:
                self.state = 1932
                self.url_part()
                pass
            elif token in [ZmeiLangParser.LT]:
                self.state = 1933
                self.url_param()
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Url_segmentsContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def SLASH(self, i:int=None):
            if i is None:
                return self.getTokens(ZmeiLangParser.SLASH)
            else:
                return self.getToken(ZmeiLangParser.SLASH, i)

        def url_segment(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(ZmeiLangParser.Url_segmentContext)
            else:
                return self.getTypedRuleContext(ZmeiLangParser.Url_segmentContext,i)


        def getRuleIndex(self):
            return ZmeiLangParser.RULE_url_segments

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterUrl_segments" ):
                listener.enterUrl_segments(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitUrl_segments" ):
                listener.exitUrl_segments(self)




    def url_segments(self):

        localctx = ZmeiLangParser.Url_segmentsContext(self, self._ctx, self.state)
        self.enterRule(localctx, 384, self.RULE_url_segments)
        self._la = 0 # Token type
        try:
            self.state = 1946
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,190,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 1936
                self.match(ZmeiLangParser.SLASH)
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 1939 
                self._errHandler.sync(self)
                _alt = 1
                while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                    if _alt == 1:
                        self.state = 1937
                        self.match(ZmeiLangParser.SLASH)
                        self.state = 1938
                        self.url_segment()

                    else:
                        raise NoViableAltException(self)
                    self.state = 1941 
                    self._errHandler.sync(self)
                    _alt = self._interp.adaptivePredict(self._input,188,self._ctx)

                self.state = 1944
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==ZmeiLangParser.SLASH:
                    self.state = 1943
                    self.match(ZmeiLangParser.SLASH)


                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Page_nameContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def id_or_kw(self):
            return self.getTypedRuleContext(ZmeiLangParser.Id_or_kwContext,0)


        def getRuleIndex(self):
            return ZmeiLangParser.RULE_page_name

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPage_name" ):
                listener.enterPage_name(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPage_name" ):
                listener.exitPage_name(self)




    def page_name(self):

        localctx = ZmeiLangParser.Page_nameContext(self, self._ctx, self.state)
        self.enterRule(localctx, 386, self.RULE_page_name)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1948
            self.id_or_kw()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Page_bodyContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def page_field(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(ZmeiLangParser.Page_fieldContext)
            else:
                return self.getTypedRuleContext(ZmeiLangParser.Page_fieldContext,i)


        def page_function(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(ZmeiLangParser.Page_functionContext)
            else:
                return self.getTypedRuleContext(ZmeiLangParser.Page_functionContext,i)


        def page_code(self):
            return self.getTypedRuleContext(ZmeiLangParser.Page_codeContext,0)


        def NL(self, i:int=None):
            if i is None:
                return self.getTokens(ZmeiLangParser.NL)
            else:
                return self.getToken(ZmeiLangParser.NL, i)

        def page_annotation(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(ZmeiLangParser.Page_annotationContext)
            else:
                return self.getTypedRuleContext(ZmeiLangParser.Page_annotationContext,i)


        def getRuleIndex(self):
            return ZmeiLangParser.RULE_page_body

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPage_body" ):
                listener.enterPage_body(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPage_body" ):
                listener.exitPage_body(self)




    def page_body(self):

        localctx = ZmeiLangParser.Page_bodyContext(self, self._ctx, self.state)
        self.enterRule(localctx, 388, self.RULE_page_body)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1953
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,191,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 1950
                    self.page_field() 
                self.state = 1955
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,191,self._ctx)

            self.state = 1959
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,192,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 1956
                    self.page_function() 
                self.state = 1961
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,192,self._ctx)

            self.state = 1963
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==ZmeiLangParser.ASSIGN or _la==ZmeiLangParser.CODE_BLOCK:
                self.state = 1962
                self.page_code()


            self.state = 1968
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,194,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 1965
                    self.match(ZmeiLangParser.NL) 
                self.state = 1970
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,194,self._ctx)

            self.state = 1974
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,195,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 1971
                    self.page_annotation() 
                self.state = 1976
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,195,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Page_codeContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def python_code(self):
            return self.getTypedRuleContext(ZmeiLangParser.Python_codeContext,0)


        def getRuleIndex(self):
            return ZmeiLangParser.RULE_page_code

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPage_code" ):
                listener.enterPage_code(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPage_code" ):
                listener.exitPage_code(self)




    def page_code(self):

        localctx = ZmeiLangParser.Page_codeContext(self, self._ctx, self.state)
        self.enterRule(localctx, 390, self.RULE_page_code)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1977
            self.python_code()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Page_fieldContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def page_field_name(self):
            return self.getTypedRuleContext(ZmeiLangParser.Page_field_nameContext,0)


        def ASSIGN(self):
            return self.getToken(ZmeiLangParser.ASSIGN, 0)

        def page_field_code(self):
            return self.getTypedRuleContext(ZmeiLangParser.Page_field_codeContext,0)


        def EOF(self):
            return self.getToken(ZmeiLangParser.EOF, 0)

        def NL(self, i:int=None):
            if i is None:
                return self.getTokens(ZmeiLangParser.NL)
            else:
                return self.getToken(ZmeiLangParser.NL, i)

        def getRuleIndex(self):
            return ZmeiLangParser.RULE_page_field

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPage_field" ):
                listener.enterPage_field(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPage_field" ):
                listener.exitPage_field(self)




    def page_field(self):

        localctx = ZmeiLangParser.Page_fieldContext(self, self._ctx, self.state)
        self.enterRule(localctx, 392, self.RULE_page_field)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1979
            self.page_field_name()
            self.state = 1980
            self.match(ZmeiLangParser.ASSIGN)
            self.state = 1981
            self.page_field_code()
            self.state = 1988
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [ZmeiLangParser.NL]:
                self.state = 1983 
                self._errHandler.sync(self)
                _alt = 1
                while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                    if _alt == 1:
                        self.state = 1982
                        self.match(ZmeiLangParser.NL)

                    else:
                        raise NoViableAltException(self)
                    self.state = 1985 
                    self._errHandler.sync(self)
                    _alt = self._interp.adaptivePredict(self._input,196,self._ctx)

                pass
            elif token in [ZmeiLangParser.EOF]:
                self.state = 1987
                self.match(ZmeiLangParser.EOF)
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Page_field_nameContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def id_or_kw(self):
            return self.getTypedRuleContext(ZmeiLangParser.Id_or_kwContext,0)


        def getRuleIndex(self):
            return ZmeiLangParser.RULE_page_field_name

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPage_field_name" ):
                listener.enterPage_field_name(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPage_field_name" ):
                listener.exitPage_field_name(self)




    def page_field_name(self):

        localctx = ZmeiLangParser.Page_field_nameContext(self, self._ctx, self.state)
        self.enterRule(localctx, 394, self.RULE_page_field_name)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1990
            self.id_or_kw()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Page_field_codeContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def PYTHON_CODE(self):
            return self.getToken(ZmeiLangParser.PYTHON_CODE, 0)

        def getRuleIndex(self):
            return ZmeiLangParser.RULE_page_field_code

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPage_field_code" ):
                listener.enterPage_field_code(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPage_field_code" ):
                listener.exitPage_field_code(self)




    def page_field_code(self):

        localctx = ZmeiLangParser.Page_field_codeContext(self, self._ctx, self.state)
        self.enterRule(localctx, 396, self.RULE_page_field_code)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1992
            self.match(ZmeiLangParser.PYTHON_CODE)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Page_functionContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def page_function_name(self):
            return self.getTypedRuleContext(ZmeiLangParser.Page_function_nameContext,0)


        def BRACE_OPEN(self):
            return self.getToken(ZmeiLangParser.BRACE_OPEN, 0)

        def BRACE_CLOSE(self):
            return self.getToken(ZmeiLangParser.BRACE_CLOSE, 0)

        def EOF(self):
            return self.getToken(ZmeiLangParser.EOF, 0)

        def page_function_args(self):
            return self.getTypedRuleContext(ZmeiLangParser.Page_function_argsContext,0)


        def code_block(self):
            return self.getTypedRuleContext(ZmeiLangParser.Code_blockContext,0)


        def NL(self, i:int=None):
            if i is None:
                return self.getTokens(ZmeiLangParser.NL)
            else:
                return self.getToken(ZmeiLangParser.NL, i)

        def getRuleIndex(self):
            return ZmeiLangParser.RULE_page_function

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPage_function" ):
                listener.enterPage_function(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPage_function" ):
                listener.exitPage_function(self)




    def page_function(self):

        localctx = ZmeiLangParser.Page_functionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 398, self.RULE_page_function)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1994
            self.page_function_name()
            self.state = 1995
            self.match(ZmeiLangParser.BRACE_OPEN)
            self.state = 1997
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if ((((_la - 42)) & ~0x3f) == 0 and ((1 << (_la - 42)) & ((1 << (ZmeiLangParser.KW_AUTH_TYPE_BASIC - 42)) | (1 << (ZmeiLangParser.KW_AUTH_TYPE_SESSION - 42)) | (1 << (ZmeiLangParser.KW_AUTH_TYPE_TOKEN - 42)) | (1 << (ZmeiLangParser.COL_FIELD_TYPE_LONGTEXT - 42)) | (1 << (ZmeiLangParser.COL_FIELD_TYPE_HTML - 42)) | (1 << (ZmeiLangParser.COL_FIELD_TYPE_HTML_MEDIA - 42)) | (1 << (ZmeiLangParser.COL_FIELD_TYPE_FLOAT - 42)) | (1 << (ZmeiLangParser.COL_FIELD_TYPE_DECIMAL - 42)) | (1 << (ZmeiLangParser.COL_FIELD_TYPE_DATE - 42)) | (1 << (ZmeiLangParser.COL_FIELD_TYPE_DATETIME - 42)) | (1 << (ZmeiLangParser.COL_FIELD_TYPE_CREATE_TIME - 42)) | (1 << (ZmeiLangParser.COL_FIELD_TYPE_UPDATE_TIME - 42)) | (1 << (ZmeiLangParser.COL_FIELD_TYPE_IMAGE - 42)) | (1 << (ZmeiLangParser.COL_FIELD_TYPE_FILE - 42)) | (1 << (ZmeiLangParser.COL_FIELD_TYPE_FILER_IMAGE - 42)) | (1 << (ZmeiLangParser.COL_FIELD_TYPE_FILER_FILE - 42)) | (1 << (ZmeiLangParser.COL_FIELD_TYPE_FILER_FOLDER - 42)) | (1 << (ZmeiLangParser.COL_FIELD_TYPE_FILER_IMAGE_FOLDER - 42)) | (1 << (ZmeiLangParser.COL_FIELD_TYPE_TEXT - 42)) | (1 << (ZmeiLangParser.COL_FIELD_TYPE_INT - 42)) | (1 << (ZmeiLangParser.COL_FIELD_TYPE_SLUG - 42)) | (1 << (ZmeiLangParser.COL_FIELD_TYPE_BOOL - 42)) | (1 << (ZmeiLangParser.COL_FIELD_TYPE_ONE - 42)) | (1 << (ZmeiLangParser.COL_FIELD_TYPE_ONE2ONE - 42)) | (1 << (ZmeiLangParser.COL_FIELD_TYPE_MANY - 42)) | (1 << (ZmeiLangParser.COL_FIELD_CHOICES - 42)) | (1 << (ZmeiLangParser.KW_THEME - 42)) | (1 << (ZmeiLangParser.KW_INSTALL - 42)) | (1 << (ZmeiLangParser.KW_HEADER - 42)) | (1 << (ZmeiLangParser.KW_SERVICES - 42)) | (1 << (ZmeiLangParser.KW_SELENIUM_PYTEST - 42)) | (1 << (ZmeiLangParser.KW_CHILD - 42)) | (1 << (ZmeiLangParser.KW_FILTER_OUT - 42)) | (1 << (ZmeiLangParser.KW_FILTER_IN - 42)) | (1 << (ZmeiLangParser.KW_PAGE - 42)) | (1 << (ZmeiLangParser.KW_LINK_SUFFIX - 42)) | (1 << (ZmeiLangParser.KW_URL_PREFIX - 42)) | (1 << (ZmeiLangParser.KW_CAN_EDIT - 42)) | (1 << (ZmeiLangParser.KW_OBJECT_EXPR - 42)) | (1 << (ZmeiLangParser.KW_BLOCK - 42)) | (1 << (ZmeiLangParser.KW_ITEM_NAME - 42)) | (1 << (ZmeiLangParser.KW_PK_PARAM - 42)) | (1 << (ZmeiLangParser.KW_LIST_FIELDS - 42)) | (1 << (ZmeiLangParser.KW_DELETE - 42)) | (1 << (ZmeiLangParser.KW_EDIT - 42)) | (1 << (ZmeiLangParser.KW_CREATE - 42)) | (1 << (ZmeiLangParser.KW_DETAIL - 42)) | (1 << (ZmeiLangParser.KW_SKIP - 42)) | (1 << (ZmeiLangParser.KW_FROM - 42)) | (1 << (ZmeiLangParser.KW_POLY_LIST - 42)) | (1 << (ZmeiLangParser.KW_CSS - 42)) | (1 << (ZmeiLangParser.KW_JS - 42)) | (1 << (ZmeiLangParser.KW_INLINE_TYPE_TABULAR - 42)) | (1 << (ZmeiLangParser.KW_INLINE_TYPE_STACKED - 42)) | (1 << (ZmeiLangParser.KW_INLINE_TYPE_POLYMORPHIC - 42)) | (1 << (ZmeiLangParser.KW_INLINE - 42)) | (1 << (ZmeiLangParser.KW_TYPE - 42)) | (1 << (ZmeiLangParser.KW_USER_FIELD - 42)) | (1 << (ZmeiLangParser.KW_ANNOTATE - 42)) | (1 << (ZmeiLangParser.KW_ON_CREATE - 42)) | (1 << (ZmeiLangParser.KW_QUERY - 42)) | (1 << (ZmeiLangParser.KW_AUTH - 42)) | (1 << (ZmeiLangParser.KW_COUNT - 42)) | (1 << (ZmeiLangParser.KW_I18N - 42)))) != 0) or ((((_la - 106)) & ~0x3f) == 0 and ((1 << (_la - 106)) & ((1 << (ZmeiLangParser.KW_EXTENSION - 106)) | (1 << (ZmeiLangParser.KW_TABS - 106)) | (1 << (ZmeiLangParser.KW_LIST - 106)) | (1 << (ZmeiLangParser.KW_READ_ONLY - 106)) | (1 << (ZmeiLangParser.KW_LIST_EDITABLE - 106)) | (1 << (ZmeiLangParser.KW_LIST_FILTER - 106)) | (1 << (ZmeiLangParser.KW_LIST_SEARCH - 106)) | (1 << (ZmeiLangParser.KW_FIELDS - 106)) | (1 << (ZmeiLangParser.KW_IMPORT - 106)) | (1 << (ZmeiLangParser.KW_AS - 106)) | (1 << (ZmeiLangParser.WRITE_MODE - 106)) | (1 << (ZmeiLangParser.BOOL - 106)) | (1 << (ZmeiLangParser.ID - 106)) | (1 << (ZmeiLangParser.DOT - 106)))) != 0):
                self.state = 1996
                self.page_function_args()


            self.state = 1999
            self.match(ZmeiLangParser.BRACE_CLOSE)
            self.state = 2001
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==ZmeiLangParser.CODE_BLOCK:
                self.state = 2000
                self.code_block()


            self.state = 2009
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [ZmeiLangParser.NL]:
                self.state = 2004 
                self._errHandler.sync(self)
                _alt = 1
                while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                    if _alt == 1:
                        self.state = 2003
                        self.match(ZmeiLangParser.NL)

                    else:
                        raise NoViableAltException(self)
                    self.state = 2006 
                    self._errHandler.sync(self)
                    _alt = self._interp.adaptivePredict(self._input,200,self._ctx)

                pass
            elif token in [ZmeiLangParser.EOF]:
                self.state = 2008
                self.match(ZmeiLangParser.EOF)
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Page_function_nameContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def id_or_kw(self):
            return self.getTypedRuleContext(ZmeiLangParser.Id_or_kwContext,0)


        def getRuleIndex(self):
            return ZmeiLangParser.RULE_page_function_name

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPage_function_name" ):
                listener.enterPage_function_name(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPage_function_name" ):
                listener.exitPage_function_name(self)




    def page_function_name(self):

        localctx = ZmeiLangParser.Page_function_nameContext(self, self._ctx, self.state)
        self.enterRule(localctx, 400, self.RULE_page_function_name)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 2011
            self.id_or_kw()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Page_function_argsContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def page_function_arg(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(ZmeiLangParser.Page_function_argContext)
            else:
                return self.getTypedRuleContext(ZmeiLangParser.Page_function_argContext,i)


        def COMA(self, i:int=None):
            if i is None:
                return self.getTokens(ZmeiLangParser.COMA)
            else:
                return self.getToken(ZmeiLangParser.COMA, i)

        def getRuleIndex(self):
            return ZmeiLangParser.RULE_page_function_args

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPage_function_args" ):
                listener.enterPage_function_args(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPage_function_args" ):
                listener.exitPage_function_args(self)




    def page_function_args(self):

        localctx = ZmeiLangParser.Page_function_argsContext(self, self._ctx, self.state)
        self.enterRule(localctx, 402, self.RULE_page_function_args)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 2013
            self.page_function_arg()
            self.state = 2018
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==ZmeiLangParser.COMA:
                self.state = 2014
                self.match(ZmeiLangParser.COMA)
                self.state = 2015
                self.page_function_arg()
                self.state = 2020
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Page_function_argContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def id_or_kw(self):
            return self.getTypedRuleContext(ZmeiLangParser.Id_or_kwContext,0)


        def DOT(self):
            return self.getToken(ZmeiLangParser.DOT, 0)

        def getRuleIndex(self):
            return ZmeiLangParser.RULE_page_function_arg

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPage_function_arg" ):
                listener.enterPage_function_arg(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPage_function_arg" ):
                listener.exitPage_function_arg(self)




    def page_function_arg(self):

        localctx = ZmeiLangParser.Page_function_argContext(self, self._ctx, self.state)
        self.enterRule(localctx, 404, self.RULE_page_function_arg)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 2022
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==ZmeiLangParser.DOT:
                self.state = 2021
                self.match(ZmeiLangParser.DOT)


            self.state = 2024
            self.id_or_kw()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Page_annotationContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def an_stream(self):
            return self.getTypedRuleContext(ZmeiLangParser.An_streamContext,0)


        def an_react(self):
            return self.getTypedRuleContext(ZmeiLangParser.An_reactContext,0)


        def an_html(self):
            return self.getTypedRuleContext(ZmeiLangParser.An_htmlContext,0)


        def an_markdown(self):
            return self.getTypedRuleContext(ZmeiLangParser.An_markdownContext,0)


        def an_crud_delete(self):
            return self.getTypedRuleContext(ZmeiLangParser.An_crud_deleteContext,0)


        def an_post(self):
            return self.getTypedRuleContext(ZmeiLangParser.An_postContext,0)


        def an_auth(self):
            return self.getTypedRuleContext(ZmeiLangParser.An_authContext,0)


        def an_crud_create(self):
            return self.getTypedRuleContext(ZmeiLangParser.An_crud_createContext,0)


        def an_crud_edit(self):
            return self.getTypedRuleContext(ZmeiLangParser.An_crud_editContext,0)


        def an_crud(self):
            return self.getTypedRuleContext(ZmeiLangParser.An_crudContext,0)


        def an_crud_list(self):
            return self.getTypedRuleContext(ZmeiLangParser.An_crud_listContext,0)


        def an_menu(self):
            return self.getTypedRuleContext(ZmeiLangParser.An_menuContext,0)


        def an_crud_detail(self):
            return self.getTypedRuleContext(ZmeiLangParser.An_crud_detailContext,0)


        def an_priority_marker(self):
            return self.getTypedRuleContext(ZmeiLangParser.An_priority_markerContext,0)


        def an_get(self):
            return self.getTypedRuleContext(ZmeiLangParser.An_getContext,0)


        def an_error(self):
            return self.getTypedRuleContext(ZmeiLangParser.An_errorContext,0)


        def NL(self):
            return self.getToken(ZmeiLangParser.NL, 0)

        def getRuleIndex(self):
            return ZmeiLangParser.RULE_page_annotation

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPage_annotation" ):
                listener.enterPage_annotation(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPage_annotation" ):
                listener.exitPage_annotation(self)




    def page_annotation(self):

        localctx = ZmeiLangParser.Page_annotationContext(self, self._ctx, self.state)
        self.enterRule(localctx, 406, self.RULE_page_annotation)
        try:
            self.state = 2043
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [ZmeiLangParser.AN_STREAM]:
                self.enterOuterAlt(localctx, 1)
                self.state = 2026
                self.an_stream()
                pass
            elif token in [ZmeiLangParser.AN_REACT, ZmeiLangParser.AN_REACT_CLIENT, ZmeiLangParser.AN_REACT_SERVER]:
                self.enterOuterAlt(localctx, 2)
                self.state = 2027
                self.an_react()
                pass
            elif token in [ZmeiLangParser.AN_HTML]:
                self.enterOuterAlt(localctx, 3)
                self.state = 2028
                self.an_html()
                pass
            elif token in [ZmeiLangParser.AN_MARKDOWN]:
                self.enterOuterAlt(localctx, 4)
                self.state = 2029
                self.an_markdown()
                pass
            elif token in [ZmeiLangParser.AN_CRUD_DELETE]:
                self.enterOuterAlt(localctx, 5)
                self.state = 2030
                self.an_crud_delete()
                pass
            elif token in [ZmeiLangParser.AN_POST]:
                self.enterOuterAlt(localctx, 6)
                self.state = 2031
                self.an_post()
                pass
            elif token in [ZmeiLangParser.AN_AUTH]:
                self.enterOuterAlt(localctx, 7)
                self.state = 2032
                self.an_auth()
                pass
            elif token in [ZmeiLangParser.AN_CRUD_CREATE]:
                self.enterOuterAlt(localctx, 8)
                self.state = 2033
                self.an_crud_create()
                pass
            elif token in [ZmeiLangParser.AN_CRUD_EDIT]:
                self.enterOuterAlt(localctx, 9)
                self.state = 2034
                self.an_crud_edit()
                pass
            elif token in [ZmeiLangParser.AN_CRUD]:
                self.enterOuterAlt(localctx, 10)
                self.state = 2035
                self.an_crud()
                pass
            elif token in [ZmeiLangParser.AN_CRUD_LIST]:
                self.enterOuterAlt(localctx, 11)
                self.state = 2036
                self.an_crud_list()
                pass
            elif token in [ZmeiLangParser.AN_MENU]:
                self.enterOuterAlt(localctx, 12)
                self.state = 2037
                self.an_menu()
                pass
            elif token in [ZmeiLangParser.AN_CRUD_DETAIL]:
                self.enterOuterAlt(localctx, 13)
                self.state = 2038
                self.an_crud_detail()
                pass
            elif token in [ZmeiLangParser.AN_PRIORITY]:
                self.enterOuterAlt(localctx, 14)
                self.state = 2039
                self.an_priority_marker()
                pass
            elif token in [ZmeiLangParser.AN_GET]:
                self.enterOuterAlt(localctx, 15)
                self.state = 2040
                self.an_get()
                pass
            elif token in [ZmeiLangParser.AN_ERROR]:
                self.enterOuterAlt(localctx, 16)
                self.state = 2041
                self.an_error()
                pass
            elif token in [ZmeiLangParser.NL]:
                self.enterOuterAlt(localctx, 17)
                self.state = 2042
                self.match(ZmeiLangParser.NL)
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class An_streamContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def AN_STREAM(self):
            return self.getToken(ZmeiLangParser.AN_STREAM, 0)

        def BRACE_OPEN(self):
            return self.getToken(ZmeiLangParser.BRACE_OPEN, 0)

        def BRACE_CLOSE(self):
            return self.getToken(ZmeiLangParser.BRACE_CLOSE, 0)

        def an_stream_model(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(ZmeiLangParser.An_stream_modelContext)
            else:
                return self.getTypedRuleContext(ZmeiLangParser.An_stream_modelContext,i)


        def NL(self, i:int=None):
            if i is None:
                return self.getTokens(ZmeiLangParser.NL)
            else:
                return self.getToken(ZmeiLangParser.NL, i)

        def getRuleIndex(self):
            return ZmeiLangParser.RULE_an_stream

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAn_stream" ):
                listener.enterAn_stream(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAn_stream" ):
                listener.exitAn_stream(self)




    def an_stream(self):

        localctx = ZmeiLangParser.An_streamContext(self, self._ctx, self.state)
        self.enterRule(localctx, 408, self.RULE_an_stream)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 2045
            self.match(ZmeiLangParser.AN_STREAM)

            self.state = 2046
            self.match(ZmeiLangParser.BRACE_OPEN)
            self.state = 2049 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 2049
                self._errHandler.sync(self)
                token = self._input.LA(1)
                if token in [ZmeiLangParser.KW_AUTH_TYPE_BASIC, ZmeiLangParser.KW_AUTH_TYPE_SESSION, ZmeiLangParser.KW_AUTH_TYPE_TOKEN, ZmeiLangParser.COL_FIELD_TYPE_LONGTEXT, ZmeiLangParser.COL_FIELD_TYPE_HTML, ZmeiLangParser.COL_FIELD_TYPE_HTML_MEDIA, ZmeiLangParser.COL_FIELD_TYPE_FLOAT, ZmeiLangParser.COL_FIELD_TYPE_DECIMAL, ZmeiLangParser.COL_FIELD_TYPE_DATE, ZmeiLangParser.COL_FIELD_TYPE_DATETIME, ZmeiLangParser.COL_FIELD_TYPE_CREATE_TIME, ZmeiLangParser.COL_FIELD_TYPE_UPDATE_TIME, ZmeiLangParser.COL_FIELD_TYPE_IMAGE, ZmeiLangParser.COL_FIELD_TYPE_FILE, ZmeiLangParser.COL_FIELD_TYPE_FILER_IMAGE, ZmeiLangParser.COL_FIELD_TYPE_FILER_FILE, ZmeiLangParser.COL_FIELD_TYPE_FILER_FOLDER, ZmeiLangParser.COL_FIELD_TYPE_FILER_IMAGE_FOLDER, ZmeiLangParser.COL_FIELD_TYPE_TEXT, ZmeiLangParser.COL_FIELD_TYPE_INT, ZmeiLangParser.COL_FIELD_TYPE_SLUG, ZmeiLangParser.COL_FIELD_TYPE_BOOL, ZmeiLangParser.COL_FIELD_TYPE_ONE, ZmeiLangParser.COL_FIELD_TYPE_ONE2ONE, ZmeiLangParser.COL_FIELD_TYPE_MANY, ZmeiLangParser.COL_FIELD_CHOICES, ZmeiLangParser.KW_THEME, ZmeiLangParser.KW_INSTALL, ZmeiLangParser.KW_HEADER, ZmeiLangParser.KW_SERVICES, ZmeiLangParser.KW_SELENIUM_PYTEST, ZmeiLangParser.KW_CHILD, ZmeiLangParser.KW_FILTER_OUT, ZmeiLangParser.KW_FILTER_IN, ZmeiLangParser.KW_PAGE, ZmeiLangParser.KW_LINK_SUFFIX, ZmeiLangParser.KW_URL_PREFIX, ZmeiLangParser.KW_CAN_EDIT, ZmeiLangParser.KW_OBJECT_EXPR, ZmeiLangParser.KW_BLOCK, ZmeiLangParser.KW_ITEM_NAME, ZmeiLangParser.KW_PK_PARAM, ZmeiLangParser.KW_LIST_FIELDS, ZmeiLangParser.KW_DELETE, ZmeiLangParser.KW_EDIT, ZmeiLangParser.KW_CREATE, ZmeiLangParser.KW_DETAIL, ZmeiLangParser.KW_SKIP, ZmeiLangParser.KW_FROM, ZmeiLangParser.KW_POLY_LIST, ZmeiLangParser.KW_CSS, ZmeiLangParser.KW_JS, ZmeiLangParser.KW_INLINE_TYPE_TABULAR, ZmeiLangParser.KW_INLINE_TYPE_STACKED, ZmeiLangParser.KW_INLINE_TYPE_POLYMORPHIC, ZmeiLangParser.KW_INLINE, ZmeiLangParser.KW_TYPE, ZmeiLangParser.KW_USER_FIELD, ZmeiLangParser.KW_ANNOTATE, ZmeiLangParser.KW_ON_CREATE, ZmeiLangParser.KW_QUERY, ZmeiLangParser.KW_AUTH, ZmeiLangParser.KW_COUNT, ZmeiLangParser.KW_I18N, ZmeiLangParser.KW_EXTENSION, ZmeiLangParser.KW_TABS, ZmeiLangParser.KW_LIST, ZmeiLangParser.KW_READ_ONLY, ZmeiLangParser.KW_LIST_EDITABLE, ZmeiLangParser.KW_LIST_FILTER, ZmeiLangParser.KW_LIST_SEARCH, ZmeiLangParser.KW_FIELDS, ZmeiLangParser.KW_IMPORT, ZmeiLangParser.KW_AS, ZmeiLangParser.WRITE_MODE, ZmeiLangParser.BOOL, ZmeiLangParser.ID, ZmeiLangParser.HASH]:
                    self.state = 2047
                    self.an_stream_model()
                    pass
                elif token in [ZmeiLangParser.NL]:
                    self.state = 2048
                    self.match(ZmeiLangParser.NL)
                    pass
                else:
                    raise NoViableAltException(self)

                self.state = 2051 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not (((((_la - 42)) & ~0x3f) == 0 and ((1 << (_la - 42)) & ((1 << (ZmeiLangParser.KW_AUTH_TYPE_BASIC - 42)) | (1 << (ZmeiLangParser.KW_AUTH_TYPE_SESSION - 42)) | (1 << (ZmeiLangParser.KW_AUTH_TYPE_TOKEN - 42)) | (1 << (ZmeiLangParser.COL_FIELD_TYPE_LONGTEXT - 42)) | (1 << (ZmeiLangParser.COL_FIELD_TYPE_HTML - 42)) | (1 << (ZmeiLangParser.COL_FIELD_TYPE_HTML_MEDIA - 42)) | (1 << (ZmeiLangParser.COL_FIELD_TYPE_FLOAT - 42)) | (1 << (ZmeiLangParser.COL_FIELD_TYPE_DECIMAL - 42)) | (1 << (ZmeiLangParser.COL_FIELD_TYPE_DATE - 42)) | (1 << (ZmeiLangParser.COL_FIELD_TYPE_DATETIME - 42)) | (1 << (ZmeiLangParser.COL_FIELD_TYPE_CREATE_TIME - 42)) | (1 << (ZmeiLangParser.COL_FIELD_TYPE_UPDATE_TIME - 42)) | (1 << (ZmeiLangParser.COL_FIELD_TYPE_IMAGE - 42)) | (1 << (ZmeiLangParser.COL_FIELD_TYPE_FILE - 42)) | (1 << (ZmeiLangParser.COL_FIELD_TYPE_FILER_IMAGE - 42)) | (1 << (ZmeiLangParser.COL_FIELD_TYPE_FILER_FILE - 42)) | (1 << (ZmeiLangParser.COL_FIELD_TYPE_FILER_FOLDER - 42)) | (1 << (ZmeiLangParser.COL_FIELD_TYPE_FILER_IMAGE_FOLDER - 42)) | (1 << (ZmeiLangParser.COL_FIELD_TYPE_TEXT - 42)) | (1 << (ZmeiLangParser.COL_FIELD_TYPE_INT - 42)) | (1 << (ZmeiLangParser.COL_FIELD_TYPE_SLUG - 42)) | (1 << (ZmeiLangParser.COL_FIELD_TYPE_BOOL - 42)) | (1 << (ZmeiLangParser.COL_FIELD_TYPE_ONE - 42)) | (1 << (ZmeiLangParser.COL_FIELD_TYPE_ONE2ONE - 42)) | (1 << (ZmeiLangParser.COL_FIELD_TYPE_MANY - 42)) | (1 << (ZmeiLangParser.COL_FIELD_CHOICES - 42)) | (1 << (ZmeiLangParser.KW_THEME - 42)) | (1 << (ZmeiLangParser.KW_INSTALL - 42)) | (1 << (ZmeiLangParser.KW_HEADER - 42)) | (1 << (ZmeiLangParser.KW_SERVICES - 42)) | (1 << (ZmeiLangParser.KW_SELENIUM_PYTEST - 42)) | (1 << (ZmeiLangParser.KW_CHILD - 42)) | (1 << (ZmeiLangParser.KW_FILTER_OUT - 42)) | (1 << (ZmeiLangParser.KW_FILTER_IN - 42)) | (1 << (ZmeiLangParser.KW_PAGE - 42)) | (1 << (ZmeiLangParser.KW_LINK_SUFFIX - 42)) | (1 << (ZmeiLangParser.KW_URL_PREFIX - 42)) | (1 << (ZmeiLangParser.KW_CAN_EDIT - 42)) | (1 << (ZmeiLangParser.KW_OBJECT_EXPR - 42)) | (1 << (ZmeiLangParser.KW_BLOCK - 42)) | (1 << (ZmeiLangParser.KW_ITEM_NAME - 42)) | (1 << (ZmeiLangParser.KW_PK_PARAM - 42)) | (1 << (ZmeiLangParser.KW_LIST_FIELDS - 42)) | (1 << (ZmeiLangParser.KW_DELETE - 42)) | (1 << (ZmeiLangParser.KW_EDIT - 42)) | (1 << (ZmeiLangParser.KW_CREATE - 42)) | (1 << (ZmeiLangParser.KW_DETAIL - 42)) | (1 << (ZmeiLangParser.KW_SKIP - 42)) | (1 << (ZmeiLangParser.KW_FROM - 42)) | (1 << (ZmeiLangParser.KW_POLY_LIST - 42)) | (1 << (ZmeiLangParser.KW_CSS - 42)) | (1 << (ZmeiLangParser.KW_JS - 42)) | (1 << (ZmeiLangParser.KW_INLINE_TYPE_TABULAR - 42)) | (1 << (ZmeiLangParser.KW_INLINE_TYPE_STACKED - 42)) | (1 << (ZmeiLangParser.KW_INLINE_TYPE_POLYMORPHIC - 42)) | (1 << (ZmeiLangParser.KW_INLINE - 42)) | (1 << (ZmeiLangParser.KW_TYPE - 42)) | (1 << (ZmeiLangParser.KW_USER_FIELD - 42)) | (1 << (ZmeiLangParser.KW_ANNOTATE - 42)) | (1 << (ZmeiLangParser.KW_ON_CREATE - 42)) | (1 << (ZmeiLangParser.KW_QUERY - 42)) | (1 << (ZmeiLangParser.KW_AUTH - 42)) | (1 << (ZmeiLangParser.KW_COUNT - 42)) | (1 << (ZmeiLangParser.KW_I18N - 42)))) != 0) or ((((_la - 106)) & ~0x3f) == 0 and ((1 << (_la - 106)) & ((1 << (ZmeiLangParser.KW_EXTENSION - 106)) | (1 << (ZmeiLangParser.KW_TABS - 106)) | (1 << (ZmeiLangParser.KW_LIST - 106)) | (1 << (ZmeiLangParser.KW_READ_ONLY - 106)) | (1 << (ZmeiLangParser.KW_LIST_EDITABLE - 106)) | (1 << (ZmeiLangParser.KW_LIST_FILTER - 106)) | (1 << (ZmeiLangParser.KW_LIST_SEARCH - 106)) | (1 << (ZmeiLangParser.KW_FIELDS - 106)) | (1 << (ZmeiLangParser.KW_IMPORT - 106)) | (1 << (ZmeiLangParser.KW_AS - 106)) | (1 << (ZmeiLangParser.WRITE_MODE - 106)) | (1 << (ZmeiLangParser.BOOL - 106)) | (1 << (ZmeiLangParser.NL - 106)) | (1 << (ZmeiLangParser.ID - 106)) | (1 << (ZmeiLangParser.HASH - 106)))) != 0)):
                    break

            self.state = 2053
            self.match(ZmeiLangParser.BRACE_CLOSE)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class An_stream_modelContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def an_stream_target_model(self):
            return self.getTypedRuleContext(ZmeiLangParser.An_stream_target_modelContext,0)


        def an_stream_target_filter(self):
            return self.getTypedRuleContext(ZmeiLangParser.An_stream_target_filterContext,0)


        def an_stream_field_list(self):
            return self.getTypedRuleContext(ZmeiLangParser.An_stream_field_listContext,0)


        def COMA(self):
            return self.getToken(ZmeiLangParser.COMA, 0)

        def NL(self):
            return self.getToken(ZmeiLangParser.NL, 0)

        def getRuleIndex(self):
            return ZmeiLangParser.RULE_an_stream_model

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAn_stream_model" ):
                listener.enterAn_stream_model(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAn_stream_model" ):
                listener.exitAn_stream_model(self)




    def an_stream_model(self):

        localctx = ZmeiLangParser.An_stream_modelContext(self, self._ctx, self.state)
        self.enterRule(localctx, 410, self.RULE_an_stream_model)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 2055
            self.an_stream_target_model()
            self.state = 2057
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==ZmeiLangParser.CODE_BLOCK:
                self.state = 2056
                self.an_stream_target_filter()


            self.state = 2060
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==ZmeiLangParser.EQUALS:
                self.state = 2059
                self.an_stream_field_list()


            self.state = 2063
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==ZmeiLangParser.COMA:
                self.state = 2062
                self.match(ZmeiLangParser.COMA)


            self.state = 2066
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,210,self._ctx)
            if la_ == 1:
                self.state = 2065
                self.match(ZmeiLangParser.NL)


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class An_stream_target_modelContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def model_ref(self):
            return self.getTypedRuleContext(ZmeiLangParser.Model_refContext,0)


        def classname(self):
            return self.getTypedRuleContext(ZmeiLangParser.ClassnameContext,0)


        def getRuleIndex(self):
            return ZmeiLangParser.RULE_an_stream_target_model

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAn_stream_target_model" ):
                listener.enterAn_stream_target_model(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAn_stream_target_model" ):
                listener.exitAn_stream_target_model(self)




    def an_stream_target_model(self):

        localctx = ZmeiLangParser.An_stream_target_modelContext(self, self._ctx, self.state)
        self.enterRule(localctx, 412, self.RULE_an_stream_target_model)
        try:
            self.state = 2070
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [ZmeiLangParser.HASH]:
                self.enterOuterAlt(localctx, 1)
                self.state = 2068
                self.model_ref()
                pass
            elif token in [ZmeiLangParser.KW_AUTH_TYPE_BASIC, ZmeiLangParser.KW_AUTH_TYPE_SESSION, ZmeiLangParser.KW_AUTH_TYPE_TOKEN, ZmeiLangParser.COL_FIELD_TYPE_LONGTEXT, ZmeiLangParser.COL_FIELD_TYPE_HTML, ZmeiLangParser.COL_FIELD_TYPE_HTML_MEDIA, ZmeiLangParser.COL_FIELD_TYPE_FLOAT, ZmeiLangParser.COL_FIELD_TYPE_DECIMAL, ZmeiLangParser.COL_FIELD_TYPE_DATE, ZmeiLangParser.COL_FIELD_TYPE_DATETIME, ZmeiLangParser.COL_FIELD_TYPE_CREATE_TIME, ZmeiLangParser.COL_FIELD_TYPE_UPDATE_TIME, ZmeiLangParser.COL_FIELD_TYPE_IMAGE, ZmeiLangParser.COL_FIELD_TYPE_FILE, ZmeiLangParser.COL_FIELD_TYPE_FILER_IMAGE, ZmeiLangParser.COL_FIELD_TYPE_FILER_FILE, ZmeiLangParser.COL_FIELD_TYPE_FILER_FOLDER, ZmeiLangParser.COL_FIELD_TYPE_FILER_IMAGE_FOLDER, ZmeiLangParser.COL_FIELD_TYPE_TEXT, ZmeiLangParser.COL_FIELD_TYPE_INT, ZmeiLangParser.COL_FIELD_TYPE_SLUG, ZmeiLangParser.COL_FIELD_TYPE_BOOL, ZmeiLangParser.COL_FIELD_TYPE_ONE, ZmeiLangParser.COL_FIELD_TYPE_ONE2ONE, ZmeiLangParser.COL_FIELD_TYPE_MANY, ZmeiLangParser.COL_FIELD_CHOICES, ZmeiLangParser.KW_THEME, ZmeiLangParser.KW_INSTALL, ZmeiLangParser.KW_HEADER, ZmeiLangParser.KW_SERVICES, ZmeiLangParser.KW_SELENIUM_PYTEST, ZmeiLangParser.KW_CHILD, ZmeiLangParser.KW_FILTER_OUT, ZmeiLangParser.KW_FILTER_IN, ZmeiLangParser.KW_PAGE, ZmeiLangParser.KW_LINK_SUFFIX, ZmeiLangParser.KW_URL_PREFIX, ZmeiLangParser.KW_CAN_EDIT, ZmeiLangParser.KW_OBJECT_EXPR, ZmeiLangParser.KW_BLOCK, ZmeiLangParser.KW_ITEM_NAME, ZmeiLangParser.KW_PK_PARAM, ZmeiLangParser.KW_LIST_FIELDS, ZmeiLangParser.KW_DELETE, ZmeiLangParser.KW_EDIT, ZmeiLangParser.KW_CREATE, ZmeiLangParser.KW_DETAIL, ZmeiLangParser.KW_SKIP, ZmeiLangParser.KW_FROM, ZmeiLangParser.KW_POLY_LIST, ZmeiLangParser.KW_CSS, ZmeiLangParser.KW_JS, ZmeiLangParser.KW_INLINE_TYPE_TABULAR, ZmeiLangParser.KW_INLINE_TYPE_STACKED, ZmeiLangParser.KW_INLINE_TYPE_POLYMORPHIC, ZmeiLangParser.KW_INLINE, ZmeiLangParser.KW_TYPE, ZmeiLangParser.KW_USER_FIELD, ZmeiLangParser.KW_ANNOTATE, ZmeiLangParser.KW_ON_CREATE, ZmeiLangParser.KW_QUERY, ZmeiLangParser.KW_AUTH, ZmeiLangParser.KW_COUNT, ZmeiLangParser.KW_I18N, ZmeiLangParser.KW_EXTENSION, ZmeiLangParser.KW_TABS, ZmeiLangParser.KW_LIST, ZmeiLangParser.KW_READ_ONLY, ZmeiLangParser.KW_LIST_EDITABLE, ZmeiLangParser.KW_LIST_FILTER, ZmeiLangParser.KW_LIST_SEARCH, ZmeiLangParser.KW_FIELDS, ZmeiLangParser.KW_IMPORT, ZmeiLangParser.KW_AS, ZmeiLangParser.WRITE_MODE, ZmeiLangParser.BOOL, ZmeiLangParser.ID]:
                self.enterOuterAlt(localctx, 2)
                self.state = 2069
                self.classname()
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class An_stream_target_filterContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def code_block(self):
            return self.getTypedRuleContext(ZmeiLangParser.Code_blockContext,0)


        def getRuleIndex(self):
            return ZmeiLangParser.RULE_an_stream_target_filter

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAn_stream_target_filter" ):
                listener.enterAn_stream_target_filter(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAn_stream_target_filter" ):
                listener.exitAn_stream_target_filter(self)




    def an_stream_target_filter(self):

        localctx = ZmeiLangParser.An_stream_target_filterContext(self, self._ctx, self.state)
        self.enterRule(localctx, 414, self.RULE_an_stream_target_filter)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 2072
            self.code_block()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class An_stream_field_listContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def EQUALS(self):
            return self.getToken(ZmeiLangParser.EQUALS, 0)

        def GT(self):
            return self.getToken(ZmeiLangParser.GT, 0)

        def STAR(self):
            return self.getToken(ZmeiLangParser.STAR, 0)

        def an_stream_field_name(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(ZmeiLangParser.An_stream_field_nameContext)
            else:
                return self.getTypedRuleContext(ZmeiLangParser.An_stream_field_nameContext,i)


        def COMA(self, i:int=None):
            if i is None:
                return self.getTokens(ZmeiLangParser.COMA)
            else:
                return self.getToken(ZmeiLangParser.COMA, i)

        def getRuleIndex(self):
            return ZmeiLangParser.RULE_an_stream_field_list

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAn_stream_field_list" ):
                listener.enterAn_stream_field_list(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAn_stream_field_list" ):
                listener.exitAn_stream_field_list(self)




    def an_stream_field_list(self):

        localctx = ZmeiLangParser.An_stream_field_listContext(self, self._ctx, self.state)
        self.enterRule(localctx, 416, self.RULE_an_stream_field_list)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 2074
            self.match(ZmeiLangParser.EQUALS)
            self.state = 2075
            self.match(ZmeiLangParser.GT)
            self.state = 2085
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [ZmeiLangParser.STAR]:
                self.state = 2076
                self.match(ZmeiLangParser.STAR)
                pass
            elif token in [ZmeiLangParser.KW_AUTH_TYPE_BASIC, ZmeiLangParser.KW_AUTH_TYPE_SESSION, ZmeiLangParser.KW_AUTH_TYPE_TOKEN, ZmeiLangParser.COL_FIELD_TYPE_LONGTEXT, ZmeiLangParser.COL_FIELD_TYPE_HTML, ZmeiLangParser.COL_FIELD_TYPE_HTML_MEDIA, ZmeiLangParser.COL_FIELD_TYPE_FLOAT, ZmeiLangParser.COL_FIELD_TYPE_DECIMAL, ZmeiLangParser.COL_FIELD_TYPE_DATE, ZmeiLangParser.COL_FIELD_TYPE_DATETIME, ZmeiLangParser.COL_FIELD_TYPE_CREATE_TIME, ZmeiLangParser.COL_FIELD_TYPE_UPDATE_TIME, ZmeiLangParser.COL_FIELD_TYPE_IMAGE, ZmeiLangParser.COL_FIELD_TYPE_FILE, ZmeiLangParser.COL_FIELD_TYPE_FILER_IMAGE, ZmeiLangParser.COL_FIELD_TYPE_FILER_FILE, ZmeiLangParser.COL_FIELD_TYPE_FILER_FOLDER, ZmeiLangParser.COL_FIELD_TYPE_FILER_IMAGE_FOLDER, ZmeiLangParser.COL_FIELD_TYPE_TEXT, ZmeiLangParser.COL_FIELD_TYPE_INT, ZmeiLangParser.COL_FIELD_TYPE_SLUG, ZmeiLangParser.COL_FIELD_TYPE_BOOL, ZmeiLangParser.COL_FIELD_TYPE_ONE, ZmeiLangParser.COL_FIELD_TYPE_ONE2ONE, ZmeiLangParser.COL_FIELD_TYPE_MANY, ZmeiLangParser.COL_FIELD_CHOICES, ZmeiLangParser.KW_THEME, ZmeiLangParser.KW_INSTALL, ZmeiLangParser.KW_HEADER, ZmeiLangParser.KW_SERVICES, ZmeiLangParser.KW_SELENIUM_PYTEST, ZmeiLangParser.KW_CHILD, ZmeiLangParser.KW_FILTER_OUT, ZmeiLangParser.KW_FILTER_IN, ZmeiLangParser.KW_PAGE, ZmeiLangParser.KW_LINK_SUFFIX, ZmeiLangParser.KW_URL_PREFIX, ZmeiLangParser.KW_CAN_EDIT, ZmeiLangParser.KW_OBJECT_EXPR, ZmeiLangParser.KW_BLOCK, ZmeiLangParser.KW_ITEM_NAME, ZmeiLangParser.KW_PK_PARAM, ZmeiLangParser.KW_LIST_FIELDS, ZmeiLangParser.KW_DELETE, ZmeiLangParser.KW_EDIT, ZmeiLangParser.KW_CREATE, ZmeiLangParser.KW_DETAIL, ZmeiLangParser.KW_SKIP, ZmeiLangParser.KW_FROM, ZmeiLangParser.KW_POLY_LIST, ZmeiLangParser.KW_CSS, ZmeiLangParser.KW_JS, ZmeiLangParser.KW_INLINE_TYPE_TABULAR, ZmeiLangParser.KW_INLINE_TYPE_STACKED, ZmeiLangParser.KW_INLINE_TYPE_POLYMORPHIC, ZmeiLangParser.KW_INLINE, ZmeiLangParser.KW_TYPE, ZmeiLangParser.KW_USER_FIELD, ZmeiLangParser.KW_ANNOTATE, ZmeiLangParser.KW_ON_CREATE, ZmeiLangParser.KW_QUERY, ZmeiLangParser.KW_AUTH, ZmeiLangParser.KW_COUNT, ZmeiLangParser.KW_I18N, ZmeiLangParser.KW_EXTENSION, ZmeiLangParser.KW_TABS, ZmeiLangParser.KW_LIST, ZmeiLangParser.KW_READ_ONLY, ZmeiLangParser.KW_LIST_EDITABLE, ZmeiLangParser.KW_LIST_FILTER, ZmeiLangParser.KW_LIST_SEARCH, ZmeiLangParser.KW_FIELDS, ZmeiLangParser.KW_IMPORT, ZmeiLangParser.KW_AS, ZmeiLangParser.WRITE_MODE, ZmeiLangParser.BOOL, ZmeiLangParser.ID]:
                self.state = 2077
                self.an_stream_field_name()
                self.state = 2082
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,212,self._ctx)
                while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                    if _alt==1:
                        self.state = 2078
                        self.match(ZmeiLangParser.COMA)
                        self.state = 2079
                        self.an_stream_field_name() 
                    self.state = 2084
                    self._errHandler.sync(self)
                    _alt = self._interp.adaptivePredict(self._input,212,self._ctx)

                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class An_stream_field_nameContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def id_or_kw(self):
            return self.getTypedRuleContext(ZmeiLangParser.Id_or_kwContext,0)


        def getRuleIndex(self):
            return ZmeiLangParser.RULE_an_stream_field_name

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAn_stream_field_name" ):
                listener.enterAn_stream_field_name(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAn_stream_field_name" ):
                listener.exitAn_stream_field_name(self)




    def an_stream_field_name(self):

        localctx = ZmeiLangParser.An_stream_field_nameContext(self, self._ctx, self.state)
        self.enterRule(localctx, 418, self.RULE_an_stream_field_name)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 2087
            self.id_or_kw()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class An_reactContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def an_react_type(self):
            return self.getTypedRuleContext(ZmeiLangParser.An_react_typeContext,0)


        def DOT(self):
            return self.getToken(ZmeiLangParser.DOT, 0)

        def an_react_descriptor(self):
            return self.getTypedRuleContext(ZmeiLangParser.An_react_descriptorContext,0)


        def BRACE_OPEN(self):
            return self.getToken(ZmeiLangParser.BRACE_OPEN, 0)

        def BRACE_CLOSE(self):
            return self.getToken(ZmeiLangParser.BRACE_CLOSE, 0)

        def an_react_child(self):
            return self.getTypedRuleContext(ZmeiLangParser.An_react_childContext,0)


        def getRuleIndex(self):
            return ZmeiLangParser.RULE_an_react

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAn_react" ):
                listener.enterAn_react(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAn_react" ):
                listener.exitAn_react(self)




    def an_react(self):

        localctx = ZmeiLangParser.An_reactContext(self, self._ctx, self.state)
        self.enterRule(localctx, 420, self.RULE_an_react)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 2089
            self.an_react_type()
            self.state = 2092
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==ZmeiLangParser.DOT:
                self.state = 2090
                self.match(ZmeiLangParser.DOT)
                self.state = 2091
                self.an_react_descriptor()


            self.state = 2099
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==ZmeiLangParser.BRACE_OPEN:
                self.state = 2094
                self.match(ZmeiLangParser.BRACE_OPEN)
                self.state = 2096
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==ZmeiLangParser.KW_CHILD:
                    self.state = 2095
                    self.an_react_child()


                self.state = 2098
                self.match(ZmeiLangParser.BRACE_CLOSE)


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class An_react_typeContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def AN_REACT(self):
            return self.getToken(ZmeiLangParser.AN_REACT, 0)

        def AN_REACT_CLIENT(self):
            return self.getToken(ZmeiLangParser.AN_REACT_CLIENT, 0)

        def AN_REACT_SERVER(self):
            return self.getToken(ZmeiLangParser.AN_REACT_SERVER, 0)

        def getRuleIndex(self):
            return ZmeiLangParser.RULE_an_react_type

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAn_react_type" ):
                listener.enterAn_react_type(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAn_react_type" ):
                listener.exitAn_react_type(self)




    def an_react_type(self):

        localctx = ZmeiLangParser.An_react_typeContext(self, self._ctx, self.state)
        self.enterRule(localctx, 422, self.RULE_an_react_type)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 2101
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << ZmeiLangParser.AN_REACT) | (1 << ZmeiLangParser.AN_REACT_CLIENT) | (1 << ZmeiLangParser.AN_REACT_SERVER))) != 0)):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class An_react_descriptorContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def id_or_kw(self):
            return self.getTypedRuleContext(ZmeiLangParser.Id_or_kwContext,0)


        def getRuleIndex(self):
            return ZmeiLangParser.RULE_an_react_descriptor

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAn_react_descriptor" ):
                listener.enterAn_react_descriptor(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAn_react_descriptor" ):
                listener.exitAn_react_descriptor(self)




    def an_react_descriptor(self):

        localctx = ZmeiLangParser.An_react_descriptorContext(self, self._ctx, self.state)
        self.enterRule(localctx, 424, self.RULE_an_react_descriptor)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 2103
            self.id_or_kw()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class An_react_childContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def KW_CHILD(self):
            return self.getToken(ZmeiLangParser.KW_CHILD, 0)

        def COLON(self):
            return self.getToken(ZmeiLangParser.COLON, 0)

        def BOOL(self):
            return self.getToken(ZmeiLangParser.BOOL, 0)

        def getRuleIndex(self):
            return ZmeiLangParser.RULE_an_react_child

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAn_react_child" ):
                listener.enterAn_react_child(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAn_react_child" ):
                listener.exitAn_react_child(self)




    def an_react_child(self):

        localctx = ZmeiLangParser.An_react_childContext(self, self._ctx, self.state)
        self.enterRule(localctx, 426, self.RULE_an_react_child)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 2105
            self.match(ZmeiLangParser.KW_CHILD)
            self.state = 2106
            self.match(ZmeiLangParser.COLON)
            self.state = 2107
            self.match(ZmeiLangParser.BOOL)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class An_htmlContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def AN_HTML(self):
            return self.getToken(ZmeiLangParser.AN_HTML, 0)

        def code_block(self):
            return self.getTypedRuleContext(ZmeiLangParser.Code_blockContext,0)


        def DOT(self):
            return self.getToken(ZmeiLangParser.DOT, 0)

        def an_html_descriptor(self):
            return self.getTypedRuleContext(ZmeiLangParser.An_html_descriptorContext,0)


        def getRuleIndex(self):
            return ZmeiLangParser.RULE_an_html

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAn_html" ):
                listener.enterAn_html(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAn_html" ):
                listener.exitAn_html(self)




    def an_html(self):

        localctx = ZmeiLangParser.An_htmlContext(self, self._ctx, self.state)
        self.enterRule(localctx, 428, self.RULE_an_html)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 2109
            self.match(ZmeiLangParser.AN_HTML)
            self.state = 2112
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==ZmeiLangParser.DOT:
                self.state = 2110
                self.match(ZmeiLangParser.DOT)
                self.state = 2111
                self.an_html_descriptor()


            self.state = 2114
            self.code_block()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class An_html_descriptorContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def id_or_kw(self):
            return self.getTypedRuleContext(ZmeiLangParser.Id_or_kwContext,0)


        def getRuleIndex(self):
            return ZmeiLangParser.RULE_an_html_descriptor

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAn_html_descriptor" ):
                listener.enterAn_html_descriptor(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAn_html_descriptor" ):
                listener.exitAn_html_descriptor(self)




    def an_html_descriptor(self):

        localctx = ZmeiLangParser.An_html_descriptorContext(self, self._ctx, self.state)
        self.enterRule(localctx, 430, self.RULE_an_html_descriptor)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 2116
            self.id_or_kw()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class An_markdownContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def AN_MARKDOWN(self):
            return self.getToken(ZmeiLangParser.AN_MARKDOWN, 0)

        def code_block(self):
            return self.getTypedRuleContext(ZmeiLangParser.Code_blockContext,0)


        def DOT(self):
            return self.getToken(ZmeiLangParser.DOT, 0)

        def an_markdown_descriptor(self):
            return self.getTypedRuleContext(ZmeiLangParser.An_markdown_descriptorContext,0)


        def getRuleIndex(self):
            return ZmeiLangParser.RULE_an_markdown

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAn_markdown" ):
                listener.enterAn_markdown(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAn_markdown" ):
                listener.exitAn_markdown(self)




    def an_markdown(self):

        localctx = ZmeiLangParser.An_markdownContext(self, self._ctx, self.state)
        self.enterRule(localctx, 432, self.RULE_an_markdown)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 2118
            self.match(ZmeiLangParser.AN_MARKDOWN)
            self.state = 2121
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==ZmeiLangParser.DOT:
                self.state = 2119
                self.match(ZmeiLangParser.DOT)
                self.state = 2120
                self.an_markdown_descriptor()


            self.state = 2123
            self.code_block()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class An_markdown_descriptorContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def id_or_kw(self):
            return self.getTypedRuleContext(ZmeiLangParser.Id_or_kwContext,0)


        def getRuleIndex(self):
            return ZmeiLangParser.RULE_an_markdown_descriptor

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAn_markdown_descriptor" ):
                listener.enterAn_markdown_descriptor(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAn_markdown_descriptor" ):
                listener.exitAn_markdown_descriptor(self)




    def an_markdown_descriptor(self):

        localctx = ZmeiLangParser.An_markdown_descriptorContext(self, self._ctx, self.state)
        self.enterRule(localctx, 434, self.RULE_an_markdown_descriptor)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 2125
            self.id_or_kw()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class An_crud_deleteContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def AN_CRUD_DELETE(self):
            return self.getToken(ZmeiLangParser.AN_CRUD_DELETE, 0)

        def an_crud_params(self):
            return self.getTypedRuleContext(ZmeiLangParser.An_crud_paramsContext,0)


        def getRuleIndex(self):
            return ZmeiLangParser.RULE_an_crud_delete

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAn_crud_delete" ):
                listener.enterAn_crud_delete(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAn_crud_delete" ):
                listener.exitAn_crud_delete(self)




    def an_crud_delete(self):

        localctx = ZmeiLangParser.An_crud_deleteContext(self, self._ctx, self.state)
        self.enterRule(localctx, 436, self.RULE_an_crud_delete)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 2127
            self.match(ZmeiLangParser.AN_CRUD_DELETE)
            self.state = 2128
            self.an_crud_params()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class An_crudContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def AN_CRUD(self):
            return self.getToken(ZmeiLangParser.AN_CRUD, 0)

        def an_crud_params(self):
            return self.getTypedRuleContext(ZmeiLangParser.An_crud_paramsContext,0)


        def getRuleIndex(self):
            return ZmeiLangParser.RULE_an_crud

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAn_crud" ):
                listener.enterAn_crud(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAn_crud" ):
                listener.exitAn_crud(self)




    def an_crud(self):

        localctx = ZmeiLangParser.An_crudContext(self, self._ctx, self.state)
        self.enterRule(localctx, 438, self.RULE_an_crud)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 2130
            self.match(ZmeiLangParser.AN_CRUD)
            self.state = 2131
            self.an_crud_params()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class An_crud_paramsContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def BRACE_OPEN(self):
            return self.getToken(ZmeiLangParser.BRACE_OPEN, 0)

        def an_crud_target_model(self):
            return self.getTypedRuleContext(ZmeiLangParser.An_crud_target_modelContext,0)


        def BRACE_CLOSE(self):
            return self.getToken(ZmeiLangParser.BRACE_CLOSE, 0)

        def DOT(self):
            return self.getToken(ZmeiLangParser.DOT, 0)

        def an_crud_descriptor(self):
            return self.getTypedRuleContext(ZmeiLangParser.An_crud_descriptorContext,0)


        def NL(self, i:int=None):
            if i is None:
                return self.getTokens(ZmeiLangParser.NL)
            else:
                return self.getToken(ZmeiLangParser.NL, i)

        def an_crud_target_filter(self):
            return self.getTypedRuleContext(ZmeiLangParser.An_crud_target_filterContext,0)


        def an_crud_theme(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(ZmeiLangParser.An_crud_themeContext)
            else:
                return self.getTypedRuleContext(ZmeiLangParser.An_crud_themeContext,i)


        def an_crud_skip(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(ZmeiLangParser.An_crud_skipContext)
            else:
                return self.getTypedRuleContext(ZmeiLangParser.An_crud_skipContext,i)


        def an_crud_fields(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(ZmeiLangParser.An_crud_fieldsContext)
            else:
                return self.getTypedRuleContext(ZmeiLangParser.An_crud_fieldsContext,i)


        def an_crud_list_fields(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(ZmeiLangParser.An_crud_list_fieldsContext)
            else:
                return self.getTypedRuleContext(ZmeiLangParser.An_crud_list_fieldsContext,i)


        def an_crud_pk_param(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(ZmeiLangParser.An_crud_pk_paramContext)
            else:
                return self.getTypedRuleContext(ZmeiLangParser.An_crud_pk_paramContext,i)


        def an_crud_item_name(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(ZmeiLangParser.An_crud_item_nameContext)
            else:
                return self.getTypedRuleContext(ZmeiLangParser.An_crud_item_nameContext,i)


        def an_crud_block(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(ZmeiLangParser.An_crud_blockContext)
            else:
                return self.getTypedRuleContext(ZmeiLangParser.An_crud_blockContext,i)


        def an_crud_object_expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(ZmeiLangParser.An_crud_object_exprContext)
            else:
                return self.getTypedRuleContext(ZmeiLangParser.An_crud_object_exprContext,i)


        def an_crud_can_edit(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(ZmeiLangParser.An_crud_can_editContext)
            else:
                return self.getTypedRuleContext(ZmeiLangParser.An_crud_can_editContext,i)


        def an_crud_url_prefix(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(ZmeiLangParser.An_crud_url_prefixContext)
            else:
                return self.getTypedRuleContext(ZmeiLangParser.An_crud_url_prefixContext,i)


        def an_crud_link_suffix(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(ZmeiLangParser.An_crud_link_suffixContext)
            else:
                return self.getTypedRuleContext(ZmeiLangParser.An_crud_link_suffixContext,i)


        def an_crud_list_type(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(ZmeiLangParser.An_crud_list_typeContext)
            else:
                return self.getTypedRuleContext(ZmeiLangParser.An_crud_list_typeContext,i)


        def an_crud_header(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(ZmeiLangParser.An_crud_headerContext)
            else:
                return self.getTypedRuleContext(ZmeiLangParser.An_crud_headerContext,i)


        def COMA(self, i:int=None):
            if i is None:
                return self.getTokens(ZmeiLangParser.COMA)
            else:
                return self.getToken(ZmeiLangParser.COMA, i)

        def an_crud_next_page(self):
            return self.getTypedRuleContext(ZmeiLangParser.An_crud_next_pageContext,0)


        def an_crud_next_page_url(self):
            return self.getTypedRuleContext(ZmeiLangParser.An_crud_next_page_urlContext,0)


        def an_crud_page_override(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(ZmeiLangParser.An_crud_page_overrideContext)
            else:
                return self.getTypedRuleContext(ZmeiLangParser.An_crud_page_overrideContext,i)


        def getRuleIndex(self):
            return ZmeiLangParser.RULE_an_crud_params

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAn_crud_params" ):
                listener.enterAn_crud_params(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAn_crud_params" ):
                listener.exitAn_crud_params(self)




    def an_crud_params(self):

        localctx = ZmeiLangParser.An_crud_paramsContext(self, self._ctx, self.state)
        self.enterRule(localctx, 440, self.RULE_an_crud_params)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 2135
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==ZmeiLangParser.DOT:
                self.state = 2133
                self.match(ZmeiLangParser.DOT)
                self.state = 2134
                self.an_crud_descriptor()


            self.state = 2137
            self.match(ZmeiLangParser.BRACE_OPEN)
            self.state = 2141
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==ZmeiLangParser.NL:
                self.state = 2138
                self.match(ZmeiLangParser.NL)
                self.state = 2143
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 2144
            self.an_crud_target_model()
            self.state = 2146
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==ZmeiLangParser.CODE_BLOCK:
                self.state = 2145
                self.an_crud_target_filter()


            self.state = 2165
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,223,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 2163
                    self._errHandler.sync(self)
                    token = self._input.LA(1)
                    if token in [ZmeiLangParser.KW_THEME]:
                        self.state = 2148
                        self.an_crud_theme()
                        pass
                    elif token in [ZmeiLangParser.KW_SKIP]:
                        self.state = 2149
                        self.an_crud_skip()
                        pass
                    elif token in [ZmeiLangParser.KW_FIELDS]:
                        self.state = 2150
                        self.an_crud_fields()
                        pass
                    elif token in [ZmeiLangParser.KW_LIST_FIELDS]:
                        self.state = 2151
                        self.an_crud_list_fields()
                        pass
                    elif token in [ZmeiLangParser.KW_PK_PARAM]:
                        self.state = 2152
                        self.an_crud_pk_param()
                        pass
                    elif token in [ZmeiLangParser.KW_ITEM_NAME]:
                        self.state = 2153
                        self.an_crud_item_name()
                        pass
                    elif token in [ZmeiLangParser.KW_BLOCK]:
                        self.state = 2154
                        self.an_crud_block()
                        pass
                    elif token in [ZmeiLangParser.KW_OBJECT_EXPR]:
                        self.state = 2155
                        self.an_crud_object_expr()
                        pass
                    elif token in [ZmeiLangParser.KW_CAN_EDIT]:
                        self.state = 2156
                        self.an_crud_can_edit()
                        pass
                    elif token in [ZmeiLangParser.KW_URL_PREFIX]:
                        self.state = 2157
                        self.an_crud_url_prefix()
                        pass
                    elif token in [ZmeiLangParser.KW_LINK_SUFFIX]:
                        self.state = 2158
                        self.an_crud_link_suffix()
                        pass
                    elif token in [ZmeiLangParser.KW_LIST]:
                        self.state = 2159
                        self.an_crud_list_type()
                        pass
                    elif token in [ZmeiLangParser.KW_HEADER]:
                        self.state = 2160
                        self.an_crud_header()
                        pass
                    elif token in [ZmeiLangParser.NL]:
                        self.state = 2161
                        self.match(ZmeiLangParser.NL)
                        pass
                    elif token in [ZmeiLangParser.COMA]:
                        self.state = 2162
                        self.match(ZmeiLangParser.COMA)
                        pass
                    else:
                        raise NoViableAltException(self)
             
                self.state = 2167
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,223,self._ctx)

            self.state = 2171
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,224,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 2168
                    self.match(ZmeiLangParser.NL) 
                self.state = 2173
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,224,self._ctx)

            self.state = 2176
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,225,self._ctx)
            if la_ == 1:
                self.state = 2174
                self.an_crud_next_page()

            elif la_ == 2:
                self.state = 2175
                self.an_crud_next_page_url()


            self.state = 2181
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,226,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 2178
                    self.match(ZmeiLangParser.NL) 
                self.state = 2183
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,226,self._ctx)

            self.state = 2187
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while ((((_la - 85)) & ~0x3f) == 0 and ((1 << (_la - 85)) & ((1 << (ZmeiLangParser.KW_DELETE - 85)) | (1 << (ZmeiLangParser.KW_EDIT - 85)) | (1 << (ZmeiLangParser.KW_CREATE - 85)) | (1 << (ZmeiLangParser.KW_DETAIL - 85)) | (1 << (ZmeiLangParser.KW_LIST - 85)))) != 0):
                self.state = 2184
                self.an_crud_page_override()
                self.state = 2189
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 2193
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==ZmeiLangParser.NL:
                self.state = 2190
                self.match(ZmeiLangParser.NL)
                self.state = 2195
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 2196
            self.match(ZmeiLangParser.BRACE_CLOSE)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class An_crud_page_overrideContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def an_crud_view_name(self):
            return self.getTypedRuleContext(ZmeiLangParser.An_crud_view_nameContext,0)


        def BRACE_OPEN(self):
            return self.getToken(ZmeiLangParser.BRACE_OPEN, 0)

        def page_body(self):
            return self.getTypedRuleContext(ZmeiLangParser.Page_bodyContext,0)


        def BRACE_CLOSE(self):
            return self.getToken(ZmeiLangParser.BRACE_CLOSE, 0)

        def NL(self, i:int=None):
            if i is None:
                return self.getTokens(ZmeiLangParser.NL)
            else:
                return self.getToken(ZmeiLangParser.NL, i)

        def getRuleIndex(self):
            return ZmeiLangParser.RULE_an_crud_page_override

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAn_crud_page_override" ):
                listener.enterAn_crud_page_override(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAn_crud_page_override" ):
                listener.exitAn_crud_page_override(self)




    def an_crud_page_override(self):

        localctx = ZmeiLangParser.An_crud_page_overrideContext(self, self._ctx, self.state)
        self.enterRule(localctx, 442, self.RULE_an_crud_page_override)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 2198
            self.an_crud_view_name()
            self.state = 2202
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==ZmeiLangParser.NL:
                self.state = 2199
                self.match(ZmeiLangParser.NL)
                self.state = 2204
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 2205
            self.match(ZmeiLangParser.BRACE_OPEN)
            self.state = 2209
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,230,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 2206
                    self.match(ZmeiLangParser.NL) 
                self.state = 2211
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,230,self._ctx)

            self.state = 2212
            self.page_body()
            self.state = 2216
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==ZmeiLangParser.NL:
                self.state = 2213
                self.match(ZmeiLangParser.NL)
                self.state = 2218
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 2219
            self.match(ZmeiLangParser.BRACE_CLOSE)
            self.state = 2223
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,232,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 2220
                    self.match(ZmeiLangParser.NL) 
                self.state = 2225
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,232,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class An_crud_descriptorContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def id_or_kw(self):
            return self.getTypedRuleContext(ZmeiLangParser.Id_or_kwContext,0)


        def getRuleIndex(self):
            return ZmeiLangParser.RULE_an_crud_descriptor

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAn_crud_descriptor" ):
                listener.enterAn_crud_descriptor(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAn_crud_descriptor" ):
                listener.exitAn_crud_descriptor(self)




    def an_crud_descriptor(self):

        localctx = ZmeiLangParser.An_crud_descriptorContext(self, self._ctx, self.state)
        self.enterRule(localctx, 444, self.RULE_an_crud_descriptor)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 2226
            self.id_or_kw()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class An_crud_next_pageContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def EQUALS(self):
            return self.getToken(ZmeiLangParser.EQUALS, 0)

        def GT(self):
            return self.getToken(ZmeiLangParser.GT, 0)

        def code_block(self):
            return self.getTypedRuleContext(ZmeiLangParser.Code_blockContext,0)


        def BRACE_OPEN(self):
            return self.getToken(ZmeiLangParser.BRACE_OPEN, 0)

        def an_crud_next_page_event_name(self):
            return self.getTypedRuleContext(ZmeiLangParser.An_crud_next_page_event_nameContext,0)


        def BRACE_CLOSE(self):
            return self.getToken(ZmeiLangParser.BRACE_CLOSE, 0)

        def getRuleIndex(self):
            return ZmeiLangParser.RULE_an_crud_next_page

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAn_crud_next_page" ):
                listener.enterAn_crud_next_page(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAn_crud_next_page" ):
                listener.exitAn_crud_next_page(self)




    def an_crud_next_page(self):

        localctx = ZmeiLangParser.An_crud_next_pageContext(self, self._ctx, self.state)
        self.enterRule(localctx, 446, self.RULE_an_crud_next_page)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 2232
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==ZmeiLangParser.BRACE_OPEN:
                self.state = 2228
                self.match(ZmeiLangParser.BRACE_OPEN)
                self.state = 2229
                self.an_crud_next_page_event_name()
                self.state = 2230
                self.match(ZmeiLangParser.BRACE_CLOSE)


            self.state = 2234
            self.match(ZmeiLangParser.EQUALS)
            self.state = 2235
            self.match(ZmeiLangParser.GT)
            self.state = 2236
            self.code_block()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class An_crud_next_page_event_nameContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def KW_DELETE(self):
            return self.getToken(ZmeiLangParser.KW_DELETE, 0)

        def KW_CREATE(self):
            return self.getToken(ZmeiLangParser.KW_CREATE, 0)

        def KW_EDIT(self):
            return self.getToken(ZmeiLangParser.KW_EDIT, 0)

        def getRuleIndex(self):
            return ZmeiLangParser.RULE_an_crud_next_page_event_name

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAn_crud_next_page_event_name" ):
                listener.enterAn_crud_next_page_event_name(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAn_crud_next_page_event_name" ):
                listener.exitAn_crud_next_page_event_name(self)




    def an_crud_next_page_event_name(self):

        localctx = ZmeiLangParser.An_crud_next_page_event_nameContext(self, self._ctx, self.state)
        self.enterRule(localctx, 448, self.RULE_an_crud_next_page_event_name)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 2238
            _la = self._input.LA(1)
            if not(((((_la - 85)) & ~0x3f) == 0 and ((1 << (_la - 85)) & ((1 << (ZmeiLangParser.KW_DELETE - 85)) | (1 << (ZmeiLangParser.KW_EDIT - 85)) | (1 << (ZmeiLangParser.KW_CREATE - 85)))) != 0)):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class An_crud_next_page_urlContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def EQUALS(self):
            return self.getToken(ZmeiLangParser.EQUALS, 0)

        def GT(self):
            return self.getToken(ZmeiLangParser.GT, 0)

        def an_crud_next_page_url_val(self):
            return self.getTypedRuleContext(ZmeiLangParser.An_crud_next_page_url_valContext,0)


        def BRACE_OPEN(self):
            return self.getToken(ZmeiLangParser.BRACE_OPEN, 0)

        def an_crud_next_page_event_name(self):
            return self.getTypedRuleContext(ZmeiLangParser.An_crud_next_page_event_nameContext,0)


        def BRACE_CLOSE(self):
            return self.getToken(ZmeiLangParser.BRACE_CLOSE, 0)

        def getRuleIndex(self):
            return ZmeiLangParser.RULE_an_crud_next_page_url

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAn_crud_next_page_url" ):
                listener.enterAn_crud_next_page_url(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAn_crud_next_page_url" ):
                listener.exitAn_crud_next_page_url(self)




    def an_crud_next_page_url(self):

        localctx = ZmeiLangParser.An_crud_next_page_urlContext(self, self._ctx, self.state)
        self.enterRule(localctx, 450, self.RULE_an_crud_next_page_url)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 2244
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==ZmeiLangParser.BRACE_OPEN:
                self.state = 2240
                self.match(ZmeiLangParser.BRACE_OPEN)
                self.state = 2241
                self.an_crud_next_page_event_name()
                self.state = 2242
                self.match(ZmeiLangParser.BRACE_CLOSE)


            self.state = 2246
            self.match(ZmeiLangParser.EQUALS)
            self.state = 2247
            self.match(ZmeiLangParser.GT)
            self.state = 2248
            self.an_crud_next_page_url_val()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class An_crud_next_page_url_valContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def STRING_DQ(self):
            return self.getToken(ZmeiLangParser.STRING_DQ, 0)

        def STRING_SQ(self):
            return self.getToken(ZmeiLangParser.STRING_SQ, 0)

        def getRuleIndex(self):
            return ZmeiLangParser.RULE_an_crud_next_page_url_val

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAn_crud_next_page_url_val" ):
                listener.enterAn_crud_next_page_url_val(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAn_crud_next_page_url_val" ):
                listener.exitAn_crud_next_page_url_val(self)




    def an_crud_next_page_url_val(self):

        localctx = ZmeiLangParser.An_crud_next_page_url_valContext(self, self._ctx, self.state)
        self.enterRule(localctx, 452, self.RULE_an_crud_next_page_url_val)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 2250
            _la = self._input.LA(1)
            if not(_la==ZmeiLangParser.STRING_DQ or _la==ZmeiLangParser.STRING_SQ):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class An_crud_target_modelContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def model_ref(self):
            return self.getTypedRuleContext(ZmeiLangParser.Model_refContext,0)


        def classname(self):
            return self.getTypedRuleContext(ZmeiLangParser.ClassnameContext,0)


        def getRuleIndex(self):
            return ZmeiLangParser.RULE_an_crud_target_model

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAn_crud_target_model" ):
                listener.enterAn_crud_target_model(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAn_crud_target_model" ):
                listener.exitAn_crud_target_model(self)




    def an_crud_target_model(self):

        localctx = ZmeiLangParser.An_crud_target_modelContext(self, self._ctx, self.state)
        self.enterRule(localctx, 454, self.RULE_an_crud_target_model)
        try:
            self.state = 2254
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [ZmeiLangParser.HASH]:
                self.enterOuterAlt(localctx, 1)
                self.state = 2252
                self.model_ref()
                pass
            elif token in [ZmeiLangParser.KW_AUTH_TYPE_BASIC, ZmeiLangParser.KW_AUTH_TYPE_SESSION, ZmeiLangParser.KW_AUTH_TYPE_TOKEN, ZmeiLangParser.COL_FIELD_TYPE_LONGTEXT, ZmeiLangParser.COL_FIELD_TYPE_HTML, ZmeiLangParser.COL_FIELD_TYPE_HTML_MEDIA, ZmeiLangParser.COL_FIELD_TYPE_FLOAT, ZmeiLangParser.COL_FIELD_TYPE_DECIMAL, ZmeiLangParser.COL_FIELD_TYPE_DATE, ZmeiLangParser.COL_FIELD_TYPE_DATETIME, ZmeiLangParser.COL_FIELD_TYPE_CREATE_TIME, ZmeiLangParser.COL_FIELD_TYPE_UPDATE_TIME, ZmeiLangParser.COL_FIELD_TYPE_IMAGE, ZmeiLangParser.COL_FIELD_TYPE_FILE, ZmeiLangParser.COL_FIELD_TYPE_FILER_IMAGE, ZmeiLangParser.COL_FIELD_TYPE_FILER_FILE, ZmeiLangParser.COL_FIELD_TYPE_FILER_FOLDER, ZmeiLangParser.COL_FIELD_TYPE_FILER_IMAGE_FOLDER, ZmeiLangParser.COL_FIELD_TYPE_TEXT, ZmeiLangParser.COL_FIELD_TYPE_INT, ZmeiLangParser.COL_FIELD_TYPE_SLUG, ZmeiLangParser.COL_FIELD_TYPE_BOOL, ZmeiLangParser.COL_FIELD_TYPE_ONE, ZmeiLangParser.COL_FIELD_TYPE_ONE2ONE, ZmeiLangParser.COL_FIELD_TYPE_MANY, ZmeiLangParser.COL_FIELD_CHOICES, ZmeiLangParser.KW_THEME, ZmeiLangParser.KW_INSTALL, ZmeiLangParser.KW_HEADER, ZmeiLangParser.KW_SERVICES, ZmeiLangParser.KW_SELENIUM_PYTEST, ZmeiLangParser.KW_CHILD, ZmeiLangParser.KW_FILTER_OUT, ZmeiLangParser.KW_FILTER_IN, ZmeiLangParser.KW_PAGE, ZmeiLangParser.KW_LINK_SUFFIX, ZmeiLangParser.KW_URL_PREFIX, ZmeiLangParser.KW_CAN_EDIT, ZmeiLangParser.KW_OBJECT_EXPR, ZmeiLangParser.KW_BLOCK, ZmeiLangParser.KW_ITEM_NAME, ZmeiLangParser.KW_PK_PARAM, ZmeiLangParser.KW_LIST_FIELDS, ZmeiLangParser.KW_DELETE, ZmeiLangParser.KW_EDIT, ZmeiLangParser.KW_CREATE, ZmeiLangParser.KW_DETAIL, ZmeiLangParser.KW_SKIP, ZmeiLangParser.KW_FROM, ZmeiLangParser.KW_POLY_LIST, ZmeiLangParser.KW_CSS, ZmeiLangParser.KW_JS, ZmeiLangParser.KW_INLINE_TYPE_TABULAR, ZmeiLangParser.KW_INLINE_TYPE_STACKED, ZmeiLangParser.KW_INLINE_TYPE_POLYMORPHIC, ZmeiLangParser.KW_INLINE, ZmeiLangParser.KW_TYPE, ZmeiLangParser.KW_USER_FIELD, ZmeiLangParser.KW_ANNOTATE, ZmeiLangParser.KW_ON_CREATE, ZmeiLangParser.KW_QUERY, ZmeiLangParser.KW_AUTH, ZmeiLangParser.KW_COUNT, ZmeiLangParser.KW_I18N, ZmeiLangParser.KW_EXTENSION, ZmeiLangParser.KW_TABS, ZmeiLangParser.KW_LIST, ZmeiLangParser.KW_READ_ONLY, ZmeiLangParser.KW_LIST_EDITABLE, ZmeiLangParser.KW_LIST_FILTER, ZmeiLangParser.KW_LIST_SEARCH, ZmeiLangParser.KW_FIELDS, ZmeiLangParser.KW_IMPORT, ZmeiLangParser.KW_AS, ZmeiLangParser.WRITE_MODE, ZmeiLangParser.BOOL, ZmeiLangParser.ID]:
                self.enterOuterAlt(localctx, 2)
                self.state = 2253
                self.classname()
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class An_crud_target_filterContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def code_block(self):
            return self.getTypedRuleContext(ZmeiLangParser.Code_blockContext,0)


        def getRuleIndex(self):
            return ZmeiLangParser.RULE_an_crud_target_filter

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAn_crud_target_filter" ):
                listener.enterAn_crud_target_filter(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAn_crud_target_filter" ):
                listener.exitAn_crud_target_filter(self)




    def an_crud_target_filter(self):

        localctx = ZmeiLangParser.An_crud_target_filterContext(self, self._ctx, self.state)
        self.enterRule(localctx, 456, self.RULE_an_crud_target_filter)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 2256
            self.code_block()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class An_crud_themeContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def KW_THEME(self):
            return self.getToken(ZmeiLangParser.KW_THEME, 0)

        def COLON(self):
            return self.getToken(ZmeiLangParser.COLON, 0)

        def id_or_kw(self):
            return self.getTypedRuleContext(ZmeiLangParser.Id_or_kwContext,0)


        def getRuleIndex(self):
            return ZmeiLangParser.RULE_an_crud_theme

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAn_crud_theme" ):
                listener.enterAn_crud_theme(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAn_crud_theme" ):
                listener.exitAn_crud_theme(self)




    def an_crud_theme(self):

        localctx = ZmeiLangParser.An_crud_themeContext(self, self._ctx, self.state)
        self.enterRule(localctx, 458, self.RULE_an_crud_theme)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 2258
            self.match(ZmeiLangParser.KW_THEME)
            self.state = 2259
            self.match(ZmeiLangParser.COLON)
            self.state = 2260
            self.id_or_kw()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class An_crud_url_prefixContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def KW_URL_PREFIX(self):
            return self.getToken(ZmeiLangParser.KW_URL_PREFIX, 0)

        def COLON(self):
            return self.getToken(ZmeiLangParser.COLON, 0)

        def an_crud_url_prefix_val(self):
            return self.getTypedRuleContext(ZmeiLangParser.An_crud_url_prefix_valContext,0)


        def getRuleIndex(self):
            return ZmeiLangParser.RULE_an_crud_url_prefix

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAn_crud_url_prefix" ):
                listener.enterAn_crud_url_prefix(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAn_crud_url_prefix" ):
                listener.exitAn_crud_url_prefix(self)




    def an_crud_url_prefix(self):

        localctx = ZmeiLangParser.An_crud_url_prefixContext(self, self._ctx, self.state)
        self.enterRule(localctx, 460, self.RULE_an_crud_url_prefix)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 2262
            self.match(ZmeiLangParser.KW_URL_PREFIX)
            self.state = 2263
            self.match(ZmeiLangParser.COLON)
            self.state = 2264
            self.an_crud_url_prefix_val()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class An_crud_url_prefix_valContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def STRING_DQ(self):
            return self.getToken(ZmeiLangParser.STRING_DQ, 0)

        def STRING_SQ(self):
            return self.getToken(ZmeiLangParser.STRING_SQ, 0)

        def getRuleIndex(self):
            return ZmeiLangParser.RULE_an_crud_url_prefix_val

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAn_crud_url_prefix_val" ):
                listener.enterAn_crud_url_prefix_val(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAn_crud_url_prefix_val" ):
                listener.exitAn_crud_url_prefix_val(self)




    def an_crud_url_prefix_val(self):

        localctx = ZmeiLangParser.An_crud_url_prefix_valContext(self, self._ctx, self.state)
        self.enterRule(localctx, 462, self.RULE_an_crud_url_prefix_val)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 2266
            _la = self._input.LA(1)
            if not(_la==ZmeiLangParser.STRING_DQ or _la==ZmeiLangParser.STRING_SQ):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class An_crud_link_suffixContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def KW_LINK_SUFFIX(self):
            return self.getToken(ZmeiLangParser.KW_LINK_SUFFIX, 0)

        def COLON(self):
            return self.getToken(ZmeiLangParser.COLON, 0)

        def an_crud_link_suffix_val(self):
            return self.getTypedRuleContext(ZmeiLangParser.An_crud_link_suffix_valContext,0)


        def getRuleIndex(self):
            return ZmeiLangParser.RULE_an_crud_link_suffix

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAn_crud_link_suffix" ):
                listener.enterAn_crud_link_suffix(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAn_crud_link_suffix" ):
                listener.exitAn_crud_link_suffix(self)




    def an_crud_link_suffix(self):

        localctx = ZmeiLangParser.An_crud_link_suffixContext(self, self._ctx, self.state)
        self.enterRule(localctx, 464, self.RULE_an_crud_link_suffix)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 2268
            self.match(ZmeiLangParser.KW_LINK_SUFFIX)
            self.state = 2269
            self.match(ZmeiLangParser.COLON)
            self.state = 2270
            self.an_crud_link_suffix_val()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class An_crud_link_suffix_valContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def STRING_DQ(self):
            return self.getToken(ZmeiLangParser.STRING_DQ, 0)

        def STRING_SQ(self):
            return self.getToken(ZmeiLangParser.STRING_SQ, 0)

        def getRuleIndex(self):
            return ZmeiLangParser.RULE_an_crud_link_suffix_val

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAn_crud_link_suffix_val" ):
                listener.enterAn_crud_link_suffix_val(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAn_crud_link_suffix_val" ):
                listener.exitAn_crud_link_suffix_val(self)




    def an_crud_link_suffix_val(self):

        localctx = ZmeiLangParser.An_crud_link_suffix_valContext(self, self._ctx, self.state)
        self.enterRule(localctx, 466, self.RULE_an_crud_link_suffix_val)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 2272
            _la = self._input.LA(1)
            if not(_la==ZmeiLangParser.STRING_DQ or _la==ZmeiLangParser.STRING_SQ):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class An_crud_item_nameContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def KW_ITEM_NAME(self):
            return self.getToken(ZmeiLangParser.KW_ITEM_NAME, 0)

        def COLON(self):
            return self.getToken(ZmeiLangParser.COLON, 0)

        def id_or_kw(self):
            return self.getTypedRuleContext(ZmeiLangParser.Id_or_kwContext,0)


        def getRuleIndex(self):
            return ZmeiLangParser.RULE_an_crud_item_name

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAn_crud_item_name" ):
                listener.enterAn_crud_item_name(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAn_crud_item_name" ):
                listener.exitAn_crud_item_name(self)




    def an_crud_item_name(self):

        localctx = ZmeiLangParser.An_crud_item_nameContext(self, self._ctx, self.state)
        self.enterRule(localctx, 468, self.RULE_an_crud_item_name)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 2274
            self.match(ZmeiLangParser.KW_ITEM_NAME)
            self.state = 2275
            self.match(ZmeiLangParser.COLON)
            self.state = 2276
            self.id_or_kw()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class An_crud_object_exprContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def KW_OBJECT_EXPR(self):
            return self.getToken(ZmeiLangParser.KW_OBJECT_EXPR, 0)

        def code_line(self):
            return self.getTypedRuleContext(ZmeiLangParser.Code_lineContext,0)


        def COLON(self):
            return self.getToken(ZmeiLangParser.COLON, 0)

        def code_block(self):
            return self.getTypedRuleContext(ZmeiLangParser.Code_blockContext,0)


        def getRuleIndex(self):
            return ZmeiLangParser.RULE_an_crud_object_expr

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAn_crud_object_expr" ):
                listener.enterAn_crud_object_expr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAn_crud_object_expr" ):
                listener.exitAn_crud_object_expr(self)




    def an_crud_object_expr(self):

        localctx = ZmeiLangParser.An_crud_object_exprContext(self, self._ctx, self.state)
        self.enterRule(localctx, 470, self.RULE_an_crud_object_expr)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 2278
            self.match(ZmeiLangParser.KW_OBJECT_EXPR)
            self.state = 2282
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [ZmeiLangParser.ASSIGN]:
                self.state = 2279
                self.code_line()
                pass
            elif token in [ZmeiLangParser.COLON]:
                self.state = 2280
                self.match(ZmeiLangParser.COLON)
                self.state = 2281
                self.code_block()
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class An_crud_can_editContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def KW_CAN_EDIT(self):
            return self.getToken(ZmeiLangParser.KW_CAN_EDIT, 0)

        def code_line(self):
            return self.getTypedRuleContext(ZmeiLangParser.Code_lineContext,0)


        def COLON(self):
            return self.getToken(ZmeiLangParser.COLON, 0)

        def code_block(self):
            return self.getTypedRuleContext(ZmeiLangParser.Code_blockContext,0)


        def getRuleIndex(self):
            return ZmeiLangParser.RULE_an_crud_can_edit

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAn_crud_can_edit" ):
                listener.enterAn_crud_can_edit(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAn_crud_can_edit" ):
                listener.exitAn_crud_can_edit(self)




    def an_crud_can_edit(self):

        localctx = ZmeiLangParser.An_crud_can_editContext(self, self._ctx, self.state)
        self.enterRule(localctx, 472, self.RULE_an_crud_can_edit)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 2284
            self.match(ZmeiLangParser.KW_CAN_EDIT)
            self.state = 2288
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [ZmeiLangParser.ASSIGN]:
                self.state = 2285
                self.code_line()
                pass
            elif token in [ZmeiLangParser.COLON]:
                self.state = 2286
                self.match(ZmeiLangParser.COLON)
                self.state = 2287
                self.code_block()
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class An_crud_blockContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def KW_BLOCK(self):
            return self.getToken(ZmeiLangParser.KW_BLOCK, 0)

        def COLON(self):
            return self.getToken(ZmeiLangParser.COLON, 0)

        def id_or_kw(self):
            return self.getTypedRuleContext(ZmeiLangParser.Id_or_kwContext,0)


        def getRuleIndex(self):
            return ZmeiLangParser.RULE_an_crud_block

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAn_crud_block" ):
                listener.enterAn_crud_block(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAn_crud_block" ):
                listener.exitAn_crud_block(self)




    def an_crud_block(self):

        localctx = ZmeiLangParser.An_crud_blockContext(self, self._ctx, self.state)
        self.enterRule(localctx, 474, self.RULE_an_crud_block)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 2290
            self.match(ZmeiLangParser.KW_BLOCK)
            self.state = 2291
            self.match(ZmeiLangParser.COLON)
            self.state = 2292
            self.id_or_kw()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class An_crud_pk_paramContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def KW_PK_PARAM(self):
            return self.getToken(ZmeiLangParser.KW_PK_PARAM, 0)

        def COLON(self):
            return self.getToken(ZmeiLangParser.COLON, 0)

        def id_or_kw(self):
            return self.getTypedRuleContext(ZmeiLangParser.Id_or_kwContext,0)


        def getRuleIndex(self):
            return ZmeiLangParser.RULE_an_crud_pk_param

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAn_crud_pk_param" ):
                listener.enterAn_crud_pk_param(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAn_crud_pk_param" ):
                listener.exitAn_crud_pk_param(self)




    def an_crud_pk_param(self):

        localctx = ZmeiLangParser.An_crud_pk_paramContext(self, self._ctx, self.state)
        self.enterRule(localctx, 476, self.RULE_an_crud_pk_param)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 2294
            self.match(ZmeiLangParser.KW_PK_PARAM)
            self.state = 2295
            self.match(ZmeiLangParser.COLON)
            self.state = 2296
            self.id_or_kw()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class An_crud_skipContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def KW_SKIP(self):
            return self.getToken(ZmeiLangParser.KW_SKIP, 0)

        def COLON(self):
            return self.getToken(ZmeiLangParser.COLON, 0)

        def an_crud_skip_values(self):
            return self.getTypedRuleContext(ZmeiLangParser.An_crud_skip_valuesContext,0)


        def getRuleIndex(self):
            return ZmeiLangParser.RULE_an_crud_skip

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAn_crud_skip" ):
                listener.enterAn_crud_skip(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAn_crud_skip" ):
                listener.exitAn_crud_skip(self)




    def an_crud_skip(self):

        localctx = ZmeiLangParser.An_crud_skipContext(self, self._ctx, self.state)
        self.enterRule(localctx, 478, self.RULE_an_crud_skip)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 2298
            self.match(ZmeiLangParser.KW_SKIP)
            self.state = 2299
            self.match(ZmeiLangParser.COLON)
            self.state = 2300
            self.an_crud_skip_values()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class An_crud_skip_valuesContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def an_crud_view_name(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(ZmeiLangParser.An_crud_view_nameContext)
            else:
                return self.getTypedRuleContext(ZmeiLangParser.An_crud_view_nameContext,i)


        def COMA(self, i:int=None):
            if i is None:
                return self.getTokens(ZmeiLangParser.COMA)
            else:
                return self.getToken(ZmeiLangParser.COMA, i)

        def getRuleIndex(self):
            return ZmeiLangParser.RULE_an_crud_skip_values

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAn_crud_skip_values" ):
                listener.enterAn_crud_skip_values(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAn_crud_skip_values" ):
                listener.exitAn_crud_skip_values(self)




    def an_crud_skip_values(self):

        localctx = ZmeiLangParser.An_crud_skip_valuesContext(self, self._ctx, self.state)
        self.enterRule(localctx, 480, self.RULE_an_crud_skip_values)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 2302
            self.an_crud_view_name()
            self.state = 2307
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,238,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 2303
                    self.match(ZmeiLangParser.COMA)
                    self.state = 2304
                    self.an_crud_view_name() 
                self.state = 2309
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,238,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class An_crud_view_nameContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def KW_DELETE(self):
            return self.getToken(ZmeiLangParser.KW_DELETE, 0)

        def KW_LIST(self):
            return self.getToken(ZmeiLangParser.KW_LIST, 0)

        def KW_CREATE(self):
            return self.getToken(ZmeiLangParser.KW_CREATE, 0)

        def KW_EDIT(self):
            return self.getToken(ZmeiLangParser.KW_EDIT, 0)

        def KW_DETAIL(self):
            return self.getToken(ZmeiLangParser.KW_DETAIL, 0)

        def getRuleIndex(self):
            return ZmeiLangParser.RULE_an_crud_view_name

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAn_crud_view_name" ):
                listener.enterAn_crud_view_name(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAn_crud_view_name" ):
                listener.exitAn_crud_view_name(self)




    def an_crud_view_name(self):

        localctx = ZmeiLangParser.An_crud_view_nameContext(self, self._ctx, self.state)
        self.enterRule(localctx, 482, self.RULE_an_crud_view_name)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 2310
            _la = self._input.LA(1)
            if not(((((_la - 85)) & ~0x3f) == 0 and ((1 << (_la - 85)) & ((1 << (ZmeiLangParser.KW_DELETE - 85)) | (1 << (ZmeiLangParser.KW_EDIT - 85)) | (1 << (ZmeiLangParser.KW_CREATE - 85)) | (1 << (ZmeiLangParser.KW_DETAIL - 85)) | (1 << (ZmeiLangParser.KW_LIST - 85)))) != 0)):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class An_crud_fieldsContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def KW_FIELDS(self):
            return self.getToken(ZmeiLangParser.KW_FIELDS, 0)

        def COLON(self):
            return self.getToken(ZmeiLangParser.COLON, 0)

        def an_crud_fields_expr(self):
            return self.getTypedRuleContext(ZmeiLangParser.An_crud_fields_exprContext,0)


        def getRuleIndex(self):
            return ZmeiLangParser.RULE_an_crud_fields

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAn_crud_fields" ):
                listener.enterAn_crud_fields(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAn_crud_fields" ):
                listener.exitAn_crud_fields(self)




    def an_crud_fields(self):

        localctx = ZmeiLangParser.An_crud_fieldsContext(self, self._ctx, self.state)
        self.enterRule(localctx, 484, self.RULE_an_crud_fields)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 2312
            self.match(ZmeiLangParser.KW_FIELDS)
            self.state = 2313
            self.match(ZmeiLangParser.COLON)
            self.state = 2314
            self.an_crud_fields_expr()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class An_crud_list_typeContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def KW_LIST(self):
            return self.getToken(ZmeiLangParser.KW_LIST, 0)

        def COLON(self):
            return self.getToken(ZmeiLangParser.COLON, 0)

        def an_crud_list_type_var(self):
            return self.getTypedRuleContext(ZmeiLangParser.An_crud_list_type_varContext,0)


        def getRuleIndex(self):
            return ZmeiLangParser.RULE_an_crud_list_type

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAn_crud_list_type" ):
                listener.enterAn_crud_list_type(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAn_crud_list_type" ):
                listener.exitAn_crud_list_type(self)




    def an_crud_list_type(self):

        localctx = ZmeiLangParser.An_crud_list_typeContext(self, self._ctx, self.state)
        self.enterRule(localctx, 486, self.RULE_an_crud_list_type)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 2316
            self.match(ZmeiLangParser.KW_LIST)
            self.state = 2317
            self.match(ZmeiLangParser.COLON)
            self.state = 2318
            self.an_crud_list_type_var()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class An_crud_list_type_varContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def KW_INLINE_TYPE_TABULAR(self):
            return self.getToken(ZmeiLangParser.KW_INLINE_TYPE_TABULAR, 0)

        def KW_INLINE_TYPE_STACKED(self):
            return self.getToken(ZmeiLangParser.KW_INLINE_TYPE_STACKED, 0)

        def KW_INLINE_TYPE_POLYMORPHIC(self):
            return self.getToken(ZmeiLangParser.KW_INLINE_TYPE_POLYMORPHIC, 0)

        def getRuleIndex(self):
            return ZmeiLangParser.RULE_an_crud_list_type_var

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAn_crud_list_type_var" ):
                listener.enterAn_crud_list_type_var(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAn_crud_list_type_var" ):
                listener.exitAn_crud_list_type_var(self)




    def an_crud_list_type_var(self):

        localctx = ZmeiLangParser.An_crud_list_type_varContext(self, self._ctx, self.state)
        self.enterRule(localctx, 488, self.RULE_an_crud_list_type_var)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 2320
            _la = self._input.LA(1)
            if not(((((_la - 94)) & ~0x3f) == 0 and ((1 << (_la - 94)) & ((1 << (ZmeiLangParser.KW_INLINE_TYPE_TABULAR - 94)) | (1 << (ZmeiLangParser.KW_INLINE_TYPE_STACKED - 94)) | (1 << (ZmeiLangParser.KW_INLINE_TYPE_POLYMORPHIC - 94)))) != 0)):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class An_crud_headerContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def KW_HEADER(self):
            return self.getToken(ZmeiLangParser.KW_HEADER, 0)

        def COLON(self):
            return self.getToken(ZmeiLangParser.COLON, 0)

        def an_crud_header_enabled(self):
            return self.getTypedRuleContext(ZmeiLangParser.An_crud_header_enabledContext,0)


        def getRuleIndex(self):
            return ZmeiLangParser.RULE_an_crud_header

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAn_crud_header" ):
                listener.enterAn_crud_header(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAn_crud_header" ):
                listener.exitAn_crud_header(self)




    def an_crud_header(self):

        localctx = ZmeiLangParser.An_crud_headerContext(self, self._ctx, self.state)
        self.enterRule(localctx, 490, self.RULE_an_crud_header)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 2322
            self.match(ZmeiLangParser.KW_HEADER)
            self.state = 2323
            self.match(ZmeiLangParser.COLON)
            self.state = 2324
            self.an_crud_header_enabled()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class An_crud_header_enabledContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def BOOL(self):
            return self.getToken(ZmeiLangParser.BOOL, 0)

        def getRuleIndex(self):
            return ZmeiLangParser.RULE_an_crud_header_enabled

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAn_crud_header_enabled" ):
                listener.enterAn_crud_header_enabled(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAn_crud_header_enabled" ):
                listener.exitAn_crud_header_enabled(self)




    def an_crud_header_enabled(self):

        localctx = ZmeiLangParser.An_crud_header_enabledContext(self, self._ctx, self.state)
        self.enterRule(localctx, 492, self.RULE_an_crud_header_enabled)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 2326
            self.match(ZmeiLangParser.BOOL)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class An_crud_fields_exprContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def an_crud_field(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(ZmeiLangParser.An_crud_fieldContext)
            else:
                return self.getTypedRuleContext(ZmeiLangParser.An_crud_fieldContext,i)


        def COMA(self, i:int=None):
            if i is None:
                return self.getTokens(ZmeiLangParser.COMA)
            else:
                return self.getToken(ZmeiLangParser.COMA, i)

        def getRuleIndex(self):
            return ZmeiLangParser.RULE_an_crud_fields_expr

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAn_crud_fields_expr" ):
                listener.enterAn_crud_fields_expr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAn_crud_fields_expr" ):
                listener.exitAn_crud_fields_expr(self)




    def an_crud_fields_expr(self):

        localctx = ZmeiLangParser.An_crud_fields_exprContext(self, self._ctx, self.state)
        self.enterRule(localctx, 494, self.RULE_an_crud_fields_expr)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 2328
            self.an_crud_field()
            self.state = 2333
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,239,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 2329
                    self.match(ZmeiLangParser.COMA)
                    self.state = 2330
                    self.an_crud_field() 
                self.state = 2335
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,239,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class An_crud_fieldContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def an_crud_field_spec(self):
            return self.getTypedRuleContext(ZmeiLangParser.An_crud_field_specContext,0)


        def an_crud_field_filter(self):
            return self.getTypedRuleContext(ZmeiLangParser.An_crud_field_filterContext,0)


        def getRuleIndex(self):
            return ZmeiLangParser.RULE_an_crud_field

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAn_crud_field" ):
                listener.enterAn_crud_field(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAn_crud_field" ):
                listener.exitAn_crud_field(self)




    def an_crud_field(self):

        localctx = ZmeiLangParser.An_crud_fieldContext(self, self._ctx, self.state)
        self.enterRule(localctx, 496, self.RULE_an_crud_field)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 2336
            self.an_crud_field_spec()
            self.state = 2338
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==ZmeiLangParser.CODE_BLOCK:
                self.state = 2337
                self.an_crud_field_filter()


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class An_crud_field_specContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def STAR(self):
            return self.getToken(ZmeiLangParser.STAR, 0)

        def id_or_kw(self):
            return self.getTypedRuleContext(ZmeiLangParser.Id_or_kwContext,0)


        def EXCLUDE(self):
            return self.getToken(ZmeiLangParser.EXCLUDE, 0)

        def getRuleIndex(self):
            return ZmeiLangParser.RULE_an_crud_field_spec

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAn_crud_field_spec" ):
                listener.enterAn_crud_field_spec(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAn_crud_field_spec" ):
                listener.exitAn_crud_field_spec(self)




    def an_crud_field_spec(self):

        localctx = ZmeiLangParser.An_crud_field_specContext(self, self._ctx, self.state)
        self.enterRule(localctx, 498, self.RULE_an_crud_field_spec)
        self._la = 0 # Token type
        try:
            self.state = 2345
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [ZmeiLangParser.STAR]:
                self.enterOuterAlt(localctx, 1)
                self.state = 2340
                self.match(ZmeiLangParser.STAR)
                pass
            elif token in [ZmeiLangParser.KW_AUTH_TYPE_BASIC, ZmeiLangParser.KW_AUTH_TYPE_SESSION, ZmeiLangParser.KW_AUTH_TYPE_TOKEN, ZmeiLangParser.COL_FIELD_TYPE_LONGTEXT, ZmeiLangParser.COL_FIELD_TYPE_HTML, ZmeiLangParser.COL_FIELD_TYPE_HTML_MEDIA, ZmeiLangParser.COL_FIELD_TYPE_FLOAT, ZmeiLangParser.COL_FIELD_TYPE_DECIMAL, ZmeiLangParser.COL_FIELD_TYPE_DATE, ZmeiLangParser.COL_FIELD_TYPE_DATETIME, ZmeiLangParser.COL_FIELD_TYPE_CREATE_TIME, ZmeiLangParser.COL_FIELD_TYPE_UPDATE_TIME, ZmeiLangParser.COL_FIELD_TYPE_IMAGE, ZmeiLangParser.COL_FIELD_TYPE_FILE, ZmeiLangParser.COL_FIELD_TYPE_FILER_IMAGE, ZmeiLangParser.COL_FIELD_TYPE_FILER_FILE, ZmeiLangParser.COL_FIELD_TYPE_FILER_FOLDER, ZmeiLangParser.COL_FIELD_TYPE_FILER_IMAGE_FOLDER, ZmeiLangParser.COL_FIELD_TYPE_TEXT, ZmeiLangParser.COL_FIELD_TYPE_INT, ZmeiLangParser.COL_FIELD_TYPE_SLUG, ZmeiLangParser.COL_FIELD_TYPE_BOOL, ZmeiLangParser.COL_FIELD_TYPE_ONE, ZmeiLangParser.COL_FIELD_TYPE_ONE2ONE, ZmeiLangParser.COL_FIELD_TYPE_MANY, ZmeiLangParser.COL_FIELD_CHOICES, ZmeiLangParser.KW_THEME, ZmeiLangParser.KW_INSTALL, ZmeiLangParser.KW_HEADER, ZmeiLangParser.KW_SERVICES, ZmeiLangParser.KW_SELENIUM_PYTEST, ZmeiLangParser.KW_CHILD, ZmeiLangParser.KW_FILTER_OUT, ZmeiLangParser.KW_FILTER_IN, ZmeiLangParser.KW_PAGE, ZmeiLangParser.KW_LINK_SUFFIX, ZmeiLangParser.KW_URL_PREFIX, ZmeiLangParser.KW_CAN_EDIT, ZmeiLangParser.KW_OBJECT_EXPR, ZmeiLangParser.KW_BLOCK, ZmeiLangParser.KW_ITEM_NAME, ZmeiLangParser.KW_PK_PARAM, ZmeiLangParser.KW_LIST_FIELDS, ZmeiLangParser.KW_DELETE, ZmeiLangParser.KW_EDIT, ZmeiLangParser.KW_CREATE, ZmeiLangParser.KW_DETAIL, ZmeiLangParser.KW_SKIP, ZmeiLangParser.KW_FROM, ZmeiLangParser.KW_POLY_LIST, ZmeiLangParser.KW_CSS, ZmeiLangParser.KW_JS, ZmeiLangParser.KW_INLINE_TYPE_TABULAR, ZmeiLangParser.KW_INLINE_TYPE_STACKED, ZmeiLangParser.KW_INLINE_TYPE_POLYMORPHIC, ZmeiLangParser.KW_INLINE, ZmeiLangParser.KW_TYPE, ZmeiLangParser.KW_USER_FIELD, ZmeiLangParser.KW_ANNOTATE, ZmeiLangParser.KW_ON_CREATE, ZmeiLangParser.KW_QUERY, ZmeiLangParser.KW_AUTH, ZmeiLangParser.KW_COUNT, ZmeiLangParser.KW_I18N, ZmeiLangParser.KW_EXTENSION, ZmeiLangParser.KW_TABS, ZmeiLangParser.KW_LIST, ZmeiLangParser.KW_READ_ONLY, ZmeiLangParser.KW_LIST_EDITABLE, ZmeiLangParser.KW_LIST_FILTER, ZmeiLangParser.KW_LIST_SEARCH, ZmeiLangParser.KW_FIELDS, ZmeiLangParser.KW_IMPORT, ZmeiLangParser.KW_AS, ZmeiLangParser.WRITE_MODE, ZmeiLangParser.BOOL, ZmeiLangParser.ID, ZmeiLangParser.EXCLUDE]:
                self.enterOuterAlt(localctx, 2)
                self.state = 2342
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==ZmeiLangParser.EXCLUDE:
                    self.state = 2341
                    self.match(ZmeiLangParser.EXCLUDE)


                self.state = 2344
                self.id_or_kw()
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class An_crud_field_filterContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def code_block(self):
            return self.getTypedRuleContext(ZmeiLangParser.Code_blockContext,0)


        def getRuleIndex(self):
            return ZmeiLangParser.RULE_an_crud_field_filter

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAn_crud_field_filter" ):
                listener.enterAn_crud_field_filter(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAn_crud_field_filter" ):
                listener.exitAn_crud_field_filter(self)




    def an_crud_field_filter(self):

        localctx = ZmeiLangParser.An_crud_field_filterContext(self, self._ctx, self.state)
        self.enterRule(localctx, 500, self.RULE_an_crud_field_filter)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 2347
            self.code_block()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class An_crud_list_fieldsContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def KW_LIST_FIELDS(self):
            return self.getToken(ZmeiLangParser.KW_LIST_FIELDS, 0)

        def COLON(self):
            return self.getToken(ZmeiLangParser.COLON, 0)

        def an_crud_list_fields_expr(self):
            return self.getTypedRuleContext(ZmeiLangParser.An_crud_list_fields_exprContext,0)


        def getRuleIndex(self):
            return ZmeiLangParser.RULE_an_crud_list_fields

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAn_crud_list_fields" ):
                listener.enterAn_crud_list_fields(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAn_crud_list_fields" ):
                listener.exitAn_crud_list_fields(self)




    def an_crud_list_fields(self):

        localctx = ZmeiLangParser.An_crud_list_fieldsContext(self, self._ctx, self.state)
        self.enterRule(localctx, 502, self.RULE_an_crud_list_fields)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 2349
            self.match(ZmeiLangParser.KW_LIST_FIELDS)
            self.state = 2350
            self.match(ZmeiLangParser.COLON)
            self.state = 2351
            self.an_crud_list_fields_expr()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class An_crud_list_fields_exprContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def an_crud_list_field(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(ZmeiLangParser.An_crud_list_fieldContext)
            else:
                return self.getTypedRuleContext(ZmeiLangParser.An_crud_list_fieldContext,i)


        def COMA(self, i:int=None):
            if i is None:
                return self.getTokens(ZmeiLangParser.COMA)
            else:
                return self.getToken(ZmeiLangParser.COMA, i)

        def getRuleIndex(self):
            return ZmeiLangParser.RULE_an_crud_list_fields_expr

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAn_crud_list_fields_expr" ):
                listener.enterAn_crud_list_fields_expr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAn_crud_list_fields_expr" ):
                listener.exitAn_crud_list_fields_expr(self)




    def an_crud_list_fields_expr(self):

        localctx = ZmeiLangParser.An_crud_list_fields_exprContext(self, self._ctx, self.state)
        self.enterRule(localctx, 504, self.RULE_an_crud_list_fields_expr)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 2353
            self.an_crud_list_field()
            self.state = 2358
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,243,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 2354
                    self.match(ZmeiLangParser.COMA)
                    self.state = 2355
                    self.an_crud_list_field() 
                self.state = 2360
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,243,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class An_crud_list_fieldContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def an_crud_list_field_spec(self):
            return self.getTypedRuleContext(ZmeiLangParser.An_crud_list_field_specContext,0)


        def getRuleIndex(self):
            return ZmeiLangParser.RULE_an_crud_list_field

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAn_crud_list_field" ):
                listener.enterAn_crud_list_field(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAn_crud_list_field" ):
                listener.exitAn_crud_list_field(self)




    def an_crud_list_field(self):

        localctx = ZmeiLangParser.An_crud_list_fieldContext(self, self._ctx, self.state)
        self.enterRule(localctx, 506, self.RULE_an_crud_list_field)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 2361
            self.an_crud_list_field_spec()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class An_crud_list_field_specContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def STAR(self):
            return self.getToken(ZmeiLangParser.STAR, 0)

        def id_or_kw(self):
            return self.getTypedRuleContext(ZmeiLangParser.Id_or_kwContext,0)


        def EXCLUDE(self):
            return self.getToken(ZmeiLangParser.EXCLUDE, 0)

        def getRuleIndex(self):
            return ZmeiLangParser.RULE_an_crud_list_field_spec

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAn_crud_list_field_spec" ):
                listener.enterAn_crud_list_field_spec(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAn_crud_list_field_spec" ):
                listener.exitAn_crud_list_field_spec(self)




    def an_crud_list_field_spec(self):

        localctx = ZmeiLangParser.An_crud_list_field_specContext(self, self._ctx, self.state)
        self.enterRule(localctx, 508, self.RULE_an_crud_list_field_spec)
        self._la = 0 # Token type
        try:
            self.state = 2368
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [ZmeiLangParser.STAR]:
                self.enterOuterAlt(localctx, 1)
                self.state = 2363
                self.match(ZmeiLangParser.STAR)
                pass
            elif token in [ZmeiLangParser.KW_AUTH_TYPE_BASIC, ZmeiLangParser.KW_AUTH_TYPE_SESSION, ZmeiLangParser.KW_AUTH_TYPE_TOKEN, ZmeiLangParser.COL_FIELD_TYPE_LONGTEXT, ZmeiLangParser.COL_FIELD_TYPE_HTML, ZmeiLangParser.COL_FIELD_TYPE_HTML_MEDIA, ZmeiLangParser.COL_FIELD_TYPE_FLOAT, ZmeiLangParser.COL_FIELD_TYPE_DECIMAL, ZmeiLangParser.COL_FIELD_TYPE_DATE, ZmeiLangParser.COL_FIELD_TYPE_DATETIME, ZmeiLangParser.COL_FIELD_TYPE_CREATE_TIME, ZmeiLangParser.COL_FIELD_TYPE_UPDATE_TIME, ZmeiLangParser.COL_FIELD_TYPE_IMAGE, ZmeiLangParser.COL_FIELD_TYPE_FILE, ZmeiLangParser.COL_FIELD_TYPE_FILER_IMAGE, ZmeiLangParser.COL_FIELD_TYPE_FILER_FILE, ZmeiLangParser.COL_FIELD_TYPE_FILER_FOLDER, ZmeiLangParser.COL_FIELD_TYPE_FILER_IMAGE_FOLDER, ZmeiLangParser.COL_FIELD_TYPE_TEXT, ZmeiLangParser.COL_FIELD_TYPE_INT, ZmeiLangParser.COL_FIELD_TYPE_SLUG, ZmeiLangParser.COL_FIELD_TYPE_BOOL, ZmeiLangParser.COL_FIELD_TYPE_ONE, ZmeiLangParser.COL_FIELD_TYPE_ONE2ONE, ZmeiLangParser.COL_FIELD_TYPE_MANY, ZmeiLangParser.COL_FIELD_CHOICES, ZmeiLangParser.KW_THEME, ZmeiLangParser.KW_INSTALL, ZmeiLangParser.KW_HEADER, ZmeiLangParser.KW_SERVICES, ZmeiLangParser.KW_SELENIUM_PYTEST, ZmeiLangParser.KW_CHILD, ZmeiLangParser.KW_FILTER_OUT, ZmeiLangParser.KW_FILTER_IN, ZmeiLangParser.KW_PAGE, ZmeiLangParser.KW_LINK_SUFFIX, ZmeiLangParser.KW_URL_PREFIX, ZmeiLangParser.KW_CAN_EDIT, ZmeiLangParser.KW_OBJECT_EXPR, ZmeiLangParser.KW_BLOCK, ZmeiLangParser.KW_ITEM_NAME, ZmeiLangParser.KW_PK_PARAM, ZmeiLangParser.KW_LIST_FIELDS, ZmeiLangParser.KW_DELETE, ZmeiLangParser.KW_EDIT, ZmeiLangParser.KW_CREATE, ZmeiLangParser.KW_DETAIL, ZmeiLangParser.KW_SKIP, ZmeiLangParser.KW_FROM, ZmeiLangParser.KW_POLY_LIST, ZmeiLangParser.KW_CSS, ZmeiLangParser.KW_JS, ZmeiLangParser.KW_INLINE_TYPE_TABULAR, ZmeiLangParser.KW_INLINE_TYPE_STACKED, ZmeiLangParser.KW_INLINE_TYPE_POLYMORPHIC, ZmeiLangParser.KW_INLINE, ZmeiLangParser.KW_TYPE, ZmeiLangParser.KW_USER_FIELD, ZmeiLangParser.KW_ANNOTATE, ZmeiLangParser.KW_ON_CREATE, ZmeiLangParser.KW_QUERY, ZmeiLangParser.KW_AUTH, ZmeiLangParser.KW_COUNT, ZmeiLangParser.KW_I18N, ZmeiLangParser.KW_EXTENSION, ZmeiLangParser.KW_TABS, ZmeiLangParser.KW_LIST, ZmeiLangParser.KW_READ_ONLY, ZmeiLangParser.KW_LIST_EDITABLE, ZmeiLangParser.KW_LIST_FILTER, ZmeiLangParser.KW_LIST_SEARCH, ZmeiLangParser.KW_FIELDS, ZmeiLangParser.KW_IMPORT, ZmeiLangParser.KW_AS, ZmeiLangParser.WRITE_MODE, ZmeiLangParser.BOOL, ZmeiLangParser.ID, ZmeiLangParser.EXCLUDE]:
                self.enterOuterAlt(localctx, 2)
                self.state = 2365
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==ZmeiLangParser.EXCLUDE:
                    self.state = 2364
                    self.match(ZmeiLangParser.EXCLUDE)


                self.state = 2367
                self.id_or_kw()
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class An_postContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def AN_POST(self):
            return self.getToken(ZmeiLangParser.AN_POST, 0)

        def code_block(self):
            return self.getTypedRuleContext(ZmeiLangParser.Code_blockContext,0)


        def getRuleIndex(self):
            return ZmeiLangParser.RULE_an_post

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAn_post" ):
                listener.enterAn_post(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAn_post" ):
                listener.exitAn_post(self)




    def an_post(self):

        localctx = ZmeiLangParser.An_postContext(self, self._ctx, self.state)
        self.enterRule(localctx, 510, self.RULE_an_post)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 2370
            self.match(ZmeiLangParser.AN_POST)
            self.state = 2372
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==ZmeiLangParser.CODE_BLOCK:
                self.state = 2371
                self.code_block()


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class An_authContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def AN_AUTH(self):
            return self.getToken(ZmeiLangParser.AN_AUTH, 0)

        def code_block(self):
            return self.getTypedRuleContext(ZmeiLangParser.Code_blockContext,0)


        def getRuleIndex(self):
            return ZmeiLangParser.RULE_an_auth

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAn_auth" ):
                listener.enterAn_auth(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAn_auth" ):
                listener.exitAn_auth(self)




    def an_auth(self):

        localctx = ZmeiLangParser.An_authContext(self, self._ctx, self.state)
        self.enterRule(localctx, 512, self.RULE_an_auth)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 2374
            self.match(ZmeiLangParser.AN_AUTH)
            self.state = 2376
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==ZmeiLangParser.CODE_BLOCK:
                self.state = 2375
                self.code_block()


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class An_crud_createContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def AN_CRUD_CREATE(self):
            return self.getToken(ZmeiLangParser.AN_CRUD_CREATE, 0)

        def an_crud_params(self):
            return self.getTypedRuleContext(ZmeiLangParser.An_crud_paramsContext,0)


        def getRuleIndex(self):
            return ZmeiLangParser.RULE_an_crud_create

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAn_crud_create" ):
                listener.enterAn_crud_create(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAn_crud_create" ):
                listener.exitAn_crud_create(self)




    def an_crud_create(self):

        localctx = ZmeiLangParser.An_crud_createContext(self, self._ctx, self.state)
        self.enterRule(localctx, 514, self.RULE_an_crud_create)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 2378
            self.match(ZmeiLangParser.AN_CRUD_CREATE)
            self.state = 2379
            self.an_crud_params()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class An_crud_editContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def AN_CRUD_EDIT(self):
            return self.getToken(ZmeiLangParser.AN_CRUD_EDIT, 0)

        def an_crud_params(self):
            return self.getTypedRuleContext(ZmeiLangParser.An_crud_paramsContext,0)


        def getRuleIndex(self):
            return ZmeiLangParser.RULE_an_crud_edit

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAn_crud_edit" ):
                listener.enterAn_crud_edit(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAn_crud_edit" ):
                listener.exitAn_crud_edit(self)




    def an_crud_edit(self):

        localctx = ZmeiLangParser.An_crud_editContext(self, self._ctx, self.state)
        self.enterRule(localctx, 516, self.RULE_an_crud_edit)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 2381
            self.match(ZmeiLangParser.AN_CRUD_EDIT)
            self.state = 2382
            self.an_crud_params()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class An_crud_listContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def AN_CRUD_LIST(self):
            return self.getToken(ZmeiLangParser.AN_CRUD_LIST, 0)

        def an_crud_params(self):
            return self.getTypedRuleContext(ZmeiLangParser.An_crud_paramsContext,0)


        def getRuleIndex(self):
            return ZmeiLangParser.RULE_an_crud_list

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAn_crud_list" ):
                listener.enterAn_crud_list(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAn_crud_list" ):
                listener.exitAn_crud_list(self)




    def an_crud_list(self):

        localctx = ZmeiLangParser.An_crud_listContext(self, self._ctx, self.state)
        self.enterRule(localctx, 518, self.RULE_an_crud_list)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 2384
            self.match(ZmeiLangParser.AN_CRUD_LIST)
            self.state = 2385
            self.an_crud_params()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class An_menuContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def AN_MENU(self):
            return self.getToken(ZmeiLangParser.AN_MENU, 0)

        def DOT(self):
            return self.getToken(ZmeiLangParser.DOT, 0)

        def an_menu_descriptor(self):
            return self.getTypedRuleContext(ZmeiLangParser.An_menu_descriptorContext,0)


        def BRACE_OPEN(self):
            return self.getToken(ZmeiLangParser.BRACE_OPEN, 0)

        def BRACE_CLOSE(self):
            return self.getToken(ZmeiLangParser.BRACE_CLOSE, 0)

        def NL(self, i:int=None):
            if i is None:
                return self.getTokens(ZmeiLangParser.NL)
            else:
                return self.getToken(ZmeiLangParser.NL, i)

        def an_menu_item(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(ZmeiLangParser.An_menu_itemContext)
            else:
                return self.getTypedRuleContext(ZmeiLangParser.An_menu_itemContext,i)


        def getRuleIndex(self):
            return ZmeiLangParser.RULE_an_menu

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAn_menu" ):
                listener.enterAn_menu(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAn_menu" ):
                listener.exitAn_menu(self)




    def an_menu(self):

        localctx = ZmeiLangParser.An_menuContext(self, self._ctx, self.state)
        self.enterRule(localctx, 520, self.RULE_an_menu)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 2387
            self.match(ZmeiLangParser.AN_MENU)
            self.state = 2388
            self.match(ZmeiLangParser.DOT)
            self.state = 2389
            self.an_menu_descriptor()
            self.state = 2390
            self.match(ZmeiLangParser.BRACE_OPEN)
            self.state = 2394
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,248,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 2391
                    self.match(ZmeiLangParser.NL) 
                self.state = 2396
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,248,self._ctx)

            self.state = 2398 
            self._errHandler.sync(self)
            _alt = 1
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt == 1:
                    self.state = 2397
                    self.an_menu_item()

                else:
                    raise NoViableAltException(self)
                self.state = 2400 
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,249,self._ctx)

            self.state = 2405
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==ZmeiLangParser.NL:
                self.state = 2402
                self.match(ZmeiLangParser.NL)
                self.state = 2407
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 2408
            self.match(ZmeiLangParser.BRACE_CLOSE)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class An_menu_descriptorContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def id_or_kw(self):
            return self.getTypedRuleContext(ZmeiLangParser.Id_or_kwContext,0)


        def getRuleIndex(self):
            return ZmeiLangParser.RULE_an_menu_descriptor

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAn_menu_descriptor" ):
                listener.enterAn_menu_descriptor(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAn_menu_descriptor" ):
                listener.exitAn_menu_descriptor(self)




    def an_menu_descriptor(self):

        localctx = ZmeiLangParser.An_menu_descriptorContext(self, self._ctx, self.state)
        self.enterRule(localctx, 522, self.RULE_an_menu_descriptor)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 2410
            self.id_or_kw()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class An_menu_itemContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def an_menu_label(self):
            return self.getTypedRuleContext(ZmeiLangParser.An_menu_labelContext,0)


        def an_menu_item_code(self):
            return self.getTypedRuleContext(ZmeiLangParser.An_menu_item_codeContext,0)


        def an_menu_target(self):
            return self.getTypedRuleContext(ZmeiLangParser.An_menu_targetContext,0)


        def COMA(self):
            return self.getToken(ZmeiLangParser.COMA, 0)

        def NL(self, i:int=None):
            if i is None:
                return self.getTokens(ZmeiLangParser.NL)
            else:
                return self.getToken(ZmeiLangParser.NL, i)

        def an_menu_item_args(self):
            return self.getTypedRuleContext(ZmeiLangParser.An_menu_item_argsContext,0)


        def getRuleIndex(self):
            return ZmeiLangParser.RULE_an_menu_item

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAn_menu_item" ):
                listener.enterAn_menu_item(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAn_menu_item" ):
                listener.exitAn_menu_item(self)




    def an_menu_item(self):

        localctx = ZmeiLangParser.An_menu_itemContext(self, self._ctx, self.state)
        self.enterRule(localctx, 524, self.RULE_an_menu_item)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 2413
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==ZmeiLangParser.COMA:
                self.state = 2412
                self.match(ZmeiLangParser.COMA)


            self.state = 2418
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==ZmeiLangParser.NL:
                self.state = 2415
                self.match(ZmeiLangParser.NL)
                self.state = 2420
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 2422
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==ZmeiLangParser.SQ_BRACE_OPEN:
                self.state = 2421
                self.an_menu_item_args()


            self.state = 2424
            self.an_menu_label()
            self.state = 2427
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [ZmeiLangParser.ASSIGN]:
                self.state = 2425
                self.an_menu_item_code()
                pass
            elif token in [ZmeiLangParser.COLON]:
                self.state = 2426
                self.an_menu_target()
                pass
            else:
                raise NoViableAltException(self)

            self.state = 2432
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,255,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 2429
                    self.match(ZmeiLangParser.NL) 
                self.state = 2434
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,255,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class An_menu_targetContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def COLON(self):
            return self.getToken(ZmeiLangParser.COLON, 0)

        def an_menu_item_page(self):
            return self.getTypedRuleContext(ZmeiLangParser.An_menu_item_pageContext,0)


        def an_menu_item_url(self):
            return self.getTypedRuleContext(ZmeiLangParser.An_menu_item_urlContext,0)


        def getRuleIndex(self):
            return ZmeiLangParser.RULE_an_menu_target

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAn_menu_target" ):
                listener.enterAn_menu_target(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAn_menu_target" ):
                listener.exitAn_menu_target(self)




    def an_menu_target(self):

        localctx = ZmeiLangParser.An_menu_targetContext(self, self._ctx, self.state)
        self.enterRule(localctx, 526, self.RULE_an_menu_target)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 2435
            self.match(ZmeiLangParser.COLON)
            self.state = 2438
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [ZmeiLangParser.KW_PAGE]:
                self.state = 2436
                self.an_menu_item_page()
                pass
            elif token in [ZmeiLangParser.STRING_DQ, ZmeiLangParser.STRING_SQ]:
                self.state = 2437
                self.an_menu_item_url()
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class An_menu_item_codeContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def code_line(self):
            return self.getTypedRuleContext(ZmeiLangParser.Code_lineContext,0)


        def getRuleIndex(self):
            return ZmeiLangParser.RULE_an_menu_item_code

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAn_menu_item_code" ):
                listener.enterAn_menu_item_code(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAn_menu_item_code" ):
                listener.exitAn_menu_item_code(self)




    def an_menu_item_code(self):

        localctx = ZmeiLangParser.An_menu_item_codeContext(self, self._ctx, self.state)
        self.enterRule(localctx, 528, self.RULE_an_menu_item_code)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 2440
            self.code_line()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class An_menu_item_argsContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def SQ_BRACE_OPEN(self):
            return self.getToken(ZmeiLangParser.SQ_BRACE_OPEN, 0)

        def an_menu_item_arg(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(ZmeiLangParser.An_menu_item_argContext)
            else:
                return self.getTypedRuleContext(ZmeiLangParser.An_menu_item_argContext,i)


        def SQ_BRACE_CLOSE(self):
            return self.getToken(ZmeiLangParser.SQ_BRACE_CLOSE, 0)

        def COMA(self, i:int=None):
            if i is None:
                return self.getTokens(ZmeiLangParser.COMA)
            else:
                return self.getToken(ZmeiLangParser.COMA, i)

        def getRuleIndex(self):
            return ZmeiLangParser.RULE_an_menu_item_args

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAn_menu_item_args" ):
                listener.enterAn_menu_item_args(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAn_menu_item_args" ):
                listener.exitAn_menu_item_args(self)




    def an_menu_item_args(self):

        localctx = ZmeiLangParser.An_menu_item_argsContext(self, self._ctx, self.state)
        self.enterRule(localctx, 530, self.RULE_an_menu_item_args)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 2442
            self.match(ZmeiLangParser.SQ_BRACE_OPEN)
            self.state = 2443
            self.an_menu_item_arg()
            self.state = 2448
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==ZmeiLangParser.COMA:
                self.state = 2444
                self.match(ZmeiLangParser.COMA)
                self.state = 2445
                self.an_menu_item_arg()
                self.state = 2450
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 2451
            self.match(ZmeiLangParser.SQ_BRACE_CLOSE)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class An_menu_item_argContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def an_menu_item_arg_key(self):
            return self.getTypedRuleContext(ZmeiLangParser.An_menu_item_arg_keyContext,0)


        def EQUALS(self):
            return self.getToken(ZmeiLangParser.EQUALS, 0)

        def an_menu_item_arg_val(self):
            return self.getTypedRuleContext(ZmeiLangParser.An_menu_item_arg_valContext,0)


        def getRuleIndex(self):
            return ZmeiLangParser.RULE_an_menu_item_arg

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAn_menu_item_arg" ):
                listener.enterAn_menu_item_arg(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAn_menu_item_arg" ):
                listener.exitAn_menu_item_arg(self)




    def an_menu_item_arg(self):

        localctx = ZmeiLangParser.An_menu_item_argContext(self, self._ctx, self.state)
        self.enterRule(localctx, 532, self.RULE_an_menu_item_arg)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 2453
            self.an_menu_item_arg_key()
            self.state = 2454
            self.match(ZmeiLangParser.EQUALS)
            self.state = 2455
            self.an_menu_item_arg_val()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class An_menu_item_arg_keyContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def id_or_kw(self):
            return self.getTypedRuleContext(ZmeiLangParser.Id_or_kwContext,0)


        def getRuleIndex(self):
            return ZmeiLangParser.RULE_an_menu_item_arg_key

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAn_menu_item_arg_key" ):
                listener.enterAn_menu_item_arg_key(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAn_menu_item_arg_key" ):
                listener.exitAn_menu_item_arg_key(self)




    def an_menu_item_arg_key(self):

        localctx = ZmeiLangParser.An_menu_item_arg_keyContext(self, self._ctx, self.state)
        self.enterRule(localctx, 534, self.RULE_an_menu_item_arg_key)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 2457
            self.id_or_kw()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class An_menu_item_arg_valContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def STRING_DQ(self):
            return self.getToken(ZmeiLangParser.STRING_DQ, 0)

        def STRING_SQ(self):
            return self.getToken(ZmeiLangParser.STRING_SQ, 0)

        def id_or_kw(self):
            return self.getTypedRuleContext(ZmeiLangParser.Id_or_kwContext,0)


        def getRuleIndex(self):
            return ZmeiLangParser.RULE_an_menu_item_arg_val

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAn_menu_item_arg_val" ):
                listener.enterAn_menu_item_arg_val(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAn_menu_item_arg_val" ):
                listener.exitAn_menu_item_arg_val(self)




    def an_menu_item_arg_val(self):

        localctx = ZmeiLangParser.An_menu_item_arg_valContext(self, self._ctx, self.state)
        self.enterRule(localctx, 536, self.RULE_an_menu_item_arg_val)
        try:
            self.state = 2462
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [ZmeiLangParser.STRING_DQ]:
                self.enterOuterAlt(localctx, 1)
                self.state = 2459
                self.match(ZmeiLangParser.STRING_DQ)
                pass
            elif token in [ZmeiLangParser.STRING_SQ]:
                self.enterOuterAlt(localctx, 2)
                self.state = 2460
                self.match(ZmeiLangParser.STRING_SQ)
                pass
            elif token in [ZmeiLangParser.KW_AUTH_TYPE_BASIC, ZmeiLangParser.KW_AUTH_TYPE_SESSION, ZmeiLangParser.KW_AUTH_TYPE_TOKEN, ZmeiLangParser.COL_FIELD_TYPE_LONGTEXT, ZmeiLangParser.COL_FIELD_TYPE_HTML, ZmeiLangParser.COL_FIELD_TYPE_HTML_MEDIA, ZmeiLangParser.COL_FIELD_TYPE_FLOAT, ZmeiLangParser.COL_FIELD_TYPE_DECIMAL, ZmeiLangParser.COL_FIELD_TYPE_DATE, ZmeiLangParser.COL_FIELD_TYPE_DATETIME, ZmeiLangParser.COL_FIELD_TYPE_CREATE_TIME, ZmeiLangParser.COL_FIELD_TYPE_UPDATE_TIME, ZmeiLangParser.COL_FIELD_TYPE_IMAGE, ZmeiLangParser.COL_FIELD_TYPE_FILE, ZmeiLangParser.COL_FIELD_TYPE_FILER_IMAGE, ZmeiLangParser.COL_FIELD_TYPE_FILER_FILE, ZmeiLangParser.COL_FIELD_TYPE_FILER_FOLDER, ZmeiLangParser.COL_FIELD_TYPE_FILER_IMAGE_FOLDER, ZmeiLangParser.COL_FIELD_TYPE_TEXT, ZmeiLangParser.COL_FIELD_TYPE_INT, ZmeiLangParser.COL_FIELD_TYPE_SLUG, ZmeiLangParser.COL_FIELD_TYPE_BOOL, ZmeiLangParser.COL_FIELD_TYPE_ONE, ZmeiLangParser.COL_FIELD_TYPE_ONE2ONE, ZmeiLangParser.COL_FIELD_TYPE_MANY, ZmeiLangParser.COL_FIELD_CHOICES, ZmeiLangParser.KW_THEME, ZmeiLangParser.KW_INSTALL, ZmeiLangParser.KW_HEADER, ZmeiLangParser.KW_SERVICES, ZmeiLangParser.KW_SELENIUM_PYTEST, ZmeiLangParser.KW_CHILD, ZmeiLangParser.KW_FILTER_OUT, ZmeiLangParser.KW_FILTER_IN, ZmeiLangParser.KW_PAGE, ZmeiLangParser.KW_LINK_SUFFIX, ZmeiLangParser.KW_URL_PREFIX, ZmeiLangParser.KW_CAN_EDIT, ZmeiLangParser.KW_OBJECT_EXPR, ZmeiLangParser.KW_BLOCK, ZmeiLangParser.KW_ITEM_NAME, ZmeiLangParser.KW_PK_PARAM, ZmeiLangParser.KW_LIST_FIELDS, ZmeiLangParser.KW_DELETE, ZmeiLangParser.KW_EDIT, ZmeiLangParser.KW_CREATE, ZmeiLangParser.KW_DETAIL, ZmeiLangParser.KW_SKIP, ZmeiLangParser.KW_FROM, ZmeiLangParser.KW_POLY_LIST, ZmeiLangParser.KW_CSS, ZmeiLangParser.KW_JS, ZmeiLangParser.KW_INLINE_TYPE_TABULAR, ZmeiLangParser.KW_INLINE_TYPE_STACKED, ZmeiLangParser.KW_INLINE_TYPE_POLYMORPHIC, ZmeiLangParser.KW_INLINE, ZmeiLangParser.KW_TYPE, ZmeiLangParser.KW_USER_FIELD, ZmeiLangParser.KW_ANNOTATE, ZmeiLangParser.KW_ON_CREATE, ZmeiLangParser.KW_QUERY, ZmeiLangParser.KW_AUTH, ZmeiLangParser.KW_COUNT, ZmeiLangParser.KW_I18N, ZmeiLangParser.KW_EXTENSION, ZmeiLangParser.KW_TABS, ZmeiLangParser.KW_LIST, ZmeiLangParser.KW_READ_ONLY, ZmeiLangParser.KW_LIST_EDITABLE, ZmeiLangParser.KW_LIST_FILTER, ZmeiLangParser.KW_LIST_SEARCH, ZmeiLangParser.KW_FIELDS, ZmeiLangParser.KW_IMPORT, ZmeiLangParser.KW_AS, ZmeiLangParser.WRITE_MODE, ZmeiLangParser.BOOL, ZmeiLangParser.ID]:
                self.enterOuterAlt(localctx, 3)
                self.state = 2461
                self.id_or_kw()
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class An_menu_item_urlContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def STRING_DQ(self):
            return self.getToken(ZmeiLangParser.STRING_DQ, 0)

        def STRING_SQ(self):
            return self.getToken(ZmeiLangParser.STRING_SQ, 0)

        def getRuleIndex(self):
            return ZmeiLangParser.RULE_an_menu_item_url

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAn_menu_item_url" ):
                listener.enterAn_menu_item_url(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAn_menu_item_url" ):
                listener.exitAn_menu_item_url(self)




    def an_menu_item_url(self):

        localctx = ZmeiLangParser.An_menu_item_urlContext(self, self._ctx, self.state)
        self.enterRule(localctx, 538, self.RULE_an_menu_item_url)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 2464
            _la = self._input.LA(1)
            if not(_la==ZmeiLangParser.STRING_DQ or _la==ZmeiLangParser.STRING_SQ):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class An_menu_item_pageContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def KW_PAGE(self):
            return self.getToken(ZmeiLangParser.KW_PAGE, 0)

        def BRACE_OPEN(self):
            return self.getToken(ZmeiLangParser.BRACE_OPEN, 0)

        def an_menu_item_page_ref(self):
            return self.getTypedRuleContext(ZmeiLangParser.An_menu_item_page_refContext,0)


        def BRACE_CLOSE(self):
            return self.getToken(ZmeiLangParser.BRACE_CLOSE, 0)

        def getRuleIndex(self):
            return ZmeiLangParser.RULE_an_menu_item_page

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAn_menu_item_page" ):
                listener.enterAn_menu_item_page(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAn_menu_item_page" ):
                listener.exitAn_menu_item_page(self)




    def an_menu_item_page(self):

        localctx = ZmeiLangParser.An_menu_item_pageContext(self, self._ctx, self.state)
        self.enterRule(localctx, 540, self.RULE_an_menu_item_page)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 2466
            self.match(ZmeiLangParser.KW_PAGE)
            self.state = 2467
            self.match(ZmeiLangParser.BRACE_OPEN)
            self.state = 2468
            self.an_menu_item_page_ref()
            self.state = 2469
            self.match(ZmeiLangParser.BRACE_CLOSE)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class An_menu_item_page_refContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def id_or_kw(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(ZmeiLangParser.Id_or_kwContext)
            else:
                return self.getTypedRuleContext(ZmeiLangParser.Id_or_kwContext,i)


        def DOT(self):
            return self.getToken(ZmeiLangParser.DOT, 0)

        def getRuleIndex(self):
            return ZmeiLangParser.RULE_an_menu_item_page_ref

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAn_menu_item_page_ref" ):
                listener.enterAn_menu_item_page_ref(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAn_menu_item_page_ref" ):
                listener.exitAn_menu_item_page_ref(self)




    def an_menu_item_page_ref(self):

        localctx = ZmeiLangParser.An_menu_item_page_refContext(self, self._ctx, self.state)
        self.enterRule(localctx, 542, self.RULE_an_menu_item_page_ref)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 2474
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,259,self._ctx)
            if la_ == 1:
                self.state = 2471
                self.id_or_kw()
                self.state = 2472
                self.match(ZmeiLangParser.DOT)


            self.state = 2476
            self.id_or_kw()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class An_menu_labelContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def STRING_DQ(self):
            return self.getToken(ZmeiLangParser.STRING_DQ, 0)

        def STRING_SQ(self):
            return self.getToken(ZmeiLangParser.STRING_SQ, 0)

        def id_or_kw(self):
            return self.getTypedRuleContext(ZmeiLangParser.Id_or_kwContext,0)


        def getRuleIndex(self):
            return ZmeiLangParser.RULE_an_menu_label

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAn_menu_label" ):
                listener.enterAn_menu_label(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAn_menu_label" ):
                listener.exitAn_menu_label(self)




    def an_menu_label(self):

        localctx = ZmeiLangParser.An_menu_labelContext(self, self._ctx, self.state)
        self.enterRule(localctx, 544, self.RULE_an_menu_label)
        try:
            self.state = 2481
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [ZmeiLangParser.STRING_DQ]:
                self.enterOuterAlt(localctx, 1)
                self.state = 2478
                self.match(ZmeiLangParser.STRING_DQ)
                pass
            elif token in [ZmeiLangParser.STRING_SQ]:
                self.enterOuterAlt(localctx, 2)
                self.state = 2479
                self.match(ZmeiLangParser.STRING_SQ)
                pass
            elif token in [ZmeiLangParser.KW_AUTH_TYPE_BASIC, ZmeiLangParser.KW_AUTH_TYPE_SESSION, ZmeiLangParser.KW_AUTH_TYPE_TOKEN, ZmeiLangParser.COL_FIELD_TYPE_LONGTEXT, ZmeiLangParser.COL_FIELD_TYPE_HTML, ZmeiLangParser.COL_FIELD_TYPE_HTML_MEDIA, ZmeiLangParser.COL_FIELD_TYPE_FLOAT, ZmeiLangParser.COL_FIELD_TYPE_DECIMAL, ZmeiLangParser.COL_FIELD_TYPE_DATE, ZmeiLangParser.COL_FIELD_TYPE_DATETIME, ZmeiLangParser.COL_FIELD_TYPE_CREATE_TIME, ZmeiLangParser.COL_FIELD_TYPE_UPDATE_TIME, ZmeiLangParser.COL_FIELD_TYPE_IMAGE, ZmeiLangParser.COL_FIELD_TYPE_FILE, ZmeiLangParser.COL_FIELD_TYPE_FILER_IMAGE, ZmeiLangParser.COL_FIELD_TYPE_FILER_FILE, ZmeiLangParser.COL_FIELD_TYPE_FILER_FOLDER, ZmeiLangParser.COL_FIELD_TYPE_FILER_IMAGE_FOLDER, ZmeiLangParser.COL_FIELD_TYPE_TEXT, ZmeiLangParser.COL_FIELD_TYPE_INT, ZmeiLangParser.COL_FIELD_TYPE_SLUG, ZmeiLangParser.COL_FIELD_TYPE_BOOL, ZmeiLangParser.COL_FIELD_TYPE_ONE, ZmeiLangParser.COL_FIELD_TYPE_ONE2ONE, ZmeiLangParser.COL_FIELD_TYPE_MANY, ZmeiLangParser.COL_FIELD_CHOICES, ZmeiLangParser.KW_THEME, ZmeiLangParser.KW_INSTALL, ZmeiLangParser.KW_HEADER, ZmeiLangParser.KW_SERVICES, ZmeiLangParser.KW_SELENIUM_PYTEST, ZmeiLangParser.KW_CHILD, ZmeiLangParser.KW_FILTER_OUT, ZmeiLangParser.KW_FILTER_IN, ZmeiLangParser.KW_PAGE, ZmeiLangParser.KW_LINK_SUFFIX, ZmeiLangParser.KW_URL_PREFIX, ZmeiLangParser.KW_CAN_EDIT, ZmeiLangParser.KW_OBJECT_EXPR, ZmeiLangParser.KW_BLOCK, ZmeiLangParser.KW_ITEM_NAME, ZmeiLangParser.KW_PK_PARAM, ZmeiLangParser.KW_LIST_FIELDS, ZmeiLangParser.KW_DELETE, ZmeiLangParser.KW_EDIT, ZmeiLangParser.KW_CREATE, ZmeiLangParser.KW_DETAIL, ZmeiLangParser.KW_SKIP, ZmeiLangParser.KW_FROM, ZmeiLangParser.KW_POLY_LIST, ZmeiLangParser.KW_CSS, ZmeiLangParser.KW_JS, ZmeiLangParser.KW_INLINE_TYPE_TABULAR, ZmeiLangParser.KW_INLINE_TYPE_STACKED, ZmeiLangParser.KW_INLINE_TYPE_POLYMORPHIC, ZmeiLangParser.KW_INLINE, ZmeiLangParser.KW_TYPE, ZmeiLangParser.KW_USER_FIELD, ZmeiLangParser.KW_ANNOTATE, ZmeiLangParser.KW_ON_CREATE, ZmeiLangParser.KW_QUERY, ZmeiLangParser.KW_AUTH, ZmeiLangParser.KW_COUNT, ZmeiLangParser.KW_I18N, ZmeiLangParser.KW_EXTENSION, ZmeiLangParser.KW_TABS, ZmeiLangParser.KW_LIST, ZmeiLangParser.KW_READ_ONLY, ZmeiLangParser.KW_LIST_EDITABLE, ZmeiLangParser.KW_LIST_FILTER, ZmeiLangParser.KW_LIST_SEARCH, ZmeiLangParser.KW_FIELDS, ZmeiLangParser.KW_IMPORT, ZmeiLangParser.KW_AS, ZmeiLangParser.WRITE_MODE, ZmeiLangParser.BOOL, ZmeiLangParser.ID]:
                self.enterOuterAlt(localctx, 3)
                self.state = 2480
                self.id_or_kw()
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class An_crud_detailContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def AN_CRUD_DETAIL(self):
            return self.getToken(ZmeiLangParser.AN_CRUD_DETAIL, 0)

        def an_crud_params(self):
            return self.getTypedRuleContext(ZmeiLangParser.An_crud_paramsContext,0)


        def getRuleIndex(self):
            return ZmeiLangParser.RULE_an_crud_detail

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAn_crud_detail" ):
                listener.enterAn_crud_detail(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAn_crud_detail" ):
                listener.exitAn_crud_detail(self)




    def an_crud_detail(self):

        localctx = ZmeiLangParser.An_crud_detailContext(self, self._ctx, self.state)
        self.enterRule(localctx, 546, self.RULE_an_crud_detail)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 2483
            self.match(ZmeiLangParser.AN_CRUD_DETAIL)
            self.state = 2484
            self.an_crud_params()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class An_priority_markerContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def AN_PRIORITY(self):
            return self.getToken(ZmeiLangParser.AN_PRIORITY, 0)

        def getRuleIndex(self):
            return ZmeiLangParser.RULE_an_priority_marker

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAn_priority_marker" ):
                listener.enterAn_priority_marker(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAn_priority_marker" ):
                listener.exitAn_priority_marker(self)




    def an_priority_marker(self):

        localctx = ZmeiLangParser.An_priority_markerContext(self, self._ctx, self.state)
        self.enterRule(localctx, 548, self.RULE_an_priority_marker)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 2486
            self.match(ZmeiLangParser.AN_PRIORITY)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class An_getContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def AN_GET(self):
            return self.getToken(ZmeiLangParser.AN_GET, 0)

        def code_block(self):
            return self.getTypedRuleContext(ZmeiLangParser.Code_blockContext,0)


        def getRuleIndex(self):
            return ZmeiLangParser.RULE_an_get

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAn_get" ):
                listener.enterAn_get(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAn_get" ):
                listener.exitAn_get(self)




    def an_get(self):

        localctx = ZmeiLangParser.An_getContext(self, self._ctx, self.state)
        self.enterRule(localctx, 550, self.RULE_an_get)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 2488
            self.match(ZmeiLangParser.AN_GET)
            self.state = 2490
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==ZmeiLangParser.CODE_BLOCK:
                self.state = 2489
                self.code_block()


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class An_errorContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def AN_ERROR(self):
            return self.getToken(ZmeiLangParser.AN_ERROR, 0)

        def BRACE_OPEN(self):
            return self.getToken(ZmeiLangParser.BRACE_OPEN, 0)

        def an_error_code(self):
            return self.getTypedRuleContext(ZmeiLangParser.An_error_codeContext,0)


        def BRACE_CLOSE(self):
            return self.getToken(ZmeiLangParser.BRACE_CLOSE, 0)

        def getRuleIndex(self):
            return ZmeiLangParser.RULE_an_error

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAn_error" ):
                listener.enterAn_error(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAn_error" ):
                listener.exitAn_error(self)




    def an_error(self):

        localctx = ZmeiLangParser.An_errorContext(self, self._ctx, self.state)
        self.enterRule(localctx, 552, self.RULE_an_error)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 2492
            self.match(ZmeiLangParser.AN_ERROR)
            self.state = 2493
            self.match(ZmeiLangParser.BRACE_OPEN)
            self.state = 2494
            self.an_error_code()
            self.state = 2495
            self.match(ZmeiLangParser.BRACE_CLOSE)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class An_error_codeContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def DIGIT(self):
            return self.getToken(ZmeiLangParser.DIGIT, 0)

        def getRuleIndex(self):
            return ZmeiLangParser.RULE_an_error_code

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAn_error_code" ):
                listener.enterAn_error_code(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAn_error_code" ):
                listener.exitAn_error_code(self)




    def an_error_code(self):

        localctx = ZmeiLangParser.An_error_codeContext(self, self._ctx, self.state)
        self.enterRule(localctx, 554, self.RULE_an_error_code)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 2497
            self.match(ZmeiLangParser.DIGIT)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx





