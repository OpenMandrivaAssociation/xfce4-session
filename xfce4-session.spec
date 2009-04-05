%define major 0
%define apiver 4.6
%define libname %mklibname xfsm-%{apiver}_%{major}
%define develname %mklibname xfsm -d

Summary:	Xfce Session Manager
Name:		xfce4-session
Version:	4.6.0
Release:	%mkrel 3
License:	GPLv2+
Group:		Graphical desktop/Xfce
URL:		http://www.xfce.org
Source0:	http://www.xfce.org/archive/xfce-%{version}/src/%{name}-%{version}.tar.bz2
Patch0:		xfce4-session-4.6.0-dont-crash-when-null-ponter-is-passed.patch
Patch1:		xfce4-session-4.6.0-fix-default-value-for-enabletcp.patch
BuildRequires:	perl(XML::Parser)
BuildRequires:	X11-devel
BuildRequires:	iceauth
BuildRequires:	dbus-glib-devel
BuildRequires:	libGConf2-devel
# (tpg) for patch 6
BuildRequires:	intltool
BuildRequires:	libxfcegui4-devel >= %{version}
BuildRequires:	libglade2-devel
BuildRequires:	libwnck-devel
Buildrequires:	xfconf-devel >= %{version}
# (tpg) needed by patch 9
BuildRequires:	libgnome-keyring-devel >= 2.22
Requires:	usermode-consoleonly
# (tpg) this satisfies xfce tips&tricks
Suggests:	fortune-mod
%if %mdkversion <= 200900
Requires:	pm-utils
%endif
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
%patch0 -p1
%patch1 -p1

%build
%configure2_5x \
%if %mdkversion < 200900
	--sysconfdir=%{_sysconfdir}/X11 \
%endif
        --enable-final \
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
rm -f %{buildroot}/%{_libdir}/xfce4/splash/engines/*.*a

%find_lang %{name}

%clean
rm -rf %{buildroot}

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif
%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%post
%{update_menus}
%update_icon_cache hicolor
%endif

%if %mdkversion < 200900
%postun
%{clean_menus}
%clean_icon_cache hicolor
%endif

%files -f %{name}.lang
%defattr(-,root,root)
%doc AUTHORS BUGS ChangeLog ChangeLog.pre-xfce-devel NEWS README TODO
%doc doc/FAQ doc/README.Kiosk doc/C/xfce4*
%doc %dir %{_datadir}/xfce4/doc/*/*.html
%doc %dir %{_datadir}/xfce4/doc/*/images/*
%dir %{_datadir}/themes
%dir %{_datadir}/themes/Default
%if %mdkversion < 200900
%exclude %{_sysconfdir}/X11/xdg/autostart/xfce4-tips-autostart.desktop
%else
%exclude %{_sysconfdir}/xdg/autostart/xfce4-tips-autostart.desktop
%endif
%exclude %{_sysconfdir}/xdg/xfce4/xfconf/xfce-perchannel-xml/xfce4-session.xml
%{_bindir}/*
%{_datadir}/applications/xfce*
%{_iconsdir}/hicolor/*/apps/*
%{_datadir}/xfce4/tips/tips*
%{_libdir}/xfce4/splash/engines/libmice.so
%{_libdir}/xfce4/splash/engines/libsimple.so
%{_libdir}/xfsm-shutdown-helper
%{_mandir}/man1/*

%files engines
%defattr(-,root,root)
%dir %{_datadir}/themes/Default/balou
%{_libdir}/balou-export-theme
%{_libdir}/balou-install-theme
%{_libdir}/xfce4/splash/engines/libbalou.so
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
