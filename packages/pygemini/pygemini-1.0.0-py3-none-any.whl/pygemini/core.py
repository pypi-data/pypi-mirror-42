# coding: utf-8

class Gemini:
    
    def __init__(self, colum_fields, key_fields=['id'],  name='pygemini'):
        self._name = name

        self._key_fields = key_fields
        self._column_fields = colum_fields
        
        self._check_key_and_field()

        self._origin_list = []
        self._new_list = []

        self._origin_keys = []
        self._new_keys = []

        self._origin_dict = []
        self._new_dict = []

        # check for ready for process
        self._ready_flag = False
        # check for get result
        self._result_flag = False

        self._rst_insert = []
        self._rst_delete = []
        self._rst_update = []

    def _check_key_and_field(self):
        """ key fields need to be in column fields
        """
        if not set(self._column_fields) >= set(self._key_fields):
            raise Exception("key fields need to be in column fields")
        
    def _gen_key(self, dct):
        k_lst = [str(dct.get(str(i),'')) for i in self._key_fields]
        return '-'.join(k_lst)

    def _gen_item_dict(self, dct):
        """ 去除多余的columns
        """
        if not isinstance(dct, dict):
            raise TypeError("Please provide list of dict items")
        keys = dct.keys()
        if set(keys) < set(self._column_fields):
            raise TypeError("dict items lack columns")

        keys_to_delete = set(keys)-set(self._column_fields)
        for key in keys_to_delete:
            del dct[key]
        return dct

    def _gen_list(self, lst):
        """ 
        """
        if not isinstance(lst, list):
            raise TypeError("Please provide list items")
        if not lst:
            return []
        return [self._gen_item_dict(item) for item in lst]

    def _gen_global_dict(self, lst):
        dct = {}
        for i in lst:
            dct[self._gen_key(i)] = i
        return dct

    def gen_keys_and_dict(self):
        self._origin_dict = self._gen_global_dict(self._origin_list)
        self._origin_keys = self._origin_dict.keys()

        self._new_dict = self._gen_global_dict(self._new_list)
        self._new_keys = self._new_dict.keys()

    def load(self, origin_lst, new_lst):
        self._origin_list = self._gen_list(origin_lst)
        self._new_list = self._gen_list(new_lst)

        try:
            self.gen_keys_and_dict()
        except Exception as e:
            raise Exception("type error occurs in loading") from e

        self._ready_flag = True

    def check_ready(self):
        if not self._ready_flag:
            raise Exception("You need load origin and new list first")

    def check_result(self):
        if not self._result_flag:
            self.process()

    def process(self):
        self.check_ready()
        set_new_keys = set(self._new_keys)
        set_origin_keys = set(self._origin_keys)

        set_new = set_new_keys - set_origin_keys
        self._rst_insert = [self._new_dict[key] for key in set_new]

        set_old = set_origin_keys - set_new_keys
        self._rst_delete = [self._origin_dict[key] for key in set_old]

        set_update = set_new_keys & set_origin_keys
        self._rst_update = []
        for key in set_update:
            if self._origin_dict[key] != self._new_dict[key]:
                self._rst_update.append(self._new_dict[key])

        self._result_flag = True

    @property
    def items_insert(self):
        self.check_result()
        return self._rst_insert

    @property
    def items_delete(self):
        self.check_result()
        return self._rst_delete

    @property
    def items_update(self):
        self.check_result()
        return self._rst_update

    