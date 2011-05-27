%define		_class		XML
%define		_subclass	image2svg
%define		upstream_name	%{_class}_%{_subclass}

%define		_requires_exceptions pear(XML_image2svg/image2svg.php)

Name:		php-pear-%{upstream_name}
Version:	0.1
Release:	%mkrel 13
Summary:	Image to SVG conversion
License:	PHP License
Group:		Development/PHP
URL:		http://pear.php.net/package/XML_image2svg/
Source0:	http://download.pear.php.net/package/%{upstream_name}-%{version}.tar.bz2
Patch0:		%{name}-fix-path.patch
Requires(post): php-pear
Requires(preun): php-pear
Requires:	php-pear
BuildArch:	noarch
BuildRequires:	php-pear
BuildRoot:	%{_tmppath}/%{name}-%{version}

%description
The class converts images, such as of the format JPEG, PNG and GIF to
a standalone SVG representation. The image is being encoded by the PHP
native encode_base64() function. You can use it to get back a complete
SVG file, which is based on a predefinded, easy adaptable template
file, or you can take the encoded file as a return value, using the
get() method. Due to the encoding by base64, the SVG files will
increase approx. 30% in size compared to the conventional image.


%prep
%setup -q -c
%patch0 -p1
mv package.xml %{upstream_name}-%{version}/%{upstream_name}.xml

%install
rm -rf %{buildroot}

cd %{upstream_name}-%{version}
pear install --nodeps --packagingroot %{buildroot} %{upstream_name}.xml
rm -rf %{buildroot}%{_datadir}/pear/.??*

rm -rf %{buildroot}%{_datadir}/pear/docs
rm -rf %{buildroot}%{_datadir}/pear/tests

install -d %{buildroot}%{_datadir}/pear/packages
install -m 644 %{upstream_name}.xml %{buildroot}%{_datadir}/pear/packages

%clean
rm -rf %{buildroot}

%post
%if %mdkversion < 201000
pear install --nodeps --soft --force --register-only \
    %{_datadir}/pear/packages/%{upstream_name}.xml >/dev/null || :
%endif

%preun
%if %mdkversion < 201000
if [ "$1" -eq "0" ]; then
    pear uninstall --nodeps --ignore-errors --register-only \
        %{pear_name} >/dev/null || :
fi
%endif

%files
%defattr(-,root,root)
%{_datadir}/pear/%{_class}
%{_datadir}/pear/packages/%{upstream_name}.xml


