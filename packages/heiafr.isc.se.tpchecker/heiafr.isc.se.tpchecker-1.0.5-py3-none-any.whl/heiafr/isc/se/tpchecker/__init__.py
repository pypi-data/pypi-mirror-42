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

import jinja2
import weasyprint

from . import checkdoc, checkgit


class TpChecker:

    def __init__(self, projectRoot: str, subtitle=None):
        self.env = jinja2.Environment(
            loader=jinja2.PackageLoader(
                'heiafr.isc.se.tpchecker', 'templates'),
            autoescape=jinja2.select_autoescape(['html', 'xml'])
        )
        self.projectRoot = projectRoot
        self.subtitle = subtitle
        self.doc = None
        self.git = None
        self.gitlog = None

    def checkDoc(self, path):
        self.doc = checkdoc.checkDoc(self.projectRoot, path)

    def checkGit(self):
        self.git = checkgit.checkGit(self.projectRoot)

    def genReport(self, filename):
        template = self.env.get_template('report.html')
        html = template.render(data=self)
        weasyprint.HTML(string=html).write_pdf(
            filename,
            stylesheets=[
                weasyprint.CSS(pathlib.Path(__file__).parent.joinpath("css", "pure-nr.css")),
                weasyprint.CSS(pathlib.Path(__file__).parent.joinpath("css", "style.css"))
            ]
        )
