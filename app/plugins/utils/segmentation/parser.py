#  This file is part of DeepSpineTool
#  Copyright (C) 2021 VG-Lab (Visualization & Graphics Lab), Universidad Rey Juan Carlos
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.

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
