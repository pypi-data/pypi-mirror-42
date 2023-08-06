#!/usr/bin/printf you must "source %s"\n
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
if [ -z "$LBENV_SOURCED" ] ; then
  _host_os=$(%target_dir%/bin/host_os)

  if [ -e %lbenv_root%/$_host_os/bin/activate ] ; then
    source %lbenv_root%/$_host_os/bin/activate
    eval $(python -m LbEnv --sh --siteroot %siteroot% "$@" || echo deactivate)
  else
    echo "Platform not supported ($_host_os)"
  fi
  unset _host_os
else
  if [ -n "$LBENV_ALIASES" ] ; then
    source "$LBENV_ALIASES"
  fi
fi
