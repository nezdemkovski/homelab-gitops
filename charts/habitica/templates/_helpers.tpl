{{- define "habitica.name" -}}
{{- .Chart.Name | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "habitica.fullname" -}}
{{- if contains .Chart.Name .Release.Name -}}
{{- .Release.Name | trunc 63 | trimSuffix "-" -}}
{{- else -}}
{{- printf "%s-%s" .Release.Name .Chart.Name | trunc 63 | trimSuffix "-" -}}
{{- end -}}
{{- end -}}

{{- define "habitica.serverLabels" -}}
app.kubernetes.io/name: {{ include "habitica.name" . }}
{{- end -}}

{{- define "habitica.mongoLabels" -}}
app.kubernetes.io/name: {{ include "habitica.mongoServiceName" . }}
{{- end -}}

{{- define "habitica.mongoServiceName" -}}
{{ include "habitica.fullname" . }}-mongo
{{- end -}}

{{- define "habitica.mongoPodHost" -}}
{{ include "habitica.mongoServiceName" . }}-0.{{ include "habitica.mongoServiceName" . }}.{{ .Release.Namespace }}.svc.cluster.local
{{- end -}}

{{- define "habitica.mongoUri" -}}
mongodb://{{ include "habitica.mongoPodHost" . }}:{{ .Values.mongo.service.port }}/habitica?replicaSet={{ .Values.mongo.replicaSetName }}
{{- end -}}
