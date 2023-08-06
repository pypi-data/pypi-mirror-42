"""

require: https://wkhtmltopdf.org/

Bug on Ubuntu:

QXcbConnection: Could not connect to display
https://github.com/wkhtmltopdf/wkhtmltopdf/issues/2037

Run:
sudo apt install xvfb
to install xvfb-run command

Ubunntu:

xvfb-run -- wkhtmltopdf https://www.baidu.com/ baidu.pdf

Mac:

wkhtmltopdf https://www.baidu.com/ baidu.pdf
"""
import os
import sys
import subprocess

from iutil.hashes import (
    md5_for_text,
)


cmd_url2pdf_choices = {
    'linux': 'xvfb-run -- wkhtmltopdf',  # ubuntu 18.04
    'darwin': 'wkhtmltopdf',  # Mac
}

platform = sys.platform

cmd_url2pdf = cmd_url2pdf_choices[platform]


def url2pdf(url, out_dir='.', out_filename=None):
    if not out_filename:
        url_hash = md5_for_text(url)
        out_filename = '%s.pdf' % url_hash

    out_file = os.path.join(out_dir, out_filename)

    full_cmd = [cmd_url2pdf, '--log-level', 'none', url, out_file]
    # print(' '.join(full_cmd))
    res = subprocess.call(full_cmd)

    return res, out_file
