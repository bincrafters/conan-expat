#!/usr/bin/env python
# -*- coding: utf-8 -*-


from bincrafters import build_template_default
import os

if __name__ == "__main__":

    mingw = os.getenv("MINGW_CONFIGURATIONS", None)
    shared_option_name = False if mingw else "expat:shared"
    builder = build_template_default.get_builder(pure_c=True, shared_option_name=shared_option_name)

    builder.run()
