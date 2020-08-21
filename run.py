# -*- coding: utf-8 -*-
from scrapy.cmdline import execute
import sys

if __name__ == '__main__':
    if len(sys.argv) == 1:
        sys.argv.append(' ')
    if len(sys.argv) == 2:
        sys.argv.append('1')
    cmd = "scrapy crawl epio_spider -a keyword=%s -a page_num=%s" % (sys.argv[1], sys.argv[2])
    execute(cmd.split())
