"""
SageMaker Client for LLM Inference
Handles communication with deployed SageMaker endpoints.
"""
import json
import boto3
from typing import Optional, Dict, Any, List
from botocore.exceptions import ClientError


class SageMakerClient:
    """Client for invoking SageMaker LLM endpoints."""
    
    def __init__(
        self,
        endpoint_name: str,
        region: str = "us-east-1",
        max_retries: int = 3
    ):
        """
        Initialize SageMaker client.
        
        Args:
            endpoint_name: Name of the SageMaker endpoint
            region: AWS region where endpoint is deployed
            max_retries: Maximum number of retry attempts
        """
        self.endpoint_name = endpoint_name
        self.region = region
        self.max_retries = max_retries
        self.runtime_client = boto3.client(
            'sagemaker-runtime',
            region_name=region
        )
    
    def generate(
        self,
        prompt: str,
        max_tokens: int = 1024,
        temperature: float = 0.7,
        top_p: float = 0.9,
        stop_sequences: Optional[List[str]] = None
    ) -> str:
        """
        Generate text from the SageMaker endpoint.
        
        Args:
            prompt: Input text prompt
            max_tokens: Maximum number of tokens to generate
            temperature: Sampling temperature (0.0 to 1.0)
            top_p: Nucleus sampling parameter
            stop_sequences: List of sequences that stop generation
            
        Returns:
            Generated text response
        """
        # Prepare payload for Hugging Face Text Generation Inference format
        payload = {
            "inputs": prompt,
            "parameters": {
                "max_new_tokens": max_tokens,
                "temperature": temperature,
                "top_p": top_p,
                "do_sample": temperature > 0,
                "return_full_text": False
            }
        }
        
        if stop_sequences:
            payload["parameters"]["stop"] = stop_sequences
        
        try:
            response = self.runtime_client.invoke_endpoint(
                EndpointName=self.endpoint_name,
                ContentType="application/json",
                Body=json.dumps(payload)
            )
            
            # Parse response
            result = json.loads(response['Body'].read().decode())
            
            # Handle different response formats
            if isinstance(result, list) and len(result) > 0:
                return result[0].get("generated_text", "")
            elif isinstance(result, dict):
                return result.get("generated_text", "")
            else:
                return str(result)
                
        except ClientError as e:
            error_code = e.response['Error']['Code']
            error_msg = e.response['Error']['Message']
            raise RuntimeError(
                f"SageMaker endpoint error ({error_code}): {error_msg}"
            )
    
    def chat(
        self,
        messages: List[Dict[str, str]],
        max_tokens: int = 1024,
        temperature: float = 0.7
    ) -> str:
        """
        Chat completion using conversation format.
        
        Args:
            messages: List of message dicts with 'role' and 'content'
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature
            
        Returns:
            Assistant's response text
        """
        # Convert messages to prompt format for instruct models
        prompt = self._format_chat_prompt(messages)
        return self.generate(
            prompt=prompt,
            max_tokens=max_tokens,
            temperature=temperature
        )
    
    def _format_chat_prompt(self, messages: List[Dict[str, str]]) -> str:
        """
        Format chat messages into a prompt for instruct models.
        
        Supports multiple formats:
        - Llama 2: [INST] {prompt} [/INST]
        - Mistral: <s>[INST] {prompt} [/INST]
        - Generic: System: {system}\nUser: {user}\nAssistant:
        """
        # Try to detect model type from endpoint name
        endpoint_lower = self.endpoint_name.lower()
        
        if "llama" in endpoint_lower:
            return self._format_llama_prompt(messages)
        elif "mistral" in endpoint_lower:
            return self._format_mistral_prompt(messages)
        else:
            return self._format_generic_prompt(messages)
    
    def _format_llama_prompt(self, messages: List[Dict[str, str]]) -> str:
        """Format for Llama 2 chat models."""
        formatted = ""
        system_prompt = None
        
        for msg in messages:
            if msg["role"] == "system":
                system_prompt = msg["content"]
            elif msg["role"] == "user":
                if system_prompt and not formatted:
                    # Include system prompt in first user message
                    formatted += f"[INST] <<SYS>>\n{system_prompt}\n<</SYS>>\n\n{msg['content']} [/INST] "
                    system_prompt = None
                else:
                    formatted += f"[INST] {msg['content']} [/INST] "
            elif msg["role"] == "assistant":
                formatted += f"{msg['content']} "
        
        return formatted.strip()
    
    def _format_mistral_prompt(self, messages: List[Dict[str, str]]) -> str:
        """Format for Mistral instruct models."""
        formatted = "<s>"
        
        for msg in messages:
            if msg["role"] == "system":
                # Mistral doesn't have explicit system role, prepend to first user message
                continue
            elif msg["role"] == "user":
                formatted += f"[INST] {msg['content']} [/INST]"
            elif msg["role"] == "assistant":
                formatted += f" {msg['content']}</s>"
        
        return formatted
    
    def _format_generic_prompt(self, messages: List[Dict[str, str]]) -> str:
        """Generic format for instruct models."""
        formatted = ""
        
        for msg in messages:
            role = msg["role"].capitalize()
            content = msg["content"]
            
            if msg["role"] == "system":
                formatted += f"System: {content}\n\n"
            elif msg["role"] == "user":
                formatted += f"User: {content}\n\n"
            elif msg["role"] == "assistant":
                formatted += f"Assistant: {content}\n\n"
        
        # Add final assistant prompt
        if messages[-1]["role"] != "assistant":
            formatted += "Assistant:"
        
        return formatted.strip()
    
    def health_check(self) -> Dict[str, Any]:
        """
        Check if endpoint is healthy and responsive.
        
        Returns:
            Health status dictionary
        """
        try:
            # Try a simple generation
            response = self.generate(
                prompt="Hello",
                max_tokens=10,
                temperature=0.0
            )
            
            return {
                "status": "healthy",
                "endpoint": self.endpoint_name,
                "region": self.region,
                "test_response": response
            }
        except Exception as e:
            return {
                "status": "unhealthy",
                "endpoint": self.endpoint_name,
                "region": self.region,
                "error": str(e)
            }


def test_sagemaker_client():
    """Test SageMaker client with a deployed endpoint."""
    import os
    
    endpoint_name = os.getenv("SAGEMAKER_ENDPOINT_NAME")
    region = os.getenv("AWS_REGION", "us-east-1")
    
    if not endpoint_name:
        print("Error: SAGEMAKER_ENDPOINT_NAME environment variable not set")
        return
    
    print(f"Testing SageMaker endpoint: {endpoint_name}")
    print(f"Region: {region}")
    print("="*70)
    
    client = SageMakerClient(
        endpoint_name=endpoint_name,
        region=region
    )
    
    # Test 1: Health check
    print("\n[Test 1] Health Check")
    health = client.health_check()
    print(f"Status: {health['status']}")
    if health['status'] == 'healthy':
        print(f"✓ Test response: {health['test_response']}")
    else:
        print(f"✗ Error: {health['error']}")
        return
    
    # Test 2: Simple generation
    print("\n[Test 2] Simple Generation")
    prompt = "What is the capital of France?"
    response = client.generate(prompt, max_tokens=50, temperature=0.0)
    print(f"Prompt: {prompt}")
    print(f"Response: {response}")
    
    # Test 3: Chat format
    print("\n[Test 3] Chat Format")
    messages = [
        {"role": "system", "content": "You are a helpful career coach."},
        {"role": "user", "content": "What are the top 3 skills for a software engineer?"}
    ]
    response = client.chat(messages, max_tokens=200, temperature=0.7)
    print(f"Chat response: {response}")
    
    print("\n" + "="*70)
    print("✅ All tests completed")


if __name__ == "__main__":
    test_sagemaker_client()
