# -*- coding: utf-8 -*-
# This file is part of the lib3to6 project
# https://gitlab.com/mbarkhau/lib3to6
#
# Copyright (c) 2019 Manuel Barkhau (mbarkhau@gmail.com) - MIT License
# SPDX-License-Identifier: MIT

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import sys
import ast
try:
    import builtins
except ImportError:
    import __builtin__ as builtins
import itertools
import typing as typ
str = getattr(builtins, 'unicode', str)
zip = getattr(itertools, 'izip', zip)
from . import common
from . import utils
ContainerNodes = ast.List, ast.Set, ast.Tuple
ImmutableValueNodes = ast.Num, ast.Str, ast.Bytes, ast.NameConstant
LeafNodes = (ast.Num, ast.Str, ast.Bytes, ast.NameConstant, ast.Name, ast.
    cmpop, ast.boolop, ast.operator, ast.unaryop, ast.expr_context)
ArgUnpackNodes = ast.Call, ast.List, ast.Tuple, ast.Set
KwArgUnpackNodes = ast.Call, ast.Dict


class VersionInfo(object):
    apply_since = None
    apply_until = None
    works_since = None
    works_until = None

    def __init__(self, apply_since, apply_until, works_since=None,
        works_until=None):
        self.apply_since = apply_since
        self.apply_until = apply_until
        if works_since is None:
            self.works_since = self.apply_since
        else:
            self.works_since = works_since
        self.works_until = works_until


class FixerBase(object):
    version_info = None
    required_imports = None
    module_declarations = None

    def __init__(self):
        self.required_imports = set()
        self.module_declarations = set()

    def __call__(self, cfg, tree):
        raise NotImplementedError()

    def is_required_for(self, version):
        nfo = self.version_info
        return nfo.apply_since <= version <= nfo.apply_until

    def is_compatible_with(self, version):
        nfo = self.version_info
        return nfo.works_since <= version and (nfo.works_until is None or 
            version <= nfo.works_until)

    def is_applicable_to(self, src_version, tgt_version):
        return self.is_compatible_with(src_version) and self.is_required_for(
            tgt_version)


class TransformerFixerBase(FixerBase, ast.NodeTransformer):

    def __call__(self, cfg, tree):
        try:
            return self.visit(tree)
        except common.FixerError as ex:
            if ex.module is None:
                ex.module = tree
            raise


class FutureImportFixerBase(FixerBase):
    future_name = None

    def __call__(self, cfg, tree):
        self.required_imports.add(common.ImportDecl('__future__', self.
            future_name, None))
        return tree


class AnnotationsFutureFixer(FutureImportFixerBase):
    version_info = VersionInfo(apply_since='3.7', apply_until='3.9')
    future_name = 'annotations'


class GeneratorStopFutureFixer(FutureImportFixerBase):
    version_info = VersionInfo(apply_since='3.5', apply_until='3.6')
    future_name = 'generator_stop'


class UnicodeLiteralsFutureFixer(FutureImportFixerBase):
    version_info = VersionInfo(apply_since='2.6', apply_until='2.7')
    future_name = 'unicode_literals'


class PrintFunctionFutureFixer(FutureImportFixerBase):
    version_info = VersionInfo(apply_since='2.6', apply_until='2.7')
    future_name = 'print_function'


class WithStatementFutureFixer(FutureImportFixerBase):
    version_info = VersionInfo(apply_since='2.5', apply_until='2.5')
    future_name = 'with_statement'


class AbsoluteImportFutureFixer(FutureImportFixerBase):
    version_info = VersionInfo(apply_since='2.5', apply_until='2.7')
    future_name = 'absolute_import'


class DivisionFutureFixer(FutureImportFixerBase):
    version_info = VersionInfo(apply_since='2.2', apply_until='2.7')
    future_name = 'division'


class GeneratorsFutureFixer(FutureImportFixerBase):
    version_info = VersionInfo(apply_since='2.2', apply_until='2.2')
    future_name = 'generators'


class NestedScopesFutureFixer(FutureImportFixerBase):
    version_info = VersionInfo(apply_since='2.1', apply_until='2.1')
    future_name = 'nested_scopes'


class ModuleImportFallbackFixerBase(TransformerFixerBase):
    new_name = None
    old_name = None

    def _try_fallback(self, node, fallback_node):
        return ast.Try(body=[node], handlers=[ast.ExceptHandler(type=ast.
            Name(id='ImportError', ctx=ast.Load()), name=None, body=[
            fallback_node])], orelse=[], finalbody=[])

    def visit_Import(self, node):
        if len(node.names) != 1:
            return node
        alias = node.names[0]
        if alias.name != self.new_name:
            return node
        if alias.asname:
            asname = alias.asname
        elif '.' in self.new_name:
            asname = self.new_name.replace('.', '_')
            msg = (
                "Prohibited use of 'import {0}', use 'import {1} as {2}' instead."
                .format(self.new_name, self.new_name, asname))
            raise common.CheckError(msg, node)
        else:
            asname = self.new_name
        return self._try_fallback(node, ast.Import(names=[ast.alias(name=
            self.old_name, asname=asname)]))

    def visit_ImportFrom(self, node):
        if node.module != self.new_name:
            return node
        return self._try_fallback(node, ast.ImportFrom(module=self.old_name,
            names=node.names, level=node.level))


class ConfigParserImportFallbackFixer(ModuleImportFallbackFixerBase):
    version_info = VersionInfo(apply_since='2.3', apply_until='2.7',
        works_until='3.7')
    new_name = 'configparser'
    old_name = 'ConfigParser'


class SocketServerImportFallbackFixer(ModuleImportFallbackFixerBase):
    version_info = VersionInfo(apply_since='2.3', apply_until='2.7',
        works_until='3.7')
    new_name = 'socketserver'
    old_name = 'SocketServer'


class BuiltinsImportFallbackFixer(ModuleImportFallbackFixerBase):
    version_info = VersionInfo(apply_since='2.3', apply_until='2.7',
        works_until='3.7')
    new_name = 'builtins'
    old_name = '__builtin__'


class QueueImportFallbackFixer(ModuleImportFallbackFixerBase):
    version_info = VersionInfo(apply_since='2.3', apply_until='2.7',
        works_until='3.7')
    new_name = 'queue'
    old_name = 'Queue'


class CopyRegImportFallbackFixer(ModuleImportFallbackFixerBase):
    version_info = VersionInfo(apply_since='2.3', apply_until='2.7',
        works_until='3.7')
    new_name = 'copyreg'
    old_name = 'copy_reg'


class WinRegImportFallbackFixer(ModuleImportFallbackFixerBase):
    version_info = VersionInfo(apply_since='2.3', apply_until='2.7',
        works_until='3.7')
    new_name = 'winreg'
    old_name = '_winreg'


class ReprLibImportFallbackFixer(ModuleImportFallbackFixerBase):
    version_info = VersionInfo(apply_since='2.3', apply_until='2.7',
        works_until='3.7')
    new_name = 'reprlib'
    old_name = 'repr'


class ThreadImportFallbackFixer(ModuleImportFallbackFixerBase):
    version_info = VersionInfo(apply_since='2.3', apply_until='2.7',
        works_until='3.7')
    new_name = '_thread'
    old_name = 'thread'


class DummyThreadImportFallbackFixer(ModuleImportFallbackFixerBase):
    version_info = VersionInfo(apply_since='2.3', apply_until='2.7',
        works_until='3.7')
    new_name = '_dummy_thread'
    old_name = 'dummy_thread'


class HttpCookiejarImportFallbackFixer(ModuleImportFallbackFixerBase):
    version_info = VersionInfo(apply_since='2.3', apply_until='2.7',
        works_until='3.7')
    new_name = 'http.cookiejar'
    old_name = 'cookielib'


class UrllibParseImportFallbackFixer(ModuleImportFallbackFixerBase):
    version_info = VersionInfo(apply_since='2.3', apply_until='2.7',
        works_until='3.7')
    new_name = 'urllib.parse'
    old_name = 'urlparse'


class UrllibRequestImportFallbackFixer(ModuleImportFallbackFixerBase):
    version_info = VersionInfo(apply_since='2.3', apply_until='2.7',
        works_until='3.7')
    new_name = 'urllib.request'
    old_name = 'urllib2'


class UrllibErrorImportFallbackFixer(ModuleImportFallbackFixerBase):
    version_info = VersionInfo(apply_since='2.3', apply_until='2.7',
        works_until='3.7')
    new_name = 'urllib.error'
    old_name = 'urllib2'


class UrllibRobotParserImportFallbackFixer(ModuleImportFallbackFixerBase):
    version_info = VersionInfo(apply_since='2.3', apply_until='2.7',
        works_until='3.7')
    new_name = 'urllib.robotparser'
    old_name = 'robotparser'


class XMLRPCClientImportFallbackFixer(ModuleImportFallbackFixerBase):
    version_info = VersionInfo(apply_since='2.3', apply_until='2.7',
        works_until='3.7')
    new_name = 'xmlrpc.client'
    old_name = 'xmlrpclib'


class XmlrpcServerImportFallbackFixer(ModuleImportFallbackFixerBase):
    version_info = VersionInfo(apply_since='2.3', apply_until='2.7',
        works_until='3.7')
    new_name = 'xmlrpc.server'
    old_name = 'SimpleXMLRPCServer'


class HtmlParserImportFallbackFixer(ModuleImportFallbackFixerBase):
    version_info = VersionInfo(apply_since='2.3', apply_until='2.7',
        works_until='3.7')
    new_name = 'html.parser'
    old_name = 'HTMLParser'


class HttpClientImportFallbackFixer(ModuleImportFallbackFixerBase):
    version_info = VersionInfo(apply_since='2.3', apply_until='2.7',
        works_until='3.7')
    new_name = 'http.client'
    old_name = 'httplib'


class HttpCookiesImportFallbackFixer(ModuleImportFallbackFixerBase):
    version_info = VersionInfo(apply_since='2.3', apply_until='2.7',
        works_until='3.7')
    new_name = 'http.cookies'
    old_name = 'Cookie'


class PickleImportFallbackFixer(ModuleImportFallbackFixerBase):
    version_info = VersionInfo(apply_since='2.3', apply_until='2.7',
        works_until='3.7')
    new_name = 'pickle'
    old_name = 'cPickle'


class DbmGnuImportFallbackFixer(ModuleImportFallbackFixerBase):
    version_info = VersionInfo(apply_since='2.3', apply_until='2.7',
        works_until='3.7')
    new_name = 'dbm.gnu'
    old_name = 'gdbm'


class EmailMimeBaseImportFallbackFixer(ModuleImportFallbackFixerBase):
    version_info = VersionInfo(apply_since='2.3', apply_until='2.7',
        works_until='3.7')
    new_name = 'email.mime.base'
    old_name = 'email.MIMEBase'


class EmailMimeImageImportFallbackFixer(ModuleImportFallbackFixerBase):
    version_info = VersionInfo(apply_since='2.3', apply_until='2.7',
        works_until='3.7')
    new_name = 'email.mime.image'
    old_name = 'email.MIMEImage'


class EmailMimeMultipartImportFallbackFixer(ModuleImportFallbackFixerBase):
    version_info = VersionInfo(apply_since='2.3', apply_until='2.7',
        works_until='3.7')
    new_name = 'email.mime.multipart'
    old_name = 'email.MIMEMultipart'


class EmailMimeNonmultipartImportFallbackFixer(ModuleImportFallbackFixerBase):
    version_info = VersionInfo(apply_since='2.3', apply_until='2.7',
        works_until='3.7')
    new_name = 'email.mime.nonmultipart'
    old_name = 'email.MIMENonMultipart'


class EmailMimeTextImportFallbackFixer(ModuleImportFallbackFixerBase):
    version_info = VersionInfo(apply_since='2.3', apply_until='2.7',
        works_until='3.7')
    new_name = 'email.mime.text'
    old_name = 'email.MIMEText'


class TkinterImportFallbackFixer(ModuleImportFallbackFixerBase):
    version_info = VersionInfo(apply_since='2.3', apply_until='2.7',
        works_until='3.7')
    new_name = 'tkinter'
    old_name = 'Tkinter'


class TkinterDialogImportFallbackFixer(ModuleImportFallbackFixerBase):
    version_info = VersionInfo(apply_since='2.3', apply_until='2.7',
        works_until='3.7')
    new_name = 'tkinter.dialog'
    old_name = 'Dialog'


class TkinterScrolledTextImportFallbackFixer(ModuleImportFallbackFixerBase):
    version_info = VersionInfo(apply_since='2.3', apply_until='2.7',
        works_until='3.7')
    new_name = 'tkinter.scrolledtext'
    old_name = 'ScrolledText'


class TkinterTixImportFallbackFixer(ModuleImportFallbackFixerBase):
    version_info = VersionInfo(apply_since='2.3', apply_until='2.7',
        works_until='3.7')
    new_name = 'tkinter.tix'
    old_name = 'Tix'


class TkinterTtkImportFallbackFixer(ModuleImportFallbackFixerBase):
    version_info = VersionInfo(apply_since='2.3', apply_until='2.7',
        works_until='3.7')
    new_name = 'tkinter.ttk'
    old_name = 'ttk'


class TkinterConstantsImportFallbackFixer(ModuleImportFallbackFixerBase):
    version_info = VersionInfo(apply_since='2.3', apply_until='2.7',
        works_until='3.7')
    new_name = 'tkinter.constants'
    old_name = 'Tkconstants'


class TkinterDndImportFallbackFixer(ModuleImportFallbackFixerBase):
    version_info = VersionInfo(apply_since='2.3', apply_until='2.7',
        works_until='3.7')
    new_name = 'tkinter.dnd'
    old_name = 'Tkdnd'


class TkinterColorchooserImportFallbackFixer(ModuleImportFallbackFixerBase):
    version_info = VersionInfo(apply_since='2.3', apply_until='2.7',
        works_until='3.7')
    new_name = 'tkinter.colorchooser'
    old_name = 'tkColorChooser'


class TkinterCommonDialogImportFallbackFixer(ModuleImportFallbackFixerBase):
    version_info = VersionInfo(apply_since='2.3', apply_until='2.7',
        works_until='3.7')
    new_name = 'tkinter.commondialog'
    old_name = 'tkCommonDialog'


class TkinterFontImportFallbackFixer(ModuleImportFallbackFixerBase):
    version_info = VersionInfo(apply_since='2.3', apply_until='2.7',
        works_until='3.7')
    new_name = 'tkinter.font'
    old_name = 'tkFont'


class TkinterMessageboxImportFallbackFixer(ModuleImportFallbackFixerBase):
    version_info = VersionInfo(apply_since='2.3', apply_until='2.7',
        works_until='3.7')
    new_name = 'tkinter.messagebox'
    old_name = 'tkMessageBox'


class BuiltinsRenameFixerBase(FixerBase):
    new_name = None
    old_name = None

    def __call__(self, cfg, tree):
        for node in ast.walk(tree):
            is_access_to_builtin = isinstance(node, ast.Name) and isinstance(
                node.ctx, ast.Load) and node.id == self.new_name
            if is_access_to_builtin:
                self.required_imports.add(common.ImportDecl('builtins',
                    None, '__builtin__'))
                builtin_renmae_decl_str = (
                    """
                {0} = getattr(builtins, '{1}', {2})
                """
                    .format(self.new_name, self.old_name, self.new_name))
                self.module_declarations.add(builtin_renmae_decl_str.strip())
        return tree


class XrangeToRangeFixer(BuiltinsRenameFixerBase):
    version_info = VersionInfo(apply_since='1.0', apply_until='2.7',
        works_until='3.7')
    new_name = 'range'
    old_name = 'xrange'


class UnicodeToStrFixer(BuiltinsRenameFixerBase):
    version_info = VersionInfo(apply_since='1.0', apply_until='2.7',
        works_until='3.7')
    new_name = 'str'
    old_name = 'unicode'


class UnichrToChrFixer(BuiltinsRenameFixerBase):
    version_info = VersionInfo(apply_since='1.0', apply_until='2.7',
        works_until='3.7')
    new_name = 'chr'
    old_name = 'unichr'


class RawInputToInputFixer(BuiltinsRenameFixerBase):
    version_info = VersionInfo(apply_since='1.0', apply_until='2.7',
        works_until='3.7')
    new_name = 'input'
    old_name = 'raw_input'


class RemoveFunctionDefAnnotationsFixer(FixerBase):
    version_info = VersionInfo(apply_since='1.0', apply_until='2.7')

    def __call__(self, cfg, tree):
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                node.returns = None
                for arg in node.args.args:
                    arg.annotation = None
                for arg in node.args.kwonlyargs:
                    arg.annotation = None
                if node.args.vararg:
                    node.args.vararg.annotation = None
                if node.args.kwarg:
                    node.args.kwarg.annotation = None
        return tree


class RemoveAnnAssignFixer(TransformerFixerBase):
    version_info = VersionInfo(apply_since='1.0', apply_until='3.5')

    def visit_AnnAssign(self, node):
        tgt_node = node.target
        if not isinstance(tgt_node, (ast.Name, ast.Attribute)):
            raise common.FixerError('Unexpected Node type', tgt_node)
        value = None
        if node.value is None:
            value = ast.NameConstant(value=None)
        else:
            value = node.value
        return ast.Assign(targets=[tgt_node], value=value)


class ShortToLongFormSuperFixer(TransformerFixerBase):
    version_info = VersionInfo(apply_since='2.2', apply_until='2.7')

    def visit_ClassDef(self, node):
        for maybe_method in ast.walk(node):
            if not isinstance(maybe_method, ast.FunctionDef):
                continue
            method = maybe_method
            method_args = method.args
            if len(method_args.args) == 0:
                continue
            self_arg = method_args.args[0]
            for maybe_super_call in ast.walk(method):
                if not isinstance(maybe_super_call, ast.Call):
                    continue
                func_node = maybe_super_call.func
                if not (isinstance(func_node, ast.Name) and func_node.id ==
                    'super'):
                    continue
                super_call = maybe_super_call
                if len(super_call.args) > 0:
                    continue
                super_call.args = [ast.Name(id=node.name, ctx=ast.Load()),
                    ast.Name(id=self_arg.arg, ctx=ast.Load())]
        return node


class InlineKWOnlyArgsFixer(TransformerFixerBase):
    version_info = VersionInfo(apply_since='1.0', apply_until='3.5')

    def visit_FunctionDef(self, node):
        if not node.args.kwonlyargs:
            return node
        if node.args.kwarg:
            kw_name = node.args.kwarg.arg
        else:
            kw_name = 'kwargs'
            node.args.kwarg = ast.arg(arg=kw_name, annotation=None)
        kwonlyargs = reversed(node.args.kwonlyargs)
        kw_defaults = reversed(node.args.kw_defaults)
        for arg, default in zip(kwonlyargs, kw_defaults):
            arg_name = arg.arg
            node_value = None
            if default is None:
                node_value = ast.Subscript(value=ast.Name(id=kw_name, ctx=
                    ast.Load()), slice=ast.Index(value=ast.Str(s=arg_name)),
                    ctx=ast.Load())
            elif not isinstance(default, ImmutableValueNodes):
                msg = (
                    'Keyword only arguments must be immutable. Found: {0} for {1}'
                    .format(default, arg_name))
                raise common.FixerError(msg, node)
            else:
                node_value = ast.Call(func=ast.Attribute(value=ast.Name(id=
                    kw_name, ctx=ast.Load()), attr='get', ctx=ast.Load()),
                    args=[ast.Str(s=arg_name), default], keywords=[])
            new_node = ast.Assign(targets=[ast.Name(id=arg_name, ctx=ast.
                Store())], value=node_value)
            node.body.insert(0, new_node)
        node.args.kwonlyargs = []
        return node


if sys.version_info >= (3, 6):


    class FStringToStrFormatFixer(TransformerFixerBase):
        version_info = VersionInfo(apply_since='2.6', apply_until='3.5')

        def _formatted_value_str(self, fmt_val_node, arg_nodes):
            arg_index = len(arg_nodes)
            arg_nodes.append(fmt_val_node.value)
            format_spec_node = fmt_val_node.format_spec
            if format_spec_node is None:
                format_spec = ''
            elif not isinstance(format_spec_node, ast.JoinedStr):
                raise common.FixerError('Unexpected Node Type',
                    format_spec_node)
            else:
                format_spec = ':' + self._joined_str_str(format_spec_node,
                    arg_nodes)
            return '{' + str(arg_index) + format_spec + '}'

        def _joined_str_str(self, joined_str_node, arg_nodes):
            fmt_str = ''
            for val in joined_str_node.values:
                if isinstance(val, ast.Str):
                    fmt_str += val.s
                elif isinstance(val, ast.FormattedValue):
                    fmt_str += self._formatted_value_str(val, arg_nodes)
                else:
                    raise common.FixerError('Unexpected Node Type', val)
            return fmt_str

        def visit_JoinedStr(self, node):
            arg_nodes = []
            fmt_str = self._joined_str_str(node, arg_nodes)
            format_attr_node = ast.Attribute(value=ast.Str(s=fmt_str), attr
                ='format', ctx=ast.Load())
            return ast.Call(func=format_attr_node, args=arg_nodes, keywords=[])


class NewStyleClassesFixer(TransformerFixerBase):
    version_info = VersionInfo(apply_since='2.0', apply_until='2.7')

    def visit_ClassDef(self, node):
        self.generic_visit(node)
        if len(node.bases) == 0:
            node.bases.append(ast.Name(id='object', ctx=ast.Load()))
        return node


class ItertoolsBuiltinsFixer(TransformerFixerBase):
    version_info = VersionInfo(apply_since='2.3', apply_until='2.7',
        works_until='3.7')

    def __call__(self, cfg, tree):
        return self.visit(tree)

    def visit_Name(self, node):
        if isinstance(node.ctx, ast.Load) and node.id in ('map', 'zip',
            'filter'):
            self.required_imports.add(common.ImportDecl('itertools', None,
                None))
            global_decl = "{0} = getattr(itertools, 'i{1}', {2})".format(node
                .id, node.id, node.id)
            self.module_declarations.add(global_decl)
        return node


def is_dict_call(node):
    return isinstance(node, ast.Call) and isinstance(node.func, ast.Name
        ) and node.func.id == 'dict'


class UnpackingGeneralizationsFixer(FixerBase):
    version_info = VersionInfo(apply_since='2.0', apply_until='3.4')

    def _has_stararg_g12n(self, node):
        if isinstance(node, ast.Call):
            elts = node.args
        elif isinstance(node, (ast.List, ast.Tuple, ast.Set)):
            elts = node.elts
        else:
            raise TypeError('Unexpected node: {0}'.format(node))
        has_starred_arg = False
        for arg in elts:
            if has_starred_arg:
                return True
            has_starred_arg = isinstance(arg, ast.Starred)
        return False

    def _has_starstarargs_g12n(self, node):
        if isinstance(node, ast.Call):
            has_kwstarred_arg = False
            for kw in node.keywords:
                if has_kwstarred_arg:
                    return True
                has_kwstarred_arg = kw.arg is None
            return False
        elif isinstance(node, ast.Dict):
            has_kwstarred_arg = False
            for key in node.keys:
                if has_kwstarred_arg:
                    return True
                has_kwstarred_arg = key is None
            return False
        else:
            raise TypeError('Unexpected node: {0}'.format(node))

    def _node_with_elts(self, node, new_elts):
        if isinstance(node, ast.Call):
            node.args = new_elts
            return node
        elif isinstance(node, ast.List):
            return ast.List(elts=new_elts)
        elif isinstance(node, ast.Set):
            return ast.Set(elts=new_elts)
        elif isinstance(node, ast.Tuple):
            return ast.Tuple(elts=new_elts)
        else:
            raise TypeError('Unexpected node type {0}'.format(type(node)))

    def _node_with_binop(self, node, binop):
        if isinstance(node, ast.Call):
            node.args = [ast.Starred(value=binop, ctx=ast.Load())]
            return node
        elif isinstance(node, ast.List):
            return binop
        elif isinstance(node, ast.Set):
            return ast.Call(func=ast.Name(id='set', ctx=ast.Load()), args=[
                binop], keywords=[])
        elif isinstance(node, ast.Tuple):
            return ast.Call(func=ast.Name(id='tuple', ctx=ast.Load()), args
                =[binop], keywords=[])
        else:
            raise TypeError('Unexpected node type {0}'.format(type(node)))

    def expand_stararg_g12n(self, node, parent, field_name):
        """Convert fn(*x, *[1, 2], z) -> fn(*(list(x) + [1, 2, z])).

        NOTE (mb 2018-07-06): The goal here is to create an expression
          which is a list, by either creating
            1. a single list node
            2. a BinOp tree where all of the node.elts/args
                are converted to lists and concatenated.
        """
        if isinstance(node, ast.Call):
            elts = node.args
        elif isinstance(node, ContainerNodes):
            elts = node.elts
        else:
            raise TypeError('Unexpected node: {0}'.format(node))
        operands = [ast.List(elts=[])]
        for elt in elts:
            tail_list = operands[-1]
            assert isinstance(tail_list, ast.List)
            tail_elts = tail_list.elts
            if not isinstance(elt, ast.Starred):
                tail_elts.append(elt)
                continue
            val = elt.value
            if isinstance(val, ContainerNodes):
                tail_elts.extend(val.elts)
                continue
            new_val_node = ast.Call(func=ast.Name(id='list', ctx=ast.Load()
                ), args=[val], keywords=[])
            if len(tail_elts) == 0:
                operands[-1] = new_val_node
            else:
                operands.append(new_val_node)
            operands.append(ast.List(elts=[]))
        tail_list = operands[-1]
        assert isinstance(tail_list, ast.List)
        if len(tail_list.elts) == 0:
            operands = operands[:-1]
        if len(operands) == 1:
            tail_list = operands[0]
            assert isinstance(tail_list, ast.List)
            return self._node_with_elts(node, tail_list.elts)
        if len(operands) > 1:
            binop = ast.BinOp(left=operands[0], op=ast.Add(), right=operands[1]
                )
            for operand in operands[2:]:
                binop = ast.BinOp(left=binop, op=ast.Add(), right=operand)
            return self._node_with_binop(node, binop)
        raise RuntimeError('This should not happen')

    def expand_starstararg_g12n(self, node, parent, field_name):
        chain_values = []
        chain_val = None
        if isinstance(node, ast.Dict):
            for key, val in zip(node.keys, node.values):
                if key is None:
                    chain_val = val
                else:
                    chain_val = ast.Dict(keys=[key], values=[val])
                chain_values.append(chain_val)
        elif isinstance(node, ast.Call):
            for kw in node.keywords:
                if kw.arg is None:
                    chain_val = kw.value
                else:
                    chain_val = ast.Dict(keys=[ast.Str(s=kw.arg)], values=[
                        kw.value])
                chain_values.append(chain_val)
        else:
            raise TypeError('Unexpected node type {0}'.format(node))
        collapsed_chain_values = []
        for chain_val in chain_values:
            if len(collapsed_chain_values) == 0:
                collapsed_chain_values.append(chain_val)
            else:
                prev_chain_val = collapsed_chain_values[-1]
                if isinstance(chain_val, ast.Dict) and isinstance(
                    prev_chain_val, ast.Dict):
                    for key, val in zip(chain_val.keys, chain_val.values):
                        prev_chain_val.keys.append(key)
                        prev_chain_val.values.append(val)
                else:
                    collapsed_chain_values.append(chain_val)
        assert len(collapsed_chain_values) > 0
        if len(collapsed_chain_values) == 1:
            collapsed_chain_value = collapsed_chain_values[0]
            if isinstance(node, ast.Dict):
                return collapsed_chain_value
            elif isinstance(node, ast.Call):
                node_func = node.func
                node_args = node.args
                if isinstance(node_func, ast.Name) and node_func.id == 'dict':
                    return collapsed_chain_value
                else:
                    return ast.Call(func=node_func, args=node_args,
                        keywords=[ast.keyword(arg=None, value=
                        collapsed_chain_value)])
            else:
                raise TypeError('Unexpected node type {0}'.format(node))
        else:
            assert isinstance(node, ast.Call)
            self.required_imports.add(common.ImportDecl('itertools', None,
                None))
            chain_args = []
            for val in chain_values:
                items_func = ast.Attribute(value=val, attr='items', ctx=ast
                    .Load())
                chain_args.append(ast.Call(func=items_func, args=[],
                    keywords=[]))
            value_node = ast.Call(func=ast.Name(id='dict', ctx=ast.Load()),
                args=[ast.Call(func=ast.Attribute(value=ast.Name(id=
                'itertools', ctx=ast.Load()), attr='chain', ctx=ast.Load()),
                args=chain_args, keywords=[])], keywords=[])
            node.keywords = [ast.keyword(arg=None, value=value_node)]
        return node

    def visit_expr(self, node, parent, field_name):
        new_node = node
        if isinstance(node, ArgUnpackNodes) and self._has_stararg_g12n(node):
            new_node = self.expand_stararg_g12n(new_node, parent, field_name)
        if isinstance(node, KwArgUnpackNodes) and self._has_starstarargs_g12n(
            node):
            new_node = self.expand_starstararg_g12n(new_node, parent,
                field_name)
        return new_node

    def is_stmtlist(self, nodelist):
        return isinstance(nodelist, list) and all(isinstance(n, ast.stmt) for
            n in nodelist)

    def walk_stmtlist(self, stmtlist, parent, field_name):
        assert self.is_stmtlist(stmtlist)
        new_stmts = []
        for stmt in stmtlist:
            new_stmt = self.walk_stmt(stmt, parent, field_name)
            new_stmts.append(new_stmt)
        return new_stmts

    def walk_expr(self, node, parent, parent_field_name):
        new_node_expr = self.walk_node(node, parent, parent_field_name)
        assert isinstance(new_node_expr, ast.expr)
        return new_node_expr

    def iter_walkable_fields(self, node):
        for field_name, field_node in ast.iter_fields(node):
            if isinstance(field_node, ast.arguments):
                continue
            if isinstance(field_node, ast.expr_context):
                continue
            if isinstance(field_node, LeafNodes):
                continue
            yield field_name, field_node

    def walk_node(self, node, parent, parent_field_name):
        if isinstance(node, LeafNodes):
            return node
        for field_name, field_node in self.iter_walkable_fields(node):
            if isinstance(field_node, ast.AST):
                new_node = self.walk_node(field_node, node, field_name)
                setattr(node, field_name, new_node)
            elif isinstance(field_node, list):
                new_field_node = []
                new_sub_node = None
                for sub_node in field_node:
                    if isinstance(sub_node, LeafNodes):
                        new_sub_node = sub_node
                    elif isinstance(sub_node, ast.AST):
                        new_sub_node = self.walk_node(sub_node, node,
                            field_name)
                    else:
                        new_sub_node = sub_node
                    new_field_node.append(new_sub_node)
                setattr(node, field_name, new_field_node)
        if not isinstance(node, ast.expr):
            return node
        new_expr_node = self.visit_expr(node, parent, parent_field_name)
        if isinstance(new_expr_node, ast.Call):
            is_single_dict_splat = is_dict_call(new_expr_node) and len(
                new_expr_node.args) == 0 and len(new_expr_node.keywords
                ) == 1 and new_expr_node.keywords[0].arg is None
            if is_single_dict_splat:
                keyword_node = new_expr_node.keywords[0]
                if is_dict_call(keyword_node.value) or isinstance(keyword_node
                    .value, ast.Dict):
                    return keyword_node.value
        return new_expr_node

    def walk_stmt(self, node, parent, field_name):
        assert not self.is_stmtlist(node)
        for field_name, field_node in self.iter_walkable_fields(node):
            if self.is_stmtlist(field_node):
                old_field_nodelist = field_node
                new_field_nodelist = self.walk_stmtlist(old_field_nodelist,
                    parent=node, field_name=field_name)
                setattr(node, field_name, new_field_nodelist)
            elif isinstance(field_node, ast.stmt):
                new_stmt = self.walk_stmt(field_node, node, field_name)
                setattr(node, field_name, new_stmt)
            elif isinstance(field_node, ast.AST):
                new_node = self.walk_node(field_node, node, field_name)
                setattr(node, field_name, new_node)
            elif isinstance(field_node, list):
                new_field_node = []
                new_sub_node = None
                for sub_node in field_node:
                    if isinstance(sub_node, LeafNodes):
                        new_sub_node = sub_node
                    elif isinstance(sub_node, ast.AST):
                        new_sub_node = self.walk_node(sub_node, node,
                            field_name)
                    else:
                        new_sub_node = sub_node
                    new_field_node.append(new_sub_node)
                setattr(node, field_name, new_field_node)
            else:
                continue
        return node

    def __call__(self, cfg, tree):
        tree.body = self.walk_stmtlist(tree.body, tree, 'body')
        return tree


class NamedTupleClassToAssignFixer(TransformerFixerBase):
    version_info = VersionInfo(apply_since='2.6', apply_until='3.4')
    _typing_module_name = None
    _namedtuple_class_name = None

    def __init__(self):
        self._typing_module_name = None
        self._namedtuple_class_name = None
        super(NamedTupleClassToAssignFixer, self).__init__()

    def visit_ImportFrom(self, node):
        if node.module == 'typing':
            for alias in node.names:
                if alias.name == 'NamedTuple':
                    if alias.asname is None:
                        self._namedtuple_class_name = alias.name
                    else:
                        self._namedtuple_class_name = alias.asname
        return node

    def visit_Import(self, node):
        for alias in node.names:
            if alias.name == 'typing':
                if alias.asname is None:
                    self._typing_module_name = alias.name
                else:
                    self._typing_module_name = alias.asname
        return node

    def visit_ClassDef(self, node):
        self.generic_visit(node)
        if len(node.bases) == 0:
            return node
        if not (self._typing_module_name or self._namedtuple_class_name):
            return node
        has_namedtuple_base = utils.has_base_class(node, self.
            _typing_module_name, self._namedtuple_class_name or 'NamedTuple')
        if not has_namedtuple_base:
            return node
        func = None
        if self._typing_module_name:
            func = ast.Attribute(value=ast.Name(id=self._typing_module_name,
                ctx=ast.Load()), attr='NamedTuple', ctx=ast.Load())
        elif self._namedtuple_class_name:
            func = ast.Name(id=self._namedtuple_class_name, ctx=ast.Load())
        else:
            raise RuntimeError('')
        elts = []
        for assign in node.body:
            if not isinstance(assign, ast.AnnAssign):
                continue
            tgt = assign.target
            if not isinstance(tgt, ast.Name):
                continue
            elts.append(ast.Tuple(elts=[ast.Str(s=tgt.id), assign.
                annotation], ctx=ast.Load()))
        return ast.Assign(targets=[ast.Name(id=node.name, ctx=ast.Store())],
            value=ast.Call(func=func, args=[ast.Str(s=node.name), ast.List(
            elts=elts, ctx=ast.Load())], keywords=[]))
