%define __os_install_post %{nil}
%define uek %( uname -r | egrep -i uek | wc -l | awk '{print $1}' )
%define rpm_arch %( uname -p )
%define rpm_author Jason W. Plummer
%define rpm_author_email jason.plummer@ingramcontent.com
%define distro_id %( lsb_release -is )
%define distro_ver %( lsb_release -rs )
%define distro_major_ver %( echo "%{distro_ver}" | awk -F'.' '{print $1}' )
%define source_url http://repo1.maven.org/maven2/org/codehaus/sonar/runner/sonar-runner-dist

Summary: The SonarQube platform is an open source quality management platform
Name: icg-sonar-runner
Release: 1.EL%{distro_major_ver}
License: GNU
Group: Development/Compiler
BuildRoot: %{_tmppath}/%{name}-root

# This does a scrape of the %{source_url} looking for the version specified
%define sonar_runner_archive_name sonar-runner
%define sonar_runner_version 2.4
%define sonar_runner_version_url %( elinks -dump %{source_url}/%{sonar_runner_version}/ | egrep "%{source_url}.*%{sonar_runner_archive_name}\-dist\-%{sonar_runner_version}.zip$" | sort | tail -1 | awk '{print $NF}' )

Version: %{sonar_runner_version}
URL: %{sonar_runner_version_url}

# This block handles Oracle Linux UEK .vs. EL BuildRequires
#%if %{uek}
#BuildRequires: kernel-uek-devel, kernel-uek-headers
#%else
#BuildRequires: kernel-devel, kernel-headers
#%endif
# These BuildRequires can be found in EPEL

# These Requires can be found in Base
Requires: curl  >= 0
Requires: unzip >= 0

%define install_dir /usr/local

# Define our variables here
Source0: %{url}

%description
The SonarQube® platform is an open source quality management platform, 
dedicated to continuously analyzing and measuring the technical quality 
of source code, from project portfolio down to the method level, and 
tracking the introduction of new Bugs, Vulnerabilities, and Code Smells 
in the Leak Period

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{install_dir}
# Populate %{buildroot}
cd %{buildroot}%{install_dir} && curl -O %{url}
if [ -e "%{sonar_runner_archive_name}-dist-%{sonar_runner_version}.zip" ]; then
    unzip "%{sonar_runner_archive_name}-dist-%{sonar_runner_version}.zip"
fi
if [ -d "%{sonar_runner_archive_name}-%{sonar_runner_version}" ]; then
    rm -f "%{sonar_runner_archive_name}-dist-%{sonar_runner_version}.zip"
fi
# Build packaging manifest
rm -rf /tmp/MANIFEST.%{name}* > /dev/null 2>&1
echo '%defattr(-,root,root)' > /tmp/MANIFEST.%{name}
chown -R root:root %{buildroot} > /dev/null 2>&1
cd %{buildroot}
find . -depth -type d -exec chmod 755 {} \;
find . -depth -type f -exec chmod 644 {} \;
for i in `find . -depth -type f | sed -e 's/\ /zzqc/g'` ; do
    filename=`echo "${i}" | sed -e 's/zzqc/\ /g'`
    eval is_exe=`file "${filename}" | egrep -i "executable" | wc -l | awk '{print $1}'`
    if [ "${is_exe}" -gt 0 ]; then
        chmod 555 "${filename}"
    fi
done
find . -type f -or -type l | sed -e 's/\ /zzqc/' -e 's/^.//' -e '/^$/d' > /tmp/MANIFEST.%{name}.tmp
for i in `awk '{print $0}' /tmp/MANIFEST.%{name}.tmp` ; do
    filename=`echo "${i}" | sed -e 's/zzqc/\ /g'`
    dir=`dirname "${filename}"`
    echo "${dir}/*"
done | sort -u >> /tmp/MANIFEST.%{name}
# Clean up what we can now and allow overwrite later
rm -f /tmp/MANIFEST.%{name}.tmp
chmod 666 /tmp/MANIFEST.%{name}

%files -f /tmp/MANIFEST.%{name}

%changelog
%define today %( date +%a" "%b" "%d" "%Y )
* %{today} %{rpm_author} <%{rpm_author_email}>
- built version %{version} for %{distro_id} %{distro_ver}

