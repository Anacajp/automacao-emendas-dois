# Arquivo de configuração para deploy no Google Cloud

## 📋 Pré-requisitos

1. **Instalar Google Cloud CLI**

   ```bash
   # Baixar de: https://cloud.google.com/sdk/docs/install
   ```

2. **Fazer login no Google Cloud**

   ```bash
   gcloud auth login
   gcloud config set project SEU_PROJECT_ID
   ```

3. **Habilitar APIs necessárias**
   ```bash
   gcloud services enable cloudbuild.googleapis.com
   gcloud services enable run.googleapis.com
   gcloud services enable cloudscheduler.googleapis.com
   gcloud services enable sheets.googleapis.com
   ```

## 🚀 Deploy Passo a Passo

### 1. Definir variáveis

```bash
export PROJECT_ID="seu-project-id"
export REGION="us-central1"
export SERVICE_NAME="emendas-automation"
export GOOGLE_SHEET_ID="seu-google-sheet-id"
```

### 2. Build e Deploy

```bash
gcloud builds submit \
  --config cloudbuild.yaml \
  --substitutions _GOOGLE_SHEET_ID=$GOOGLE_SHEET_ID,_SERVICE_ACCOUNT_EMAIL=planilha-bot@emendas-gabinete-leo.iam.gserviceaccount.com
```

### 3. Criar agendamento (executar todo dia às 9h)

```bash
gcloud scheduler jobs create http emendas-daily \
  --schedule="0 9 * * *" \
  --uri="https://emendas-automation-HASH-uc.a.run.app" \
  --http-method=POST \
  --location=$REGION \
  --description="Execução diária da automação de emendas"
```

### 4. Criar agendamento (executar toda segunda às 8h)

```bash
gcloud scheduler jobs create http emendas-weekly \
  --schedule="0 8 * * 1" \
  --uri="https://emendas-automation-HASH-uc.a.run.app" \
  --http-method=POST \
  --location=$REGION \
  --description="Execução semanal da automação de emendas"
```

## 🔧 Comandos Úteis

### Ver logs da aplicação

```bash
gcloud logging read "resource.type=cloud_run_revision AND resource.labels.service_name=emendas-automation" --limit=50 --format="table(timestamp,textPayload)"
```

### Atualizar apenas o código (sem rebuild completo)

```bash
gcloud builds submit --config cloudbuild.yaml
```

### Ver status do Cloud Run

```bash
gcloud run services describe emendas-automation --region=$REGION
```

### Executar manualmente (para teste)

```bash
gcloud run services proxy emendas-automation --port=8080 --region=$REGION
curl -X POST http://localhost:8080
```

## 🛡️ Segurança

- O service account já está configurado no projeto
- As credenciais são injetadas automaticamente no container
- O Cloud Run roda isolado e seguro
- Logs ficam no Cloud Logging para auditoria

## 💰 Custos Estimados

- **Cloud Run**: ~$0.24/mês (100 execuções)
- **Cloud Scheduler**: Grátis (até 3 jobs)
- **Cloud Storage**: ~$0.02/mês (logs)

**Total estimado: < $1/mês** 🎉
