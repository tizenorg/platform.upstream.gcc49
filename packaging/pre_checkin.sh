#!/bin/bash
# This script is called automatically during autobuild checkin.
case $0 in
  \./*)
    here=$PWD
    ;;
  */*)
    here=${0%/*}
    ;;
  *)
    here=$PWD
    ;;
esac
_here=$here
# remove packaging/
_here=${here/\/packaging/}
case ${_here##*/} in
  gcc-*)
    suffix=${_here##*/}
    set ${suffix#*-}-
    ;;
  gcc[0-9]*)
    suffix=${_here##*/}
    set ${suffix#gcc}
    ;;
esac
. ${here}/change_spec
