# -*- coding: utf-8 -*-
"""
A paired down version of static_anslysis from xdoctest
"""
from __future__ import absolute_import, division, print_function, unicode_literals
import os
import sys
import ast
import six
import sysconfig
from collections import OrderedDict
from os.path import (join, exists, expanduser, abspath, split, splitext,
                     isfile, dirname, basename, isdir, realpath, relpath)


def _parse_static_node_value(node):
    """
    Extract a constant value from an ast node if possible

    Args:
        node (ast.Node)

    Returns:
        object: static value of the node
    """
    if isinstance(node, ast.Num):
        value = node.n
    elif isinstance(node, ast.Str):
        value = node.s
    elif isinstance(node, ast.List):
        value = list(map(_parse_static_node_value, node.elts))
    elif isinstance(node, ast.Tuple):
        value = tuple(map(_parse_static_node_value, node.elts))
    elif isinstance(node, (ast.Dict)):
        keys = map(_parse_static_node_value, node.keys)
        values = map(_parse_static_node_value, node.values)
        value = OrderedDict(zip(keys, values))
        # value = dict(zip(keys, values))
    else:
        raise TypeError('Cannot parse a static value from non-static node '
                        'of type: {!r}'.format(type(node)))
    return value


def parse_static_value(key, source=None, fpath=None):
    """
    Statically parse a constant variable's value from python code.

    TODO: This does not belong here. Move this to an external static analysis
    library.

    Args:
        key (str): name of the variable
        source (str): python text
        fpath (str): filepath to read if source is not specified

    Example:
        >>> key = 'foo'
        >>> source = 'foo = 123'
        >>> assert parse_static_value(key, source=source) == 123
        >>> source = 'foo = "123"'
        >>> assert parse_static_value(key, source=source) == '123'
        >>> source = 'foo = [1, 2, 3]'
        >>> assert parse_static_value(key, source=source) == [1, 2, 3]
        >>> source = 'foo = (1, 2, "3")'
        >>> assert parse_static_value(key, source=source) == (1, 2, "3")
        >>> source = 'foo = {1: 2, 3: 4}'
        >>> assert parse_static_value(key, source=source) == {1: 2, 3: 4}
        >>> #parse_static_value('bar', source=source)
        >>> #parse_static_value('bar', source='foo=1; bar = [1, foo]')
    """
    if source is None:  # pragma: no branch
        with open(fpath, 'rb') as file_:
            source = file_.read().decode('utf-8')
    pt = ast.parse(source)

    class AssignentVisitor(ast.NodeVisitor):
        def visit_Assign(self, node):
            for target in node.targets:
                if getattr(target, 'id', None) == key:
                    self.value = _parse_static_node_value(node.value)

    sentinal = object()
    visitor = AssignentVisitor()
    visitor.value = sentinal
    visitor.visit(pt)
    if visitor.value is sentinal:
        raise NameError('No static variable named {!r}'.format(key))
    return visitor.value


def _extension_module_tags():
    """
    Returns valid tags an extension module might have
    """
    tags = []
    if six.PY2:
        # see also 'SHLIB_EXT'
        multiarch = sysconfig.get_config_var('MULTIARCH')
        if multiarch is not None:
            tags.append(multiarch)
    else:
        # handle PEP 3149 -- ABI version tagged .so files
        # ABI = application binary interface
        tags.append(sysconfig.get_config_var('SOABI'))
        tags.append('abi3')  # not sure why this one is valid but it is
    tags = [t for t in tags if t]
    return tags


def _platform_pylib_exts():  # nocover
    """
    Returns .so, .pyd, or .dylib depending on linux, win or mac.
    On python3 return the previous with and without abi (e.g.
    .cpython-35m-x86_64-linux-gnu) flags. On python2 returns with
    and without multiarch.
    """
    valid_exts = []
    if six.PY2:
        # see also 'SHLIB_EXT'
        base_ext = '.' + sysconfig.get_config_var('SO').split('.')[-1]
    else:
        # return with and without API flags
        # handle PEP 3149 -- ABI version tagged .so files
        base_ext = '.' + sysconfig.get_config_var('EXT_SUFFIX').split('.')[-1]
    for tag in _extension_module_tags():
        valid_exts.append('.' + tag + base_ext)
    valid_exts.append(base_ext)
    return tuple(valid_exts)


def normalize_modpath(modpath, hide_init=True, hide_main=False):
    """
    Normalizes __init__ and __main__ paths.

    Notes:
        Adds __init__ if reasonable, but only removes __main__ by default

    Args:
        hide_init (bool): if True, always return package modules
           as __init__.py files otherwise always return the dpath.
        hide_init (bool): if True, always strip away main files otherwise
           ignore __main__.py.

    Example:
        >>> import mkinit.static_analysis as static
        >>> modpath = static.__file__
        >>> assert static.normalize_modpath(modpath) == modpath
        >>> dpath = dirname(modpath)
        >>> res0 = static.normalize_modpath(dpath, hide_init=0, hide_main=0)
        >>> res1 = static.normalize_modpath(dpath, hide_init=0, hide_main=1)
        >>> res2 = static.normalize_modpath(dpath, hide_init=1, hide_main=0)
        >>> res3 = static.normalize_modpath(dpath, hide_init=1, hide_main=1)
        >>> assert res0.endswith('__init__.py')
        >>> assert res1.endswith('__init__.py')
        >>> assert not res2.endswith('.py')
        >>> assert not res3.endswith('.py')
    """
    if hide_init:
        if basename(modpath) == '__init__.py':
            modpath = dirname(modpath)
            hide_main = True
    else:
        # add in init, if reasonable
        modpath_with_init = join(modpath, '__init__.py')
        if exists(modpath_with_init):
            modpath = modpath_with_init
    if hide_main:
        # We can remove main, but dont add it
        if basename(modpath) == '__main__.py':
            # corner case where main might just be a module name not in a pkg
            parallel_init = join(dirname(modpath), '__init__.py')
            if exists(parallel_init):
                modpath = dirname(modpath)
    return modpath


def package_modpaths(pkgpath, with_pkg=False, with_mod=True, followlinks=True,
                     recursive=True, with_libs=False, check=True):
    r"""
    Finds sub-packages and sub-modules belonging to a package.

    Args:
        pkgpath (str): path to a module or package
        with_pkg (bool): if True includes package __init__ files (default =
            False)
        with_mod (bool): if True includes module files (default = True)
        exclude (list): ignores any module that matches any of these patterns
        recursive (bool): if False, then only child modules are included
        with_libs (bool): if True then compiled shared libs will be returned as well
        check (bool): if False, then then pkgpath is considered a module even
            if it does not contain an __init__ file.

    Yields:
        str: module names belonging to the package

    References:
        http://stackoverflow.com/questions/1707709/list-modules-in-py-package

    Example:
        >>> from mkinit.static_analysis import *
        >>> pkgpath = modname_to_modpath('mkinit')
        >>> paths = list(package_modpaths(pkgpath))
        >>> print('\n'.join(paths))
        >>> names = list(map(modpath_to_modname, paths))
        >>> assert 'mkinit.static_mkinit' in names
        >>> assert 'mkinit.__main__' in names
        >>> assert 'mkinit' not in names
        >>> print('\n'.join(names))
    """
    if isfile(pkgpath):
        # If input is a file, just return it
        yield pkgpath
    else:
        if with_pkg:
            root_path = join(pkgpath, '__init__.py')
            if not check or exists(root_path):
                yield root_path

        valid_exts = ['.py']
        if with_libs:
            valid_exts += _platform_pylib_exts()

        for dpath, dnames, fnames in os.walk(pkgpath, followlinks=followlinks):
            ispkg = exists(join(dpath, '__init__.py'))
            if ispkg or not check:
                check = True  # always check subdirs
                if with_mod:
                    for fname in fnames:
                        if splitext(fname)[1] in valid_exts:
                            # dont yield inits. Handled in pkg loop.
                            if fname != '__init__.py':
                                path = join(dpath, fname)
                                yield path
                if with_pkg:
                    for dname in dnames:
                        path = join(dpath, dname, '__init__.py')
                        if exists(path):
                            yield path
            else:
                # Stop recursing when we are out of the package
                del dnames[:]
            if not recursive:
                break


def split_modpath(modpath, check=True):
    """
    Splits the modpath into the dir that must be in PYTHONPATH for the module
    to be imported and the modulepath relative to this directory.

    Args:
        modpath (str): module filepath
        check (bool): if False, does not raise an error if modpath is a
            directory and does not contain an `__init__.py` file.

    Returns:
        tuple: (directory, rel_modpath)

    Raises:
        ValueError: if modpath does not exist or is not a package

    Example:
        >>> from mkinit import static_analysis
        >>> modpath = abspath(static_analysis.__file__)
        >>> modpath = modpath.replace('.pyc', '.py')
        >>> dpath, rel_modpath = split_modpath(modpath)
        >>> assert join(dpath, rel_modpath) == modpath, (
        >>>     '{!r} != {!r}'.format(join(dpath, rel_modpath), modpath))
        >>> assert rel_modpath == join('mkinit', 'static_analysis.py'), (
        >>>     '{!r} != {!r}'.format(rel_modpath, join('mkinit', 'static_analysis.py')))
    """
    modpath_ = abspath(expanduser(modpath))
    if check:
        if not exists(modpath_):
            if not exists(modpath):
                raise ValueError('modpath={} does not exist'.format(modpath))
            raise ValueError('modpath={} is not a module'.format(modpath))
        if isdir(modpath_) and not exists(join(modpath, '__init__.py')):
            # dirs without inits are not modules
            raise ValueError('modpath={} is not a module'.format(modpath))
    full_dpath, fname_ext = split(modpath_)
    _relmod_parts = [fname_ext]
    # Recurse down directories until we are out of the package
    dpath = full_dpath
    while exists(join(dpath, '__init__.py')):
        dpath, dname = split(dpath)
        _relmod_parts.append(dname)
    relmod_parts = _relmod_parts[::-1]
    rel_modpath = os.path.sep.join(relmod_parts)
    return dpath, rel_modpath


def modpath_to_modname(modpath, hide_init=True, hide_main=False, check=True,
                       relativeto=None):
    """
    Determines importable name from file path

    Converts the path to a module (__file__) to the importable python name
    (__name__) without importing the module.

    The filename is converted to a module name, and parent directories are
    recursively included until a directory without an __init__.py file is
    encountered.

    Args:
        modpath (str): module filepath
        hide_init (bool): removes the __init__ suffix (default True)
        hide_main (bool): removes the __main__ suffix (default False)
        check (bool): if False, does not raise an error if modpath is a dir
            and does not contain an __init__ file.
        relativeto (str, optional): if specified, all checks are ignored and
            this is considered the path to the root module.

    Returns:
        str: modname

    Raises:
        ValueError: if check is True and the path does not exist

    Example:
        >>> from mkinit import static_analysis
        >>> modpath = static_analysis.__file__
        >>> modpath = modpath.replace('.pyc', '.py')
        >>> modname = modpath_to_modname(modpath)
        >>> assert modname == 'mkinit.static_analysis'

    Example:
        >>> import mkinit
        >>> assert modpath_to_modname(mkinit.__file__) == 'mkinit'
        >>> assert modpath_to_modname(dirname(mkinit.__file__)) == 'mkinit'

    Example:
        >>> modpath = modname_to_modpath('_ctypes')
        >>> modname = modpath_to_modname(modpath)
        >>> assert modname == '_ctypes'
    """
    if check:
        if not exists(modpath):
            raise ValueError('modpath={} does not exist'.format(modpath))
    modpath_ = abspath(expanduser(modpath))

    modpath_ = normalize_modpath(modpath_, hide_init=hide_init,
                                 hide_main=hide_main)
    if relativeto:
        dpath = dirname(abspath(expanduser(relativeto)))
        rel_modpath = relpath(modpath_, dpath)
    else:
        dpath, rel_modpath = split_modpath(modpath_, check=check)

    modname = splitext(rel_modpath)[0]
    if '.' in modname:
        modname, abi_tag = modname.split('.')
    modname = modname.replace('/', '.')
    modname = modname.replace('\\', '.')
    return modname


def modname_to_modpath(modname, hide_init=True, hide_main=False, sys_path=None):
    """
    Finds the path to a python module from its name.

    Determines the path to a python module without directly import it

    Converts the name of a module (__name__) to the path (__file__) where it is
    located without importing the module. Returns None if the module does not
    exist.

    Args:
        modname (str): module filepath
        hide_init (bool): if False, __init__.py will be returned for packages
        hide_main (bool): if False, and hide_init is True, __main__.py will be
            returned for packages, if it exists.
        sys_path (list): if specified overrides `sys.path` (default None)

    Returns:
        str: modpath - path to the module, or None if it doesn't exist

    CommandLine:
        python -m mkinit.static_analysis modname_to_modpath:0

    Example:
        >>> modname = 'mkinit.__main__'
        >>> modpath = modname_to_modpath(modname, hide_main=False)
        >>> assert modpath.endswith('__main__.py')
        >>> modname = 'mkinit'
        >>> modpath = modname_to_modpath(modname, hide_init=False)
        >>> assert modpath.endswith('__init__.py')
        >>> modpath = basename(modname_to_modpath('_ctypes'))
        >>> assert 'ctypes' in modpath
    """
    modpath = _syspath_modname_to_modpath(modname, sys_path)
    if modpath is None:
        return None

    modpath = normalize_modpath(modpath, hide_init=hide_init,
                                hide_main=hide_main)
    return modpath


def _syspath_modname_to_modpath(modname, sys_path=None, exclude=None):
    """
    syspath version of modname_to_modpath

    Args:
        modname (str): name of module to find
        sys_path (list): if specified overrides `sys.path` (default None)
        exclude (list): list of directory paths. if specified prevents these
            directories from being searched.

    Notes:
        This is much slower than the pkgutil mechanisms.

    CommandLine:
        python -m mkinit.static_analysis _syspath_modname_to_modpath

    Example:
        >>> print(_syspath_modname_to_modpath('mkinit.static_analysis'))
        ...static_analysis.py
        >>> print(_syspath_modname_to_modpath('mkinit'))
        ...mkinit
        >>> print(_syspath_modname_to_modpath('_ctypes'))
        ..._ctypes...
        >>> assert _syspath_modname_to_modpath('mkinit', sys_path=[]) is None
        >>> assert _syspath_modname_to_modpath('mkinit.static_analysis', sys_path=[]) is None
        >>> assert _syspath_modname_to_modpath('_ctypes', sys_path=[]) is None
        >>> assert _syspath_modname_to_modpath('this', sys_path=[]) is None

    Example:
        >>> # test what happens when the module is not visible in the path
        >>> modname = 'mkinit.static_analysis'
        >>> modpath = _syspath_modname_to_modpath(modname)
        >>> exclude = [split_modpath(modpath)[0]]
        >>> found = _syspath_modname_to_modpath(modname, exclude=exclude)
        >>> # this only works if installed in dev mode, pypi fails
        >>> assert found is None, 'should not have found {}'.format(found)
    """

    def _isvalid(modpath, base):
        # every directory up to the module, should have an init
        subdir = dirname(modpath)
        while subdir and subdir != base:
            if not exists(join(subdir, '__init__.py')):
                return False
            subdir = dirname(subdir)
        return True

    _fname_we = modname.replace('.', os.path.sep)
    candidate_fnames = [
        _fname_we + '.py',
        # _fname_we + '.pyc',
        # _fname_we + '.pyo',
    ]
    # Add extension library suffixes
    candidate_fnames += [_fname_we + ext for ext in _platform_pylib_exts()]

    if sys_path is None:
        sys_path = sys.path

    # the empty string in sys.path indicates cwd. Change this to a '.'
    candidate_dpaths = ['.' if p == '' else p for p in sys_path]

    if exclude:
        def normalize(p):
            if sys.platform.startswith('win32'):
                return realpath(p).lower()
            else:
                return realpath(p)
        # Keep only the paths not in exclude
        real_exclude = {normalize(p) for p in exclude}
        candidate_dpaths = [p for p in candidate_dpaths
                            if normalize(p) not in real_exclude]

    for dpath in candidate_dpaths:
        # Check for directory-based modules (has presidence over files)
        modpath = join(dpath, _fname_we)
        if exists(modpath):
            if isfile(join(modpath, '__init__.py')):
                if _isvalid(modpath, dpath):
                    return modpath

        # If that fails, check for file-based modules
        for fname in candidate_fnames:
            modpath = join(dpath, fname)
            if isfile(modpath):
                if _isvalid(modpath, dpath):
                    return modpath


def is_balanced_statement(lines):
    """
    Checks if the lines have balanced parens, brakets, curlies and strings

    Args:
        lines (list): list of strings

    Returns:
        bool: False if the statement is not balanced

    Doctest:
        >>> assert is_balanced_statement(['print(foobar)'])
        >>> assert is_balanced_statement(['foo = bar']) is True
        >>> assert is_balanced_statement(['foo = (']) is False
        >>> assert is_balanced_statement(['foo = (', "')(')"]) is True
        >>> assert is_balanced_statement(
        ...     ['foo = (', "'''", ")]'''", ')']) is True
        >>> #assert is_balanced_statement(['foo = ']) is False
        >>> #assert is_balanced_statement(['== ']) is False

    """
    from six.moves import cStringIO as StringIO
    import tokenize
    block = '\n'.join(lines)
    if six.PY2:
        block = block.encode('utf8')
    stream = StringIO()
    stream.write(block)
    stream.seek(0)
    try:
        for t in tokenize.generate_tokens(stream.readline):
            pass
    except tokenize.TokenError as ex:
        message = ex.args[0]
        if message.startswith('EOF in multi-line'):
            return False
        raise
    else:
        # Note: trying to use ast.parse(block) will not work
        # here because it breaks in try, except, else
        return True


def _locate_ps1_linenos(source_lines):
    """
    Determines which lines in the source begin a "logical block" of code.

    Notes:
        implementation taken from xdoctest.parser

    Args:
        source_lines (list): lines belonging only to the doctest src
            these will be unindented, prefixed, and without any want.

    Returns:
        (list, bool): a list of indices indicating which lines
           are considered "PS1" and a flag indicating if the final line
           should be considered for a got/want assertion.

    Example:
        >>> source_lines = ['>>> def foo():', '>>>     return 0', '>>> 3']
        >>> linenos, eval_final = _locate_ps1_linenos(source_lines)
        >>> assert linenos == [0, 2]
        >>> assert eval_final is True

    Example:
        >>> source_lines = ['>>> x = [1, 2, ', '>>> 3, 4]', '>>> print(len(x))']
        >>> linenos, eval_final = _locate_ps1_linenos(source_lines)
        >>> assert linenos == [0, 2]
        >>> assert eval_final is True
    """
    import ast
    import sys
    # print('source_lines = {!r}'.format(source_lines))
    # Strip indentation (and PS1 / PS2 from source)
    exec_source_lines = [p[4:] for p in source_lines]

    # Hack to make comments appear like executable statements
    # note, this hack never leaves this function because we only are
    # returning line numbers.
    exec_source_lines = ['_._  = None' if p.startswith('#') else p
                         for p in exec_source_lines]

    source_block = '\n'.join(exec_source_lines)
    try:
        pt = ast.parse(source_block, filename='<source_block>')
    except SyntaxError as syn_ex:
        # Assign missing information to the syntax error.
        if syn_ex.text is None:
            if syn_ex.lineno is not None:
                # Grab the line where the error occurs
                # (why is this not populated in SyntaxError by default?)
                # (because filename does not point to a valid loc)
                line = source_block.split('\n')[syn_ex.lineno - 1]
                syn_ex.text = line  + '\n'
        raise syn_ex

    statement_nodes = pt.body
    ps1_linenos = [node.lineno - 1 for node in statement_nodes]
    NEED_16806_WORKAROUND = True
    if NEED_16806_WORKAROUND:  # pragma: nobranch
        ps1_linenos = _workaround_16806(ps1_linenos, exec_source_lines)
    # Respect any line explicitly defined as PS2 (via its prefix)
    ps2_linenos = {
        x for x, p in enumerate(source_lines) if p[:4] != '>>> '
    }
    ps1_linenos = sorted(ps1_linenos.difference(ps2_linenos))

    if len(statement_nodes) == 0:
        eval_final = False
    else:
        # Is the last statement evaluatable?
        if sys.version_info.major == 2:  # nocover
            eval_final = isinstance(statement_nodes[-1], (
                ast.Expr, ast.Print))
        else:
            # This should just be an Expr in python3
            # (todo: ensure this is true)
            eval_final = isinstance(statement_nodes[-1], ast.Expr)

    return ps1_linenos, eval_final


def _workaround_16806(ps1_linenos, exec_source_lines):
    """
    workaround for python issue 16806 (https://bugs.python.org/issue16806)

    Issue causes lineno for multiline strings to give the line they end on,
    not the line they start on.  A patch for this issue exists
    `https://github.com/python/cpython/pull/1800`

    Notes:
        Starting from the end look at consecutive pairs of indices to
        inspect the statment it corresponds to.  (the first statment goes
        from ps1_linenos[-1] to the end of the line list.

        Implementation taken from xdoctest.parser
    """
    new_ps1_lines = []
    b = len(exec_source_lines)
    for a in ps1_linenos[::-1]:
        # the position of `b` is correct, but `a` may be wrong
        # is_balanced_statement will be False iff `a` is wrong.
        while not is_balanced_statement(exec_source_lines[a:b]):
            # shift `a` down until it becomes correct
            a -= 1
        # push the new correct value back into the list
        new_ps1_lines.append(a)
        # set the end position of the next string to be `a` ,
        # note, because this `a` is correct, the next `b` is
        # must also be correct.
        b = a
    ps1_linenos = set(new_ps1_lines)
    return ps1_linenos


if __name__ == '__main__':
    """
    CommandLine:
        python -m mkinit.static_analysis all
    """
    import xdoctest
    xdoctest.doctest_module(__file__)
