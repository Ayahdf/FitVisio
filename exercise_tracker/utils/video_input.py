import cv2

class VideoInput:
    @staticmethod
    def get_video_source(source=0):
        """Get video source (webcam or video file)"""
        cap = cv2.VideoCapture(source)
        if not cap.isOpened():
            raise ValueError("Unable to open video source")
        return cap

    @staticmethod
    def get_frame_size(cap):
        """Get frame width and height"""
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        return (width, height)

    @staticmethod
    def get_fps(cap):
        """Get frames per second"""
        return cap.get(cv2.CAP_PROP_FPS)