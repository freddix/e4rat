Summary:	Toolset to accelerate the boot process and application startups
Name:		e4rat
Version:	0.2.3
Release:	1
License:	GPL
Group:		Applications
Source0:	http://downloads.sourceforge.net/project/%{name}/%{version}/%{name}_%{version}_src.tar.gz
# Source0-md5:	e8e7db69018036f11d509b65c32d3ea4
Patch0:		%{name}-boostfsv3.patch
Patch1:		%{name}-shared-build.patch
Patch2:		%{name}-libdir.patch
Patch3:		%{name}-defaults.patch
URL:		http://e4rat.sourceforge.net/
BuildRequires:	audit-devel
BuildRequires:	boost-devel
BuildRequires:	cmake
BuildRequires:	e2fsprogs-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
e4rat ("Ext4 - Reducing Access Times") is a toolset to accelerate the
boot process as well as application startups. Through physical file
realloction e4rat eliminates both seek times and rotational delays.
This leads to a high disk transfer rate. Placing files on disk in a
sequentially ordered way allows to efficiently read-ahead files in
parallel to the program startup. The combination of sequentially
reading and a high cache hit rate may reduce the boot time by a factor
of three, as the example below shows.

e4rat is based on the online defragmentation ioctl EXT4_IOC_MOVE_EXT
from the Ext4 filesystem, which was introduced in Linux Kernel 2.6.31.
Other filesystem types and/or earlier versions of extended filesystems
are not supported.

%prep
%setup -q
%patch0 -p0
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
install -d build
cd build
%cmake .. \
	-DBOOST_LIBRARYDIR=%{_libdir}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /usr/sbin/ldconfig
%postun	-p /usr/sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README
%attr(755,root,root) %{_sbindir}/e4rat-collect
%attr(755,root,root) %{_sbindir}/e4rat-preload
%attr(755,root,root) %{_sbindir}/e4rat-realloc
%attr(755,root,root) %{_libdir}/libe4rat-core.so.0
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/e4rat.conf
%{_mandir}/man[58]/*.[58]*

