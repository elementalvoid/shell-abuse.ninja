Title: When OSX shebang won't use Bash 4 from brew
Category: OSX
Tags: osx, bash, ugly hack
Summary: What do you do when OSX decides to replace Bash4 with Bash3? Get creative!

Gah! A fellow at work had a Mac that refused to run Bash 4 as installed via [Brew](http://brew.sh/). He could run `bash` from a shell and get 4.x but no matter what we did to the shebang of our script it always ended up running Bash 3 as installed by Apple. We came up with this ugly bit:
```language-bash
#!/usr/bin/env bash
## ensure bash 4.x
if [[ ${BASH_VERSION} < 4.0 && \
      -x /usr/local/bin/bash && \
      $(/usr/local/bin/bash -c 'echo $BASH_VERSION') > 4.0 ]]; then
  exec /usr/local/bin/bash ${0} ${@}
elif [[ ${BASH_VERSION} < 4.0 ]]; then
  echo 'Mac FOOL. Try running: brew install bash coreutils'
  exit 42
fi
```
It works on both Linux and Mac.
