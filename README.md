> **WARNING**: This project is vibe-coded by AI, since I'm in immediate need for such an application.
>
> A more sophisticated, production-ready and human-created version is under development. Do not use this application in production.

# MiniServe

A minimal object storage application. Use Flask for API and NGINX for static serving.

MiniServe is **never** intended to be deployed at large scale. It lacks crucial features such as token limits. Use it for development and side projects only!

## Setup

Currently MiniServe focuses on Podman image deployment. You can extract useful information from `Containerfile` if you want to install it natively.

### Podman Compose (recommended)

Copy and paste content of `conf/compose.example.yml` to a desired location and adjust to to your needs.

`conf/compose.example.yml` contains a full, production-ready MiniServe setup, while NGINX configuration is neither complete nor secure. Use `conf/miniserve.conf` as an example and create NGINX instance tailored to your needs.

## Usage

For safety, API endpoints and static serving are on different domain by default, as seen in `conf/miniserve.conf`, though they can be combined.

Before starting the container, you should set environmental variables:

- `MAX_CONTENT_LENGTH`: Maximum accepted file size, in MB.
- `AUTH_TOKEN`: The token for uploading and deleting files.

Upload:

```bash
# `Bearer` can be omitted
curl -s -X POST \
    -H "Authorization: Bearer $AUTH_TOKEN" \
    -F "file=@test.txt" \
    "$API_ENDPOINT/upload"
```

A new file name is in the response, which is used for hotlink, further API actions, etc.

Delete:

```bash
curl -s -X DELETE \
    -H "Authorization: Bearer $AUTH_TOKEN" \
    "$API_ENDPOINT/delete/<file_name>"
```

Access: `$API_ENDPOINT/<file_name>`

## License

The Unlicense
