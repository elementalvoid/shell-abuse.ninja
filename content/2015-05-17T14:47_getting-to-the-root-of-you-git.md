Title:Getting to the root of your Git
Category: Dev Tools
Tags: git, bash, util
Summary: How to quickly cd to the root of your git repository.

```bash
function gcd {
  if which git &> /dev/null; then
    STATUS=$(git status 2>/dev/null)
    if [[ -z ${STATUS} ]]; then
      return
    fi
    TARGET="./$(command git rev-parse --show-cdup)$1"
    cd ${TARGET}
  fi
}
```
Tab completion!
```bash
function _git_cd {
  if $(which git &> /dev/null); then
    STATUS=$(git status 2>/dev/null)
    if [[ -z ${STATUS} ]]; then
      return
    fi
    TARGET="./$(command git rev-parse --show-cdup)"
    if [[ -d $TARGET ]]; then
      TARGET="$TARGET/"
    fi
    COMPREPLY=()
    cur="${COMP_WORDS[COMP_CWORD]}"
    prev="${COMP_WORDS[COMP_CWORD-1]}$2"
    opts=$(cd $TARGET; compgen -d -o dirnames -S / -X '@(*/.git|*/.git/|.git|.git/)' $2)
    if [[ ${cur} == * ]]; then
      COMPREPLY=( $(compgen -W "${opts}" -- ${cur}) )
      return 0
    fi
  fi
}
```
Usage:
```bash
ls -d .git  # <- we're in the root
mkdir -p a/b/c d/e/f
cd a/b/c
gcd d<TAB>
```
