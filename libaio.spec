Name: libaio
Version: 0.3.107
Release: 10%{?dist}
Summary: Linux-native asynchronous I/O access library
License: LGPLv2+
Group:  System Environment/Libraries
Source: %{name}-%{version}.tar.gz
URL: http://git.kernel.org/?p=libs/libaio/libaio.git
BuildRoot: %{_tmppath}/%{name}-root
Patch1: libaio-install-to-slash.patch

%description
The Linux-native asynchronous I/O facility ("async I/O", or "aio") has a
richer API and capability set than the simple POSIX async I/O facility.
This library, libaio, provides the Linux-native API for async I/O.
The POSIX async I/O facility requires this library in order to provide
kernel-accelerated async I/O capabilities, as do applications which
require the Linux-native async I/O API.

%define libdir /%{_lib}
%define usrlibdir %{_prefix}/%{_lib}

%package devel
Summary: Development files for Linux-native asynchronous I/O access
Group: Development/System
Requires: libaio = %{version}-%{release}

%description devel
This package provides header files to include and libraries to link with
for the Linux-native asynchronous I/O facility ("async I/O", or "aio").

%prep
%setup -q -a 0
%patch1 -p1
mv %{name}-%{version} compat-%{name}-%{version}

%build
# A library with a soname of 1.0.0 was inadvertantly released.  This
# build process builds a version of the library with the broken soname in
# the compat-libaio-0.3.103 directory, and then builds the library again
# with the correct soname.
cd compat-%{name}-%{version}
make soname='libaio.so.1.0.0' libname='libaio.so.1.0.0'
cd ..
make

%install
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT
cd compat-%{name}-%{version}
install -D -m 755 src/libaio.so.1.0.0 \
  $RPM_BUILD_ROOT/%{libdir}/libaio.so.1.0.0
cd ..
make destdir=$RPM_BUILD_ROOT prefix=/ libdir=%{libdir} usrlibdir=%{usrlibdir} \
	includedir=%{_includedir} install

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%attr(0755,root,root) %{libdir}/libaio.so.*
%doc COPYING TODO

%files devel
%defattr(-,root,root)
%attr(0644,root,root) %{_includedir}/*
%attr(0755,root,root) %{usrlibdir}/libaio.so*
%attr(0644,root,root) %{_libdir}/libaio.a

%changelog
* Tue Feb 23 2010 Jeff Moyer <jmoyer@redhat.com> - 0.3.107-10
- Fix up packaging guideline problems.
- Resolves bz#567783

* Mon Nov 30 2009 Dennis Gregorovic <dgregor@redhat.com> - 0.3.107-9.1
- Rebuilt for RHEL 6

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.107-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.107-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Jan 20 2009 Jeff Moyer <jmoyer@redhat.com> - 0.3.107-7
- Fix the install to / patch.

* Wed Oct 01 2008 Dennis Gilmore <dennis@ausil.us> - 0.3.107-6
- add patch with sparc support

* Wed Oct 01 2008 Dennis Gilmore <dennis@ausil.us> - 0.3.107-5
- remove ExclusiveArch line

* Wed Sep  3 2008 Jeff Moyer <jmoyer@redhat.com> - 0.3.107-4
- Install to / instead of /usr for early users of libaio (Jeff Moyer)
- Resolves: bz#459158

* Tue Aug  5 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.3.107-3
- fix license tag

* Thu Jun 05 2008 Jeff Moyer <jmoyer@redhat.com> - 0.3.107-2
- Update to the latest upstream which adds eventfd support and fixes broken
  test cases.  (Rusty Russell)

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.3.106-4.2
- Autorebuild for GCC 4.3

* Mon Jul 17 2006 Jeff Moyer <jmoyer@redhat.com> - 0.3.106-3.2
- rebuild

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 0.3.106-3.1
- rebuild

* Wed Jun  7 2006 Jeremy Katz <katzj@redhat.com> - 0.3.106-3
- rebuild for -devel deps

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 0.3.106-2.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 0.3.106-2.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Wed Jan 04 2006 Jeff Moyer <jmoyer@redhat.com> - 0.3.106-2
- Update to the latest sources, which contain the following change:
  Add a .proc directive for the ia64_aio_raw_syscall macro.  This sounds a lot
  like the previous entry, but that one fixed the __ia64_raw_syscall macro,
  located in syscall-ia64.h.  This macro is in raw_syscall.c, which pretty much
  only exists for ia64.  This bug prevented the package from building with
  newer version of gcc.

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Fri Apr  1 2005 Jeff Moyer <jmoyer@redhat.com> - 0.3.104-2
- Add Alpha architecture support.  (Sergey Tikhonov <tsv@solvo.ru>)

* Wed Mar 16 2005 Jeff Moyer <jmoyer@redhat.com> - 0.3.103-6
- Rebuild with gcc 4.

* Mon Feb 14 2005 Jeff Moyer <jmoyer@redhat.com> - 0.3.103-4
- Build the library twice.  Once with the old SONAME and once with the new
  one.  This fixes the wrong SONAME problem by keeping a library around with
  the wrong name (libaio.so.1.0.0) and generating a new one (libaio.so.1.0.1).

* Thu Oct 14 2004 Jeff Moyer <jmoyer@redhat.com> - 0.3.102-1
- update to 102.  Fixes build errors on s390:
  - S390 asm had a bug; I forgot to update the clobber list.  Lucky for me,
    newer compilers complain about such things.
  - Also update the s390 asm to look more like the new kernel variants.

* Wed Oct 13 2004 Jeff Moyer <jmoyer@redhat.com> - 0.3.101-1
- update to 101.  Fixes bz 133253 -  libaio backwards compatibility severely
  broken.

* Tue Sep 14 2004 Jeff Moyer <jmoyer@redhat.com> - 0.3.100-1
- update to 100.  Fixes bz 129910.  Add pseries and iseries to
  exclusivearch.

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Mar 30 2004 Jeff Moyer <jmoyer@redhat.com> - 0.3.99-2
- Apparently the 0.3.93 patch was not meant for 0.3.96.  Backed it out.

* Tue Mar 30 2004 Jeff Moyer <jmoyer@redhat.com> - 0.3.99-1
- Fix compat calls.
- make library .so.1.0.0 and make symlinks properly.
- Fix header file for inclusion in c++ code.

* Thu Feb 26 2004 Jeff Moyer <jmoyer@redhat.com> 0.3.98-2
- bah.  fix version nr in changelog.

* Thu Feb 26 2004 Jeff Moyer <jmoyer@redhat.com> 0.3.98-1
- fix compiler warnings.

* Thu Feb 26 2004 Jeff Moyer <jmoyer@redhat.com> 0.3.97-2
- make srpm was using rpm to do a build.  changed that to use rpmbuild if
  it exists, and fallback to rpm if it doesn't.

* Tue Feb 24 2004 Jeff Moyer <jmoyer@redhat.com> 0.3.97-1
- Use libc syscall(2) instead of rolling our own calling mechanism.  This 
  change is inspired due to a failure to build with newer gcc, since clobber 
  lists were wrong.
- Add -fpic to the CFLAGS for all architectures.  Should address bz #109457.
- change a #include from <linux/types.h> to <sys/types.h>.  Fixes a build
  issue on s390.

* Wed Jul  7 2003 Bill Nottingham <notting@redhat.com> 0.3.96-3
- fix paths on lib64 arches

* Wed Jun 18 2003 Michael K. Johnson <johnsonm@redhat.com> 0.3.96-2
- optimization in io_getevents from Arjan van de Ven in 0.3.96-1
- deal with ia64 in 0.3.96-2

* Wed May 28 2003 Michael K. Johnson <johnsonm@redhat.com> 0.3.95-1
- ppc bugfix from Julie DeWandel

* Tue May 20 2003 Michael K. Johnson <johnsonm@redhat.com> 0.3.94-1
- symbol versioning fix from Ulrich Drepper

* Mon Jan 27 2003 Benjamin LaHaise <bcrl@redhat.com>
- bump to 0.3.93-3 for rebuild.

* Mon Dec 16 2002 Benjamin LaHaise <bcrl@redhat.com>
- libaio 0.3.93 test release
- add powerpc support from Gianni Tedesco <gianni@ecsc.co.uk>
- add s/390 support from Arnd Bergmann <arnd@bergmann-dalldorf.de>

* Fri Sep 12 2002 Benjamin LaHaise <bcrl@redhat.com>
- libaio 0.3.92 test release
- build on x86-64

* Thu Sep 12 2002 Benjamin LaHaise <bcrl@redhat.com>
- libaio 0.3.91 test release
- build on ia64
- remove libredhat-kernel from the .spec file

* Thu Sep  5 2002 Benjamin LaHaise <bcrl@redhat.com>
- libaio 0.3.90 test release

* Mon Apr 29 2002 Benjamin LaHaise <bcrl@redhat.com>
- add requires initscripts >= 6.47-1 to get boot time libredhat-kernel 
  linkage correct.
- typo fix

* Thu Apr 25 2002 Benjamin LaHaise <bcrl@redhat.com>
- make /usr/lib/libredhat-kernel.so point to /lib/libredhat-kernel.so.1.0.0

* Mon Apr 15 2002 Tim Powers <timp@redhat.com>
- make the post scriptlet not use /bin/sh

* Sat Apr 12 2002 Benjamin LaHaise <bcrl@redhat.com>
- add /lib/libredhat-kernel* to %%files.

* Fri Apr 12 2002 Benjamin LaHaise <bcrl@redhat.com>
- make the dummy install as /lib/libredhat-kernel.so.1.0.0 so 
  that ldconfig will link against it if no other is installed.

* Tue Jan 22 2002 Benjamin LaHaise <bcrl@redhat.com>
- add io_getevents

* Tue Jan 22 2002 Michael K. Johnson <johnsonm@redhat.com>
- Make linker happy with /usr/lib symlink for libredhat-kernel.so

* Mon Jan 21 2002 Michael K. Johnson <johnsonm@redhat.com>
- Added stub library

* Sun Jan 20 2002 Michael K. Johnson <johnsonm@redhat.com>
- Initial packaging
