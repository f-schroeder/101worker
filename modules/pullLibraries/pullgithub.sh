#!/bin/bash
USAGE="$0 <githubrepository> <absoluteTargetDirectory>"
GITHUB_REPOSITORY=${1?$USAGE}
TARGET_DIRECTORY=${2?$USAGE}
CURRENT_DIRECTORY=`pwd`
echo "  pullgithub.sh $1 $2"


#----- clone the repository in target dir if not already present
if [ -d "${TARGET_DIRECTORY?}/.git" ]
then
  echo "    Directory ${TARGET_DIRECTORY?}/.git exist. "
else
  echo "    Directory ${TARGET_DIRECTORY?}/.git does not exist."
  echo "    Cloning ${GITHUB_REPOSITORY?}"
  git clone https://github.com/${GITHUB_REPOSITORY?} ${TARGET_DIRECTORY?}
  echo "    clone done"
fi

#----- pull the repository
# get back to the directory where the script was before. 
# this is necessary as the target directory might be relative. 
cd ${TARGET_DIRECTORY?}
echo "    pulling ${GITHUB_REPOSITORY?} into ${TARGET_DIRECTORY?}"
git pull 
echo "    done"
