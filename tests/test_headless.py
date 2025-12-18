from __future__ import annotations

import sys

from _pytest.monkeypatch import MonkeyPatch

from hanoi.cli import main


def test_no_animate_does_not_import_pygame(monkeypatch: MonkeyPatch):
    monkeypatch.setattr(sys, 'argv', ['hanoi-viz', '--no-animate', '3'])
    main()
    assert 'pygame' not in sys.modules
