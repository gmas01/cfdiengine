class Frame(object):

    FRAME_HEADER_LENGTH = 4
    FRAME_BODY_MAX_LENGTH = 512
    ACTION_FLOW_INFO_SEGMENT_LENGTH = 2
    ACTION_ACK_DATA_SIZE = 2
    FRAME_FULL_MAX_LENGTH = FRAME_HEADER_LENGTH + FRAME_BODY_MAX_LENGTH
    ACTION_DATA_SEGMENT_MAX_LENGTH = FRAME_BODY_MAX_LENGTH - ACTION_FLOW_INFO_SEGMENT_LENGTH
    C_NULL_CHARACTER = 0

    REPLY_PASS = b'\x06'
    REPLY_FAIL = b'\x15'

    def __init__(self):
        byteszero = lambda n: bytes([0] * n)
        header = byteszero(self.FRAME_HEADER_LENGTH)
        body = byteszero(self.FRAME_BODY_MAX_LENGTH)

    @staticmethod
    def encode_header(action_length):
        l = []
        for sc in '{:3d}'.format(action_length):
            l.append(ord(sc))
        l.append(Frame.C_NULL_CHARACTER)
        return bytes(l)

    @staticmethod
    def decode_header(header):
        cut_nullchar = lambda s: s[0:-1]
        if (len(header) == Frame.FRAME_HEADER_LENGTH):
            return int(cut_nullchar(header).decode("utf-8"))
