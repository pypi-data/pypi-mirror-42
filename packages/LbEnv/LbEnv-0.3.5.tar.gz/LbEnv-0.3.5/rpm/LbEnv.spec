%define prefix /opt/LHCbSoft

%global __os_install_post /usr/lib/rpm/check-buildroot

Name: LbEnv
# version and release values are filled by the gitlab-ci job
Version: 0
Release: 0
Vendor: LHCb
Summary: Entry scripts for LHCb login environment
License: GPLv3
URL:     https://gitlab.cern.ch/lhcb-core/%{name}
Source0: https://gitlab.cern.ch/lhcb-core/%{name}/-/archive/%{version}/%{name}-%{version}.tar.gz

Group: LHCb

BuildArch: noarch
AutoReqProv: no
Prefix: %{prefix}
Provides: /bin/sh
Provides: /bin/bash

%description
Entry scripts for LHCb login environment

%prep
%setup -q

%build

%install
mkdir -p ${RPM_BUILD_ROOT}%{prefix}/bin
install -m 0755 'rpm/data/bin/host_os' ${RPM_BUILD_ROOT}/%{prefix}/bin

for flavour in prod pre-prod dev ; do
  for suff in '' .sh .csh ; do
    tgt=${RPM_BUILD_ROOT}/%{prefix}/LbEnv-${flavour}${suff}
    install -m 0644 "rpm/data/LbEnv-flavour${suff}" "${tgt}"
    sed -i "s/%flavour%/${flavour}/g" "${tgt}"
  done
done
for suff in '' .sh .csh ; do
  ln -s LbEnv-prod${suff} ${RPM_BUILD_ROOT}/%{prefix}/LbEnv${suff}
done

%clean

%post -p /bin/bash
for flavour in prod pre-prod dev ; do
  for suff in '' .sh .csh ; do
    tgt=${RPM_INSTALL_PREFIX}/LbEnv-${flavour}${suff}
    sed -i "s#%\(target_dir\|siteroot\)%#${RPM_INSTALL_PREFIX}#g;s#%lbenv_root%#${RPM_INSTALL_PREFIX}/var/lib/LbEnv/${flavour}#g" "${tgt}"
  done
done

%postun -p /bin/bash

%files
%defattr(-,root,root)
%{prefix}/bin/host_os
%{prefix}/LbEnv
%{prefix}/LbEnv.sh
%{prefix}/LbEnv.csh
%{prefix}/LbEnv-prod
%{prefix}/LbEnv-prod.sh
%{prefix}/LbEnv-prod.csh
%{prefix}/LbEnv-pre-prod
%{prefix}/LbEnv-pre-prod.sh
%{prefix}/LbEnv-pre-prod.csh
%{prefix}/LbEnv-dev
%{prefix}/LbEnv-dev.sh
%{prefix}/LbEnv-dev.csh


%changelog
* Mon Oct 22 2018 Marco Clemencic <marco.clemencic@cern.ch>
- first rpm package
