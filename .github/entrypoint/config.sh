#!/bin/sh

setup_config() {
	# pinned repos
	# https://stackoverflow.com/a/43358500/4058484
	curl -s -X POST "${GITHUB_GRAPHQL_URL}" -H "Authorization: bearer $TOKEN" --data-raw '{"query":"{\n  user(login: \"'${GITHUB_REPOSITORY_OWNER}'\") {\n pinnedItems(first: 6, types: REPOSITORY) {\n nodes {\n ... on Repository {\n name\n }\n }\n }\n }\n}"' | jq --raw-output '.data.user.pinnedItems' | yq eval -P | sed "s/name: //g" > nodes.yaml

	for i in 0 1 2 3 4 5
	do
	   j=$(($i+1))
	   NAME=$(yq eval ".nodes[$i]" nodes.yaml)
	   [ -z "${GITHUB_REPOSITORY##*$NAME*}" ] && TARGET=$(yq eval ".nodes[$j]" nodes.yaml)
	done

	rm nodes.yaml
	rm -Rf -- */ && mv /maps/text/_* .
	REPOSITORY=${GITHUB_REPOSITORY_OWNER}/${TARGET}
	[ "${REPOSITORY}" == "eq19/eq19.github.io" ] && mv /maps/assets .

	sed -i "1s|^|target_repository: $REPOSITORY\n|" ${JEKYLL_CFG}
	sed -i "1s|^|repository: $GITHUB_REPOSITORY\n|" ${JEKYLL_CFG}
}
