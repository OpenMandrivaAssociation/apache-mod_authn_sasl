#Module-Specific definitions
%define apache_version 2.2.8
%define mod_name mod_authn_sasl
%define mod_conf B38_%{mod_name}.conf
%define mod_so %{mod_name}.so

Summary:	User authentication using Cyrus libsasl2 password verification service
Name:		apache-%{mod_name}
Version:	1.2
Release:	2
Group:		System/Servers
License:	Apache License
URL:		http://sourceforge.net/projects/mod-authn-sasl/
Source0:	http://dfn.dl.sourceforge.net/sourceforge/mod-authn-sasl/%{mod_name}-%{version}.tar.bz2
Source1:	%{mod_conf}
Requires(pre): rpm-helper
Requires(postun): rpm-helper
Requires(pre):  apache-conf >= %{apache_version}
Requires(pre):  apache >= %{apache_version}
Requires:	apache-conf >= %{apache_version}
Requires:	apache >= %{apache_version}
BuildRequires:	apache-mpm-prefork >= %{apache_version}
BuildRequires:	apache-devel >= %{apache_version}
BuildRequires:	dos2unix
BuildRequires:	libsasl-devel

%description
mod_authn_sasl is a SASL authentication backend provider module for the Apache
2.2 webserver. It provides password checking functionality for HTTP Basic
Authentication. Username and password are checked against the SASL password
checking backends.

%prep

%setup -q -n %{mod_name}-%{version}

cp %{SOURCE1} %{mod_conf}

find -type f -exec dos2unix -U {} \;

# fix borked test
perl -pi -e "s|ap_httpd_version=.*|ap_httpd_version=\"2\.2\"|g" configure

# fix docs
rm -rf html_docs; mkdir -p html_docs; cp -rp doc/* html_docs/; find html_docs -name "Makefile*" | xargs rm -f

%build

%configure2_5x --localstatedir=/var/lib \
    --with-apxs=%{_bindir}/apxs
        
%make

%install

install -d %{buildroot}%{_libdir}/apache-extramodules
install -d %{buildroot}%{_sysconfdir}/httpd/modules.d

install -m0755 .libs/%{mod_so} %{buildroot}%{_libdir}/apache-extramodules/
install -m0644 %{mod_conf} %{buildroot}%{_sysconfdir}/httpd/modules.d/%{mod_conf}

%post
if [ -f %{_var}/lock/subsys/httpd ]; then
    %{_initrddir}/httpd restart 1>&2;
fi

%postun
if [ "$1" = "0" ]; then
    if [ -f %{_var}/lock/subsys/httpd ]; then
        %{_initrddir}/httpd restart 1>&2
    fi
fi

%files
%doc AUTHORS LICENSE html_docs/*
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/modules.d/%{mod_conf}
%attr(0755,root,root) %{_libdir}/apache-extramodules/%{mod_so}



%changelog
* Tue May 24 2011 Oden Eriksson <oeriksson@mandriva.com> 1.1-3mdv2011.0
+ Revision: 678278
- mass rebuild

* Sun Oct 24 2010 Oden Eriksson <oeriksson@mandriva.com> 1.1-2mdv2011.0
+ Revision: 587936
- rebuild

* Sun Oct 17 2010 Oden Eriksson <oeriksson@mandriva.com> 1.1-1mdv2011.0
+ Revision: 586377
- 1.1

* Mon Mar 08 2010 Oden Eriksson <oeriksson@mandriva.com> 1.0.2-6mdv2010.1
+ Revision: 516064
- rebuilt for apache-2.2.15

* Sat Aug 01 2009 Oden Eriksson <oeriksson@mandriva.com> 1.0.2-5mdv2010.0
+ Revision: 406538
- rebuild

* Tue Jan 06 2009 Oden Eriksson <oeriksson@mandriva.com> 1.0.2-4mdv2009.1
+ Revision: 325571
- rebuild

* Mon Jul 14 2008 Oden Eriksson <oeriksson@mandriva.com> 1.0.2-3mdv2009.0
+ Revision: 234731
- rebuild

* Thu Jun 05 2008 Oden Eriksson <oeriksson@mandriva.com> 1.0.2-2mdv2009.0
+ Revision: 215544
- fix rebuild
- hard code %%{_localstatedir}/lib to ease backports

* Sun May 18 2008 Oden Eriksson <oeriksson@mandriva.com> 1.0.2-1mdv2009.0
+ Revision: 208658
- fix build (stupid autoconf stuff...)
- import apache-mod_authn_sasl


* Sun May 18 2008 Oden Eriksson <oeriksson@mandriva.com> 1.0.2-1mdv2009.0
- initial Mandriva package
