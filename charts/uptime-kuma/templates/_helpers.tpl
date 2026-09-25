{{- define "uptime-kuma.name" -}}
{{- .Chart.Name | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "uptime-kuma.fullname" -}}
{{- .Release.Name | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "uptime-kuma.labels" -}}
app.kubernetes.io/name: {{ include "uptime-kuma.name" . }}
{{- end -}}
