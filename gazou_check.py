

#xにはupファイルのバイナリデータを代入する
def extension_check(x):
    #with open(x,"rb") as f:
        #a = f.read(5)
        #print(a)
        a = x.read(5)
        x.seek(0)
        if  "PNG" in str(a):
            #print("png")
            return True
        elif "GIF" in str(a):
            #print("gif")
            return True
        elif "xff\\xd8" in str(a):
            #print("jpg")
            return True
        else:
            #print("gif,png,jpegではない")
            return False


# if __name__ == "__main__":
#         #テスト
#     y = b'\xff\xd8\xff\xe0\x00'
#     if extension_check(y):
#         print("ｔ")
#     else:
#         print("f")