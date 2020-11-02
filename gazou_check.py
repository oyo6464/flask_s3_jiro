#画像ファイルのバイナリを出す(gif)
#JPEG	FF D8
#PNG	89 50 4E 47
#GIF	47 49 46 38

#この引数に画像ファイルを入れる
####jpg###
#x="images.jpg"#b'\xff\xd8\xff\xe0\x00\x10JFIF'
#x = "kaeru_2.jpg" #b'\xff\xd8\xff\xee\x00\x0eAdob'
#x = "kaeru.jpg" #b'\xff\xd8\xff\xee\x00\x0eAdob'
#x = "20191005_092254.jpg"

####gif####
#x = "kaeru.gif" #b'GIF89ax\x01|\x01'
#x = "scratch-animgif2-01.gif" #b'GIF89a\x96\x00\xa2\x00'


###png####
#x = "kaeru.png" #b'\x89PNG\r\n\x1a\n\x00\x00'
#x = "kame.Png" #b'\x89PNG\r\n\x1a\n\x00\x00'
#x = "素材.png" #b'\x89PNG\r\n\x1a\n\x00\x00'
#x = "neko1.png" #b'\x89PNG\r\n\x1a\n\x00\x00

###名前だけ拡張子変えてるやつ
#x = "pose_pien_uruuru_woman.gif"#b'\x89PNG\r\n\x1a\n\x00\x00' あってる

###psd###
#x = "29081 (1).psd" #b'8BPS\x00\x01\x00\x00\x00\x00'
#x = "scratch-animgif2-01.gif" #b'GIF89a\x96\x00\xa2\x00'

#xにはupファイルのバイナリデータを代入する
def extension_check(x):
    #with open(x,"rb") as f:
        #a = f.read(5)
        #print(a)
        a = x.read(5)
        x.seek(0)
        if  "PNG" in str(a):
            print("png")
            return True
        elif "GIF" in str(a):
            print("gif")
            return True
        elif "xff\\xd8" in str(a):
            print("jpg")
            return True
        else:
            print("gif,png,jpegではない")
            return False


if __name__ == "__main__":
        #テスト
    y = b'\xff\xd8\xff\xe0\x00'
    if extension_check(y):
        print("ｔ")
    else:
        print("f")
