#!/bin/bash

# 1. Authenticate
token=$(curl -s -H "Content-Type: application/json" -X POST \
  -d "{\"username\": \"$HUB_USERNAME\", \"password\": \"$HUB_PASSWORD\"}" \
  https://hub.docker.com/v2/users/login/ | jq -r .token)
[ -z "$token" ] && { echo "❌ Auth failed"; exit 1; }

# 2. Get manifests with tags
response=$(curl -s -H "Authorization: JWT $token" \
  "https://hub.docker.com/v2/repositories/$IMAGE_NAME/tags/?page_size=$MAX_DELETIONS&ordering=last_updated")

# 3. Process deletions
deleted=0
echo "$response" | jq -c '.results[]' | while read -r item; do
  tag=$(echo "$item" | jq -r '.name')
  digest=$(echo "$item" | jq -r '.images[0].digest')
  
  echo "Processing ${digest:7:12}..."
  
  # Delete tag first (if not latest)
  if [ "$tag" != "null" ] && [ "$tag" != "latest" ]; then
    echo "  🏷️ Deleting tag: $tag"
    curl -s -o /dev/null -X DELETE \
      -H "Authorization: JWT $token" \
      "https://hub.docker.com/v2/namespaces/${IMAGE_NAME%/*}/repositories/${IMAGE_NAME#*/}/tags/$tag"
  fi
  
  # Delete the actual image manifest
  echo "  🖼️ Deleting image manifest..."
  status=$(curl -s -o /dev/null -w "%{http_code}" -X DELETE \
    -H "Authorization: JWT $token" \
    -H "Accept: application/vnd.docker.distribution.manifest.v2+json" \
    "https://hub.docker.com/v2/repositories/$IMAGE_NAME/manifests/$digest")
  
  if [ "$status" -eq 202 ]; then
    ((deleted++))
    echo "  ✅ Deleted successfully"
  else
    echo "  ❌ Failed to delete image (HTTP $status)"
  fi
  
  sleep 2
  [ $deleted -ge $MAX_DELETIONS ] && break
done

echo "Result: Deleted $deleted images (tags AND manifests)"
