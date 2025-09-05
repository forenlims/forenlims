import shutil
import subprocess
from typing import List


def run_cmd(cmd: List[str]) -> int:
    exe = shutil.which(cmd[0])
    if exe is None:
        raise RuntimeError(f"Command not found: {cmd[0]}")
    cmd[0] = exe
    print(f"🔧 Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, check=False) # noqa: S603
    if result.returncode == 0:
        print('✅ Success')
    else:
        print(f"⚠️ Command exited with {result.returncode}, continuing...")
    return result.returncode


def main() -> None:
    """Run auto-fixers analog zu den Pre-Commit Hooks."""
    run_cmd(['ruff', 'check', '--fix', '.'])
    run_cmd(['djlint', '--reformat', '.'])
    print('🎉 All fixers have finished!')


if __name__ == '__main__':
    main()
