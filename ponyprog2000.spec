%define name    ponyprog2000
%define version 2.07a
%define release %mkrel 1

Name:           %{name}
Version:        %{version}
Release:        %{release}
Summary:        Serial device programmer
Source0:        http://downloads.sourceforge.net/ponyprog/PonyProg2000-%{version}.tar.gz
# ponyprog 2000 is under GPL according to Author message:
# http://ponyprog1.sourceforge.net/phorum/read.php?f=1&i=4096&t=4096
Source1:        %{name}.png
Patch0:         PonyProg2000-2.07a.patch
License:        GPL
Group:          Development/Other
Url:            http://www.lancos.com/prog.html
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires:  ImageMagick
BuildRequires:  libv-devel
BuildRequires:  X11-devel
ExclusiveArch:  x86_64 %{ix86}
Requires(post,postun): desktop-common-data

%description
PonyProg is a serial device programmer software with a user friendly GUI 
framework available for Windows95, 98, 2000 & NT and Intel Linux. Its purpose 
is reading and writing every serial device. At the moment it supports I�C Bus,
Microwire, SPI eeprom, the Atmel AVR and Microchip PIC micro.

%prep
%setup -q -n PonyProg2000-%{version}
%patch0 -p1

%build
export CFLAGS=$RPM_OPT_FLAGS
export CXXFLAGS=$RPM_OPT_FLAGS

%make

%install
rm -rf $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT%{_bindir}
cp bin/ponyprog2000 $RPM_BUILD_ROOT%{_bindir}

mkdir -p $RPM_BUILD_ROOT%{_iconsdir}
mkdir -p $RPM_BUILD_ROOT%{_miconsdir}
mkdir -p $RPM_BUILD_ROOT%{_liconsdir}

convert -resize 16x16 %SOURCE1 $RPM_BUILD_ROOT%{_miconsdir}/%{name}.png
convert -resize 32x32 %SOURCE1 $RPM_BUILD_ROOT%{_iconsdir}/%{name}.png
convert -resize 48x48 %SOURCE1 $RPM_BUILD_ROOT%{_liconsdir}/%{name}.png

# menu entry
mkdir -p %buildroot/%_menudir
cat > %buildroot/%_menudir/%name << EOF
?package(%name): \
command="%_bindir/%name" \
needs="x11" \
icon="%name.png" \
section="More Applications/Sciences/Robotics" \
title="Ponyprog2000" \
longtitle="Serial device programmer" \
mimetypes="" accept_url="false" \
multiple_files="false" \
xdg="true"
EOF

mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications
cat > $RPM_BUILD_ROOT%{_datadir}/applications/mandriva-%{name}.desktop << EOF
[Desktop Entry]
Name=Ponyprog2000
Comment=Serial device programmer
Exec=%_bindir/%name
Icon=%{name}
Terminal=false
Type=Application
Categories=X-MandrivaLinux-MoreApplications-Sciences-Robotics;Science;Electronics;
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%post
%{update_menus}

%postun
%{clean_menus}

%files
%defattr(-,root,root,755)
%doc README
%{_bindir}/%{name}
%{_miconsdir}/%{name}.png
%{_liconsdir}/%{name}.png
%{_iconsdir}/%{name}.png
%{_menudir}/%{name}
%{_datadir}/applications/*
