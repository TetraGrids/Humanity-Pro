---
content_title: humanity-keyd Troubleshooting
---

## How to solve the error "Failed to lock access to wallet directory; is another `humanity-keyd` running"?

Since `humanity` may auto-launch an instance of `humanity-keyd`, it is possible to end up with multiple instances of `humanity-keyd` running. That can cause unexpected behavior or the error message above.

To fix this issue, you can terminate all running `humanity-keyd` instances and restart `humanity-keyd`. The following command will find and terminate all instances of `humanity-keyd` running on the system:

```sh
pkill humanity-keyd
```
