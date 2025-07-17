# 🚀 Guia de Deploy - Automação de Emendas

## ✅ O que você já tem pronto:
- ✅ Código funcionando 100%
- ✅ Dockerfile configurado
- ✅ Arquivos de deploy prontos
- ✅ Service account do Google configurado

## 🎯 Próximos Passos:

### 1. Preparar o ambiente (uma vez só)

**Instalar Google Cloud CLI:**
- Windows: https://cloud.google.com/sdk/docs/install-windows
- Ou pelo PowerShell: `(New-Object Net.WebClient).DownloadFile("https://dl.google.com/dl/cloudsdk/channels/rapid/GoogleCloudSDKInstaller.exe", "$env:Temp\GoogleCloudSDKInstaller.exe") & $env:Temp\GoogleCloudSDKInstaller.exe`

**Fazer login:**
```powershell
gcloud auth login
gcloud config set project emendas-gabinete-leo  # ou seu project ID
```

**Habilitar APIs:**
```powershell
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com  
gcloud services enable cloudscheduler.googleapis.com
```

### 2. Deploy inicial (primeira vez)

**No PowerShell, na pasta do projeto:**
```powershell
# Definir suas variáveis
$PROJECT_ID = "emendas-gabinete-leo"  # Substitua pelo seu
$GOOGLE_SHEET_ID = "1abc123..."       # Substitua pelo ID da sua planilha

# Fazer o build e deploy com variáveis de ambiente
gcloud builds submit --tag gcr.io/emendas-gabinete-leo/automacao-emendas

# Deploy com configuração de variáveis
gcloud run deploy automacao-emendas `
  --image gcr.io/emendas-gabinete-leo/automacao-emendas `
  --platform managed `
  --region us-central1 `
  --no-allow-unauthenticated `
  --memory 2Gi `
  --cpu 1 `
  --timeout 3600 `
  --min-instances 0 `
  --max-instances 1 `
  --set-env-vars GOOGLE_SHEET_ID=1P29SRgMtLLg7IcRbVeS3sAc_4NRgDW5u2k1eqCq-w7c
```

### 3. Configurar agendamento

**Para executar TODO DIA às 9h da manhã:**
```powershell
gcloud scheduler jobs create http emendas-daily --schedule="0 9 * * *" --uri="https://emendas-automation-HASH-uc.a.run.app" --http-method=POST --location=us-central1 --description="Execução diária da automação de emendas"
```

**OU para executar TODA SEGUNDA às 8h:**
```powershell
gcloud scheduler jobs create http emendas-weekly --schedule="0 8 * * 1" --uri="https://emendas-automation-HASH-uc.a.run.app" --http-method=POST --location=us-central1 --description="Execução semanal da automação de emendas"
```

> ⚠️ **Importante:** Após o deploy, o gcloud vai te dar a URL real. Substitua "HASH" pela URL verdadeira.

### 4. Testar se funcionou

**Ver logs em tempo real:**
```powershell
gcloud logging read "resource.type=cloud_run_revision AND resource.labels.service_name=emendas-automation" --limit=10 --format="table(timestamp,textPayload)"
```

**Executar manualmente (teste):**
```powershell
# Pegar a URL do serviço
gcloud run services describe emendas-automation --region=us-central1 --format="value(status.url)"

# Executar (substitua pela URL real)
curl -X POST https://sua-url-aqui.a.run.app
```

## 🎉 Resultado Final:

- ✅ Seu código rodando na nuvem
- ✅ Execução automática (diária ou semanal)
- ✅ Independente de qualquer computador
- ✅ Logs para acompanhar execuções
- ✅ Custo < $1/mês

## 📞 Em caso de dúvida:

1. **Ver status do serviço:**
   ```powershell
   gcloud run services list
   ```

2. **Ver agendamentos:**
   ```powershell
   gcloud scheduler jobs list --location=us-central1
   ```

3. **Atualizar código (quando fizer mudanças):**
   ```powershell
   gcloud builds submit --config cloudbuild.yaml
   ```

## 🛡️ Segurança:
- Suas credenciais ficam seguras no Google Cloud
- Ninguém mais precisa ter acesso ao seu computador
- Logs ficam armazenados para auditoria
- Service account com permissões mínimas necessárias
