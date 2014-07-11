# TODO:
# Not packaged:
# /usr/include/KF5
# /usr/share/kservicetypes5

%define         _state          stable
%define		orgname		kinit

Summary:	Helper library to speed up start of applications on KDE workspaces
Name:		kf5-%{orgname}
Version:	5.0.0
Release:	0.1
License:	LGPL v2.1+
Group:		X11/Libraries
Source0:	ftp://ftp.kde.org/pub/kde/%{_state}/frameworks/%{version}/%{orgname}-%{version}.tar.xz
# Source0-md5:	09860896223814082037a184fe1fdcb9
URL:		http://www.kde.org/
BuildRequires:	cmake >= 2.8.12
BuildRequires:	gettext-devel
BuildRequires:	kf5-extra-cmake-modules >= 1.0.0
BuildRequires:	libcap-devel
BuildRequires:	rpmbuild(macros) >= 1.164
BuildRequires:	tar >= 1:1.22
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	xz
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		qt5dir		%{_libdir}/qt5

%description
kdeinit is a process launcher somewhat similar to the famous init used
for booting UNIX.

It launches processes by forking and then loading a dynamic library
which should contain a 'kdemain(...)' function.

Using kdeinit to launch KDE applications makes starting a typical KDE
applications 2.5 times faster (100ms instead of 250ms on a P-III 500)
It reduces memory consumption by approx. 350Kb per application.

%package devel
Summary:	Header files for %{orgname} development
Summary(pl.UTF-8):	Pliki nagłówkowe dla programistów używających %{orgname}
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for %{orgname} development.

%description devel -l pl.UTF-8
Pliki nagłówkowe dla programistów używających %{orgname}.

%prep
%setup -q -n %{orgname}-%{version}

%build
install -d build
cd build
%cmake \
	-DBIN_INSTALL_DIR=%{_bindir} \
	-DKCFG_INSTALL_DIR=%{_datadir}/config.kcfg \
	-DPLUGIN_INSTALL_DIR=%{qt5dir}/plugins \
	-DQT_PLUGIN_INSTALL_DIR=%{qt5dir}/plugins \
	-DQML_INSTALL_DIR=%{qt5dir}/qml \
	-DIMPORTS_INSTALL_DIR=%{qt5dirs}/imports \
	-DSYSCONF_INSTALL_DIR=%{_sysconfdir} \
	-DLIBEXEC_INSTALL_DIR=%{_libexecdir} \
	-DKF5_LIBEXEC_INSTALL_DIR=%{_libexecdir} \
	-DKF5_INCLUDE_INSTALL_DIR=%{_includedir} \
	-DECM_MKSPECS_INSTALL_DIR=%{qt5dir}/mkspecs/modules \
	-D_IMPORT_PREFIX=%{_prefix} \
	../
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build/ install \
        DESTDIR=$RPM_BUILD_ROOT

%find_lang %{orgname}5

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files -f %{orgname}5.lang
%defattr(644,root,root,755)
%doc README.md
%attr(755,root,root) %{_bindir}/kdeinit5
%attr(755,root,root) %{_bindir}/kdeinit5_shutdown
%attr(755,root,root) %{_bindir}/kdeinit5_wrapper
%attr(755,root,root) %{_bindir}/kshell5
%attr(755,root,root) %{_bindir}/kwrapper5
%attr(755,root,root) %{_libdir}/kf5/klauncher
%attr(755,root,root) %{_libdir}/kf5/start_kdeinit
%attr(755,root,root) %{_libdir}/kf5/start_kdeinit_wrapper
%attr(755,root,root) %{_libdir}/libkdeinit5_klauncher.so
%{_datadir}/dbus-1/interfaces/kf5_org.kde.KLauncher.xml
%{_mandir}/man8/kdeinit5.8*

%files devel
%defattr(644,root,root,755)
%{_libdir}/cmake/KF5Init
