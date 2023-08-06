"""
hudai.resources.model_score
"""
from ..helpers.resource import Resource


class ModelScoreResource(Resource):
    def __init__(self, client):
        Resource.__init__(self, client, base_path='/articles/scores')
        self.resource_name = 'ModelScore'

    def list(self,
               content_id=None,
               content_type=None,
               importance_score_min=None,
               tipsheet_X_G_B_score_min=None,
               local_X_G_B_score_min=None,
               shill_X_G_B_score_min=None,
               importance_score_max=None,
               tipsheet_X_G_B_score_max=None,
               local_X_G_B_score_max=None,
               shill_X_G_B_score_max=None):
        return self._create(
            content_id=content_id,
            content_type=content_type,
            importance_score_min=importance_score_min,
            tipsheet_X_G_B_score_min=tipsheet_X_G_B_score_min,
            local_X_G_B_score_min=local_X_G_B_score_min,
            shill_X_G_B_score_min=shill_X_G_B_score_min,
            importance_score_max=importance_score_max,
            tipsheet_X_G_B_score_max=tipsheet_X_G_B_score_max,
            local_X_G_B_score_max=local_X_G_B_score_max,
            shill_X_G_B_score_max=shill_X_G_B_score_max
        )

    def create(self,
               content_id=None,
               content_type=None,
               importance_score=None,
               tipsheet_X_G_B_score=None,
               local_X_G_B_score=None,
               shill_X_G_B_score=None):
        return self._create(
            content_id=content_id,
            content_type=content_type,
            importance_score=importance_score,
            tipsheet_X_G_B_score=tipsheet_X_G_B_score,
            local_X_G_B_score=local_X_G_B_score,
            shill_X_G_B_score=shill_X_G_B_score
        )

    def fetch(self, entity_id):
        return self._fetch(entity_id)

    def upsert(self,
               content_id=None,
               content_type=None,
               importance_score=None,
               tipsheet_X_G_B_score=None,
               local_X_G_B_score=None,
               shill_X_G_B_score=None):
        return self._upsert(
            content_id=content_id,
            content_type=content_type,
            importance_score=importance_score,
            tipsheet_X_G_B_score=tipsheet_X_G_B_score,
            local_X_G_B_score=local_X_G_B_score,
            shill_X_G_B_score=shill_X_G_B_score
        )

    def delete(self, entity_id):
        return self._delete(entity_id)
