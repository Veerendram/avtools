from _winreg import HKEY_CURRENT_USER, HKEY_USERS, HKEY_LOCAL_MACHINE, \
    OpenKey, QueryInfoKey, EnumKey, CloseKey, EnumValue, QueryValueEx, \
    SetValueEx, FlushKey, KEY_ALL_ACCESS, KEY_SET_VALUE

from os import path

hkey_mapping = {
    "HKLM": HKEY_LOCAL_MACHINE,
    "HKCU": HKEY_CURRENT_USER,
    "HKU": HKEY_USERS
}

# Values are defined in _winreg.py
data_type_mapping = {
    "REG_NONE": 0,
    "REG_SZ": 1,
    "REG_EXPAND_SZ": 2,
    "REG_BINARY": 3,
    "REG_DWORD": 4,
    "REG_DWORD_LITTLE_ENDIAN": 4,
    "REG_DWORD_BIG_ENDIAN": 5,
    "REG_LINK": 6,
    "REG_MULTI_SZ": 7,
    "REG_RESOURCE_LIST": 8
}


class RegistryHandler:
    """
    Utility to Interact with Windows Registry to

    - Check if given Registry path exists
    - Get SubKeys in a Key
    - Get all the value and values_names in a give key/Sub-key
    - Get individual  Registry key -> value_name -> value
    - Modify single Registry key -> value_name -> value by value names.

    Hkeys are mapped to short form using a dictionary `mapping`

    Abbreviations:
    hkey - root key ( Handle to registry key)
    key - Main key , which could be software/system configurations key
    sub-key - a key under a main key
    value_name - Name of the parameter under key
    value_data - Data of the value_name

    """

    def __init__(self):
        pass

    @staticmethod
    def key_path_exists(hkey, key_path):
        """
        checks if key path exists.Given hkey(root key handle) and key path.
        This method will try to open the key and in case if that path
        doesn't exists in Registry, it will raise ValueError.
        """

        try:
            key = OpenKey(hkey_mapping[hkey], key_path)
        except WindowsError:
            raise ValueError("Key Path doesn't exist")
        CloseKey(key)
        return True

    def get_sub_keys(self, hkey, key_path):
        """
        Retrieves all the sub keys for given handle for registry key(hkey)
        and the application registry path.
        """

        self.key_path_exists(hkey, key_path)
        key = OpenKey(hkey_mapping[hkey], key_path)
        sub_keys = []
        no_of_subkeys = QueryInfoKey(key)[0]
        for i in range(0, no_of_subkeys):
            sub_keys.append(EnumKey(key, i))
        CloseKey(key)
        return sub_keys

    def get_sub_key_values(self, hkey, key_path, sub_key):
        """
        Get all the values of sub key value_name's as dictionary, for a given
        hkey, key path and sub key.
        """

        values = {}
        full_path = path.join(key_path, sub_key)
        self.key_path_exists(hkey, full_path)
        key = OpenKey(hkey_mapping[hkey], full_path)

        print "Number of value names: {} ".format(QueryInfoKey(key)[1])
        no_of_values = QueryInfoKey(key)[1]
        for i in range(0, no_of_values):
            values[EnumValue(key, i)[0]] = EnumValue(key, i)[1]
        CloseKey(key)
        return values

    def get_value_data(self, hkey, key_path, sub_key, value_name):
        """
        Get value_data for value_name, provided valid registry path with
        key and sub key path.
        """

        full_path = path.join(key_path, sub_key)
        self.key_path_exists(hkey, full_path)
        key = OpenKey(hkey_mapping[hkey], full_path, 0, KEY_ALL_ACCESS)
        try:
            result = QueryValueEx(key, value_name)
            CloseKey(key)
            return result[0]
        except KeyError:
            raise KeyError("unable to find registry Key and Value".format(key,
                                                                          value_name))

    def set_value_data(self, hkey, key_path, sub_key, value_name,
                       value_type, value_data):
        """
        Set the value_data for a value_name , provided valid registry path with
        key and sub key path.
        value_type parameter takes values for the data types.
        https://docs.python.org/2/library/_winreg.html#value-types
        """

        full_path = path.join(key_path, sub_key)
        self.key_path_exists(hkey, full_path)
        key = OpenKey(hkey_mapping[hkey], full_path, 0, KEY_SET_VALUE)
        SetValueEx(key, value_name, 0, data_type_mapping[value_type],
                   value_data)
        FlushKey(key)
        CloseKey(key)
