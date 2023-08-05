# -*- coding: utf8 -*-
from ..dulwich.object_store import BaseObjectStore


class _MlBaseObjectStore(BaseObjectStore):
    def __init__(self):
        self._multi_process_control = None

    def _get_loose_object(self, metadata):
        pass

    def _gen_upload_sync_args(self, obj):
        pass

    def set_multi_process_control(self, multi_process_control):
        self._multi_process_control = multi_process_control

    def get_raw(self, metadata):
        """Obtain the raw text for an object.

        :param metadata: metadata for the object.
        :return: tuple with numeric type and object contents.
        """
        ret = self._get_loose_object(metadata)
        if ret is not None:
            return ret.type_num, ret.as_raw_string()

        raise KeyError(metadata)

    def _async_execute(self, sync_method, obj, callback=None):
        args = self._gen_upload_sync_args(obj)

        def on_finish(result):
            callback(obj)

        self._multi_process_control.execute(sync_method, args=args, callback=on_finish if callback else None)
