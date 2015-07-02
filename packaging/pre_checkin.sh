#!/bin/bash

# the script takes gcc.spec and creates the gcc-* packages
for arch in armv7l aarch64; do

   echo -n "Building package for $arch --> gcc-$arch ..."

   echo "%define cross $arch" > gcc-${arch}.spec
   echo "%define $arch 1" >> gcc-${arch}.spec
   echo "" >> gcc-${arch}.spec
   cat gcc.spec >> gcc-${arch}.spec
   echo " done."
done

