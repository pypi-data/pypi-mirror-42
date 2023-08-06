# fd-replay project

fd-replay is an open-source daemon for replaying live HTTP traffic into multiple test environments.

## Getting started
For example, if you use nginx in our production environment, you can add mirror (http://nginx.org/en/docs/http/ngx_http_mirror_module.html) or post_action directive to forward traffic to fd-replay.
Edit fd-replay.yml file to declare your differents endpoints.

## Installation

pip install fd-replay

### Running daemon

`fd-replay -c <conffile> -p <pidfile> --logfile <logfile>`

### Running foreground

`fd-replay -f -c <conffile> -p <pidfile> --logfile <logfile>`


