import argparse
import ocr

def main():
    """
    Command line arguments:
      -h, --help        show help
      -i, --image       image input
      -v, --video       video input
      -c, --camera      realtime video capture source (default 0)
      -f, --fps         fps for saved video
      -s, --saveFile    file name where data is to be saved
      -l, --lang        tesseract language
    """
 
    parser = argparse.ArgumentParser(
                        prog="OCR",
                        description="Used to get text data from images, videos or realtime.")
    
    g = parser.add_mutually_exclusive_group()
    g.add_argument('-i', '--image', help="image input", type=str)
    g.add_argument('-v', '--video', help="video input", type=str)
    g.add_argument('-c', '--camera', help="source for video capture", type=int, default=0)
    parser.add_argument('-f', '--fps', help="fps for saved video", type=int, default=30)
    parser.add_argument('-s', '--saveFile', help="file name (without extension) where data is to be saved ", type=str, default="save")
    parser.add_argument('-l', '--lang', help="tesseract language (default 'eng')", type=str, default="eng")

    args = parser.parse_args()
    if (args.image):
        ocr.Image(args.image, args.saveFile, args.lang)
    elif args.video:
        ocr.Video(args.video, args.saveFile, args.fps, args.lang)
    else:
        ocr.Video(args.camera , args.saveFile, args.fps, args.lang)

if __name__ == '__main__':
    main()