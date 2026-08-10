# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- **k3s container log rotation defaults**: `k3s_container_log_max_size`
  (`10Mi`) and `k3s_container_log_max_files` (`5`) now have defaults in
  `defaults/main.yml` and entries in `meta/argument_specs.yml`. Both were
  previously only read by an `is defined` guard in the agent config template,
  so out of the box kubelet never received `container-log-max-size` /
  `container-log-max-files` and container logs grew unbounded. The guards stay
  in place, so setting `k3s_container_log_max_size` to `""` or
  `k3s_container_log_max_files` to `0` still omits the respective flag.

- **k3s hardening variables**: eight new variables defined in both
  `defaults/main.yml` and `meta/argument_specs.yml` —
  `k3s_secrets_encryption`, `k3s_protect_kernel_defaults`,
  `k3s_audit_log_enabled`, `k3s_audit_log_maxage`, `k3s_anonymous_auth`,
  `k3s_node_restriction`, `k3s_kubelet_read_only_port_disabled`,
  `k3s_audit_log_level` and `k3s_pod_security_admission_profile`. All are gated
  by `k3s_security_hardening`, which previously only covered SELinux/AppArmor.
- **k3s audit policy**: renders `audit-policy.yaml` and passes
  `audit-policy-file` to the kube-apiserver when audit logging is enabled.
  Without a policy file the apiserver matches no events and the audit log stays
  empty. Drops high-volume node/proxy and health-endpoint traffic, caps secrets
  and configmaps at `Metadata`, and logs everything else at
  `k3s_audit_log_level`.
- **k3s Pod Security Admission**: optional cluster-wide default profile via
  `k3s_pod_security_admission_profile` (empty by default, so no behaviour
  change). Renders `psa-config.yaml` with `kube-system` exempt and wires it as
  `admission-control-config-file`.
- **k3s molecule hardening assertions**: `verify.yml` checks the rendered
  config for the hardening flags, `k3s secrets-encrypt status` for `Enabled`,
  the credential directory for `0700`, and that a user-supplied
  `kube-apiserver-arg` survives the hardening merge.
- **Molecule coverage** for the five previously-untested roles, each with a
  `default` scenario under `roles/<role>/molecule/default/` and a matching
  `molecule-<role>` job wired into `pull-request.yml` (qemu/KVM driver,
  Ubuntu 22.04 cloud image, pinned to `ci-ansible-molecule.yml@2026-06-18`).
- **docker_login** molecule — full converge: a `prepare.yml` installs Docker via
  the `docker` role and starts a throwaway local `registry:2` container,
  converge logs into `localhost:5000`, and verify asserts the registry appears
  under `auths` in the Docker client config.
- **docker_compose_v2** molecule — full converge: `prepare.yml` installs Docker,
  converge deploys a minimal `nginx` compose project, and verify asserts the
  compose plugin, the rendered project file, the systemd unit and a running
  container.
- **helm**, **fleet**, **tailscale** molecule — syntax-only scenarios
  (`test_sequence` stops after `syntax`). These roles drive a live Kubernetes
  API (HelmChart CRDs, Rancher Fleet GitOps CRDs, the Tailscale operator CRDs)
  and cannot converge without a running cluster; standing up k3s per role would
  make CI slow and flaky, so the converge/verify against a real cluster is
  deferred and documented at the top of each `molecule.yml`. Syntax checking
  still validates playbook/role wiring cheaply.

### Fixed

- **k3s server nodes ignored container log rotation**: the
  `container-log-max-size` and `container-log-max-files` kubelet args were only
  built by `agent-config.yaml.j2`, so a server node never rotated container
  logs even with the variables set. `server-config.yaml.j2` now builds the same
  two args, and `molecule/default/verify.yml` asserts both reach the rendered
  config.

- **k3s server config template used the pre-migration fact spelling**: the
  `ansible_facts` migration left
  `templates/etc/rancher/k3s/server-config.yaml.j2` on `ansible_local.k3s`,
  while the sister template `agent-config.yaml.j2` in the same role had already
  moved to `ansible_facts['ansible_local']['k3s']`. Both templates read the same
  fact in two different spellings. No behaviour change: `ansible_local` is
  exempt from the `INJECT_FACTS_AS_VARS` deprecation and is always promoted to
  the top level, so the old spelling still resolved. A sweep for
  `ansible_local.` across `roles/` confirms this was the last remaining
  occurrence.

- **k3s environment variables were never rendered**: `k3s_environment_vars` was
  fully wired — documented in `defaults/main.yml`, declared as a `dict` in
  `meta/argument_specs.yml`, consumed by
  `templates/etc/systemd/system/k3s.service.env.j2` and loaded by the unit via
  `EnvironmentFile=` — but the task that renders the file was commented out in
  `roles/k3s/tasks/utilities.yml`. Setting `HTTP_PROXY`/`HTTPS_PROXY`, the
  documented use case, produced no error and no file: the leading `-` in
  `EnvironmentFile=-` makes systemd treat the missing file as fine, so k3s ran
  without proxy settings and failed image pulls silently. The task is active
  again and notifies `Restart k3s` instead of the stale lowercase handler name
  `restart k3s`, which no longer exists. Because `utilities.yml` is included
  after the role has already flushed its handlers and waited for the API server,
  the task flushes handlers itself and waits for the server to come back, so a
  following play never meets a restarting cluster. `verify.yml` asserts the file
  is rendered `0600` and carries the value set through `k3s_environment_vars`,
  matching it with `grep` instead of reading the file into a variable.
- **k3s environment file broke idempotence**: the environment template rendered
  `K3S_TOKEN` whenever `k3s_token` was set. On a fresh node the variable is
  empty during the first run and only read back once the datastore exists, so
  the line appeared on the second run and rewrote the file every time. The
  template no longer renders the token; `server-config.yaml.j2` already writes
  it into `config.yaml`, which the unit loads through `K3S_CONFIG_FILE`, so the
  join credential now lives in one file instead of two. `verify.yml` asserts the
  environment file carries no `K3S_TOKEN=` line.
- **k3s secrets encryption was silently off**: `server-config.yaml.j2`
  referenced `k3s_secrets_encryption`, `k3s_protect_kernel_defaults` and
  `k3s_audit_log_enabled`, but none of them were defined in `defaults/main.yml`
  or `argument_specs.yml`. Every default deployment therefore ran without
  secrets encryption while `k3s_security_hardening: true` suggested otherwise.
- **k3s dead permission tasks**: the kubeconfig, token-file and credential
  directory permission tasks were commented out, making `k3s_kubeconfig_mode`,
  `k3s_kubeconfig_owner` and `k3s_kubeconfig_group` dead configuration. All
  three are restored with a `stat` pre-check, since `security.yml` runs before
  the installation. The orphaned `stat` on the credential directory has its
  consumer back.
- **k3s bash completion never ran**: both completion tasks in
  `roles/k3s/tasks/utilities.yml` were gated on `k3s_completion_test`, a
  variable that was never registered anywhere in the collection, so the
  condition was always false and the tasks were silently skipped on every run
  despite `k3s_create_bash_completion` defaulting to `true`. The completion
  output is now generated by a dedicated probe task per binary and written with
  `ansible.builtin.copy`, which replaces the `changed_when: true` shell
  redirects and reports `changed` only when the file content actually differs.
  `verify.yml` asserts that both completion files exist and are non-empty.
- **k3s dead security blocks removed**: the commented-out audit-policy task
  referenced `templates/etc/kubernetes/audit-policy.yaml.j2`, which does not
  exist in the repository, and the commented-out debug summary duplicated the
  active debug task in the same file.
- **k3s `cluster-init` drift on re-runs**: the first server rewrote
  `config.yaml` and restarted k3s on every run after the first. `cluster-init`
  was derived from `k3s_server_init`, which follows `should_init` and requires
  the datastore to be absent — so the flag was written on the initial run and
  dropped on every later one. `cluster-init` is a bootstrap flag that k3s only
  evaluates while creating the datastore, so it is now kept for as long as this
  node runs the cluster. Secondary servers and agents keep writing `server:` as
  before.
- **k3s config drift on re-runs**: a server rewrote `config.yaml` and restarted
  k3s on every run after the first. On the initial run the cluster database does
  not exist yet, so the role initialises the cluster and `k3s_token` stays empty
  — the rendered config carries no `token`. From the second run on, the token
  file exists, the role reads it back and writes it into the config, which
  changes the file and notifies `Restart k3s`. A token read from the node's own
  `server/node-token` is redundant in `config.yaml` and is now left out of the
  server config. A token fetched from another host stays in place, so secondary
  servers and agents can still join.
- **docker_compose_v2 molecule idempotence**: the `default` scenario failed on
  the launch task with `Idempotence test failed`. `nginx:alpine` is an OCI image
  index with 16 manifests, and compose stores the resolved image ID in the
  container's `com.docker.compose.image` label. Once the tag resolved to a
  different ID than the stored one, compose recreated the container on every
  run — the config hash still matched on both sides, so only the image label
  differed. The converge image is now pinned by digest.
- **Secret masking**: tasks that read, render or transport credentials ran
  without `no_log: true`, so the values were printed with `-v` or in the task
  result. The k3s cluster join token (`slurp` + `set_fact` in
  `roles/k3s/tasks/main.yml`), the k3s config and registries templates, the
  Fleet GitRepo auth secret and the Fleet `ClusterRegistrationToken` lookup,
  and the `docker_login` registry login are now all masked. The `k3s_token`
  and `docker_login_password` options in `argument_specs.yml` carry `no_log`
  as well, matching the already-masked `k3s_etcd_s3_*` keys.
- **fleet argument_specs**: the main entry point used six separate `<<:` merge
  keys in one mapping, which `ruamel.yaml` (used by ansible-lint) rejects as
  duplicate keys. Consolidated into a single YAML 1.1 list-form merge
  (`<<: [*a, *b, ...]`); the merged result is byte-for-key identical.
- **omit defaults**: `docker_login` and `fleet` declared optional parameters
  with a string `default: "{{ omit }}"`, which fails argument-spec validation on
  Ansible 2.18+ for non-string types. Removed the string-omit defaults; the
  `docker_login` tasks now resolve those values with `| default(omit)`.

- **docker role**: the Docker prune service/timer setup called
  `arillso.system.systemd_unit`, a role that no longer exists in
  `arillso.system` (replaced by the `systemd` role with a `systemd_units`
  list interface), so the role failed with "role
  'arillso.system.systemd_unit' was not found". Rewrite the prune units in
  the `systemd_units` format and call `arillso.system.systemd`.
- **docker role**: add the missing `log-opts` option to the `docker_daemon`
  argument spec. `log-opts` is a valid `daemon.json` key but was absent from
  the spec, so passing it (e.g. log rotation `max-size`/`max-file`) failed
  argument validation.
- **docker role — hardening and merge documentation**: new `## Hardening`
  section in the role README covering the `no-new-privileges` opt-out and the
  `userns-remap` opt-in with its costs, plus a Quick Start that explains the
  merge semantics. The log-rotation troubleshooting entry now states that
  `max-size`/`max-file` are `json-file` options and are ignored under the
  default `journald` driver, which limits size via `SystemMaxUse` instead.
- **docker role — merge coverage in tests**: the molecule `verify.yml` asserts
  that role defaults survive a user-provided `docker_daemon` and that nested
  `log-opts` merge per sub-key; the integration target asserts the pure
  default path, which no test previously covered.

### Changed

- **Role-internal registers now carry a role prefix**: every register in
  `roles/helm` and `roles/k3s` was renamed to `_<role>_<name>`, so
  role-internal state no longer leaks into the play namespace. This covers
  both the 12 registers that carried no role prefix at all (`cluster_token`,
  `kubeconfig_check`, `facts_check` → `_k3s_cluster_token`,
  `_helm_kubeconfig_check`, `_k3s_facts_check`) and the 16 that already had
  one but no leading underscore (`helm_repo_check`, `k3s_release_checksum`,
  `k3s_selinux_restorecon` → `_helm_repo_check`, `_k3s_release_checksum`,
  `_k3s_selinux_restorecon`). The second group was already lint-clean;
  renaming it keeps a single style inside the two roles. The molecule verify
  playbooks for `docker` and `k3s` use the plain `<role>_<name>` form, since
  play-level variables are not role-internal. `k3s_token`, `k3s_token_file`
  and `k3s_token_source` are the role interface and are unchanged.
- **`ansible-lint` runs the production profile**: `.ansible-lint` gains
  `profile: production` and `strict: true`, and drops
  `var-naming[no-role-prefix]` from `skip_list`, which turns the prefix
  convention into an enforced rule. `package-latest` stays skipped.
- **BREAKING — k3s hardening now applies by default**: `k3s_secrets_encryption`,
  `k3s_anonymous_auth`, `k3s_node_restriction` and
  `k3s_kubelet_read_only_port_disabled` take effect on existing clusters running
  default variables. Secrets encryption restarts K3s (no data loss);
  `anonymous-auth=false` breaks anonymous health probes; `NodeRestriction`
  breaks node credentials modifying foreign node objects; `read-only-port=0`
  breaks collectors on kubelet port 10255. Set `k3s_security_hardening: false`
  to keep the previous behaviour.
- **k3s apiserver and kubelet args merge instead of overwrite**:
  `k3s_kube_apiserver_args` and `k3s_kubelet_args` previously replaced the
  argument list wholesale, leaving no room for role-managed hardening flags.
  They are now appended after the hardening args, so a user-supplied duplicate
  still wins (K3s keeps the last occurrence of a repeated flag).
- **docker role — daemon config is now merged, not replaced** (BREAKING).
  `/etc/docker/daemon.json` is rendered from the new `docker_daemon_base`
  (role defaults) recursively merged with `docker_daemon` (user config,
  now defaulting to `{}`). Previously the template rendered `docker_daemon`
  alone, so any playbook setting it silently dropped the role defaults
  `log-driver: journald` and `live-restore: true`. Existing playbooks keep
  working and additionally inherit the defaults; to drop a base key instead
  of overriding it, replace `docker_daemon_base`. The per-key `default:`
  entries for `log-driver` and `live-restore` were removed from the
  `docker_daemon` argument spec, since argument validation would otherwise
  inject them into the user dict and defeat the merge.
- **docker role — `no-new-privileges: true` is now a default** (BREAKING).
  Set in `docker_daemon_base`, so new containers can no longer gain
  privileges via setuid/setgid binaries. Images relying on them (e.g. `sudo`,
  some `ping` builds) will break. Opt out with
  `docker_daemon: {no-new-privileges: false}`. `userns-remap` deliberately
  stays opt-in; see the role README for its costs.
- **Deprecated syntax**: replace top-level `ansible_*` fact references with
  `ansible_facts['...']` across the docker, k3s and helm roles (and their
  `defaults`/`argument_specs`), and migrate the docker Debian/Ubuntu
  repository tasks from the deprecated `ansible.builtin.apt_repository` to
  `ansible.builtin.deb822_repository`. Removes the `INJECT_FACTS_AS_VARS`
  (core 2.24) and `apt_repository` (core 2.25) deprecation warnings. The
  docker role now installs `python3-debian` (required by
  `deb822_repository`) and removes any legacy `docker.list` left by earlier
  role versions to avoid a duplicate apt source. A follow-up pass covers the
  references the first migration missed: the `hostvars[...]['ansible_*']`
  lookups in `install_docker_redhat.yml` and the k3s server-URL fallbacks,
  `ansible_local.k3s` → `ansible_facts['ansible_local']['k3s']` on the k3s
  cluster-init path and in the agent config template, plus
  `ansible_swaptotal_mb` and the molecule/integration references. Custom facts
  keep their `ansible_local` key inside `ansible_facts`, unlike the built-in
  facts that drop the `ansible_` prefix there.
- **Renovate**: track the `python_version` CI input via Renovate. Each
  `python_version:` in `pull-request.yml`/`merge.yml` carries a
  `# renovate: datasource=github-releases depName=python/cpython` marker, and
  the local regex manager now scans `.github/workflows/*.yml`, so the Python
  version is bumped automatically instead of drifting hardcoded.
- **Dependency**: raise the `arillso.system` lower bound from `>=0.0.17` to
  `>=1.0.0` — the `systemd` role with the `systemd_units` interface the docker
  role now uses is only available from 1.0.0 onwards.
- **Molecule (CI)**: run the docker and k3s scenarios on both Ubuntu 22.04 and
  Debian 12 (was Ubuntu-only), restoring the two-distro coverage from the
  pre-KVM docker-driver setup.
- Align the release workflow with the org convention: set
  `name: Release - Ansible Collection`, simplify `run-name` to
  `Release <ref>`, use a `release-<ref>` concurrency group, rename the job to
  `release`, and pin the reusable workflow to `@2026-06-18`.
- `.python-version` `3.14` → `3.13` (org-wide target — `3.14` is rejected by
  `ansible-test`, which supports at most `3.13`).
- Security scan runs as `nightly-security.yml` (`name: Nightly Security Scan`)
  on a daily cron (`0 2 * * *`). Per the repo-standard visibility rule, public
  repos run the scan daily (free Actions minutes); private repos run it weekly.
- `LICENSE` copyright `2025` → `2023-2026` (org range `FIRST-CURRENT`,
  consistent with the README).
- **Role metadata**: drop EOL Ubuntu `focal` (and Debian `buster` where present)
  from `galaxy_info.platforms` across all roles; ensure `jammy`/`noble` and
  `bullseye`/`bookworm` are listed.
- **Role READMEs**: add a `Troubleshooting` section to the `docker`, `k3s`, and
  `fleet` READMEs and correct the `helm` README, which documented a non-existent
  `helm_version` binary install — the role drives the K3s-embedded Helm
  controller via `HelmChart` CRDs, so the Quick Start now uses `helm_charts`.

## [1.4.0] - 2026-06-12

### Added

- New `k3s_etcd_s3_access_key` / `k3s_etcd_s3_secret_key` variables in the k3s
  role: render `etcd-s3-access-key` / `etcd-s3-secret-key` into the server
  config so scheduled etcd snapshots can authenticate against S3-compatible
  storage (e.g. Cloudflare R2). The config file is deployed with mode `0600`,
  so credentials stay root-only on disk. Both variables are optional and
  omitted when unset — existing consumers are unaffected.
- New `k3s_health_check_delay` / `k3s_health_check_timeout` /
  `k3s_health_check_sleep` variables (defaults `30` / `600` / `10`,
  backwards-compatible) parametrise the server API readiness probe in the
  k3s role. The `wait_for` task previously hard-coded `delay: 30`, an
  unconditional pre-sleep on every run; consumers running against an
  already-converged server can now set `k3s_health_check_delay: 0` to skip
  the idle wait while `timeout`/`sleep` still cover the cold-bootstrap race.

### Changed

- Documented the full etcd snapshot variable family in the k3s role's
  `argument_specs.yml` (`k3s_etcd_expose_metrics`,
  `k3s_etcd_snapshot_schedule_cron`, `k3s_etcd_snapshot_retention`,
  `k3s_etcd_snapshot_dir`, `k3s_etcd_s3`, `k3s_etcd_s3_endpoint`,
  `k3s_etcd_s3_region`, `k3s_etcd_s3_bucket`, `k3s_etcd_s3_folder` plus the two
  new credential variables). These were previously template-only and
  undocumented. All are `required: false` and carry no spec default — the
  template gates each with `is defined`, so a default would change behaviour —
  and the two credential keys are marked `no_log: true`.

### Fixed

- `docker_compose_v2` role: removed bogus `"{{ omit }}"` defaults for optional
  variables. The literal placeholder string broke argument-spec validation for
  non-`str`-typed vars (`docker_compose_v2_scale` as `dict`,
  `_files`/`_profiles`/`_services` as `list[str]`) under Ansible 2.18+.
  Optional vars are now intentionally undefined and the module-call kwargs
  apply `| default(omit)` to emit a real omit sentinel. End behaviour is
  unchanged for consumers that did not override these vars.

## [1.3.13] - 2026-05-03

### Added

- New `k3s_cri_apparmor_profile_enabled` variable (default `true`,
  backwards-compatible) to opt out of deploying the `cri-containerd.apparmor.d`
  profile in the k3s role; when set to `false` the role unloads the profile
  from the kernel, removes the file, and notifies `Restart k3s`. Workaround
  for kernel 6.17 AppArmor profile-stacking bugs
  ([k3s-io/k3s#13625](https://github.com/k3s-io/k3s/issues/13625),
  [containerd/containerd#12886](https://github.com/containerd/containerd/issues/12886))
  which cause pod termination to hang and flood dmesg with SIGURG denials

## [1.3.12] - 2026-04-01

### Changed

- Reverted unrestricted `signal,` AppArmor rule back to targeted peer-specific rules in k3s security profile; restricts signal operations to known peers (host and containerd manager) for a tighter security posture while maintaining full functionality
- Added `signal (send) peer=cri-containerd.apparmor.d` rule to allow container processes to signal each other (e.g. PID 1 sending SIGTERM to children during graceful shutdown)

## [1.3.11] - 2026-03-31

### Fixed

- Replaced restrictive AppArmor signal rules (`signal (receive) peer=unconfined` and `signal (receive) peer=cri-containerd.apparmor.d`) with unrestricted `signal,` in k3s security profile; runc requires full signal capabilities (send/receive) to deliver SIGTERM/SIGKILL to container init processes during pod termination

## [1.3.10] - 2026-03-28

### Fixed

- Deploy `/etc/apparmor.d/cri-containerd.apparmor.d` with `change_profile -> **,` in k3s role;
  on Ubuntu 24.04 (kernel 6.8, AppArmor 4.x) containerd generates this profile dynamically
  without the rule, causing `kubectl exec` to fail with
  `apparmor failed to apply profile: write fsmount:fscontext:proc/thread-self/attr/apparmor/exec:
operation not permitted`. Pre-deploying the fixed profile ensures runc can apply AppArmor
  profiles to exec'd container processes.

## [1.3.9] - 2026-03-28

### Fixed

- Replaced invalid `fsmount,` AppArmor rule (parse error: `unexpected TOK_END_OF_RULE, expecting TOK_MODE`) with `change_profile -> **,` in k3s security profile; this allows containerd to write the target profile name to `/proc/thread-self/attr/apparmor/exec` before exec, which is how AppArmor profiles are applied to container processes

## [1.3.8] - 2026-03-28

### Fixed

- Added `fsmount,` AppArmor rule to k3s security profile; required for AppArmor 4.x (kernel >= 6.x) where containerd writes the AppArmor exec profile via the `fsmount` LSM hook when applying profiles to container processes (`apparmor failed to apply profile: write fsmount:fscontext:proc/thread-self/attr/apparmor/exec: operation not permitted`)
- Moved Docker GPG key from deprecated `/etc/apt/trusted.gpg.d/` to `/etc/apt/keyrings/` and added task to create the keyrings directory; fixes apt warnings on Ubuntu 22.04+ that treat keys outside `/etc/apt/keyrings/` as untrusted

## [1.3.7] - 2026-03-21

### Fixed

- Added AppArmor rule `/proc/thread-self/attr/** rw` to k3s security profile; required for containerd to apply AppArmor profiles to container exec processes (`apparmor failed to apply profile: write /proc/thread-self/attr/apparmor/exec: operation not permitted`)

## [1.3.6] - 2026-03-21

### Fixed

- Fixed k3s binary upgrade being skipped due to HTTP 304 Not Modified from cached ETag; replaced `force: true` workaround with proper SHA256 checksum verification fetched from the k3s GitHub release — Ansible now compares the local binary against the expected checksum locally, bypassing HTTP cache entirely

## [1.3.5] - 2026-03-21

### Fixed

- Fixed invalid AppArmor permission `rwxk` → `rwixk` for `/var/lib/kubelet/plugins/**` in k3s security profile; bare `x` must be preceded by an exec qualifier (`i`, `p`, or `u`)

## [1.3.4] - 2026-03-21

### Fixed

- Added missing AppArmor rule `/var/lib/kubelet/** rwk` to k3s security profile for kubelet pod management including etc-hosts, projected volumes, and plugin sockets
- Added AppArmor rule `/var/lib/kubelet/plugins/** rwxk` for CSI driver and device plugin binary execution
- Added AppArmor rules for CNI state (`/var/lib/cni/** rwk`) and CNI binary execution (`/opt/cni/bin/** rix`)
- Added `unix,` AppArmor rule for Unix domain socket mediation required on kernel ≥ 6.17

## [1.3.3] - 2026-03-20

### Fixed

- Fixed missing `meta/main.yml` in tailscale role causing Galaxy import warning "Could not get role description, no role metadata found" (#57)
- Added missing AppArmor proc rules for containerd: `/proc/thread-self/mountinfo r` and `/proc/*/net/** r` to prevent AppArmor denials in k3s role (#58)

## [1.3.2] - 2026-03-20

### Fixed

- Fixed remaining k3s handler name case mismatches: `reload systemd` → `Reload systemd` and `restart k3s` → `Restart k3s` in systemd service task
- Added `meta: flush_handlers` before k3s server health check to ensure server restarts before agents attempt to connect
- Fixed AppArmor configuration block missing `when: k3s_security_framework == "apparmor"` condition, causing AppArmor tasks to run on all systems
- Renamed `security_framework` set_fact variable to `k3s_security_framework` to follow role naming convention and prevent collisions with other roles

## [1.3.1] - 2026-03-20

### Fixed

- Fixed k3s role handler name case mismatch: `restart k3s` → `Restart k3s` causing deployment failures when k3s binary or config changes trigger a service restart

## [1.3.0] - 2026-03-19

### Added

- Added k3s upgrade path validation: blocks downgrades and enforces one-minor-version-at-a-time upgrades
- Added automatic k3s binary upgrade detection by comparing installed version with target `k3s_version`
- Added upgrade documentation to k3s role README

## [1.2.0] - 2026-03-18

### Added

- Added comprehensive argument specs for K3s role covering networking, storage, security, service, and facts variables (#46)
- Added K3s facts configuration variables (`k3s_facts_collect_cluster_state`, `k3s_facts_collect_service_status`, `k3s_facts_collect_inventory_info`, `k3s_facts_collect_health_metrics`) with expanded fact template (#51)
- Added K3s facts dependency wiring to `arillso.system.facts` role via configurable variables (#51)
- Added `docker_compose_v2_scale` and `docker_compose_v2_build`/`docker_compose_v2_ca_path` argument specs for Docker Compose v2 role (#45)
- Added `fleet_registration_tokens`, Fleet authentication defaults (`fleet_git_username`, `fleet_git_token`, etc.) and missing argument specs (`fleet_dry_run`, `fleet_secret_timeout`, `fleet_resource_timeout`) for Fleet role (#45)
- Added nested `options` for `helm_defaults` in Helm role argument specs (#45)
- Added Makefile with targets for lint, test, format, build, clean, and install-dev (#44)
- Added pyproject.toml with black, isort, ruff, and pytest configuration (#44)
- Added pre-commit configuration with trailing-whitespace, end-of-file-fixer, and ansible-lint hooks (#44)
- Added security scanning configurations: checkov, gitleaks, grype, trivy, secretlint (#44)
- Added markdownlint, markdown-link-check, jscpd, and kics configuration files (#44)

### Changed

- Renamed `k3s_facts_health_check_interval` to `k3s_facts_health_check_timeout` (#51)
- Changed `k3s_enable_helm_integration` default from `true` to `false` (#51)
- Changed `docker_compose_v2_recreate` default from `smart` to `auto` and added type to `docker_compose_v2_pull` (#45)
- Updated `docker_version` default in argument specs to `28.5.2`, `docker_compose_v2_version` to `5.1.0` (#45)
- Renamed Fleet auth variables to use `fleet_` prefix (`git_username` → `fleet_git_username`, etc.) (#45)
- Updated `helm_repositories` default to include `noqa: argument-specs` annotation (#45)
- Replaced `.yamllint.yml` with comprehensive `.yamllint` configuration (stricter rules, 160 char line limit) (#44)
- Modernized `.ansible-lint` configuration (removed `experimental` skip, cleaned up formatting) (#44)
- Expanded `.gitignore` with testing, build, and environment patterns (#44)
- Simplified CONTRIBUTING.md (reduced from 334 to 167 lines, modernized prerequisites to Python 3.12/Ansible 2.18) (#44)
- Migrated pytest configuration from `pytest.ini` to `pyproject.toml` (#44)
- Bumped `requires_ansible` from `>=2.15.5` to `>=2.18.0` in `meta/runtime.yml` (#44)
- Updated Renovate config to pin shared preset version and add custom regex manager for role defaults (#43)
- Updated CI workflows to `@2026-03-09` shared workflow refs (#43)
- Restricted Claude AI workflow triggers to `@claude` mentions only (#43)
- Updated Claude review to trigger only on PR open events (#43)
- Updated Python development dependencies (pytest-cov v7, molecule v26/v25, ansible-lint v26, black v26, sphinx v9, and others) (#47, #48, #49, #50, #52)

### Removed

- Removed `k3s_require_facts_role` variable from K3s defaults (#51)

## [1.1.0] - 2026-03-08

### Changed

- Migrated CI/CD workflows to shared reusable workflows from `arillso/.github`
- Updated Docker Engine default version from 27.5.1 to 28.5.2
- Updated Docker Compose v2 default version from 2.32.4 to 5.1.0
- Updated K3s default version from v1.33.3+k3s1 to v1.35.2+k3s1
- Updated Python development dependencies (pytest-cov, pylint, sphinx-rtd-theme)
- Updated documentation links with UTM tracking parameters
- Excluded `ansible-core` from Renovate updates (version controlled by CI matrix)

### Added

- Added Claude AI workflow for automated issue and PR handling
- Added Claude AI review workflow for pull requests

## [1.0.2] - 2026-01-17

### Fixed

- Fixed K3s role Galaxy validation errors by removing invalid `no_log` field from argument_specs.yml
- Fixed Fleet role Galaxy validation errors by replacing YAML anchor references with explicit descriptions
- Resolved 13 total validation errors preventing proper indexing on Ansible Galaxy
- K3s and Fleet roles now properly documented and searchable on Galaxy

## [1.0.1] - 2026-01-16

### Fixed

- Fixed K3s configuration directory permissions causing unnecessary 'changed' status on every run
- Improved K3s AppArmor profile with comprehensive permissions for container operations
- Added sys_chroot, sys_ptrace, dac_override capabilities
- Added xtables-nft-multi, nft, modprobe subprocess execution permissions
- Expanded proc/sys and sys filesystem access for full K3s functionality
- Added file locking support (k flag) to k3s data directory
- Added ptrace permissions for containerd process management
- Improved Galaxy collection description for better discoverability

### Changed

- Disabled K3s AppArmor profile by default (k3s_apparmor_profile: false)
- K3s configuration directory now created with correct 0700 permissions from the start

## [1.0.0] - 2026-01-15

### Added

- Added new K3s role with comprehensive Kubernetes support (v1.33.3+k3s1)
- Added new Helm role for Kubernetes package management
- Added new Fleet role for Rancher Fleet GitOps management
- Added new Tailscale role with support for all ProxyGroup types (ingress, egress, kube-apiserver)
- Added GitHub issue templates (bug report, documentation, feature request)
- Added GitHub pull request template
- Added comprehensive documentation (AGENTS.md, CONTRIBUTING.md, CLAUDE.md)
- Added filter plugins for Fleet management with 15 unit tests
- Added CI/CD workflow with integrated linting and testing
- Added Molecule tests for Docker and K3s roles
- Added integration tests for Docker and K3s roles
- Added argument_specs.yml for all roles with complete variable documentation
- Added K3s security hardening (SELinux, AppArmor) with auto-detection
- Added K3s auto-facts collection with caching
- Added K3s private registry configuration support
- Added logrotate configuration for K3s logs
- Added EditorConfig for consistent code style
- Added yamllint configuration
- Added pytest configuration
- Added Renovate for automated dependency management
- Added CODEOWNERS file

### Changed

- Updated README to include all 8 roles
- Updated copyright years to 2023-2026 across all files
- Updated ansible-lint configuration to use extended profile
- Updated Docker platform support to EL 8/9
- Updated all roles to use FQCN (Fully Qualified Collection Names)
- Improved role READMEs with links to guide.arillso.io
- Consolidated all tests (unit, molecule, integration) into single CI workflow
- Reduced comments in defaults/main.yml files for better readability
- Refactored Tailscale role to support unified ProxyGroup management

### Removed

- Removed deprecated docker_compose v1 role (migrate to docker_compose_v2)
- Removed dependabot configuration (replaced by Renovate)
- Removed pre-commit configuration
- Removed separate linter workflow (integrated into ci.yml)
- Removed RHEL 7 support from Docker role

### Fixed

- Fixed all YAML linting issues (document-start, comments-indentation, line-length)
- Fixed all ansible-lint violations (FQCN, schema, task-key-order)
- Fixed ansible-test sanity errors (shebangs, empty-init)
- Fixed platform schema validation for Ansible Galaxy
- Fixed Jinja2 template shebangs to avoid sanity errors
- Fixed license header consistency (MIT throughout)

## [0.0.7] - 2024-02-16

### Added

- Added meta documentation

## [0.0.6] - 2024-02-16

### Fixed

- Fixed docker-compose v2 scale functionality

### Changed

- Updated super-linter from version 5 to 6

## [0.0.5] - 2024-02-12

### Added

- Added docker_compose_v2 role for Docker Compose v2 support

## [0.0.4] - 2023-11-29

### Added

- Initial collection structure with docker role
- Added docker_compose role
- Added docker_login role
- Added k3s role
- Added fleet role
- Added helm role
- Added tailscale role

## [0.0.3] - 2023-11-29

### Changed

- Collection metadata improvements

## [0.0.2] - 2023-11-18

### Changed

- Role refinements and bug fixes

## [0.0.1] - 2023-11-12

### Added

- Initial release of arillso.container collection
- Basic collection structure
- Initial CI/CD workflows
