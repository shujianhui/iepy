"""
Wikia Series Pre Processing

Usage:
    preprocess.py <dbname>

"""
import re

from docopt import docopt
from mwtextextractor import get_body_text

from iepy.db import connect, DocumentManager
from iepy.preprocess import PreProcessPipeline
from iepy.tokenizer import TokenizeSentencerRunner


def media_wiki_to_txt(doc):
    if not doc.text and doc.metadata.get('raw_text', ''):
        # After MW strip, titles will not be recognizable. If they dont
        # with a dot, will be very hard to split in sentences correctly.
        raw = doc.metadata['raw_text']
        raw = re.subn(r'==(.*)==', r'==\1.==', raw)[0]
        doc.text = get_body_text(raw)
        doc.save()

if __name__ == '__main__':
    import logging
    logger = logging.getLogger('iepy')
    logger.setLevel(logging.DEBUG)
    logger.addHandler(logging.StreamHandler())
    opts = docopt(__doc__, version=0.1)
    connect(opts['<dbname>'])
    docs = DocumentManager()
    pipeline = PreProcessPipeline(
        [media_wiki_to_txt, TokenizeSentencerRunner()], docs)
    pipeline.process_everything()