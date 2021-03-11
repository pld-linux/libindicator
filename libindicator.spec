Summary:	Shared functions for Ayatana indicators (GTK+ 2.x version)
Summary(pl.UTF-8):	Funkcje współdzielone dla wskaźników Ayatana (wersja dla GTK+ 2.x)
Name:		libindicator
Version:	12.10.1
Release:	3
License:	GPL v3
Group:		Libraries
#Source0Download: https://launchpad.net/libindicator/+download
Source0:	http://launchpad.net/libindicator/12.10/%{version}/+download/%{name}-%{version}.tar.gz
# Source0-md5:	5fd4d6bab339fc9611078b64c44a85a8
Patch0:		%{name}-sh.patch
URL:		https://launchpad.net/libindicator
BuildRequires:	autoconf >= 2.64
BuildRequires:	automake >= 1:1.11
BuildRequires:	glib2-devel >= 1:2.22
BuildRequires:	gtk+2-devel >= 2:2.18
BuildRequires:	gtk+3-devel >= 3.0
BuildRequires:	libtool >= 2:2.2
BuildRequires:	pkgconfig
BuildRequires:	sed >= 4.0
BuildRequires:	which
Requires:	glib2 >= 1:2.22
Requires:	gtk+2 >= 2:2.18
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
A set of symbols and convenience functions that all Ayatana indicators
are likely to use. This package contains GTK+ 2.x version.

%description -l pl.UTF-8
Zbiór symboli i wygodnych funkcji, które mogą być używane przez
wszystkie wskaźniki Ayatana. Ten pakiet zawiera wersję dla GTK+ 2.x.

%package devel
Summary:	Development files for libindicator (GTK+ 2.x version)
Summary(pl.UTF-8):	Pliki programistyczne biblioteki libindicator (wersja dla GTK+ 2.x)
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	glib2-devel >= 1:2.22
Requires:	gtk+2-devel >= 2:2.18

%description devel
This package contains the header files for developing applications
that use libindicator (GTK+ 2.x version).

%description devel -l pl.UTF-8
Ten pakiet zawiera pliki nagłówkowe do tworzenia aplikacji
wykorzystujących bibliotekę libindicator (w wersji dla GTK+ 2.x).

%package gtk3
Summary:	Shared functions for Ayatana indicators (GTK+ 3.x version)
Summary(pl.UTF-8):	Funkcje współdzielone dla wskaźników Ayatana (wersja dla GTK+ 3.x)
Group:		Libraries
Requires:	glib2 >= 1:2.22
Requires:	gtk+3 >= 3.0

%description gtk3
A set of symbols and convenience functions that all Ayatana indicators
are likely to use. This package contains GTK+ 3.x version.

%description gtk3 -l pl.UTF-8
Zbiór symboli i wygodnych funkcji, które mogą być używane przez
wszystkie wskaźniki Ayatana. Ten pakiet zawiera wersję dla GTK+ 3.x.

%package gtk3-devel
Summary:	Development files for libindicator (GTK+ 3.x version)
Summary(pl.UTF-8):	Pliki programistyczne biblioteki libindicator (wersja dla GTK+ 3.x)
Group:		Development/Libraries
Requires:	%{name}-gtk3 = %{version}-%{release}
Requires:	glib2-devel >= 1:2.22
Requires:	gtk+3-devel >= 3.0

%description gtk3-devel
This package contains the header files for developing applications
that use libindicator (GTK+ 3.x version).

%description gtk3-devel -l pl.UTF-8
Ten pakiet zawiera pliki nagłówkowe do tworzenia aplikacji
wykorzystujących bibliotekę libindicator (w wersji dla GTK+ 3.x).

%prep
%setup -q
%patch0 -p1

%{__sed} -i -e 's|-Werror||g' */Makefile.am

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
# we build it twice, once against GTK+ 3 and once against GTK+ 2, so
# both GTK+ 2 and GTK+ 3 apps can use it; the GTK+ 3 build is
# libindicator-gtk3. When we have no need for the GTK+ 2 build any more
# we can drop the -gtk3 package and have the main package build against
# GTK+ 3.
install -d build-gtk{2,3}
cd build-gtk2
../%configure \
	--disable-silent-rules \
	--disable-static \
	--with-gtk=2
%{__make}

cd ../build-gtk3
../%configure \
	--disable-silent-rules \
	--disable-static \
	--with-gtk=3
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build-gtk2 install -j1 \
	DESTDIR=$RPM_BUILD_ROOT
%{__make} -C build-gtk3 install -j1 \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/lib*.la

# dirs for library users, see .pc files for paths
install -d $RPM_BUILD_ROOT%{_libdir}/{indicators,indicators3}/7
install -d $RPM_BUILD_ROOT%{_datadir}/libindicator/icons

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
%doc AUTHORS ChangeLog NEWS
%attr(755,root,root) %{_libdir}/libindicator.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libindicator.so.7
%attr(755,root,root) %{_libexecdir}/indicator-loader
%dir %{_libdir}/indicators
%dir %{_libdir}/indicators/7
%dir %{_datadir}/libindicator
%dir %{_datadir}/libindicator/icons

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libindicator.so
%{_includedir}/libindicator-0.4
%{_pkgconfigdir}/indicator-0.4.pc
# This is marked as 'for development use only'
%{_datadir}/libindicator/80indicator-debugging

%files gtk3
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS
%attr(755,root,root) %{_libdir}/libindicator3.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libindicator3.so.7
%attr(755,root,root) %{_libexecdir}/indicator-loader3
%dir %{_libdir}/indicators3
%dir %{_libdir}/indicators3/7
%dir %{_datadir}/libindicator
%dir %{_datadir}/libindicator/icons

%files gtk3-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libindicator3.so
%{_includedir}/libindicator3-0.4
%{_pkgconfigdir}/indicator3-0.4.pc
