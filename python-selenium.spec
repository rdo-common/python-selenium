%if 0%{?fedora}
%global with_python3 1
%endif

%global upstream_name selenium
%global upstream_version 2.41.0

Name:          python-%{upstream_name}
Version:       %{upstream_version}
Release:       1%{?dist}
Summary:       Python bindings for Selenium
License:       ASL 2.0
URL:           http://docs.seleniumhq.org/
Source0:       http://pypi.python.org/packages/source/s/%{upstream_name}/%{upstream_name}-%{upstream_version}.tar.gz

BuildRequires: python2-devel
BuildRequires: python-setuptools
Requires:      python-rdflib
BuildArch:     noarch

Patch1:        selenium-use-without-bundled-libs.patch

%if 0%{?with_python3}
%package -n python3-%{upstream_name}
Summary:       Python bindings for Selenium

BuildRequires: python3-devel
BuildRequires: python3-setuptools
Requires:      python-rdflib
BuildArch:     noarch

%description -n python3-%{upstream_name}
The selenium package is used automate web browser interaction from Python.

Several browsers/drivers are supported (Firefox, Chrome, Internet Explorer,
PhantomJS), as well as the Remote protocol.

%endif # if with_python3

%description
The selenium package is used automate web browser interaction from Python.

Several browsers/drivers are supported (Firefox, Chrome, Internet Explorer,
PhantomJS), as well as the Remote protocol.

%prep
%setup -qn %{upstream_name}-%{upstream_version}
rm -r %{upstream_name}.egg-info

find %{_builddir}/%{upstream_name}-%{upstream_version} -type f -name "*.py" -exec sed -i '1{/^#!/d;}' {} \;

%patch1 -p1

%if %{with python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
%endif

%build
%{__python2} setup.py build

%if %{with python3}
pushd %{py3dir}
%{__python3} setup.py build
popd
%endif

%install
%{__python2} setup.py install --skip-build --root %{buildroot}

rm -f %{buildroot}%{python2_sitelib}/selenium/webdriver/firefox/amd64/x_ignore_nofocus.so
rm -f %{buildroot}%{python2_sitelib}/selenium/webdriver/firefox/x86/x_ignore_nofocus.so

%if %{with python3}
pushd %{py3dir}
%{__python3} setup.py install --skip-build --root %{buildroot}
popd
rm -f %{buildroot}%{python3_sitelib}/selenium/webdriver/firefox/amd64/x_ignore_nofocus.so
rm -f %{buildroot}%{python3_sitelib}/selenium/webdriver/firefox/x86/x_ignore_nofocus.so
%endif

%files
%{python2_sitelib}/*
%doc py/README

%if %{with python3}
%files -n python3-%{upstream_name}
%{python3_sitelib}/*
%doc py/README
%endif

%changelog
* Fri Apr 04 2014 Dhiru Kholia <dhiru@openwall.com> - 2.41.0-1
- update to new upstream version

* Thu Feb 27 2014 Dhiru Kholia <dhiru@openwall.com> - 2.40.0-2
- fixed shebangs (BZ #1070125)

* Wed Feb 26 2014 Dhiru Kholia <dhiru@openwall.com> - 2.40.0-1
- initial version
