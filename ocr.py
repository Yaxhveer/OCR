import cv2
import pytesseract
import PIL
import numpy as np

pytesseract.pytesseract.tesseract_cmd = 'C:\Program Files\Tesseract-OCR\\tesseract.exe'

class VideoStream:
    def __init__(self, path: int|str, fileName: str, fps: int, lang: str) -> None:
        self.video = cv2.VideoCapture(path)
        self.stopped = True
        self.count = 0
        self.duration = 0
        self.record = None
        self.fileName = fileName
        self.fps = fps
        self.lang = lang 

    def start(self) -> object:
        self.stopped = False
        print("Press q to exit.")
        width = int(self.video.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(self.video.get(cv2.CAP_PROP_FRAME_HEIGHT))
        size = (width, height)
        self.record = cv2.VideoWriter(filename=self.fileName+".avi", fourcc=cv2.VideoWriter_fourcc(*'MJPG'), fps=self.fps, frameSize=size)

        self.getFrames()
        return self

    def getFrames(self) -> None:
        while not self.stopped:
            (self.ret, self.frame) = self.video.read()
            if not self.ret or cv2.waitKey(1) == ord('q'):
                print("End")
                self.stop()
                break

            self.OCR()

    def OCR(self):
        ocr = OCR(self.frame, self.lang)
        self.frame = ocr.ocr()
        self.record.write(self.frame)
        cv2.imshow('frame', self.frame)

    def stop(self) -> None:
        self.stopped = False
        self.video.release()
        self.record.release()
        cv2.destroyAllWindows()

class OCR:
    def __init__(self, image, lang):
        self.image = image
        self.data = []
        self.lang = lang
    def start(self):
        self.ocr()

    def preprocess(self):
        im = self.image
        channels = im.shape[-1] if im.ndim == 3 else 1
        if channels != 1:
            im = cv2.cvtColor(im, cv2.COLOR_RGB2GRAY)
            _, im = cv2.threshold(im, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)

        return im

    def extractData(self, image):
        value = pytesseract.image_to_data(image, lang=self.lang, output_type = pytesseract.Output.DICT)
        for i in range(len(value["text"])):
            confidence = int(value["conf"][i])
            if confidence >= 35:
                x = value["left"][i]
                y = value["top"][i]
                w = value["width"][i]
                h = value["height"][i]
                text = value["text"][i]
                self.data.append({'text': text, 'x': x, 'y': y, 'w': w, 'h': h})

    def putData(self):
        for word in self.data:
            x, y, w, h, text = word['x'], word['y'],word['w'], word['h'], word['text']
            self.image = cv2.rectangle(self.image, (x, y), (x + w, y + h), (255, 0, 0), 1)
            
            # ignoring unicode characters since CV2 is only able to display ascii characters at the moment 
            text = text.encode("ascii", "ignore")
            text = text.decode()

            cv2.putText(self.image, text, (x, y-4), cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 0), 1, 2)

    def ocr(self):
        self.image = np.array(self.image)
        preprocessedImage = self.preprocess()
        self.extractData(preprocessedImage)
        self.putData()
        return self.image

def Video(path: str | int, fileName: str, fps: int, lang: str):
    stream = VideoStream(path, fileName, fps, lang)
    stream.start()

def Image(path: str, file: str, lang: str):
    image = PIL.Image.open(path)
    ocr = OCR(image, lang)
    image = ocr.ocr()
    cv2.imwrite(file+'.jpeg', image)