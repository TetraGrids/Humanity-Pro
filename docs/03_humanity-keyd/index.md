---
content_title: humanity-keyd
---

## Introduction

`humanity-keyd` is a key manager service daemon for storing private keys and signing digital messages. It provides a secure key storage medium for keys to be encrypted at rest in the associated wallet file. `humanity-keyd` also defines a secure enclave for signing transaction created by `humanity` or a third part library.

## Installation

`humanity-keyd` is distributed as part of the [Humanity Pro software suite](https://github.com/TetraGrids/Humanity-Pro). To install `humanity-keyd` just visit the [Humanity Pro Software Installation](../00_install/index.md) section.

## Operation

When a wallet is unlocked with the corresponding password, `humanity` can request `humanity-keyd` to sign a transaction with the appropriate private keys. Also, `humanity-keyd` provides support for hardware-based wallets such as Secure Encalve and YubiHSM.

[[info | Audience]]
| `humanity-keyd` is intended to be used by Antelope developers only.
