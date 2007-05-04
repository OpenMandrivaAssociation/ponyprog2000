%define name    ponyprog2000
%define version 2.06e
%define release %mkrel 5

Name:           %{name}
Version:        %{version}
Release:        %{release}
Summary:        Serial device programmer
Source0:        %{name}-%{version}.tar.bz2
Patch0:		%name-2.06e.patch.bz2
# ponyprog 2000 is under GPL according to Author message:
# http://ponyprog1.sourceforge.net/phorum/read.php?f=1&i=4096&t=4096
Source1:	%{name}.png
License:        GPL
Group:          Development/Other
Url:         	http://sourceforge.net/projects/ponyprog1/
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires:  libv-devel, ImageMagick
BuildRequires:  X11-devel
ExclusiveArch: x86_64 %{ix86}

%description
PonyProg is a serial device programmer software with a user friendly GUI 
framework available for Windows95, 98, 2000 & NT and Intel Linux. Its purpose 
is reading and writing every serial device. At the moment it supports I²C Bus,
Microwire, SPI eeprom, the Atmel AVR and Microchip PIC micro.

%prep
%setup -q -n software
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
