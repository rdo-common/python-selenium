%if 0%{?fedora}
%global with_python3 1
%endif

%global upstream_name selenium

Name:          python-%{upstream_name}
Version:       2.53.2
Release:       1.1%{?dist}
Summary:       Python bindings for Selenium
License:       ASL 2.0
URL:           http://docs.seleniumhq.org/
Source0:       https://pypi.python.org/packages/source/s/%{upstream_name}/%{upstream_name}-%{version}.tar.gz

BuildArch:     noarch

Patch1:        selenium-use-without-bundled-libs.patch

%description
The selenium package is used automate web browser interaction from Python.

Several browsers/drivers are supported (Firefox, Chrome, Internet Explorer,
PhantomJS), as well as the Remote protocol.

%package -n python2-%{upstream_name}
Summary:       Python bindings for Selenium

%{?python_provide:%python_provide python2-%{upstream_name}}
BuildRequires: python2-devel
BuildRequires: python-setuptools
Requires:      python-rdflib

%description -n python2-%{upstream_name}
The selenium package is used automate web browser interaction from Python.

Several browsers/drivers are supported (Firefox, Chrome, Internet Explorer,
PhantomJS), as well as the Remote protocol.


%if 0%{?with_python3}
%package -n python3-%{upstream_name}
Summary:       Python bindings for Selenium
%{?python_provide:%python_provide python3-%{upstream_name}}

BuildRequires: python3-devel
BuildRequires: python3-setuptools
Requires:      python3-rdflib
BuildArch:     noarch

%description -n python3-%{upstream_name}
The selenium package is used automate web browser interaction from Python.

Several browsers/drivers are supported (Firefox, Chrome, Internet Explorer,
PhantomJS), as well as the Remote protocol.

%endif # if with_python3

%prep
%setup -qn %{upstream_name}-%{version}
rm -r %{upstream_name}.egg-info

find . -type f -name "*.py" -exec sed -i '1{/^#!/d;}' {} \;

%patch1 -p1

%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
%endif

%build
%{__python2} setup.py build

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py build
popd
%endif

%install
%{__python2} setup.py install --skip-build --root %{buildroot}

rm -f %{buildroot}%{python2_sitelib}/selenium/webdriver/firefox/amd64/x_ignore_nofocus.so
rm -f %{buildroot}%{python2_sitelib}/selenium/webdriver/firefox/x86/x_ignore_nofocus.so

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install --skip-build --root %{buildroot}
popd
rm -f %{buildroot}%{python3_sitelib}/selenium/webdriver/firefox/amd64/x_ignore_nofocus.so
rm -f %{buildroot}%{python3_sitelib}/selenium/webdriver/firefox/x86/x_ignore_nofocus.so
%endif

%files -n python2-%{upstream_name}
%{python2_sitelib}/*
%doc py/README.rst

%if 0%{?with_python3}
%files -n python3-%{upstream_name}
%{python3_sitelib}/*
%doc py/README.rst
%endif

%changelog
* Fri Jun 10 2016 Alan Pevec <apevec AT redhat.com> - 2.53.2-1.1
- fix conditionals for EL7

* Wed May 18 2016 Matthias Runge <mrunge@redhat.com> - 2.53.2-1
- update to 2.53.2

* Fri Feb 12 2016 Matthias Runge <mrunge@redhat.com> - 2.52.0-1
- update to 2.52.0

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.49.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Jan 18 2016 Matthias Runge <mrunge@redhat.com> - 2.49.0-1
- update to 2.49.0 (rhbz#1298407)
- spec cleanup, add py2 subpackage

* Wed Nov 04 2015 Robert Kuska <rkuska@redhat.com> - 2.48.0-2
- Rebuilt for Python3.5 rebuild

* Wed Oct 14 2015 Dhiru Kholia <dhiru@openwall.com> - 2.48.0-1
- update to 2.48.0

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.45.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Mar 02 2015 Matthias Runge <mrunge@redhat.com> - 2.45.0-1
- update to 2.45.0 to fix compat issues with Firefox 36 (rhbz#1196922)

* Mon Feb 23 2015 Matthias Runge <mrunge@redhat.com> - 2.44.0-1
- update to 2.44.0

* Mon Oct 20 2014 Matthias Runge <mrunge@redhat.com> - 2.43.0-1
- update to 2.43.0
- correct deps for py3 version (rhbz#1116470)

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.42.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri May 30 2014 Matthias Runge <mrunge@redhat.com> - 2.42.1-1
- rebuilt for python3.4 feature
- update to 2.42.1
- minor specs cleanup

* Fri Apr 04 2014 Dhiru Kholia <dhiru@openwall.com> - 2.41.0-1
- update to new upstream version

* Thu Feb 27 2014 Dhiru Kholia <dhiru@openwall.com> - 2.40.0-2
- fixed shebangs (BZ #1070125)

* Wed Feb 26 2014 Dhiru Kholia <dhiru@openwall.com> - 2.40.0-1
- initial version
