Summary:	NUT multimedia container library
Summary(pl.UTF-8):	Biblioteka obsługująca kontener multimedialny NUT
# "nut" name is already occupied by Network UPS Tools
Name:		libnut
Version:	0
%define	svnver	675
Release:	0.%{svnver}.1
License:	MIT
Group:		Libraries
# svn co svn://svn.mplayerhq.hu/nut/src/trunk nut
Source0:	nut-r%{svnver}.tar.xz
# Source0-md5:	be7a95aa5033fd8d9386902ee9dd83c1
Patch0:		%{name}-make.patch
# dead atm.
#URL:		http://www.nut-container.org/
URL:		http://www.ffmpeg.org/~michael/nut.txt
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
NUT multimedia container library.

%description -l pl.UTF-8
Biblioteka obsługująca kontener multimedialny NUT.

%package devel
Summary:	Header file for NUT library
Summary(pl.UTF-8):	Plik nagłówkowy biblioteki NUT
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header file for NUT library.

%description devel -l pl.UTF-8
Pliki nagłówkowy biblioteki NUT.

%package static
Summary:	Static NUT library
Summary(pl.UTF-8):	Statyczna biblioteka NUT
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static NUT library.

%description static -l pl.UTF-8
Statyczna biblioteka NUT.

%prep
%setup -q -n nut
%patch0 -p1

%build
cat > config.mak <<'EOF'
PREFIX=%{_prefix}
LIBDIR=%{_libdir}
CFLAGS=%{rpmcflags} %{rpmcppflags} -Wall -fPIC
CFLAGS+=-D_LARGEFILE_SOURCE -D_FILE_OFFSET_BITS=64
LDFLAGS=%{rpmldflags}
CC=%{__cc}
RANLIB=ranlib
AR=ar
EOF

%{__make} libnut/libnut.a libnut/libnut.so nututils

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install-libnut-shared install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc COPYING README
%attr(755,root,root) %{_bindir}/nutmerge
%attr(755,root,root) %{_bindir}/nutindex
%attr(755,root,root) %{_bindir}/nutparse
%attr(755,root,root) %{_libdir}/libnut.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libnut.so
%{_includedir}/libnut.h

%files static
%defattr(644,root,root,755)
%{_libdir}/libnut.a
