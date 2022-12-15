%define url_ver %(echo %{version} | cut -d. -f1,2)

%define major 0

%define _disable_rebuild_configure 1

Summary:	Xfce Session Manager
Name:		xfce4-session
Version:	4.18.0
Release:	1
License:	GPLv2+
Group:		Graphical desktop/Xfce
URL:		http://www.xfce.org
Source0:	http://archive.xfce.org/src/xfce/%{name}/%{url_ver}/%{name}-%{version}.tar.bz2
Source2:	xfce4.pam

BuildRequires:	intltool
BuildRequires:	xfce4-dev-tools
BuildRequires:	perl(XML::Parser)
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(ice)
BuildRequires:	pkgconfig(sm)
BuildRequires:	pkgconfig(systemd)
BuildRequires:	iceauth
BuildRequires:	pkgconfig(dbus-glib-1)
BuildRequires:	pkgconfig(gconf-2.0)
BuildRequires:	pkgconfig(libxfce4ui-2)
BuildRequires:	pkgconfig(libxfce4util-1.0)
BuildRequires:  pkgconfig(libxfce4panel-2.0)
BuildRequires:	pkgconfig(libwnck-3.0)
BuildRequires:	pkgconfig(libxfconf-0)
BuildRequires:	pkgconfig(libsystemd)
BuildRequires:	pkgconfig(polkit-gobject-1)
BuildConflicts:	hal-devel
Requires:	usermode-consoleonly
# (tpg) this satisfies xfce tips&tricks
#Suggests:	fortune-mod
#Requires:	polkit-gnome
#Requires:	mate-polkit
Requires:	xfce-polkit
Requires:	xscreensaver
#Requires(pre):	distro-xfce-config-common
#Requires(post):	distro-xfce-config-common
Obsoletes:	xfce-session < 4.5.91
%rename	xfce-utils

%description
The session manager allows the user to save sessions and
restore them after login. It is capable of saving several
different sessions. It comes with three splash screen engines.
And at last it helps you to log out, reboot, and shutdown the system.

%prep
%setup -q
%autopatch -p1

%build
NOCONFIGURE=1

%configure \
	--enable-legacy-sm \
	--enable-systemd \
	--disable-static

%make_build

%install
%make_install

# (tpg) this file is in mandriva-xfce-config package
#rm -rf %{buildroot}%{_sysconfdir}/xdg/autostart/xfce4-tips-autostart.desktop
#rm -rf %{buildroot}%{_sysconfdir}/xdg/xfce4/xfconf/xfce-perchannel-xml/xfce4-session.xml
# xscreensaver.desktop file is not provided by main xscreensaver. So to avaoid files conflicting let's drop it from here and add as dep.
rm -rf %{buildroot}%{_sysconfdir}/xdg/autostart/xscreensaver.desktop

# pam
mkdir -p %{buildroot}%{_sysconfdir}/pam.d
install -m 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/pam.d/xfce4

%find_lang %{name} %{name}.lang

%files -f %{name}.lang
%doc AUTHORS BUGS ChangeLog NEWS README* TODO
%doc doc/FAQ doc/README.Kiosk
%{_sysconfdir}/pam.d/xfce4
%{_sysconfdir}/xdg/xfce4/Xft.xrdb
%{_sysconfdir}/xdg/xfce4/xinitrc
%{_sysconfdir}/xdg/xfce4/xfconf/xfce-perchannel-xml/xfce4-session.xml
%{_bindir}/*
%{_datadir}/polkit-1/actions/org.xfce.session.policy
%{_datadir}/applications/xfce*
%{_iconsdir}/hicolor/*/*/*.{png,svg}
%{_libdir}/xfce4/session/xfsm-shutdown-helper
%{_datadir}/xsessions/xfce.desktop
%{_mandir}/man1/*
