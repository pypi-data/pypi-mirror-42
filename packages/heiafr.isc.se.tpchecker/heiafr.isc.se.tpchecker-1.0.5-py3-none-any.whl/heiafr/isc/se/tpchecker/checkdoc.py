# Copyright 2019 Jacques Supcik, HEIA-FR
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import pathlib
import subprocess
from . import command

def checkDoc(root, path):
    p = pathlib.Path(root, path)
    if not p.is_file():
        return command.Result(ok=False, err='File "{0}" not found'.format(path))

    try:
        return command.Result(out=subprocess.check_output(
            ["pdfinfo", p],
            stderr=subprocess.STDOUT,
        ).decode("utf-8"))
        
    except subprocess.CalledProcessError as e:
        return command.Result(ok=False, err=e.stderr, out=e.stdout)
 