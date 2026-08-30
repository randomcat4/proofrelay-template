from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class ValidatorTest(unittest.TestCase):
    def test_template_repository_passes(self) -> None:
        result = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "validate_repo.py")],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("PASS:", result.stdout)


if __name__ == "__main__":
    unittest.main()
