%define realname vodafone-mobile-connect-card-driver-for-linux
%define version 2.0
%define pre beta3
%define rel 4

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

%files -f INSTALLED_FILES
%defattr(-,root,root)
%doc README

