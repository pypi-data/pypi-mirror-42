# -*- coding: utf-8 -*-
from __future__ import absolute_import

import tempfile
import mmap
import struct

from .mapped_struct import StrongIdMap

# Default section size is set to 128MB which is a size at which most
# malloc implementations turn to mmap
DEFAULT_SECTION_SIZE = 128<<20

DEFAULT_PACK_BUFFER = 65536

class Section(object):

    def __init__(self, buf, implicit_offs=0, idmap_kwargs={}):
        self.buf = buf
        self.real_buf = buffer(buf)
        self.attach(implicit_offs, idmap_kwargs)

    def allocate(self, size=None):
        write_pos = self.write_pos
        if size is None:
            size = len(self.buf) - write_pos
        if (write_pos + size) <= len(self.buf):
            self.write_pos += size
            return write_pos
        else:
            raise IndexError("Buffer overflow trying to allocate %d bytes from section" % size)

    def append(self, buf, verify_pos=None):
        write_pos = self.allocate(len(buf))
        if verify_pos is not None and verify_pos != write_pos:
            raise RuntimeError("Concurrent modification")
        self.buf[write_pos:write_pos+len(buf)] = bytes(buf)
        return write_pos

    @property
    def free_space(self):
        return len(self.buf) - self.write_pos

    def detach(self):
        del self.idmap

    def attach(self, implicit_offs=0, idmap_kwargs={}):
        self.implicit_offs = implicit_offs
        self.write_pos = 0
        self.idmap = StrongIdMap(**idmap_kwargs)

class BaseObjectPool(object):

    def _mktemp(self):
        raise NotImplementedError

    def __init__(self, section_size=DEFAULT_SECTION_SIZE, temp_kwargs={}, idmap_kwargs={},
            section_freelist=None):
        self.temp_kwargs = temp_kwargs
        self.idmap_kwargs = idmap_kwargs
        self.section_size = section_size
        self.sections = []
        self.total_size = 0
        self.idmap_preload = []
        self.section_freelist = section_freelist

    @property
    def size(self):
        if self.sections:
            last_section = self.sections[-1]
            return last_section.implicit_offs + last_section.write_pos
        else:
            return 0

    def add_section(self):
        f = None
        try:
            new_section = None
            implicit_offs = self.total_size

            if self.section_freelist:
                new_section = self.section_freelist.pop()
                new_section.attach(implicit_offs, self.idmap_kwargs)

            if new_section is None:
                f = self._mktemp()
                f.truncate(self.section_size)
                buf = mmap.mmap(
                    f.fileno(), 0,
                    access = mmap.ACCESS_WRITE)
                new_section = Section(buf, implicit_offs, self.idmap_kwargs)
                new_section.fileobj = f
            else:
                buf = new_section.buf

            self.total_size += len(buf)

            # Initialize with preloaded items
            if self.idmap_preload:
                idmap = {}
                try:
                    for schema, obj in self.idmap_preload:
                        self._pack_into(schema, obj, new_section, None, idmap)
                except (struct.error, IndexError):
                    raise RuntimeError("Preload items dont't fit in empty section, increase section size")
                new_section.idmap.preload(idmap)
        except:
            if f is not None:
                f.close()
            raise

        self.sections.append(new_section)
        return new_section

    def _pack_into(self, schema, obj, section, min_pack_buffer_cell=None, idmap=None, pack_buffer=None):
        write_pos = section.write_pos
        if idmap is None:
            idmap = section.idmap
        implicit_offs = section.implicit_offs + write_pos
        if hasattr(schema, 'pack'):
            buf = schema.pack(obj, idmap, implicit_offs=implicit_offs)
        elif hasattr(schema, 'pack_into'):
            if pack_buffer is None:
                if min_pack_buffer_cell:
                    pack_buffer_size = min_pack_buffer_cell[0]
                else:
                    pack_buffer_size = 1 << 20
                pack_buffer = bytearray(pack_buffer_size)
            endp = schema.pack_into(obj, pack_buffer, 0, idmap, implicit_offs=implicit_offs)
            buf = pack_buffer[:endp]
        if min_pack_buffer_cell:
            min_pack_buffer_cell[0] = max(min_pack_buffer_cell[0], len(buf))
        return section.append(buf, write_pos)

    def pack(self, schema, obj, min_pack_buffer=DEFAULT_PACK_BUFFER, clear_idmaps_on_new_section=True,
            pack_buffer=None):
        sections = self.sections
        _min_pack_buffer=[min_pack_buffer]
        for section in reversed(sections):
            if section.free_space < _min_pack_buffer[0]:
                continue

            try:
                pos = self._pack_into(schema, obj, section, _min_pack_buffer)
            except (struct.error, IndexError):
                # Possibly corrupt
                section.idmap.clear()
            else:
                break
        else:
            if clear_idmaps_on_new_section:
                self.clear_idmaps()
            section = self.add_section()
            pos = self._pack_into(schema, obj, section)
        return pos + section.implicit_offs, schema.unpack_from(section.real_buf, pos)

    def add(self, schema, buf, clear_idmaps_on_new_section=True):
        """
        Make sure the contents of buf are relocatable (ie: have no external references)
        """
        sections = self.sections
        for section in sections:
            if section.free_space < len(buf):
                continue

            try:
                pos = section.append(buf, section.write_pos)
            except (struct.error, IndexError):
                pass
            else:
                break
        else:
            if clear_idmaps_on_new_section:
                self.clear_idmaps()
            section = self.add_section()
            pos = section.append(buf, section.write_pos)
        return pos + section.implicit_offs, schema.unpack_from(section.real_buf, pos)

    def add_preload(self, schema, obj):
        """
        Preload this object and all its contents into all the individual sections.
        Fix those in the per-section idmap. Can improve both speed and reduce size
        if the objects to be appended references the objects contained in the preloaded
        objects a lot.
        """
        self.idmap_preload.append((schema, obj))

    def find_section(self, pos):
        for section in self.sections:
            if section.implicit_offs <= pos < section.implicit_offs + len(section.buf):
                return section

    def unpack(self, schema, pos):
        section = self.find_section(pos)
        if section is None:
            raise IndexError("Position %d out of bounds for object pool" % pos)
        return schema.unpack_from(section.real_buf, pos - section.implicit_offs)

    def clear_idmaps(self):
        for section in self.sections:
            section.idmap.clear()

    def dump(self, fileobj):
        if not self.sections:
            return 0

        for section in self.sections[:-1]:
            fileobj.write(section.real_buf)
        section = self.sections[-1]

        # Align to 8-bytes
        write_bytes = section.write_pos
        write_bytes += (8 - write_bytes % 8) % 8
        fileobj.write(section.real_buf[:write_bytes])
        return section.implicit_offs + write_bytes

    def close(self):
        sections = self.sections
        self.sections = []

        if self.section_freelist is not None:
            for section in sections:
                section.detach()
            self.section_freelist.extend(sections)

        self.total_size = 0

class TemporaryObjectPool(BaseObjectPool):

    def _mktemp(self):
        return tempfile.TemporaryFile(**self.temp_kwargs)
