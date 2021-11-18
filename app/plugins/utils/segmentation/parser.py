import yaml


class YAMLConfig:
    def __init__(self, path):
        with open(str(path), 'r') as stream:
            self.config = yaml.safe_load(stream)

    def get_entry(self, entry_path, required=True):
        temp_value = self.config
        for key in entry_path:
            if key not in temp_value and required:
                raise ValueError('Parameter "{}" with path "{}" '
                                 'not found in configuration file.'.format(key, entry_path))
            elif key not in temp_value:
                return None
            else:
                temp_value = temp_value[key]

        return temp_value
