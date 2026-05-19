{{- define "n8n-postgres.name" -}}
{{- .Chart.Name | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "n8n-postgres.fullname" -}}
{{- default .Release.Name .Values.fullnameOverride | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "n8n-postgres.labels" -}}
app.kubernetes.io/name: {{ include "n8n-postgres.name" . }}
{{- end -}}
