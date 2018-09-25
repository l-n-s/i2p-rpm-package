%ifarch i386
%define wrapper_dir linux
%endif
%ifarch x86_64
%define wrapper_dir linux64
%endif
%ifarch ppc
%define wrapper_dir linux-ppc
%endif

Name:           i2p
Version:        0.9.36
Release:        1%{?dist}
Summary:        Invisible Internet Project (I2P) - anonymous network
Conflicts:      i2pd

License:        GPL
URL:            https://geti2p.net/
Source0:        https://download.i2p2.de/releases/%version/i2psource_%version.tar.bz2

BuildRequires:  java-1.8.0-openjdk-devel 
BuildRequires:  gettext-devel 
BuildRequires:  ant
BuildRequires:  systemd-units

Requires:	systemd
Requires(pre):  %{_sbindir}/useradd %{_sbindir}/groupadd

%description
I2P is an anonymizing network, offering a simple layer that identity-sensitive
applications can use to securely communicate. All data is wrapped with several
layers of encryption, and the network is both distributed and dynamic, with no
trusted parties.

%global debug_package %{nil}

%prep
%setup -q
sed -i '/EnvironmentFile/d' debian/i2p.service
sed -i 's/usr\/sbin\/wrapper/usr\/bin\/i2psvc/' debian/i2p.service
sed -i 's/\$INSTALL_PATH/\/usr\/share\/i2p/' installer/resources/wrapper.config


%build
TZ=UTC JAVA_TOOL_OPTIONS=-Dfile.encoding=UTF8 ant preppkg-linux-only

%install

#wrapper
install -D -m 755 %{_builddir}/%{name}-%{version}/pkg-temp/lib/wrapper/%{wrapper_dir}/i2psvc %{buildroot}%{_bindir}/i2psvc

install -D -m 644 %{_builddir}/%{name}-%{version}/debian/i2p.service %{buildroot}%{_unitdir}/i2p.service

#data
install -d -m 755 %{buildroot}%{_datadir}/i2p
install -D -m 644 %{_builddir}/%{name}-%{version}/history.txt %{buildroot}%{_datadir}/i2p
install -D -m 644 %{_builddir}/%{name}-%{version}/pkg-temp/blocklist.txt %{buildroot}%{_datadir}/i2p
install -D -m 644 %{_builddir}/%{name}-%{version}/pkg-temp/hosts.txt %{buildroot}%{_datadir}/i2p
install -D -m 644 %{_builddir}/%{name}-%{version}/pkg-temp/*.config %{buildroot}%{_datadir}/i2p
install -d -m 755 %{buildroot}%{_datadir}/i2p/lib
install -D -m 644 %{_builddir}/%{name}-%{version}/pkg-temp/lib/*.jar %{buildroot}%{_datadir}/i2p/lib
install -D -m 755 %{_builddir}/%{name}-%{version}/pkg-temp/lib/wrapper/%{wrapper_dir}/libwrapper.so %{buildroot}%{_datadir}/i2p/lib/libwrapper.so
%{__cp} -r %{_builddir}/%{name}-%{version}/pkg-temp/certificates %{buildroot}%{_datadir}/i2p 
%{__cp} -r %{_builddir}/%{name}-%{version}/pkg-temp/docs %{buildroot}%{_datadir}/i2p 
%{__cp} -r %{_builddir}/%{name}-%{version}/pkg-temp/eepsite %{buildroot}%{_datadir}/i2p 
%{__cp} -r %{_builddir}/%{name}-%{version}/pkg-temp/geoip %{buildroot}%{_datadir}/i2p 
%{__cp} -r %{_builddir}/%{name}-%{version}/pkg-temp/locale %{buildroot}%{_datadir}/i2p 
%{__cp} -r %{_builddir}/%{name}-%{version}/pkg-temp/webapps %{buildroot}%{_datadir}/i2p 

#licenses
install -d -m 755 %{buildroot}%{_datadir}/licenses/i2p
%{__cp} -r %{_builddir}/%{name}-%{version}/pkg-temp/licenses/* %{buildroot}%{_datadir}/licenses/i2p

install -d -m 755 %{buildroot}%{_sysconfdir}/i2p
ln -s %{_datadir}/i2p/clients.config %{buildroot}%{_sysconfdir}/i2p/clients.config
ln -s %{_datadir}/i2p/i2psnark.config %{buildroot}%{_sysconfdir}/i2p/i2psnark.config
ln -s %{_datadir}/i2p/i2ptunnel.config %{buildroot}%{_sysconfdir}/i2p/i2ptunnel.config
ln -s %{_datadir}/i2p/systray.config %{buildroot}%{_sysconfdir}/i2p/systray.config
ln -s %{_datadir}/i2p/wrapper.config %{buildroot}%{_sysconfdir}/i2p/wrapper.config

install -d -m 700 %{buildroot}%{_sharedstatedir}/i2p
install -d -m 700 %{buildroot}%{_localstatedir}/log/i2p

%pre
getent group i2psvc >/dev/null || %{_sbindir}/groupadd -r i2psvc
getent passwd i2psvc >/dev/null || \
  %{_sbindir}/useradd -r -g i2psvc -s %{_sbindir}/nologin \
                      -d %{_sharedstatedir}/i2p -c 'I2P Service' i2psvc

%post
%systemd_post i2p.service


%preun
%systemd_preun i2p.service


%postun
%systemd_postun_with_restart i2p.service


%files
# wrappers
%{_bindir}/i2psvc
%{_unitdir}/i2p.service
# configs and data
%defattr(644,i2psvc,i2psvc,755)
%dir  %{_datadir}/i2p
%{_datadir}/i2p/*
%dir  %{_sysconfdir}/i2p
%{_sysconfdir}/i2p/*.config
# misc directories
%dir %{_datadir}/licenses/i2p
%{_datadir}/licenses/i2p/*
%dir  %{_sharedstatedir}/i2p
%dir  %{_localstatedir}/log/i2p

%changelog
* Mon Sep 24 2018 Viktor Villainov <supervillain@riseup.net> - 0.9.36-1
- initial package for version 0.9.36
