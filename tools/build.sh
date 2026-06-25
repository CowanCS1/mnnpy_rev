#!/usr/bin/env bash
# Build mnnpy_rev into a wheel using a dedicated build env (compilers + Cython).
# Installing the wheel into a consuming env (e.g. sc_make_atlas) is a SEPARATE
# step -- this script only produces dist/mnnpy_rev-*.whl.
#
#   bash tools/build.sh
#
# Requires `mamba` or `conda` on PATH. The build env is provisioned from
# env/build_environment.yml; the runtime/consumer env never needs build tooling.

set -euo pipefail
REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BUILD_ENV="mnnpy_build"
CONDA="$(command -v mamba || command -v conda || true)"
[[ -n "${CONDA}" ]] || { echo "[build] need mamba or conda on PATH" >&2; exit 1; }

# 1. Provision the build env (compilers + Cython) reproducibly.
if "${CONDA}" env list | grep -qE "^[[:space:]]*${BUILD_ENV}[[:space:]]"; then
    "${CONDA}" env update -n "${BUILD_ENV}" -f "${REPO}/env/build_environment.yml" --prune
else
    "${CONDA}" env create -f "${REPO}/env/build_environment.yml"
fi

# 2. Build the wheel with the build env's toolchain (no build isolation, so it
#    uses that env's Cython + gcc). Force a fresh Cython regen of the extension.
rm -f "${REPO}/mnnpy/_utils.c"
rm -rf "${REPO}/dist" "${REPO}/build"
"${CONDA}" run -n "${BUILD_ENV}" python -m pip wheel "${REPO}" \
    --no-build-isolation --no-deps -w "${REPO}/dist"

echo "[build] built: $(ls "${REPO}"/dist/*.whl)"
