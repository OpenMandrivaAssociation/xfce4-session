%define url_ver %(echo %{version} | cut -d. -f1,2)

%define major 0
%define apiver 4.6
%define libname %mklibname xfsm-%{apiver}_%{major}
%define develname %mklibname xfsm -d

Summary:	Xfce Session Manager
Name:		xfce4-session
Version:	4.10.0
Release:	5
License:	GPLv2+
Group:		Graphical desktop/Xfce
URL:		http://www.xfce.org
Source0:	http://archive.xfce.org/src/xfce/%{name}/%{url_ver}/%{name}-%{version}.tar.bz2
Source1:	06Xfce
Source2:	xfce4.pam
Patch0:		xfce4-session-4.9.0-xinitrc.patch
Patch1:		xfce4-session-4.10.0-remove-gnome-keyring-remains.patch
# (tpg) https://bugzilla.xfce.org/show_bug.cgi?id=8729
# below is a rediffed patch
Patch2:		xfce4-session-4.10.0-add-systemd-support.patch
Patch3:		xfce4-session-4.10.0-fix--fast-action.patch
Patch4:		xfce4-session-4.10.0-handle-multiple-interactive-session-save.patch
Patch5:		xfce4-session-4.10.0-fix-duplicated-accelerators.patch
BuildRequires:	perl(XML::Parser)
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(ice)
BuildRequires:	pkgconfig(sm)
BuildRequires:	iceauth
BuildRequires:	dbus-glib-devel
BuildRequires:	pkgconfig(gconf-2.0)
# (tpg) for patch 6
BuildRequires:	intltool
BuildRequires:	libxfce4ui-devel >= 4.10.0
BuildRequires:	libxfce4util-devel >= 4.10.0
BuildRequires:	libwnck-devel
BuildRequires:	xfconf-devel >= 4.10.0
BuildRequires:	pkgconfig(libsystemd-login)
BuildRequires:	pkgconfig(polkit-gobject-1)
BuildRequires:	xfce4-panel-devel >= 4.10.0
BuildConflicts:	hal-devel
Requires:	usermode-consoleonly
# (tpg) this satisfies xfce tips&tricks
#Suggests:	fortune-mod
Requires:	polkit-gnome
Requires(pre):	mandriva-xfce-config
Requires(post):	mandriva-xfce-config
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
# (tpg) for new automake
sed -i -e 's,AM_CONFIG_HEADER,AC_CONFIG_HEADERS,g' configure.*

#(tpg) this is needed for patch 1 which enables systemd support
NOCONFIGURE=yes xdt-autogen

%configure2_5x \
	--enable-legacy-sm \
	--enable-systemd \
	--disable-static

%make

%install
%makeinstall_std

# (tpg) this file is in mandriva-xfce-config package
rm -rf %{buildroot}%{_sysconfdir}/xdg/autostart/xfce4-tips-autostart.desktop
rm -rf %{buildroot}%{_sysconfdir}/xdg/xfce4/xfconf/xfce-perchannel-xml/xfce4-session.xml

# session
mkdir -p %{buildroot}%{_sysconfdir}/X11/wmsession.d
install -m 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/X11/wmsession.d

# pam
mkdir -p %{buildroot}%{_sysconfdir}/pam.d
install -m 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/pam.d/xfce4


%find_lang %{name} %{name}.lang

%files -f %{name}.lang
%doc AUTHORS BUGS ChangeLog NEWS README TODO
%doc doc/FAQ doc/README.Kiosk
%dir %{_datadir}/themes
%dir %{_datadir}/themes/Default

%{_sysconfdir}/X11/wmsession.d/06Xfce
%{_sysconfdir}/pam.d/xfce4
%{_sysconfdir}/xdg/autostart/*.desktop
%{_sysconfdir}/xdg/xfce4/Xft.xrdb
%{_sysconfdir}/xdg/xfce4/xinitrc
%{_bindir}/*
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


%changelog
* Thu Aug 02 2012 Tomasz Pawel Gajc <tpg@mandriva.org> 4.10.0-2
+ Revision: 811558
- add support for systemd for mdv 2012

* Sat May 05 2012 Tomasz Pawel Gajc <tpg@mandriva.org> 4.10.0-1
+ Revision: 796479
- adjust buildrequires version
- update to new version 4.10.0

* Sat Apr 21 2012 Tomasz Pawel Gajc <tpg@mandriva.org> 4.9.2-1
+ Revision: 792606
- update to new version 4.9.2

* Sun Apr 15 2012 Tomasz Pawel Gajc <tpg@mandriva.org> 4.9.1-1
+ Revision: 791062
- update to new version 4.9.1

* Sun Apr 08 2012 Tomasz Pawel Gajc <tpg@mandriva.org> 4.9.0-3
+ Revision: 789813
- Patch0: backport patch from xfce-utils
- add pam configs and wmsession from xfce-utils

* Sat Apr 07 2012 Tomasz Pawel Gajc <tpg@mandriva.org> 4.9.0-2
+ Revision: 789751
- properrly obsolete and provide xfce-utils

* Wed Apr 04 2012 Tomasz Pawel Gajc <tpg@mandriva.org> 4.9.0-1
+ Revision: 789251
- drop old patches
- do not suggest fortune-mod
- update to new version 4.9.0
- update buildrequires
- remove obsolete configure options
- drop ols stuff from spec file
- fix file list

* Sat Feb 18 2012 Tomasz Pawel Gajc <tpg@mandriva.org> 4.8.3-1
+ Revision: 776850
- patch 4 has been applied by upstream
- update to new version 4.8.3

* Fri Jan 06 2012 Tomasz Pawel Gajc <tpg@mandriva.org> 4.8.2-3
+ Revision: 758003
- add missing libs while linking into patch 4
- add buildconflicts on hal-devel
- Patch3: respect SaveOnExit option
- Patch4: fix linking
- Patch2: force start xfsettingsd
- drop la files

* Thu Sep 22 2011 Tomasz Pawel Gajc <tpg@mandriva.org> 4.8.2-1
+ Revision: 700942
- update to new version 4.8.2

* Fri Apr 15 2011 Tomasz Pawel Gajc <tpg@mandriva.org> 4.8.1-3
+ Revision: 653077
- requires polkit-gnome

* Mon Feb 28 2011 Funda Wang <fwang@mandriva.org> 4.8.1-2
+ Revision: 640877
- rebuild

* Tue Feb 15 2011 Tomasz Pawel Gajc <tpg@mandriva.org> 4.8.1-1
+ Revision: 637859
- update to new version 4.8.1

* Thu Feb 03 2011 Funda Wang <fwang@mandriva.org> 4.8.0-2
+ Revision: 635654
- tighten BR

* Wed Jan 26 2011 Tomasz Pawel Gajc <tpg@mandriva.org> 4.8.0-1
+ Revision: 633041
- update to new version 4.8.0
- fix file list

* Thu Jan 06 2011 Tomasz Pawel Gajc <tpg@mandriva.org> 4.7.3-1mdv2011.0
+ Revision: 629115
- update to new version 4.7.3

* Sat Dec 04 2010 Tomasz Pawel Gajc <tpg@mandriva.org> 4.7.2-1mdv2011.0
+ Revision: 609366
- update to new version 4.7.2

* Sat Nov 06 2010 Tomasz Pawel Gajc <tpg@mandriva.org> 4.7.1-1mdv2011.0
+ Revision: 593835
- update to new version 4.7.1
- disable patch 1
- drop some conditions in spec file for mdv older than 20090

* Sun Sep 19 2010 Tomasz Pawel Gajc <tpg@mandriva.org> 4.7.0-2mdv2011.0
+ Revision: 579846
- Patch1: reuse existing ConsoleKit sessions

* Sat Sep 18 2010 Tomasz Pawel Gajc <tpg@mandriva.org> 4.7.0-1mdv2011.0
+ Revision: 579372
- update to new version 4.7.0
- fix file list
- adjust buildrequires
- disable patch 0

* Fri Jul 16 2010 Tomasz Pawel Gajc <tpg@mandriva.org> 4.6.2-1mdv2011.0
+ Revision: 553890
- update to new version 4.6.2

* Thu Jun 03 2010 Tomasz Pawel Gajc <tpg@mandriva.org> 4.6.1-3mdv2010.1
+ Revision: 547055
- Patch0: fix gnome-keyring support (upstream xfce bug #5912)

* Fri May 07 2010 Tomasz Pawel Gajc <tpg@mandriva.org> 4.6.1-2mdv2010.1
+ Revision: 543220
- rebuild for mdv 2010.1

* Tue Apr 21 2009 Tomasz Pawel Gajc <tpg@mandriva.org> 4.6.1-1mdv2010.0
+ Revision: 368577
- update to new version 4.6.1

* Sun Apr 05 2009 Tomasz Pawel Gajc <tpg@mandriva.org> 4.6.0-3mdv2009.1
+ Revision: 364198
- Patch0: don't crash when NULL pointer is passed
- Patch1: fix default value for EnableTcp
- drop useless stuff

* Thu Mar 05 2009 Tomasz Pawel Gajc <tpg@mandriva.org> 4.6.0-2mdv2009.1
+ Revision: 349228
- rebuild whole xfce

* Sat Feb 28 2009 Tomasz Pawel Gajc <tpg@mandriva.org> 4.6.0-1mdv2009.1
+ Revision: 346150
- update to new version 4.6.0

* Mon Jan 26 2009 Tomasz Pawel Gajc <tpg@mandriva.org> 4.5.99.1-1mdv2009.1
+ Revision: 333929
- update to new version 4.5.99.1

* Wed Jan 14 2009 Tomasz Pawel Gajc <tpg@mandriva.org> 4.5.93-1mdv2009.1
+ Revision: 329517
- update to new version 4.5.93

* Mon Nov 24 2008 Tomasz Pawel Gajc <tpg@mandriva.org> 4.5.92-3mdv2009.1
+ Revision: 306422
- pre requires on mandriva-xfce-config

* Mon Nov 24 2008 Tomasz Pawel Gajc <tpg@mandriva.org> 4.5.92-2mdv2009.1
+ Revision: 306419
- xfce4-session.xml file is in mandriva-xfce-config package
- post requires on mandriva-xfce-config
- drop Source1 and patches 4 and 7 as they are not needed at all
- add full path for the Source0

* Sat Nov 15 2008 Tomasz Pawel Gajc <tpg@mandriva.org> 4.5.92-1mdv2009.1
+ Revision: 303498
- update to new version 4.5.92 (Xfce 4.6 Beta 2 Hopper)
- remove buildrequires on libgdk_pixbuf2.0-devel
- pm-utils are required by xfce4-power-manager
- do not suggests sudo anymore
- require usermode-consoleonly
- do not build static libraries

* Thu Oct 16 2008 Tomasz Pawel Gajc <tpg@mandriva.org> 4.5.91-1mdv2009.1
+ Revision: 294512
- Xfce4.6 beta1 is landing on cooker
- disable all patches, probably some of them are still useful, will investigate later
- fix file list
- bump apiver
- tune up buildrequires
- obsolete old library
- requires policykit-gnome
- Patch10: new version

* Fri Sep 05 2008 Tomasz Pawel Gajc <tpg@mandriva.org> 4.4.2-12mdv2009.0
+ Revision: 281321
- Patch11: use dbus-glib for configure script
- Patch12: update translation for logoff dialog box
- suggests sudo

* Thu Aug 21 2008 Tomasz Pawel Gajc <tpg@mandriva.org> 4.4.2-11mdv2009.0
+ Revision: 274449
- Patch10: speed up xfce startup, gain in speed is about 1 sec. (patch taken from xfce mailing list)

* Tue Aug 19 2008 Tomasz Pawel Gajc <tpg@mandriva.org> 4.4.2-10mdv2009.0
+ Revision: 274072
- Patch9: do not spawn another gnome-keyring-daemon, if one is already running (upstream bug #3007)

* Sat Jun 28 2008 Tomasz Pawel Gajc <tpg@mandriva.org> 4.4.2-9mdv2009.0
+ Revision: 229843
- enable patch 6, fixes underlinking problems
- suggest fortune-mod

  + Anssi Hannula <anssi@mandriva.org>
    - fix icons.patch to make xdt-autogen succeed (lines wrongly ending in
      backslash)

  + Pixel <pixel@mandriva.com>
    - rpm filetriggers deprecates update_menus/update_scrollkeeper/update_mime_database/update_icon_cache/update_desktop_database/post_install_gconf_schemas
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers

* Mon May 12 2008 Tomasz Pawel Gajc <tpg@mandriva.org> 4.4.2-8mdv2009.0
+ Revision: 206275
- change sysconfdir from /etc/X11/xdg to /etc/xdg only for Mandriva releases newer than 2008.1

* Wed Mar 19 2008 Tomasz Pawel Gajc <tpg@mandriva.org> 4.4.2-7mdv2008.1
+ Revision: 188938
- fix libification introduced in last commit

* Wed Mar 19 2008 Tomasz Pawel Gajc <tpg@mandriva.org> 4.4.2-6mdv2008.1
+ Revision: 188854
- Patch7: add missing icon xfce4-autostart-editor.png
- spec file clean

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

* Wed Dec 19 2007 Tomasz Pawel Gajc <tpg@mandriva.org> 4.4.2-5mdv2008.1
+ Revision: 133073
- rediff patch 7,  remove xfsm-shutdown.svg icon
- enable legacy session management, fixes mdv bug #29853

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Fri Nov 30 2007 Jérôme Soyer <saispo@mandriva.org> 4.4.2-4mdv2008.1
+ Revision: 114057
- Add configure option

* Sun Nov 25 2007 Jérôme Soyer <saispo@mandriva.org> 4.4.2-3mdv2008.1
+ Revision: 111974
- Add more beautiful icons on quit dialogbox
- Add more beautiful icons on quit dialogbox

* Tue Nov 20 2007 Tomasz Pawel Gajc <tpg@mandriva.org> 4.4.2-2mdv2008.1
+ Revision: 110667
- do not package COPYING and INSTALL files
- add missing buildrequires on libGConf2-devel

* Sun Nov 18 2007 Jérôme Soyer <saispo@mandriva.org> 4.4.2-1mdv2008.1
+ Revision: 109978
- New release 4.4.2

  + Tomasz Pawel Gajc <tpg@mandriva.org>
    - use upstream tarball name as a real name
    - use upstream name

* Sun Sep 23 2007 Tomasz Pawel Gajc <tpg@mandriva.org> 4.4.1-11mdv2008.0
+ Revision: 92364
- update patch 5 (logout dialog)

* Fri Sep 21 2007 Tomasz Pawel Gajc <tpg@mandriva.org> 4.4.1-10mdv2008.0
+ Revision: 91881
- exclude config files, which are now in mandriva-xfce-config package

* Tue Sep 11 2007 Tomasz Pawel Gajc <tpg@mandriva.org> 4.4.1-9mdv2008.0
+ Revision: 84450
- since there is suspend/hibernate option in logout menu, then pm-utils should be required

* Fri Sep 07 2007 Tomasz Pawel Gajc <tpg@mandriva.org> 4.4.1-8mdv2008.0
+ Revision: 81907
- remove old patch 4, replace it with new one since all conf files are handle by mandriva-xfce-config package
- provide patch8, which make use of GtkFileChooser

* Tue Jun 26 2007 Tomasz Pawel Gajc <tpg@mandriva.org> 4.4.1-7mdv2008.0
+ Revision: 44263
- fix file list
- new devel library policy
- disable legacy X11R5 session management
- move Source 1 and 2 to the xfce-config package
- adjust provides/obsoletes

* Thu Jun 07 2007 Anssi Hannula <anssi@mandriva.org> 4.4.1-6mdv2008.0
+ Revision: 36215
- rebuild with correct optflags

  + Tomasz Pawel Gajc <tpg@mandriva.org>
    - move balou splash engine to separate package (i hope someone will make a mandriva theme :)
    - rediff P4 (splash should be disabled now)

* Mon Jun 04 2007 Tomasz Pawel Gajc <tpg@mandriva.org> 4.4.1-4mdv2008.0
+ Revision: 35071
- provide patch 5
  o add suspend and hibernate options to the session dialog
  o shutdown without a password
- provide patch 6 and 7
- provide Source 3 (icons for suspend/hibernate stolen from gnome-power-manager :)
- add requires on fortune-mod (tips&tricks works now)
- add buildrequires on dbus-glib-devel
- disable splash
- update description
- use macros in %%post and %%postun
- adjust configure options
- spec file clean

* Thu May 31 2007 Jérôme Soyer <saispo@mandriva.org> 4.4.1-3mdv2008.0
+ Revision: 33091
- Add autostart

* Fri May 25 2007 Jérôme Soyer <saispo@mandriva.org> 4.4.1-2mdv2008.0
+ Revision: 31093
- Add mandriva default theme

* Thu Apr 19 2007 Jérôme Soyer <saispo@mandriva.org> 4.4.1-1mdv2008.0
+ Revision: 14934
- New release 4.4.1

