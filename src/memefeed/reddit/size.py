import urllib.request
from PIL import ImageFile


def getsizes(uri):
    # get file size *and* image size (None if not known)
    with urllib.request.urlopen(uri) as file:
        size = file.headers.get("content-length")
        if size:
            size = int(size)
        p = ImageFile.Parser()
        while 1:
            data = file.read(1024)
            if not data:
                break
            p.feed(data)
            if p.image:
                return size, p.image.size
                break
    return size, None


print(getsizes("https://i.redd.it/qg98174dpw8a1.jpg"))
