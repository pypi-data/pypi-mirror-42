# -*- coding: utf8 -*-
import logging
import os
from .ml_base_object_store import _MlBaseObjectStore

from missinglink.legit import path_utils
from missinglink.legit.dulwich.objects import hex_to_filename, Blob


class DiskObjectStore(_MlBaseObjectStore):
    def __init__(self, volume_id, path, is_embedded):
        self.__path = path_utils.expend_and_validate_dir(path, validate_path=False)
        self.__volume_id = volume_id
        self.__is_embedded = is_embedded
        super(DiskObjectStore, self).__init__()

    @classmethod
    def _get_file_data(cls, full_object_path):
        return open(full_object_path, 'rb').read()

    def _get_loose_object(self, metadata):
        logging.debug('get object %s', metadata)

        sha = metadata['@id']

        if self.__is_embedded:
            object_path = os.path.join(self.__path, str(self.__volume_id), self._get_shafile_path(sha))
        else:
            object_path = os.path.join(self.__path, metadata['@path'])

        data = self._get_file_data(object_path)

        blob = Blob()
        blob.set_raw_chunks([data], sha)
        return blob

    @classmethod
    def _get_shafile_path(cls, sha):
        # Check from object dir
        return hex_to_filename('objects', sha)

    def _gen_upload_sync_args(self, obj):
        object_name = self._get_shafile_path(obj.sha)

        object_name = os.path.join(self.__path, str(self.__volume_id), object_name)

        return obj.full_path, object_name

    @classmethod
    def _copy_file(cls, src, dest):
        from shutil import copyfile

        path_utils.makedir(dest)
        copyfile(src, dest)

    def add_objects_async(self, objects, callback=None):
        for obj in objects:
            self._async_execute(self._copy_file, obj, callback=callback)
