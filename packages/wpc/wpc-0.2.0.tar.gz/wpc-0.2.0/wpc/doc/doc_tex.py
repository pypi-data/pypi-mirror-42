import os

from wpc.doc import Doc


class DocTex(Doc):

    def ext_src(self):
        return 'tex'
