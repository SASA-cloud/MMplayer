from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # 主界面（播放器界面）
    path('inputMedia', views.inputMedia, name='inputMedia'),  # 上传本地媒体
    path('playMedia', views.playMedia, name='playMedia'),  # 播放媒体
    path('formatChange', views.formatChange, name='formatChange'),  # 格式转换页面
    path('inputImgToTransform', views.input_img_to_transform, name='inputImgToTransform'),  # 图片文件格式转换
    path('downLoadFile/<str:dirName>/<str:rqType>', views.downLoadFile, name='downLoadFile'),  # 下载文件
    path('inputVideoToAudio', views.input_video_to_audio, name='inputVideoToAudio'),  # 视频转音频
    path('inputImgToResize', views.input_img_to_resize, name='inputImgToResize'),  # 图片大小修改
    # path('playMedia')
    # path('streamMedia', views.streamMedia, name='streamMedia'),  # 流媒体
    # path('findMusic', views.findMusic, name='findMusic'),
]
