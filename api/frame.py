class Frame(object):

    FRAME_HEADER_LENGTH = 4
    FRAME_BODY_MAX_LENGTH = 512
    ACTION_FLOW_INFO_SEGMENT_LENGTH = 2
    ACTION_ACK_DATA_SIZE = 2
    FRAME_FULL_MAX_LENGTH = FRAME_HEADER_LENGTH + FRAME_BODY_MAX_LENGTH
    ACTION_DATA_SEGMENT_MAX_LENGTH = FRAME_BODY_MAX_LENGTH - ACTION_FLOW_INFO_SEGMENT_LENGTH
    C_NULL_CHARACTER = 0

    def __init__(self):
        pass
