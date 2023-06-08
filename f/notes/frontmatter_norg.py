# ========== PYTHON-FRONTMATTER WRAPPER CLASS - adds norg as a handler
# unused as im using YAML frontmatter
from frontmatter.default_handlers import BaseHandler
import frontmatter
import re


# BaseHandler.detect() is called from frontmatter.load() or frontmatter.loads()
class NORGHandler(BaseHandler):
    START_DELIMITER = "@document.meta"
    END_DELIMITER = "@end"
    FM_BOUNDARY = re.compile(r"^@document.meta\s*$|^@end\s*$", re.MULTILINE)

    def load(self, fm, **kwargs):
        """Parse Norg frontmatter"""
        metadata = {}
        for line in fm.split("\n"):
            if line == "":
                continue
            split = line.split(':')
            k = split[0].strip()
            v = split[1].strip()
            v = split[1].split(" ") if " " in v else v
            v = ' '.join(v).split() if isinstance(v, list) else v
            metadata[k] = v
        return metadata

    def export(self, metadata, **kwargs): 
        print("norg export not implemented yet")

frontmatter.handlers.append(NORGHandler())