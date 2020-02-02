import json
import sys
import six
from six.moves import urllib, cStringIO
import collections
import logging
from pkg_resources import resource_stream
from .utils import aslist, flatten
from . import schema
from .codegen_base import TypeDef, CodeGenBase, shortname
from typing import List, Text, Dict, Union, IO, Any

class PythonCodeGen(CodeGenBase):
    def __init__(self, out):
        # type: (IO[str]) -> None
        super(PythonCodeGen, self).__init__()
        self.out = out
        self.current_class_is_abstract = False

    def safe_name(self, n):
        # type: (Text) -> Text

        avn = schema.avro_name(n)
        if avn in ("class", "in"):
            # reserved words
            avn = avn+"_"
        return avn


    def prologue(self):
        # type: () -> None

        self.out.write("""#
# This file was autogenerated using schema-salad-tool --codegen=python
#
""")

        rs = resource_stream(__name__, 'sourceline.py')
        self.out.write(rs.read().decode("UTF-8"))
        rs.close()
        self.out.write("\n\n")

        rs = resource_stream(__name__, 'python_codegen_support.py')
        self.out.write(rs.read().decode("UTF-8"))
        rs.close()
        self.out.write("\n\n")

        for p in six.itervalues(self.prims):
            self.declare_type(p)


    def begin_class(self, classname, extends, doc, abstract):
        # type: (Text, List[Text], Text, bool) -> None

        classname = self.safe_name(classname)

        if extends:
            ext = ", ".join(self.safe_name(e) for e in extends)
        else:
            ext = "Savable"

        self.out.write("class %s(%s):\n" % (self.safe_name(classname), ext))

        if doc:
            self.out.write('    """\n')
            self.out.write(str(doc))
            self.out.write('\n    """\n')

        self.serializer = cStringIO()

        self.current_class_is_abstract = abstract
        if self.current_class_is_abstract:
            self.out.write("    pass\n\n")
            return

        self.out.write(
            """    def __init__(self, _doc, baseuri, loadingOptions, docRoot=None):
        doc = copy.copy(_doc)
        if hasattr(_doc, 'lc'):
            doc.lc.data = _doc.lc.data
            doc.lc.filename = _doc.lc.filename
        errors = []
        #doc = {expand_url(d, u"", loadingOptions, scoped_id=False, vocab_term=True): v for d,v in doc.items()}
""")

        self.serializer.write("""
    def save(self):
        r = {}
""")

    def end_class(self, classname):
        # type: (Text) -> None

        if self.current_class_is_abstract:
            return

        self.out.write("""
        if errors:
            raise ValidationException(\"Trying '%s'\\n\"+\"\\n\".join(errors))
""" % self.safe_name(classname))

        self.serializer.write("        return r\n")
        self.out.write(self.serializer.getvalue())
        self.out.write("\n\n")

    prims = {
        u"http://www.w3.org/2001/XMLSchema#string": TypeDef("strtype", "_PrimitiveLoader((str, six.text_type))"),
        u"http://www.w3.org/2001/XMLSchema#int": TypeDef("inttype", "_PrimitiveLoader(int)"),
        u"http://www.w3.org/2001/XMLSchema#long": TypeDef("inttype", "_PrimitiveLoader(int)"),
        u"http://www.w3.org/2001/XMLSchema#float": TypeDef("floattype", "_PrimitiveLoader(float)"),
        u"http://www.w3.org/2001/XMLSchema#double": TypeDef("floattype", "_PrimitiveLoader(float)"),
        u"http://www.w3.org/2001/XMLSchema#boolean": TypeDef("booltype", "_PrimitiveLoader(bool)"),
        u"https://w3id.org/cwl/salad#null": TypeDef("None_type", "_PrimitiveLoader(type(None))"),
        u"https://w3id.org/cwl/salad#Any": TypeDef("Any_type", "_AnyLoader()")
    }

    def type_loader(self, t):
        # type: (Union[List[Any], Dict[Text, Any], Text]) -> TypeDef

        if isinstance(t, list):
            sub = [self.type_loader(i) for i in t]
            return self.declare_type(TypeDef("union_of_%s" % "_or_".join(s.name for s in sub), "_UnionLoader((%s,))" % (", ".join(s.name for s in sub))))
        if isinstance(t, dict):
            if t["type"] in ("array", "https://w3id.org/cwl/salad#array"):
                i = self.type_loader(t["items"])
                return self.declare_type(TypeDef("array_of_%s" % i.name, "_ArrayLoader(%s)" % i.name))
            elif t["type"] in ("enum", "https://w3id.org/cwl/salad#enum"):
                for sym in t["symbols"]:
                    self.add_vocab(shortname(sym), sym)
                return self.declare_type(TypeDef(self.safe_name(t["name"])+"Loader", '_EnumLoader(("%s",))' % (
                    '", "'.join(self.safe_name(sym) for sym in t["symbols"]))))
            elif t["type"] in ("record", "https://w3id.org/cwl/salad#record"):
                return self.declare_type(TypeDef(self.safe_name(t["name"])+"Loader", "_RecordLoader(%s)" % self.safe_name(t["name"])))
            else:
                raise Exception("wft %s" % t["type"])
        if t in self.prims:
            return self.prims[t]
        return self.collected_types[self.safe_name(t)+"Loader"]

    def declare_id_field(self, name, fieldtype, doc):
        # type: (Text, TypeDef, Text) -> None

        if self.current_class_is_abstract:
            return

        self.declare_field(name, fieldtype, doc, True)
        self.out.write("""
        if self.{safename} is None:
            if docRoot is not None:
                self.{safename} = docRoot
            else:
                raise ValidationException("Missing {fieldname}")
        baseuri = self.{safename}
""".
                       format(safename=self.safe_name(name),
                              fieldname=shortname(name)))

    def declare_field(self, name, fieldtype, doc, optional):
        # type: (Text, TypeDef, Text, bool) -> None

        if self.current_class_is_abstract:
            return

        if optional:
            self.out.write("        if '{fieldname}' in doc:\n".format(fieldname=shortname(name)))
            spc = "    "
        else:
            spc = ""
        self.out.write("""{spc}        try:
{spc}            self.{safename} = load_field(doc.get('{fieldname}'), {fieldtype}, baseuri, loadingOptions)
{spc}        except ValidationException as e:
{spc}            errors.append(SourceLine(doc, '{fieldname}', str).makeError(\"the `{fieldname}` field is not valid because:\\n\"+str(e)))
""".
                       format(safename=self.safe_name(name),
                              fieldname=shortname(name),
                              fieldtype=fieldtype.name,
                              spc=spc))
        if optional:
            self.out.write("""        else:
            self.{safename} = None
""".format(safename=self.safe_name(name)))

        self.out.write("\n")

        self.serializer.write("        if self.%s is not None:\n            r['%s'] = save(self.%s)\n" % (self.safe_name(name), shortname(name), self.safe_name(name)))

    def uri_loader(self, inner, scoped_id, vocab_term, refScope):
        # type: (TypeDef, bool, bool, Union[int, None]) -> TypeDef
        return self.declare_type(TypeDef("uri_%s_%s_%s_%s" % (inner.name, scoped_id, vocab_term, refScope),
                                         "_URILoader(%s, %s, %s, %s)" % (inner.name, scoped_id, vocab_term, refScope)))

    def idmap_loader(self, field, inner, mapSubject, mapPredicate):
        # type: (Text, TypeDef, Text, Union[Text, None]) -> TypeDef
        return self.declare_type(TypeDef("idmap_%s_%s" % (self.safe_name(field), inner.name),
                                         "_IdMapLoader(%s, '%s', '%s')" % (inner.name, mapSubject, mapPredicate)))

    def typedsl_loader(self, inner, refScope):
        # type: (TypeDef, Union[int, None]) -> TypeDef
        return self.declare_type(TypeDef("typedsl_%s_%s" % (inner.name, refScope),
                                         "_TypeDSLLoader(%s, %s)" % (inner.name, refScope)))

    def epilogue(self, rootLoader):
        # type: (TypeDef) -> None
        self.out.write("_vocab = {\n")
        for k in sorted(self.vocab.keys()):
            self.out.write("    \"%s\": \"%s\",\n" % (k, self.vocab[k]))
        self.out.write("}\n")

        self.out.write("_rvocab = {\n")
        for k in sorted(self.vocab.keys()):
            self.out.write("    \"%s\": \"%s\",\n" % (self.vocab[k], k))
        self.out.write("}\n\n")

        for k,tv in six.iteritems(self.collected_types):
            self.out.write("%s = %s\n" % (tv.name, tv.init))
        self.out.write("\n\n")

        self.out.write("""
def load_document(doc, baseuri=None, loadingOptions=None):
    if baseuri is None:
        baseuri = file_uri(os.getcwd()) + "/"
    if loadingOptions is None:
        loadingOptions = LoadingOptions()
    return _document_load(%s, doc, baseuri, loadingOptions)
""" % rootLoader.name)
