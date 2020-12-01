#encoding:utf-8

import requests
import base64
import time
import urllib
import base64
import json

from PIL import Image
import numpy as np

import cv2
#client_id 为官网获取的AK， client_secret 为官网获取的SK
client_id = 'QfowbVxCoywxnpHVdVeouc56'
client_secret = 'rmuG3DAIdFk3f1fSMb3Y3vzLQo8CA8m0'


#获取token
def get_token():
    host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=' + client_id + '&client_secret=' + client_secret
    request = urllib.request.Request(host)
    request.add_header('Content-Type', 'application/json; charset=UTF-8')
    response = urllib.request.urlopen(request)
    token_content = response.read()
    if token_content:
        token_info = json.loads(token_content)
        token_key = token_info['access_token']
    return token_key





def draw_bodys(originfilename,bodys,resultfilename,pointsize):
    from PIL import Image, ImageDraw

    image_origin = Image.open(originfilename)
    draw =ImageDraw.Draw(image_origin)

    for body in bodys:
    
        for body_part in body['body_parts'].values():
            #print(body_part)
            draw.ellipse((body_part['x']-pointsize,body_part['y']-pointsize,body_part['x']+pointsize,body_part['y']+pointsize),fill = "blue")
        gesture = body['location'] 
        draw.rectangle((gesture['left'],gesture['top'],gesture['left']+gesture['width'],gesture['top']+gesture['height']),outline = "red")

    image_origin.save(resultfilename, "JPEG")



#人体识别
#filename:原图片名（本地存储包括路径）
def body_analysis(filename,resultfilename,pointsize):
    request_url = 'https://aip.baidubce.com/rest/2.0/image-classify/v1/body_analysis'
    print(filename)
    # 二进制方式打开图片文件
    f = open(filename, 'rb') #jpg
    #f = filename   #frame
    img = base64.b64encode(f.read())

    params = dict()
    params['image'] = img
    params = urllib.parse.urlencode(params).encode("utf-8")
    #params = json.dumps(params).encode('utf-8')

    access_token = get_token()
    begin = time.perf_counter()
    request_url = request_url + "?access_token=" + access_token
    request = urllib.request.Request(url=request_url, data=params)
    request.add_header('Content-Type', 'application/x-www-form-urlencoded')
    response = urllib.request.urlopen(request)
    content = response.read()
    end = time.perf_counter()

    print('处理时长:'+'%.2f'%(end-begin)+'秒')
    if content:
        #print(content)
        content=content.decode('utf-8')
        print(content)
        data = json.loads(content)
        
        #print(data)
        #print(data)
        result=data['person_info']
    
        draw_bodys(filename,result,resultfilename,pointsize)



if __name__ == '__main__':

    
    # Step 2. 打开摄像头
    #captuer = cv2.VideoCapture(0)
    captuer = cv2.VideoCapture(1)
    #参数设置
    captuer.set(3,480)#视频每一帧的宽
    captuer.set(4,320)#视频每一帧的高
    # Step 4. 创建一个窗口
    cv2.namedWindow(u"摄像头")

     # Step 5. 实时检查摄像头
    while  True :
        # 5.1 读取摄像头图片
        ret , frame = captuer.read()
        #frame就是每一帧的图像，是个三维矩阵
        #s = base64_data.decode()
        # 5.2 将图片转换为灰色图
        #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # 5.2 显示图片
        if(ret) : 
            
            resultfilename = 'testafter.jpg'
            pointsize = 5
            #保存图片
            cv2.imwrite("out_cv2.jpg", frame)
            filename = "out_cv2.jpg"

            body_analysis(filename, resultfilename, pointsize)
            cv2.waitKey(20)

            fnew = cv2.imread(resultfilename)
            cv2.imshow(u"显示图片", fnew)
            
        # 5.3 暂停窗口
        if cv2.waitKeyEx(5) & 0xFF == ord("q") :
            break

    # Step 6. 释放资源
    captuer.release()
    # Step 7. 关闭窗口
    cv2.destroyAllWindows()
    


    '''
    filename = 'test.jpg'
    resultfilename = 'testafter.jpg'
    pointsize = 5
    body_analysis(filename, resultfilename, pointsize)
    '''