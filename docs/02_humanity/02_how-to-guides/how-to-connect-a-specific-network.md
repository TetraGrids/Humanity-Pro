## Goal

Connect to a specific `humanityd` or `humanity-keyd` host to send COMMAND

`humanity` and `humanity-keyd` can connect to a specific node by using the `--url` or `--wallet-url` optional arguments, respectively, followed by the http address and port number these services are listening to.

[[info | Default address:port]]
| If no optional arguments are used (i.e. `--url` or `--wallet-url`), `humanity` attempts to connect to a local `humanityd` or `humanity-keyd` running at localhost `127.0.0.1` and default port `8888`.

## Before you begin

* Install the currently supported version of `humanity`

## Steps
### Connecting to Humanityd

```sh
humanity -url http://humanityd-host:8888 COMMAND
```

### Connecting to humanity-keyd

```sh
humanity --wallet-url http://humanity-keyd-host:8888 COMMAND
```
