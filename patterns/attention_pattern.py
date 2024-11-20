class AttentionPattern:
    def determine_block_status(self, sub_block_statuses):
        if all(status == "Sleeping" for status in sub_block_statuses):
            return "Sleepy"
        if all(status == "HeadTurned" for status in sub_block_statuses):
            return "Distracted"
        if all(status == "OpenEyes" for status in sub_block_statuses):
            return "HighlyFocused"

        blink_count = sub_block_statuses.count("Blinked")
        if blink_count > len(sub_block_statuses) / 2:
            return "ModeratelyFocused"

        return "LostAttention"
