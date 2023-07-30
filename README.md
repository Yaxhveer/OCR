# OCR

Perform text detection on text, video and realtime with webcam using TesseractOCR.

# Use

Command line arguments:

    -h, --help        show help
    -i, --image       image input
    -v, --video       video input
    -c, --camera      realtime video capture source (default 0)
    -f, --fps         fps for saved video
    -s, --saveFile    file name where data is to be saved
    -l, --lang        tesseract language


# Installation

- Download tesseract.exe from https://github.com/UB-Mannheim/tesseract/wiki and install this exe in "C:\Program Files (x86)\Tesseract-OCR"

- Install the packages
```
pip install -r requirements.txt
```
- Run script
```
python main.py OCR [-h] [-i | -v | -c] [-f] [-s] [-l]
```
