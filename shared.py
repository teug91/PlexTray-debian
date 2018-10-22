#!/usr/bin/python

import sys, os, subprocess

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def open_browser(url):
    env = dict(os.environ)
    lp_key = 'LD_LIBRARY_PATH'
    lp_orig = env.get(lp_key + '_ORIG')
    if lp_orig is not None:
        env[lp_key] = lp_orig
    else:
        lp = env.get(lp_key)
        if lp is not None:
            env.pop(lp_key)
    subprocess.Popen(["xdg-open", url], env=env)
