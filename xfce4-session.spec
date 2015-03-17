%define url_ver %(echo %{version} | cut -d. -f1,2)

%define major 0
%define apiver 4.6
%define libname %mklibname xfsm-%{apiver}_%{major}
%define develname %mklibname xfsm -d

Summary:	Xfce Session Manager
Name:		xfce4-session
Version:	4.12.1
Release:	0.1
License:	GPLv2+
Group:		Graphical desktop/Xfce
URL:		http://www.xfce.org
Source0:	http://archive.xfce.org/src/xfce/%{name}/%{url_ver}/%{name}-%{version}.tar.bz2
Source2:	xfce4.pam
Patch0:		xfce4-session-4.9.0-xinitrc.patch
BuildRequires:	perl(XML::Parser)
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(ice)
BuildRequires:	pkgconfig(sm)
BuildRequires:	iceauth
BuildRequires:	pkgconfig(dbus-glib-1)
BuildRequires:	pkgconfig(gconf-2.0)
BuildRequires:	pkgconfig(libxfce4ui-1) >= 4.12
BuildRequires:	pkgconfig(libxfce4util-1.0) >= 4.12
BuildRequires:	pkgconfig(libwnck-1.0)
BuildRequires:	pkgconfig(libxfconf-0) >= 4.12
BuildRequires:	pkgconfig(libsystemd-login)
BuildRequires:	pkgconfig(polkit-gobject-1)
BuildRequires:	pkgconfig(libxfce4panel-1.0) >= 4.12
BuildConflicts:	hal-devel
Requires:	usermode-consoleonly
# (tpg) this satisfies xfce tips&tricks
#Suggests:	fortune-mod
Requires:	polkit-gnome
Requires(pre):	distro-xfce-config-common
Requires(post):	distro-xfce-config-common
Requires:	%{libname} = %{version}
Obsoletes:	xfce-session < 4.5.91
%rename	xfce-utils

%description
The session manager allows the user to save sessions and
restore them after login. It is capable of saving several
different sessions. It comes with three splash screen engines.
And at last it helps you to log out, reboot, and shutdown the system.

%package engines
Summary:	Balou splash engine
Group:		Graphical desktop/Xfce
Requires:	%{name} = %{version}
Obsoletes:	xfce-session-engines

%description engines
Balou is an addidional splash engine for the Xfce.

%package -n %{libname}
Summary:	Libraries for the Xfce Session Manager
Group:		Graphical desktop/Xfce
Obsoletes:	%mklibname xfsm-%{apiver}0
Obsoletes:	%{mklibname xfsm-4.2 0}

%description -n %{libname}
Libraries for xfce-session manager.

%package -n %{develname}
Summary:	Libraries and header files for the Xfce Session Manager
Group:		Development/Other
Requires:	%{libname} = %{version}
Provides:	libxfsm-devel = %{EVRD}
Obsoletes:	%mklibname xfsm-%{apiver}_0 -d

%description -n %{develname}
Libraries and header files for the Xfce Session Manager.

%prep
%setup -q
%apply_patches

%build
NOCONFIGURE=1 xdt-autogen

%configure \
	--enable-legacy-sm \
	--enable-systemd \
	--disable-static

%make

%install
%makeinstall_std

# (tpg) this file is in mandriva-xfce-config package
rm -rf %{buildroot}%{_sysconfdir}/xdg/autostart/xfce4-tips-autostart.desktop
rm -rf %{buildroot}%{_sysconfdir}/xdg/xfce4/xfconf/xfce-perchannel-xml/xfce4-session.xml

# pam
mkdir -p %{buildroot}%{_sysconfdir}/pam.d
install -m 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/pam.d/xfce4

%find_lang %{name} %{name}.lang

%files -f %{name}.lang
%doc AUTHORS BUGS ChangeLog NEWS README TODO
%doc doc/FAQ doc/README.Kiosk
%dir %{_datadir}/themes
%dir %{_datadir}/themes/Default
%{_sysconfdir}/pam.d/xfce4
%{_sysconfdir}/xdg/autostart/*.desktop
%{_sysconfdir}/xdg/xfce4/Xft.xrdb
%{_sysconfdir}/xdg/xfce4/xinitrc
%{_bindir}/*
%{_datadir}/polkit-1/actions/org.xfce.session.policy
%{_datadir}/applications/xfce*
%{_iconsdir}/hicolor/*/apps/*
%{_libdir}/xfce4/session/splash-engines/libmice.*
%{_libdir}/xfce4/session/splash-engines/libsimple.*
%{_libdir}/xfce4/session/xfsm-shutdown-helper
%{_datadir}/xsessions/xfce.desktop
%{_mandir}/man1/*

%files engines
%dir %{_datadir}/themes/Default/balou
%{_libdir}/xfce4/session/balou-export-theme
%{_libdir}/xfce4/session//balou-install-theme
%{_libdir}/xfce4/session/splash-engines/libbalou.*
%{_datadir}/themes/Default/balou/logo.png
%{_datadir}/themes/Default/balou/themerc

%files -n %{libname}
%{_libdir}/*%{apiver}.so.%{major}*

%files -n %{develname}
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/*.pc
%{_includedir}/xfce4/xfce4-session-%{apiver}
