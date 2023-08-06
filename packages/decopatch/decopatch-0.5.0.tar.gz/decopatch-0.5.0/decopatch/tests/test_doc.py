from __future__ import print_function
import sys

import pytest

from decopatch import function_decorator, DECORATED, \
    InvalidMandatoryArgError, AmbiguousDecoratorDefinitionError, class_decorator

try:  # python 3.3+
    from inspect import signature
except ImportError:
    from funcsigs import signature


@pytest.mark.parametrize('usage_first', [True, False], ids="usage_first={}".format)
@pytest.mark.parametrize('uses_introspection', [True, False], ids="uses_introspection={}".format)
def test_doc_impl_first_tag_mandatory(uses_introspection, usage_first):
    """ The first implementation-first example in the doc """

    if usage_first:
        @function_decorator(enable_stack_introspection=uses_introspection)
        def add_tag(tag):
            """
            This decorator adds the 'my_tag' tag on the decorated function,
            with the value provided as argument

            :param tag: the tag value to set
            :param f: represents the decorated item. Automatically injected.
            :return:
            """

            def replace_f(f):
                setattr(f, 'my_tag', tag)
                return f

            return replace_f
    else:
        @function_decorator(enable_stack_introspection=uses_introspection)
        def add_tag(tag, f=DECORATED):
            """
            This decorator adds the 'my_tag' tag on the decorated function,
            with the value provided as argument

            :param tag: the tag value to set
            :param f: represents the decorated item. Automatically injected.
            :return:
            """
            setattr(f, 'my_tag', tag)
            return f

    @add_tag('hello')
    def foo():
        return

    assert foo.my_tag == 'hello'

    err_type = TypeError if uses_introspection else InvalidMandatoryArgError
    with pytest.raises(err_type):
        # add_tag() missing 1 required positional argument: 'tag'
        @add_tag
        def foo():
            if True:
                return

    if not uses_introspection:
        with pytest.raises(InvalidMandatoryArgError):
            # first argument is a callable > problem
            @add_tag(print)
            def foo():
                return
    else:
        # no problem
        @add_tag(print)
        def foo():
            return

        assert foo.my_tag == print


def test_doc_impl_first_tag_optional():
    """ The second implementation-first example in the doc """

    @function_decorator
    def add_tag(tag='tag!', f=DECORATED):
        """
        This decorator adds the 'my_tag' tag on the decorated function,
        with the value provided as argument

        :param tag: the tag value to set
        :param f: represents the decorated item. Automatically injected.
        :return:
        """
        setattr(f, 'my_tag', tag)
        return f

    @add_tag('hello')  # normal arg
    def foo():
        return

    assert foo.my_tag == 'hello'

    @add_tag(tag='hello')  # normal kwarg
    def foo():
        return

    assert foo.my_tag == 'hello'

    @add_tag  # no parenthesis
    def foo():
        return

    assert foo.my_tag == 'tag!'

    @add_tag()  # empty parenthesis
    def foo():
        return

    assert foo.my_tag == 'tag!'

    @add_tag(print)  # callable as first arg
    def foo():
        return

    assert foo.my_tag == print

    @add_tag(tag=print)  # callable as first kwarg
    def foo():
        return

    assert foo.my_tag == print


def test_doc_impl_first_say_hello(capsys):
    """The second implementation-first example in the doc"""

    @function_decorator
    def say_hello(person='world', f=DECORATED):
        """
        This decorator modifies the decorated function so that a nice hello
        message is printed before the call.

        :param person: the person name in the print message. Default = "world"
        :param f: represents the decorated item. Automatically injected.
        :return: a modified version of `f` that will print a hello message before executing
        """

        # create a wrapper of f that will do the print before call
        # we rely on `makefun.with_signature` to preserve signature
        def new_f(*args, **kwargs):
            # nonlocal person
            person = new_f.person
            print("hello, %s !" % person)  # say hello
            return f(*args, **kwargs)  # call f

        # we use the trick at https://stackoverflow.com/a/16032631/7262247
        # to access the nonlocal 'person' variable in python 2 and 3
        # for python 3 only you can use 'nonlocal' https://www.python.org/dev/peps/pep-3104/
        new_f.person = person

        # return the wrapper
        return new_f

    @say_hello
    def foo(a, b):
        return a + b

    @say_hello()
    def bar(a, b):
        return a + b

    @say_hello("you")
    def custom(a, b):
        return a + b

    assert foo(1, 3) == 4
    assert bar(1, 3) == 4
    assert custom(1, 3) == 4

    help(say_hello)

    print("Signature: %s" % signature(say_hello))

    captured = capsys.readouterr()
    with capsys.disabled():
        print(captured.out)

    assert captured.out == """hello, world !
hello, world !
hello, you !
Help on function say_hello in module decopatch.tests.test_doc:

say_hello(person='world')
    This decorator modifies the decorated function so that a nice hello
    message is printed before the call.
    
    :param person: the person name in the print message. Default = "world"
    :param f: represents the decorated item. Automatically injected.
    :return: a modified version of `f` that will print a hello message before executing

Signature: (person='world')
"""

    assert captured.err == ""


@pytest.mark.parametrize('uses_introspection', [True, False])
def test_doc_impl_first_class_tag_mandatory(uses_introspection):
    """ The first implementation-first example in the doc """

    @class_decorator(enable_stack_introspection=uses_introspection)
    def add_tag(tag, c=DECORATED):
        """
        This decorator adds the 'my_tag' tag on the decorated function,
        with the value provided as argument

        :param tag: the tag value to set
        :param c: represents the decorated item. Automatically injected.
        :return:
        """
        setattr(c, 'my_tag', tag)
        return c

    @add_tag('hello')
    class Foo(object):
        pass

    assert Foo.my_tag == 'hello'

    err_type = TypeError if uses_introspection else InvalidMandatoryArgError
    with pytest.raises(err_type):
        # add_tag() missing 1 required positional argument: 'tag'
        @add_tag
        class Foo(object):
            def __init__(self):
                if True:
                    pass

            def blah(self):
                pass

    if not uses_introspection:
        with pytest.raises(InvalidMandatoryArgError):
            # first argument is a class > problem
            @add_tag(object)
            class Foo(object):
                pass
    else:
        # no problem
        @add_tag(object)
        class Foo(object):
            pass

        assert Foo.my_tag == object


def test_doc_usage_first_tag_mandatory():

    @function_decorator
    def add_tag(tag):
        """
        This decorator adds the 'my_tag' tag on the decorated function,
        with the value provided as argument

        :param tag: the tag value to set
        :param f: represents the decorated item. Automatically injected.
        :return:
        """

        def replace_f(f):
            setattr(f, 'my_tag', tag)
            return f

        return replace_f


# ----------- more complex / other tests derived from the above for the advanced section

@pytest.mark.parametrize('with_star', [True], ids="kwonly={}".format)
@pytest.mark.parametrize('uses_introspection', [True, False], ids="uses_introspection={}".format)
def test_doc_impl_first_tag_mandatory_protected(with_star, uses_introspection):

    if with_star:
        if sys.version_info < (3, 0):
            pytest.skip("test skipped in python 2.x because kw only is not syntactically correct")
        else:
            from decopatch.tests._test_doc_py3 import create_test_doc_impl_first_tag_mandatory_protected_with_star
            add_tag = create_test_doc_impl_first_tag_mandatory_protected_with_star(uses_introspection)
    else:
        raise NotImplementedError()

    @add_tag(tag='hello')
    def foo():
        return

    assert foo.my_tag == 'hello'

    with pytest.raises(TypeError):
        # add_tag() missing 1 required positional argument: 'tag'
        @add_tag
        def foo():
            return

    @add_tag(tag=print)
    def foo():
        return

    assert foo.my_tag == print


@pytest.mark.parametrize('with_star', [False, True], ids="kwonly={}".format)
def test_doc_impl_first_tag_optional_nonprotected(with_star):
    """Tests that an error is raised when nonprotected code is created """
    with pytest.raises(AmbiguousDecoratorDefinitionError):
        if with_star:
            if sys.version_info < (3, 0):
                pytest.skip("test skipped in python 2.x because kw only is not syntactically correct")
            else:
                from decopatch.tests._test_doc_py3 import create_test_doc_impl_first_tag_optional_nonprotected_star
                add_tag = create_test_doc_impl_first_tag_optional_nonprotected_star()
        else:
            @function_decorator(enable_stack_introspection=False)
            def add_tag(tag='tag!', f=DECORATED):
                """
                This decorator adds the 'my_tag' tag on the decorated function,
                with the value provided as argument

                :param tag: the tag value to set
                :param f: represents the decorated item. Automatically injected.
                :return:
                """
                setattr(f, 'my_tag', tag)
                return f

    # @add_tag(tag='hello')
    # def foo():
    #     return
    #
    # assert foo.my_tag == 'hello'
    #
    # @add_tag
    # def foo():
    #     return
    #
    # assert foo.my_tag == 'tag!'


@pytest.mark.parametrize('with_star', [False, True], ids="kwonly={}".format)
@pytest.mark.parametrize('uses_introspection', [True, False], ids="introspection={}".format)
def test_doc_impl_first_tag_optional_protected(with_star, uses_introspection):
    """ The second implementation-first example in the doc """

    if with_star:
        if sys.version_info < (3, 0):
            pytest.skip("test skipped in python 2.x because kw only is not syntactically correct")
        else:
            from decopatch.tests._test_doc_py3 import create_test_doc_impl_first_tag_optional_protected
            add_tag = create_test_doc_impl_first_tag_optional_protected(uses_introspection)
    else:
        # protect it explicitly if introspection is disabled
        @function_decorator(can_first_arg_be_ambiguous=None if uses_introspection else False,
                            enable_stack_introspection=uses_introspection)
        def add_tag(tag='tag!', f=DECORATED):
            """
            This decorator adds the 'my_tag' tag on the decorated function,
            with the value provided as argument

            :param tag: the tag value to set
            :param f: represents the decorated item. Automatically injected.
            :return:
            """
            setattr(f, 'my_tag', tag)
            return f

    @add_tag(tag='hello')
    def foo():
        return

    assert foo.my_tag == 'hello'

    @add_tag
    def foo():
        return

    assert foo.my_tag == 'tag!'

    if with_star or uses_introspection:
        # when we add the star, disambiguation always works (even without introspection
        @add_tag(tag=print)
        def foo():
            return

        assert foo.my_tag == print
    else:
        # when we do not add the star and "poor man's disambiguation" (no introspection) is used, theres a problem
        with pytest.raises(AttributeError):
            @add_tag(tag=print)
            def foo():
                return

    if not uses_introspection:
        with pytest.raises(AttributeError):
            @add_tag(print)
            def foo():
                return
    elif with_star:
        with pytest.raises(TypeError):
            @add_tag(print)
            def foo():
                return
    else:
        @add_tag(print)
        def foo():
            return

        assert foo.my_tag == print
