"""OpenRouter API client for text transformations."""

import httpx
from typing import Optional, List, Dict


class OpenRouterClient:
    """Client for OpenRouter API."""

    BASE_URL = "https://openrouter.ai/api/v1"

    def __init__(self, api_key: str, model: str = "openai/gpt-4o-mini"):
        """Initialize OpenRouter client.

        Args:
            api_key: OpenRouter API key
            model: Model identifier (default: openai/gpt-4o-mini)
        """
        self.api_key = api_key
        self.model = model
        self.client = httpx.AsyncClient(timeout=60.0)

    async def transform_text(
        self,
        text: str,
        transformations: List[str],
        user_details: Optional[Dict[str, str]] = None,
        temperature: float = 0.0
    ) -> str:
        """Apply transformations to text using LLM.

        Args:
            text: Text to transform
            transformations: List of transformation prompts
            user_details: Optional user details to inject
            temperature: Temperature for generation (default: 0.0 for consistency)

        Returns:
            Transformed text

        Raises:
            httpx.HTTPError: If API request fails
        """
        # Build the system prompt
        system_parts = []

        # Add transformation instructions
        if len(transformations) == 1:
            system_parts.append(transformations[0])
        else:
            system_parts.append("Please apply the following list of edits to the text:")
            system_parts.append("\n\n---\n\n".join(transformations))

        # Add user details if provided
        if user_details:
            details_text = "\n".join(f"{k}: {v}" for k, v in user_details.items())
            system_parts.append(
                f"\nUser details (customize using these if necessary):\n{details_text}"
            )

        system_prompt = "\n\n".join(system_parts)

        # Make API request
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": text}
            ],
            "temperature": temperature,
        }

        response = await self.client.post(
            f"{self.BASE_URL}/chat/completions",
            headers=headers,
            json=payload
        )
        response.raise_for_status()

        data = response.json()
        return data["choices"][0]["message"]["content"]

    async def close(self):
        """Close the HTTP client."""
        await self.client.aclose()

    async def __aenter__(self):
        """Async context manager entry."""
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.close()
