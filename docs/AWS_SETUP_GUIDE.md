# AWS SageMaker Setup Guide

## Prerequisites

Before deploying to AWS SageMaker, you need:
1. AWS Account (Free Tier available)
2. AWS IAM credentials with SageMaker permissions
3. Basic understanding of AWS costs (SageMaker charges for compute)

---

## Step 1: AWS Account Setup

### Create AWS Account (if you don't have one)
1. Go to https://aws.amazon.com/
2. Click "Create an AWS Account"
3. Follow the registration process
4. Add payment method (required even for Free Tier)
5. Verify your identity

**Free Tier Benefits:**
- 250 hours/month of SageMaker notebook instances (first 2 months)
- 50 hours/month of training and inference (first 2 months)
- After Free Tier: Pay-as-you-go pricing

---

## Step 2: Create IAM User for SageMaker

### 2.1 Navigate to IAM
1. Log in to AWS Console: https://console.aws.amazon.com/
2. Search for "IAM" in the top search bar
3. Click "IAM" to open Identity and Access Management

### 2.2 Create New IAM User
1. Click **"Users"** in left sidebar
2. Click **"Create user"** button
3. **User name:** `resumecoach-sagemaker`
4. Click **"Next"**

### 2.3 Set Permissions
1. Select **"Attach policies directly"**
2. Search and check these policies:
   - ✅ `AmazonSageMakerFullAccess`
   - ✅ `AmazonS3FullAccess`
   - ✅ `IAMReadOnlyAccess`
3. Click **"Next"**
4. Review and click **"Create user"**

### 2.4 Create Access Keys
1. Click on the newly created user name
2. Go to **"Security credentials"** tab
3. Scroll to **"Access keys"** section
4. Click **"Create access key"**
5. Select **"Application running outside AWS"**
6. Click **"Next"**
7. Optional: Add description tag
8. Click **"Create access key"**

### 2.5 Save Your Credentials
⚠️ **CRITICAL:** Copy and save these immediately:
```
Access Key ID: AKIA...
Secret Access Key: wJalrXUt...
```

**You won't be able to see the Secret Access Key again!**

---

## Step 3: Choose AWS Region

### Recommended Regions for SageMaker

| Region | Region Code | Benefits |
|--------|-------------|----------|
| US East (N. Virginia) | `us-east-1` | ✅ Recommended - Most services, lowest prices |
| US West (Oregon) | `us-west-2` | Good alternative, many services |
| Europe (Ireland) | `eu-west-1` | Best for EU users |
| Asia Pacific (Tokyo) | `ap-northeast-1` | Best for Asia users |

**How to choose:**
- Use `us-east-1` if unsure (default for most tutorials)
- Choose region closest to your users for lower latency
- Check pricing: https://aws.amazon.com/sagemaker/pricing/

---

## Step 4: Configure Your Application

### 4.1 Update .env File

Edit your `/Users/michaelkuzmyn/projects/ik/ResumeCoach/.env` file:

```bash
# AWS Configuration
AWS_ACCESS_KEY_ID=AKIA...                    # Your Access Key ID
AWS_SECRET_ACCESS_KEY=wJalrXUt...            # Your Secret Access Key
AWS_REGION=us-east-1                          # Your chosen region
SAGEMAKER_ENDPOINT_NAME=resumecoach-llm-endpoint  # We'll create this
```

### 4.2 Verify AWS CLI (Optional but Recommended)

Test your credentials work:

```bash
# Install AWS CLI if not installed
pip install awscli

# Configure AWS CLI
aws configure
# Enter your Access Key ID
# Enter your Secret Access Key
# Enter your default region (e.g., us-east-1)
# Enter output format: json

# Test connection
aws sts get-caller-identity
```

Expected output:
```json
{
    "UserId": "AIDA...",
    "Account": "123456789012",
    "Arn": "arn:aws:iam::123456789012:user/resumecoach-sagemaker"
}
```

---

## Step 5: Understand SageMaker Costs

### Pricing Overview (as of 2026)

**SageMaker Hosting (Inference):**
- `ml.t2.medium`: ~$0.065/hour (~$47/month if running 24/7)
- `ml.t3.medium`: ~$0.083/hour (~$60/month if running 24/7)
- `ml.m5.large`: ~$0.192/hour (~$140/month if running 24/7)

**Cost Saving Tips:**
1. **Use smaller instances** for testing (ml.t2.medium)
2. **Stop instances** when not in use
3. **Auto-scaling** to scale to zero during low usage
4. **Monitor usage** with AWS Cost Explorer

**For Development:**
- Recommended: Keep using OpenAI API during development ($0.002 per 1K tokens)
- Deploy to SageMaker only for production or cost optimization

---

## Step 6: Alternative - OpenAI vs SageMaker

### When to Use OpenAI (Current Setup)
✅ **Pros:**
- Already working and tested
- No infrastructure management
- Pay-per-use (no minimum cost)
- Latest models (GPT-4, GPT-3.5-turbo)
- Easier to get started

❌ **Cons:**
- Can be expensive at scale
- Data sent to external service
- Dependent on OpenAI availability

### When to Use SageMaker
✅ **Pros:**
- Better for high volume (>100K requests/day)
- Full data control (stays in your AWS account)
- Can use open-source models (Llama 2, Mistral, etc.)
- Cost predictable with reserved capacity

❌ **Cons:**
- Higher complexity
- Fixed costs even when idle
- Requires DevOps knowledge
- Model quality may be lower than GPT-4

---

## Step 7: Decision Point

### Option A: Continue with OpenAI (Recommended for MVP)
**Current Cost:** ~$0.002 per analysis (very low)

**Recommendation:** Keep using OpenAI for:
- Development and testing
- MVP launch
- Until you reach 10,000+ users

**No additional AWS setup needed!**

### Option B: Deploy to SageMaker (For Production/Scale)
**Proceed if:**
- You have high volume of requests expected
- You need data privacy (no external APIs)
- You want to use open-source models
- You have AWS credits or budget

**Required:**
- Complete AWS credential setup above
- Budget for ~$50-150/month for SageMaker endpoints
- Time for deployment and testing

---

## Quick Setup Checklist

### If Choosing OpenAI (Current):
- ✅ OpenAI API key configured (already done)
- ✅ Application tested and working (done)
- ✅ No additional setup needed
- ⏭️ Skip to Days 11-12 (Integration & Testing)

### If Choosing SageMaker:
- [ ] AWS Account created
- [ ] IAM user created with SageMaker permissions
- [ ] Access Key ID obtained
- [ ] Secret Access Key obtained
- [ ] Region selected
- [ ] Credentials added to .env file
- [ ] AWS CLI configured (optional)
- [ ] Budget approved (~$50-150/month)
- ✅ Ready for SageMaker deployment

---

## Next Steps

After completing AWS setup, we'll:
1. Choose an open-source LLM model (Llama 2, Mistral, etc.)
2. Deploy the model to SageMaker endpoint
3. Update LLMService to support SageMaker
4. Test the integration
5. Compare performance and costs

**Let me know which path you'd like to take!**

---

## Security Best Practices

⚠️ **Important Security Notes:**

1. **Never commit AWS credentials to git:**
   - `.env` is in `.gitignore` (already configured)
   - Never share credentials in chat or email

2. **Use least privilege:**
   - Only grant necessary permissions
   - Create separate IAM users for different purposes

3. **Enable MFA:**
   - Add multi-factor authentication to your AWS account
   - Protects against credential theft

4. **Rotate credentials regularly:**
   - Change access keys every 90 days
   - Delete unused access keys

5. **Monitor usage:**
   - Set up AWS billing alerts
   - Review CloudTrail logs periodically

---

## Support Resources

- **AWS Free Tier:** https://aws.amazon.com/free/
- **SageMaker Documentation:** https://docs.aws.amazon.com/sagemaker/
- **SageMaker Pricing:** https://aws.amazon.com/sagemaker/pricing/
- **AWS Support:** https://console.aws.amazon.com/support/

---

**Ready to proceed? Let me know:**
1. Which option you choose (OpenAI or SageMaker)
2. If SageMaker: Confirm you have AWS credentials configured
