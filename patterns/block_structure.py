class FrameStatus:
    OPEN_EYES = "OpenEyes"
    CLOSED_EYES = "ClosedEyes"
    HEAD_TURNED_LEFT = "HeadTurnedLeft"
    HEAD_TURNED_RIGHT = "HeadTurnedRight"
    HEAD_STRAIGHT = "HeadStraight"
    FACE_NOT_DETECTED = "FaceNotDetected"


class SubBlockStatus:
    BLINKED = "Blinked"
    SLEEPING = "Sleeping"
    OPEN_EYES = "OpenEyes"
    HEAD_TURNED = "HeadTurned"
    PERSON_NOT_FOUND = "PersonNotFound"


class BlockStatus:
    HIGHLY_FOCUSED = "HighlyFocused"
    MODERATELY_FOCUSED = "ModeratelyFocused"
    DISTRACTED = "Distracted"
    SLEEPY = "Sleepy"
    LOST_ATTENTION = "LostAttention"

from patterns.attention_pattern import AttentionPattern
class SubBlock:
    def __init__(self, frames):
        self.frames = frames
        self.status = self.determine_status()

    def determine_status(self):
        if all(status == FrameStatus.FACE_NOT_DETECTED for status in self.frames):
            return SubBlockStatus.PERSON_NOT_FOUND
        if all(status == FrameStatus.CLOSED_EYES for status in self.frames):
            return SubBlockStatus.SLEEPING
        if all(status in [FrameStatus.HEAD_TURNED_LEFT, FrameStatus.HEAD_TURNED_RIGHT] for status in self.frames):
            return SubBlockStatus.HEAD_TURNED
        if FrameStatus.OPEN_EYES in self.frames and FrameStatus.CLOSED_EYES in self.frames:
            return SubBlockStatus.BLINKED

        return SubBlockStatus.OPEN_EYES


class Block:
    def __init__(self, sub_blocks):
        self.sub_blocks = sub_blocks
        self.status = self.determine_status()

    def determine_status(self):
        pattern = AttentionPattern()
        return pattern.determine_block_status([sub_block.status for sub_block in self.sub_blocks])
