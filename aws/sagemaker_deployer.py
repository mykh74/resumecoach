"""
SageMaker Model Deployment Script
Deploys open-source LLM models (Llama 2, Mistral) to AWS SageMaker endpoints.
"""
import os
import json
import boto3
import time
from typing import Optional, Dict, Any
from botocore.exceptions import ClientError


class SageMakerDeployer:
    """Handles deployment of LLM models to AWS SageMaker."""
    
    # Supported models with their configurations
    SUPPORTED_MODELS = {
        "llama-2-7b-chat": {
            "model_id": "meta-textgeneration-llama-2-7b-f",
            "instance_type": "ml.g5.2xlarge",  # GPU instance
            "instance_count": 1,
            "description": "Llama 2 7B Chat - Fast, cost-effective"
        },
        "llama-2-13b-chat": {
            "model_id": "meta-textgeneration-llama-2-13b-f",
            "instance_type": "ml.g5.4xlarge",  # Larger GPU
            "instance_count": 1,
            "description": "Llama 2 13B Chat - Better quality"
        },
        "mistral-7b-instruct": {
            "model_id": "mistralai-mistral-7b-instruct-v0-2",
            "instance_type": "ml.g5.2xlarge",
            "instance_count": 1,
            "description": "Mistral 7B Instruct - Excellent performance"
        },
        "falcon-7b-instruct": {
            "model_id": "huggingface-llm-falcon-7b-instruct-bf16",
            "instance_type": "ml.g5.2xlarge",
            "instance_count": 1,
            "description": "Falcon 7B Instruct - Open source alternative"
        }
    }
    
    def __init__(self, region: str = "us-east-1"):
        """
        Initialize SageMaker deployer.
        
        Args:
            region: AWS region for deployment
        """
        self.region = region
        self.sagemaker_client = boto3.client('sagemaker', region_name=region)
        self.iam_client = boto3.client('iam', region_name=region)
        self.account_id = boto3.client('sts').get_caller_identity()['Account']
        
    def create_sagemaker_role(self, role_name: str = "ResumeCoachSageMakerRole") -> str:
        """
        Create IAM role for SageMaker with necessary permissions.
        
        Args:
            role_name: Name for the IAM role
            
        Returns:
            ARN of the created or existing role
        """
        trust_policy = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Principal": {"Service": "sagemaker.amazonaws.com"},
                    "Action": "sts:AssumeRole"
                }
            ]
        }
        
        try:
            # Try to get existing role
            response = self.iam_client.get_role(RoleName=role_name)
            role_arn = response['Role']['Arn']
            print(f"✓ Using existing IAM role: {role_arn}")
            return role_arn
            
        except ClientError as e:
            if e.response['Error']['Code'] == 'NoSuchEntity':
                # Create new role
                print(f"Creating IAM role: {role_name}...")
                response = self.iam_client.create_role(
                    RoleName=role_name,
                    AssumeRolePolicyDocument=json.dumps(trust_policy),
                    Description="Role for ResumeCoach SageMaker endpoints"
                )
                role_arn = response['Role']['Arn']
                
                # Attach required policies
                policies = [
                    "arn:aws:iam::aws:policy/AmazonSageMakerFullAccess",
                    "arn:aws:iam::aws:policy/AmazonS3FullAccess"
                ]
                
                for policy_arn in policies:
                    self.iam_client.attach_role_policy(
                        RoleName=role_name,
                        PolicyArn=policy_arn
                    )
                
                print(f"✓ Created IAM role: {role_arn}")
                print("  Waiting 10 seconds for IAM propagation...")
                time.sleep(10)  # Wait for IAM propagation
                
                return role_arn
            else:
                raise
    
    def deploy_model(
        self,
        model_name: str,
        endpoint_name: Optional[str] = None,
        instance_type: Optional[str] = None,
        wait: bool = True
    ) -> Dict[str, Any]:
        """
        Deploy a model to SageMaker endpoint.
        
        Args:
            model_name: Name of the model from SUPPORTED_MODELS
            endpoint_name: Custom endpoint name (default: resumecoach-{model_name})
            instance_type: Override default instance type
            wait: Whether to wait for deployment to complete
            
        Returns:
            Dictionary with deployment information
        """
        if model_name not in self.SUPPORTED_MODELS:
            raise ValueError(
                f"Unsupported model: {model_name}. "
                f"Supported models: {list(self.SUPPORTED_MODELS.keys())}"
            )
        
        model_config = self.SUPPORTED_MODELS[model_name]
        endpoint_name = endpoint_name or f"resumecoach-{model_name}"
        instance_type = instance_type or model_config["instance_type"]
        
        print(f"\n{'='*70}")
        print(f"Deploying {model_name} to SageMaker")
        print(f"{'='*70}")
        print(f"Model ID: {model_config['model_id']}")
        print(f"Instance Type: {instance_type}")
        print(f"Endpoint Name: {endpoint_name}")
        print(f"Region: {self.region}")
        print(f"{'='*70}\n")
        
        # Step 1: Create IAM role
        role_arn = self.create_sagemaker_role()
        
        # Step 2: Create SageMaker model from JumpStart
        sm_model_name = f"{endpoint_name}-model"
        print(f"\n[1/4] Creating SageMaker model: {sm_model_name}")
        
        try:
            model_response = self.sagemaker_client.create_model(
                ModelName=sm_model_name,
                PrimaryContainer={
                    "Image": self._get_jumpstart_image_uri(model_config["model_id"]),
                    "ModelDataUrl": self._get_jumpstart_model_uri(model_config["model_id"]),
                    "Environment": {
                        "SAGEMAKER_PROGRAM": "inference.py",
                        "SAGEMAKER_SUBMIT_DIRECTORY": "/opt/ml/model/code",
                        "SAGEMAKER_CONTAINER_LOG_LEVEL": "20",
                        "SAGEMAKER_MODEL_SERVER_TIMEOUT": "3600"
                    }
                },
                ExecutionRoleArn=role_arn
            )
            print(f"✓ Model created: {model_response['ModelArn']}")
        except ClientError as e:
            if e.response['Error']['Code'] == 'ValidationException':
                print(f"⚠ Model {sm_model_name} already exists, using existing model")
            else:
                raise
        
        # Step 3: Create endpoint configuration
        endpoint_config_name = f"{endpoint_name}-config"
        print(f"\n[2/4] Creating endpoint configuration: {endpoint_config_name}")
        
        try:
            config_response = self.sagemaker_client.create_endpoint_config(
                EndpointConfigName=endpoint_config_name,
                ProductionVariants=[
                    {
                        "VariantName": "AllTraffic",
                        "ModelName": sm_model_name,
                        "InstanceType": instance_type,
                        "InitialInstanceCount": model_config["instance_count"],
                        "InitialVariantWeight": 1.0
                    }
                ]
            )
            print(f"✓ Endpoint config created: {config_response['EndpointConfigArn']}")
        except ClientError as e:
            if e.response['Error']['Code'] == 'ValidationException':
                print(f"⚠ Config {endpoint_config_name} already exists, using existing config")
            else:
                raise
        
        # Step 4: Create endpoint
        print(f"\n[3/4] Creating endpoint: {endpoint_name}")
        print("⏳ This will take 5-10 minutes...")
        
        try:
            endpoint_response = self.sagemaker_client.create_endpoint(
                EndpointName=endpoint_name,
                EndpointConfigName=endpoint_config_name
            )
            print(f"✓ Endpoint creation initiated: {endpoint_response['EndpointArn']}")
        except ClientError as e:
            if e.response['Error']['Code'] == 'ValidationException':
                print(f"⚠ Endpoint {endpoint_name} already exists")
                return self.get_endpoint_status(endpoint_name)
            else:
                raise
        
        # Step 5: Wait for endpoint to be in service
        if wait:
            print(f"\n[4/4] Waiting for endpoint to be in service...")
            status = self._wait_for_endpoint(endpoint_name)
            
            if status == "InService":
                print(f"\n{'='*70}")
                print(f"✅ DEPLOYMENT SUCCESSFUL!")
                print(f"{'='*70}")
                print(f"Endpoint Name: {endpoint_name}")
                print(f"Status: {status}")
                print(f"Region: {self.region}")
                print(f"\nAdd to your .env file:")
                print(f"SAGEMAKER_ENDPOINT_NAME={endpoint_name}")
                print(f"AWS_REGION={self.region}")
                print(f"{'='*70}\n")
            else:
                print(f"\n⚠ Deployment finished with status: {status}")
        
        return {
            "endpoint_name": endpoint_name,
            "model_name": model_name,
            "instance_type": instance_type,
            "region": self.region,
            "status": "Creating" if not wait else status
        }
    
    def get_endpoint_status(self, endpoint_name: str) -> Dict[str, Any]:
        """Get current status of a SageMaker endpoint."""
        try:
            response = self.sagemaker_client.describe_endpoint(
                EndpointName=endpoint_name
            )
            return {
                "endpoint_name": endpoint_name,
                "status": response["EndpointStatus"],
                "creation_time": response.get("CreationTime"),
                "last_modified_time": response.get("LastModifiedTime"),
                "instance_type": response["ProductionVariants"][0]["InstanceType"],
                "current_instance_count": response["ProductionVariants"][0]["CurrentInstanceCount"]
            }
        except ClientError as e:
            if e.response['Error']['Code'] == 'ValidationException':
                return {"endpoint_name": endpoint_name, "status": "NotFound"}
            raise
    
    def delete_endpoint(self, endpoint_name: str, delete_model: bool = True) -> None:
        """
        Delete a SageMaker endpoint and optionally its model and config.
        
        Args:
            endpoint_name: Name of the endpoint to delete
            delete_model: Whether to also delete the model and config
        """
        print(f"Deleting endpoint: {endpoint_name}...")
        
        try:
            # Get endpoint details before deletion
            endpoint = self.sagemaker_client.describe_endpoint(
                EndpointName=endpoint_name
            )
            endpoint_config_name = endpoint["EndpointConfigName"]
            
            # Delete endpoint
            self.sagemaker_client.delete_endpoint(EndpointName=endpoint_name)
            print(f"✓ Endpoint {endpoint_name} deleted")
            
            if delete_model:
                # Get and delete model
                endpoint_config = self.sagemaker_client.describe_endpoint_config(
                    EndpointConfigName=endpoint_config_name
                )
                model_name = endpoint_config["ProductionVariants"][0]["ModelName"]
                
                # Delete endpoint config
                self.sagemaker_client.delete_endpoint_config(
                    EndpointConfigName=endpoint_config_name
                )
                print(f"✓ Endpoint config {endpoint_config_name} deleted")
                
                # Delete model
                self.sagemaker_client.delete_model(ModelName=model_name)
                print(f"✓ Model {model_name} deleted")
            
            print(f"✅ Complete deletion of {endpoint_name}")
            
        except ClientError as e:
            if e.response['Error']['Code'] == 'ValidationException':
                print(f"⚠ Endpoint {endpoint_name} not found")
            else:
                raise
    
    def list_endpoints(self) -> list:
        """List all SageMaker endpoints."""
        response = self.sagemaker_client.list_endpoints(
            SortBy='CreationTime',
            SortOrder='Descending',
            MaxResults=100
        )
        return response.get('Endpoints', [])
    
    def _wait_for_endpoint(self, endpoint_name: str, timeout: int = 900) -> str:
        """Wait for endpoint to reach InService status."""
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            try:
                response = self.sagemaker_client.describe_endpoint(
                    EndpointName=endpoint_name
                )
                status = response["EndpointStatus"]
                
                if status == "InService":
                    return status
                elif status in ["Failed", "OutOfService"]:
                    failure_reason = response.get("FailureReason", "Unknown")
                    print(f"\n❌ Endpoint deployment failed: {failure_reason}")
                    return status
                
                elapsed = int(time.time() - start_time)
                print(f"  Status: {status} (elapsed: {elapsed}s / {timeout}s)", end="\r")
                time.sleep(30)  # Check every 30 seconds
                
            except ClientError:
                time.sleep(30)
                continue
        
        print(f"\n⚠ Timeout waiting for endpoint after {timeout}s")
        return "Timeout"
    
    def _get_jumpstart_image_uri(self, model_id: str) -> str:
        """Get the Docker image URI for a JumpStart model."""
        # This is a simplified version - in production, use sagemaker.image_uris.retrieve()
        region_mapping = {
            "us-east-1": "763104351884",
            "us-east-2": "763104351884",
            "us-west-1": "763104351884",
            "us-west-2": "763104351884",
            "eu-west-1": "763104351884",
            "eu-central-1": "763104351884",
            "ap-northeast-1": "763104351884",
        }
        
        account = region_mapping.get(self.region, "763104351884")
        return f"{account}.dkr.ecr.{self.region}.amazonaws.com/huggingface-pytorch-tgi-inference:2.1.1-tgi1.4.0-gpu-py310-cu121-ubuntu20.04"
    
    def _get_jumpstart_model_uri(self, model_id: str) -> str:
        """Get the S3 URI for a JumpStart model."""
        # Simplified version - actual URIs are in SageMaker JumpStart registry
        return f"s3://jumpstart-cache-prod-{self.region}/huggingface-infer/{model_id}/"


def main():
    """CLI interface for SageMaker deployment."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Deploy LLM models to AWS SageMaker"
    )
    parser.add_argument(
        "action",
        choices=["deploy", "list", "status", "delete"],
        help="Action to perform"
    )
    parser.add_argument(
        "--model",
        choices=list(SageMakerDeployer.SUPPORTED_MODELS.keys()),
        help="Model to deploy"
    )
    parser.add_argument(
        "--endpoint",
        help="Endpoint name (for status/delete actions)"
    )
    parser.add_argument(
        "--region",
        default=os.getenv("AWS_REGION", "us-east-1"),
        help="AWS region (default: from AWS_REGION env or us-east-1)"
    )
    parser.add_argument(
        "--instance-type",
        help="Override default instance type"
    )
    parser.add_argument(
        "--no-wait",
        action="store_true",
        help="Don't wait for deployment to complete"
    )
    
    args = parser.parse_args()
    
    deployer = SageMakerDeployer(region=args.region)
    
    if args.action == "deploy":
        if not args.model:
            print("Error: --model required for deploy action")
            print("\nSupported models:")
            for model, config in SageMakerDeployer.SUPPORTED_MODELS.items():
                print(f"  • {model}: {config['description']}")
            return
        
        result = deployer.deploy_model(
            model_name=args.model,
            instance_type=args.instance_type,
            wait=not args.no_wait
        )
        print(json.dumps(result, indent=2, default=str))
    
    elif args.action == "list":
        endpoints = deployer.list_endpoints()
        print(f"\nSageMaker Endpoints in {args.region}:")
        print(f"{'='*70}")
        for ep in endpoints:
            print(f"  • {ep['EndpointName']}: {ep['EndpointStatus']}")
        print(f"\nTotal: {len(endpoints)} endpoint(s)")
    
    elif args.action == "status":
        if not args.endpoint:
            print("Error: --endpoint required for status action")
            return
        
        status = deployer.get_endpoint_status(args.endpoint)
        print(json.dumps(status, indent=2, default=str))
    
    elif args.action == "delete":
        if not args.endpoint:
            print("Error: --endpoint required for delete action")
            return
        
        deployer.delete_endpoint(args.endpoint)


if __name__ == "__main__":
    main()
