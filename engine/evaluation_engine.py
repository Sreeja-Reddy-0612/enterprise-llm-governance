"""
Core evaluation engine for orchestrating multiple evaluators.
"""

from typing import Dict, List
from ..evaluators import (
    HallucinationEvaluator,
    ToneEvaluator,
    DeterminismEvaluator,
    RefusalEvaluator,
    PolicyViolationEvaluator
)


class EvaluationEngine:
    """Orchestrates multiple evaluators to assess LLM responses."""
    
    def __init__(self, policy_rules: Dict = None):
        """
        Initialize the evaluation engine.
        
        Args:
            policy_rules: Policy rules for policy violation evaluator
        """
        self.hallucination_evaluator = HallucinationEvaluator()
        self.tone_evaluator = ToneEvaluator()
        self.determinism_evaluator = DeterminismEvaluator()
        self.refusal_evaluator = RefusalEvaluator()
        self.policy_violation_evaluator = PolicyViolationEvaluator(policy_rules)
    
    def evaluate(self, response: str, query: str, context: Dict = None) -> Dict:
        """
        Run all evaluators on a response.
        
        Args:
            response: The LLM response to evaluate
            query: The original query
            context: Optional context for evaluation
            
        Returns:
            Dictionary with all evaluation results
        """
        results = {
            'hallucination': self.hallucination_evaluator.evaluate(response, context),
            'tone': self.tone_evaluator.evaluate(response),
            'refusal': self.refusal_evaluator.evaluate(response, query),
            'policy_violation': self.policy_violation_evaluator.evaluate(response, query),
        }
        
        return results
    
    def evaluate_determinism(self, responses: List[str], query: str) -> Dict:
        """
        Evaluate determinism across multiple responses.
        
        Args:
            responses: List of responses to the same query
            query: The original query
            
        Returns:
            Dictionary with determinism evaluation results
        """
        return self.determinism_evaluator.evaluate(responses, query)

