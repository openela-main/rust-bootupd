%bcond_without check

%global crate bootupd

Name:           rust-%{crate}
Version:        0.2.28
Release:        3%{?dist}
Summary:        Bootloader updater

License:        Apache-2.0
URL:            https://github.com/coreos/bootupd
Source0:        %{url}/releases/download/v%{version}/bootupd-%{version}.tar.zstd
Source1:        %{url}/releases/download/v%{version}/bootupd-%{version}-vendor.tar.zstd
%if 0%{?fedora} || 0%{?rhel} >= 10
ExcludeArch:    %{ix86}
%endif

Patch0:         0001-install-attempt-to-use-an-already-mounted-ESP-at-the.patch

BuildRequires: git
# For now, see upstream
BuildRequires: make
BuildRequires:  openssl-devel
%if 0%{?rhel}
BuildRequires: rust-toolset
%else
BuildRequires:  cargo-rpm-macros >= 25
%endif
BuildRequires:  systemd

%global _description %{expand:
Bootloader updater}
%description %{_description}

%package     -n %{crate}
Summary:        %{summary}
# Apache-2.0
# Apache-2.0 OR BSL-1.0
# Apache-2.0 OR MIT
# Apache-2.0 WITH LLVM-exception
# Apache-2.0 WITH LLVM-exception OR Apache-2.0 OR MIT
# BSD-3-Clause
# MIT
# MIT OR Apache-2.0
# Unlicense OR MIT
License:        Apache-2.0 AND (Apache-2.0 WITH LLVM-exception) AND BSD-3-Clause AND MIT AND (Apache-2.0 OR BSL-1.0) AND (Apache-2.0 OR MIT) AND (Apache-2.0 WITH LLVM-exception OR Apache-2.0 OR MIT) AND (Unlicense OR MIT)
%{?systemd_requires}

%description -n %{crate} %{_description}

%files -n %{crate}
%license LICENSE
%license LICENSE.dependencies
%license cargo-vendor.txt
%doc README.md
%{_bindir}/bootupctl
%{_libexecdir}/bootupd
%{_prefix}/lib/bootupd/grub2-static/
%{_unitdir}/bootloader-update.service

%prep
%autosetup -n %{crate}-%{version} -p1 -Sgit -a1
# Default -v vendor config doesn't support non-crates.io deps (i.e. git)
cp .cargo/vendor-config.toml .
%cargo_prep -N
cat vendor-config.toml >> .cargo/config.toml
rm vendor-config.toml

%build
%cargo_build
%cargo_vendor_manifest
# https://pagure.io/fedora-rust/rust-packaging/issue/33
sed -i -e '/https:\/\//d' cargo-vendor.txt
%cargo_license_summary
%{cargo_license} > LICENSE.dependencies

%install
%make_install INSTALL="install -p -c"
%{__make} install-grub-static DESTDIR=%{?buildroot} INSTALL="%{__install} -p"
%{__make} install-systemd-unit DESTDIR=%{?buildroot} INSTALL="%{__install} -p"

%changelog
* Wed Feb 12 2025 Joseph Marrero <jmarrero@fedoraproject.org> - 0.2.27-3
- spec: remove ExcludeArch ix86 as this is c9s
  Resolves: #RHEL-77736, #RHEL-79091

* Wed Feb 12 2025 Joseph Marrero <jmarrero@fedoraproject.org> - 0.2.27-2
- Add git to the build requires
  Resolves: #RHEL-77736, #RHEL-79091

* Wed Feb 12 2025 Joseph Marrero <jmarrero@fedoraproject.org> - 0.2.27-1
- https://github.com/coreos/bootupd/releases/tag/v0.2.27
  Resolves: #RHEL-77736

* Thu Dec 12 2024 HuijingHei <hhei@redhat.com> - 0.2.25-1
- new version

* Fri May 17 2024 Joseph Marrero <jmarrero@fedoraproject.org> - 0.2.19-1
- https://github.com/coreos/bootupd/releases/tag/v0.2.19
  Resolves: RHEL-35887

* Thu Feb 22 2024 Joseph Marrero <jmarrero@fedoraproject.org> - 0.2.18-1
- https://github.com/coreos/bootupd/releases/tag/v0.2.18
  backport patch to support GRUB console.cfg
  Resolves: RHEL-26439

* Tue Dec 19 2023 Joseph Marrero <jmarrero@fedoraproject.org> - 0.2.17-1
- https://github.com/coreos/bootupd/releases/tag/v0.2.17
  Resolves: RHEL-14388

* Fri Dec 15 2023 Huijing Hei <hhei@redhat.com> - 0.2.16-4
- Sync spec with upstream
  Related: https://issues.redhat.com/browse/RHEL-14388

* Wed Dec 13 2023 Colin Walters <walters@verbum.org> - 0.2.16-3
- Build on all architectures
  Related: https://issues.redhat.com/browse/RHEL-14388

* Wed Dec 13 2023 Colin Walters <walters@verbum.org> - 0.2.16-2
- Update to 0.2.16
  Related: https://issues.redhat.com/browse/RHEL-14388

* Tue Nov 28 2023 Colin Walters <walters@verbum.org> - 0.2.15-2
- https://github.com/coreos/bootupd/releases/tag/v0.2.15
  Related: https://issues.redhat.com/browse/RHEL-14388

* Fri Oct 20 2023 Colin Walters <walters@verbum.org> - 0.2.12-2
- https://github.com/coreos/bootupd/releases/tag/v0.2.12

* Tue Sep 19 2023 Colin Walters <walters@verbum.org> - 0.2.11-2
- https://github.com/coreos/bootupd/releases/tag/v0.2.11
  Resolves: https://issues.redhat.com/browse/RHEL-5273

* Mon Aug 01 2022 Colin Walters <walters@verbum.org> - 0.2.7-2
- https://github.com/coreos/bootupd/releases/tag/v0.2.7

* Thu Sep 16 2021 Luca BRUNO <lucab@lucabruno.net> - 0.2.6-1
- New upstream version
  https://github.com/coreos/bootupd/releases/tag/v0.2.6

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jan  6 14:48:03 UTC 2021 Colin Walters <walters@verbum.org> - 0.2.5-2
- https://github.com/coreos/bootupd/releases/tag/v0.2.5

* Tue Dec 15 14:48:20 UTC 2020 Colin Walters <walters@verbum.org> - 0.2.4-2
- https://github.com/coreos/bootupd/releases/tag/v0.2.4

* Tue Nov 17 14:33:06 UTC 2020 Colin Walters <walters@verbum.org> - 0.2.3-2
- https://github.com/coreos/rpm-ostree/bootupd/tag/v0.2.3

* Wed Nov 11 18:07:38 UTC 2020 Colin Walters <walters@verbum.org> - 0.2.2-2
- Update to 0.2.2

* Mon Nov  2 23:03:03 UTC 2020 Colin Walters <walters@verbum.org> - 0.2.0-3
- Switch to vendored sources since RHEL requires it

* Mon Oct 26 15:06:37 UTC 2020 Colin Walters <walters@verbum.org> - 0.2.0-2
- https://github.com/coreos/bootupd/releases/tag/v0.2.0

* Tue Oct 13 2020 Colin Walters <walters@verbum.org> - 0.1.3-2
- https://github.com/coreos/bootupd/releases/tag/v0.1.3

* Tue Sep 22 2020 Colin Walters <walters@verbum.org> - 0.1.2-2
- New upstream

* Mon Sep 21 2020 Colin Walters <walters@verbum.org> - 0.1.1-2
- Also build on aarch64

* Fri Sep 11 2020 Colin Walters <walters@verbum.org> - 0.1.0-3
- Initial package

