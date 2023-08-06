###############################################################################
# (c) Copyright 2018 CERN                                                     #
#                                                                             #
# This software is distributed under the terms of the GNU General Public      #
# Licence version 3 (GPL Version 3), copied verbatim in the file "LICENSE".   #
#                                                                             #
# In applying this licence, CERN does not waive the privileges and immunities #
# granted to it by virtue of its status as an Intergovernmental Organization  #
# or submit itself to any jurisdiction.                                       #
###############################################################################
lb-set-platform() {
  export BINARY_TAG="$1"
  export CMTCONFIG="$1"
}
export -f lb-set-platform

LbLogin() {
  if [ "$1" = "-c" ] ; then
    echo "'LbLogin -c' is deprecated, use 'lb-set-platform $2'"
    lb-set-platform "$2"
  else
    echo "error: invalid arguments: only -c option is supported"
    return 1
  fi
}
export -f LbLogin

lb-set-workspace() {
  local old="$CMAKE_PREFIX_PATH"
  if [ -n "$1" ] ; then
    local ws=$(cd "$1" && pwd)
  else
    local ws=
  fi
  export CMAKE_PREFIX_PATH="$ws":$(printenv -0 CMAKE_PREFIX_PATH | tr : \\0 | grep -vzxF "$LBENV_CURRENT_WORKSPACE" | tr \\0 :)
  export CMAKE_PREFIX_PATH=$(printenv CMAKE_PREFIX_PATH | sed 's/^:*//;s/:*$//')
  export LBENV_CURRENT_WORKSPACE="$ws"
  if [ "$CMAKE_PREFIX_PATH" != "$old" ] ; then
    echo "new CMAKE_PREFIX_PATH is:"
    printenv CMAKE_PREFIX_PATH | tr : \\n | sed "s/^/  /"
  else
    echo "no change to CMAKE_PREFIX_PATH needed"
  fi
}
export -f lb-set-workspace

if [ -n "$BASH_VERSION" -a -n "$VIRTUAL_ENV" ] ; then
  lb-enable-shell-completion() {
    source "$VIRTUAL_ENV/share/bash-completion/bash_completion"
  }
  export -f lb-enable-shell-completion
fi
