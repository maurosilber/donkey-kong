from tifffile import TiffFile

from .local_target import LocalTarget


class LocalTiff(LocalTarget):
    tif = None

    def open(self):
        self.tif = TiffFile(self.path)
        return self

    def close(self):
        if self.tif is not None:
            self.tif.close()

    def __len__(self):
        return len(self.tif.pages)

    @property
    def shape(self):
        return (len(self), *self.tif.pages[0].shape)

    def __getitem__(self, item):
        if isinstance(item, tuple):
            if isinstance(item[0], int):
                return self[item[0]][item[1:]]
            else:
                return self[item[0]][item]
        else:
            out = self.tif.asarray(key=item)
            if isinstance(item, list) and len(item) == 1:
                return out[None]  # Add axis
            elif isinstance(item, slice) and len(range(*item.indices(len(self)))) == 1:
                return out[None]  # Add axis
            else:
                return out
