import shutil
import subprocess
import sys
from typing import List


def run_cmd(cmd: List[str]) -> int:
    exe = shutil.which(cmd[0])
    if exe is None:
        raise RuntimeError(f"Command not found: {cmd[0]}")
    cmd[0] = exe
    print(f"🔍 Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, check=False) # noqa: S603
    if result.returncode == 0:
        print('✅ Passed')
    else:
        print(f"❌ Failed with {result.returncode}")
    return result.returncode


def main() -> None:
    """Run the same checks as pre-commit (without auto-fix)."""
    codes = []
    codes.append(run_cmd(['ruff', 'check', '.']))
    codes.append(run_cmd(['djlint', '--check', '.']))
    sys.exit(max(codes))


if __name__ == '__main__':
    main()
