import os
import requests
from pathlib import Path
from dotenv import load_dotenv
from typing import Optional
# =============================================================================

# Smart environment loading
def load_environment():
    """Find and load .env file from multiple possible locations"""
    possible_locations = [
        '.env',
        '../.env', 
        '../../.env',
        Path.cwd() / '.env',
        Path.cwd().parent / '.env',
    ]
    
    for env_path in possible_locations:
        # Ensure env_path is always a Path object for consistency
        path_obj = env_path if isinstance(env_path, Path) else Path(env_path)
        if path_obj.exists():
            load_dotenv(path_obj, override=True)
            print(f"Loaded environment from: {path_obj}")
            return str(path_obj)
    
    print("No .env file found - using default settings")
    return None


# Load environment on import
load_environment()

# =============================================================================

class LLMManager:
    """
    Minimal provider-agnostic LLM manager.
    Supported providers: 'ollama' (default), 'openai'
    Configure via env:
      - LLM_PROVIDER: 'ollama' | 'openai' (default: 'ollama')
      - OLLAMA_BASE_URL (default: http://localhost:11434)
      - OLLAMA_DEFAULT_MODEL (default: llama3.2)
      - OPENAI_API_KEY
      - OPENAI_DEFAULT_MODEL (default: gpt-4o-mini)
    """

    def __init__(self, provider: Optional[str] = None):
        self.provider = (provider or os.getenv("LLM_PROVIDER", "ollama")).lower()
        self.available_providers = self._check_availability()  # <--- add this line

    def _check_availability(self) -> dict:
        available = {}
        # Check Ollama
        try:
            response = requests.get("http://localhost:11434/api/tags", timeout=2)
            print(f"Ollama check: status_code={response.status_code}")  # Debugging line
            available['ollama'] = response.status_code == 200
        except Exception as e:
            print(f"Ollama check failed: {e}")  # Debugging line
            available['ollama'] = False
        # Add other providers as needed...
        print(f"Available providers: {available}") # Debugging line
        return available
    
    def get_llm(self, provider: Optional[str] = None, model: Optional[str] = None):
        """Return an LLM client with provider-aware selection."""
        # Resolve provider
        if provider is None:
            provider = self._get_preferred_provider()
        elif provider not in self.available_providers or not self.available_providers[provider]:
            raise ValueError(f"Provider '{provider}' not available or not configured")

        # Dispatch to provider-specific factory
        if provider == "ollama":
            return self._get_ollama(model)
        elif provider == "google":
            return self._get_google(model)
        elif provider == "deepseek":
            return self._get_deepseek(model)
        elif provider == "groq":
            return self._get_groq(model)
        elif provider == "mistral":
            return self._get_mistral(model)
        elif provider == "anthropic":
            return self._get_anthropic(model)
        elif provider == "openai":
            return self._get_openai(model)
        else:
            raise ValueError(f"Unknown provider: {provider}")


    def _get_ollama(self, model: Optional[str] = None):
        """Local Ollama."""
        from langchain_ollama import ChatOllama
        default_model = os.getenv("OLLAMA_DEFAULT_MODEL", "llama3.2")
        base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        return ChatOllama(
            model=model or default_model,
            base_url=base_url,
            temperature=0.1,
        )


    def _get_google(self, model: Optional[str] = None):
        """Google Gemini."""
        from langchain_google_genai import ChatGoogleGenerativeAI
        default_model = os.getenv("GOOGLE_DEFAULT_MODEL", "gemini-2.0-flash-exp")
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY is not set")
        return ChatGoogleGenerativeAI(
            model=model or default_model,
            google_api_key=api_key,
            temperature=0.1,
        )


    def _get_deepseek(self, model: Optional[str] = None):
        """DeepSeek via OpenAI-compatible endpoint."""
        from langchain_openai import ChatOpenAI
        default_model = os.getenv("DEEPSEEK_DEFAULT_MODEL", "deepseek-chat")
        api_key = os.getenv("DEEPSEEK_API_KEY")
        if not api_key:
            raise ValueError("DEEPSEEK_API_KEY is not set")
        return ChatOpenAI(
            model=model or default_model,
            api_key=api_key,
            base_url="https://api.deepseek.com",
            temperature=0.1,
        )


    def _get_groq(self, model: Optional[str] = None):
        """Groq (ultra-fast)."""
        from langchain_groq import ChatGroq
        default_model = os.getenv("GROQ_DEFAULT_MODEL", "llama-3.1-8b-instant")
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY is not set")
        return ChatGroq(
            model=model or default_model,
            groq_api_key=api_key,
            temperature=0.1,
        )


    def _get_mistral(self, model: Optional[str] = None):
        """Mistral AI."""
        from langchain_mistralai import ChatMistralAI
        default_model = os.getenv("MISTRAL_DEFAULT_MODEL", "ministral-3b-latest")
        api_key = os.getenv("MISTRAL_API_KEY")
        if not api_key:
            raise ValueError("MISTRAL_API_KEY is not set")
        return ChatMistralAI(
            model=model or default_model,
            mistral_api_key=api_key,
            temperature=0.1,
        )


    def _get_anthropic(self, model: Optional[str] = None):
        """Anthropic Claude."""
        from langchain_anthropic import ChatAnthropic
        default_model = os.getenv("ANTHROPIC_DEFAULT_MODEL", "claude-3-haiku-20240307")
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY is not set")
        return ChatAnthropic(
            model=model or default_model,
            anthropic_api_key=api_key,
            temperature=0.1,
        )


    def _get_openai(self, model: Optional[str] = None):
        """OpenAI GPT."""
        from langchain_openai import ChatOpenAI
        default_model = os.getenv("OPENAI_DEFAULT_MODEL", "gpt-4o-mini")
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY is not set")
        return ChatOpenAI(
            model=model or default_model,
            api_key=api_key,
            temperature=0.1,
        )

    
# =============================================================================

# Convenience functions for agents
_default_manager: Optional[LLMManager] = None

def get_llm(provider: Optional[str] = None, model: Optional[str] = None):
    """
    Returns an LLM client. If provider is given, it is passed through to the manager,
    which will either use that provider or fall back to its preferred/default.
    """
    global _default_manager
    if _default_manager is None:
        _default_manager = LLMManager()  # Manager handles provider selection internally
    return _default_manager.get_llm(provider=provider, model=model)
