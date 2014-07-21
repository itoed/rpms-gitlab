Name:           %{_name}
Version:        %{_version}
Release:        %{_release}
Summary:        GitLab Community Edition
License:        None
BuildArch:      %{_arch}
AutoReqProv:	no
Source0:        gitlab-ce
Source1:        gitlab-shell
Source2:        gitlab-unicorn
Requires:       libicu
Requires:       libxslt
Requires:       ruby > 2
Requires:       redis
Requires:       rsync

%define         homedir /home/git
%define         gitlabdir %{homedir}/gitlab
%define         shelldir %{homedir}/gitlab-shell

%description
GitLab Community Edition (CE) is open source software to collaborate on code. 
Create projects and repositories, manage access and do code reviews. 
GitLab CE is on-premises software that you can install and use on your server(s).

%install
rm -rf %{buildroot}
install -dm 750 %{buildroot}%{homedir}

# Gitlab directory
cp -r %{SOURCE0}/ %{buildroot}%{gitlabdir}
pushd %{buildroot}/%{gitlabdir} >/dev/null
bundle install --deployment --without development test postgres aws
popd >/dev/null

# Gitlab Shell directory
cp -r %{SOURCE1}/ %{buildroot}%{shelldir}

# Gitlab initd script
install -dm 755 %{buildroot}/etc/init.d
cp %{SOURCE2} %{buildroot}/etc/init.d/gitlab
chmod +x %{buildroot}/etc/init.d/gitlab

chmod -R g+r %{buildroot}%{homedir}

%pre
getent group git > /dev/null || groupadd -r git
getent passwd git > /dev/null || \
    useradd -r -g git -s /bin/sh -c "Gitlab" git

%files
%defattr(-,git,git,-)
/home/git
%attr(-,root,root) /etc/init.d/gitlab

%changelog
* Sun Jul 20 2014 Eduardo Ito <ed@fghijk.local> - 7.0.0-1
- Initial release
