#!/usr/bin/env bash

GH_USER=avawal
GH_PATH=`cat ~/.ghtoken`
GH_REPO=test_release
GH_TARGET=master
ASSETS_PATH=build
#<run some build command>
VERSION=`grep '"version":' version.json | cut -d\" -f4` 

git add -u
git commit -m "$VERSION release"
git push

content=`cat mppv2_artifact.json` 
res=`curl --user "$GH_USER:$GH_PATH" -X POST https://api.github.com/repos/${GH_USER}/${GH_REPO}/releases \
-d "
{
  \"tag_name\": \"v$VERSION\",
  \"target_commitish\": \"$GH_TARGET\",
  \"name\": \"v$VERSION\",
  \"body\":  $content  ,
  \"draft\": false,
  \"prerelease\": false
}"`
echo Create release result: ${res}
rel_id=`echo ${res} | python -c 'import json,sys;print(json.load(sys.stdin)["id"])'`
file_name=yourproj-${VERSION}.ext

curl --user "$GH_USER:$GH_PATH" -X POST https://uploads.github.com/repos/${GH_USER}/${GH_REPO}/releases/${rel_id}/assets?name=${file_name}\
 --header 'Content-Type: text/javascript ' --upload-file ${ASSETS_PATH}/${file_name}

rm ${ASSETS_PATH}/${file_name}
