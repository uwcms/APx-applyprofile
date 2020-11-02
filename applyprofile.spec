%define name applyprofile

Name:           %{name}
Version:        %{version_rpm_spec_version}
Release:        %{version_rpm_spec_release}%{?dist}
Summary:        A tool for downloading, verifying and excuting manifests with puppet-apply.

License:        Reserved
URL:            https://github.com/uwcms/APx-%{name}
Source0:        %{name}-%{version_rpm_spec_version}.tar.gz

BuildArch:      noarch
BuildRequires:  python3 python-rpm-macros python3-rpm-macros python3-setuptools
Requires:       python3 python3-yaml

%global debug_package %{nil}

%description
A tool for downloading, verifying and excuting manifests with puppet-apply.


%prep
%autosetup -n %{name}-%{version}


%build
export %{version_shellvars}
%py3_build


%install
export %{version_shellvars}
%py3_install
install -D -m 0600 applyprofile-config.yaml %{buildroot}/%{_sysconfdir}/applyprofile-config.yaml
install -D -m 0644 applyprofile.service %{buildroot}/%{_unitdir}/applyprofile.service
install -D -m 0644 applyprofile-onboot.timer %{buildroot}/%{_unitdir}/applyprofile-onboot.timer


%files
%doc README.md
%{python3_sitelib}/*
%{_bindir}/applyprofile
%config(noreplace) %{_sysconfdir}/applyprofile-config.yaml
%{_unitdir}/applyprofile.service
%{_unitdir}/applyprofile-onboot.timer


%post
# This macro will call 'preset' on the provided service.
# applyprofile.service has no 'enable' functionality.
%systemd_post applyprofile-onboot.timer


%preun
# This macro will call 'disable --now' on the provided service.
# applyprofile.service has no 'disable' functionality.
%systemd_preun applyprofile-onboot.timer


%postun
# This macro will call 'try-restart' on the provided service.
# applyprofile.service should not be triggered automatically.
%systemd_postun_with_restart applyprofile-onboot.timer


%changelog
* Tue Oct 27 2020 Jesra Tikalsky <jtikalsky@hep.wisc.edu>
- Initial spec file
