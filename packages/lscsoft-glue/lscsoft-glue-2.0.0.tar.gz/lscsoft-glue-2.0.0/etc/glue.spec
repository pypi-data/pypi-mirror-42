Name: 		glue
Summary:	The Grid LSC User Environment
Version:    2.0.0	
Release:	1%{?dist}
License:	GPLv2+
Group:		Development/Libraries
Source:		lscsoft-%{name}-%{version}.tar.gz
Url:		http://www.lsc-group.phys.uwm.edu/daswg/projects/glue.html
BuildRoot:	%{_tmppath}/%{name}-%{version}-root
Requires:	python-cjson pyOpenSSL numpy python-six glue-common python >= 2.7

# build requirements
BuildRequires:  gcc
BuildRequires:  python-rpm-macros
BuildRequires:  python2-rpm-macros
BuildRequires:  python3-rpm-macros
BuildRequires:  python-devel
BuildRequires:  python-setuptools
BuildRequires:  python%{python3_version_nodots}-devel
BuildRequires:  python%{python3_version_nodots}-setuptools

# testing requirements
BuildRequires:  make
BuildRequires:  python-matplotlib
BuildRequires:  numpy
BuildRequires:  python-six
BuildRequires:  python2-ligo-segments
BuildRequires:  python%{python3_version_nodots}-numpy
BuildRequires:  python%{python3_version_nodots}-six
BuildRequires:  python%{python3_version_nodots}-ligo-segments

Prefix:         %{_exec_prefix}
%description
Glue (Grid LSC User Environment) is a suite of python modules and programs to
allow users to run LSC codes on the grid.

%package -n python%{python3_version_nodots}-glue
Summary:        The Grid LSC User Environment
Group:          Development/Libraries
Requires:       python%{python3_version_nodots}
Requires:       python%{python3_version_nodots}-numpy
Requires:       python%{python3_version_nodots}-six
Requires:       python%{python3_version_nodots}-glue-common
%{?python_provide:%python_provide python%{python3_version_nodots}-glue}
%description -n python%{python3_version_nodots}-glue
Glue (Grid LSC User Environment) is a suite of python modules and programs to
allow users to run LSC codes on the grid.

%package common
Summary:	The common files needed for all sub-packages
Group: 		Development/Libraries
Requires: 	python numpy python-six
%description common
This is for the files that are common across the glue subpackages, namely
git_version, iterutils and __init__.py

%package -n python%{python3_version_nodots}-glue-common
Summary:        The common files needed for all sub-packages
Group:          Development/Libraries
Requires:       python%{python3_version_nodots}
Requires:       python%{python3_version_nodots}-numpy
Requires:       python%{python3_version_nodots}-six
%description -n python%{python3_version_nodots}-glue-common
This is for the files that are common across the glue subpackages, namely
git_version, iterutils and __init__.py

%prep
%setup -n lscsoft-%{name}-%{version}

%build
%py3_build
%py2_build

%install
%py2_install
%py3_install

%check
PYTHONPATH="${RPM_BUILD_ROOT}%{python2_sitearch}" \
PYTHON=%{__python2} \
PATH=${RPM_BUILD_ROOT}%{_bindir}:${PATH} \
make -C test \
    -o lal_verify \
    -o ligolw_test01 \
    -o test_ligolw_lsctables \
    -o test_ligolw_table \
    -o test_ligolw_utils_segments
PYTHONPATH="${RPM_BUILD_ROOT}%{python3_sitearch}" \
PYTHON=%{__python3} \
make -C test \
    -o iterutils_verify \
    -o lal_verify \
    -o ligolw_test01 \
    -o test_ligolw_lsctables \
    -o test_ligolw_table \
    -o test_ligolw_utils_segments

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%license LICENSE
%{python2_sitearch}/lscsoft_glue-*.egg-info/
%{python2_sitearch}/glue/
%{_bindir}/*
%exclude %{_exec_prefix}/etc/
%exclude %{_exec_prefix}/var/
%exclude %{python2_sitearch}/glue/__init__.py*
%exclude %{python2_sitearch}/glue/iterutils.py*
%exclude %{python2_sitearch}/glue/git_version.py*
#%exclude %{_exec_prefix}/test/verifyutils.py

%files -n python%{python3_version_nodots}-glue
%defattr(-,root,root)
%license LICENSE
%{python3_sitearch}/lscsoft_glue-*.egg-info/
%{python3_sitearch}/glue/
%exclude %{_bindir}/
%exclude %{_exec_prefix}/etc/
%exclude %{_exec_prefix}/var/
%exclude %{python3_sitearch}/glue/__init__.py
%exclude %{python3_sitearch}/glue/__pycache__/__init__.cpython-%{python3_version_nodots}.py?
%exclude %{python3_sitearch}/glue/__pycache__/segments.cpython-%{python3_version_nodots}.py?
%exclude %{python3_sitearch}/glue/iterutils.py
%exclude %{python3_sitearch}/glue/__pycache__/iterutils.cpython-%{python3_version_nodots}.py?
%exclude %{python3_sitearch}/glue/git_version.py
%exclude %{python3_sitearch}/glue/__pycache__/git_version.cpython-%{python3_version_nodots}.py?
#%exclude %{_exec_prefix}/test/verifyutils.py

%files common
%license LICENSE
%{python2_sitearch}/glue/__init__.py
%{python2_sitearch}/glue/__init__.pyc
%{python2_sitearch}/glue/iterutils.pyc
%{python2_sitearch}/glue/iterutils.py
%{python2_sitearch}/glue/git_version.py
%{python2_sitearch}/glue/git_version.pyc

%files -n python%{python3_version_nodots}-glue-common
%license LICENSE
%{python3_sitearch}/glue/__init__.py
%{python3_sitearch}/glue/__pycache__/__init__.cpython-%{python3_version_nodots}.pyc
%{python3_sitearch}/glue/iterutils.py
%{python3_sitearch}/glue/__pycache__/iterutils.cpython-%{python3_version_nodots}.pyc
%{python3_sitearch}/glue/git_version.py
%{python3_sitearch}/glue/__pycache__/git_version.cpython-%{python3_version_nodots}.pyc

%changelog
* Wed Feb 20 2019 Ryan Fisher <rpfisher@syr.edu>
- Major version update with many changes and removal of segments subpackage.

* Tue Jun 19 2018 Ryan Fisher <rpfisher@syr.edu>
- 1.59.2 removing old M2Crypto import hiding in LDBDWClient.py.

* Thu Jun 7 2018 Ryan Fisher <rpfisher@syr.edu>
- 1.59.1 adding more python 3 package generation.

* Tue Jun 5 2018 Ryan Fisher <rpfisher@syr.edu>
- Pre O-3 release with removal of old codes, more packaging changes, better testing and more Python 3 compatibility.

* Tue Mar 13 2018 Ryan Fisher <rpfisher@syr.edu>
- Pre O-3 release with packaging changes, better testing and more Python 3 compatibility.

* Tue Jun 13 2017 Ryan Fisher <rpfisher@syr.edu>
- Mid O2 release to include M2Crypto removal and Kipp packaging changes.

* Thu Apr 13 2017 Duncan Macleod <duncan.macleod@ligo.org>
- Switched dependency from M2Crypto -> pyOpenSSL.

* Fri Apr 7 2017 Ryan Fisher <ryan.fisher@ligo.org>
- Added install_requires for pip installations.

* Thu Apr 6 2017 Ryan Fisher <ryan.fisher@ligo.org>
- Cleaned up RPM and debian codes.

* Thu Apr 6 2017 Duncan Brown <duncan.brown@ligo.org>
- O2 mid-run updated release. Change sdist name for PyPi compatibility.

* Wed Jan 25 2017 Ryan Fisher <rpfisher@syr.edu>
- O2 mid-run updated release. Updated python 3 compatibility fix from Leo to fix Debian package build for lalsuite.  Various updates from Kipp.

* Wed Oct 19 2016 Ryan Fisher <rpfisher@syr.edu>
- ER10 updated release. Python 3 compatibility from Leo, various updates from Kipp.

* Tue Sep 13 2016 Ryan Fisher <rpfisher@syr.edu>
- ER10 release. (forgot to update this changelog for last several releases)

* Thu Jul 23 2015 Ryan Fisher <rpfisher@syr.edu>
- Pre-ER8 release, attempt 2.

* Wed Jul 22 2015 Ryan Fisher <rpfisher@syr.edu>
- Pre-ER8 release.

* Fri May 22 2015 Ryan Fisher <rpfisher@syr.edu>
- ER7 release.

* Wed Nov 19 2014 Ryan Fisher <rpfisher@syr.edu>
- ER6 pre-release bug fix for dmt files method of ligolw_segment_query.

* Thu Nov 13 2014 Ryan Fisher <rpfisher@syr.edu>
- ER6 pre-release.

* Tue May 6 2014 Ryan Fisher <rpfisher@syr.edu>
- Version update to match git tag.

* Tue May 6 2014 Ryan Fisher <rpfisher@syr.edu>
- Sub-version release to add datafind to debian package.

* Tue Dec 3  2013 Ryan Fisher <rpfisher@syr.edu>
- ER5 release.

* Tue Jul 2 2013 Ryan Fisher <rpfisher@syr.edu>
- ER4 release, matching spec file.

* Tue Jul 2 2013 Ryan Fisher <rpfisher@syr.edu>
- ER4 release.

* Thu Mar 7 2013 Ryan Fisher <rpfisher@syr.edu>
- Post ER3 release of glue for pegasus 4.2 transition, added new RFC Proxy
    support.

* Fri Mar 1 2013 Ryan Fisher <rpfisher@syr.edu>
- Post ER3 release of glue for pegasus 4.2 transition.

* Mon Nov 19 2012 Ryan Fisher <rpfisher@syr.edu>
- New Release of glue for ER3 with updates to ligolw and lal codes.

* Tue Sep 4 2012 Ryan Fisher <rpfisher@syr.edu>
- New Release of glue with upgrades and bugfixes to segment database infrastructure.

* Fri May 18 2012 Ryan Fisher <rpfisher@syr.edu>
- Bugfix release of 1.39 labelled 1.39.2.  Includes fix to ligolw for URL reading, and packaging fixes.

* Fri May 11 2012 Ryan Fisher <rpfisher@syr.edu>
- Bugfix release of 1.39 labelled 1.39.1

* Thu May 10 2012 Ryan Fisher <rpfisher@syr.edu>
- New release of glue to replace Apr 12 near-release.  This includes ligolw changes and updates for job submission over remote pools.

* Thu Apr 12 2012 Ryan Fisher <rpfisher@syr.edu>
- New release of glue with updates to ligolw library, including some bug fixes for ligowl_sqlite and ligolw_print.

* Wed Nov 16 2011 Ryan Fisher <rpfisher@syr.edu>
- New release of glue with glue-segments and glue-common split from glue, lvalerts, lars and gracedb removed.

* Mon Oct 10 2011 Ryan Fisher <rpfisher@syr.edu>
- New release of glue to fix build issues called 1.36.

* Fri Oct 7 2011 Ryan Fisher <rpfisher@syr.edu>
- New release of glue with Kipp's fixes to ligolw_sqlite bugs, Kipp's checksums added, and Peter and my change to the coalescing script for segment databases.

* Thu Sep 29 2011 Ryan Fisher <rpfisher@syr.edu>
- New release of glue with speedup to string to xml conversion and 10 digit gps fixes.

* Wed Sep 15 2010 Peter Couvares <pfcouvar@syr.edu>
- New release of glue with GEO publishing

* Thu Apr 22 2010 Duncan Brown <dabrown@physics.syr.edu>
- Third S6 release of glue

* Wed Nov 11 2009 Duncan Brown <dabrown@physics.syr.edu>
- Second S6 release of glue

* Mon Jul 27 2009 Duncan Brown <dabrown@physics.syr.edu>
- First S6 release of glue

* Wed Jul 01 2009 Duncan Brown <dabrown@physics.syr.edu>
- Pre S6 release of glue

* Wed Jun 24 2009 Duncan Brown <dabrown@physics.syr.edu>
- Post E14 release of glue

* Thu Jun 11 2009 Duncan Brown <dabrown@physics.syr.edu>
- Allow segment tools to see multiple ifos

* Wed Jun 10 2009 Duncan Brown <dabrown@physics.syr.edu>
- Restored LSCdataFindcheck and fixed debian control files

* Tue Jun 09 2009 Duncan Brown <dabrown@physics.syr.edu>
- Build for glue 1.19-1

* Tue Jun 24 2008 Ping Wei <piwei@syr.edu>
- Build for glue 1.18-1

* Thu Jun 19 2008 Duncan Brown <dabrown@physics.syr.edu>
- Build for glue 1.17

* Fri Nov 04 2005 Duncan Brown <dbrown@ligo.caltech.edu>
- Build for glue 1.6

* Tue Aug 23 2005 Duncan Brown <dbrown@ligo.caltech.edu>
- Initial build for glue 1.0
