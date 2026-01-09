#!/usr/bin/env python3
"""
Quick deployment script for AWS SageMaker
Automates the deployment of LLM models to SageMaker endpoints.
"""

import os
import sys
import argparse
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from aws.sagemaker_deployer import SageMakerDeployer


def print_banner(text: str):
    """Print a banner with text."""
    print("\n" + "=" * 70)
    print(f"  {text}")
    print("=" * 70 + "\n")


def main():
    """Main deployment orchestrator."""
    parser = argparse.ArgumentParser(
        description="Deploy ResumeCoach to AWS SageMaker",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Deploy Mistral 7B (recommended for cost/performance balance)
  python deploy_sagemaker.py --model mistral-7b-instruct

  # Deploy Llama 2 7B (good alternative)
  python deploy_sagemaker.py --model llama-2-7b-chat

  # List available models
  python deploy_sagemaker.py --list-models

  # Check endpoint status
  python deploy_sagemaker.py --check-status resumecoach-mistral-7b-instruct

  # Delete endpoint
  python deploy_sagemaker.py --delete resumecoach-mistral-7b-instruct
        """
    )
    
    parser.add_argument(
        "--model",
        choices=list(SageMakerDeployer.SUPPORTED_MODELS.keys()),
        help="Model to deploy"
    )
    parser.add_argument(
        "--region",
        default=os.getenv("AWS_REGION", "us-east-1"),
        help="AWS region (default: AWS_REGION env or us-east-1)"
    )
    parser.add_argument(
        "--endpoint-name",
        help="Custom endpoint name (default: resumecoach-{model})"
    )
    parser.add_argument(
        "--list-models",
        action="store_true",
        help="List supported models"
    )
    parser.add_argument(
        "--check-status",
        metavar="ENDPOINT",
        help="Check status of an endpoint"
    )
    parser.add_argument(
        "--delete",
        metavar="ENDPOINT",
        help="Delete an endpoint"
    )
    parser.add_argument(
        "--list-endpoints",
        action="store_true",
        help="List all SageMaker endpoints"
    )
    
    args = parser.parse_args()
    
    # Handle list models
    if args.list_models:
        print_banner("Supported Models for ResumeCoach")
        for model_name, config in SageMakerDeployer.SUPPORTED_MODELS.items():
            print(f"🤖 {model_name}")
            print(f"   Description: {config['description']}")
            print(f"   Instance: {config['instance_type']}")
            print(f"   Est. Cost: ~$0.07-0.12/hour\n")
        return
    
    deployer = SageMakerDeployer(region=args.region)
    
    # Handle list endpoints
    if args.list_endpoints:
        print_banner(f"SageMaker Endpoints in {args.region}")
        endpoints = deployer.list_endpoints()
        if endpoints:
            for ep in endpoints:
                status_emoji = "✅" if ep["EndpointStatus"] == "InService" else "⏳"
                print(f"{status_emoji} {ep['EndpointName']}: {ep['EndpointStatus']}")
        else:
            print("No endpoints found")
        return
    
    # Handle check status
    if args.check_status:
        print_banner(f"Endpoint Status: {args.check_status}")
        status = deployer.get_endpoint_status(args.check_status)
        if status.get("status") == "NotFound":
            print(f"❌ Endpoint not found: {args.check_status}")
        else:
            print(f"Status: {status['status']}")
            print(f"Instance Type: {status.get('instance_type', 'N/A')}")
            print(f"Instance Count: {status.get('current_instance_count', 'N/A')}")
            print(f"Created: {status.get('creation_time', 'N/A')}")
        return
    
    # Handle delete
    if args.delete:
        print_banner(f"Deleting Endpoint: {args.delete}")
        response = input(f"⚠️  Are you sure you want to delete '{args.delete}'? (yes/no): ")
        if response.lower() == "yes":
            deployer.delete_endpoint(args.delete, delete_model=True)
        else:
            print("Deletion cancelled")
        return
    
    # Deploy model
    if not args.model:
        parser.print_help()
        print("\n❌ Error: --model required for deployment")
        print("\nRun with --list-models to see available models")
        return
    
    print_banner("ResumeCoach SageMaker Deployment")
    print(f"Model: {args.model}")
    print(f"Region: {args.region}")
    
    # Check AWS credentials
    if not os.getenv("AWS_ACCESS_KEY_ID"):
        print("❌ AWS credentials not configured")
        print("\nPlease set the following environment variables:")
        print("  - AWS_ACCESS_KEY_ID")
        print("  - AWS_SECRET_ACCESS_KEY")
        print("  - AWS_REGION (optional, default: us-east-1)")
        print("\nSee docs/AWS_SETUP_GUIDE.md for instructions")
        return
    
    # Confirm deployment
    print("\n⚠️  WARNING: This will create AWS resources that incur costs")
    model_config = SageMakerDeployer.SUPPORTED_MODELS[args.model]
    print(f"Instance Type: {model_config['instance_type']}")
    print(f"Estimated Cost: ~$0.07-0.12 per hour (~$50-90/month if running 24/7)")
    print("\n💡 TIP: You can delete the endpoint anytime to stop charges")
    
    response = input("\nProceed with deployment? (yes/no): ")
    if response.lower() != "yes":
        print("Deployment cancelled")
        return
    
    # Deploy
    print_banner("Starting Deployment")
    result = deployer.deploy_model(
        model_name=args.model,
        endpoint_name=args.endpoint_name,
        wait=True
    )
    
    if result.get("status") == "InService":
        print_banner("✅ DEPLOYMENT SUCCESSFUL")
        print("Next steps:")
        print(f"\n1. Add to your .env file:")
        print(f"   SAGEMAKER_ENDPOINT_NAME={result['endpoint_name']}")
        print(f"   AWS_REGION={result['region']}")
        print(f"\n2. Test the endpoint:")
        print(f"   python aws/sagemaker_client.py")
        print(f"\n3. Update your application to use SageMaker:")
        print(f"   # In your code:")
        print(f"   llm_service = LLMService(provider='sagemaker')")
        print(f"\n4. Run comparison tests:")
        print(f"   python scripts/compare_providers.py")
    else:
        print(f"\n⚠️  Deployment finished with status: {result.get('status')}")
        print("Check AWS Console for details")


if __name__ == "__main__":
    main()
