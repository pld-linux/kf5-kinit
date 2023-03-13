#
# Conditional build:
%bcond_with	tests		# build with tests
%define		kdeframever	5.104
%define		qtver		5.15.2
%define		kfname		kinit

Summary:	Helper library to speed up start of applications on KDE workspaces
Name:		kf5-%{kfname}
Version:	5.104.0
Release:	1
License:	LGPL v2.1+
Group:		X11/Libraries
Source0:	https://download.kde.org/stable/frameworks/%{kdeframever}/%{kfname}-%{version}.tar.xz
# Source0-md5:	448714f06ebcdbf9b8c3835226525f96
URL:		http://www.kde.org/
BuildRequires:	Qt5Core-devel >= %{qtver}
BuildRequires:	Qt5DBus-devel >= %{qtver}
BuildRequires:	Qt5Gui-devel >= %{qtver}
BuildRequires:	cmake >= 3.5
BuildRequires:	kf5-extra-cmake-modules >= %{version}
BuildRequires:	kf5-kconfig-devel >= %{version}
BuildRequires:	kf5-kcrash-devel >= %{version}
BuildRequires:	kf5-kdbusaddons-devel >= %{version}
BuildRequires:	kf5-kdoctools-devel >= %{version}
BuildRequires:	kf5-ki18n-devel >= %{version}
BuildRequires:	kf5-kio-devel >= %{version}
BuildRequires:	kf5-kservice-devel >= %{version}
BuildRequires:	kf5-kwindowsystem-devel >= %{version}
BuildRequires:	libcap-devel
BuildRequires:	libxcb-devel
BuildRequires:	ninja
BuildRequires:	rpmbuild(macros) >= 1.736
BuildRequires:	tar >= 1:1.22
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	xz
Requires:	Qt5Core >= %{qtver}
Requires:	Qt5DBus >= %{qtver}
Requires:	Qt5Gui >= %{qtver}
Requires:	kf5-dirs
Requires:	kf5-kconfig >= %{version}
Requires:	kf5-kcrash >= %{version}
Requires:	kf5-kdbusaddons >= %{version}
Requires:	kf5-ki18n >= %{version}
Requires:	kf5-kio >= %{version}
Requires:	kf5-kservice >= %{version}
Requires:	kf5-kwindowsystem >= %{version}
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
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON \
	../
%ninja_build

%if %{with tests}
ctest
%endif


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
%lang(fr) %{_mandir}/fr/man8/kdeinit5.8*
%{_datadir}/qlogging-categories5/kinit.renamecategories

%files devel
%defattr(644,root,root,755)
%{_libdir}/cmake/KF5Init
