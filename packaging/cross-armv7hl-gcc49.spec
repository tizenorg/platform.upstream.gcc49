%define pkgname cross-armv7hl-gcc49
%define cross_arch armv7hl
%define gcc_target_arch armv7hl-tizen-linux-gnueabi
%define gcc_icecream 1
#! /bin/sh

#
# call this via pre_checkin.sh
#
# 2005-05-09, jw@suse.de

test -z "$cross_arch" && echo 1>&2 "Error: $0 needs environment variable 'cross_arch'"
test -z "$outfile" && echo 1>&2 "Error: $0 needs environment variable 'outfile'"
cross_arch_cpu=`echo $cross_arch | sed -e 's/\([^-]*\)-\?.*/\1/'`

cat << EOF
#
# spec file for package gcc (Version 4.8.2)
#
# Copyright (c) 2005 SUSE Linux AG, Nuernberg, Germany.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Please submit bugfixes or comments via http://www.suse.de/feedback/
#

%define build_cp 1
%define build_ada 0
%define build_libjava 0
%define build_java 0

%define build_fortran 0
%define build_objc 0
%define build_objcp 0
%define build_go 0
%define gcc_target_arch $cross_arch

%define binutils_target %{cross_arch}
%if %{cross_arch} == "armv7l" || %{cross_arch} == "armv7hl"
%define binutils_target arm
%endif
%if %{cross_arch} == "armv6l" || %{cross_arch} == "armv6hl"
%define binutils_target arm
%endif
%if %{cross_arch} == "armv5tel"
%define binutils_target arm
%endif
%if %{cross_arch} == "aarch64"
%define binutils_target arm
%endif
%define canonical_target %(echo %{binutils_target} | sed -e "s/i.86/i586/;s/ppc/powerpc/;s/sparc64.*/sparc64/;s/sparcv.*/sparc/;")
%if %{binutils_target} == "arm"
%define canonical_target_abi -gnueabi
%endif

%if 0%{?gcc_icecream:1}
%define build_sysroot /
%endif


Name:         %{pkgname}
BuildRequires: cross-%{binutils_target}-binutils
BuildRequires: gcc-c++
BuildRequires: bison
BuildRequires: flex
BuildRequires: gettext-devel
BuildRequires: glibc-devel-32bit
BuildRequires: mpc-devel
BuildRequires: mpfr-devel
BuildRequires: perl
BuildRequires: makeinfo
BuildRequires: zlib-devel
%ifarch %ix86 x86_64 ppc ppc64 s390 s390x ia64 %sparc hppa %arm
BuildRequires: cloog-devel
BuildRequires: ppl-devel
%endif
BuildRequires: cross-$cross_arch_cpu-binutils
%ifarch ia64
BuildRequires: libunwind-devel
%endif
%if 0%{!?gcc_icecream:1}
BuildRequires: cross-%cross_arch-glibc-devel
%endif

%define biarch_targets x86_64 s390x powerpc64 powerpc sparc sparc64

URL:          http://gcc.gnu.org/
Version: 4.9.1
Release:      1
%define gcc_dir_version 4.9
%define binsuffix -4.9
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
Source:		gcc-%{version}.tar.bz2
Source1:	change_spec
Source2:	libffi49-rpmlintrc
Source3:	gcc49-rpmlintrc
Source4:	ecj.jar
Source5:	baselibs.conf
Source6:	libgcj49-rpmlintrc

Group:          Development/Building
Summary:	The GNU C Compiler and Support Files
License:        GPL-3.0+

%description
Core package for the GNU Compiler Collection, including the C language
frontend.

Language frontends other than C are split to different sub-packages,
namely gcc-ada, gcc-c++, gcc-fortran, gcc-java, gcc-objc and
gcc-obj-c++.




# Define the canonical target and host architecture
#   %gcc_target_arch  is supposed to be the full target triple
#   %TARGET_ARCH      is the canonicalized CPU part
#   %CONFIGURE_TARGET is the target triple used for --target=
%if 0%{?gcc_target_arch:1}
%define CONFIGURE_TARGET %{gcc_target_arch}
%define TARGET_ARCH %(echo %{gcc_target_arch} | cut -d - -f 1 | sed -e "s/i.86/i586/;s/ppc/powerpc/;s/sparc64.*/sparc64/;s/sparcv.*/sparc/;")
%if 0%{?gcc_icecream:1} && %{TARGET_ARCH} == "powerpc"
%define CONFIGURE_TARGET powerpc64-tizen-linux
%endif
%if 0%{?gcc_icecream:1} && %{TARGET_ARCH} == "powerpc64"
%define CONFIGURE_TARGET powerpc64-tizen-linux
%endif
%if 0%{?gcc_icecream:1} && %{TARGET_ARCH} == "i586"
%define CONFIGURE_TARGET i586-tizen-linux
%endif
%if 0%{?gcc_icecream:1} && %{TARGET_ARCH} == "aarch64"
%define CONFIGURE_TARGET aarch64-tizen-linux
%endif
%if 0%{?gcc_icecream:1} && %{TARGET_ARCH} == "armv7l"
%define CONFIGURE_TARGET armv7l-tizen-linux-gnueabi
%endif
%if 0%{?gcc_icecream:1} && %{TARGET_ARCH} == "armv7hl"
%define CONFIGURE_TARGET armv7hl-tizen-linux-gnueabi
%endif
%if 0%{?gcc_icecream:1} && %{TARGET_ARCH} == "armv5tel"
%define CONFIGURE_TARGET armv5tel-tizen-linux-gnueabi
%endif
%else
%define TARGET_ARCH %(echo %{_target_cpu} | sed -e "s/i.86/i586/;s/ppc/powerpc/;s/sparc64.*/sparc64/;s/sparcv.*/sparc/;")
%endif
%define biarch %(case " %{biarch_targets} " in (*" %{TARGET_ARCH} "*) echo 1;; (*) echo 0;; esac)

%define HOST_ARCH %(echo %{_host_cpu} | sed -e "s/i.86/i586/;s/ppc/powerpc/;s/sparc64.*/sparc64/;s/sparcv.*/sparc/;")
%ifarch ppc
%define GCCDIST powerpc64-tizen-linux
%else
%ifarch %sparc
%define GCCDIST sparc64-tizen-linux
%else
%ifarch %arm
%define GCCDIST %{HOST_ARCH}-tizen-linux-gnueabi
%else
%define GCCDIST %{HOST_ARCH}-tizen-linux
%endif
%endif
%endif

%define libsubdir %{_libdir}/gcc/%{GCCDIST}/%{gcc_dir_version}
%define gxxinclude %{_prefix}/include/c++/%{gcc_dir_version}


%prep
%setup -q -n gcc-%{version}

# We are configuring ppc as ppc64 but with switched multilibs.  Adjust
# the libstdc++ abi testsuite baseline files accordingly
%ifarch ppc
if [ -d libstdc++-v3/config/abi/post/powerpc64-linux-gnu ]; then
  mkdir -p libstdc++-v3/config/abi/post/powerpc64-linux-gnu/64
  mv libstdc++-v3/config/abi/post/powerpc64-linux-gnu/baseline_symbols.txt \
	libstdc++-v3/config/abi/post/powerpc64-linux-gnu/64/
  mv libstdc++-v3/config/abi/post/powerpc64-linux-gnu/32/baseline_symbols.txt \
	libstdc++-v3/config/abi/post/powerpc64-linux-gnu/
fi
%endif

%build
# Avoid rebuilding of generated files
contrib/gcc_update --touch
# Avoid fucking up testsuite results with Java and indirect dispatch
export LD_AS_NEEDED=0
# Split version file into version used for directories (X.Y) and
# version to report with --version (X.Y.Z).
# See also gcc-dir-version.patch.
# Also decrement the patchlevel version by one if possible and remove
# the 'prerelease' tagging in this case
if test `cat gcc/DEV-PHASE` == "prerelease"; then
  if test `cat gcc/BASE-VER | cut -d '.' -f 3` != "0"; then
    : > gcc/DEV-PHASE
  fi
  ( cat gcc/BASE-VER | cut -d '.' -f 1-2 | tr -d '\n'; echo -n .; cat gcc/BASE-VER | cut -d '.' -f 3 | tr '0123456789' '0012345678' ) > gcc/FULL-VER
else
  mv gcc/BASE-VER gcc/FULL-VER
fi
cat gcc/FULL-VER | cut -d '.' -f 1-2 > gcc/BASE-VER

rm -rf obj-%{GCCDIST}
mkdir obj-%{GCCDIST}
cd obj-%{GCCDIST}
RPM_OPT_FLAGS="$RPM_OPT_FLAGS -U_FORTIFY_SOURCE"
RPM_OPT_FLAGS=`echo $RPM_OPT_FLAGS|sed -e 's/-fno-rtti//g' -e 's/-fno-exceptions//g' -e 's/-Wmissing-format-attribute//g' -e 's/-fstack-protector//g' -e 's/-ffortify=.//g' -e 's/-Wall//g' -e 's/-m32//g' -e 's/-m64//g' -e 's/-fexceptions//'`
%ifarch %ix86
# -mcpu is superceded by -mtune but -mtune is not supported by
# our bootstrap compiler.  -mcpu gives a warning that stops
# the build process, so remove it for now.  Also remove all other
# -march and -mtune flags.  They are superseeded by proper
# default compiler settings now.
RPM_OPT_FLAGS=`echo $RPM_OPT_FLAGS|sed -e 's/-mcpu=i.86//g' -e 's/-march=i.86//g' -e 's/-mtune=i.86//g'`
%endif
%ifarch s390 s390x
RPM_OPT_FLAGS=`echo $RPM_OPT_FLAGS|sed -e 's/-fsigned-char//g'`
RPM_OPT_FLAGS=`echo $RPM_OPT_FLAGS|sed -e 's/-O1/-O2/g'`
%endif
%if 0%{?gcc_target_arch:1} && 0%{!?gcc_icecream:1}
# Kill all -march/tune/cpu because that screws building the target libs
RPM_OPT_FLAGS=`echo $RPM_OPT_FLAGS|sed -e 's/-m\(arch\|tune\|cpu\)=[^ ]*//g'`
%endif
# Replace 2 spaces by one finally
RPM_OPT_FLAGS=`echo $RPM_OPT_FLAGS|sed -e 's/  / /g'`

languages=c
%if %{build_cp}
languages=$languages,c++
%endif
%if %{build_objc}
languages=$languages,objc
%endif
%if %{build_fortran}
languages=$languages,fortran
%endif
%if %{build_objcp}
languages=$languages,obj-c++
%endif
%if %{build_java}
languages=$languages,java
%endif
%if %{build_ada}
languages=$languages,ada
%endif
%if %{build_go}
languages=$languages,go
%endif

J=%{?jobs:%jobs}
if test -z "$J"; then
  J=$(getconf _NPROCESSORS_CONF)
  JL=$(($J * 2))
else
  test 1 -gt "$J" && J=1
  JL=$(($(getconf _NPROCESSORS_CONF)*2))
fi
if test "$J" == "0"; then
  J=1
fi
if test "$JL" == "0"; then
  JL=1
fi
PARALLEL="-j$J -l$JL"

# we don't want some miscompiles in the testsuite, or some fault in
# the compiler to kill the machine.  Hence we limit the amount of memory
# by the physical RAM plus half of swap
#MEM=$(free -m | awk '/^Mem:/ {print $2}')
#SWAP=$(free -m | awk '/^Swap:/ {print $2}')
#ulimit -v $(((MEM + SWAP/2)*1024))

# In general we want to ship release checking enabled compilers
# and run BETA with checking enabled.
#ENABLE_CHECKING="--enable-checking=yes"
ENABLE_CHECKING="--enable-checking=release"

# Work around tail/head -1 changes
export _POSIX2_VERSION=199209

%if %{build_ada}
# Using the host gnatmake like
#   CC="gcc%{hostsuffix}" GNATBIND="gnatbind%{hostsuffix}"
#   GNATMAKE="gnatmake%{hostsuffix}"
# doesn't work due to PR33857, so an un-suffixed gnatmake has to be
# available
mkdir -p host-tools/bin
cp -a /usr/bin/gnatmake%{hostsuffix} host-tools/bin/gnatmake
cp -a /usr/bin/gnatlink%{hostsuffix} host-tools/bin/gnatlink
cp -a /usr/bin/gnatbind%{hostsuffix} host-tools/bin/gnatbind
cp -a /usr/bin/gcc%{hostsuffix} host-tools/bin/gcc
ln -sf /usr/%{_lib} host-tools/%{_lib}
export PATH="`pwd`/host-tools/bin:$PATH"
%endif
#%if 0%{?gcc_target_arch:1} && 0%{!?gcc_icecream:1}
#%else
#	--enable-threads=posix \
#%endif
#	--enable-shared \
%if "%{TARGET_ARCH}" == "armv7l" || "%{TARGET_ARCH}" == "armv7hl"
# temporary workaround for a miscompilation of hash functions in java code
GCJ_EXTRA_FLAGS="-marm"
%endif

export RPM_OPT_FLAGS="`echo $RPM_OPT_FLAGS | sed -e "s/ -Wp,-D_FORTIFY_SOURCE=2 / /g"`"

CFLAGS="$RPM_OPT_FLAGS" CXXFLAGS="$RPM_OPT_FLAGS" XCFLAGS="$RPM_OPT_FLAGS" \
TCFLAGS="$RPM_OPT_FLAGS" GCJFLAGS="$RPM_OPT_FLAGS $GCJ_EXTRA_FLAGS" \
../configure \
	--prefix=%{_prefix} \
	--infodir=%{_infodir} \
	--mandir=%{_mandir} \
	--libdir=%{_libdir} \
	--libexecdir=%{_libdir} \
    --disable-bootstrap \
	--enable-languages=$languages \
	$ENABLE_CHECKING \
	--with-gxx-include-dir=%{_prefix}/include/c++/%{gcc_dir_version} \
	--enable-ssp \
	--disable-libssp \
%if 0%{!?build_libvtv:1}
	--disable-libvtv \
%endif
	--disable-plugin \
	--with-bugurl="http://bugs.tizen.org/" \
	--with-pkgversion="Tizen" \
%if !%{build_fortran}
	--disable-libquadmath \
%endif
%if !%{build_libjava}
        --disable-libgcj \
%else
	--with-java-home=%{_libdir}/jvm/java-1.5.0-gcj%{binsuffix}-1.5.0.0/jre \
	--with-ecj-jar=%{libsubdir}/ecj.jar \
        --disable-java-awt \
%if !%{biarch_libjava}
        --disable-libjava-multilib \
%endif
%endif
	--with-slibdir=/%{_lib} \
	--with-system-zlib \
	--enable-__cxa_atexit \
	--enable-libstdcxx-allocator=new \
	--disable-libstdcxx-pch \
	--enable-version-specific-runtime-libs \
	--enable-linker-build-id \
	--enable-linux-futex \
	--program-suffix=%{binsuffix} \
%if 0%{!?gcc_target_arch:1}
%ifarch ia64
	--with-system-libunwind \
%else
	--without-system-libunwind \
%endif
%endif
%if 0%{?gcc_target_arch:1}
	--program-prefix=%{gcc_target_arch}- \
	--target=%{gcc_target_arch} \
	--disable-nls \
%if 0%{?sysroot:1}
	--with-sysroot=%sysroot \
%else
	--with-sysroot=%{_prefix}/%{gcc_target_arch} \
%endif
%if 0%{?build_sysroot:1}
	--with-build-sysroot=%{build_sysroot} \
%else
%if 0%{?sysroot:1}
	--with-build-sysroot=%{sysroot} \
%else
	--with-build-sysroot=%{_prefix}/%{gcc_target_arch} \
%endif
%endif
%if 0%{?canonical_target:1}
	--with-build-time-tools=/usr/%{canonical_target}-tizen-linux%{?canonical_target_abi:%canonical_target_abi}/bin \
%endif
%if "%{TARGET_ARCH}" == "spu"
	--with-gxx-include-dir=%sysroot/include/c++/%{gcc_dir_version} \
	--with-newlib \
%endif
%endif
%if "%{TARGET_ARCH}" == "armv5tel"
	--with-arch=armv5te \
	--with-float=soft \
	--with-mode=arm \
	--with-abi=aapcs-linux \
	--disable-sjlj-exceptions \
%endif
%if "%{TARGET_ARCH}" == "armv7l" 
	--with-arch=armv7-a \
	--with-tune=cortex-a8 \
	--with-float=softfp \
	--with-fpu=vfpv3 \
	--with-mode=thumb \
	--disable-sjlj-exceptions \
%endif
%if "%{TARGET_ARCH}" == "armv7hl"
	--with-arch=armv7-a \
	--with-tune=cortex-a9 \
	--with-float=hard \
	--with-abi=aapcs-linux \
	--with-fpu=vfpv3-d16 \
	--disable-sjlj-exceptions \
%endif
%if  "%{TARGET_ARCH}" == "aarch64"
	--with-arch=armv8-a \
	--disable-sjlj-exceptions \
%endif
%if "%{TARGET_ARCH}" == "powerpc" || "%{TARGET_ARCH}" == "powerpc64"
%if "%{TARGET_ARCH}" == "powerpc"
        --with-cpu=default32 \
%endif
%if "%{TARGET_ARCH}" == "powerpc64le"
	--with-cpu=power7 \
%else
	--with-cpu-64=power4 \
%endif
	--enable-secureplt \
	--with-long-double-128 \
%if "%{TARGET_ARCH}" == "powerpc64le"
	--disable-multilib \
%endif
%endif
%if "%{TARGET_ARCH}" == "sparc64"
	--with-cpu=ultrasparc \
	--with-long-double-128 \
%endif
%if "%{TARGET_ARCH}" == "sparc"
	--with-cpu=v8 \
	--with-long-double-128 \
%endif
%if "%{TARGET_ARCH}" == "i586"
	--with-arch-32=i586 \
	--with-tune=generic \
%endif
%if "%{TARGET_ARCH}" == "x86_64"
	--with-arch-32=i586 \
	--with-tune=generic \
	--disable-multilib \
%endif
%if "%{TARGET_ARCH}" == "s390"
        --with-tune=zEC12 --with-arch=z196 \
	--with-long-double-128 \
	--enable-decimal-float \
%endif
%if "%{TARGET_ARCH}" == "s390x"
        --with-tune=zEC12 --with-arch=z196 \
	--with-long-double-128 \
	--enable-decimal-float \
%endif
%if "%{TARGET_ARCH}" == "m68k"
	--disable-multilib \
%endif
	--build=%{GCCDIST} \
	--host=%{GCCDIST}


%if 0%{!?gcc_icecream:1}
make %{?jobs:-j%jobs}
%else
make %{?jobs:-j%jobs} all-host
%endif

%define _prefix /opt/cross

%package -n cross-%cross_arch-gcc49-icecream-backend
Summary: Icecream backend for the GNU C Compiler
Group:	Development/Languages/C and C++

%description -n cross-%cross_arch-gcc49-icecream-backend
This package contains the icecream environment for the GNU C Compiler


%define targetlibsubdir %{_libdir}/gcc/%{gcc_target_arch}/%{gcc_dir_version}

%install
cd obj-%{GCCDIST}

# install and fixup host parts
make DESTDIR=$RPM_BUILD_ROOT install-host
# with the present setup fixincludes are for the build includes which
# is wrong - get rid of them
rm -rf $RPM_BUILD_ROOT/%{targetlibsubdir}/include-fixed
rm -f $RPM_BUILD_ROOT/%{targetlibsubdir}/liblto_plugin.la
# common fixup
rm -f $RPM_BUILD_ROOT%{_libdir}/libiberty.a
# remove docs
rm -rf $RPM_BUILD_ROOT%{_mandir}
rm -rf $RPM_BUILD_ROOT%{_infodir}


# install and fixup target parts
# ???  don't do this - debugedit is not prepared for this and crashes
# so expect the sysroot to be populated from natively built binaries
#%if 0%{?sysroot:1}
#make DESTDIR=$RPM_BUILD_ROOT/%{sysroot} install-target
#%else
#make DESTDIR=$RPM_BUILD_ROOT/%{_prefix}/%{gcc_target_arch} install-target
#%endif


# Build an icecream environment
# The assembler comes from the cross-binutils, and hence is _not_
# named funnily, not even on ppc, so there we need the original target
install -s -D %{_prefix}/bin/%{canonical_target}-tizen-linux%{?canonical_target_abi:%canonical_target_abi}-as \
	$RPM_BUILD_ROOT/env/usr/bin/as
install -s $RPM_BUILD_ROOT/%{_prefix}/bin/%{gcc_target_arch}-g++%{binsuffix} \
	$RPM_BUILD_ROOT/env/usr/bin/g++
install -s $RPM_BUILD_ROOT/%{_prefix}/bin/%{gcc_target_arch}-gcc%{binsuffix} \
	$RPM_BUILD_ROOT/env/usr/bin/gcc

for back in cc1 cc1plus; do 
	install -s -D $RPM_BUILD_ROOT/%{targetlibsubdir}/$back \
		$RPM_BUILD_ROOT/env%{targetlibsubdir}/$back
done
if test -f $RPM_BUILD_ROOT/%{targetlibsubdir}/liblto_plugin.so; then
  install -s -D $RPM_BUILD_ROOT/%{targetlibsubdir}/liblto_plugin.so \
		$RPM_BUILD_ROOT/env%{targetlibsubdir}/liblto_plugin.so
fi

# Make sure to also pull in all shared library requirements for the
# binaries we put into the environment which is operated by chrooting
# into it and execing the compiler
libs=`for bin in $RPM_BUILD_ROOT/env/usr/bin/* $RPM_BUILD_ROOT/env%{targetlibsubdir}/*; do \
  ldd $bin | sed -n '\,^[^/]*\(/[^ ]*\).*,{ s//\1/; p; }'  ;\
done | sort -u `
for lib in $libs; do
  # Check wether the same library also exists in the parent directory,
  # and prefer that on the assumption that it is a more generic one.
  baselib=`echo "$lib" | sed 's,/[^/]*\(/[^/]*\)$,\1,'`
  test -f "$baselib" && lib=$baselib
  install -s -D $lib $RPM_BUILD_ROOT/env$lib
done

cd $RPM_BUILD_ROOT/env
tar cvzf ../%{name}_%{_arch}.tar.gz *
cd ..
mkdir -p usr/share/icecream-envs
mv %{name}_%{_arch}.tar.gz usr/share/icecream-envs
rpm -q --changelog glibc >  usr/share/icecream-envs/%{name}_%{_arch}.glibc
rpm -q --changelog binutils >  usr/share/icecream-envs/%{name}_%{_arch}.binutils
rm -r env

%files
%defattr(-,root,root)
%{_prefix}/bin
%dir %{targetlibsubdir}
%dir %{_libdir}/gcc/%{gcc_target_arch}
%{targetlibsubdir}

%files -n cross-%cross_arch-gcc49-icecream-backend
%defattr(-,root,root)
/usr/share/icecream-envs

EOF
