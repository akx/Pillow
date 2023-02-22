#
# The Python Imaging Library.
# $Id$
#
# Windows Cursor support for PIL
#
# notes:
#       uses IcoImagePlugin.py to read the bitmap data.
#       Icons and cursors are almost identical,
#       except for the header format.
#
# history:
#       96-05-27 fl     Created
#
# Copyright (c) Secret Labs AB 1997.
# Copyright (c) Fredrik Lundh 1996.
#
# See the README file for information on usage and redistribution.
#
from . import IcoImagePlugin, Image


#
# --------------------------------------------------------------------


def _accept(prefix):
    return prefix[:4] == b"\0\0\2\0"


class CurFile(IcoImagePlugin.IcoFile):
    def _check_header(self, header):
        if not _accept(header):
            msg = "not a CUR file"
            raise SyntaxError(msg)

    def _read_icon_header(self, buf) -> dict:
        header = super()._read_icon_header(buf)
        # The planes/bpp fields are used for hotspot coordinates in cursors,
        # so rename them in the header to avoid confusion; removing `bpp`
        # (which would be a bogus value for a CUR) affects how IcoFile.frame()
        # determines a given sub-image's mask.
        header["hotspot_x"] = header.pop("planes")
        header["hotspot_y"] = header.pop("bpp")
        return header


class CurImageFile(IcoImagePlugin.IcoImageFile):
    """
    PIL read-only image support for Microsoft Windows .cur files.
    """
    format = "CUR"
    format_description = "Windows Cursor"
    _ico_file_class = CurFile


#
# --------------------------------------------------------------------

Image.register_open(CurImageFile.format, CurImageFile, _accept)

Image.register_extension(CurImageFile.format, ".cur")
