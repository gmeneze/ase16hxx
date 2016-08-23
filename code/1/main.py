from utest import ok, oks
import who1
import who2
import who3

@ok
def _ok3():
  "New passing test case"
  assert 2==2, "equality failure"

oks()