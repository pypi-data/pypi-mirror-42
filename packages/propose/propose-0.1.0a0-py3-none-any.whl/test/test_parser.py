from textwrap import dedent

from few.errors import ErrorHandler, IndentationError, LexingError, ParsingError

from few.ast import *

from few.lexer import Lexer, lex
from few.parser import Parser, State, parse

from few.renderer.ast import render_ast

def _parse(input):
    try:
        tokens = lex(input)
    except (IndentationError, LexingError) as e:
        ErrorHandler(e).call()
    try:
        ast = parse(input, tokens, State())
    except ParsingError as e:
        ErrorHandler(e).call()

    return render_ast(ast)

def _match_ast(expected, actual, element):
    assert dedent(expected) == '\n' + actual + '\n', element + ' not recognized'

def test_file():
    input = """"""
    ast = """
          (File)
          """

    _match_ast(ast, _parse(dedent(input)), 'File')

def test_block():
    input = """
            struct Test
              1
            """
    ast = """
          (File
            (StructDecl (SimpleType) (Block
              (Integer))))
          """

    _match_ast(ast, _parse(dedent(input)), 'Block')

def test_variable():
    input = """
            var
            really?
            """
    ast = """
          (File
            (Variable)
            (Variable))
          """

    _match_ast(ast, _parse(dedent(input)), 'Variable')

def test_simple_type():
    input = """
            Type
            """
    ast = """
          (File
            (SimpleType))
          """

    _match_ast(ast, _parse(dedent(input)), 'SimpleType')

def test_generic_type():
    input = """
            Test[AnotherTest[SomeMoreTests, A007, ThisNEVEREnds]]
            """
    ast = """
          (File
            (GenericType (SimpleType)
              (GenericType (SimpleType)
                (SimpleType)
                (SimpleType)
                (SimpleType))))
          """

    _match_ast(ast, _parse(dedent(input)), 'GenericType')

def test_parameter():
    input = """
            func = (a: Int,
                    b: Int = 1,
                    **c: Hash[A, B],
                    **d: Hash[C, D] = {},
                    *e: Array[E],
                    *f: Array[F] = [],
                    g: Int when g == 1,
                    *h: Int when h.length == 5,
                    **i: Int when i.length == 5,
                    j < 1,
                    k <= 1,
                    l > 1,
                    m >= 1,
                    n == 1,
                    o != 1,
                    p: interface Anything) => 1
            """
    ast = """
          (File
            (Assignment (Variable) (Function (Block
              (Integer)) (SimpleType)
              (Parameter (Variable) (SimpleType))
              (Parameter (Variable) (SimpleType) (Integer))
              (Parameter (Variable) (GenericType (SimpleType)
                (SimpleType)
                (SimpleType)))
              (Parameter (Variable) (GenericType (SimpleType)
                (SimpleType)
                (SimpleType)) (Hash))
              (Parameter (Variable) (GenericType (SimpleType)
                (SimpleType)))
              (Parameter (Variable) (GenericType (SimpleType)
                (SimpleType)) (Array))
              (Parameter (Variable) (SimpleType) (Equals (Variable) (Integer)))
              (Parameter (Variable) (SimpleType) (Equals (ChainedCall (Variable) (Variable)) (Integer)))
              (Parameter (Variable) (SimpleType) (Equals (ChainedCall (Variable) (Variable)) (Integer)))
              (Parameter (Variable) (Less (Variable) (Integer)))
              (Parameter (Variable) (LessEquals (Variable) (Integer)))
              (Parameter (Variable) (Greater (Variable) (Integer)))
              (Parameter (Variable) (GreaterEquals (Variable) (Integer)))
              (Parameter (Variable) (Equals (Variable) (Integer)))
              (Parameter (Variable) (Unequals (Variable) (Integer)))
              (Parameter (Variable) (InterfaceDecl (SimpleType))))))
          """

    _match_ast(ast, _parse(dedent(input)), 'Parameter')

def test_argument():
    input = """
            call(1)
            call(a=1)
            call(() =>
              1
            )
            """
    ast = """
          (File
            (FunctionCall (Variable)
              (Argument (Integer)))
            (FunctionCall (Variable)
              (Argument (Integer) (Variable)))
            (FunctionCall (Variable)
              (Argument (Function (Block
                (Integer)) (SimpleType)))))
          """

    _match_ast(ast, _parse(dedent(input)), 'Argument')

def test_struct_decl():
    input = """
            struct Test
              1

            mutable struct Test
              1
            """
    ast = """
          (File
            (StructDecl (SimpleType) (Block
              (Integer)))
            (StructDecl (SimpleType) (Block
              (Integer))))
          """

    _match_ast(ast, _parse(dedent(input)), 'StructDecl')

def test_module_decl():
    input = """
            module Test
              1

            mutable module Test
              1
            """
    ast = """
          (File
            (ModuleDecl (SimpleType) (Block
              (Integer)))
            (ModuleDecl (SimpleType) (Block
              (Integer))))
          """

    _match_ast(ast, _parse(dedent(input)), 'ModuleDecl')

def test_interface_decl():
    input = """
            interface Test
            interface Test
              func = ()
            """
    ast = """
          (File
            (InterfaceDecl (SimpleType))
            (InterfaceDecl (SimpleType)
              (AbstractFunction (SimpleType))))
          """

    _match_ast(ast, _parse(dedent(input)), 'InterfaceDecl')

def test_abstract_function():
    input = """
            interface Test
              func = ()
              func = (): Int
              func = (a: Int)
              __+__ = (a: Int, b: Int): Int
            """
    ast = """
          (File
            (InterfaceDecl (SimpleType)
              (AbstractFunction (SimpleType))
              (AbstractFunction (SimpleType))
              (AbstractFunction (SimpleType)
                (Parameter (Variable) (SimpleType)))
              (AbstractFunction (SimpleType)
                (Parameter (Variable) (SimpleType))
                (Parameter (Variable) (SimpleType)))))
          """

    _match_ast(ast, _parse(dedent(input)), 'AbstractFunction')

def test_function():
    input = """
            func = () =>
              1
            func = (): A => 1
            func = (a: Int) => 1
            func = (a: Int): A =>
              1
            __+__ = (a: Int, b: Int) => 1
            """
    ast = """
          (File
            (Assignment (Variable) (Function (Block
              (Integer)) (SimpleType)))
            (Assignment (Variable) (Function (Block
              (Integer)) (SimpleType)))
            (Assignment (Variable) (Function (Block
              (Integer)) (SimpleType)
              (Parameter (Variable) (SimpleType))))
            (Assignment (Variable) (Function (Block
              (Integer)) (SimpleType)
              (Parameter (Variable) (SimpleType))))
            (Assignment (Variable) (Function (Block
              (Integer)) (SimpleType)
              (Parameter (Variable) (SimpleType))
              (Parameter (Variable) (SimpleType)))))
          """

    _match_ast(ast, _parse(dedent(input)), 'Function')

def test_return():
    input = """
            ret 1
            ret if true
              1
            ret
            """
    ast = """
          (File
            (Return (Integer))
            (Return (If (Boolean) (Block
              (Integer))))
            (Return))
          """

    _match_ast(ast, _parse(dedent(input)), 'Return')

def test_else_clause():
    input = """
            if true
              1
            else
              1
            """
    ast = """
          (File
            (If (Boolean) (Block
              (Integer)) (Else (Block
              (Integer)))))
          """

    _match_ast(ast, _parse(dedent(input)), 'Else')

def test_else_if_clause():
    input = """
            if true
              1
            else if true
              1
            """
    ast = """
          (File
            (If (Boolean) (Block
              (Integer))
              (ElseIf (Boolean) (Block
                (Integer)))))
          """

    _match_ast(ast, _parse(dedent(input)), 'ElseIf')

def test_if():
    input = """
            if true
              1

            if true
              1
            else if true
              1

            if true
              1
            else if true
              1
            else if true
              1

            if true
              1
            else
              1

            if true
              1
            else if true
              1
            else
              1

            if true
              1
            else if true
              1
            else if true
              1
            else
              1
            """
    ast = """
          (File
            (If (Boolean) (Block
              (Integer)))
            (If (Boolean) (Block
              (Integer))
              (ElseIf (Boolean) (Block
                (Integer))))
            (If (Boolean) (Block
              (Integer))
              (ElseIf (Boolean) (Block
                (Integer)))
              (ElseIf (Boolean) (Block
                (Integer))))
            (If (Boolean) (Block
              (Integer)) (Else (Block
              (Integer))))
            (If (Boolean) (Block
              (Integer))
              (ElseIf (Boolean) (Block
                (Integer))) (Else (Block
              (Integer))))
            (If (Boolean) (Block
              (Integer))
              (ElseIf (Boolean) (Block
                (Integer)))
              (ElseIf (Boolean) (Block
                (Integer))) (Else (Block
              (Integer)))))
          """

    _match_ast(ast, _parse(dedent(input)), 'If')

def test_when_clause():
    input = """
            case true
            when false, nil
              1
            """
    ast = """
          (File
            (Case (Boolean)
              (When
                (Boolean)
                (Nil) (Block
                (Integer)))))
          """

    _match_ast(ast, _parse(dedent(input)), 'When')

def test_case():
    input = """
            case true
            when false
              1

            case true
            when false
              1
            when false
              1

            case true
            when false
              1
            else
              1
            """
    ast = """
          (File
            (Case (Boolean)
              (When
                (Boolean) (Block
                (Integer))))
            (Case (Boolean)
              (When
                (Boolean) (Block
                (Integer)))
              (When
                (Boolean) (Block
                (Integer))))
            (Case (Boolean)
              (When
                (Boolean) (Block
                (Integer))) (Else (Block
              (Integer)))))
          """

    _match_ast(ast, _parse(dedent(input)), 'Case')

def test_catch_clause():
    input = """
            try
              1
            catch Type
              1
            catch Type as var
              1
            """
    ast = """
          (File
            (Try (Block
              (Integer))
              (Catch (SimpleType) (Block
                (Integer)))
              (Catch (SimpleType) (Block
                (Integer)))))
          """

    _match_ast(ast, _parse(dedent(input)), 'Catch')

def test_try():
    input = """
            try
              1
            catch Type
              1
            try
              1
            catch Type
              1
            catch Type as var
              1
            """
    ast = """
          (File
            (Try (Block
              (Integer))
              (Catch (SimpleType) (Block
                (Integer))))
            (Try (Block
              (Integer))
              (Catch (SimpleType) (Block
                (Integer)))
              (Catch (SimpleType) (Block
                (Integer)))))
          """

    _match_ast(ast, _parse(dedent(input)), 'Try')

def test_select():
    input = """
            select
            when false
              1

            select
            when false
              1
            when false
              1

            select
            when false
              1
            else
              1
            """
    ast = """
          (File
            (Select
              (When
                (Boolean) (Block
                (Integer))))
            (Select
              (When
                (Boolean) (Block
                (Integer)))
              (When
                (Boolean) (Block
                (Integer))))
            (Select
              (When
                (Boolean) (Block
                (Integer))) (Else (Block
              (Integer)))))
          """

    _match_ast(ast, _parse(dedent(input)), 'Select')

def test_atomic():
    input = """
            atomic
              1
            """
    ast = """
          (File
            (Atomic (Block
              (Integer))))
          """

    _match_ast(ast, _parse(dedent(input)), 'Atomic')

def test_next():
    input = """
            next
            """
    ast = """
          (File
            (Return (Nil)))
          """

    _match_ast(ast, _parse(dedent(input)), 'Next')

def test_super():
    input = """
            super(Type[Type])
            """
    ast = """
          (File
            (Super (GenericType (SimpleType)
              (SimpleType))))
          """

    _match_ast(ast, _parse(dedent(input)), 'Super')

def test_panic():
    input = """
            panic 1
            panic if true
              1
            """
    ast = """
          (File
            (Panic (Integer))
            (Panic (If (Boolean) (Block
              (Integer)))))
          """

    _match_ast(ast, _parse(dedent(input)), 'Panic')

def test_throw():
    input = """
            throw 1
            throw if true
              1
            """
    ast = """
          (File
            (Throw (Integer))
            (Throw (If (Boolean) (Block
              (Integer)))))
          """

    _match_ast(ast, _parse(dedent(input)), 'Throw')

def test_hold():
    input = """
            hold 1
            hold if true
              1
            """
    ast = """
          (File
            (Hold (Integer))
            (Hold (If (Boolean) (Block
              (Integer)))))
          """

    _match_ast(ast, _parse(dedent(input)), 'Hold')

def test_do():
    input = """
            do call()
            do if true
              call()
            """
    ast = """
          (File
            (Do (FunctionCall (Variable)))
            (Do (If (Boolean) (Block
              (FunctionCall (Variable))))))
          """

    _match_ast(ast, _parse(dedent(input)), 'Do')

def test_retry():
    input = """
            retry
            """
    ast = """
          (File
            (Retry))
          """

    _match_ast(ast, _parse(dedent(input)), 'Retry')

def test_import():
    input = """
            import 'str'
            import Type from 'str'
            import Type, Type from 'str'
            import Type as Type from 'str'
            import * as Type from 'str'
            """
    ast = """
          (File
            (Import (String))
            (Import (String)
              (SimpleType): (SimpleType))
            (Import (String)
              (SimpleType): (SimpleType)
              (SimpleType): (SimpleType))
            (Import (String)
              (SimpleType): (SimpleType))
            (Import (String)))
          """

    _match_ast(ast, _parse(dedent(input)), 'Import')

def test_default_export():
    input = """
            export default Type
            """
    ast = """
          (File
            (DefaultExport (SimpleType)))
          """

    _match_ast(ast, _parse(dedent(input)), 'DefaultExport')

def test_export():
    input = """
            export Type
            export Type, Type
            """
    ast = """
          (File
            (Export
              (SimpleType))
            (Export
              (SimpleType)
              (SimpleType)))
          """

    _match_ast(ast, _parse(dedent(input)), 'Export')

def test_include():
    input = """
            include Type
            include Type, Type
            """
    ast = """
          (File
            (Include
              (SimpleType))
            (Include
              (SimpleType)
              (SimpleType)))
          """

    _match_ast(ast, _parse(dedent(input)), 'Include')

def test_grouping_expr():
    input = """
            (1 + (1 - 1))
            """
    ast = """
          (File
            (Sum (Integer) (Sub (Integer) (Integer))))
          """

    _match_ast(ast, _parse(dedent(input)), 'grouping expression')

def test_hash():
    input = """
            {}
            {'str': 1, 1: 'str'}
            """
    ast = """
          (File
            (Hash)
            (Hash
              (Integer): (String)
              (String): (Integer)))
          """

    _match_ast(ast, _parse(dedent(input)), 'Hash')

def test_array():
    input = """
            []
            [1, 'str']
            """
    ast = """
          (File
            (Array)
            (Array
              (Integer)
              (String)))
          """

    _match_ast(ast, _parse(dedent(input)), 'Array')

def test_get_call():
    input = """
            data[1]
            """
    ast = """
          (File
            (GetCall (Variable) (Integer)))
          """

    _match_ast(ast, _parse(dedent(input)), 'GetCall')

def test_function_call():
    input = """
            func()
            func(1, a, b='str')
            """
    ast = """
          (File
            (FunctionCall (Variable))
            (FunctionCall (Variable)
              (Argument (Integer))
              (Argument (Variable))
              (Argument (String) (Variable))))
          """

    _match_ast(ast, _parse(dedent(input)), 'FunctionCall')

def test_chained_call():
    input = """
            .a.b&.c
            """
    ast = """
          (File
            (ChainedCall (ChainedCall (ChainedCall (Self) (Variable)) (Variable)) (Variable)))
          """

    _match_ast(ast, _parse(dedent(input)), 'ChainedCall')

def test_unary_operation():
    input = """
            ++var
            --var
            **splat
            *splat
            not true
            ~1
            +1
            -1
            """
    ast = """
          (File
            (Assignment (Variable) (Sum (Variable) (Integer)))
            (Assignment (Variable) (Sub (Variable) (Integer)))
            (HashSplat (Variable))
            (ArraySplat (Variable))
            (LogicalNot (Boolean))
            (BinaryNot (Integer))
            (Pos (Integer))
            (Neg (Integer)))
          """

    _match_ast(ast, _parse(dedent(input)), 'unary operation')

def test_binary_operation():
    input = """
            1 ** 1
            1 * 1
            1 / 1
            1 mod 1
            1 + 1
            1 - 1
            1 << 1
            1 >> 1
            1 < 1
            1 <= 1
            1 > 1
            1 >= 1
            1 == 1
            1 != 1
            1 is 1
            1 & 1
            1 ^ 1
            1 | 1
            true and false
            true or false
            1 + 1 * 1 / 2 + 3 mod 4 - ~2
            """
    ast = """
          (File
            (Pow (Integer) (Integer))
            (Mul (Integer) (Integer))
            (Div (Integer) (Integer))
            (Mod (Integer) (Integer))
            (Sum (Integer) (Integer))
            (Sub (Integer) (Integer))
            (LeftShift (Integer) (Integer))
            (RightShift (Integer) (Integer))
            (Less (Integer) (Integer))
            (LessEquals (Integer) (Integer))
            (Greater (Integer) (Integer))
            (GreaterEquals (Integer) (Integer))
            (Equals (Integer) (Integer))
            (Unequals (Integer) (Integer))
            (Identical (Integer) (Integer))
            (BinaryAnd (Integer) (Integer))
            (BinaryXor (Integer) (Integer))
            (BinaryOr (Integer) (Integer))
            (LogicalAnd (Boolean) (Boolean))
            (LogicalOr (Boolean) (Boolean))
            (Sub (Sum (Sum (Integer) (Div (Mul (Integer) (Integer)) (Integer))) (Mod (Integer) (Integer))) (BinaryNot (Integer))))
          """

    _match_ast(ast, _parse(dedent(input)), 'binary operation')

def test_simple_if():
    input = """
            1 if true
            1 if false else 1
            """
    ast = """
          (File
            (SimpleIf (Boolean) (Integer))
            (SimpleIf (Boolean) (Integer) (Integer)))
          """

    _match_ast(ast, _parse(dedent(input)), 'SimpleIf')

def test_assignment():
    input = """
            var = 1
            var **= 1
            var *= 1
            var /= 1
            var mod= 1
            var += 1
            var -= 1
            var <<= 1
            var >>= 1
            var &= 1
            var ^= 1
            var |= 1
            var and= 1
            var or= 1
            bound.var or= 1
            var = if true
              1
            var **= if true
              1
            var *= if true
              1
            var /= if true
              1
            var mod= if true
              1
            var += if true
              1
            var -= if true
              1
            var <<= if true
              1
            var >>= if true
              1
            var &= if true
              1
            var ^= if true
              1
            var |= if true
              1
            var and= if true
              1
            var or= if true
              1
            bound.var or= if true
              1
            """
    ast = """
          (File
            (Assignment (Variable) (Integer))
            (Assignment (Variable) (Pow (Variable) (Integer)))
            (Assignment (Variable) (Mul (Variable) (Integer)))
            (Assignment (Variable) (Div (Variable) (Integer)))
            (Assignment (Variable) (Mod (Variable) (Integer)))
            (Assignment (Variable) (Sum (Variable) (Integer)))
            (Assignment (Variable) (Sub (Variable) (Integer)))
            (Assignment (Variable) (LeftShift (Variable) (Integer)))
            (Assignment (Variable) (RightShift (Variable) (Integer)))
            (Assignment (Variable) (BinaryAnd (Variable) (Integer)))
            (Assignment (Variable) (BinaryXor (Variable) (Integer)))
            (Assignment (Variable) (BinaryOr (Variable) (Integer)))
            (Assignment (Variable) (LogicalAnd (Variable) (Integer)))
            (Assignment (Variable) (LogicalOr (Variable) (Integer)))
            (Assignment (ChainedCall (Variable) (Variable)) (LogicalOr (ChainedCall (Variable) (Variable)) (Integer)))
            (Assignment (Variable) (If (Boolean) (Block
              (Integer))))
            (Assignment (Variable) (Pow (Variable) (If (Boolean) (Block
              (Integer)))))
            (Assignment (Variable) (Mul (Variable) (If (Boolean) (Block
              (Integer)))))
            (Assignment (Variable) (Div (Variable) (If (Boolean) (Block
              (Integer)))))
            (Assignment (Variable) (Mod (Variable) (If (Boolean) (Block
              (Integer)))))
            (Assignment (Variable) (Sum (Variable) (If (Boolean) (Block
              (Integer)))))
            (Assignment (Variable) (Sub (Variable) (If (Boolean) (Block
              (Integer)))))
            (Assignment (Variable) (LeftShift (Variable) (If (Boolean) (Block
              (Integer)))))
            (Assignment (Variable) (RightShift (Variable) (If (Boolean) (Block
              (Integer)))))
            (Assignment (Variable) (BinaryAnd (Variable) (If (Boolean) (Block
              (Integer)))))
            (Assignment (Variable) (BinaryXor (Variable) (If (Boolean) (Block
              (Integer)))))
            (Assignment (Variable) (BinaryOr (Variable) (If (Boolean) (Block
              (Integer)))))
            (Assignment (Variable) (LogicalAnd (Variable) (If (Boolean) (Block
              (Integer)))))
            (Assignment (Variable) (LogicalOr (Variable) (If (Boolean) (Block
              (Integer)))))
            (Assignment (ChainedCall (Variable) (Variable)) (LogicalOr (ChainedCall (Variable) (Variable)) (If (Boolean) (Block
              (Integer))))))
          """

    _match_ast(ast, _parse(dedent(input)), 'Assignment')

def test_decimal_expr():
    input = """
            1.0
            1_1.0_0
            1e1
            1e-1
            """
    ast = """
          (File
            (Decimal (Decimal))
            (Decimal (Decimal))
            (Decimal (Decimal))
            (Decimal (Decimal)))
          """

    _match_ast(ast, _parse(dedent(input)), 'Decimal')

def test_integer_expr():
    input = """
            1
            1_1
            """
    ast = """
          (File
            (Integer)
            (Integer))
          """

    _match_ast(ast, _parse(dedent(input)), 'Integer')

def test_string_expr():
    input = """
            's\\x00tr'
            'st\\'r'
            'lorem
            ipsum
            dolor
            set
            amet'
            'lorem
            ipsum
            dolor
            set
            amet'
            """
    ast = """
          (File
            (String)
            (String)
            (String)
            (String))
          """

    _match_ast(ast, _parse(dedent(input)), 'String')

def test_boolean_expr():
    input = """
            false
            true
            """
    ast = """
          (File
            (Boolean)
            (Boolean))
          """

    _match_ast(ast, _parse(dedent(input)), 'Boolean')

def test_nil_expr():
    input = """
            nil
            """
    ast = """
          (File
            (Nil))
          """

    _match_ast(ast, _parse(dedent(input)), 'Nil')

def test_self_expr():
    input = """
            self
            """
    ast = """
          (File
            (Self))
          """

    _match_ast(ast, _parse(dedent(input)), 'Self')

def test_complex_blocks():
    input = """
            module AnotherType
              1

            struct Type
              include AnotherType

              func = () =>
                1
            """
    ast = """
          (File
            (ModuleDecl (SimpleType) (Block
              (Integer)))
            (StructDecl (SimpleType) (Block
              (Include
                (SimpleType))
              (Assignment (Variable) (Function (Block
                (Integer)) (SimpleType))))))
          """

    _match_ast(ast, _parse(dedent(input)), 'complex blocks')

def test_four_spaces():
    input = """
            struct Test
                1
            """
    ast = """
          (File
            (StructDecl (SimpleType) (Block
              (Integer))))
          """

    _match_ast(ast, _parse(dedent(input)), 'four space indentation')

def test_tabs():
    input = """
            struct Test
            \t1
            """
    ast = """
          (File
            (StructDecl (SimpleType) (Block
              (Integer))))
          """

    _match_ast(ast, _parse(dedent(input)), 'tab indentation')

def test_leading_whitespace():
    input = """

            1
            """
    ast = """
          (File
            (Integer))
          """

    _match_ast(ast, _parse(dedent(input)), 'leading whitespace')

def test_trailing_whitespace():
    input = """
            1

            """
    ast = """
          (File
            (Integer))
          """

    _match_ast(ast, _parse(dedent(input)), 'trailing whitespace')

def test_comments():
    input = """
            1 // C$mment
            1// C$mment
            1/* C$mment
            C$mment

            C$mment*/ + 1
            /* C$mment */
            1
            """
    ast = """
          (File
            (Integer)
            (Integer)
            (Sum (Integer) (Integer))
            (Integer))
          """

    _match_ast(ast, _parse(dedent(input)), 'comments')

def test_ignore_newline_after_chr():
    input = """
            'hello' + \\
            'world'
            """
    ast = """
          (File
            (Sum (String) (String)))
          """

    _match_ast(ast, _parse(dedent(input)), 'ignore newline after \\')

def test_ignore_newlines_in_list():
    input = """
            ['hello', 'more',
                'nl',
                    'world']
            """
    ast = """
          (File
            (Array
              (String)
              (String)
              (String)
              (String)))
          """

    _match_ast(ast, _parse(dedent(input)), 'ignore newlines in list')

def test_ignore_redundant_newlines():
    input = """
            1


            1
            """
    ast = """
          (File
            (Integer)
            (Integer))
          """

    _match_ast(ast, _parse(dedent(input)), 'ignore redundant newlines')
