from  utest import ok, oks
import who1
import who2

@ok
def _ok4():
  "Can at least one test pass?"
  assert 1==1, "equality failure"

oks()
