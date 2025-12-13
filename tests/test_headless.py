from __future__ import annotations

import sys

from hanoi.cli import main


def test_no_animate_does_not_import_pygame(monkeypatch):
    monkeypatch.setattr(sys, 'argv', ['hanoi-viz', '--no-animate', '3'])
    main()
    assert 'pygame' not in sys.modules
