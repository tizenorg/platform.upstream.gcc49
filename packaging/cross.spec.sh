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
%ifarch ia64
BuildRequires: libunwind-devel
%endif
%if 0%{!?gcc_icecream:1}
BuildRequires: cross-%cross_arch-glibc-devel
%endif

# COMMON-BEGIN
# COMMON-END

%if 0%{!?gcc_icecream:1}
make %{?jobs:-j%jobs}
%else
make %{?jobs:-j%jobs} all-host
%endif

%package -n cross-%cross_arch-gcc@base_ver@-icecream-backend
Summary: Icecream backend for the GNU C Compiler
Group:	Development/Languages/C and C++

%description -n cross-%cross_arch-gcc@base_ver@-icecream-backend
This package contains the icecream environment for the GNU C Compiler


%define targetlibsubdir %{_libdir}/gcc/%{gcc_target_arch}/%{gcc_dir_version}

%install
cd obj-%{GCCDIST}

# install and fixup host parts
make DESTDIR=\$RPM_BUILD_ROOT install-host
# with the present setup fixincludes are for the build includes which
# is wrong - get rid of them
rm -rf \$RPM_BUILD_ROOT/%{targetlibsubdir}/include-fixed
rm -f \$RPM_BUILD_ROOT/%{targetlibsubdir}/liblto_plugin.la
# common fixup
rm -f \$RPM_BUILD_ROOT%{_libdir}/libiberty.a

# remove docs
%remove_docs
rm -f \$RPM_BUILD_ROOT/documentation.list


# install and fixup target parts
# ???  don't do this - debugedit is not prepared for this and crashes
# so expect the sysroot to be populated from natively built binaries
#%if 0%{?sysroot:1}
#make DESTDIR=\$RPM_BUILD_ROOT/%{sysroot} install-target
#%else
#make DESTDIR=\$RPM_BUILD_ROOT/%{_prefix}/%{gcc_target_arch} install-target
#%endif


# Build an icecream environment
# The assembler comes from the cross-binutils, and hence is _not_
# named funnily, not even on ppc, so there we need the original target
install -s -D %{_prefix}/bin/%{canonical_target}-tizen-linux%{?canonical_target_abi:%canonical_target_abi}-as \
	\$RPM_BUILD_ROOT/env/usr/bin/as
install -s \$RPM_BUILD_ROOT/%{_prefix}/bin/%{gcc_target_arch}-g++%{binsuffix} \
	\$RPM_BUILD_ROOT/env/usr/bin/g++
install -s \$RPM_BUILD_ROOT/%{_prefix}/bin/%{gcc_target_arch}-gcc%{binsuffix} \
	\$RPM_BUILD_ROOT/env/usr/bin/gcc

for back in cc1 cc1plus; do
	install -s -D \$RPM_BUILD_ROOT/%{targetlibsubdir}/\$back \
		\$RPM_BUILD_ROOT/env%{targetlibsubdir}/\$back
done
if test -f \$RPM_BUILD_ROOT/%{targetlibsubdir}/liblto_plugin.so; then
  install -s -D \$RPM_BUILD_ROOT/%{targetlibsubdir}/liblto_plugin.so \
		\$RPM_BUILD_ROOT/env%{targetlibsubdir}/liblto_plugin.so
fi

# Make sure to also pull in all shared library requirements for the
# binaries we put into the environment which is operated by chrooting
# into it and execing the compiler
libs=\`for bin in \$RPM_BUILD_ROOT/env/usr/bin/* \$RPM_BUILD_ROOT/env%{targetlibsubdir}/*; do \
  ldd \$bin | sed -n '\,^[^/]*\(/[^ ]*\).*,{ s//\1/; p; }'  ;\
done | sort -u\`
for lib in \$libs; do
  # Check wether the same library also exists in the parent directory,
  # and prefer that on the assumption that it is a more generic one.
  baselib=\`echo "\$lib" | sed 's,/[^/]*\(/[^/]*\)\$,\1,'\`
  test -f "\$baselib" && lib=\$baselib
  install -s -D \$lib \$RPM_BUILD_ROOT/env\$lib
done

cd \$RPM_BUILD_ROOT/env
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

%files -n cross-%cross_arch-gcc@base_ver@-icecream-backend
%defattr(-,root,root)
/usr/share/icecream-envs

EOF
