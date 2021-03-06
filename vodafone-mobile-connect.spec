%define realname vodafone-mobile-connect-card-driver-for-linux
%define version 2.0
%define pre beta3
%define rel 6

Summary: 	Vodafone Mobile Connect Card Driver (GUI) for Linux
Name: 		vodafone-mobile-connect
Version: 	%{version}
Release:	%mkrel %{expand:%{?pre:0.%pre.}}%rel
Source0: 	https://forge.vodafonebetavine.net/frs/download.php/57/%{realname}-%{version}%{?pre:.%pre}.tar.gz
Source1:	vmc-mandriva-plugin.py
#Patch:		
License:	GPLv2+
Group: 		System/Configuration/Networking
BuildArch:	noarch
BuildRoot: 	%{_tmppath}/%{name}-buildroot
URL:		https://forge.betavine.net/projects/vodafonemobilec/
Provides:	%{realname} = %{version}-%{release} vmc
Obsoletes:	%{realname} < %{version} vmc
# < %{version}-{release}
BuildRequires:	python-devel python-setuptools >= 0.6c5
Requires:	python-twisted python-serial pygtk2.0-libglade 
Requires:	python-twisted-conch >= 0.8.0
Requires:	python-matplotlib python-dbus gksu wvdial
Requires:	gnome-python gnome-python-extras
Requires:	lsb-release
%if %mdkversion <= 200900
# With 2.6.26 and later, this is not required, but on 2.6.24 (2008.1) it still is:
Suggests:	huaweiaktbbo
%endif
# TODO
# contrib/ovation
# contrib/option_icon

%description
Vodafone Mobile Connect Card driver for Linux is a GPRS/UMTS/HSDPA device
manager written in Python, licensed under the GPL. Features: Data call handling
Send/Receive SMS SIM phone book management Graphical user interface using GTK

%prep
%setup -q -n %{realname}-%{version}%{?pre:.%pre}
install -m644 %{SOURCE1} plugins/mandriva.py
find . -name '*~' -o -name '*.bak' -exec rm -f {} \;
rm -f plugins/suse.py~

%build
env CFLAGS="$RPM_OPT_FLAGS" python setup.py build

%install
rm -Rf %{buildroot}
#rm -f INSTALLED_FILES
python setup.py install --root=$RPM_BUILD_ROOT --record=INSTALLED_FILES

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc README
%py_puresitedir/*
%_bindir/*
%_datadir/applications/*.desktop
%_datadir/pixmaps/*.png
%_datadir/vodafone-mobile-connect-card-driver-for-linux


%changelog
* Mon Nov 08 2010 Funda Wang <fwang@mandriva.org> 2.0-0.beta3.6mdv2011.0
+ Revision: 595036
- rebuild for py 2.7

  + Michael Scherer <misc@mandriva.org>
    - rebuild for python 2.7

* Sun Sep 20 2009 Thierry Vignaud <tv@mandriva.org> 2.0-0.beta3.4mdv2010.0
+ Revision: 445701
- rebuild

* Sat Sep 20 2008 Buchan Milne <bgmilne@mandriva.org> 2.0-0.beta3.3mdv2009.1
+ Revision: 286075
- Rename vmc to vodafone-mobile-connect

* Fri Aug 01 2008 Buchan Milne <bgmilne@mandriva.org> 2.0-0.beta3.3mdv2009.0
+ Revision: 259491
- Require python-twisted-conch >= 0.8.0
- Require gnome-python-extras

* Fri Aug 01 2008 Buchan Milne <bgmilne@mandriva.org> 2.0-0.beta3.2mdv2009.0
+ Revision: 259445
- Require gnome-python

* Fri Aug 01 2008 Buchan Milne <bgmilne@mandriva.org> 2.0-0.beta3.1mdv2009.0
+ Revision: 259407
- import vmc

