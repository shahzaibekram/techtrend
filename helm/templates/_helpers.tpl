# helm/techtrends/templates/_helpers.tpl

{{- define "techtrends.fullname" -}}
{{- printf "%s-%s" .Release.Name .Chart.Name -}}
{{- end -}}
