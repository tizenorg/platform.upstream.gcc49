%define cross armv7l
%define armv7l 1

#
# spec file for package gcc49
#
# Copyright (c) 2009 SUSE LINUX Products GmbH, Nuernberg, Germany.
# Copyright (c) 2015 Tizen
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via http://bugs.tizen.org/
#
# we use %%{?macro: ... } as it is more compact 
%if 0%{?run_tests}
%define gcc_run_tests 1
%endif

%define quadmath_arch %ix86 x86_64 ia64
%define tsan_arch x86_64
%define asan_arch x86_64 %ix86 ppc ppc64 %sparc %arm
%define itm_arch x86_64 %ix86 %arm ppc ppc64 ppc64le s390 s390x %sparc aarch64
%define atomic_arch x86_64 %ix86 %arm aarch64 ppc ppc64 ppc64le s390 s390x %sparc m68k
%define lsan_arch x86_64
%define ubsan_arch x86_64 %ix86 ppc ppc64 %arm
%define cilkrts_arch x86_64 %ix86

%ifarch armv7l
%define ARCH armv7l
%define ABI eabi
%endif
%ifarch %ix86
%define ARCH i586
%endif
%ifarch x86_64
%define ARCH x86_64
%endif
%ifarch aarch64
%define ARCH aarch64
%endif
%define host_arch %{ARCH}-tizen-linux-gnu%{?ABI}

%define target_cpu %{?cross}%{!?cross:%{ARCH}}
%define target_abi %{?cross:%{?armv7l:eabi}}%{!?cross:%{?ABI}}

%define target_arch %{target_cpu}-tizen-linux-gnu%{?target_abi}
%define libdir %{!?cross:%{_libdir}}%{?cross:%{_prefix}/lib%{?aarch64:64}}
%define libsubdir %{libdir}/gcc/%{target_arch}/%{version}

Name:         gcc%{?cross:-%{cross}}
# With generated files in src we could drop the following
BuildRequires: bison
BuildRequires: flex
BuildRequires: gettext-devel
BuildRequires: makeinfo
## until here, but at least renaming and patching info files breaks this
BuildRequires: gcc-c++
BuildRequires: cloog-isl-devel
BuildRequires: isl-devel
BuildRequires: mpc-devel
BuildRequires: zlib-devel
BuildRequires: mpfr-devel
%ifarch x86_64
BuildRequires: glibc-devel-32bit
%endif
BuildRequires: perl
%{?cross:BuildRequires: binutils-%{cross}}
# here we use %%if because OBS spec parser cannot expand
# %%{?macro:...} correctly
%if 0%{?gcc_run_tests}
BuildRequires: dejagnu
BuildRequires: expect
BuildRequires: gdb
%endif
URL:           http://gcc.gnu.org/
Version:       4.9.2.0
Release:       0
Source:        gcc-%{version}.tar.bz2
Group:         Development/Building
Summary:       The GNU C Compiler and Support Files
License:       GPL-3.0+
%{?cross:ExcludeArch: %{cross}}
%description
Core package for the GNU Compiler Collection, including the C language
frontend.

%package c++
Summary:       The GNU C++ Compiler
License:       GPL-3.0+
Group:         Development/Languages
%description c++
This package contains the GNU compiler for C++.

%package -n libstdc++
Summary:       The standard C++ shared library
License:       GPL-3.0-with-GCC-exception
Group:         Development/Building
%description -n libstdc++
The standard C++ library, needed for dynamically linked C++ programs.
%post -n libstdc++ -p /sbin/ldconfig
%postun -n libstdc++ -p /sbin/ldconfig

%package -n libstdc++-devel
Summary:       Include Files and Libraries mandatory for Development
License:       GPL-3.0-with-GCC-exception
Group:         Development/Building
%description -n libstdc++-devel
This package contains all the headers and libraries of the standard C++
library. It is needed for compiling C++ code.

%package -n libgcc
Summary:       C compiler runtime library
License:       GPL-3.0-with-GCC-exception
Group:         Development/Building
%description -n libgcc
Libgcc is needed for dynamically linked C programs.
%post -n libgcc -p /sbin/ldconfig
%postun -n libgcc -p /sbin/ldconfig

%package -n libgomp
Summary:       The GNU compiler collection OpenMP runtime library
License:       GPL-3.0-with-GCC-exception
Group:         Development/Building
%description -n libgomp
This is the OpenMP runtime library needed by OpenMP enabled programs
that were built with the -fopenmp compiler option and by programs that
were auto-parallelized via the -ftree-parallelize-loops compiler
option.
%post -n libgomp -p /sbin/ldconfig
%postun -n libgomp -p /sbin/ldconfig

%package objc
Summary:       GNU Objective C Compiler
License:       GPL-3.0+
Group:         Development/Languages
%description objc
This package contains the GNU Objective C compiler. Objective C is an
object oriented language, created by Next Inc. and used in their
Nextstep OS. The source code is available in the gcc package.

%package -n libobjc
Summary:       Library for the GNU Objective C Compiler
License:       GPL-3.0-with-GCC-exception
Group:         Development/Building
%description -n libobjc
The library for the GNU Objective C compiler.
%post -n libobjc -p /sbin/ldconfig
%postun -n libobjc -p /sbin/ldconfig

%package obj-c++
Summary:       GNU Objective C++ Compiler
License:       GPL-3.0+
Group:         Development/Languages
%description obj-c++
This package contains the GNU Objective C++ compiler. Objective C++ is an
object oriented language, created by Next Inc. and used in their
Nextstep OS. The source code is available in the gcc package.

%package -n cpp
Summary:       The GCC Preprocessor
License:       GPL-3.0+
Group:         Development/Languages
%description -n cpp
This Package contains just the preprocessor that is used by the X11
packages.

%package ada
Summary:       GNU Ada95 Compiler Based on GCC (GNAT)
License:       GPL-3.0+
Group:         Development/Languages
%description ada
This package contains an Ada95 compiler and associated development
tools based on the GNU GCC technology. Ada95 is the object oriented
successor of the Ada83 language. To build this package from source you
must have installed a binary version to bootstrap the compiler.

%package -n libada
Summary:      GNU Ada Runtime Libraries
License:      GPL-3.0-with-GCC-exception
Group:        Development/Languages
%description -n libada
This package contains the shared libraries required to run programs
compiled with the GNU Ada compiler (GNAT) if they are compiled to use
shared libraries. It also contains the shared libraries for the
Implementation of the Ada Semantic Interface Specification (ASIS), the
implementation of Distributed Systems Programming (GLADE) and the Posix
1003.5 Binding (Florist).
%post -n libada -p /sbin/ldconfig
%postun -n libada -p /sbin/ldconfig

%package fortran
Summary:       The GNU Fortran Compiler and Support Files
License:       GPL-3.0+
Group:         Development/Languages
%description fortran
This is the Fortran compiler of the GNU Compiler Collection (GCC).

%package -n libgfortran
Summary:       The GNU Fortran Compiler Runtime Library
License:       GPL-3.0-with-GCC-exception
Group:         Development/Languages
%description -n libgfortran
The runtime library needed to run programs compiled with the Fortran compiler
of the GNU Compiler Collection (GCC).
%post -n libgfortran -p /sbin/ldconfig
%postun -n libgfortran -p /sbin/ldconfig

%package -n libquadmath
Summary:       The GNU Fortran Compiler Quadmath Runtime Library
License:       LGPL-2.1
Group:         Development/Languages
%description -n libquadmath
The runtime library needed to run programs compiled with the Fortran compiler
of the GNU Compiler Collection (GCC) and quadruple precision floating point
operations.
%post -n libquadmath -p /sbin/ldconfig
%postun -n libquadmath -p /sbin/ldconfig

%package -n libitm
Summary:       The GNU Compiler Transactional Memory Runtime Library
License:       MIT
Group:         Development/Languages
%description -n libitm
The runtime library needed to run programs compiled with the
-fgnu-tm option of the GNU Compiler Collection (GCC).
%post -n libitm -p /sbin/ldconfig
%postun -n libitm -p /sbin/ldconfig

%package -n libasan
Summary:       The GNU Compiler Address Sanitizer Runtime Library
License:       MIT
Group:         Development/Languages
%description -n libasan
The runtime library needed to run programs compiled with the
-fsanitize=address option of the GNU Compiler Collection (GCC).
%post -n libasan -p /sbin/ldconfig
%postun -n libasan -p /sbin/ldconfig

%package -n libtsan
Summary:       The GNU Compiler Thread Sanitizer Runtime Library
License:       MIT
Group:         Development/Languages
%description -n libtsan
The runtime library needed to run programs compiled with the
-fsanitize=thread option of the GNU Compiler Collection (GCC).
%post -n libtsan -p /sbin/ldconfig
%postun -n libtsan -p /sbin/ldconfig

%package -n libatomic
Summary:       The GNU Compiler Atomic Operations Runtime Library
License:       GPL-3.0-with-GCC-exception
Group:         Development/Languages
%description -n libatomic
The runtime library for atomic operations of the GNU Compiler Collection (GCC).
%post -n libatomic -p /sbin/ldconfig
%postun -n libatomic -p /sbin/ldconfig

%package -n libcilkrts
Summary:       The GNU Compiler Cilk+ Runtime Library
License:       MIT
Group:         Development/Languages
%description -n libcilkrts
The runtime library needed to run programs compiled with the
-fcilkplus option of the GNU Compiler Collection (GCC).
%post -n libcilkrts -p /sbin/ldconfig
%postun -n libcilkrts -p /sbin/ldconfig

%package -n liblsan
Summary:       The GNU Compiler Leak Sanitizer Runtime Library
License:       MIT
Group:         Development/Languages
%description -n liblsan
The runtime library needed to run programs compiled with the
-fsanitize=leak option of the GNU Compiler Collection (GCC).
%post -n liblsan -p /sbin/ldconfig
%postun -n liblsan -p /sbin/ldconfig

%package -n libubsan
Summary:       The GNU Compiler Undefined Sanitizer Runtime Library
License:       MIT
Group:         Development/Languages
%description -n libubsan
The runtime library needed to run programs compiled with the
-fsanitize=undefined option of the GNU Compiler Collection (GCC).
%post -n libubsan -p /sbin/ldconfig
%postun -n libubsan -p /sbin/ldconfig

%package -n libvtv
Summary:       The GNU Compiler Vtable Verifier Runtime Library
License:       MIT
Group:         Development/Languages
%description -n libvtv
The runtime library needed to run programs compiled with the
-fvtable-verify option of the GNU Compiler Collection (GCC).
%post -n libvtv -p /sbin/ldconfig
%postun -n libvtv -p /sbin/ldconfig

%package -n libgcj
Summary:       Java Runtime Library for gcc
License:       GPL-2.0-with-classpath-exception
Group:         Development/Building
%description -n libgcj
This library is needed if you want to use the GNU Java compiler, gcj.
Source code for this package is in gcc.
%post -n libgcj -p /sbin/ldconfig
%postun -n libgcj -p /sbin/ldconfig

%package java
Summary:       The GNU Java Compiler
License:       GPL-3.0+
Group:         Development/Languages
%description java
The Java compiler from the GCC-tools-suite.

%package -n libgcj_bc
Summary:       Fake library for BC-ABI compatibility.
License:       GPL-2.0-with-classpath-exception
Group:         Development/Languages
%description -n libgcj_bc
A fake library that is used at link time only. It ensures that
binaries built with the BC-ABI link against a constant SONAME.
This way, BC-ABI binaries continue to work if the SONAME underlying
libgcj.so changes.

%package -n libgcj-jar
Summary:       Java runtime library (jar files).
License:       GPL-2.0-with-classpath-exception
Group:         Development/Languages
%description -n libgcj-jar
These are the jar files that go along with the gcj front end to gcc.

%package -n libgcj-devel
Summary:       Include Files and Libraries mandatory for Development.
License:       GPL-2.0-with-classpath-exception
Group:         Development/Languages
%description -n libgcj-devel
This package contains all necessary include files and libraries needed
to develop applications that require these.

%package -n gcc-gij
Summary:       Java Bytecode Interpreter for gcc
License:       GPL-2.0-with-classpath-exception
Group:         Development/Languages
%description -n gcc-gij
This package contains the java bytecode interpreter gij and related tools.

%package -n libffi
Summary:       Foreign Function Interface library
License:       BSD-3-Clause
Group:         Development/Building
%description -n libffi
A foreign function interface is the popular name for the interface that allows code written in one language to call code written in another language.
%post -n libffi -p /sbin/ldconfig
%postun -n libffi -p /sbin/ldconfig

%package -n libffi-devel
Summary:       Foreign Function Interface library development files
License:       BSD 3-Clause
Group:         Development/Building
%description -n libffi-devel
A foreign function interface is the popular name for the interface that allows code written in one language to call code written in another language.

%package go
Summary:       GNU Go Compiler
License:       GPL-3.0+
Group:         Development/Languages
%description go
This package contains a Go compiler and associated development
files based on the GNU GCC technology.

%package -n libgo
Summary:       GNU Go compiler runtime library
License:       BSD-3-Clause
Group:         Development/Languages
%description -n libgo
A foreign function interface is the popular name for the interface that allows code written in one language to call code written in another language.
%post -n libgo -p /sbin/ldconfig
%postun -n libgo -p /sbin/ldconfig

%package testresults
Summary:       Testsuite results
License:       SUSE-Public-Domain
Group:         Development/Languages
%description testresults
Results from running the gcc and target library testsuites.

%package -n gcc-32bit
Summary:       The GNU C Compiler 32bit support
Group:         Development/Building
%description -n gcc-32bit
This package contains 32bit support for the GNU Compiler Collection.

%package -n libstdc++-devel-32bit
Summary:       Include Files and Libraries mandatory for Development
License:       GPL-3.0-with-GCC-exception
Group:         Development/Building
%description -n libstdc++-devel-32bit
This package contains all the headers and libraries of the standard C++
library. It is needed for compiling C++ code.

%package -n libgcc-32bit
Summary:       C compiler runtime library
License:       GPL-3.0-with-GCC-exception
Group:         Development/Building
%description -n libgcc-32bit
Libgcc is needed for dynamically linked C programs.
%post -n libgcc-32bit -p /sbin/ldconfig
%postun -n libgcc-32bit -p /sbin/ldconfig

%package -n libgomp-32bit
Summary:       The GNU compiler collection OpenMP runtime library
License:       GPL-3.0-with-GCC-exception
Group:         Development/Building
%description -n libgomp-32bit
This is the OpenMP runtime library needed by OpenMP enabled programs
that were built with the -fopenmp compiler option and by programs that
were auto-parallelized via the -ftree-parallelize-loops compiler
option.
%post -n libgomp-32bit -p /sbin/ldconfig
%postun -n libgomp-32bit -p /sbin/ldconfig

%package -n libstdc++-32bit
Summary:       The standard C++ shared library
License:       GPL-3.0-with-GCC-exception
Group:         Development/Building
%description -n libstdc++-32bit
The standard C++ library, needed for dynamically linked C++ programs.
%post -n libstdc++-32bit -p /sbin/ldconfig
%postun -n libstdc++-32bit -p /sbin/ldconfig

%package objc-32bit
Summary:       GNU Objective C Compiler
License:       GPL-3.0+
Group:         Development/Languages
%description objc-32bit
This package contains the GNU Objective C compiler. Objective C is an
object oriented language, created by Next Inc. and used in their
Nextstep OS. The source code is available in the gcc package.

%package -n libobjc-32bit
Summary:       Library for the GNU Objective C Compiler
License:       GPL-3.0-with-GCC-exception
Group:         Development/Building
%description -n libobjc-32bit
The library for the GNU Objective C compiler.
%post -n libobjc-32bit -p /sbin/ldconfig
%postun -n libobjc-32bit -p /sbin/ldconfig

%package ada-32bit
Summary:       GNU Ada95 Compiler Based on GCC (GNAT)
License:       GPL-3.0+
Group:         Development/Languages
%description ada-32bit
This package contains an Ada95 compiler and associated development
tools based on the GNU GCC technology. Ada95 is the object oriented
successor of the Ada83 language. To build this package from source you
must have installed a binary version to bootstrap the compiler.

%package -n libada-32bit
Summary:       GNU Ada Runtime Libraries
License:       GPL-3.0-with-GCC-exception
Group:         Development/Languages
%description -n libada-32bit
This package contains the shared libraries required to run programs
compiled with the GNU Ada compiler (GNAT) if they are compiled to use
shared libraries. It also contains the shared libraries for the
Implementation of the Ada Semantic Interface Specification (ASIS), the
implementation of Distributed Systems Programming (GLADE) and the Posix
1003.5 Binding (Florist).
%post -n libada-32bit -p /sbin/ldconfig
%postun -n libada-32bit -p /sbin/ldconfig

%package fortran-32bit
Summary:       The GNU Fortran Compiler and Support Files
License:       GPL-3.0+
Group:         Development/Languages
%description fortran-32bit
This is the Fortran compiler of the GNU Compiler Collection (GCC).

%package -n libgfortran-32bit
Summary:       The GNU Fortran Compiler Runtime Library
License:       GPL-3.0-with-GCC-exception
Group:         Development/Languages
%description -n libgfortran-32bit
The runtime library needed to run programs compiled with the Fortran compiler
of the GNU Compiler Collection (GCC).
%post -n libgfortran-32bit -p /sbin/ldconfig
%postun -n libgfortran-32bit -p /sbin/ldconfig

%package -n libquadmath-32bit
Summary:       The GNU Fortran Compiler Quadmath Runtime Library
License:       LGPL-2.1
Group:         Development/Languages
%description -n libquadmath-32bit
The runtime library needed to run programs compiled with the Fortran compiler
of the GNU Compiler Collection (GCC) and quadruple precision floating point
operations.
%post -n libquadmath-32bit -p /sbin/ldconfig
%postun -n libquadmath-32bit -p /sbin/ldconfig

%package -n libitm-32bit
Summary:       The GNU Compiler Transactional Memory Runtime Library
License:       MIT
Group:         Development/Languages
%description -n libitm-32bit
The runtime library needed to run programs compiled with the
-fgnu-tm option of the GNU Compiler Collection (GCC).
%post -n libitm-32bit -p /sbin/ldconfig
%postun -n libitm-32bit -p /sbin/ldconfig

%package -n libasan-32bit
Summary:       The GNU Compiler Address Sanitizer Runtime Library
License:       MIT
Group:         Development/Languages
%description -n libasan-32bit
The runtime library needed to run programs compiled with the
-fsanitize=address option of the GNU Compiler Collection (GCC).
%post -n libasan-32bit -p /sbin/ldconfig
%postun -n libasan-32bit -p /sbin/ldconfig

%package -n libtsan-32bit
Summary:       The GNU Compiler Thread Sanitizer Runtime Library
License:       MIT
Group:         Development/Languages
%description -n libtsan-32bit
The runtime library needed to run programs compiled with the
-fsanitize=thread option of the GNU Compiler Collection (GCC).
%post -n libtsan-32bit -p /sbin/ldconfig
%postun -n libtsan-32bit -p /sbin/ldconfig

%package -n libatomic-32bit
Summary:       The GNU Compiler Atomic Operations Runtime Library
License:       GPL-3.0-with-GCC-exception
Group:         Development/Languages
%description -n libatomic-32bit
The runtime library for atomic operations of the GNU Compiler Collection (GCC).
%post -n libatomic-32bit -p /sbin/ldconfig
%postun -n libatomic-32bit -p /sbin/ldconfig

%package -n libcilkrts-32bit
Summary:       The GNU Compiler Cilk+ Runtime Library
License:       MIT
Group:         Development/Languages
%description -n libcilkrts-32bit
The runtime library needed to run programs compiled with the
-fcilkplus option of the GNU Compiler Collection (GCC).
%post -n libcilkrts-32bit -p /sbin/ldconfig
%postun -n libcilkrts-32bit -p /sbin/ldconfig

%package -n liblsan-32bit
Summary:       The GNU Compiler Leak Sanitizer Runtime Library
License:       MIT
Group:         Development/Languages
%description -n liblsan-32bit
The runtime library needed to run programs compiled with the
-fsanitize=leak option of the GNU Compiler Collection (GCC).
%post -n liblsan-32bit -p /sbin/ldconfig
%postun -n liblsan-32bit -p /sbin/ldconfig

%package -n libubsan-32bit
Summary:       The GNU Compiler Undefined Sanitizer Runtime Library
License:       MIT
Group:         Development/Languages
%description -n libubsan-32bit
The runtime library needed to run programs compiled with the
-fsanitize=undefined option of the GNU Compiler Collection (GCC).
%post -n libubsan-32bit -p /sbin/ldconfig
%postun -n libubsan-32bit -p /sbin/ldconfig

%package -n libvtv-32bit
Summary:       The GNU Compiler Vtable Verifier Runtime Library
License:       MIT
Group:         Development/Languages
%description -n libvtv-32bit
The runtime library needed to run programs compiled with the
-fvtable-verify option of the GNU Compiler Collection (GCC).
%post -n libvtv-32bit -p /sbin/ldconfig
%postun -n libvtv-32bit -p /sbin/ldconfig

%package -n libffi-32bit
Summary:       Foreign Function Interface library
License:       BSD-3-Clause
Group:         Development/Building
%description -n libffi-32bit
A foreign function interface is the popular name for the interface that allows code written in one language to call code written in another language.
%post -n libffi-32bit -p /sbin/ldconfig
%postun -n libffi-32bit -p /sbin/ldconfig

%package -n libffi-devel-32bit
Summary:       Foreign Function Interface library development files
License:       BSD 3-Clause
Group:         Development/Building
%description -n libffi-devel-32bit
A foreign function interface is the popular name for the interface that allows code written in one language to call code written in another language.

%package go-32bit
Summary:       GNU Go Compiler
License:       GPL-3.0+
Group:         Development/Languages
%description go-32bit
This package contains a Go compiler and associated development
files based on the GNU GCC technology.

%package -n libgo-32bit
Summary:       GNU Go compiler runtime library
License:       BSD-3-Clause
Group:         Development/Languages
%description -n libgo-32bit
A foreign function interface is the popular name for the interface that allows code written in one language to call code written in another language.
%post -n libgo-32bit -p /sbin/ldconfig
%postun -n libgo-32bit -p /sbin/ldconfig


%prep
%setup -q -n gcc-%{version}

%build
rm -rf obj
mkdir obj
cd obj

RPM_OPT_FLAGS=`echo $RPM_OPT_FLAGS|sed -e 's/-fno-rtti//g' -e 's/-fno-exceptions//g' -e 's/-Wmissing-format-attribute//g' -e 's/-fstack-protector//g' -e 's/-ffortify=.//g' -e 's/-Wall//g' -e 's/-m32//g' -e 's/-m64//g' -e 's/-fexceptions//' -e 's/\([[:space:]]\+.*-D_FORTIFY_SOURCE=\)[[:alnum:]]\+/\10/g'
RPM_OPT_FLAGS="$RPM_OPT_FLAGS -D__USE_FORTIFY_LEVEL=0"`
%{?cross:
RPM_OPT_FLAGS=`echo $RPM_OPT_FLAGS|sed -e 's/-m\(arch\|tune\|cpu\)=[^ ]*//g'`
RPM_OPT_FLAGS=`echo $RPM_OPT_FLAGS|sed -e 's/-m\(sse\|fpmath\)[^ ]*//g'`
}
RPM_OPT_FLAGS=`echo $RPM_OPT_FLAGS|sed -e 's/  */ /g'`



CFLAGS="$RPM_OPT_FLAGS" CXXFLAGS="$RPM_OPT_FLAGS" XCFLAGS="$RPM_OPT_FLAGS" \
TCFLAGS="$RPM_OPT_FLAGS" GCJFLAGS="$RPM_OPT_FLAGS" \
../configure \
	--prefix=%{_prefix} \
	--infodir=%{_infodir} \
	--mandir=%{_mandir} \
	--libdir=%{libdir} \
	--libexecdir=%{libdir} \
	--enable-languages=c,c++,fortran \
	--enable-checking=release \
	--enable-ssp \
	--disable-libssp \
	--disable-bootstrap \
	--disable-libvtv \
	--disable-plugin \
	--disable-libgcj \
	--with-slibdir=%{libdir} \
	--with-system-zlib \
	--with-sysroot=/ \
	--enable-__cxa_atexit \
	--enable-libstdcxx-allocator=new \
	--disable-libstdcxx-pch \
	--enable-version-specific-runtime-libs \
	--enable-linker-build-id \
	--enable-linux-futex \
	--without-system-libunwind \
	--enable-threads=posix \
	--disable-multilib \
%{!?cross: \
%ifarch armv7l
	--with-arch=armv7-a \
	--with-tune=cortex-a8 \
	--with-float=softfp \
	--with-fpu=neon \
	--with-mode=thumb \
	--disable-sjlj-exceptions \
%endif
%ifarch aarch64
	--with-arch=armv8-a \
	--disable-sjlj-exceptions \
%endif
%ifarch %ix86
	--with-arch-32=i586 \
	--with-tune=generic \
%endif
%ifarch x86_64
	--with-arch-32=i586 \
	--with-tune=generic \
	--enable-multilib \
%endif
} \
%{?cross: \
%{?armv7l: \
	--with-arch=armv7-a \
	--with-tune=cortex-a8 \
	--with-float=softfp \
	--with-fpu=neon \
	--with-mode=thumb \
	--disable-sjlj-exceptions \
} \
%{?aarch64: \
	--with-arch=armv8-a \
	--disable-sjlj-exceptions \
} \
	--disable-libgcc \
	--disable-libquadmath \
	--disable-libgfortran \
	--disable-libgomp \
	--disable-libatomic \
	--disable-libstdc++-v3 \
	--disable-libsanitizer \
	--disable-libitm \
} \
	--with-bugurl="http://bugs.tizen.org/" \
	--with-pkgversion="Tizen" \
	--target=%{target_arch} \
	--host=%{host_arch} \
	--build=%{host_arch}



make BOOT_CFLAGS="$RPM_OPT_FLAGS" %{?_smp_mflags}
%{?gcc_run_tests:
  echo "Run testsuite"
  # asan needs a whole shadow address space
  ulimit -v unlimited || true
  make -k check %{?_smp_mflags} || true
  mkdir ../testresults
  ../contrib/test_summary | tee ../testresults/test_summary.txt
}

%install
cd obj

make install DESTDIR=$RPM_BUILD_ROOT

%{?gcc_run_tests:
  cp `find . -name "*.sum"` ../testresults/
  cp `find . -name "*.log"  \! -name "config.log" | grep -v 'acats.\?/tests' ` ../testresults/
  chmod 644 ../testresults/*
}

%{remove_docs}
rm -rf %{buildroot}/%{_datadir}/locale

#remove everything we don't need
rm -rf %{buildroot}/%{libsubdir}/install-tools
find %{buildroot}/%{libsubdir} -name "*.la" -exec rm -rf {} +

%{!?cross:
ln -s gcc %{buildroot}%{_bindir}/cc
mv %{buildroot}%{libsubdir}/libstdc++.so*-gdb.py %{buildroot}%{_datadir}/gcc-%{version}/python/libstdcxx/

# expose plugins for ar (required for lto builds)
mkdir -p %{buildroot}%{_prefix}/lib/bfd-plugins
ln -sf %{libsubdir}/liblto_plugin.so %{buildroot}%{_prefix}/lib/bfd-plugins/liblto_plugin.so

# legacy preprocessor
mkdir -p %{buildroot}/lib
ln -s %{_bindir}/cpp %{buildroot}/lib/cpp

# 32-bit libgcc in multilib configuration
%ifarch x86_64
mv %{buildroot}%{_prefix}/lib/libgcc_s.so* %{buildroot}%{libsubdir}/32/
%endif

# move libraries to libdir
for lib in asan atomic cilkrts gfortran gomp itm lsan quadmath stdc++ supc++ tsan ubsan
do
  [ -e %{buildroot}%{libsubdir}/lib$lib.a ] && mv %{buildroot}%{libsubdir}/lib$lib.a %{buildroot}%{libdir}/
  [ -e %{buildroot}%{libsubdir}/lib$lib.so ] && mv %{buildroot}%{libsubdir}/lib$lib.so* %{buildroot}%{libdir}/
done
}

%{?cross:
rm -rf %{buildroot}/%{libsubdir}/include-fixed
rm -rf %{buildroot}/%{libsubdir}/include
}

%files
%defattr(-,root,root)
%{?cross:
%{_bindir}/*
%{libsubdir}/*
}
%{!?cross:
%{_bindir}/gcc
%{_bindir}/cc
%{_bindir}/gcov
%{_bindir}/gcc-ar
%{_bindir}/gcc-nm
%{_bindir}/gcc-ranlib
%{_bindir}/%{target_arch}-gcc
%{_bindir}/%{target_arch}-gcc-%{version}
%{_bindir}/%{target_arch}-gcc-ar
%{_bindir}/%{target_arch}-gcc-nm
%{_bindir}/%{target_arch}-gcc-ranlib
%{libsubdir}/collect2
%{libsubdir}/lto1
%{libsubdir}/lto-wrapper
%{libsubdir}/liblto_plugin.so*
%{_prefix}/lib/bfd-plugins/liblto_plugin.so
%{libsubdir}/include-fixed/*
%{libsubdir}/include/*.h
%{libsubdir}/*.a
%{libsubdir}/*.so
%{libsubdir}/*.o
%{libsubdir}/*.spec
%{libdir}/*.so
%{libdir}/*.a
%ifarch %cilkrts_arch
%{libsubdir}/include/cilk/*
%endif
%ifnarch aarch64
%{libsubdir}/include/sanitizer/*
%endif

%files c++
%defattr(-,root,root)
%{libsubdir}/cc1plus
%{_bindir}/g++
%{_bindir}/c++
%{_bindir}/%{target_arch}-g++
%{_bindir}/%{target_arch}-c++

%files -n libstdc++
%defattr(-,root,root)
%{libdir}/libstdc++.so.*

%files -n libstdc++-devel
%defattr(-,root,root)
%{libdir}/libstdc++.so
%{libdir}/libstdc++.a
%{libdir}/libsupc++.a
%{libsubdir}/include/c++/*
%{_datadir}/gcc-%{version}/python/libstdcxx/*

%files -n libgcc
%defattr(-,root,root)
%{libdir}/libgcc_s.so.*

%files -n libgomp
%defattr(-,root,root)
%{libdir}/libgomp.so.*

%ifarch %asan_arch
%files -n libasan
%defattr(-,root,root)
%{libdir}/libasan.so.*
%endif

%ifarch %lsan_arch
%files -n liblsan
%defattr(-,root,root)
%{libdir}/liblsan.so.*
%endif

%ifarch %tsan_arch
%files -n libtsan
%defattr(-,root,root)
%{libdir}/libtsan.so.*
%endif

%ifarch %atomic_arch
%files -n libatomic
%defattr(-,root,root)
%{libdir}/libatomic.so.*
%endif

%ifarch %itm_arch
%files -n libitm
%defattr(-,root,root)
%{libdir}/libitm.so.*
%endif

%ifarch %cilkrts_arch
%files -n libcilkrts
%defattr(-,root,root)
%{libdir}/libcilkrts.so.*
%endif

%ifarch %ubsan_arch
%files -n libubsan
%defattr(-,root,root)
%{libdir}/libubsan.so.*
%endif

%files fortran
%defattr(-,root,root)
%dir %{libsubdir}/finclude
%{_bindir}/gfortran
%{_bindir}/%{target_arch}-gfortran
%{libsubdir}/f951
%{libsubdir}/finclude/*
%{libdir}/libgfortran.a
%{libdir}/libgfortran.so
%{libsubdir}/libgfortran.spec
%{libsubdir}/libgfortranbegin.a
%{libsubdir}/libcaf_single.a
%ifarch %quadmath_arch
%{libdir}/libquadmath.a
%{libdir}/libquadmath.so
%endif

%files -n libgfortran
%defattr(-,root,root)
%{libdir}/libgfortran.so.*

%ifarch %quadmath_arch
%files -n libquadmath
%defattr(-,root,root)
%{libdir}/libquadmath.so.*
%endif

%files -n cpp
%defattr(-,root,root)
%{_bindir}/cpp
%{libsubdir}/cc1
/lib/cpp


%{?gcc_run_tests:
%files testresults
%defattr(-,root,root)
%doc testresults/test_summary.txt
%doc testresults/*.sum
%doc testresults/*.log
}
%ifarch x86_64
%files -n gcc-32bit
%defattr(-,root,root)
%{libsubdir}/32/crt*
%{libsubdir}/32/*.a
%{libsubdir}/32/*.so
%{libsubdir}/32/*.o
%{libsubdir}/32/*.spec

%ifarch %asan_arch
%files -n libasan-32bit
%defattr(-,root,root)
%{libsubdir}/32/libasan.so.*
%endif

%ifarch %atomic_arch
%files -n libatomic-32bit
%defattr(-,root,root)
%{libsubdir}/32/libatomic.so.*
%endif

%ifarch %cilkrts_arch
%files -n libcilkrts-32bit
%defattr(-,root,root)
%{libsubdir}/32/libcilkrts.so.*
%endif

%files -n libgfortran-32bit
%defattr(-,root,root)
%{libsubdir}/32/libgfortran.so.*

%files -n libgcc-32bit
%defattr(-,root,root)
%{libsubdir}/32/libgcc_s.so.*

%files -n libgomp-32bit
%defattr(-,root,root)
%{libsubdir}/32/libgomp.so.*

%ifarch %itm_arch
%files -n libitm-32bit
%defattr(-,root,root)
%{libsubdir}/32/libitm.so.*
%endif

%ifarch %quadmath_arch
%files -n libquadmath-32bit
%defattr(-,root,root)
%{libsubdir}/32/libquadmath.so.*
%endif

%ifarch %ubsan_arch
%files -n libubsan-32bit
%defattr(-,root,root)
%{libsubdir}/32/libubsan.so.*
%endif

%files -n libstdc++-32bit
%defattr(-,root,root)
%{libsubdir}/32/libstdc++.so.*
%exclude %{libsubdir}/32/libstdc++.so.*-gdb.py

%files -n libstdc++-devel-32bit
%defattr(-,root,root)
%{libsubdir}/32/libstdc++.so.*-gdb.py
%endif
}

%changelog
