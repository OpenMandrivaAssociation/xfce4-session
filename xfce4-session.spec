%define url_ver %(echo %{version} | cut -c 1-3)

%define major 0
%define apiver 4.6
%define libname %mklibname xfsm-%{apiver}_%{major}
%define develname %mklibname xfsm -d

Summary:	Xfce Session Manager
Name:		xfce4-session
Version:	4.7.2
Release:	%mkrel 1
License:	GPLv2+
Group:		Graphical desktop/Xfce
URL:		http://www.xfce.org
Source0:	http://archive.xfce.org/src/xfce/%{name}/%{url_ver}/%{name}-%{version}.tar.bz2
# (tpg) fix gnome-keyring support
# http://bugzilla.xfce.org/show_bug.cgi?id=5912
Patch0:		xfce4-session-4.6.1-fix_gnome_keyring_support.patch
Patch1:		xfce4-session-4.7.0-reuse-existing-ConsoleKit-sessions.patch
BuildRequires:	perl(XML::Parser)
BuildRequires:	X11-devel
BuildRequires:	iceauth
BuildRequires:	dbus-glib-devel
BuildRequires:	libGConf2-devel
# (tpg) for patch 6
BuildRequires:	intltool
BuildRequires:	libxfce4ui-devel >= 4.7.0
BuildRequires:	libxfce4util-devel >= 4.7.0
BuildRequires:	libglade2-devel
BuildRequires:	libwnck-devel
Buildrequires:	xfconf-devel >= 4.7.0
# (tpg) needed by patch 9
BuildRequires:	libgnome-keyring-devel >= 2.22
BuildRequires:	consolekit-devel
BuildRequires:	UPower-devel
BuildRequires:	polkit-devel
BuildRequires:	xfce4-panel-devel >= 4.7.0
BuildRequires:	hal-devel
Requires:	usermode-consoleonly
# (tpg) this satisfies xfce tips&tricks
Suggests:	fortune-mod
Requires:	policykit-gnome
Requires(pre):	mandriva-xfce-config
Requires(post):	mandriva-xfce-config
Requires:	%{libname} = %{version}-%{release}
Obsoletes:	xfce-session < 4.5.91
BuildRoot:	%{_tmppath}/%{name}-%{version}-buildroot

%description
The session manager allows the user to save sessions and
restore them after login. It is capable of saving several
different sessions. It comes with three splash screen engines.
And at last it helps you to log out, reboot, and shutdown the system.

%package engines
Summary:	Balou splash engine
Group:		Graphical desktop/Xfce
Requires:	%{name} = %{version}-%{release}
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
Requires:	%{libname} = %{version}-%{release}
Provides:	libxfsm-devel = %{version}-%{release}
Obsoletes:	%mklibname xfsm-%{apiver}_0 -d

%description -n %{develname}
Libraries and header files for the Xfce Session Manager.

%prep
%setup -q
#%patch0 -p1
#%patch1 -p1

%build
%configure2_5x \
	--enable-gnome \
	--enable-session-screenshots \
	--enable-legacy-sm \
	--enable-libgnome-keyring \
	--disable-static
%make

%install
rm -rf %{buildroot}
%makeinstall_std

# Remove devel files from plugins
rm -f %{buildroot}%{_libdir}/xfce4/splash/engines/*.*a

# (tpg) this file is in mandriva-xfce-config package
rm -rf %{buildroot}%{_sysconfdir}/xdg/autostart/xfce4-tips-autostart.desktop
rm -rf %{buildroot}%{_sysconfdir}/xdg/xfce4/xfconf/xfce-perchannel-xml/xfce4-session.xml

%find_lang %{name}

%clean
rm -rf %{buildroot}

%files -f %{name}.lang
%defattr(-,root,root)
%doc AUTHORS BUGS ChangeLog NEWS README TODO
%doc doc/FAQ doc/README.Kiosk
%dir %{_datadir}/themes
%dir %{_datadir}/themes/Default
%{_bindir}/*
%{_datadir}/applications/xfce*
%{_iconsdir}/hicolor/*/apps/*
%{_datadir}/xfce4/tips/tips
%{_datadir}/xfce4/panel-plugins/xfsm-*.desktop
%{_libdir}/xfce4/panel/plugins/libxfsm-*
%{_libdir}/xfce4/session/splash-engines/libmice.*
%{_libdir}/xfce4/session/splash-engines/libsimple.*
%{_libdir}/xfce4/session/xfsm-shutdown-helper
%{_mandir}/man1/*

%files engines
%defattr(-,root,root)
%dir %{_datadir}/themes/Default/balou
%{_libdir}/xfce4/session/balou-export-theme
%{_libdir}/xfce4/session//balou-install-theme
%{_libdir}/xfce4/session/splash-engines/libbalou.*
%{_datadir}/themes/Default/balou/logo.png
%{_datadir}/themes/Default/balou/themerc

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/*%{apiver}.so.%{major}*

%files -n %{develname}
%defattr(-,root,root)
%{_libdir}/lib*.so
%{_libdir}/*.la
%{_libdir}/pkgconfig/*.pc
%{_includedir}/xfce4/xfce4-session-%{apiver}
