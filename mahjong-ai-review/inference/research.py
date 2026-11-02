"""Research facade: retain empirical baseline for unproven wait/risk tasks."""
import json,torch
from inference.predictor import Predictor
class ResearchPredictor:
    def __init__(self,checkpoint,baseline):
        self.predictor=Predictor(checkpoint);self.baseline=json.load(open(baseline))
    def predict(self,features,candidate_mask=None,target_active=None):
        r=self.predictor.predict(features);j=torch.tensor(self.baseline['joint']);w=torch.tensor(self.baseline['conditional_wait'])
        r['research_only']=True;r['deployment_status']='not_a_decision_policy';r['recommended_wait_given_tenpai']=w.tolist();r['recommended_deal_in_probability']=(1-j[:,0]).tolist();r['fallback_reason']='wait/risk improvement not established; empirical training-frequency baseline retained'
        r['flags']+=['SCORE_SUPPORT_EMPIRICAL','TAIL_UNVALIDATED','CALLER_MUST_ENFORCE_LEGALITY_MASKS','BASELINE_FALLBACK_NOT_GAME_CONDITIONED','SIMULATOR_ONLY','NO_REAL_PLAYER_VALIDATION']
        if candidate_mask is not None:
            if len(candidate_mask)!=27:raise ValueError('candidate mask must have 27 entries')
            r['candidate_mask']=list(candidate_mask)
            r['recommended_deal_in_probability']=[p if candidate_mask[i] else None for i,p in enumerate(r['recommended_deal_in_probability'])]
        if target_active is not None:
            if len(target_active)!=3:raise ValueError('active mask must have 3 entries')
            r['target_active']=list(target_active)
            r['recommended_wait_given_tenpai']=[w if target_active[i] else [0.]*27 for i,w in enumerate(r['recommended_wait_given_tenpai'])]
        return r
