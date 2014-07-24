%define building_libffi 1
#
# spec file for package gcc49
#
# Copyright (c) 2009 SUSE LINUX Products GmbH, Nuernberg, Germany.
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via http://bugs.opensuse.org/
#

# norootforbuild
# icecream 0


%define build_ada 0

%define quadmath_arch %ix86 x86_64 ia64 aarch64
%define tsan_arch x86_64
%define asan_arch x86_64 %ix86 ppc ppc64 %sparc %arm
%define itm_arch x86_64 %ix86 %arm ppc ppc64 ppc64le s390 s390x %sparc
%define atomic_arch x86_64 %ix86 %arm aarch64 ppc ppc64 ppc64le s390 s390x %sparc m68k
%define lsan_arch x86_64
%define ubsan_arch x86_64 %ix86 ppc ppc64 %arm
%if 0%{?build_libvtv:1}
%define vtv_arch x86_64 %ix86
%endif
%define cilkrts_arch x86_64 %ix86

# We don't want to build java
%define build_java 0
%define build_libjava 0

%define build_cp 1
%define build_fortran !0%{?building_libjava:1}%{?building_libffi:1}
%define build_objc !0%{?building_libjava:1}%{?building_libffi:1}
%define build_objcp !0%{?building_libjava:1}%{?building_libffi:1}
%define build_go !0%{?building_libjava:1}%{?building_libffi:1}

%if %{build_objcp}
%define build_cp 1
%define build_objc 1
%endif

%if %{build_libjava}
%define build_cp 1
%endif

# For optional compilers only build C, C++ and Fortran
%if 0%{?build_optional_compiler_languages:1}
%define build_ada 0
%define build_java 0
%define build_libjava 0
%define build_objc 0
%define build_objcp 0
%define build_go 0
%endif

# Shared library SONAME versions
%ifarch hppa
%define libgcc_s 4
%else
%ifarch m68k
%define libgcc_s 2
%else
%define libgcc_s 1
%endif
%endif
%define libgcj_sover %{nil}
%define libgcj_bc_sover %{nil}
%define libffi_sover %{nil}
%define libgomp_sover %{nil}
%define libstdcxx_sover %{nil}
%define libobjc_sover %{nil}
%define libgfortran_sover %{nil}
%define libquadmath_sover %{nil}
%define libasan_sover %{nil}
%define libtsan_sover %{nil}
%define libatomic_sover %{nil}
%define libitm_sover %{nil}
%define libubsan_sover %{nil}
%define liblsan_sover %{nil}
%define libvtv_sover %{nil}
%define libcilkrts_sover %{nil}
%define libgo_sover %{nil}

# Shared library package suffix
# This is used for the "non-standard" set of libraries, the standard
# being defined by %product_libs_gcc_ver, the GCC version that should
# provide un-suffixed shared library packages following the shared-library
# policy.  Even suffixed variants should provide the shared-library policy
# mandated names and ensure they conflict with each other.
# Note that on SONAME changes of any library the %product_libs_gcc_ver
# define needs to be either split or the newest GCC version still providing
# the old SONAME needs to unconditionally produce an un-suffixed library
# if %product_libs_gcc_ver is newer than it.  Similar the _oldest_ GCC
# version first providing a new SONAME needs to unconditionally produce
# an un-suffixed library if %product_libs_gcc_ver is lower that it.
%if %{!?product_libs_gcc_ver:49}%{?product_libs_gcc_ver} != 49
%define pne 1
%endif
%define libgcc_s_suffix %{?pne:-gcc49}
# libgcj SONAME changes with every GCC version
%define libgcj_suffix %nil
%define libgcj_bc_suffix %{?pne:-gcc49}
%define libffi_suffix %{?pne:-gcc49}
%define libgomp_suffix %{?pne:-gcc49}
%define libstdcxx_suffix %{?pne:-gcc49}
%define libobjc_suffix %{?pne:-gcc49}
%define libgfortran_suffix %{?pne:-gcc49}
%define libquadmath_suffix %{?pne:-gcc49}
%define libasan_suffix %{?pne:-gcc49}
%define libtsan_suffix %{?pne:-gcc49}
%define libatomic_suffix %{?pne:-gcc49}
%define libitm_suffix %{?pne:-gcc49}


%define libubsan_suffix %{?pne:-gcc49}
%define liblsan_suffix %{?pne:-gcc49}
%define libvtv_suffix %{?pne:-gcc49}
%define libcilkrts_suffix %{?pne:-gcc49}
%define libgo_suffix %{?pne:-gcc49}

%define selfconflict() %1

Name: libffi49
# With generated files in src we could drop the following
BuildRequires: bison
BuildRequires: flex
BuildRequires: gettext-devel
BuildRequires: makeinfo
# until here, but at least renaming and patching info files breaks this
BuildRequires: gcc-c++
BuildRequires: glibc-devel-32bit
BuildRequires: mpc-devel
BuildRequires: mpfr-devel
BuildRequires: perl
BuildRequires: zlib-devel
%ifarch %ix86 x86_64 ppc ppc64 s390 s390x ia64 %sparc hppa %arm aarch64
BuildRequires: cloog-isl-devel
BuildRequires: isl-devel
%endif
%if %{build_ada}
%define hostsuffix -4.9
BuildRequires: gcc49-ada
%endif
%if 0%{?building_libjava:1}%{?building_testsuite:1}
BuildRequires: fastjar
%endif
%if 0%{?building_libffi:1}
BuildRequires: pkg-config
%endif
%ifarch ia64
BuildRequires: libunwind-devel
%endif
%if 0%{?run_tests:1}
BuildRequires: dejagnu
BuildRequires: expect
BuildRequires: gdb
%endif

%define separate_bi32 0
%define separate_bi64 0
%ifarch ppc sparcv9
# Beware, this does _not_ separate libgcj, as for that one multilibing
# is inactive for the time being
%define separate_bi64 1
%endif
%ifarch x86_64 s390x ppc64 sparc64
%define separate_bi32 1
%endif

# Define two macros to trigger -32bit or -64bit package variants
%define separate_biarch 0
%if %{separate_bi32}
%define separate_biarch 1
%define separate_biarch_suffix -32bit
%endif
%if %{separate_bi64}
%define separate_biarch 1
%define separate_biarch_suffix -64bit
%endif

%ifarch x86_64 ia64 s390x alpha ppc64 sparc64 aarch64
# 64-bit is primary build target
%define build_primary_64bit 1
%else
%define build_primary_64bit 0
%endif

%define biarch_libjava 0

%define biarch_targets x86_64 s390x powerpc64 powerpc sparc sparc64

URL:          http://gcc.gnu.org/
Version: 4.9.1
Release:      1
%define gcc_dir_version 4.9
%define binsuffix -4.9

%if !0%{?building_libjava:1}%{?building_libffi:1}%{?building_testsuite:1}
Requires: binutils glibc-devel
Requires: cpp49 = %{version}-%{release}
Requires: libgcc_s%{libgcc_s} >= %{version}-%{release}
Requires: libgomp%{libgomp_sover} >= %{version}-%{release}
%ifarch %asan_arch
Requires: libasan%{libasan_sover} >= %{version}-%{release}
%endif
%ifarch %tsan_arch
Requires: libtsan%{libtsan_sover} >= %{version}-%{release}
%endif
%ifarch %atomic_arch
Requires: libatomic%{libatomic_sover} >= %{version}-%{release}
%endif
%ifarch %itm_arch
Requires: libitm%{libitm_sover} >= %{version}-%{release}
%endif
%ifarch %cilkrts_arch
Requires: libcilkrts%{libcilkrts_sover} >= %{version}-%{release}
%endif
%ifarch %lsan_arch
Requires: liblsan%{liblsan_sover} >= %{version}-%{release}
%endif
%ifarch %ubsan_arch
Requires: libubsan%{libubsan_sover} >= %{version}-%{release}
%endif
%ifarch %vtv_arch
Requires: libvtv%{libvtv_sover} >= %{version}-%{release}
%endif
Suggests: gcc49-info gcc49-locale
%endif

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
%package -n libffi%{libffi_sover}%{libffi_suffix}
Summary:      Foreign Function Interface library
License:        BSD-3-Clause
Group:        Development/Building
Provides:	libffi%{libffi_sover} = %{version}-%{release}

%description -n libffi%{libffi_sover}%{libffi_suffix}
A foreign function interface is the popular name for the interface that allows code written in one language to call code written in another language.

%post -n libffi%{libffi_sover}%{libffi_suffix} -p /sbin/ldconfig

%postun -n libffi%{libffi_sover}%{libffi_suffix} -p /sbin/ldconfig
%package -n libffi%{libffi_sover}%{libffi_suffix}-32bit
Summary:      Foreign Function Interface library
License:        BSD-3-Clause
Group:        Development/Building
Provides:	libffi%{libffi_sover}-32bit = %{version}-%{release}

%description -n libffi%{libffi_sover}%{libffi_suffix}-32bit
A foreign function interface is the popular name for the interface that allows code written in one language to call code written in another language.

%post -n libffi%{libffi_sover}%{libffi_suffix}-32bit -p /sbin/ldconfig

%postun -n libffi%{libffi_sover}%{libffi_suffix}-32bit -p /sbin/ldconfig
%package -n libffi%{libffi_sover}%{libffi_suffix}-64bit
Summary:      Foreign Function Interface library
License:        BSD-3-Clause
Group:        Development/Building
Provides:	libffi%{libffi_sover}-64bit = %{version}-%{release}

%description -n libffi%{libffi_sover}%{libffi_suffix}-64bit
A foreign function interface is the popular name for the interface that allows code written in one language to call code written in another language.

%post -n libffi%{libffi_sover}%{libffi_suffix}-64bit -p /sbin/ldconfig

%postun -n libffi%{libffi_sover}%{libffi_suffix}-64bit -p /sbin/ldconfig

%package -n libffi49-devel
Summary:      Foreign Function Interface library development files
License:        BSD 3-Clause
Group:        Development/Building
Requires: libffi%{libffi_sover} >= %{version}-%{release}
Provides: libffi-devel = %{version}-%{release}

%description -n libffi49-devel
A foreign function interface is the popular name for the interface that allows code written in one language to call code written in another language.
%package -n libffi49-devel-32bit
Summary:      Foreign Function Interface library development files
License:        BSD 3-Clause
Group:        Development/Building
Requires: libffi%{libffi_sover}-32bit >= %{version}-%{release}
Provides: libffi-devel-32bit = %{version}-%{release}

%description -n libffi49-devel-32bit
A foreign function interface is the popular name for the interface that allows code written in one language to call code written in another language.
%package -n libffi49-devel-64bit
Summary:      Foreign Function Interface library development files
License:        BSD 3-Clause
Group:        Development/Building
Requires: libffi%{libffi_sover}-64bit >= %{version}-%{release}
Provides: libffi-devel-64bit = %{version}-%{release}

%description -n libffi49-devel-64bit
A foreign function interface is the popular name for the interface that allows code written in one language to call code written in another language.

%package go
Summary:      GNU Go Compiler
License:        GPL-3.0+ 
Group:        Development/Languages
Requires: gcc49 = %{version}-%{release}
Requires: libgo%{libgo_sover} >= %{version}-%{release}

%description go
This package contains a Go compiler and associated development
files based on the GNU GCC technology.
%package go-32bit
Summary:      GNU Go Compiler
License:        GPL-3.0+ 
Group:        Development/Languages
Requires: gcc49-32bit = %{version}-%{release}
Requires: libgo%{libgo_sover}-32bit >= %{version}-%{release}

%description go-32bit
This package contains a Go compiler and associated development
files based on the GNU GCC technology.
%package go-64bit
Summary:      GNU Go Compiler
License:        GPL-3.0+ 
Group:        Development/Languages
Requires: gcc49-64bit = %{version}-%{release}
Requires: libgo%{libgo_sover}-64bit >= %{version}-%{release}

%description go-64bit
This package contains a Go compiler and associated development
files based on the GNU GCC technology.

%package -n libgo%{libgo_sover}%{libgo_suffix}
Summary:      GNU Go compiler runtime library
License:        BSD-3-Clause
Group:        Development/Languages
Provides:	libgo%{libgo_sover} = %{version}-%{release}

%description -n libgo%{libgo_sover}%{libgo_suffix}
A foreign function interface is the popular name for the interface that allows code written in one language to call code written in another language.

%post -n libgo%{libgo_sover}%{libgo_suffix} -p /sbin/ldconfig

%postun -n libgo%{libgo_sover}%{libgo_suffix} -p /sbin/ldconfig
%package -n libgo%{libgo_sover}%{libgo_suffix}-32bit
Summary:      GNU Go compiler runtime library
License:        BSD-3-Clause
Group:        Development/Languages
Provides:	libgo%{libgo_sover}-32bit = %{version}-%{release}

%description -n libgo%{libgo_sover}%{libgo_suffix}-32bit
A foreign function interface is the popular name for the interface that allows code written in one language to call code written in another language.

%post -n libgo%{libgo_sover}%{libgo_suffix}-32bit -p /sbin/ldconfig

%postun -n libgo%{libgo_sover}%{libgo_suffix}-32bit -p /sbin/ldconfig
%package -n libgo%{libgo_sover}%{libgo_suffix}-64bit
Summary:      GNU Go compiler runtime library
License:        BSD-3-Clause
Group:        Development/Languages
Provides:	libgo%{libgo_sover}-64bit = %{version}-%{release}

%description -n libgo%{libgo_sover}%{libgo_suffix}-64bit
A foreign function interface is the popular name for the interface that allows code written in one language to call code written in another language.

%post -n libgo%{libgo_sover}%{libgo_suffix}-64bit -p /sbin/ldconfig

%postun -n libgo%{libgo_sover}%{libgo_suffix}-64bit -p /sbin/ldconfig


%package -n gcc49-testresults
Summary:      Testsuite results
License:	SUSE-Public-Domain
Group:        Development/Languages

%description -n gcc49-testresults
Results from running the gcc and target library testsuites.




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


# Versionspecific directories
%define versmainlibdir %{libsubdir}
%define versmainlibdirbi32 %{libsubdir}/32
%define versmainlibdirbi64 %{libsubdir}/64
%ifarch ppc
%define versmainlibdirbi32 %{libsubdir}
%define versmainlibdirbi64 %{libsubdir}/64
%endif
%if %{build_primary_64bit}
%define versmainlibdirbi %{versmainlibdirbi32}
%else
%define versmainlibdirbi %{versmainlibdirbi64}
%endif

%define mainlibdir %{_libdir}
%define mainlibdirbi32 %{_prefix}/lib
%define mainlibdirbi64 %{_prefix}/lib64
%if %{build_primary_64bit}
%define mainlibdirbi %{mainlibdirbi32}
%else
%define mainlibdirbi %{mainlibdirbi64}
%endif


# Now define a few macros that make it easy to package libs and
# related files just to the right package, without caring for the
# exact path the files are in.
#   %mainlib  package X from all dirs that belong to the main package
#   %biarchlib   package X from all dirs that belong to the -32/64bit package
%define mainlib() %{mainlibdir}/%1\
%{nil}
%define biarchlib() %{nil}
%if %{biarch}
%if !%{separate_biarch}
%define mainlib() %{mainlibdir}/%1\
%{mainlibdirbi}/%1\
%{nil}
%else
%define biarchlib() %{mainlibdirbi}/%1\
%{nil}
%endif
%endif

%define versmainlib() %{versmainlibdir}/%1\
%{nil}
%define versbiarchlib() %{nil}
%if %{biarch}
%if !%{separate_biarch}
%define versmainlib() %{versmainlibdir}/%1\
%{versmainlibdirbi}/%1\
%{nil}
%else
%define versbiarchlib() %{versmainlibdirbi}/%1\
%{nil}
%endif
%endif



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

CFLAGS="$RPM_OPT_FLAGS" CXXFLAGS="$RPM_OPT_FLAGS" XCFLAGS="$RPM_OPT_FLAGS" \
TCFLAGS="$RPM_OPT_FLAGS" GCJFLAGS="$RPM_OPT_FLAGS $GCJ_EXTRA_FLAGS" \
../configure \
	--prefix=%{_prefix} \
	--infodir=%{_infodir} \
	--mandir=%{_mandir} \
	--libdir=%{_libdir} \
	--libexecdir=%{_libdir} \
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
	--enable-multilib \
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


%if 0%{?building_libffi:1}
make stage1-bubble $PARALLEL
make all-target-libffi $PARALLEL
%else
STAGE1_FLAGS="-g"
# Only run profiled bootstrap on archs where it works and matters
%ifarch x86_64 ppc64le s390x
make profiledbootstrap STAGE1_CFLAGS="$STAGE1_FLAGS" BOOT_CFLAGS="$RPM_OPT_FLAGS" $PARALLEL
%else
make STAGE1_CFLAGS="$STAGE1_FLAGS" BOOT_CFLAGS="$RPM_OPT_FLAGS" $PARALLEL
%endif
make info
%if 0%{?building_libjava:1}
make -C %{GCCDIST}/libstdc++-v3/doc doc-html-doxygen
%endif
%if 0%{?run_tests:1}
echo "Run testsuite"
(make -C %{GCCDIST}/libstdc++-v3 check-abi || true)
mv %{GCCDIST}/libstdc++-v3/testsuite/libstdc++.log %{GCCDIST}/libstdc++-v3/testsuite/libstdc++-abi.log
mv %{GCCDIST}/libstdc++-v3/testsuite/libstdc++.sum %{GCCDIST}/libstdc++-v3/testsuite/libstdc++-abi.sum
# asan needs a whole shadow address space
ulimit -v unlimited || true
make -k check $PARALLEL || true
mkdir ../testresults
../contrib/test_summary | tee ../testresults/test_summary.txt
%endif
%endif

%install
export NO_BRP_CHECK_BYTECODE_VERSION=true
cd obj-%{GCCDIST}
# Work around tail/head -1 changes
export _POSIX2_VERSION=199209
export LIBRARY_PATH=$RPM_BUILD_ROOT%{libsubdir}:$RPM_BUILD_ROOT%{mainlibdirbi}
%if 0%{?building_libffi:1}
make -C %{GCCDIST}/libffi install DESTDIR=$RPM_BUILD_ROOT
%else
%if 0%{?building_libjava:1}
make -C %{GCCDIST}/libjava install DESTDIR=$RPM_BUILD_ROOT
make -C gcc java.install-man DESTDIR=$RPM_BUILD_ROOT
make -C gcc java.install-common DESTDIR=$RPM_BUILD_ROOT
make -C gcc install-common DESTDIR=$RPM_BUILD_ROOT COMPILERS='jc1$(exeext) jvgenmain$(exeext)'
# copy the libstdc++ API reference
cp -r %{GCCDIST}/libstdc++-v3/doc/doxygen/html ../libstdc++-v3/doc/html/api
# install-common also installs collect2, gcov and the g++ and gfortran driver
%if %{build_cp}
rm $RPM_BUILD_ROOT%{_prefix}/bin/g++%{binsuffix}
%endif
%if %{build_fortran}
rm $RPM_BUILD_ROOT%{_prefix}/bin/gfortran%{binsuffix}
%endif
rm $RPM_BUILD_ROOT%{_prefix}/bin/gcov%{binsuffix}
rm $RPM_BUILD_ROOT%{libsubdir}/collect2
%else
make install DESTDIR=$RPM_BUILD_ROOT
%if %{build_java}
make -C gcc java.uninstall DESTDIR=$RPM_BUILD_ROOT
make -C gcc java.install-info DESTDIR=$RPM_BUILD_ROOT
rm $RPM_BUILD_ROOT%{_prefix}/bin/jcf-dump%{binsuffix}
rm $RPM_BUILD_ROOT%{_mandir}/man1/jcf-dump%{binsuffix}.1
rm $RPM_BUILD_ROOT%{libsubdir}/jc1
rm $RPM_BUILD_ROOT%{libsubdir}/jvgenmain
%endif
%endif
%endif

# Remove libffi installed files if we did not want to build it
%if !0%{?building_libffi:1}
rm -f $RPM_BUILD_ROOT%{mainlibdir}/libffi.*
%if %{biarch}
  rm -f $RPM_BUILD_ROOT%{mainlibdirbi}/libffi.*
%endif
rm -f $RPM_BUILD_ROOT%{libsubdir}/include/ffi.h
rm -f $RPM_BUILD_ROOT%{libsubdir}/include/ffitarget.h
rm -f $RPM_BUILD_ROOT%{_mandir}/man3/ffi%{binsuffix}.3*
rm -f $RPM_BUILD_ROOT%{_mandir}/man3/ffi_call%{binsuffix}.3*
rm -f $RPM_BUILD_ROOT%{_mandir}/man3/ffi_prep_cif%{binsuffix}.3*
rm -f $RPM_BUILD_ROOT%{_mandir}/man3/ffi_prep_cif_var%{binsuffix}.3*
%endif

# Remove some useless .la files
for lib in libobjc libgfortran libgfortranbegin libquadmath libcaf_single \
    libgomp libstdc++ libsupc++ libgcj-tools libgij libgo \
    libasan libatomic libitm libtsan libcilkrts liblsan libubsan libvtv; do
  rm -f $RPM_BUILD_ROOT%{versmainlibdir}/$lib.la
%if %{biarch}
  rm -f $RPM_BUILD_ROOT%{versmainlibdirbi}/$lib.la
%endif
done

mkdir -p $RPM_BUILD_ROOT%{_libdir}
%if %{biarch}
%if %{build_primary_64bit}
mkdir -p $RPM_BUILD_ROOT%{_prefix}/lib
%else
mkdir -p $RPM_BUILD_ROOT%{_prefix}/lib64
%endif
%endif


%if %{build_ada}
mv $RPM_BUILD_ROOT%{libsubdir}/adalib/lib*-*.so $RPM_BUILD_ROOT%{_libdir}
ln -sf %{_libdir}/libgnarl%{binsuffix}.so $RPM_BUILD_ROOT%{libsubdir}/adalib/libgnarl.so
ln -sf %{_libdir}/libgnat%{binsuffix}.so $RPM_BUILD_ROOT%{libsubdir}/adalib/libgnat.so
chmod a+x $RPM_BUILD_ROOT%{_libdir}/libgna*-*.so
%if %{biarch}
mv $RPM_BUILD_ROOT%{versmainlibdirbi}/adalib/lib*-*.so $RPM_BUILD_ROOT%{mainlibdirbi}/
ln -sf %{mainlibdirbi}/libgnarl%{binsuffix}.so $RPM_BUILD_ROOT%{versmainlibdirbi}/adalib/libgnarl.so
ln -sf %{mainlibdirbi}/libgnat%{binsuffix}.so $RPM_BUILD_ROOT%{versmainlibdirbi}/adalib/libgnarl.so
chmod a+x $RPM_BUILD_ROOT%{mainlibdirbi}/libgna*-*.so
%endif
%endif

rm -f $RPM_BUILD_ROOT%{_prefix}/bin/c++%{binsuffix}

# Remove some crap from the .la files:
for l in `find $RPM_BUILD_ROOT -name '*.la'`; do
  echo "changing $l"
# -e '/^dependency_libs/s|%{libsubdir}/\([^.]*\)\.la |%{_libdir}/\1\.la |g'
  sed -e '/^dependency_libs/s| -L%{_builddir}/[^ ]*||g' \
      -e '/^dependency_libs/s| -L/usr/%{GCCDIST}/bin||g' \
      -e '/^dependency_libs/s|-lm \(-lm \)*|-lm |' \
      -e '/^dependency_libs/s|-L[^ ]* ||g' \
%if %{biarch}
%if %{build_primary_64bit}
      -e '/^libdir/s|%{_libdir}/32|%{_prefix}/lib|' \
      -e '/^libdir/s|lib64/\.\./||' \
%else
      -e '/^libdir/s|%{_libdir}/64|%{_prefix}/lib64|' \
%endif
%endif
      < $l  > $l.new
  mv $l.new $l
done

%if 0%{?run_tests:1} 
cp `find . -name "*.sum"` ../testresults/
cp `find . -name "*.log"  \! -name "config.log" | grep -v 'acats.\?/tests' ` ../testresults/
chmod 644 ../testresults/*
%endif
# Remove files that we do not need to clean up filelist
rm -f $RPM_BUILD_ROOT%{_prefix}/bin/%{GCCDIST}-*
rm -rf $RPM_BUILD_ROOT%{libsubdir}/install-tools
#rm -rf $RPM_BUILD_ROOT%{_libdir}/pkgconfig/libgcj%{binsuffix}.pc
rm -f $RPM_BUILD_ROOT%{libsubdir}/include-fixed/zutil.h
rm -f $RPM_BUILD_ROOT%{libsubdir}/include-fixed/linux/a.out.h
rm -f $RPM_BUILD_ROOT%{libsubdir}/include-fixed/asm-generic/socket.h
# no plugins
rm -rf $RPM_BUILD_ROOT%{libsubdir}/plugin
rm -f  $RPM_BUILD_ROOT%{_infodir}/dir


%if 0%{?building_libjava:1}
# gcj -static doesn't work properly anyway, unless using --whole-archive
# let's save the space instead.
find $RPM_BUILD_ROOT -name libgcj.a \
	-o -name libgcj-tools.a \
	-o -name libgij.a \
	-o -name libjvm.a \
	-o -name libgcj_bc.a \
  | xargs rm -f

find $RPM_BUILD_ROOT -name libgcj.spec | xargs \
  sed -i -e 's/lib: /&%%{static:%%eJava programs cannot be linked statically}/'

# security files have broken install locations, also they cause conflicts
# between libgcj versions.  Simply delete them here, libgcj will use its
# defaults in this case (which is what these files contain anyway).
rm -f $RPM_BUILD_ROOT%{libsubdir}/logging.properties
rm -r $RPM_BUILD_ROOT%{libsubdir}/security
%endif

%if 0%{?building_libffi:1}
# Move libffi headers, remove empty libffi libtool file
mkdir -p $RPM_BUILD_ROOT%{_prefix}/include
mv $RPM_BUILD_ROOT%{libsubdir}/include/ffitarget.h $RPM_BUILD_ROOT%{_prefix}/include/
mv $RPM_BUILD_ROOT%{libsubdir}/include/ffi.h $RPM_BUILD_ROOT%{_prefix}/include/
rm -f $RPM_BUILD_ROOT%{mainlibdir}/libffi.la
%if %{biarch}
rm -f $RPM_BUILD_ROOT%{mainlibdirbi}/libffi.la
%endif
# Generate a simple pkg-config file
mkdir -p $RPM_BUILD_ROOT%{_libdir}/pkgconfig
echo -e 'Name: libffi\nVersion: 3.0.9\nDescription: libffi\nLibs: -lffi' > $RPM_BUILD_ROOT%{_libdir}/pkgconfig/libffi.pc
%endif

%if %{build_java}
%if !%{build_libjava}
rm $RPM_BUILD_ROOT%{_mandir}/man1/jv-convert%{binsuffix}.1
rm $RPM_BUILD_ROOT%{_mandir}/man1/gcj-dbtool%{binsuffix}.1
rm $RPM_BUILD_ROOT%{_mandir}/man1/gij%{binsuffix}.1
rm $RPM_BUILD_ROOT%{_mandir}/man1/grmic%{binsuffix}.1
rm $RPM_BUILD_ROOT%{_mandir}/man1/gc-analyze%{binsuffix}.1
rm $RPM_BUILD_ROOT%{_mandir}/man1/aot-compile%{binsuffix}.1
rm $RPM_BUILD_ROOT%{_mandir}/man1/rebuild-gcj-db%{binsuffix}.1
%endif
rm -f $RPM_BUILD_ROOT%{_datadir}/gcc%{binsuffix}/python/libjava/aotcompile.py
rm -f $RPM_BUILD_ROOT%{_datadir}/gcc%{binsuffix}/python/libjava/classfile.py
%endif
rm -f $RPM_BUILD_ROOT%{_mandir}/man7/fsf-funding.7
rm -f $RPM_BUILD_ROOT%{_mandir}/man7/gfdl.7
rm -f $RPM_BUILD_ROOT%{_mandir}/man7/gpl.7
rm -f $RPM_BUILD_ROOT%{_libdir}/libiberty.a
%if %{biarch}
%if %{build_primary_64bit}
rm -f $RPM_BUILD_ROOT%{_prefix}/lib/libiberty.a
%else
rm -f $RPM_BUILD_ROOT%{_prefix}/lib64/libiberty.a
%endif
%endif
rm -f $RPM_BUILD_ROOT%{libsubdir}/liblto_plugin.a
rm -f $RPM_BUILD_ROOT%{libsubdir}/liblto_plugin.la
%if %{build_go}
# gccgo.info isn't properly versioned
rm $RPM_BUILD_ROOT%{_infodir}/gccgo.info*
%endif


%if %{build_java}
%if 0%{?building_libffi:1}
%files -n libffi%{libffi_sover}%{libffi_suffix}
%defattr(-,root,root)
%mainlib libffi.so.%{libffi_sover}*

%if %{separate_biarch}
%files -n libffi%{libffi_sover}%{libffi_suffix}%{separate_biarch_suffix}
%defattr(-,root,root)
%biarchlib libffi.so.%{libffi_sover}*
%endif

%post -n libffi49-devel
%install_info --info-dir=%{_infodir} %{_infodir}/libffi%{binsuffix}.info.gz
%postun -n libffi49-devel
%install_info_delete --info-dir=%{_infodir} %{_infodir}/libffi%{binsuffix}.info.gz

%files -n libffi49-devel
%defattr(-,root,root)
%{_prefix}/include/ffi.h
%{_prefix}/include/ffitarget.h
%mainlib libffi.so
%mainlib libffi.a
%{_libdir}/pkgconfig/libffi.pc
%doc %{_infodir}/libffi%{binsuffix}.info.gz
%doc %{_mandir}/man3/ffi%{binsuffix}.3.gz
%doc %{_mandir}/man3/ffi_call%{binsuffix}.3.gz
%doc %{_mandir}/man3/ffi_prep_cif%{binsuffix}.3.gz
%doc %{_mandir}/man3/ffi_prep_cif_var%{binsuffix}.3.gz

%if %{separate_biarch}
%files -n libffi49-devel%{separate_biarch_suffix}
%defattr(-,root,root)
%biarchlib libffi.so
%biarchlib libffi.a
%endif
%endif
%endif

%if %{build_go}
%files go
%{_prefix}/bin/gccgo%{binsuffix}
%{libsubdir}/go1
%versmainlib libgo.a
%versmainlib libgo.so
%versmainlib libgobegin.a
%dir %mainlibdir/go
%dir %mainlibdir/go/%{gcc_dir_version}
%mainlibdir/go/%{gcc_dir_version}/%{GCCDIST}
%doc %{_mandir}/man1/gccgo%{binsuffix}.1.gz

%if %{separate_biarch}
%files go%{separate_biarch_suffix}
%versbiarchlib libgo.a
%versbiarchlib libgo.so
%versbiarchlib libgobegin.a
%dir %mainlibdirbi/go
%dir %mainlibdirbi/go/%{gcc_dir_version}
%mainlibdirbi/go/%{gcc_dir_version}/%{GCCDIST}
%endif

%files -n libgo%{libgo_sover}%{libgo_suffix}
%defattr(-,root,root)
%mainlib libgo.so.%{libgo_sover}*

%if %{separate_biarch}
%files -n libgo%{libgo_sover}%{libgo_suffix}%{separate_biarch_suffix}
%defattr(-,root,root)
%biarchlib libgo.so.%{libgo_sover}*
%endif
%endif

%if 0%{?run_tests:1}
%files -n gcc49-testresults
%defattr(-,root,root)
%doc testresults/test_summary.txt
%doc testresults/*.sum
%doc testresults/*.log
%endif


%changelog
