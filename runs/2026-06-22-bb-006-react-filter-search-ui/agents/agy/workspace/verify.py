#!/usr/bin/env python3
import subprocess, sys
r = subprocess.run(['node', '--test', 'tests/filter.test.mjs'], text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
print(r.stdout, end='')
if r.returncode: sys.exit(r.returncode)
print('[verify_exit_code] 0')
