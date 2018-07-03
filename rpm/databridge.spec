# daemon-reload?
# uninstall not rm bin/* + need to destroy virtualenv?
# /var/log/databridge folder + perm
# general perm + user + group?
# systemd journal same scope for all op? (to be able to log all op?)
# ???
# RM journal from conf !

%define _build_id_links none

%define __spec_prep_post true
%define __spec_prep_pre true
%define __spec_build_post true
%define __spec_build_pre true
%define __spec_install_post true
%define __spec_install_pre true
%define __spec_clean_post true
%define __spec_clean_pre true
%{?systemd_requires}
%define _binary_filedigest_algorithm 1
%define _build_binary_file_digest_algo 1
%define _binary_payload w9.gzdio

%define component databridge
%define user psale
%define source_tar_path ./%{component}.tar.gz
%define source_unit_file ./rpm/%{component}.service
%define source_path_config ./etc/%{component}.yml
%define working_dir /opt/psale/%{component}

Name: %{component}
Version: 0.1
Release: %{release}
Summary: no description given
AutoReqProv: no
BuildRoot: ./

Prefix: /

Group: default
License: Apache License Version 2.0
Vendor: Quintagroup, Ltd.
URL: http://quintagroup.com/
Packager: <info@quintagroup.com>

# BuildRequires: systemd python2-devel automake gcc redhat-rpm-config python2-virtualenv
Requires: systemd python2 python2-virtualenv

%description
no description given

%prep
# noop
rm -rf %{buildroot}
mkdir -p %{buildroot}%{working_dir}/whls/
mkdir -p %{buildroot}/usr/lib/systemd/system/
mkdir -p %{buildroot}/etc/%{component}/
cp %{source_tar_path}  %{buildroot}/%{working_dir}/whls/
cp %{source_unit_file} %{buildroot}/usr/lib/systemd/system/%{component}.service
cp %{source_path_config} %{buildroot}/etc/%{component}/

%build
# noop

%install
# noop

%clean
# noop

%pre
getent group %{user} >/dev/null || groupadd -r %{user}
getent passwd %{user} >/dev/null || useradd -r -g %{user} -s /sbin/nologin %{user}

cd %{working_dir}
virtualenv --clear --always-copy %{working_dir}
tar xvf whls/%{component}.tar.gz -C whls/
rm whls/%{component}.tar.gz
bin/pip install --no-index -f whls whls/*.whl
bin/pip list
exit 0

%post
%systemd_user_post %{component}.service

%preun
%systemd_user_preun %{component}.service

%files
%defattr(-,%{user},%{user},-)
%attr(0755,%{user},%{user}) %{working_dir}
%attr(-,root,root) %{_unitdir}/%{component}.service
%config(noreplace) /etc/%{component}

%changelog
