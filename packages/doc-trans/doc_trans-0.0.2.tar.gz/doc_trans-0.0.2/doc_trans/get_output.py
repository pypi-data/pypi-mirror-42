import sys
from io import StringIO

from y_trans.translator import Translator

class OutputInterceptor(list):
    def __enter__(self):
        self._stdout = sys.stdout
        sys.stdout = self._stringio = StringIO()
        return self

    def __exit__(self, *args):
        self.extend(self._stringio.getvalue().splitlines())
        del self._stringio
        sys.stdout = self._stdout


def rus_help(obj):
    with OutputInterceptor() as output:
        help(obj)
    
    text = '\n'.join(output)
    translate = Translator()
    print(text + translate.get_translation('\n'.join(output)))
