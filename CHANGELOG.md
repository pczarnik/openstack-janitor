# Changelog

All notable changes to this project are documented in this file. The format
follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and versions
follow [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0] - 2026-07-22

### Added

- `orphan-snapshot-images` detector — flags Glance images whose
  `block_device_mapping` references a Cinder volume snapshot that no longer
  exists (hidden images included). Detector count is now seven.
- `janitor detectors` command — lists every registered detector and its
  description without connecting to a cloud.
- Short options for `janitor audit`: `-c/--cloud`, `-d/--detector`,
  `-f/--format`, `-h/--help`.

Thanks to @pczarnik for all three contributions.

## [0.1.1] - 2026-07-14

### Changed

- Lowered the minimum supported Python from 3.11 to 3.9. On older
  interpreters pip automatically resolves the newest compatible
  openstacksdk. CI now tests Python 3.9 through 3.13.

### Added

- Standalone Linux x86_64 binary attached to GitHub releases. Built against
  glibc 2.28, so it runs on RHEL 8-era hosts without any Python install.
- Install troubleshooting notes for old distro-patched pip versions.

## [0.1.0] - 2026-07-14

First release: the complete read-only audit story.

### Added

- `janitor audit` command that scans an OpenStack cloud and reports
  orphaned/wasteful resources, with cron-friendly exit codes
  (`0` clean, `1` findings, `2` unknown detector, `3` connection failure).
- Six read-only detectors:
  - `unattached-volumes` — volumes in `available` status with no attachments.
  - `unassociated-floating-ips` — floating IPs not associated with any port.
  - `orphaned-ports` — ports with no device owner and no device id.
  - `old-snapshots` — snapshots older than a threshold (default 90 days).
  - `shutoff-instances` — instances SHUTOFF for at least a threshold
    (default 30 days, conservative lower bound).
  - `unused-security-groups` — groups with no port attachment and no
    `remote_group_id` reference; the per-project `default` group is skipped.
- `--format table|json|html` report output.
- `--cloud` (named cloud from `clouds.yaml`) and repeatable `--detector`
  selection.
- Non-admin fallback: detectors that use admin-only `all_projects` listings
  retry scoped to the caller's own project when forbidden.

[0.2.0]: https://github.com/mabunemeh/openstack-janitor/releases/tag/v0.2.0
[0.1.1]: https://github.com/mabunemeh/openstack-janitor/releases/tag/v0.1.1
[0.1.0]: https://github.com/mabunemeh/openstack-janitor/releases/tag/v0.1.0
