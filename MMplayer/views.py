# Create your views here.
from django.http import JsonResponse,HttpResponse,Http404,FileResponse
from django.shortcuts import render
import time
import os
from django.conf import settings
from . import image_converter
from . import video_to_audio
from . import image_size_change
import json
from django.views.decorators.csrf import csrf_exempt

# 返回后缀对应的mime类型
def mime_type(suffix):
    with open('MMplayer/static/mime.json','r') as f:
        json_data = json.load(f)
        return json_data['.'+suffix]



def index(request):
    with open('MMplayer/static/fileRoute.json', 'r', encoding='utf-8') as f:
        json_data = json.load(f)
        mediaList = list(json_data.keys())

    context = {
        "mediaList":mediaList,
    }
    return render(request,"MMplayer/index.html",context)


# 播放媒体
# 返回媒体路径url
@csrf_exempt  # 屏蔽csrf（不安全）
def playMedia(request):
    if request.method=='POST':
        mediaName = request.POST.get("mediaName")  # 取得媒体名称
        # print(mediaName)
        with open('MMplayer/static/fileRoute.json', 'r', encoding='utf-8') as f:
            json_data = json.load(f)
            mediaUrl=json_data[mediaName]  # 从名字取得媒体路径
            print(mediaUrl)
        return JsonResponse({"mediaUrl":mediaUrl,})


def inputMedia(request):
    if request.method == 'POST':
        media = request.FILES.get("media")  # 取得上传的文件
        old_name = media.name  # 取得文件名
        suffix = old_name.rsplit(".")[1]  # 取得文件名后缀
        new_name = int(time.time())   # 取个时间来命名
        dir = os.path.join(os.path.join(settings.BASE_DIR,'MMplayer/static/media'),str(new_name)+'.'+suffix)  # 文件路径
        destination = open(dir,'wb+')  # 创建这个文件
        for chunk in media.chunks():  # 写入文件夹
            destination.write(chunk)
        destination.close()

        mediaRoute = dir
        mediaName=str(new_name)+'.'+suffix
        print(dir)
        return JsonResponse({"mediaRoute":mediaRoute,"mediaName":mediaName})



def formatChange(request):
    # directoryRoute={}
    # context={
    #     "backData":directoryRoute
    # }
    return render(request, "MMplayer/formatChange.html")


def input_img_to_transform(request):
    if request.method == 'POST':
        media = request.FILES.get("media")  # 取得上传的文件
        old_name = media.name  # 取得文件名
        suffix = old_name.rsplit(".")[1]  # 取得文件名后缀
        directory_name = int(time.time())  # 取个时间来命名
        dir = os.path.join(os.path.join(settings.BASE_DIR, 'MMplayer\\static\\media'),str(directory_name))
        os.mkdir(dir)  # 新建文件夹

        # 储存上传的文件
        file = os.path.join(dir, media.name)  # 文件名
        destination = open(file, 'wb+')  # 创建这个文件
        for chunk in media.chunks():  # 写入文件夹
            destination.write(chunk)
        destination.close()

        image_converter.image_converter(dir)  # 格式转换 png转jpg jpg转png

        context = {  # 返回给前端的json信息
            "directoryRoute": str(directory_name),
        }
        return JsonResponse(context)


#上传 video 转 audio
def input_video_to_audio(request):
    if request.method == 'POST':
        directory_name,old_name = save_file(request) # 将前端上传的文件先保存到服务器上
        out_type = "mp3"  # 以mp3格式输出转换好的文件
        dir = os.path.join(os.path.join(settings.BASE_DIR, 'MMplayer\\static\\media'), str(directory_name)) # 转换文件
        video_to_audio.ffmpeg_VideoToAudio(dir,out_type)  # 视频转音频 out_type 是输出的audio格式

        context = {  # 返回给前端的json信息
            "directoryRoute": str(directory_name),  # 转换好的文件的地址
        }
        return JsonResponse(context)

def input_img_to_resize(request):
    if request.method == 'POST':
        directory_name,old_name = save_file(request)
        width = int(request.POST.get("width"))
        height = int(request.POST.get("height"))

        # suffix = old_name.rsplit(".")[1]  # 取得文件名后缀
        dir = os.path.join(os.path.join(settings.BASE_DIR, 'MMplayer\\static\\media'), directory_name) # 输入文件夹绝对地址

        image_size_change.image_size_change(dir,height,width)

        context = {  # 返回给前端的json信息
            "directoryRoute": str(directory_name),
        }
        return JsonResponse(context)


def downLoadFile(request,dirName,rqType):
    if(rqType=="1"):  # 下载转换好的图片
        return downLoadimg(request,dirName)
    elif(rqType=="2"):  # 下载转换好的音频
        return downLoadaudio(request,dirName)
    elif(rqType=="3"):  # 下载改好形状的图片
        return downLoadRSimg(request,dirName)


def downLoadRSimg(request,dirName):
    dir = os.path.join(os.path.join(settings.BASE_DIR, 'MMplayer\\static\\media'), dirName+'\\resize')  # 取得目标文件夹路径
    audio_list = os.listdir(dir)
    audiofiles = [os.path.join(dir, x) for x in audio_list] # 取得文件绝对路径
    if len(audiofiles):
        for i in audiofiles:
            suffix = i.rsplit(".")[1]  # 取得文件名后缀
            with open(i,'rb') as f:
                try:
                    response = HttpResponse(f.read())
                    response['content_type'] = mime_type(suffix)
                    response['Content-Disposition'] = 'attachment; filename=img.'+suffix
                    return response
                except Exception:
                    raise Http404("file does not exist")


def downLoadaudio(request,dirName):
    dir = os.path.join(os.path.join(settings.BASE_DIR, 'MMplayer\\static\\media'), dirName+'\\audio')  # 取得audio文件夹路径
    # 取得文件名列表
    audio_list = os.listdir(dir)
    audiofiles = [os.path.join(dir, x) for x in audio_list] # 取得文件绝对路径
    if len(audiofiles):
        for i in audiofiles:
            suffix = i.rsplit(".")[1]  # 取得文件名后缀
            with open(i,'rb') as f:
                try:
                    response = HttpResponse(f.read())
                    response['content_type'] = mime_type(suffix)
                    response['Content-Disposition'] = 'attachment; filename=audio.'+suffix
                    return response
                except Exception:
                    raise Http404("file does not exist")



def downLoadimg(request,dirName):
    jpg_dir = os.path.join(os.path.join(settings.BASE_DIR, 'MMplayer\\static\\media'), dirName+'\\jpg')  # 取得jpg文件夹路径
    png_dir = os.path.join(os.path.join(settings.BASE_DIR, 'MMplayer\\static\\media'), dirName+'\\png')  # 取得jpg文件夹路径

    #取得文件名列表
    jpg_list= os.listdir(jpg_dir)
    png_list= os.listdir(png_dir)

    jpgfiles = [os.path.join(jpg_dir, x) for x in jpg_list if x.endswith('.jpg') or x.endswith('.jpeg')]
    pngfiles = [os.path.join(png_dir, x) for x in png_list if x.endswith('.png')]
    files=jpgfiles+pngfiles

    if len(files):
        for i in files:
            with open(i,'rb') as f:
                try:
                    response = HttpResponse(f.read())
                    suffix = i.rsplit(".")[1]  # 取得文件名后缀
                    response['content_type'] = mime_type(suffix)
                    response['Content-Disposition'] = 'attachment; filename=img.'+suffix
                    return response
                except Exception:
                    raise Http404("file does not exist")


# def return_file(fileNameList):
#     if len(files):
#         for i in files:
#             with open(i,'rb') as f:
#                 try:
#                     response = HttpResponse(f.read())
#                     suffix = i.rsplit(".")[1]  # 取得文件名后缀
#                     response['content_type'] = mime_type(suffix)
#                     response['Content-Disposition'] = 'attachment; filename=img.'+suffix
#                     return response
#                 except Exception:
#                     raise Http404("file does not exist")




# 储存用户上传的文件并生成一个文件夹储存进里面
# 返回文件夹路径,文件名(不带路径）
def save_file(request):
    media = request.FILES.get("media")  # 取得上传的文件
    old_name = media.name  # 取得文件名
    directory_name = int(time.time())  # 取个时间来命名文件夹
    dir = os.path.join(os.path.join(settings.BASE_DIR, 'MMplayer\\static\\media'), str(directory_name))
    os.mkdir(dir)  # 新建文件夹

    # 储存上传的文件
    file = os.path.join(dir, media.name)  # 文件名
    destination = open(file, 'wb+')  # 创建这个文件
    for chunk in media.chunks():  # 写入文件夹
        destination.write(chunk)
    destination.close()

    return str(directory_name),old_name
