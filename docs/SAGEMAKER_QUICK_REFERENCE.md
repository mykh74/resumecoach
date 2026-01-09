# SageMaker Quick Reference

Quick commands and configurations for AWS SageMaker deployment.

---

## 🚀 Quick Start (5 minutes)

```bash
# 1. Set AWS credentials in .env
AWS_ACCESS_KEY_ID=your_key
AWS_SECRET_ACCESS_KEY=your_secret
AWS_REGION=us-east-1

# 2. Deploy Mistral 7B (recommended)
python deploy_sagemaker.py --model mistral-7b-instruct

# 3. Update .env with endpoint name
SAGEMAKER_ENDPOINT_NAME=resumecoach-mistral-7b-instruct

# 4. Test it
python aws/sagemaker_client.py

# 5. Use in your app
# Set LLM_PROVIDER=sagemaker in .env
```

---

## 📋 Common Commands

### Deployment

```bash
# List available models
python deploy_sagemaker.py --list-models

# Deploy a model
python deploy_sagemaker.py --model mistral-7b-instruct

# Deploy to specific region
python deploy_sagemaker.py --model llama-2-7b-chat --region us-west-2

# Custom endpoint name
python deploy_sagemaker.py --model mistral-7b-instruct --endpoint-name my-endpoint
```

### Management

```bash
# List all endpoints
python deploy_sagemaker.py --list-endpoints

# Check endpoint status
python deploy_sagemaker.py --check-status resumecoach-mistral-7b-instruct

# Delete endpoint (stops billing)
python deploy_sagemaker.py --delete resumecoach-mistral-7b-instruct
```

### Testing

```bash
# Test SageMaker endpoint
python aws/sagemaker_client.py

# Compare OpenAI vs SageMaker
python scripts/compare_providers.py

# Estimate costs for 10K requests/month
python scripts/compare_providers.py --monthly-requests 10000

# Skip SageMaker tests
python scripts/compare_providers.py --skip-sagemaker
```

---

## ⚙️ Configuration

### Environment Variables (.env)

```bash
# Required for SageMaker
AWS_ACCESS_KEY_ID=AKIA...
AWS_SECRET_ACCESS_KEY=wJalrXUt...
AWS_REGION=us-east-1
SAGEMAKER_ENDPOINT_NAME=resumecoach-mistral-7b-instruct

# Optional - Choose provider
LLM_PROVIDER=sagemaker  # or "openai" (default)
```

### Python Code

```python
# Use OpenAI (default)
from backend.services.llm_service import LLMService
llm = LLMService(provider="openai")

# Use SageMaker
llm = LLMService(provider="sagemaker")

# Both have same interface!
report = llm.generate_coaching_report(resume, job, session_id)
```

---

## 🤖 Supported Models

| Model | Best For | Cost/Hour |
|-------|----------|-----------|
| **mistral-7b-instruct** | General use ⭐ | $1.41 |
| **llama-2-7b-chat** | Alternative | $1.41 |
| **llama-2-13b-chat** | Higher quality | $2.82 |
| **falcon-7b-instruct** | Open source | $1.41 |

---

## 💰 Cost Reference

### OpenAI
- **Per request:** ~$0.003
- **1K requests/month:** ~$3
- **10K requests/month:** ~$30
- **100K requests/month:** ~$300

### SageMaker (ml.g5.2xlarge)
- **Per hour:** $1.41
- **Per day (24/7):** $33.84
- **Per month (24/7):** $1,030
- **Break-even:** ~343K requests/month

### Rule of Thumb
- **<100K requests/month:** Use OpenAI
- **>500K requests/month:** Use SageMaker
- **100K-500K:** Depends on usage pattern

---

## 🐛 Quick Troubleshooting

### "Endpoint not found"
```bash
# Check if it exists
python deploy_sagemaker.py --list-endpoints

# Verify endpoint name in .env matches deployed endpoint
```

### "Access Denied"
```bash
# Check AWS credentials
aws sts get-caller-identity

# Verify IAM permissions (need SageMaker full access)
```

### "Slow responses"
- First request after idle may take 30-60s (cold start)
- Subsequent requests should be 2-5s
- Consider keeping endpoint warm with health checks

### "High costs"
```bash
# Delete endpoint when not using
python deploy_sagemaker.py --delete resumecoach-mistral-7b-instruct

# Redeploy when needed (takes 5-10 minutes)
python deploy_sagemaker.py --model mistral-7b-instruct
```

---

## 🔗 Quick Links

- **Full Documentation:** [docs/DAY9-10_SAGEMAKER_DEPLOYMENT.md](DAY9-10_SAGEMAKER_DEPLOYMENT.md)
- **AWS Setup Guide:** [docs/AWS_SETUP_GUIDE.md](AWS_SETUP_GUIDE.md)
- **SageMaker Deployer:** [aws/sagemaker_deployer.py](../aws/sagemaker_deployer.py)
- **SageMaker Client:** [aws/sagemaker_client.py](../aws/sagemaker_client.py)
- **Comparison Tool:** [scripts/compare_providers.py](../scripts/compare_providers.py)

---

## 📞 Support

**Issues?**
1. Check [docs/DAY9-10_SAGEMAKER_DEPLOYMENT.md](DAY9-10_SAGEMAKER_DEPLOYMENT.md) Troubleshooting section
2. Review AWS CloudWatch logs
3. Check SageMaker console for endpoint status

**Cost Concerns?**
1. Delete unused endpoints immediately
2. Use auto-scaling for variable traffic
3. Consider spot instances for dev/test

---

**Last Updated:** January 8, 2026
