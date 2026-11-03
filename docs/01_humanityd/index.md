---
content_title: Humanityd
---

## Introduction

`humanityd` is the core service daemon that runs on every Antelope node. It can be configured to process smart contracts, validate transactions, produce blocks containing valid transactions, and confirm blocks to record them on the blockchain.

## Installation

`humanityd` is distributed as part of the [Humanity Pro software suite](https://github.com/TetraGrids/Humanity-Pro). To install `humanityd`, visit the [Humanity Pro Software Installation](../00_install/index.md) section.

## Explore

Navigate the sections below to configure and use `humanityd`.

* [Usage](02_usage/index.md) - Configuring and using `humanityd`, node setups/environments.
* [Plugins](03_plugins/index.md) - Using plugins, plugin options, mandatory vs. optional.
* [Replays](04_replays/index.md) - Replaying the chain from a snapshot or a blocks.log file.
* [RPC APIs](05_rpc_apis/index.md) - Remote Procedure Call API reference for plugin HTTP endpoints.
* [Logging](06_logging/index.md) - Logging config/usage, loggers, appenders, logging levels.
* [Concepts](07_concepts/index.md) - `humanityd` concepts, explainers, implementation aspects.
* [Troubleshooting](08_troubleshooting/index.md) - Common `humanityd` troubleshooting questions.

[[info | Access Node]]
| A local or remote Antelope access node running `humanityd` is required for a client application or smart contract to interact with the blockchain.
