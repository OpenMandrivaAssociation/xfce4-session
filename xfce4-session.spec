%define major 0
%define apiversion 4.2
%define libname %mklibname xfsm-%{apiversion}_%{major}
%define develname %mklibname xfsm -d

Summary:	Xfce Session Manager
Name:		xfce4-session
Version:	4.4.2
Release:	%mkrel 13
License:	GPLv2+
Group:		Graphical desktop/Xfce
URL:		http://www.xfce.org
Source0:	%{name}-%{version}.tar.bz2
Source1:	%{name}-icons.tar.bz2
# (saispo) logout dialogbox patch from Xubuntu
Patch0:         %{name}-4.4.1-logout_dialog.patch
# (saispo) default mandriva theme
Patch4:		%{name}-4.4.1-session-options.patch
Patch6:		%{name}-asneeded.patch
Patch7:		%{name}-4.4.2-icons.patch
Patch8:		%{name}-4.4.1-use-GtkFileChooser.patch
# (tpg) http://bugzilla.xfce.org/show_bug.cgi?id=3007
Patch9:		%{name}-4.4.2-gnome-keyring-compat.patch
Patch10:	%{name}-4.4.2-speed-up-startup.patch
Patch11:	%{name}-4.4.2-use-dbus-glib.patch
Patch12:	%{name}-4.4.2-update-translations.patch
BuildRequires:	xfce-mcs-manager-devel >= %{version}
BuildRequires:	libgdk_pixbuf2.0-devel
BuildRequires:	perl(XML::Parser)
BuildRequires:	X11-devel
BuildRequires:	iceauth
BuildRequires:	dbus-glib-devel
BuildRequires:	libGConf2-devel
# (tpg) for patch 6
BuildRequires:	intltool
BuildRequires:	xfce4-dev-tools
# (tpg) needed by patch 9
BuildRequires:	libgnome-keyring-devel >= 2.22
Requires:	xfce-mcs-manager >= %{version}
#Requires:	usermode-consoleonly
# (tpg) this satisfies xfce tips&tricks
Suggests:	fortune-mod
Requires:	pm-utils
Suggests:	sudo
Requires:	%{libname} = %{version}-%{release}
Obsoletes:	xfce-session
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
Obsoletes:	%mklibname xfsm-%{apiversion}0

%description -n %{libname}
Libraries for xfce-session manager

%package -n %{develname}
Summary:	Libraries and header files for the Xfce Session Manager
Group:		Development/Other
Requires:	%{libname} = %{version}-%{release}
Provides:	libxfsm-devel = %{version}-%{release}
Obsoletes:	%mklibname xfsm-%{apiversion}_0 -d

%description -n %{develname}
Libraries and header files for the Xfce Session Manager.

%prep
%setup -q -a 1
%patch0 -p1
%patch4 -p1 -b .mandriva
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1
%patch11 -p1
%patch12 -p1

%build
# (tpg) for patch 6 and 9 and 11
NOCONFIGURE=1 xdt-autogen

%configure2_5x \
%if %mdkversion < 200900
	--sysconfdir=%{_sysconfdir}/X11 \
%endif
	--with-shutdown-style=hal \
        --enable-final \
	--enable-gnome \
	--enable-dbus \
	--enable-session-screenshots \
	--enable-legacy-sm
%make

%install
rm -rf %{buildroot}
%makeinstall_std

# Remove devel files from plugins
rm -f %{buildroot}/%{_libdir}/xfce4/splash/engines/*.*a \
	%{buildroot}/%{_libdir}/xfce4/mcs-plugins/*.*a

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
%dir %{_sysconfdir}/X11/xdg/xfce4-session
%config(noreplace) %{_sysconfdir}/X11/xdg/xfce4-session/xfce4-session.rc
%exclude %{_sysconfdir}/X11/xdg/autostart/xfce4-tips-autostart.desktop
%else
%dir %{_sysconfdir}/xdg/xfce4-session
%config(noreplace) %{_sysconfdir}/xdg/xfce4-session/xfce4-session.rc
%exclude %{_sysconfdir}/xdg/autostart/xfce4-tips-autostart.desktop
%endif
%{_bindir}/*
%{_datadir}/applications/xfce*
%{_iconsdir}/hicolor/*/apps/*
%{_datadir}/xfce4/tips/tips*
%{_libdir}/xfce4/mcs-plugins/*.so
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
%{_libdir}/*%{apiversion}.so.%{major}*

%files -n %{develname}
%defattr(-,root,root)
%{_libdir}/lib*.so
%{_libdir}/*.*a
%{_libdir}/pkgconfig/*.pc
%dir %{_includedir}/xfce4/xfce4-session-4.2
%{_includedir}/xfce4/xfce4-session-4.2/*/*.h
