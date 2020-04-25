#!/bin/bash

cmd=`which quicktype`
if [ "$cmd" == "" ]; then
  npm i -g quicktype
fi

# v1
targets="groups:Groups group:Group users:Users user:User service_provider_configs:ServiceProviderConfigs"
for target in $targets
do
  t=(${target//:/ })
  cat json-schema/v1/${t[1]}.json | quicktype \
    --all-properties-optional \
    --src-lang schema \
    --lang python \
    --python-version=3.6 \
    --nice-property-names \
    -t ${t[1]} \
    -o src/slack_scim/v1/${t[0]}.py
done
