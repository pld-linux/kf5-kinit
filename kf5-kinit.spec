%define		kdeframever	5.67
%define		qtver		5.9.0
%define		kfname		kinit

Summary:	Helper library to speed up start of applications on KDE workspaces
Name:		kf5-%{kfname}
Version:	5.67.0
Release:	1
License:	LGPL v2.1+
Group:		X11/Libraries
Source0:	http://download.kde.org/stable/frameworks/%{kdeframever}/%{kfname}-%{version}.tar.xz
# Source0-md5:	646771a2d35f1af7c5d0f4cfb3f80179
URL:		http://www.kde.org/
BuildRequires:	cmake >= 2.8.12
BuildRequires:	gettext-devel
BuildRequires:	kf5-extra-cmake-modules >= 1.4.0
BuildRequires:	kf5-kio-devel >= %{version}
BuildRequires:	libcap-devel
BuildRequires:	ninja
BuildRequires:	rpmbuild(macros) >= 1.164
BuildRequires:	tar >= 1:1.22
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	xz
Requires:	kf5-dirs
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
Summary:	Header files for %{kfname} development
Summary(pl.UTF-8):	Pliki nagłówkowe dla programistów używających %{kfname}
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for %{kfname} development.

%description devel -l pl.UTF-8
Pliki nagłówkowe dla programistów używających %{kfname}.

%prep
%setup -q -n %{kfname}-%{version}

%build
install -d build
cd build
%cmake -G Ninja \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON \
	../
%ninja_build

%install
rm -rf $RPM_BUILD_ROOT
%ninja_install -C build

%find_lang %{kfname}5

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files -f %{kfname}5.lang
%defattr(644,root,root,755)
%doc README.md
%attr(755,root,root) %{_bindir}/kdeinit5
%attr(755,root,root) %{_bindir}/kdeinit5_shutdown
%attr(755,root,root) %{_bindir}/kdeinit5_wrapper
%attr(755,root,root) %{_bindir}/kshell5
%attr(755,root,root) %{_bindir}/kwrapper5
%attr(755,root,root) %{_libexecdir}/kf5/klauncher
%attr(755,root,root) %{_libexecdir}/kf5/start_kdeinit
%attr(755,root,root) %{_libexecdir}/kf5/start_kdeinit_wrapper
%attr(755,root,root) %{_libdir}/libkdeinit5_klauncher.so
%{_datadir}/dbus-1/interfaces/kf5_org.kde.KLauncher.xml
%{_datadir}/qlogging-categories5/kinit.categories
%{_mandir}/man8/kdeinit5.8*
%lang(ca) %{_mandir}/ca/man8/kdeinit5.8*
%lang(de) %{_mandir}/de/man8/kdeinit5.8*
%lang(es) %{_mandir}/es/man8/kdeinit5.8*
%lang(it) %{_mandir}/it/man8/kdeinit5.8*
%lang(nl) %{_mandir}/nl/man8/kdeinit5.8*
%lang(pt) %{_mandir}/pt/man8/kdeinit5.8*
%lang(pt_BR) %{_mandir}/pt_BR/man8/kdeinit5.8*
%lang(sv) %{_mandir}/sv/man8/kdeinit5.8*
%lang(uk) %{_mandir}/uk/man8/kdeinit5.8*

%files devel
%defattr(644,root,root,755)
%{_libdir}/cmake/KF5Init
