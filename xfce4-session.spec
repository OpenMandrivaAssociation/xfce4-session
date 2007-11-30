%define major 0
%define apiversion 4.2
%define libname %mklibname xfsm-%{apiversion}_%{major}
%define develname %mklibname xfsm -d

Summary:	Xfce Session Manager
Name:		xfce4-session
Version:	4.4.2
Release:	%mkrel 4
License:	GPLv2+
Group:		Graphical desktop/Xfce
URL:		http://www.xfce.org
Source0:	%{name}-%{version}.tar.bz2
Source1:	%{name}-icons.tar.bz2
# (saispo) logout dialogbox patch from Xubuntu
Patch0:         xfce4-session-4.4.1-logout_dialog.patch
# (saispo) default mandriva theme
Patch4:		%{name}-4.4.1-session-options.patch
Patch6:		%{name}-asneeded.patch
Patch7:		%{name}-4.4.1-icons.patch
Patch8:		%{name}-4.4.1-use-GtkFileChooser.patch
BuildRequires:	xfce-mcs-manager-devel >= %{version}
BuildRequires:	libgdk_pixbuf2.0-devel
BuildRequires:	perl(XML::Parser)
BuildRequires:	X11-devel
BuildRequires:	iceauth
BuildRequires:	dbus-glib-devel
BuildRequires:	libGConf2-devel
Requires:	xfce-mcs-manager >= %{version}
#Requires:	usermode-consoleonly
# (tpg) this satisfies xfce tips&tricks
Requires:	fortune-mod
Requires:	pm-utils
Requires:	%{libname} = %{version}-%{release}
Obsoletes:	xfce-session
BuildRoot:	%{_tmppath}/%{name}-%{version}-buildroot

%description
The session manager allows the user to save sessions and
restore them after login. It is capable of saving several
different sessions. It comes with three splash screen engines.
And at last it helps you to log out, reboot, and shutdown the system.

%package -n %{name}-engines
Summary:	Balou splash engine
Group:		Graphical desktop/Xfce
Requires:	%{name} = %{version}-%{release}
Obsoletes:	xfce-session-engines

%description -n %{name}-engines
Balou is an addidional splash engine for the Xfce.

%package -n %{libname}
Summary:	Libraries for the Xfce Session Manager
Group:		Graphical desktop/Xfce

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
%patch7 -p0
%patch8 -p1

%build
%configure2_5x \
	--sysconfdir=%{_sysconfdir}/X11 \
	--with-shutdown-style=hal \
        --enable-final \
	--enable-gnome \
	--enable-dbus \
	--enable-session-screenshots \
	--disable-legacy-sm
%make

%install
rm -rf %{buildroot}
%makeinstall_std

# Copy addons icons for autostart and about
#cp -f %{buildroot}/icons-addons/*/xfce* %{buildroot}/%{_datadir}/icons/*/*/apps/

# Remove devel files from plugins
rm -f %{buildroot}/%{_libdir}/xfce4/splash/engines/*.*a \
	%{buildroot}/%{_libdir}/xfce4/mcs-plugins/*.*a

%find_lang %{name}

%clean
rm -rf %{buildroot}

%post -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig

%post
%{update_menus}
%update_icon_cache hicolor

%postun
%{clean_menus}
%clean_icon_cache hicolor

%files -f %{name}.lang
%defattr(-,root,root)
%doc AUTHORS BUGS ChangeLog ChangeLog.pre-xfce-devel NEWS README TODO
%doc doc/FAQ doc/README.Kiosk doc/C/xfce4*
%doc %dir %{_datadir}/xfce4/doc/*/*.html
%doc %dir %{_datadir}/xfce4/doc/*/images/*
%dir %{_sysconfdir}/X11/xdg/xfce4-session
%dir %{_datadir}/themes
%dir %{_datadir}/themes/Default
%config(noreplace) %{_sysconfdir}/X11/xdg/xfce4-session/xfce4-session.rc
%exclude %{_sysconfdir}/X11/xdg/autostart/xfce4-tips-autostart.desktop
%{_bindir}/*
%{_datadir}/applications/xfce*
%{_datadir}/icons/*/*/apps/xfce*
%{_datadir}/icons/*/*/*/xfsm*
%{_datadir}/xfce4/tips/tips*
%{_libdir}/xfce4/mcs-plugins/*.so
%{_libdir}/xfce4/splash/engines/libmice.so
%{_libdir}/xfce4/splash/engines/libsimple.so
%{_libdir}/xfsm-shutdown-helper
%{_mandir}/man1/*

%files -n %{name}-engines
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
