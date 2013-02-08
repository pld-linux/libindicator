Summary:	Shared functions for Ayatana indicators
Name:		libindicator
Version:	0.4.94
Release:	1
License:	GPL v3
Group:		Libraries
URL:		https://launchpad.net/libindicator
Source0:	http://launchpad.net/libindicator/0.5/%{version}/+download/%{name}-%{version}.tar.gz
# Source0-md5:	f256d3dccfd2612fb31e19ec42ad1824
BuildRequires:	dbus-glib-devel
BuildRequires:	gtk+2-devel
BuildRequires:	gtk+3-devel
BuildRequires:	gtk-doc
BuildRequires:	libtool
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
A set of symbols and convenience functions that all Ayatana indicators
are likely to use.

%package devel
Summary:	Development files for %{name}
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%package gtk3
Summary:	GTK+3 build of %{name}
Group:		Libraries

%description gtk3
A set of symbols and convenience functions that all Ayatana indicators
are likely to use. This is the GTK+ 3 build of %{name}, for use by
GTK+ 3 apps.

%package gtk3-devel
Summary:	Development files for %{name}-gtk3
Group:		Development/Libraries
Requires:	%{name}-gtk3 = %{version}-%{release}

%description gtk3-devel
The %{name}-gtk3-devel package contains libraries and header files for
developing applications that use %{name}-gtk3.

%prep
%setup -q

%build
# we build it twice, once against GTK+ 3 and once against GTK+ 2, so
# both GTK+ 2 and GTK+ 3 apps can use it; the GTK+ 3 build is
# libindicator-gtk3. When we have no need for the GTK+ 2 build any more
# we can drop the -gtk3 package and have the main package build against
# GTK+ 3.
install -d build-gtk{2,3}
cd build-gtk2
../%configure \
	--disable-static \
	--with-gtk=2
%{__make} \
	V=1

cd ../build-gtk3
../%configure \
	--disable-static \
	--with-gtk=3
%{__make} \
	V=1

%install
rm -rf $RPM_BUILD_ROOT
%{__make} -C build-gtk2 install -j1 \
	DESTDIR=$RPM_BUILD_ROOT
%{__make} -C build-gtk3 install -j1 \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/lib*.la

# this dummy indicator is fairly useless, it's not shipped in Ubuntu
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libdummy-indicator*.so

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig
%post	gtk3 -p /sbin/ldconfig
%postun	gtk3 -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libindicator.so.*.*.*
%ghost %{_libdir}/libindicator.so.7
%attr(755,root,root) %{_libdir}/indicator-loader

%files devel
%defattr(644,root,root,755)
%{_includedir}/libindicator-0.4
%{_libdir}/libindicator.so
%{_pkgconfigdir}/indicator-0.4.pc
# Contains 80indicator-debugging
# This is marked as 'for development use only'
%{_datadir}/libindicator

%files gtk3
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libindicator3.so.*.*.*
%ghost %{_libdir}/libindicator3.so.7
%attr(755,root,root) %{_libdir}/indicator-loader3

%files gtk3-devel
%defattr(644,root,root,755)
%{_includedir}/libindicator3-0.4
%{_libdir}/libindicator3.so
%{_pkgconfigdir}/indicator3-0.4.pc
