"""
Problem Test Suite Update & Rejudge Coordinator
"""
class RejudgeService:
    @staticmethod
    def prepare_rejudge_batch(submission_ids: list) -> list:
        batch = []
        for sid in submission_ids:
            batch.append({
                "submissionId": sid,
                "status": "PENDING_REJUDGE",
                "scoreDelta": 0
            })
        return batch

    @staticmethod
    def calculate_score_delta(old_score: int, new_score: int) -> int:
        return new_score - old_score
