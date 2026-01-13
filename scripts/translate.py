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
import asyncio
import time
from pathlib import Path
from typing import Optional, Dict, List
from dotenv import load_dotenv
from concurrent.futures import ThreadPoolExecutor, as_completed, wait
from threading import Lock
from tqdm import tqdm

# Import with proxy disabled
os.environ['REQUESTS_CA_BUNDLE'] = ''
os.environ['CURL_CA_BUNDLE'] = ''

from openai import AsyncOpenAI

# Load .env file
load_dotenv()

class TranslationConfig:
    """Translation configuration class"""

    def __init__(self):
        self.api_key = os.getenv("DEFAULT_API_KEY")
        self.model = "Qwen/Qwen3-8B"
        self.temperature = 0.3
        self.max_tokens = 32*1024
        self.enable_thinking = True
        self.language = "Chinese"
        self.preserve_code = True
        self.output_suffix = ".zh-CN"
        self.max_concurrent = 10  # Reduced from 10 to avoid rate limiting
        self.max_retries = 3  # Maximum retry attempts for 429 errors
        self.initial_retry_delay = 2  # Initial delay in seconds for exponential backoff
        self.request_delay = 0.5  # Delay between requests in seconds

class MarkdownTranslator:
    """Markdown document translator"""

    def __init__(self, config: TranslationConfig):
        self.config = config
        self._init_client()
        self._shutdown_event = None
        self._semaphore = None
        self._request_lock = None

    def _init_async_objects(self):
        """Initialize async objects (must be called within an event loop)"""
        if self._semaphore is None:
            self._semaphore = asyncio.Semaphore(self.config.max_concurrent)
        if self._request_lock is None:
            self._request_lock = asyncio.Lock()
        if self._shutdown_event is None:
            self._shutdown_event = asyncio.Event()

    def _init_client(self):
        """Initialize AsyncOpenAI client"""
        import httpx

        # Create an httpx async client with timeout and no proxies
        http_client = httpx.AsyncClient(
            trust_env=False,  # Don't read environment variables
            timeout=240.0  # 240 second timeout for all operations
        )

        self.client = AsyncOpenAI(
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

    async def _call_api_with_retry(self, file_path: str, content: str) -> Optional[Dict]:
        """
        Call API with exponential backoff retry for rate limiting

        Args:
            file_path: Source file path
            content: Content to translate

        Returns:
            API response or None if failed after retries
        """
        retry_count = 0
        delay = self.config.initial_retry_delay

        while retry_count <= self.config.max_retries:
            try:
                # Control concurrent requests with semaphore
                async with self._semaphore:
                    # Add small delay between requests to avoid spikes
                    async with self._request_lock:
                        await asyncio.sleep(self.config.request_delay)

                    response = await self.client.chat.completions.create(
                        model=self.config.model,
                        messages=[
                            {"role": "system", "content": self._build_system_prompt()},
                            {"role": "user", "content": self._build_user_prompt(content)}
                        ],
                        temperature=self.config.temperature,
                        max_tokens=self.config.max_tokens,
                        extra_body={"enable_thinking": self.config.enable_thinking}
                    )
                    return response

            except Exception as e:
                error_msg = str(e)
                # Check if it's a rate limit error (429)
                if "429" in error_msg or "rate limit" in error_msg.lower() or "tpm limit" in error_msg.lower():
                    retry_count += 1
                    if retry_count <= self.config.max_retries:
                        print(f"\n⚠ Rate limited (429), retrying {file_path} in {delay}s... (attempt {retry_count}/{self.config.max_retries})")
                        await asyncio.sleep(delay)
                        # Exponential backoff: 2s -> 4s -> 8s
                        delay *= 2
                    else:
                        return None
                else:
                    # Not a rate limit error, fail immediately
                    raise

        return None

    async def translate(self, file_path: str, output_path: Optional[str] = None) -> Dict:
        """
        Translate single file asynchronously

        Args:
            file_path: Source file path
            output_path: Output file path (auto-generated if None)

        Returns:
            Dictionary with translation statistics
        """

        # Check shutdown signal
        if self._shutdown_event.is_set():
            return {"success": False, "input_file": file_path, "error": "Translation cancelled"}

        # Read source file
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except FileNotFoundError:
            return {"success": False, "input_file": file_path, "error": f"File not found: {file_path}"}
        except Exception as e:
            return {"success": False, "input_file": file_path, "error": f"Failed to read file: {e}"}

        # Call API for translation with retry
        try:
            response = await self._call_api_with_retry(file_path, content)

            if response is None:
                return {"success": False, "input_file": file_path, "error": "API call failed: Rate limit exceeded after retries"}

            translated_content = response.choices[0].message.content

        except asyncio.CancelledError:
            return {"success": False, "input_file": file_path, "error": "Translation cancelled"}
        except Exception as e:
            return {"success": False, "input_file": file_path, "error": f"API call failed: {e}"}

        # Save translation result
        if output_path is None:
            path = Path(file_path)
            output_filename = f"{path.stem}{self.config.output_suffix}{path.suffix}"
            output_path = path.parent / output_filename

        try:
            # Strip excess leading/trailing whitespace while preserving single newlines at the end
            cleaned_content = translated_content.strip()
            # Ensure file ends with a single newline
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(cleaned_content + '\n')
        except Exception as e:
            return {"success": False, "input_file": file_path, "error": f"Failed to save file: {e}"}

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
        """Batch translate multiple files with concurrent async requests"""
        return asyncio.run(self._batch_translate_async(file_paths))

    async def _batch_translate_async(self, file_paths: List[str]) -> List[Dict]:
        """Async batch translation with proper cancellation support"""
        # Initialize async objects within the event loop
        self._init_async_objects()

        results = [None] * len(file_paths)  # Preserve order
        print_lock = Lock()  # For thread-safe printing

        try:
            # Create tasks for all files
            tasks = [
                asyncio.create_task(self.translate(file_path))
                for file_path in file_paths
            ]

            # Process completed tasks with progress bar
            with tqdm(total=len(file_paths), desc="Translating", unit="file", ncols=80) as pbar:
                for idx, file_path in enumerate(file_paths):
                    try:
                        result = await tasks[idx]
                        results[idx] = result

                        # Thread-safe output
                        with print_lock:
                            status = "✓" if result["success"] else "✗"
                            if result["success"]:
                                output_file = Path(result["output_file"]).name
                                pbar.write(f"{status} {output_file}")
                            else:
                                input_file = Path(result["input_file"]).name
                                error = result.get("error", "Unknown error")
                                pbar.write(f"{status} {input_file}: {error}")
                        pbar.update(1)
                    except asyncio.CancelledError:
                        results[idx] = {
                            "success": False,
                            "input_file": file_path,
                            "error": "Translation cancelled"
                        }
                        with print_lock:
                            pbar.write(f"✗ {Path(file_path).name}: Cancelled")
                        pbar.update(1)
                    except Exception as e:
                        results[idx] = {
                            "success": False,
                            "input_file": file_path,
                            "error": f"Task failed: {str(e)}"
                        }
                        with print_lock:
                            pbar.write(f"✗ Task: {e}")
                        pbar.update(1)

        except KeyboardInterrupt:
            # Set shutdown event to signal all tasks to stop
            self._shutdown_event.set()

            # Cancel all pending tasks
            for task in tasks:
                if not task.done():
                    task.cancel()

            # Wait for all tasks to complete (with timeout)
            try:
                await asyncio.wait_for(asyncio.gather(*tasks, return_exceptions=True), timeout=2.0)
            except asyncio.TimeoutError:
                pass

            print("\n⚠ 用户中断，已停止所有翻译任务")
            raise

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
        async def _single_translate():
            translator._init_async_objects()
            return await translator.translate(file_paths[0])

        result = asyncio.run(_single_translate())
        print_stats(result)
    else:
        try:
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
        except KeyboardInterrupt:
            sys.exit(0)

    print("\nTranslation completed!")

if __name__ == "__main__":
    main()
