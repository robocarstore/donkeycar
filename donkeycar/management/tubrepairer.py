from donkeycar.parts.tub_v2 import Tub
from os import listdir, path, remove
import re


class Tub(Tub):
    def update_catalog(self, catalog):
        self.manifest.catalog_paths = catalog
        self.manifest._update_catalog_metadata(self)


class TubRepairer(object):

    def __init__(self, args, parser):
        self.args = args
        self.parser = parser
        self.tub = None

    def run(self):
        """
        Remove some 0 byte image and update catalog
        """
        if self.args.tub is None:
            print("ERR>> --tub argument missing.")
            self.parser.print_help()
            return

        tub_paths = list(self.args.tub)

        for _ in tub_paths:
            self.tub = Tub(_)
            md, useless_index, health = self.__cleansing()
            if health == 0: continue
            self.tub.delete_records(useless_index)
            self.__delete_zero_byte_image()
            self.tub.update_catalog(catalog=md)

    def __cleansing(self):
        import glob
        _ = glob.glob(f'{self.tub.base_path}/catalog_*.catalog')
        tem = [path.split(x)[-1] for x in _ if path.getsize(x) != 0]

        dir_image = listdir(self.tub.images_base_path)

        def __getZero(_):
            return {int(re.findall('\d{1,}', x)[0]) for x in dir_image if
                    path.getsize(f'{self.tub.images_base_path}/{x}') == 0}

        zero = __getZero(dir_image)

        if len(zero) == 0:  # health check
            return '', '', 0

        return sorted(tem), zero, 1

    def __delete_zero_byte_image(self):
        try:
            {remove(f'{self.tub.images_base_path}/{x}_cam_image_array_.jpg') for x in self.tub.manifest.deleted_indexes}
        except:
            print('Nothing to remove')
