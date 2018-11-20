from PIL import Image
import imagehash


class PHash:
    def hash_value(self, arg, str=True):
        if(isinstance(arg, list)):
            if(str):
                return [imagehash.phash(Image.open(x)).__str__() for x in arg]
            else:
                return [imagehash.phash(Image.open(x)) for x in arg]
        else:
            if(str):
                return [imagehash.phash(Image.open(arg)).__str__()]
            else:
                return [imagehash.phash(Image.open(arg))]

    def similarity(self, ref, target):
        ref = self.hash_value(ref, False)
        target = self.hash_value(target, False)
        return [1 - (x - y) / len(x.hash)**2 for x in ref for y in target]


p = PHash()
result = p.similarity(
    '../old_image.jpg', ['../new_image1.jpg', '../new_image2.jpg', '../new_image3.jpg'])
