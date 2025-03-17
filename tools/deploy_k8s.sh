#!/usr/bin/env bash

set -o errexit
set -o nounset

REPO_NAME="tmp_repo"
CHART_NAME="server"
FULL_CHART_NAME="$REPO_NAME/$CHART_NAME"
RELEASE_NAME="my-server"

get_installed_chart() {
    RESULT=$(kubectl get deployments --show-labels | grep "instance=$RELEASE_NAME" | grep -o "chart=$CHART_NAME-[a-zA-Z0-9\.\-_/]*" | awk -F= '{print $2}')
    echo "${RESULT}"
}

get_latest_chart() {
    RESULT=""
    LATEST_VERSION=$(helm search repo "$FULL_CHART_NAME"  | grep "$FULL_CHART_NAME" | awk '{print $2}')
    if [ -n "$LATEST_VERSION" ]; then
        RESULT="${CHART_NAME}-${LATEST_VERSION}"
    fi
    echo "${RESULT}"
}

main() {
    REPO_URL="$1"

    helm repo add "$REPO_NAME" "$REPO_URL"
    helm repo update "$REPO_NAME"

    INSTALLED_CHART=$(get_installed_chart)
    LATEST_CHART=$(get_latest_chart)

    echo "INSTALLED_CHART=$INSTALLED_CHART"
    echo "LATEST_CHART=$LATEST_CHART"

    if [ -z "$LATEST_CHART" ]; then
        echo "Latest helm chart not found"
        exit 1
    fi

    if [ "$INSTALLED_CHART" != "$LATEST_CHART" ]; then
        helm upgrade --install "$RELEASE_NAME" "$FULL_CHART_NAME"
    else
        echo "The same helm chart. Skip."
    fi
}

main "$@"
