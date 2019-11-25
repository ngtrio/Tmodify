import hashlib
from io import BytesIO
import zlib
import utils
from file_entry import FileEntry
import os
from PIL import Image


class TmodFile:
    MAGIC = 'TMOD'

    def __init__(self, path):
        self.path = path
        self.file = open(path, 'rb')

    def extract(self):
        self._read()
        self._flate()
        self._wirte()

    def _read(self):
        # magic
        if not self._check_magic():
            raise Exception('invalid .tmod file')
        # tModLoader version
        self.tml_vs = utils.read_string(self.file)
        # hash
        self.hash = self._read_bytes(20)
        # signature
        self.signature = self._read_bytes(256)
        # payload length
        self.pload_len = utils.read_int32(self.file)
        # payload
        pload = self._read_bytes(self.pload_len)
        # check data intergrity
        if self.hash != hashlib.sha1(pload).digest():
            raise Exception('data corruption')

        pload_stream = BytesIO(pload)
        # mod name
        self.name = utils.read_string(pload_stream)
        # mod version
        self.vs = utils.read_string(pload_stream)
        # mod file count
        self.file_cnt = utils.read_int32(pload_stream)
        # compressed data
        self.cprsd_data = pload_stream.read(-1)

        self.file.close()

    def _flate(self):
        self.files = []
        stream = BytesIO(self.cprsd_data)
        for i in range(self.file_cnt):
            f_name = utils.read_string(stream)
            if f_name.endswith('.rawimg'):
                f_name = '.png'.join(f_name.rsplit('.rawimg'))
            f_length = utils.read_int32(stream)
            f_cprsd_length = utils.read_int32(stream)
            self.files.append(FileEntry(f_name, f_length, f_cprsd_length))
        for fe in self.files:
            print('Flate: ' + fe.name, end='')
            if fe.length > fe.cprsd_length:
                fe.data = zlib.decompress(stream.read(fe.cprsd_length), -zlib.MAX_WBITS)
            else:
                fe.data = stream.read(fe.length)
            print(" => OK")

    def _wirte(self):
        extract_dir = self.path.replace('.tmod', '') + '/'
        if not os.path.exists(extract_dir):
            os.makedirs(extract_dir)
        for file in self.files:
            print('Write: ' + file.name, end='')
            path = extract_dir + file.name
            file_dir = os.path.split(path)[0]
            if not os.path.exists(file_dir):
                os.makedirs(file_dir)
            if file.name.endswith('.png') and file.name != 'icon.png':
                utils.raw_to_png(file.data, path)
            else:
                with open(path, 'wb') as f:
                    f.write(file.data)
            print(' ===> OK')

    def _check_magic(self):
        magic = str(self.file.read(4), "utf-8")
        if magic != self.MAGIC:
            raise Exception('invalid tmod file, expect: TMOD, actual: ' + magic)
        else:
            return True

    def _read_bytes(self, size):
        return self.file.read(size)
