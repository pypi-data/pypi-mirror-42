# -*- coding: utf-8 -*-
"""Originals Authors http://sourceforge.net/projects/pyxml/
Under Python License (CNRI Python License)
Patched by Nicolas Delaby nicolas@nexedi.com to support namespaces
"""

# Generic class for marshalling simple Python data types into an XML-based
# format.  The interface is the same as the built-in module of the
# same name, with four functions:
#   dump(value, file), load(file)
#   dumps(value), loads(string)
from functools import cmp_to_key
from six import reraise
import sys
from xml.sax import make_parser
from xml.sax.saxutils import escape, unescape
from lxml.sax import ElementTreeContentHandler, saxify
from lxml import etree
from lxml.builder import ElementMaker
from io import BytesIO

# Basic marshaller class, customizable by overriding it and
# changing various attributes and methods.
# It's also used as a SAX handler, which may be a good idea but may
# also be a stupid hack.
MARSHAL_PREFIX = 'marshal'

try:
  cmp
except NameError:
  cmp = lambda x, y: (x > y) - (x < y)
  def unicode2str(s):
    return s
else:
  def unicode2str(s):
    return s.encode('utf-8')

@cmp_to_key
def version_independent_cmp(a, b):
  a = a[0]
  b = b[0]
  try:
    return cmp(a, b)
  except TypeError:
    return cmp(repr(a), repr(b))

class Marshaller(object):

  # Names of elements.  These are specified as class attributes
  # because simple things like integers are often handled in the
  # same way, and only the element names change.
  def __init__(self, prefix=MARSHAL_PREFIX, namespace_uri=None, as_tree=False):
    self.as_tree = as_tree
    if namespace_uri:
      nsmap = {prefix: namespace_uri}
    else:
      nsmap = {}
    E = ElementMaker(namespace=namespace_uri, nsmap=nsmap)
    self.tag_root = E.marshal
    self.tag_int = E.int
    self.tag_float = E.float
    self.tag_long = E.long
    self.tag_string = E.string
    self.tag_unicode = E.unicode
    self.tag_tuple = E.tuple
    self.tag_list = E.list
    self.tag_dictionary = E.dictionary
    self.tag_complex = E.complex
    self.tag_reference = E.reference
    self.tag_code = E.code
    self.tag_none = E.none
    self.tag_instance = E.object
    self.tag_set = E.set
    self.tag_bool = E.bool

  # The four basic functions that form the caller's interface
  def dump(self, value, file):
    "Write the value on the open file"
    kw = {'id': 1}
    xml_tree = self.m_root(value, kw)

    # XXX should this just loop through the L and call file.write
    # for each item?
    file.write(etree.tostring(xml_tree))

  def dumps(self, value):
    "Marshal value, returning the resulting string"
    kw = {'id': 1}
    # now uses m_root for proper root element handling
    xml_tree = self.m_root(value, kw)
    if self.as_tree:
      return xml_tree
    else:
      return etree.tostring(xml_tree)

  # IMPORTANT NOTE: The proper entry point to marshal
  # an object is m_root; the public marshalling
  # methods dump and dumps use m_root().
  #
  # This function gets the name of the
  # type of the object being marshalled, and calls the
  # m_<typename> method.  This method must return a list of strings,
  # which will be returned to the caller.
  #
  # (This function can be called recursively, so it shouldn't
  # return just a single.  The top-level caller will perform a
  # single string.join to get the resulting XML document.
  #
  # dict is a dictionary whose keys are used to store the IDs of
  # objects that have already been marshalled, in order to allow
  # writing a reference to them.
  #
  # XXX there should be some way to disable the automatic generation of
  # references to already-marshalled objects

  def _marshal(self, value, kw):
    t = type(value)
    i = str(id(value))
    if i in kw:
      return self.m_reference(value, kw)
    else:
      method_id =  'm_%s' % (type(value).__name__,)
      callable_method = getattr(self, method_id, None)
      if callable_method is not None:
        return callable_method(value, kw)
      elif object in value.__class__.mro():
        #Fallback to instance for new style Classes 
        #http://www.pdb.org/doc/newstyle/
        return self.m_instance(value, kw)
      else:
        return self.m_unimplemented(value, kw)

  # Utility function, used for types that aren't implemented
  def m_unimplemented(self, value, kw):
    raise ValueError("Marshalling of object %r unimplemented or not supported in this DTD" % value)

  # The real entry point for marshalling, to handle properly
  # and cleanly any root tag or tags necessary for the marshalled
  # output.
  def m_root(self, value, kw):
    return self.tag_root(self._marshal(value, kw))

  #
  # All the generic marshalling functions for various Python types
  #
  def m_reference(self, value, kw):
    # This object has already been marshalled, so
    # emit a reference element.
    i = kw[str(id(value))]
    return self.tag_reference(id='i%s' % i)

  def m_string(self, value, kw):
    return self.tag_string(escape(value))

  # Since Python 2.2, the string type has a name of 'str'
  # To avoid having to rewrite all classes that implement m_string
  # we delegate m_str to m_string.
  def m_str(self, value, kw):
    return self.m_string(value, kw)
  
  def m_bytes(self, value, kw):
    return self.m_string(value.decode('utf-8'), kw)

  if str is bytes:
    m_unicode = m_str
    m_str = m_bytes

  def m_int(self, value, kw):
    return (self.tag_int if -1e24 < value < 1e24 else
            self.tag_long)(str(value))

  m_long = m_int

  def m_float(self, value, kw):
    return self.tag_float(str(value))

  def m_tuple(self, value, kw):
    xml_tree = self.tag_tuple()
    for elem in value:
      xml_tree.append(self._marshal(elem, kw))
    return xml_tree

  def m_list(self, value, kw):
    kw['id'] += 1
    i = str(kw['id'])
    kw[str(id(value))] = i
    kw[i] = value
    xml_tree = self.tag_list(id='i%s' % i)
    for elem in value:
      xml_tree.append(self._marshal(elem, kw))
    return xml_tree

  def m_dictionary(self, value, kw):
    kw['id'] += 1
    i = str(kw['id'])
    kw[str(id(value))] = i
    kw[i] = value
    xml_tree = self.tag_dictionary(id='i%s' % i)
    # Sort the items to allow reproducable results across Python
    # versions
    for key, v in sorted(value.items(),
                         key=version_independent_cmp):
      xml_tree.append(self._marshal(key, kw))
      xml_tree.append(self._marshal(v, kw))
    return xml_tree

  def m_set(self, value, kw):
    kw['id'] += 1
    i = str(kw['id'])
    kw[str(id(value))] = i
    kw[i] = value
    xml_tree = self.tag_set(id='i%s' % i)
    for elem in value:
      xml_tree.append(self._marshal(elem, kw))
    return xml_tree

  def m_bool(self, value, kw):
    return self.tag_bool(value and '1' or '0')

  # Python 2.2 renames dictionary to dict.
  def m_dict(self, value, kw):
    return self.m_dictionary(value, kw)

  def m_None(self, value, kw):
    return self.tag_none()

  # Python 2.2 renamed the type of None to NoneTye
  def m_NoneType(self, value, kw):
    return self.m_None(value, kw)

  def m_complex(self, value, kw):
    return self.tag_complex('%s %s' % (value.real, value.imag))

  def m_code(self, value, kw):
    # The full information about code objects is only available
    # from the C level, so we'll use the built-in marshal module
    # to convert the code object into a string, and include it in
    # the HTML.
    import marshal, base64
    encoded_value = base64.encodestring(marshal.dumps(value))
    return self.tag_code(encoded_value)

  def m_instance(self, value, kw):
    kw['id'] += 1
    i = str(kw['id'])
    kw[str(id(value))] = i
    kw[i] = value
    cls = value.__class__
    xml_tree = self.tag_instance(id='i%s' % i, module=cls.__module__)
    xml_tree.attrib.update({'class': cls.__name__})

    # Check for pickle's __getinitargs__
    if hasattr(value, '__getinitargs__'):
      args = value.__getinitargs__()
      len(args) # XXX Assert it's a sequence
    else:
      args = ()

    xml_tree.append(self._marshal(args, kw))

    # Check for pickle's __getstate__ function
    try:
      getstate = value.__getstate__
    except AttributeError:
      stuff = value.__dict__
    else:
      stuff = getstate()
    xml_tree.append(self._marshal(stuff, kw))
    return xml_tree

# These values are used as markers in the stack when unmarshalling
# one of the structures below.  When a <tuple> tag is encountered, for
# example, the TUPLE object is pushed onto the stack, and further
# objects are processed.  When the </tuple> tag is found, the code
# looks back into the stack until TUPLE is found; all the higher
# objects are then collected into a tuple.  Ditto for lists...

TUPLE = {}
LIST = {}
DICT = {}
SET = {}

class Unmarshaller(ElementTreeContentHandler):
  # This dictionary maps element names to the names of starting and ending
  # functions to call when unmarshalling them.  My convention is to
  # name them um_start_foo and um_end_foo, but do whatever you like.

  unmarshal_meth = {
      'marshal': ('um_start_root', None),
      'int': ('um_start_int', 'um_end_int'),
      'float': ('um_start_float', 'um_end_float'),
      'long': ('um_start_long', 'um_end_long'),
      'string': ('um_start_string', 'um_end_string'),
      'tuple': ('um_start_tuple', 'um_end_tuple'),
      'list': ('um_start_list', 'um_end_list'),
      'dictionary': ('um_start_dictionary', 'um_end_dictionary'),
      'complex': ('um_start_complex', 'um_end_complex'),
      'reference': ('um_start_reference', None),
      'code': ('um_start_code', 'um_end_code'),
      'none': ('um_start_none', 'um_end_none'),
      'object': ('um_start_instance', 'um_end_instance'),
      'set': ('um_start_set', 'um_end_set'),
      'bool': ('um_start_bool', 'um_end_bool'),
      }
  unmarshal_meth['unicode'] = unmarshal_meth['string'] # BBB

  def __init__(self):
    # Find the named methods, and convert them to the actual
    # method object.

    d = {}
    for key, (sm, em) in self.unmarshal_meth.items():
      if sm is not None:
        sm = getattr(self, sm)
      if em is not None:
        em = getattr(self, em)
      d[key] = sm, em
    self.unmarshal_meth = d
    self._clear()
    ElementTreeContentHandler.__init__(self)

  def _clear(self):
    """
    Protected method to (re)initialize the object into
    a steady state. Performed by __init__ and _load.
    """
    self.data_stack = []
    self.kw = {}
    self.accumulating_chars = 0

  def load(self, file_object):
    "Unmarshal one value, reading it from a file-like object"
    # Instantiate a new object; unmarshalling isn't thread-safe
    # because it modifies attributes on the object.
    m = self.__class__()
    return m._load(file_object)

  def load_tree(self, tree):
    """Unmarshal element_tree object and return 
    python object.
    """
    parser = make_parser()
    parser.setFeature('http://xml.org/sax/features/namespaces', True)
    parser.setContentHandler(self)
    saxify(tree, self)
    result = self.data_stack[0]
    self._clear()
    return result

  def loads(self, string):
    "Unmarshal one value from a string"
    # Instantiate a new object; unmarshalling isn't thread-safe
    # because it modifies attributes on the object.
    m = self.__class__()
    return m._load(BytesIO(string))

  # Basic unmarshalling routine; it creates a SAX XML parser,
  # registers self as the SAX handler, parses it, and returns
  # the only thing on the data stack.

  def _load(self, file_object):
    "Read one value from the open file"
    parser = make_parser()
    parser.setFeature('http://xml.org/sax/features/namespaces', True)
    parser.setContentHandler(self)
    parser.parse(file_object)
    assert len(self.data_stack) == 1
    # leave the instance in a steady state
    result = self.data_stack[0]
    self._clear()
    return result

  # find_class() is copied from pickle.py
  def find_class(self, module, name):
    try:
      module = __import__(module, globals(), locals(), [''])
    except ImportError:
      module = __import__(module, {}, locals(), [''])
    return getattr(module, name)


  # SAXlib handler methods.
  #
  # Unmarshalling is done by creating a stack (a Python list) on
  # starting the root element.  When the .character() method may be
  # called, the last item on the stack must be a list; the
  # characters will be appended to that list.
  #
  # The starting methods must, at minimum, push a single list onto
  # the stack, as um_start_generic does.
  #
  # The ending methods can then do string.join() on the list on the
  # top of the stack, and convert it to whatever Python type is
  # required.  The resulting Python object then replaces the list on
  # the top of the stack.
  #

  def startElement(self, name, attrs):
    # Call the start unmarshalling method, if specified
    sm, em = self.unmarshal_meth[name]
    if sm is not None:
      return sm(name, attrs)

  def startElementNS(self, ns_name, name, attrs):
    # Call the start unmarshalling method, if specified
    ns_uri, local_name = ns_name
    sm, em = self.unmarshal_meth[local_name]
    if sm is not None:
      attrib = {k[1]: v for k, v in attrs.items()}
      return sm(local_name, attrib)

  def characters(self, data):
    if self.accumulating_chars:
      self.data_stack[-1].append(data)

  def endElement(self, name):
    # Call the ending method
    sm, em = self.unmarshal_meth[name]
    if em is not None:
      em(name)

  def endElementNS(self, ns_name, name):
    # Call the ending method
    ns_uri, local_name = ns_name
    sm, em = self.unmarshal_meth[local_name]
    if em is not None:
      em(local_name)

  # um_start_root is really a "sentinel" method
  # which ensures that the unmarshaller is in a steady,
  # "empty" state.
  def um_start_root(self, name, attrs):
    if self.kw or self.data_stack:
      raise ValueError("root element %r found elsewhere than root"
            % name)

  def um_start_reference(self, name, attrs):
    self.data_stack.append(self.kw[attrs['id']])

  def um_start_generic(self, name, attrs):
    self.data_stack.append([])
    self.accumulating_chars = 1

  um_start_float = um_start_long = um_start_string = um_start_generic
  um_start_complex = um_start_code = um_start_none = um_start_generic
  um_start_int = um_start_generic
  um_start_bool = um_start_generic

  def um_end_string(self, name):
    ds = self.data_stack
    ds[-1] = unicode2str(unescape(''.join(ds[-1])))
    self.accumulating_chars = 0

  def um_end_int(self, name):
    ds = self.data_stack
    ds[-1] = ''.join(ds[-1])
    ds[-1] = int(ds[-1])
    self.accumulating_chars = 0

  def um_end_long(self, name):
    ds = self.data_stack
    ds[-1] = ''.join(ds[-1])
    ds[-1] = int(ds[-1])
    self.accumulating_chars = 0

  def um_end_float(self, name):
    ds = self.data_stack
    ds[-1] = ''.join(ds[-1])
    ds[-1] = float(ds[-1])
    self.accumulating_chars = 0

  def um_end_none(self, name):
    ds = self.data_stack
    ds[-1] = None
    self.accumulating_chars = 0

  def um_end_complex(self, name):
    ds = self.data_stack
    c = ''.join(ds[-1])
    c = c.split()
    c = float(c[0]) + float(c[1])*1j
    ds[-1:] = [c]
    self.accumulating_chars = 0

  def um_end_code(self, name):
    import marshal, base64
    ds = self.data_stack
    s = ''.join(ds[-1])
    s = base64.decodestring(s)
    ds[-1] = marshal.loads(s)
    self.accumulating_chars = 0

  # Trickier stuff: dictionaries, lists, tuples.
  def um_start_list(self, name, attrs):
    self.data_stack.append(LIST)
    L = []
    if 'id' in attrs:
      self.kw[attrs['id']] = L
    self.data_stack.append(L)

  def um_start_set(self, name, attrs):
    self.data_stack.append(SET)
    S = set()
    if 'id' in attrs:
      id = attrs['id']
      self.kw[id] = S
    self.data_stack.append(S)

  def um_end_bool(self, name):
    ds = self.data_stack
    ds[-1] = bool(int(''.join(ds[-1])))
    self.accumulating_chars = 0

  def um_end_list(self, name):
    ds = self.data_stack
    for index in range(len(ds)-1, -1, -1):
      if ds[index] is LIST:
        break
    assert index != -1
    L = ds[index + 1]
    L[:] = ds[index + 2:len(ds)]
    ds[index:] = [L]

  def um_end_set(self, name):
    ds = self.data_stack
    for index in range(len(ds)-1, -1, -1):
      if ds[index] is SET:
        break
    assert index != -1
    S = ds[index + 1]
    [S.add(item) for item in ds[index + 2:len(ds)]]
    ds[index:] = [S]

  def um_start_tuple(self, name, attrs):
    self.data_stack.append(TUPLE)

  def um_end_tuple(self, name):
    ds = self.data_stack
    for index in range(len(ds) - 1, -1, -1):
      if ds[index] is TUPLE:
        break
    assert index != -1
    t = tuple(ds[index+1:len(ds)])
    ds[index:] = [t]

  # Dictionary elements, in the generic format, must always have an
  # even number of objects contained inside them.  These objects are
  # treated as alternating keys and values.
  def um_start_dictionary(self, name, attrs):
    self.data_stack.append(DICT)
    d = {}
    if 'id' in attrs:
      self.kw[attrs['id']] = d
    self.data_stack.append(d)

  def um_end_dictionary(self, name):
    ds = self.data_stack
    for index in range(len(ds) - 1, -1, -1):
      if ds[index] is DICT:
        break
    assert index != -1
    d = ds[index + 1]
    for i in range(index + 2, len(ds), 2):
      key = ds[i]
      value = ds[i+1]
      d[key] = value
    ds[index:] = [d]

  def um_start_instance(self, name, attrs):
    module = attrs['module']
    classname = attrs['class']
    value = _EmptyClass()
    if 'id' in attrs:
      self.kw[attrs['id']] = value
    self.data_stack.append(value)
    self.data_stack.append(module)
    self.data_stack.append(classname)

  def um_end_instance(self, name):
    value, module, classname, initargs, kw = self.data_stack[-5:]
    klass = self.find_class(module, classname)
    if (not initargs and isinstance(klass, type) and
      not hasattr(klass, '__getinitargs__')):
      value = klass()
    else:
      try:
        value = klass(*initargs)
      except TypeError as err:
        reraise(TypeError, TypeError('in constructor for %s: %s' % (
            klass.__name__, err)), sys.exc_info()[2])

    # Now set the object's attributes from the marshalled dictionary
    for x in kw.items():
      setattr(value, *x)
    self.data_stack[-5:] = [value]

# Helper class for instance unmarshalling
class _EmptyClass:
  pass

# module functions for procedural use of module
_m = Marshaller()
_m_ns = Marshaller(namespace_uri='http://www.erp5.org/namespaces/marshaller')
dump = _m.dump
dumps = _m.dumps
dump_ns = _m_ns.dump
dumps_ns = _m_ns.dumps
_um = Unmarshaller()
load = _um.load
loads = _um.loads
load_tree = _um.load_tree

del _m, _um, _m_ns
