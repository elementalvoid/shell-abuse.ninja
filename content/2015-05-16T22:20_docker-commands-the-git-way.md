Title: Docker commands - the git way
Category: Docker
Tags: docker, git,
Author: Matt Klich - Chief Abuser
Summary: Wouldn't it be nice if you could run `docker compose` instead of `docker-compose`? What about Docker Machine? You can!

Wouldn't it be nice if you could run `docker compose` instead of `docker-compose`? What about Docker Machine? You can!
```language-bash
docker () {
  local cmd=$(command -v docker-${1});
  if [[ -n ${cmd} ]]; then
    shift;
    ${cmd} ${@};
  else
    command -p docker -- ${@};
  fi;
}
```

Throw that in your shell rc somewhere and then...
```language-bash
docker compose ps  # <-- instead of 'docker-compose ps'
       Name                      Command               State                    Ports
-------------------------------------------------------------------------------------------------------
dockerghost_ghost_1   /entrypoint.sh npm start - ...   Up      2368/tcp
dockerghost_nginx_1   /usr/bin/reefer -t /templa ...   Up      0.0.0.0:443->443/tcp, 0.0.0.0:80->80/tcp
```
---
Create your own commands - yours should be a little less pointless.
```language-bash
# Create a custom docker wrapper
docker-foo () { echo ' :: Hi there! ::'; }
# And run it
docker foo
 :: Hi there! ::
```
