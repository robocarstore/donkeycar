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
            self.__cleansing()

    def __cleansing(self):
        import glob
        _ = glob.glob(f'{self.tub.base_path}/catalog_*.catalog')
        valid_manifest = [path.split(x)[-1] for x in _ if path.getsize(x) != 0]
        invalid_manifest = {remove(x) for x in _ if path.getsize(x) == 0}

        dir_image = listdir(self.tub.images_base_path)

        invalid_image = {int(re.findall('\d{1,}', x)[0]) for x in dir_image if
                         path.getsize(f'{self.tub.images_base_path}/{x}') == 0}

        self.tub.delete_records(invalid_image)

        if len(invalid_manifest) == 0 and len(invalid_image) == 0:  # health check
            return

        try:
            {remove(f'{self.tub.images_base_path}/{x}_cam_image_array_.jpg') for x in self.tub.manifest.deleted_indexes}
        except:
            print('Already Removed')

        self.tub.update_catalog(catalog=sorted(valid_manifest))

        return
