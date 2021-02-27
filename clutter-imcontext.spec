#
# Conditional build:
%bcond_without	apidocs		# do not build and package API docs
%bcond_without	static_libs	# don't build static libraries

%define	snap	20100323
%define	rel	3
Summary:	IMContext Framework Library for Clutter
Summary(pl.UTF-8):	Biblioteka szkieletu IMContext dla Cluttera
Name:		clutter-imcontext
Version:	0.1.6
Release:	0.%{snap}.%{rel}
License:	LGPL v2.1
Group:		Libraries
# git clone git://git.moblin.org/clutter-imcontext
Source0:	%{name}.tar.xz
# Source0-md5:	f2b1781516c1a2928693fcfe9e954928
URL:		http://www.moblin.org/
BuildRequires:	autoconf >= 2.61
BuildRequires:	automake
BuildRequires:	clutter-devel >= 1.0.0
BuildRequires:	glib2-devel >= 2
BuildRequires:	gtk-doc >= 1.9
BuildRequires:	libtool
BuildRequires:	pkgconfig
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
IMContext Framework Library for Clutter.

%description -l pl.UTF-8
Biblioteka szkieletu IMContext dla Cluttera.

%package devel
Summary:	Header files for Clutter IMContext library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki Clutter IMContext
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for Clutter IMContext library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki Clutter IMContext.

%package static
Summary:	Static Clutter IMContext library
Summary(pl.UTF-8):	Statyczna biblioteka Clutter IMContext
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static Clutter IMContext library.

%description static -l pl.UTF-8
Statyczna biblioteka Clutter IMContext.

%package apidocs
Summary:	Clutter IMContext API documentation
Summary(pl.UTF-8):	Dokumentacja API biblioteki Clutter IMContext
Group:		Documentation
BuildArch:	noarch

%description apidocs
API and internal documentation for Clutter IMContext library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki Clutter IMContext.

%prep
%setup -q -n %{name}

%build
%{__gtkdocize}
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	%{!?with_static_libs:--disable-static} \
	%{?with_apidocs:--enable-gtk-doc} \
	--with-html-dir=%{_gtkdocdir}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libclutter-imcontext-0.1.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog
%attr(755,root,root) %{_bindir}/clutter-scan-immodules
%attr(755,root,root) %{_libdir}/libclutter-imcontext-0.1.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libclutter-imcontext-0.1.so.0
%dir %{_sysconfdir}/clutter-imcontext
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/clutter-imcontext/enable_autoshow

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libclutter-imcontext-0.1.so
%{_includedir}/clutter-imcontext-0.1
%{_pkgconfigdir}/clutter-imcontext-0.1.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libclutter-imcontext-0.1.a
%endif

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/clutter-imcontext
%endif
