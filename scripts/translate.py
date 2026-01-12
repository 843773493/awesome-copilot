#!/usr/bin/env python3
"""
SiliconFlow API Markdown Translation Tool
Supports batch translation, progress display, custom parameters
"""

import os
import sys

# Disable all proxy environment variables BEFORE importing other modules
# This must be done before any imports that use HTTP
for var in ['http_proxy', 'https_proxy', 'all_proxy', 'HTTP_PROXY', 'HTTPS_PROXY', 'ALL_PROXY', 'no_proxy', 'NO_PROXY']:
    if var in os.environ:
        del os.environ[var]

import json
from pathlib import Path
from typing import Optional, Dict, List
from dotenv import load_dotenv

# Import with proxy disabled
os.environ['REQUESTS_CA_BUNDLE'] = ''
os.environ['CURL_CA_BUNDLE'] = ''

from openai import OpenAI

# Load .env file
load_dotenv()

class TranslationConfig:
    """Translation configuration class"""

    def __init__(self):
        self.api_key = os.getenv("DEFAULT_API_KEY")
        self.model = "Qwen/Qwen3-8B"
        self.temperature = 0.3
        self.max_tokens = 4000
        self.language = "Chinese"
        self.preserve_code = True
        self.output_suffix = ".zh-CN"

class MarkdownTranslator:
    """Markdown document translator"""

    def __init__(self, config: TranslationConfig):
        self.config = config
        self._init_client()

    def _init_client(self):
        """Initialize OpenAI client"""
        import httpx

        # Create an httpx client with explicitly no proxies
        http_client = httpx.Client(
            trust_env=False  # Don't read environment variables
        )

        self.client = OpenAI(
            api_key=self.config.api_key,
            base_url="https://api.siliconflow.cn/v1",
            http_client=http_client
        )

    def _build_system_prompt(self) -> str:
        """Build system prompt for translation"""
        return "You are a professional technical document translator. Translate English Markdown documents into Chinese while preserving all formatting, code blocks, links, and special markers."

    def _build_user_prompt(self, content: str) -> str:
        """Build user prompt"""
        return f"Please translate the following Markdown document into Chinese:\n\n{content}"

    def translate(self, file_path: str, output_path: Optional[str] = None) -> Dict:
        """
        Translate single file

        Args:
            file_path: Source file path
            output_path: Output file path (auto-generated if None)

        Returns:
            Dictionary with translation statistics
        """

        # Read source file
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except FileNotFoundError:
            return {"success": False, "error": f"File not found: {file_path}"}
        except Exception as e:
            return {"success": False, "error": f"Failed to read file: {e}"}

        # Call API for translation
        try:
            print(f"Translating: {file_path}")
            response = self.client.chat.completions.create(
                model=self.config.model,
                messages=[
                    {"role": "system", "content": self._build_system_prompt()},
                    {"role": "user", "content": self._build_user_prompt(content)}
                ],
                temperature=self.config.temperature,
                max_tokens=self.config.max_tokens
            )

            translated_content = response.choices[0].message.content

        except Exception as e:
            return {"success": False, "error": f"API call failed: {e}"}

        # Save translation result
        if output_path is None:
            path = Path(file_path)
            output_filename = f"{path.stem}{self.config.output_suffix}{path.suffix}"
            output_path = path.parent / output_filename

        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(translated_content)
        except Exception as e:
            return {"success": False, "error": f"Failed to save file: {e}"}

        return {
            "success": True,
            "input_file": file_path,
            "output_file": str(output_path),
            "input_size": len(content),
            "output_size": len(translated_content),
            "input_chars": len(content),
            "output_chars": len(translated_content),
            "tokens_used": {
                "prompt": response.usage.prompt_tokens,
                "completion": response.usage.completion_tokens,
                "total": response.usage.total_tokens
            }
        }

    def batch_translate(self, file_paths: List[str]) -> List[Dict]:
        """Batch translate multiple files"""
        results = []
        for i, file_path in enumerate(file_paths, 1):
            print(f"\n[{i}/{len(file_paths)}] ", end="")
            result = self.translate(file_path)
            results.append(result)

            if result["success"]:
                print(f"Success: {result['output_file']}")
            else:
                print(f"Failed: {result['error']}")

        return results

def print_header():
    """Print header"""
    print("=" * 70)
    print("SiliconFlow API - Markdown Translation Tool")
    print("=" * 70)

def print_stats(result: Dict):
    """Print statistics"""
    if result["success"]:
        print("\nTranslation Statistics:")
        print(f"   Input file: {result['input_file']}")
        print(f"   Output file: {result['output_file']}")
        print(f"   Input chars: {result['input_chars']}")
        print(f"   Output chars: {result['output_chars']}")
        print(f"   Tokens used: {result['tokens_used']['total']} "
              f"(prompt: {result['tokens_used']['prompt']}, "
              f"completion: {result['tokens_used']['completion']})")

def main():
    """Main function"""

    print_header()

    # Check API key
    api_key = os.getenv("DEFAULT_API_KEY")
    if not api_key:
        print("Error: Environment variable DEFAULT_API_KEY not set")
        print("   Please set DEFAULT_API_KEY environment variable")
        sys.exit(1)

    # Parse command line arguments
    if len(sys.argv) < 2:
        print("Usage: python translate.py <file1> [file2] [file3] ...")
        print("\nExamples:")
        print("  python translate.py README.md")
        print("  python translate.py AGENTS.md CONTRIBUTING.md")
        sys.exit(1)

    file_paths = sys.argv[1:]

    # Create translator
    config = TranslationConfig()
    translator = MarkdownTranslator(config)

    # Execute translation
    if len(file_paths) == 1:
        result = translator.translate(file_paths[0])
        print_stats(result)
    else:
        results = translator.batch_translate(file_paths)

        # Summary statistics
        print("\n" + "=" * 70)
        print("Batch Translation Summary:")
        successful = sum(1 for r in results if r["success"])
        failed = len(results) - successful
        total_tokens = sum(r.get("tokens_used", {}).get("total", 0)
                          for r in results if r["success"])

        print(f"   Successful: {successful}/{len(results)}")
        print(f"   Failed: {failed}/{len(results)}")
        print(f"   Total tokens used: {total_tokens}")
        print("=" * 70)

    print("\nTranslation completed!")

if __name__ == "__main__":
    main()
