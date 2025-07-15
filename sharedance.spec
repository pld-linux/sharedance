#
# TODO: maybe run as no root user
#
Summary:	Server that centralize ephemeral key/data pairs on remote hosts
Summary(pl.UTF-8):	Serwer centralizujący efemeryczne pary kluczy/danych na zdalnych maszynach
Name:		sharedance
Version:	0.6
Release:	0.6
License:	distributable
Group:		Daemons
Source0:	http://download.pureftpd.org/pub/sharedance/%{name}-%{version}.tar.bz2
# Source0-md5:	73e60374cc04a825090530e90ce3e2ba
Source1:	%{name}.init
Source2:	%{name}.sysconfig
Patch0:		%{name}-nolocal.patch
URL:		http://sharedance.pureftpd.org/project/sharedance/
BuildRequires:	rpmbuild(macros) >= 1.228
Requires(post,preun):	/sbin/chkconfig
BuildRequires:	autoconf >= 2.58
BuildRequires:	automake
#Provides:	group(foo)
#Provides:	user(foo)
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Sharedance is a high-performance server that centralize ephemeral
key/data pairs on remote hosts, without the overhead and the
complexity of an SQL database.

It was mainly designed to share caches and sessions between a pool of
web servers. Access to a sharedance server is trivial through a simple
PHP API and it is compatible with the expectations of PHP 4 and PHP 5
session handlers.

%description -l pl.UTF-8
sharedance to wysoko wydajny serwer centralizujący efemeryczne pary
kluczy/danych na zdalnych maszynach bez narzutu i złożoności bazy
danych SQL.

Został zaprojektowany głównie do współdzielenia pamięci podręcznej i
sesji między pulą serwerów WWW. Dostęp do serwera sharedance jest
trywialny poprzez proste API PHP i jest kompatybilne z oczekiwaniami
funkcji obsługi sesji w PHP 4 i PHP 5.

%prep
%setup -q
%patch -P0 -p1

%build
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--with-largefile

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/{sysconfig,rc.d/init.d}
install -d $RPM_BUILD_ROOT/var/cache/%{name}d

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}d
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/%{name}d

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add %{name}d
%service %{name}d restart

%preun
if [ "$1" = "0" ]; then
	%service -q %{name}d stop
	/sbin/chkconfig --del %{name}d
fi

%files
%defattr(644,root,root,755)
%doc AUTHORS COPYING ChangeLog NEWS README php/*.php
%attr(755,root,root) %{_sbindir}/*
%attr(754,root,root) /etc/rc.d/init.d/%{name}d
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/%{name}d
%attr(750,root,root) %dir /var/cache/%{name}d
