from __future__ import annotations
import subprocess, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent
EVIDENCE=ROOT/'evidence'; EVIDENCE.mkdir(exist_ok=True)
cmd=[sys.executable,'-m','pytest','-q',f'--junitxml={EVIDENCE / "pytest_results.xml"}']
proc=subprocess.run(cmd,cwd=ROOT,text=True,capture_output=True)
console=(proc.stdout or '')+(proc.stderr or '')
(EVIDENCE/'pytest_console_output.txt').write_text(console,encoding='utf-8')
print(console,end='')
sys.exit(proc.returncode)
