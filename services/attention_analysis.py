from patterns.block_structure import Block, SubBlock
from patterns.attention_pattern import AttentionPattern

class AttentionAnalysisService:
    MIN_SUB_BLOCKS_FOR_BLOCK_ANALYSIS = 5

    def analyze_block(self, sub_blocks):
        if len(sub_blocks) < self.MIN_SUB_BLOCKS_FOR_BLOCK_ANALYSIS:
            return "LostAttention" 

        sub_block_statuses = [sub_block.status for sub_block in sub_blocks]
        pattern = AttentionPattern()
        return pattern.determine_block_status(sub_block_statuses)

    def analyze_sub_block(self, frame_statuses):
        if all(status == "FaceNotDetected" for status in frame_statuses):
            return "PersonNotFound"
        if all(status == "ClosedEyes" for status in frame_statuses):
            return "Sleeping"
        if all(status in ["HeadTurnedLeft", "HeadTurnedRight"] for status in frame_statuses):
            return "HeadTurned"
        if "OpenEyes" in frame_statuses and "ClosedEyes" in frame_statuses:
            return "Blinked"

        return "OpenEyes"
