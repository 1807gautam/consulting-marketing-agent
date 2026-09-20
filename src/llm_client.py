"""
IBM Consulting AI (ICA) API client.
Endpoint: https://api.nextgen-beta.ica.ibm.com/ica/v1
Model:    claude-sonnet-4-5
Supports the OpenAI-compatible /chat/completions endpoint.
"""

import os
import requests
from typing import Optional
from dotenv import load_dotenv

load_dotenv()


class ICAClient:
    """
    Client for IBM Consulting AI (ICA) nextgen-beta API.
    Environment variables (all read from .env or Streamlit secrets):
      ICA_API_KEY   — Bearer token
      ICA_BASE_URL  — Base URL (no trailing slash)
      ICA_MODEL     — Model identifier
      ICA_MAX_TOKENS — Max output tokens (default 8192)
      ICA_TEMPERATURE — Generation temperature (default 0.3)
    """

    def __init__(self):
        # Support both old-style ICA_API_BASE_URL and new ICA_BASE_URL
        self.api_base_url = (
            os.getenv("ICA_BASE_URL")
            or os.getenv("ICA_API_BASE_URL", "https://api.nextgen-beta.ica.ibm.com/ica/v1")
        ).rstrip("/")

        self.api_key = os.getenv("ICA_API_KEY", "")

        # Support both ICA_MODEL and legacy ICA_MODEL_ID
        self.model_id = (
            os.getenv("ICA_MODEL")
            or os.getenv("ICA_MODEL_ID", "claude-sonnet-4-5")
        )

        self.max_tokens = int(os.getenv("ICA_MAX_TOKENS", "8192"))
        self.temperature = float(os.getenv("ICA_TEMPERATURE", "0.3"))

        self._session = requests.Session()
        if os.getenv("HTTPS_PROXY"):
            self._session.proxies = {
                "https": os.getenv("HTTPS_PROXY"),
                "http": os.getenv("HTTP_PROXY", os.getenv("HTTPS_PROXY")),
            }

    @property
    def is_configured(self) -> bool:
        return bool(self.api_key and self.api_key not in ("", "your_ica_api_key_here"))

    def chat(self, system_prompt: str, user_prompt: str, max_tokens: Optional[int] = None) -> str:
        """
        Send a chat completion request and return the assistant's response text.
        Raises ValueError if API key is not configured.
        Raises RuntimeError on API errors.
        """
        if not self.is_configured:
            raise ValueError(
                "ICA API key is not configured. "
                "Please set ICA_API_KEY in your .env file or Streamlit secrets."
            )

        endpoint = f"{self.api_base_url}/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }

        payload = {
            "model": self.model_id,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "max_tokens": max_tokens or self.max_tokens,
            "temperature": self.temperature,
        }

        try:
            response = self._session.post(
                endpoint,
                json=payload,
                headers=headers,
                timeout=300,   # 5 min — large documents need time
            )
            response.raise_for_status()
            data = response.json()

            # OpenAI-compatible response (ICA nextgen-beta format)
            if "choices" in data and data["choices"]:
                return data["choices"][0]["message"]["content"].strip()

            # Fallback for older IBM API formats
            if "results" in data and data["results"]:
                return data["results"][0].get("generated_text", "").strip()

            raise RuntimeError(f"Unexpected API response format: {data}")

        except requests.exceptions.Timeout:
            raise RuntimeError(
                "Request timed out after 5 minutes. "
                "Try uploading smaller files or splitting the analysis."
            )
        except requests.exceptions.HTTPError as e:
            status = e.response.status_code if e.response else "unknown"
            # Capture full error body for diagnosis (truncated to 1,000 chars)
            try:
                body = e.response.text[:1000] if e.response else "(no response body)"
            except Exception:
                body = "(could not read response body)"

            # Give a human-readable hint for the most common errors
            if status == 401:
                hint = "⛔ 401 Unauthorised — your ICA API key is missing or malformed."
            elif status == 403:
                hint = (
                    "⛔ 403 Forbidden — your ICA API key has EXPIRED or is invalid.\n"
                    "Action: generate a new key at https://nextgen-beta.ica.ibm.com "
                    "and update ICA_API_KEY in your .env file (local) or Streamlit secrets (cloud)."
                )
            elif status == 429:
                hint = "⛔ 429 Rate limited — too many requests. Wait a minute and try again."
            elif status == 413:
                hint = "⛔ 413 Payload too large — reduce the number or size of uploaded files."
            else:
                hint = ""

            msg = f"ICA API HTTP {status} error."
            if hint:
                msg += f"\n{hint}"
            msg += f"\nEndpoint: {endpoint}\nModel: {self.model_id}\nAPI response: {body}"
            raise RuntimeError(msg)
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"Network error contacting ICA API: {str(e)}")


# Singleton instance — reset if env changes
_client: Optional[ICAClient] = None


def get_client() -> ICAClient:
    global _client
    if _client is None:
        _client = ICAClient()
    return _client


def reset_client() -> None:
    """Force re-initialisation (useful after env changes in tests)."""
    global _client
    _client = None
