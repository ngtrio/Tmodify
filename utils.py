from PIL import Image, ImageDraw
from io import BytesIO


def read_int32(bs, order='little'):
    return int.from_bytes(bs.read(4), order)

# 从TMOD二进制数据中读取string要按照C#中的BinaryReader.ReadString()读取方式


def read_string(bs):
    length = 0
    flag = 1
    while flag == 1:
        byte = bs.read(1)[0]
        flag = byte & 0b10000000
        length = length + (byte & 0b01111111)
    return str(bs.read(length), 'utf-8')


def raw_to_png(bs, path):
    stream = BytesIO(bs)
    version = read_int32(stream)
    width = read_int32(stream)
    height = read_int32(stream)
    num = width * height
    img = Image.new('RGBA', (width, height))
    imgdraw = ImageDraw.Draw(img, 'RGBA')
    for i in range(num):
        x = i % width
        y = i / width
        raw_color = read_int32(stream, 'big')
        r = raw_color >> 24 & 0xff
        g = raw_color >> 16 & 0xff
        b = raw_color >> 8 & 0xff
        a = raw_color >> 0 & 0xff
        ImageDraw.ImageDraw.point(imgdraw, (x, y), (r, g, b, a))
    img.save(path)

