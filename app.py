from flask import Flask, redirect, request
from flask import render_template, send_file #send_file未使用
import os, json # json未使用
import uuid
from tinydb import where, TinyDB
import boto3
#自分が作ったモジュール
from gazou_check import extension_check
from  method_for_s3 import list_files, download_file, upload_file, download_json


app = Flask(__name__)

BASE_DIR = os.path.dirname(__file__) #print(BASE_DIR) #>>c:\Users\CALIFORNIA\Desktop\このディレクトリ名
Tiny_json = BASE_DIR + "/data/data.json" 

#画像表示に使う
IMAGES_URL = BASE_DIR + "/static/userimage/"
#投稿データ 8MB以上は受け付けない
app.config["MAX_CONTENT_LENGTH"] = 1024 * 1024 * 8
#s3
BUCKET = "oyoyo6464"




#画像は任意　入口で名前を書く
@app.route("/")
def index():
    return render_template("index.html")
    

#画像get&問題作成画面_1
@app.route("/upload",methods=["POST"])
def upload():
    #upされた画像を取得
    upfile_get = request.files.get("upfile",None)
    
    #拡張子を選別する　jpg png gif以外は断る
    if not upfile_get.filename == "":
        if not extension_check(upfile_get.stream):
            return render_template("msg.html",message="アップロードできる拡張子はgif,jpeg,pngのみです",message2="お手数ですがもう一度やり直してください")


    #名前と画像（なかったら""で保存）
    meta  = {
        "p_name":request.form.get("name","名無しさん"),
        "p_filename":upfile_get.filename,
    }
    #URL 作成　uuid でユニークなIDを生成
    random_id = "FS_" + uuid.uuid4().hex
    meta["id"] = random_id
    

    #上記2点(2点)json形式で保存
    download_json(BUCKET)
    db = TinyDB(Tiny_json) #jsonファイル作る
    db.insert(meta)
    upload_file("data/data.json", BUCKET)

    #uｐfilenameが""でなければ画像ファイルそのものを保存する
    if not upfile_get.filename == "":
        #upされたfileをstatic/userimageに保存　ファイルの名前はid+元ファイル名
        upfile_name = random_id + upfile_get.filename
        upfile_get.save(IMAGES_URL + "/" + upfile_name)
        #s3に保存
        upload_file(f"static/userimage/{upfile_name}", BUCKET)

    return render_template("quiz_creation_1.html",meta=meta,id=meta["id"])



#1問目の投稿を受けるページ2問目
@app.route("/upload_2/<id>",methods=["POST"])
def upload_2(id):
    db = TinyDB(Tiny_json)
    
    #①質問内容
    q_1  = {
        "p_question":request.form.get("question","質問問題1"),
        "p_option_1":request.form.get("option_1","質問１"),
        "p_option_2":request.form.get("option_2","質問２"),
        "p_option_3":request.form.get("option_3","質問３"),
        "p_option_4":request.form.get("option_4","質問４"),
        "correct_answer":request.form.get("radio"),
        "question_count":1
    }
    db.update(q_1,where("id") ==id)#idが一致したらデータをついか
    upload_file("data/data.json", BUCKET)
    meta = db.get(where("id") ==id)

    make_url = request.host_url + "download/" + meta["id"]
    return render_template("quiz_creation_2.html",meta=meta,url = make_url,id=meta["id"])


#2問目の投稿を受けるページ3問目
@app.route("/upload_3/<id>",methods=["POST"])
def upload_3(id):
    db = TinyDB(Tiny_json)
    
    #質問内容
    q_2  = {
        "p_question_2":request.form.get("question_2","質問問題"),
        "p_option_1_2":request.form.get("option_1_2","質問１"),
        "p_option_2_2":request.form.get("option_2_2","質問２"),
        "p_option_3_2":request.form.get("option_3_2","質問３"),
        "p_option_4_2":request.form.get("option_4_2","質問４"),
        "correct_answer_2":request.form.get("radio_2"),
        "question_count":2
    }
    db.update(q_2,where("id") ==id)#idが一致したらデータを更新
    upload_file("data/data.json", BUCKET)
    meta = db.get(where("id") ==id)

    make_url = request.host_url + "download/" + meta["id"]
    return render_template("quiz_creation_3.html",meta=meta,url = make_url,id=meta["id"])


#3問目の投稿を受けるページもう終わり！
@app.route("/upload_4/<id>",methods=["POST"])
def upload_4(id):
    db = TinyDB(Tiny_json)
    
    #質問内容
    q_3  = {
        "p_question_3":request.form.get("question_3","質問問題"),
        "p_option_1_3":request.form.get("option_1_3","質問１"),
        "p_option_2_3":request.form.get("option_2_3","質問２"),
        "p_option_3_3":request.form.get("option_3_3","質問３"),
        "p_option_4_3":request.form.get("option_4_3","質問４"),
        "correct_answer_3":request.form.get("radio_3"),
        "question_count":3
    }

    db.update(q_3,where("id") ==id)#idが一致したらデータを更新
    upload_file("data/data.json", BUCKET)
    meta = db.get(where("id") ==id)

    make_url = request.host_url + "download/" + meta["id"]
    return render_template("quiz_creation_4.html",message="ok",meta=meta,url = make_url,id=meta["id"])






#---------------------------------------------------------------------------------------#
#問題に答えるページに飛ぶ権利があるかジャッジ 直接URLで来る
@app.route("/download/<id>")
def download(id):#<id>　が引数として入る

    download_json(BUCKET)
    db = TinyDB(Tiny_json)
    meta = db.get(where("id") ==id)#jsonに入ってるidと一緒のデータをdictで取ってくる
    if meta == None:
        return render_template("msg.html",message = "エラーが発生しました",message2="お手数ですがもう一度やり直してください")
    else:
        return render_template("answer_person.html",meta=meta,id=id)



#正解不正解分岐するページ
@app.route("/answer/<id>",methods=["POST"])
def answer(id):
    #正解数カウント
    c_a_count = 0
    #ご褒美ページに飛べるか
    g_mode = False

    #まず投稿者のデータを引っ張ってくる(答え合わせ)
    download_json(BUCKET)
    db = TinyDB(Tiny_json)
    meta = db.get(where("id") == id)




    #答え合わせ第一問
    #ユーザーの答えそのもの
    user_answer_1 = request.form.get("radio")#例"{{meta.p_option_1}}"等の文字が入る
    #投稿者が指定した答えでキーを作る
    kotae_key1 = "p_option_"+ meta["correct_answer"] #"p_option_2"みたいなのができる
    #投稿者の答えそのもの
    kotae_1 = meta[kotae_key1] 
    if kotae_1 == user_answer_1:#答えそのもの==答えそのもの("例{{meta.p_option_1}}")
        c_a_count += 1

    #答え合わせ第二問
    #ユーザーの答えそのもの
    if meta["question_count"] >= 2:
        user_answer_2 = request.form.get("radio_2")
        #投稿者が指定した答えでキーを作る
        kotae_key2 = "p_option_"+ meta["correct_answer_2"] +"_2"
        #投稿者の答えそのもの
        kotae_2 = meta[kotae_key2] 
        if kotae_2 == user_answer_2:
            c_a_count += 1
    else:
        kotae_2 = None
        user_answer_2 = None

    #答え合わせ第三問
    #ユーザーの答えそのもの
    if meta["question_count"] >= 3:
        user_answer_3 = request.form.get("radio_3")
        #投稿者が指定した答えでキーを作る
        kotae_key3 = "p_option_"+ meta["correct_answer_3"] +"_3"
        #投稿者の答えそのもの
        kotae_3 = meta[kotae_key3] 
        if kotae_3 == user_answer_3:
            c_a_count += 1
    else:
        kotae_3 = None
        user_answer_3 = None
    
    gohoubi_judge = c_a_count/meta["question_count"] #60%以上ならご褒美
    #これがご褒美URL
    make_url1 = request.host_url + "gohoubi/" + id
    #6割正解ならご褒美モード
    if gohoubi_judge >= 0.6:
        g_mode = True
    return render_template("passed_person.html",meta=meta,id=id,make_url = make_url1,
                            kotae_1=kotae_1,user_answer_1=user_answer_1,
                            kotae_2=kotae_2,user_answer_2=user_answer_2,
                            kotae_3=kotae_3,user_answer_3=user_answer_3,
                            c_a_count = c_a_count,
                            g_mode = g_mode,
                            gohoubi_judge = gohoubi_judge
                            )


#ご褒美ルート たどり着けた
@app.route("/gohoubi/<id>",methods=["POST"])
def gohoubi(id):

    download_json(BUCKET)
    db = TinyDB(Tiny_json)
    meta = db.get(where("id")==id)

    #s3
    file_path = f"static/userimage/{meta['id']}{meta['p_filename']}"
    download_file(file_path,BUCKET)


    if not meta["p_filename"] =="":
        gazou_arinasi = meta["p_filename"]
    else:
        gazou_arinasi = None
    return render_template("gohoubi.html",message="ご褒美画像",meta=meta,gazou=gazou_arinasi)




##以下エラーハンドリング
#404エラー
@app.errorhandler(404)
def app_notfound(e):
    return render_template("msg.html",message="存在しないページです",message2=e)

#送信ファイルサイズがnMBを超えたときのエラー ※家ではうまくいかない
@app.errorhandler(413)
def app_gazousippai(e):
    return render_template("msg.html",message="アップロードできるファイルサイズは8MB以下です",message2=e)


#405 POSTしてないのにリンク更新しちゃったときとか
@app.errorhandler(405)
def app_405(e):
    return render_template("msg.html",message="エラーが発生しました",message2=e)


#CSSの練習
@app.route("/rensyu")
def rensyu():
    return render_template("b_rensyu_common.html")





if __name__ == "__main__":
    # app.run(host="0.0.0.0")
    app.run(host="0.0.0.0",debug=True)
