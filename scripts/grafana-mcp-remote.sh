#!/usr/bin/env bash
set -euo pipefail
umask 077

export PATH="${HOME}/.local/share/mise/shims:${HOME}/.local/share/mise/installs/node/latest/bin:/opt/homebrew/bin:/usr/local/bin:${PATH}"
KUBECTL="$(command -v kubectl)"
NPX="$(command -v npx)"
RUNTIME_DIR="$(mktemp -d "${TMPDIR:-/tmp}/grafana-mcp.XXXXXX")"
HEADERS_FILE="${RUNTIME_DIR}/headers"
FORWARD_LOG="${RUNTIME_DIR}/port-forward.log"
PORT_FORWARD_PID=""
BRIDGE_PID=""

cleanup() {
  if [[ -n "${BRIDGE_PID}" ]]; then kill "${BRIDGE_PID}" 2>/dev/null || true; fi
  if [[ -n "${PORT_FORWARD_PID}" ]]; then kill "${PORT_FORWARD_PID}" 2>/dev/null || true; fi
  rm -f "${HEADERS_FILE}" "${FORWARD_LOG}"
  rmdir "${RUNTIME_DIR}" 2>/dev/null || true
}
trap cleanup EXIT
trap 'exit 130' INT
trap 'exit 143' TERM

"${KUBECTL}" --kubeconfig "${HOME}/.kube/config" --context admin@homelab \
  -n monitoring get secret grafana-mcp-server-token -o json |
  python3 -c 'import sys,json,base64; d=json.load(sys.stdin); token=base64.b64decode(d["data"]["token"]).decode(); assert token and "\n" not in token; print("Authorization: Bearer "+token); print("Host: localhost:8000")' > "${HEADERS_FILE}"

LOCAL_PORT="$(python3 -c 'import socket; s=socket.socket(); s.bind(("127.0.0.1",0)); print(s.getsockname()[1]); s.close()')"
"${KUBECTL}" --kubeconfig "${HOME}/.kube/config" --context admin@homelab \
  -n monitoring port-forward --address 127.0.0.1 service/grafana-mcp \
  "${LOCAL_PORT}:8000" > "${FORWARD_LOG}" 2>&1 &
PORT_FORWARD_PID="$!"

for _ in {1..50}; do
  SSE_RESPONSE="$(curl -fsS --header "@${HEADERS_FILE}" --max-time 1 "http://127.0.0.1:${LOCAL_PORT}/sse" 2>/dev/null || true)"
  if [[ "${SSE_RESPONSE}" == *"event: endpoint"* ]]; then
    "${NPX}" -y mcp-remote@0.16.6 "http://127.0.0.1:${LOCAL_PORT}/sse" \
      --allow-http --transport sse-only --header-file "${HEADERS_FILE}" <&0 &
    BRIDGE_PID="$!"
    wait "${BRIDGE_PID}"
    exit $?
  fi
  if ! kill -0 "${PORT_FORWARD_PID}" 2>/dev/null; then
    cat "${FORWARD_LOG}" >&2
    exit 1
  fi
  sleep 0.2
done
cat "${FORWARD_LOG}" >&2
exit 1
