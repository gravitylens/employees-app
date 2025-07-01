Self-signed certificates for the web UI. Replace with real certificates as needed.
Generate with:

```
openssl req -x509 -newkey rsa:2048 -days 365 -nodes -keyout server-key.pem -out server-cert.pem -subj "/CN=web.local"
```
