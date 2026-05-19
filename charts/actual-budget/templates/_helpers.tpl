{{- define "actual-budget.name" -}}
{{- .Chart.Name | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "actual-budget.fullname" -}}
{{- .Release.Name | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "actual-budget.labels" -}}
app.kubernetes.io/name: {{ include "actual-budget.name" . }}
{{- end -}}
