"""
Module for making governance decisions based on evaluation results.
"""

from typing import Dict, Optional
from .risk_scorer import RiskScorer


class DecisionEngine:
    """Makes governance decisions based on risk scores and evaluation results."""
    
    def __init__(self, risk_threshold: float = 0.5, risk_scorer: Optional[RiskScorer] = None):
        """
        Initialize the decision engine.
        
        Args:
            risk_threshold: Risk score threshold for approval (0.0-1.0)
            risk_scorer: Optional RiskScorer instance
        """
        self.risk_threshold = risk_threshold
        self.risk_scorer = risk_scorer or RiskScorer()
    
    def make_decision(self, evaluation_results: Dict) -> Dict:
        """
        Make a governance decision based on evaluation results.
        
        Args:
            evaluation_results: Dictionary of evaluation results from EvaluationEngine
            
        Returns:
            Dictionary with decision (approved/rejected) and reasoning
        """
        risk_score = self.risk_scorer.calculate_risk_score(evaluation_results)
        
        decision = 'approved' if risk_score < self.risk_threshold else 'rejected'
        
        return {
            'decision': decision,
            'risk_score': risk_score,
            'threshold': self.risk_threshold,
            'reasoning': self._generate_reasoning(evaluation_results, risk_score),
            'evaluation_results': evaluation_results
        }
    
    def _generate_reasoning(self, evaluation_results: Dict, risk_score: float) -> str:
        """
        Generate human-readable reasoning for the decision.
        
        Args:
            evaluation_results: Evaluation results
            risk_score: Calculated risk score
            
        Returns:
            Reasoning string
        """
        # TODO: Implement reasoning generation
        return f"Risk score: {risk_score:.2f} (threshold: {self.risk_threshold:.2f})"

