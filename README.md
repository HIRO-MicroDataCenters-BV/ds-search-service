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

You can set up automatic testing in GitHub Actions for different versions of Python. To do this, you need to specify the set of versions in the `.github/workflows/client.yaml` or `.github/workflows/server.yaml file`. For example:
```yaml
strategy:
  matrix:
    python-version: ["3.10", "3.11", "3.12"]
```

During the build and publish process, a Docker image is built, a Helm chart is created, an openapi.yaml is generated, and the web service is deployed to a Kubernetes cluster.

**Initial setup**  
1. Create the branch gh-pages and use it as a GitHub page https://pages.github.com/.  
2. Set up variables at `https://github.com/hiro-microdatacenters-bv/ds-search-service/settings/variables/actions`:
- `DOCKER_IMAGE_NAME` - The name of the Docker image for uploading to the repository.
3. Set up secrets at `https://github.com/hiro-microdatacenters-bv/ds-search-service/settings/secrets/actions`:
- `AWS_ACCESS_KEY_ID` - AWS Access Key ID. https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html
- `AWS_SECRET_ACCESS_KEY` - AWS Secret Access Key
- `AWS_REGION` - AWS region. https://aws.amazon.com/about-aws/global-infrastructure/regions_az/
- `EKS_CLUSTER_ROLE_ARN` - The IAM role's ARN in AWS, providing permissions for managing an Amazon EKS Kubernetes cluster.
- `EKS_CLUSTER_NAME` - Amazon EKS Kubernetes cluster name.
- `EKS_CLUSTER_NAMESPACE` - Amazon EKS Kubernetes cluster namespace.
- `HELM_REPO_URL` - `https://hiro-microdatacenters-bv.github.io/ds-search-service/helm-charts/`
- `PYPI_TOKEN` - The secret token for PyPI. https://pypi.org/help/#apitoken

**After execution**  
The index.yaml file containing the list of Helm charts will be available at `https://hiro-microdatacenters-bv.github.io/ds-search-service/helm-charts/index.yaml`. You can this URL on https://artifacthub.io/.  
A package of the client will be available at pypi.org.  
The Docker image will be available at `https://github.com/hiro-microdatacenters-bv/ds-search-service/pkgs/container/ds-search-service`.

## Act
You can run your GitHub Actions locally using https://github.com/nektos/act. 

Usage example:
```bash
act push -j test_and_build_client --secret-file my.secrets
```

# Collaboration guidelines
HIRO uses and requires from its partners [GitFlow with Forks](https://hirodevops.notion.site/GitFlow-with-Forks-3b737784e4fc40eaa007f04aed49bb2e?pvs=4)
