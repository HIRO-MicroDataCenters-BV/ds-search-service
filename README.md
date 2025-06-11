# Data Space Search Service
The Search Service is a service of the Data Space Node, designed to process search queries and aggregate results from decentralized catalogs.

The repository includes an server application in Python with tests, automatically generated OpenAPI file, and an automatically generated client for accessing the server API from third-party applications.

Work on the server and client is conducted in their respective directories: server and client, as the server-side and client-side parts have different dependencies, configurations, etc.

## Requirements
Python 3.10+

## Installation
```bash
pip install pre-commit
pre-commit install
```

## Working on a server
Go to the `/server` folder to install dependencies and work on the server application.  
Documentation on setting up the virtual environment, installing dependencies, and working with the server can be found [here](./server/README.md).

## Working on a client
Go to the `/client` folder to install dependencies and work on the client application.  
Documentation on setting up the virtual environment, installing dependencies, and working with the client can be found [here](./client/README.md).

## Release
The application version is specified in the VERSION file. The version should follow the format a.a.a, where 'a' is a number.  
To create a release, update the version in the VERSION file and add a tag in GIT.  
The release version for branches, pull requests, and tags will be generated based on the base version in the VERSION file.

## GitHub Actions
GitHub Actions triggers testing, builds, and application publishing for each release.  
https://docs.github.com/en/actions  

## Artifacts
* [OpenAPI specification](https://hiro-microdatacenters-bv.github.io/ds-search-service/docs/index.html)
* [Helm charts repository](https://hiro-microdatacenters-bv.github.io/ds-search-service/helm-charts/index.yaml)
* [Docker images repository](https://github.com/hiro-microdatacenters-bv/ds-search-service/pkgs/container/ds-search-service)
* [Python client](https://pypi.org/project/ds-search-service/)

# Collaboration guidelines
HIRO uses and requires from its partners [GitFlow with Forks](https://hirodevops.notion.site/GitFlow-with-Forks-3b737784e4fc40eaa007f04aed49bb2e?pvs=4)
