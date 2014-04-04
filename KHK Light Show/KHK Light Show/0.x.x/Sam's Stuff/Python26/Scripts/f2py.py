#!/usr/bin/env python.exe
# See http://cens.ioc.ee/projects/f2py2e/
import os, sys
for mode in ["g3-numpy", "2e-numeric", "2e-numarray", "2e-numpy"]:
    try:
        i=sys.argv.index("--"+mode)
        del sys.argv[i]
        break
    except ValueError: pass
os.environ["NO_SCIPY_IMPORT"]="f2py"
if mode=="g3-numpy":
    print >> sys.stderr, "G3 f2py support is not implemented, yet."
    sys.exit(1)
elif mode=="2e-numeric":
    from f2py2e import main
elif mode=="2e-numarray":
    sys.argv.append("-DNUMARRAY")
    from f2py2e import main
elif mode=="2e-numpy":
    from numpy.f2py import main
else:
    print >> sys.stderr, "Unknown mode:",`mode`
    sys.exit(1)
main()
