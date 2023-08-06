class Annotation:
    left = 0
    top = 0
    width = 0
    height = 0
    tagName = None

    def __init__(
        self, left: float, top: float, width: float, height: float,
            tagName: str = None):

        self.left = left
        self.top = top
        self.width = width
        self.height = height
        self.tagName = tagName
