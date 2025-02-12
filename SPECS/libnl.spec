Summary: Convenience library for kernel netlink sockets
Group: Development/Libraries
License: LGPLv2
Name: libnl
Version: 1.1.4
Release: 4%{?dist}
URL: http://www.infradead.org/~tgr/libnl/
Source: http://www.infradead.org/~tgr/libnl/files/libnl-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: doxygen
Patch0: libnl-1.0-pre8-more-build-output.patch
Patch1: libnl-1.1-doc-inlinesrc.patch
Patch2: CVE-2017-0553.patch

%description
This package contains a convenience library to simplify
using the Linux kernel's netlink sockets interface for
network manipulation

%package devel
Summary: Libraries and headers for using libnl
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: kernel-headers

%description devel
This package contains various headers for using libnl


%prep
%setup -q -n %{name}-%{version}
%patch0 -p1 -b .more-build-output
%patch1 -p1 -b .doc-inlinesrc
%patch2 -p1 -b .cve-2017-553

# a quick hack to make doxygen stripping builddir from html outputs.
sed -i.org -e "s,^STRIP_FROM_PATH.*,STRIP_FROM_PATH = `pwd`," doc/Doxyfile.in

%build
%configure
make
make gendoc

%install
%{__rm} -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

rm $RPM_BUILD_ROOT%{_libdir}/libnl.a

mkdir $RPM_BUILD_ROOT/%{_lib}
mv $RPM_BUILD_ROOT%{_libdir}/libnl.so.* $RPM_BUILD_ROOT/%{_lib}
for l in $RPM_BUILD_ROOT%{_libdir}/libnl.so; do
    ln -sf $(echo %{_libdir} | \
        sed 's,\(^/\|\)[^/][^/]*,..,g')/%{_lib}/$(readlink $l) $l
done

%clean
%{__rm} -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
/%{_lib}/%{name}.so.*
%doc COPYING

%files devel
%defattr(-,root,root,0755)
%{_includedir}/netlink/
%doc doc/html
%{_libdir}/%{name}.so
%{_libdir}/pkgconfig/%{name}-1.pc

%changelog
* Mon Jul 15 2024 Matt Hink <mhink@ciq.com> - 1.1.4-4
- Fix CVE-2017-0553

* Fri Jan 24 2014 Daniel Mach <dmach@redhat.com> - 1.1.4-3
- Mass rebuild 2014-01-24

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 1.1.4-2
- Mass rebuild 2013-12-27

* Tue May 07 2013 Thomas Graf <tgraf@redhat.com> - 1.1.4-1
- Update to latest stable release 1.1.4

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Mar 21 2011 Dan Williams <dcbw@redhat.com> - 1.1-14
- Fix portmap position calculation (rh #677526) (rh #677725)
- Make port allocation threadsafe (rh #677527) (rh #677724)

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon May 24 2010 Tom "spot" Callaway <tcallawa@redhat.com> - 1.1-12
- disable static by default (if you really want static lib, --enable-static)

* Thu May 13 2010 Dan Williams <dcbw@redhat.com> - 1.1-11
- Update source link for package review (rh #592042)

* Fri Feb 26 2010 Dennis Gilmore <dennis@ausil.us> - 1.1-10
- add patch for alignment issues

* Tue Dec 22 2009 John W. Linville <linville@redhat.com> - 1.1-9
- Install libnl into /%{_lib} instead of %{_libdir}

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu May 14 2009 Peter Jones <pjones@redhat.com> - 1.1-7
- Don't present "extern inline nl_object_priv();" to consumers in the headers.

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Jun 27 2008 Dan Williams <dcbw@redhat.com> - 1.1-5
- Build documentation in -devel package (rh #452646)

* Thu May 29 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.1-4
- fix license tag

* Fri Feb 22 2008 Dan Williams <dcbw@redhat.com> - 1.1-3
- Include limits.h to fix gcc 4.3 rebuild issues (rh #434055)

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.1-2
- Autorebuild for GCC 4.3

* Wed Jan 23 2008 Dan Williams <dcbw@redhat.com> - 1.1-1
- Update to version 1.1

* Tue Dec 18 2007 Dan Williams <dcbw@redhat.com> - 1.0-0.15.pre8.git20071218
- Handle removal of include/linux/ip_mp_alg.h in 2.6.24

* Tue Dec 18 2007 Dan Williams <dcbw@redhat.com> - 1.0-0.14.pre8.git20071217
- devel package should require kernel-headers

* Mon Dec 17 2007 Dan Williams <dcbw@redhat.com> - 1.0-0.13.pre8.git20071217
- Add dist tag to revision 

* Mon Dec 17 2007 Dan Williams <dcbw@redhat.com> - 1.0-0.12.pre8.git20071217
- Update to -pre8 + fixes (rh #401761)

* Mon Aug 14 2006 Peter Jones <pjones@redhat.com> - 1.0-0.10.pre5.4
- Fix nl_recv() for ppc64

* Mon Jul 31 2006 Jeremy Katz <katzj@redhat.com> - 1.0-0.10.pre5.3
- unbreak the pkgconfig file

* Wed Jul 26 2006 Matthias Clasen <mclasen@redhat.com> - 1.0-0.10.pre5.2
- Fix the pkgconfig file on 64-bit systems (#197176)

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1.0-0.10.pre5.1
- rebuild

* Thu Jun 15 2006 Peter Jones <pjones@redhat.com> 1.0-0.10.pre5
- Fix debuginfo generation.

* Fri May 26 2006 Jason Vas Dias <jvdias@redhat.com> 1.0-0.9.pre5
- Allow build to succeed with new gcc / glibc-kernheaders
  (compile failed on __u64 redefinition on x86_64).
- Add a static %{_libdir}/libnl.a library to libnl-devel for
  programs that might need to do a static link to libnl.
  Added after consultation with Christopher Aillon.

* Tue Feb 12 2006 Christopher Aillon <caillon@redhat.com> 1.0-0.8.pre5
- Rebuild

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> 1.0-0.7.pre5.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Mon Jan 16 2006 Christopher Aillon <caillon@redhat.com> 1.0-0.7.pre5
- Add patch to not chown files to root.root during make install; it
  happens normally.

* Mon Jan  9 2006 Christopher Aillon <caillon@redhat.com> 1.0-0.6.pre5
- Correctly install the pkgconfig file

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Wed Nov  2 2005 Christopher Aillon <caillon@redhat.com> 1.0-0.5.pre5
- Fix 64bit LIBDIR issue; use $LIBDIR instead of $PREFIX/lib

* Wed Nov  2 2005 Christopher Aillon <caillon@redhat.com> 1.0-0.4.pre5
- Update to 1.0-pre5

* Tue Nov  1 2005 Christopher Aillon <caillon@redhat.com> 1.0-0.3.pre4
- Update to 1.0-pre4

* Tue Nov  1 2005 Christopher Aillon <caillon@redhat.com> 1.0-0.2.pre3
- Minor specfile cleanup

* Thu Oct 27 2005 Dan Williams <dcbw@redhat.com> 1.0-0.1.pre3
- Split into main and devel packages

* Thu Oct 27 2005 Dan Williams <dcbw@redhat.com> 1.0-0.0.pre3
- initial build
