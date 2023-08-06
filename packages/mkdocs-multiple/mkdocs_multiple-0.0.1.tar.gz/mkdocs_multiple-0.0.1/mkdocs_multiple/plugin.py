import mkdocs
from mkdocs.config import config_options, Config
from mkdocs.plugins import BasePlugin
from mkdocs.structure.files import Files
from mkdocs.structure.nav import Navigation as MkDocsNavigation

import re
import json
import logging
from pathlib import Path

# See https://www.mkdocs.org/user-guide/plugins/#developing-plugins


RE_ZOTERO=re.compile(r"""\(zotero://select/items/(\d+)_([^)]+)\)""")

class MultiplePlugin(BasePlugin):

    config_scheme = (
        ('parent', mkdocs.config.config_options.Type(mkdocs.utils.string_types)),
    )

    def __init__(self):
        super().__init__()

     
    def on_post_build(self, markdown):
        pass