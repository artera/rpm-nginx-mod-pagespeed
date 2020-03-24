Summary: PageSpeed module for nginx
Name: nginx-mod-pagespeed
Version: 1.13.35.2
Release: 3%{?dist}
Vendor: Artera
URL: https://www.ngxpagespeed.com/

%define _modname            ngx_pagespeed
%define _nginxver           1.16.1
%define _pagespeedver       %{version}-stable
%define _psolver            %{version}
%define nginx_config_dir    %{_sysconfdir}/nginx
%define nginx_build_dir     %{_builddir}/nginx-%{_nginxver}

Source0: https://nginx.org/download/nginx-%{_nginxver}.tar.gz
Source1: https://github.com/pagespeed/ngx_pagespeed/archive/v%{_pagespeedver}/%{_modname}-%{_pagespeedver}.tar.gz
Source2: https://dl.google.com/dl/page-speed/psol/%{_psolver}-x64.tar.gz#/pagespeed-%{_psolver}-x86_64.tar.gz

Requires: nginx = 1:%{_nginxver}
BuildRequires: nginx
BuildRequires: libtool
BuildRequires: autoconf
BuildRequires: automake
BuildRequires: openssl-devel
BuildRequires: pcre-devel
BuildRequires: zlib-devel
BuildRequires: perl-devel
BuildRequires: gd-devel
BuildRequires: GeoIP-devel
BuildRequires: libxslt-devel
BuildRequires: perl-devel
BuildRequires: perl(ExtUtils::Embed)
BuildRequires: gperftools-devel
BuildRequires: libuuid-devel

License: GPL3

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

%description
PageSpeed module for nginx.

%prep
%setup -q -n nginx-%{_nginxver}
%setup -D -b 1 -n incubator-pagespeed-ngx-%{_pagespeedver}
%setup -T -D -a 2 -n incubator-pagespeed-ngx-%{_pagespeedver}

cd %{_builddir}/incubator-pagespeed-ngx-%{_pagespeedver}
sed -r 's@^pagespeed_libs="(\$psol_binary.*)"@pagespeed_libs="\1 -Wl,-z,noexecstack"@' -i config

%build
cd %{_builddir}/nginx-%{_nginxver}
./configure %(nginx -V 2>&1 | grep 'configure arguments' | sed -r 's@^[^:]+: @@') --add-dynamic-module=../incubator-pagespeed-ngx-%{_pagespeedver} || {
    cat %{nginx_build_dir}/objs/autoconf.err
    exit 1
}
make modules

%install
%{__rm} -rf %{buildroot}

%{__install} -Dm755 %{nginx_build_dir}/objs/%{_modname}.so \
    $RPM_BUILD_ROOT%{_libdir}/nginx/modules/%{_modname}.so

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root)
%{_libdir}/nginx/modules/*.so
