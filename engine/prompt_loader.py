"""
Module for loading and managing prompt versions.
"""

from pathlib import Path
from typing import Dict, Optional


class PromptLoader:
    """Loads and manages prompt templates."""
    
    def __init__(self, prompts_dir: str = "prompts"):
        """
        Initialize the prompt loader.
        
        Args:
            prompts_dir: Directory containing prompt files
        """
        self.prompts_dir = Path(prompts_dir)
    
    def load_prompt(self, prompt_name: str) -> Optional[str]:
        """
        Load a prompt template by name.
        
        Args:
            prompt_name: Name of the prompt file (without extension)
            
        Returns:
            Prompt content as string, or None if not found
        """
        prompt_path = self.prompts_dir / f"{prompt_name}.txt"
        if prompt_path.exists():
            return prompt_path.read_text(encoding='utf-8')
        return None
    
    def list_prompts(self) -> list:
        """
        List all available prompts.
        
        Returns:
            List of prompt names
        """
        return [f.stem for f in self.prompts_dir.glob("*.txt")]

