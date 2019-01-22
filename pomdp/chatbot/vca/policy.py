import logging
from rasa_core.policies.policy import Policy

logger = logging.getLogger(__name__)


class PomdpPolicy(Policy):

    def predict_action_probabilities(self, tracker, domain):
        logger.debug("predicting next action")
        result = [0.0] * domain.num_actions
        return result

    def train(self,
              training_trackers,  # type: List[DialogueStateTracker]
              domain,  # type: Domain
              **kwargs  # type: Any
              ):
        logger.debug("training ...")

    def persist(self, path):
        pass

    @classmethod
    def load(cls, path):
        return cls()
