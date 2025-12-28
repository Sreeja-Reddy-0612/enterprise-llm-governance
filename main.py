"""
Main entry point for the Enterprise LLM Governance system.
"""

import json
import yaml
from pathlib import Path
from typing import Dict, Optional

from engine.prompt_loader import PromptLoader
from engine.evaluation_engine import EvaluationEngine
from engine.risk_scorer import RiskScorer
from engine.decision_engine import DecisionEngine


def load_config(config_path: str = "config/governance_rules.yaml") -> Dict:
    """Load governance configuration."""
    with open(config_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def main():
    """Main execution function."""
    # Load configuration
    config = load_config()
    
    # Initialize components
    prompt_loader = PromptLoader("prompts")
    evaluation_engine = EvaluationEngine(
        policy_rules=config.get('policy_rules', {})
    )
    risk_scorer = RiskScorer(
        weights=config.get('risk_weights', {})
    )
    decision_engine = DecisionEngine(
        risk_threshold=config.get('risk_threshold', 0.5),
        risk_scorer=risk_scorer
    )
    
    # Example usage
    print("Enterprise LLM Governance System")
    print("=" * 40)
    
    # List available prompts
    prompts = prompt_loader.list_prompts()
    print(f"\nAvailable prompts: {', '.join(prompts)}")
    
    # Load sample query
    queries_path = Path("inputs/sample_queries.json")
    if queries_path.exists():
        with open(queries_path, 'r', encoding='utf-8') as f:
            queries_data = json.load(f)
            print(f"\nLoaded {len(queries_data.get('queries', []))} sample queries")
    
    print("\nSystem initialized successfully!")


if __name__ == "__main__":
    main()

