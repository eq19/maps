#!/bin/bash

# GitHub Personal Access Token (PAT) - Store securely
GITHUB_PAT="$3"

# GitHub API Base URL
GITHUB_API="https://api.github.com"

# Function to get the public key for a repository (needed for encrypting secrets)
get_public_key() {
    local repo=$1
    curl -s -H "Authorization: token $GITHUB_PAT" -H "Accept: application/vnd.github.v3+json" \
        "$GITHUB_API/repos/$repo/actions/secrets/public-key"
}

# Function to check if a secret exists in a repository
check_secret_exists() {
    local repo=$1
    local secret_name=$2
    curl -s -o /dev/null -w "%{http_code}" -H "Authorization: token $GITHUB_PAT" \
        -H "Accept: application/vnd.github.v3+json" "$GITHUB_API/repos/$repo/actions/secrets/$secret_name"
}

# Function to set a secret in a repository
set_secret() {
    local repo=$1
    local secret_name=$2
    local secret_value=$3

    # Get public key for encryption
    response=$(get_public_key "$repo")
    key_id=$(echo "$response" | jq -r '.key_id')
    key_value=$(echo "$response" | jq -r '.key')

    if [[ "$key_id" == "null" ]]; then
        echo "❌ Failed to retrieve public key for $repo"
        return
    fi

    # Encrypt secret value using openssl
    encrypted_value=$(echo -n "$secret_value" | openssl enc -base64 | tr -d '\n')

    # Set the secret
    curl -s -X PUT -H "Authorization: token $GITHUB_PAT" \
        -H "Accept: application/vnd.github.v3+json" \
        -d "{\"encrypted_value\":\"$encrypted_value\",\"key_id\":\"$key_id\"}" \
        "$GITHUB_API/repos/$repo/actions/secrets/$secret_name"
}

# Function to check if a variable exists in a repository
check_variable_exists() {
    local repo=$1
    local var_name=$2
    response=$(curl -s -H "Authorization: token $GITHUB_PAT" \
        -H "Accept: application/vnd.github.v3+json" "$GITHUB_API/repos/$repo/actions/variables")

    echo "$response" | jq -e ".variables[] | select(.name == \"$var_name\")" > /dev/null 2>&1
    return $?
}

# Function to set a variable in a repository
set_variable() {
    local repo=$1
    local var_name=$2
    local var_value=$3

    curl -s -X POST -H "Authorization: token $GITHUB_PAT" \
        -H "Accept: application/vnd.github.v3+json" \
        -d "{\"name\":\"$var_name\",\"value\":\"$var_value\"}" \
        "$GITHUB_API/repos/$repo/actions/variables"
}

# Main function to sync secrets and variables from one repo to another
sync_secrets_and_variables() {
    local source_repo=$1
    local target_repo=$2

    echo "🔄 Syncing secrets from $source_repo to $target_repo..."
    
    # Get all secrets from source repository
    secrets=$(curl -s -H "Authorization: token $GITHUB_PAT" \
        -H "Accept: application/vnd.github.v3+json" "$GITHUB_API/repos/$source_repo/actions/secrets" | jq -r '.secrets[].name')

    for secret in $secrets; do
        if [[ "$(check_secret_exists "$target_repo" "$secret")" == "404" ]]; then
            echo "➕ Secret '$secret' does not exist in $target_repo. Copying..."
            secret_value=$(curl -s -H "Authorization: token $GITHUB_PAT" \
                -H "Accept: application/vnd.github.v3+json" "$GITHUB_API/repos/$source_repo/actions/secrets/$secret" | jq -r '.value')
            set_secret "$target_repo" "$secret" "$secret_value"
        else
            echo "✅ Secret '$secret' already exists in $target_repo."
        fi
    done

    echo "🔄 Syncing variables from $source_repo to $target_repo..."
    
    # Get all variables from source repository
    variables=$(curl -s -H "Authorization: token $GITHUB_PAT" \
        -H "Accept: application/vnd.github.v3+json" "$GITHUB_API/repos/$source_repo/actions/variables" | jq -r '.variables[].name')

    for var in $variables; do
        if ! check_variable_exists "$target_repo" "$var"; then
            echo "➕ Variable '$var' does not exist in $target_repo. Copying..."
            var_value=$(curl -s -H "Authorization: token $GITHUB_PAT" \
                -H "Accept: application/vnd.github.v3+json" "$GITHUB_API/repos/$source_repo/actions/variables/$var" | jq -r '.value')
            set_variable "$target_repo" "$var" "$var_value"
        else
            echo "✅ Variable '$var' already exists in $target_repo."
        fi
    done

    echo "✅ Sync complete!"
}

# Check for required arguments
if [[ $# -ne 3 ]]; then
    echo "Usage: $0 <source_repo> <target_repo> <github_pat>"
    exit 1
fi

# Run the sync function
sync_secrets_and_variables "$1" "$2"
