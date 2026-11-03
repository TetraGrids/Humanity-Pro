---
content_title: Humanity Troubleshooting
---

## Cannot connect to RPC endpoint

Check if your local `humanityd` is running by visiting the following URL in your browser:

```sh
curl http://localhost:8888/v1/chain/get_info
```

If you are trying to connect a remote `humanityd` API endpoint, try to visit the API endpoint with the following suffix:

```sh
http://API_ENDPOINT:PORT/v1/chain/get_info
```

Replace API_ENDPOINT and PORT with your remote `humanityd` API endpoint detail

## "Missing Authorizations"

That means you are not using the required authorizations. Most likely you are not using correct Antelope account or permission level to sign the transaction
