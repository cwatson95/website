#!/usr/bin/env python3
"""Assemble ui_drive_sound-waves.js from its two parts.

    python3 make_ui.py

`_ui_head.js` is the DOM-stub harness, taken unchanged from
build/waves-intro/ui_drive_waves-intro.js (which carries the innerHTML -> textContent fix) up
to the point where that file's sim-specific helpers begin; `_ui_body.js` is this sim's own
drive.  The orchestrator runs the assembled file by name, so it is checked in whole."""
import io
import os

HERE = os.path.dirname(os.path.abspath(__file__))
head = io.open(os.path.join(HERE, '_ui_head.js'), encoding='utf-8').read()
body = io.open(os.path.join(HERE, '_ui_body.js'), encoding='utf-8').read()
out = head + '\n' + body
io.open(os.path.join(HERE, 'ui_drive_sound-waves.js'), 'w', encoding='utf-8').write(out)
print('ui_drive_sound-waves.js: %d lines' % len(out.splitlines()))
