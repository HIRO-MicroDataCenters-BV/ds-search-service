# Server application

## Requirements
* Python 3.10+
* [Data Space Catalog](https://github.com/HIRO-MicroDataCenters-BV/ds-catalog)

## Installation
1. If you don't have `Poetry` installed run:
```bash
pip install poetry
```

2. Install dependencies:
```bash
poetry config virtualenvs.in-project true
poetry install --no-root --with dev,test
```

3. Launch the project:
```bash
poetry run uvicorn app.main:app --reload
```
or do it in two steps:
```bash
poetry shell
uvicorn app.main:app
```

4. Running tests:
```bash
poetry run pytest
```

## Deployment
1. Label the nodes:
```bash
kubectl label nodes <node> node-id=node1
kubectl label nodes <node> node-id=node2
kubectl label nodes <node> node-id=node3
```
2. Define ingress.host and ingress.nodes in values.yaml:
```bash
ingress:
  host: nextgen.hiro-develop.nl
  nodes:
    - nodeId: node1
    - nodeId: node2
    - nodeId: node3
```
3. Deploy the Helm chart:
```bash
helm repo add ds-search-repo https://hiro-microdatacenters-bv.github.io/ds-search-service/helm-charts/
helm repo update ds-search-repo
helm install ds-search ds-search-repo/server -f values.yaml
```
4. The search service will be available at:
   * https://ds-search.node1.nextgen.hiro-develop.nl
   * https://ds-search.node2.nextgen.hiro-develop.nl
   * https://ds-search.node3.nextgen.hiro-develop.nl

## Prometheus metrics
The application includes prometheus-fastapi-instrumentator for monitoring performance and analyzing its operation. It automatically adds an endpoint `/metrics` where you can access application metrics for Prometheus. These metrics include information about request counts, request execution times, and other important indicators of application performance.
More on that at [Prometheus FastAPI Instrumentator](https://github.com/trallnag/prometheus-fastapi-instrumentator)
