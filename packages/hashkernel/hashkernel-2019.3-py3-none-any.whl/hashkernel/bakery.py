#!/usr/bin/env python
# -*- coding: utf-8 -*-

import abc

import threading
from datetime import datetime

from hashkernel import (
    Stringable, EnsureIt, utf8_encode, Jsonable, ensure_string,
    CodeEnum)
from hashkernel.event import Event
from io import BytesIO
import os
from hashkernel.base_x import base_x
import json
import enum
from pathlib import PurePosixPath
from typing import (
    Union, Optional, Any, Callable, Tuple, List, Iterable, Dict, IO)
import logging
from hashkernel.file_types import (
    guess_name, file_types, HSB, BINARY)
from hashkernel.smattr import (JsonWrap, SmAttr)
from hashkernel.hashing import (
    Hasher, shard_name_int, shard_num, HashBytes)

log = logging.getLogger(__name__)

B62 = base_x(62)


MAX_NUM_OF_SHARDS = 8192


class CakeRole(CodeEnum):
    SYNAPSE = (0,)
    NEURON = (1,)


_IS_PORTAL, _IS_VTREE, _IS_RESOLVED = (
    "is_portal", "is_vtree", "is_resolved" )


class CakeType(CodeEnum):
    INLINE = (0, )
    SHA256 = (1, _IS_RESOLVED)
    PORTAL = (2, _IS_PORTAL)
    VTREE = (3, _IS_VTREE)
    DMOUNT = (4, _IS_PORTAL)

    def __init__(self, code:int, *modifiers:str) -> None:
        CodeEnum.__init__(self, code)
        self.is_vtree = _IS_VTREE in modifiers
        self.is_portal = self.is_vtree or _IS_PORTAL in modifiers
        self.is_resolved = _IS_RESOLVED in modifiers


def portal_from_name(n:Optional[str])->CakeType:
    """
    >>> portal_from_name('')
    <CakeType.PORTAL: 2>
    >>> portal_from_name('PORTAL')
    <CakeType.PORTAL: 2>
    >>> portal_from_name('DMOUNT')
    <CakeType.DMOUNT: 4>
    >>> portal_from_name('VTREE')
    <CakeType.VTREE: 3>
    >>> portal_from_name('INLINE')
    Traceback (most recent call last):
    ...
    ValueError: not a portal type:INLINE
    """
    if n is None or n == '':
        return CakeType.PORTAL
    ct = CakeType[n]
    if ct.is_portal :
        return ct
    raise ValueError('not a portal type:'+n)


class CakeClass(CodeEnum):
    NO_CLASS = (0, None, None)
    EVENT = (1, CakeRole.SYNAPSE, Event)
    DAG_STATE = (2, CakeRole.NEURON, None)
    JSON_WRAP = (3, CakeRole.SYNAPSE, JsonWrap )

    def __init__(self,
                 code:int,
                 implied_role:Optional[CakeRole],
                 json_type:Optional[type]
                 ) -> None:
        CodeEnum.__init__(self, code)
        self.implied_role = implied_role
        self.json_type = json_type


inline_max_bytes=32


def nop_on_chunk(chunk:bytes)->None:
    """
    Does noting

    >>> nop_on_chunk(b'')

    :param read_buffer: takes bytes
    :return: does nothing
    """
    pass




def process_stream(fd:IO[bytes],
                   on_chunk:Callable[[bytes], None]=nop_on_chunk,
                   chunk_size:int=65355
                   )->Tuple[bytes,Optional[bytes]]:
    """
    process stream to calculate hash, length of data,
    and if it is smaller then hash size, holds on to stream
    content to use it instead of hash.

    :param fd: stream
    :param on_chunk: function  called on every chunk
    :return: (<hash>, Optional[<inline_data>])
    """
    inline_data = bytes()
    hasher = Hasher()
    length = 0
    while True:
        chunk = fd.read(chunk_size)
        if len(chunk) <= 0:
            break
        length += len(chunk)
        hasher.update(chunk)
        on_chunk(chunk)
        if length <= inline_max_bytes:
            inline_data += chunk
    fd.close()
    return (hasher.digest(),
            None if length > inline_max_bytes else inline_data)

class CakeHeader(SmAttr):
    """
    >>> CakeHeader(type=CakeType.INLINE, role=CakeRole.SYNAPSE).pack()
    0
    >>> CakeHeader(type=CakeType.SHA256, role=CakeRole.NEURON).pack()
    3
    >>> CakeHeader(type=CakeType.VTREE, role=CakeRole.NEURON,
    ...            cclass=CakeClass.DAG_STATE).pack()
    39
    >>> str(CakeHeader.unpack(0))
    '{"cclass": "NO_CLASS", "role": "SYNAPSE", "type": "INLINE"}'
    >>> str(CakeHeader.unpack(3))
    '{"cclass": "NO_CLASS", "role": "NEURON", "type": "SHA256"}'
    >>> str(CakeHeader.unpack(39))
    '{"cclass": "DAG_STATE", "role": "NEURON", "type": "VTREE"}'
    """
    type: CakeType
    role: CakeRole
    cclass: CakeClass = CakeClass.NO_CLASS

    def pack(self):
        return ((self.cclass.code&15) << 4)|\
               ((self.type.code&7) << 1)|\
               (self.role.code&1)

    @staticmethod
    def unpack(header:int)->'CakeHeader':
        return CakeHeader(
            type=CakeType.find_by_code((header >> 1) & 7),
            role=CakeRole.find_by_code(header & 1),
            cclass=CakeClass.find_by_code((header >> 4) & 15))

class Cake(Stringable, EnsureIt):
    """
    Stands for Content Address Key.

    Content addressing scheme using SHA256. For small
    content ( <=32 bytes) data is embeded  in key.  Header byte is
    followed by hash digest or inlined data. header byte split in two
    halves: `CakeType` and `CakeRole`. Base62 encoding is
    used to encode bytes.

    >>> CakeRole('SYNAPSE') == CakeRole.SYNAPSE
    True
    >>> CakeRole('SYNAPSE')
    <CakeRole.SYNAPSE: 0>
    >>> list(CakeType) #doctest: +NORMALIZE_WHITESPACE
    [<CakeType.INLINE: 0>, <CakeType.SHA256: 1>, <CakeType.PORTAL: 2>,
     <CakeType.VTREE: 3>, <CakeType.DMOUNT: 4>]

    >>> short_content = b'The quick brown fox jumps over'
    >>> short_k = Cake.from_bytes(short_content)
    >>> short_k.header.type
    <CakeType.INLINE: 0>
    >>> short_k.has_data()
    True
    >>> short_k.data() is not None
    True
    >>> short_k.data() == short_content
    True
    >>> str(short_k)
    '01aMUQDApalaaYbXFjBVMMvyCAMfSPcTojI0745igi'

    Longer content is hashed with SHA256:

    >>> longer_content = b'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.'
    >>> longer_k = Cake.from_bytes(longer_content)
    >>> longer_k.header.type
    <CakeType.SHA256: 1>
    >>> longer_k.has_data()
    False
    >>> longer_k.data() is None
    True
    >>> str(longer_k)
    '2xgkyws1ZbSlXUvZRCSIrjne73Pv1kmYArYvhOrTtqkX'
    >>> len(longer_k.hash_bytes())
    32
    >>> len(longer_k.digest())
    32
    >>> len(set([hash(longer_k) , hash(longer_k)]))
    1

    Global Unique ID can be generated, it is 32 byte
    random sequence packed in same way.

    >>> guid = Cake.new_portal()
    >>> guid.header.type
    <CakeType.PORTAL: 2>
    >>> len(str(guid))
    44
    """
    def __init__(self,
                 s:Optional[str],
                 data:Optional[bytes]=None,
                 header:Optional[CakeHeader]=None
                 )->None:
        if s is None:
            if data is None or header is None :
                raise AssertionError(
                    f'both data={data} and header={header} required')
            self._data = data
            self.header = header
        else:
            decoded = B62.decode(ensure_string(s))
            self._data = decoded[1:]
            self.header = CakeHeader.unpack(decoded[0])

        if not(self.has_data()):
            if len(self._data) != 32:
                raise AssertionError(f'invalid CAKey: {s}' )

    def shard_num(self, base:int)->int:
        """
        >>> Cake('0').shard_num(8192)
        0
        >>> Cake.from_bytes(b' ').shard_num(8192)
        32
        >>> Cake('2xgkyws1ZbSlXUvZRCSIrjne73Pv1kmYArYvhOrTtqkX').shard_num(8192)
        5937

        """
        l = len(self._data)
        if l >= 2:
            return shard_num(self._data, base)
        elif l == 1:
            return self._data[0]
        else:
            return 0

    def shard_name(self, base: int)->str:
        return shard_name_int(self.shard_num(base))

    @staticmethod
    def from_digest_and_inline_data(digest: bytes,
                                    buffer: Optional[bytes],
                                    **ch_kwargs
                                    )->'Cake':
        if 'role' not in ch_kwargs:
            ch_kwargs['role'] = CakeRole.SYNAPSE
        if buffer is not None and len(buffer) <= inline_max_bytes:
            return Cake(None,
                        data=buffer,
                        header=CakeHeader(ch_kwargs,
                                          type=CakeType.INLINE))
        else:
            return Cake(None,
                        data=digest,
                        header=CakeHeader(ch_kwargs,
                                          type=CakeType.SHA256))

    @staticmethod
    def from_stream(fd: IO[bytes], **ch_kwargs)->'Cake':
        digest, inline_data = process_stream(fd)
        return Cake.from_digest_and_inline_data(digest, inline_data,
                                                **ch_kwargs)

    @staticmethod
    def from_bytes(s, **ch_kwargs)->'Cake':
        return Cake.from_stream(BytesIO(s), **ch_kwargs)

    @staticmethod
    def from_file(file, **ch_kwargs)->'Cake':
        return Cake.from_stream(open(file, 'rb'), **ch_kwargs)

    @staticmethod
    def new_portal(**ch_kwargs)->'Cake':
        if 'role' not in ch_kwargs:
            ch_kwargs['role'] = CakeRole.SYNAPSE
        if 'type' not in ch_kwargs:
            ch_kwargs['type'] = CakeType.PORTAL
        cake = Cake(None, data=os.urandom(32),
                    header=CakeHeader(**ch_kwargs))
        cake.assert_portal()
        return cake

    def transform_portal(self, **kwargs)->'Cake':
        self.assert_portal()
        new_header = CakeHeader(self.header.to_json(), **kwargs)
        if (new_header == self.header):
            return self
        return Cake(None, data=self._data, header=new_header)

    def has_data(self)->bool:
        return self.header.type == CakeType.INLINE

    def is_resolved(self)->bool:
        return self.header.type.is_resolved

    def data(self)->Optional[bytes]:
        return self._data if self.has_data() else None

    def digest(self)->bytes:
        if not(hasattr(self, '_digest')):
            if self.has_data():
                self._digest = Hasher(self._data).digest()
            else:
                self._digest = self._data
        return self._digest

    def is_immutable(self)->bool:
        return self.has_data() or self.header.type.is_resolved

    def assert_portal(self)->None:
        if not self.header.type.is_portal:
            raise AssertionError('has to be a portal: %r' % self)

    def hash_bytes(self)->bytes:
        """
        :raise AssertionError when Cake is not hash based
        :return: hash in bytes
        """
        if not self.header.type.is_resolved:
            raise AssertionError(f"Not-hash {self.header.type} {self}")
        return self._data

    def __str__(self)->str:
        return B62.encode(bytes([(self.header.pack())]) + self._data)

    def __repr__(self)->str:
        return f"Cake({str(self)!r})"

    def __hash__(self)->int:
        if not(hasattr(self, '_hash')):
            self._hash = hash(self.digest())
        return self._hash

    def __eq__(self, other)->bool:
        if not isinstance(other, Cake):
            return False
        return self._data == other._data and \
               self.header == other.header

    def __ne__(self, other)->bool:
        return not self.__eq__(other)

HashBytes.register(Cake)


class HasCake(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def cake(self)->Cake:
        raise NotImplementedError('subclasses must override')


class PatchAction(Jsonable, enum.Enum):
    update = +1
    delete = -1

    @classmethod
    def factory(cls):
        return lambda s: cls[s]

    def __str__(self):
        return self.name

    def to_json(self):
        return str(self)


class RackRow(SmAttr):
    name: str
    cake: Optional[Cake]

    def role(self)->CakeRole:
        return CakeRole.NEURON if self.cake is None \
            else self.cake.header.role


class CakeRack(Jsonable):
    """
    sorted dictionary of names and corresponding Cakes

    >>> short_k = Cake.from_bytes(b'The quick brown fox jumps over')
    >>> longer_k = Cake.from_bytes(b'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.')

    >>> cakes = CakeRack()
    >>> cakes['short'] = short_k
    >>> cakes['longer'] = longer_k
    >>> len(cakes)
    2

    >>> cakes.keys()
    ['longer', 'short']
    >>> str(cakes.cake())
    '3fqJUOtUYjGCs3cWuPum5CwXtyyeJPRRp3gJ3A9wg3uS'
    >>> cakes.size()
    117
    >>> cakes.content()
    '[["longer", "short"], ["2xgkyws1ZbSlXUvZRCSIrjne73Pv1kmYArYvhOrTtqkX", "01aMUQDApalaaYbXFjBVMMvyCAMfSPcTojI0745igi"]]'
    >>> cakes.get_name_by_cake("2xgkyws1ZbSlXUvZRCSIrjne73Pv1kmYArYvhOrTtqkX")
    'longer'
    """
    def __init__(self,o:Any=None)->None:
        self.store: Dict[str,Optional[Cake]] = {}
        self._clear_cached()
        if o is not None:
            self.parse(o)

    def _clear_cached(self):
        self._inverse: Any = None
        self._cake: Any = None
        self._content: Any = None
        self._size: Any = None
        self._in_bytes: Any = None
        self._defined: Any = None

    def inverse(self)->Dict[Optional[Cake],str]:
        if self._inverse is None:
            self._inverse = {v: k for k, v in self.store.items()}
        return self._inverse

    def cake(self)->Cake:
        if self._cake is None:
            in_bytes = bytes(self)
            self._cake = Cake.from_digest_and_inline_data(
                Hasher(in_bytes).digest(),
                in_bytes,
                role=CakeRole.NEURON)
        return self._cake

    def content(self)->str:
        if self._content is None:
            self._content = str(self)
        return self._content

    def __bytes__(self)->bytes:
        if self._in_bytes is None:
            self._in_bytes = utf8_encode(self.content())
        return self._in_bytes

    def size(self)->int:
        if self._size is None:
            self._size = len(bytes(self))
        return self._size

    def is_defined(self)->bool:
        if self._defined is None:
            self._defined = all(
                v is not None for v in self.store.values())
        return self._defined

    def parse(self, o:Any)->'CakeRack':
        self._clear_cached()
        if isinstance(o, str):
            names, cakes = json.loads(o)
        elif type(o) in [list, tuple] and len(o) == 2:
            names, cakes = o
        else:
            names, cakes = json.load(o)
        self.store.update(zip(names, map(Cake.ensure_it_or_none, cakes)))
        return self

    def merge(self,
              previous:'CakeRack'
              )->Iterable[Tuple[PatchAction,str,Optional[Cake]]]:
        """
        >>> o1 = Cake.from_bytes(b'The quick brown fox jumps over')
        >>> o2v1 = Cake.from_bytes(b'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.')
        >>> o2v2 = Cake.from_bytes(b'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. v2')
        >>> o3 = CakeRack().cake()
        >>> r1 = CakeRack()
        >>> r1['o1']=o1
        >>> r1['o2']=o2v1
        >>> r1['o3']=None
        >>> r2 = CakeRack()
        >>> r2['o1']=o1
        >>> r2['o2']=o2v2
        >>> r2['o3']=o3
        >>> list(r2.merge(r1))
        [(<PatchAction.update: 1>, 'o2', Cake('2KLrqwGfNUC75Zk46B8SIbyYQFcm4FoW8UgOd9xnkKD9'))]
        >>> list(r1.merge(r2))
        [(<PatchAction.update: 1>, 'o2', Cake('2xgkyws1ZbSlXUvZRCSIrjne73Pv1kmYArYvhOrTtqkX'))]
        >>> r1['o1'] = None
        >>> list(r2.merge(r1)) #doctest: +NORMALIZE_WHITESPACE
        [(<PatchAction.delete: -1>, 'o1', None),
        (<PatchAction.update: 1>, 'o1', Cake('01aMUQDApalaaYbXFjBVMMvyCAMfSPcTojI0745igi')),
        (<PatchAction.update: 1>, 'o2', Cake('2KLrqwGfNUC75Zk46B8SIbyYQFcm4FoW8UgOd9xnkKD9'))]
        >>> list(r1.merge(r2)) #doctest: +NORMALIZE_WHITESPACE
        [(<PatchAction.delete: -1>, 'o1', None),
        (<PatchAction.update: 1>, 'o1', None),
        (<PatchAction.update: 1>, 'o2', Cake('2xgkyws1ZbSlXUvZRCSIrjne73Pv1kmYArYvhOrTtqkX'))]
        >>> del r1["o2"]
        >>> list(r2.merge(r1)) #doctest: +NORMALIZE_WHITESPACE
        [(<PatchAction.delete: -1>, 'o1', None),
        (<PatchAction.update: 1>, 'o1', Cake('01aMUQDApalaaYbXFjBVMMvyCAMfSPcTojI0745igi')),
        (<PatchAction.update: 1>, 'o2', Cake('2KLrqwGfNUC75Zk46B8SIbyYQFcm4FoW8UgOd9xnkKD9'))]
        >>> list(r1.merge(r2)) #doctest: +NORMALIZE_WHITESPACE
        [(<PatchAction.delete: -1>, 'o1', None),
        (<PatchAction.update: 1>, 'o1', None),
        (<PatchAction.delete: -1>, 'o2', None)]
        """
        for k in sorted(list(set(self.keys() + previous.keys()))):
            if k not in self and k in previous:
                yield PatchAction.delete, k, None
            else:
                v = self[k]
                neuron = self.is_neuron(k)
                if k in self and k not in previous:
                    yield PatchAction.update, k, v
                else:
                    prev_v = previous[k]
                    prev_neuron = previous.is_neuron(k)
                    if v != prev_v:
                        if neuron == True and prev_neuron == True:
                            continue
                        if prev_neuron == neuron:
                            yield PatchAction.update, k, v
                        else:
                            yield PatchAction.delete, k, None
                            yield PatchAction.update, k, v

    def is_neuron(self, k)->Optional[bool]:
        v = self.store[k]
        return v is None or v.header.role == CakeRole.NEURON

    def __iter__(self)->Iterable[str]:
        return iter(self.keys())

    def __setitem__(self, k:str, v:Union[Cake,str,None])->None:
        self._clear_cached()
        self.store[k] = Cake.ensure_it_or_none(v)

    def __delitem__(self, k:str):
        self._clear_cached()
        del self.store[k]

    def __getitem__(self, k:str)->Optional[Cake]:
        return self.store[k]

    def __len__(self)->int:
        return len(self.store)

    def __contains__(self, k:str)->bool:
        return k in self.store

    def get_name_by_cake(self, k:Union[Cake,str]):
        return self.inverse()[Cake.ensure_it(k)]

    def keys(self)->List[str]:
        names = list(self.store.keys())
        names.sort()
        return names

    def get_cakes(self, names=None)->List[Optional[Cake]]:
        if names is None:
            names = self.keys()
        return [self.store[k] for k in names]

    def to_json(self)->Tuple[List[str],List[Optional[Cake]]]:
        keys = self.keys()
        return (keys, self.get_cakes(keys))


HasCake.register(CakeRack)


class HasCakeFromBytesMixin:

    def cake(self)->Cake:
        return Cake.from_bytes(bytes(self)) #type: ignore


class CakePath(Stringable, EnsureIt):
    """
    >>> root = CakePath('/dCYNBHoPFLCwpVdQU5LhiF0i6U60KF')
    >>> root
    CakePath('/dCYNBHoPFLCwpVdQU5LhiF0i6U60KF/')
    >>> root.root
    Cake('dCYNBHoPFLCwpVdQU5LhiF0i6U60KF')
    >>> root.root.header.role
    <CakeRole.NEURON: 1>
    >>> root.root.header.type
    <CakeType.INLINE: 0>
    >>> root.root.data()
    b'[["b.text"], ["06wO"]]'
    >>> absolute = CakePath('/dCYNBHoPFLCwpVdQU5LhiF0i6U60KF/b.txt')
    >>> absolute
    CakePath('/dCYNBHoPFLCwpVdQU5LhiF0i6U60KF/b.txt')
    >>> relative = CakePath('y/z')
    >>> relative
    CakePath('y/z')
    >>> relative.make_absolute(absolute)
    CakePath('/dCYNBHoPFLCwpVdQU5LhiF0i6U60KF/b.txt/y/z')

    `make_absolute()` have no effect to path that already
    absolute

    >>> p0 = CakePath('/dCYNBHoPFLCwpVdQU5LhiF0i6U60KF/r/f')
    >>> p0.make_absolute(absolute)
    CakePath('/dCYNBHoPFLCwpVdQU5LhiF0i6U60KF/r/f')
    >>> p1 = p0.parent()
    >>> p2 = p1.parent()
    >>> p1
    CakePath('/dCYNBHoPFLCwpVdQU5LhiF0i6U60KF/r')
    >>> p2
    CakePath('/dCYNBHoPFLCwpVdQU5LhiF0i6U60KF/')
    >>> p2.parent()
    >>> p0.path_join()
    'r/f'
    >>> p1.path_join()
    'r'
    >>> p2.path_join()
    ''
    >>> str(CakePath('q/x/палка_в/колесе.bin'))
    'q/x/палка_в/колесе.bin'
    """
    def __init__(self, s, _root = None, _path = []):
        if s is  None:
            self.root = _root
            self.path = _path
        else:
            split = PurePosixPath(s).parts
            if len(split) > 0 and split[0] == '/' :
                self.root = Cake(split[1])
                self.path = split[2:]
            else:
                self.root = None
                self.path = split

    def child(self, name):
        path = list(self.path)
        path.append(name)
        return CakePath(None, _path=path, _root=self.root)

    def parent(self):
        if self.relative() or len(self.path) == 0 :
            return None
        return CakePath(None, _path=self.path[:-1], _root=self.root)

    def next_in_relative_path(self):
        if not self.relative():
            raise AssertionError("only can be applied to relative")
        l = len(self.path)
        reminder = None
        if l < 1:
            next= None
        else:
            next=self.path[0]
            if l > 1:
                reminder = CakePath(None, _path=self.path[1:])
        return next,reminder

    def relative(self):
        return self.root is None

    def is_root(self):
        return not self.relative() and len(self.path) == 0

    def make_absolute(self, current_cake_path):
        if self.relative():
            path = list(current_cake_path.path)
            path.extend(self.path)
            return CakePath(
                None ,_root=current_cake_path.root, _path=path)
        else:
            return self

    def __str__(self):
        if self.relative():
            return self.path_join()
        else:
            return f'/{str(self.root)}/{self.path_join()}'

    def path_join(self):
        return '/'.join(self.path)

    def filename(self):
        l = len(self.path)
        if l > 0 and self.path[l-1]:
            return self.path[l-1]


def cake_or_path(s, relative_to_root=False):
    if isinstance(s, Cake) or isinstance(s, CakePath):
        return s
    elif s[:1] == '/':
        return CakePath(s)
    elif relative_to_root and '/' in s:
        return CakePath('/'+s)
    else:
        return Cake(s)


def ensure_cakepath(s):
    if not(isinstance(s, (Cake,CakePath) )):
        s = cake_or_path(s)
    if isinstance(s, Cake):
        return CakePath(None, _root=s)
    else:
        return s


"""
@guest
    def info(self):
    def login(self, email, passwd, client_id=None):
    def authorize(self, cake, pts):
    def get_info(self, cake_path) -> PathInfo
    def get_content(self, cake_or_path) -> LookupInfo:

@user
    def logout(self):
    def write_content(self, fp, chunk_size=65355):
    def store_directories(self, directories):
    def create_portal(self, portal_id, cake):
    def edit_portal(self, portal_id, cake):
    def list_acls(self):
    def edit_portal_tree(self, files, asof_dt=None):
    def delete_in_portal_tree(self, cake_path, asof_dt = None):
    def get_portal_tree(self, portal_id, asof_dt=None):
    def grant_portal(self, portal_id, grantee, permission_type):
    def delete_portal(self, portal_id):

@admin
    def add_user(self, email, ssha_pwd, full_name = None):
    def remove_user(self, user_or_email):
    def add_acl(self, user_or_email, acl):
    def remove_acl(self, user_or_email, acl):

"""


class HashSession(metaclass=abc.ABCMeta):

    @staticmethod
    def get() -> 'HashSession':
        return threading.local().hash_ctx

    @staticmethod
    def set(ctx: 'HashSession') -> None:
        threading.local().hash_ctx = ctx

    @staticmethod
    def close() -> None:
        l = threading.local()
        if hasattr(l, 'hash_ctx'):
            l.hash_ctx.close()
            l.hash_ctx = None

    @abc.abstractmethod
    def get_info(self, cake_path:CakePath ) -> 'PathInfo':
        raise NotImplementedError('subclasses must override')

    @abc.abstractmethod
    def get_content(self, cake_path:CakePath ) -> 'LookupInfo':
        raise NotImplementedError('subclasses must override')

    # @abc.abstractmethod
    # def write_content(self, fp:IO[bytes], chunk_size:int=65355
    #                   ) -> HashBytes:
    #     raise NotImplementedError('subclasses must override')
    #
    # @abc.abstractmethod
    # def store_directories(self, directories:Dict[Cake,CakeRack]):
    #     raise NotImplementedError('subclasses must override')
    #
    # @abc.abstractmethod
    # def edit_portal(self, cake_path, cake):
    #     raise NotImplementedError('subclasses must override')
    #
    # @abc.abstractmethod
    # def query(self, cake_path, include_path_info:bool=False) -> CakeRack:
    #     raise NotImplementedError('subclasses must override')
    #
    # @abc.abstractmethod
    # def edit_portal_tree(self,
    #         files:List[PatchAction,Cake,Optional[Cake]],
    #         asof_dt:datetime=None):
    #     raise NotImplementedError('subclasses must override')


class PathResolved(SmAttr):
    path: CakePath
    resolved: Optional[Cake]


class PathInfo(SmAttr):
    mime: str
    file_type: Optional[str]
    created_dt: Optional[datetime]
    size: Optional[int]


class Content(PathInfo):
    __serialize_as__ = PathInfo
    data: Optional[bytes]
    stream_fn: Optional[Callable[[],IO[bytes]]]
    file: Optional[str]

    def has_data(self) -> bool:
        return self.data is not None

    def get_data(self) -> bytes:
        return self.stream().read() if self.data is None else self.data

    def stream(self) -> IO[bytes]:
        """
        stream is always avalable
        """
        if self.data is not None:
            return BytesIO(self.data)
        elif self.file is not None:
            return open(self.file, 'rb')
        elif self.stream_fn is not None:
            return self.stream_fn()
        else:
            raise AssertionError(f'cannot stream: {repr(self)}')

    def has_file(self):
        return self.file is not None

    def open_fd(self):
        return os.open(self.file, os.O_RDONLY)

    @classmethod
    def from_file(cls, file):
        if not(os.path.exists(file)):
            raise FileNotFoundError()
        file_type = guess_name(file)
        return cls(file=file,
                   file_type=file_type,
                   mime=file_types[file_type].mime)

    @classmethod
    def from_data_and_role(cls, role:CakeRole,
                           data: Optional[bytes]=None,
                           file:Optional[str]=None ):
        file_type = HSB if role == CakeRole.NEURON else BINARY
        if data is not None:
            return cls(data=data, size=len(data),
                       file_type=file_type,
                       mime=file_types[file_type].mime)
        elif file is not None:
            return cls(file=file,
                       file_type=file_type,
                       mime=file_types[file_type].mime)
        else:
            raise AssertionError('file or data should be defined')


class LookupInfo(Content):
    path: CakePath
    info: Optional[PathInfo]


class MoldedCake(Cake):

    def get_instance(self):
        data = HashSession.get().get_content(self).get_data()
        return self.__smattr__(json.loads(data))


class EventCake(MoldedCake):
    __smattr__= Event

class JsonWrapCake(MoldedCake):
    __smattr__ = JsonWrap



class RemoteError(ValueError): pass


class CredentialsError(ValueError): pass


class NotAuthorizedError(ValueError): pass


class NotFoundError(ValueError): pass


RESERVED_NAMES = ('_', '~', '-')


def check_bookmark_name(name):
    """
    >>> check_bookmark_name('a')
    >>> check_bookmark_name('_')
    Traceback (most recent call last):
    ...
    ValueError: Reserved name: _
    >>> check_bookmark_name('a/h')
    Traceback (most recent call last):
    ...
    ValueError: Cannot contain slash: a/h
    """
    if '/' in name:
        raise ValueError('Cannot contain slash: ' +name)
    if name in RESERVED_NAMES:
        raise ValueError('Reserved name: '+name)