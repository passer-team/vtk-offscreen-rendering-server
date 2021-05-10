"""
@author: Xiong Minghua <xiongminghua@zyheal.com>, Daryl.Xu <xuziqiang@zyheal.com>
"""
import vtk
import os
import numpy as np
from vtk.util.numpy_support import vtk_to_numpy,numpy_to_vtk
import json
import copy
import sys


def DataProcess(imageData:vtk.vtkImageData,
                colorTable,
                Opacity,
                niter:int=200)->vtk.vtkActor:
    '''将图像数据转换为多边形数据，并进行平滑处理，最后返回Actor
        参数列表：
            1、imageData：vtk图像数据
            2、colorTable：颜色表包括肝脏和血管的颜色表
            3、niter：平滑迭代次数
    '''
    # 获取标签
    vtkdata=imageData.GetPointData().GetScalars()
    labels=np.delete(np.unique(vtk_to_numpy(vtkdata)),0)
    # 转换为多边形表面数据
    Surface=vtk.vtkAppendPolyData()
    for label in labels:
        #morph=vtk.vtkImageDilateErode3D()
        #morph.SetKernelSize(2,2,2)
        #morph.SetDilateValue(label)
        #morph.SetInputData(imageData)
        #morph.Update()
        contour =vtk.vtkDiscreteMarchingCubes()
        contour.SetInputData(imageData)
        contour.SetValue(0,label)
        contour.ComputeScalarsOn()
        contour.Update()
        # 三角化
        triangles = vtk.vtkTriangleFilter()
        triangles.SetInputData(contour.GetOutput())
        triangles.Update()
        # 对多边形数据进行平滑
        smoothFilter =vtk.vtkSmoothPolyDataFilter()
        smoothFilter.SetInputConnection(triangles.GetOutputPort())
        smoothFilter.SetNumberOfIterations(niter)
        smoothFilter.SetRelaxationFactor(0.05)
        smoothFilter.Update()
        # 计算法向量，平滑效果更加明显
        polynormal=vtk.vtkPolyDataNormals()
        polynormal.SetInputConnection(smoothFilter.GetOutputPort())
        polynormal.SetAutoOrientNormals(1)
        polynormal.Update()
        # 将数据合并
        Surface.AddInputConnection(polynormal.GetOutputPort())
        Surface.Update()
    mapper=vtk.vtkPolyDataMapper()
    actor=vtk.vtkActor()
    scalar=Surface.GetOutput().GetPointData().GetScalars()
    if scalar:
        extent=scalar.GetRange()
    else:
        extent=Surface.GetOutput().GetScalarRange()
    mapper=vtk.vtkPolyDataMapper()
    mapper.SetInputData(Surface.GetOutput())
    mapper.SetScalarRange(extent[0],extent[1])#设置映射范围  
    mapper.SetLookupTable(colorTable)#添加颜色表
    actor.SetMapper(mapper)
    actor.GetProperty().SetOpacity(Opacity)
    # actor.GetProperty().SetBackfaceCulling(1)

    return actor

def ColorTable():
    '''加载颜色表，包括肝脏和血管颜色表'''
    # 读取colormaps.json文件中的颜色表
    # json文件的绝对路径
    jsonFileName=os.path.join(os.path.dirname(__file__),'colormaps.json')
    if os.path.exists(jsonFileName):
        # 打开文件
        with open(jsonFileName,'r') as fpid:
            colorDic=json.load(fpid)
        # 肝脏颜色表字典
        liverColorDic=colorDic['couinaudLabel']
        liverColorDict=copy.deepcopy(liverColorDic)
        # 创建一个颜色表
        lColorTable=vtk.vtkLookupTable()
        lColorTable.SetNumberOfColors(9)
        for i in range(1,10,1):
            colorTableValue=liverColorDict.values()
            colorValue=list(colorTableValue)[i]
            if max(colorValue)>1:
                colorValue[0]/=255
                colorValue[1]/=255
                colorValue[2]/=255
            lColorTable.SetTableValue(i-1,colorValue[0],colorValue[1],colorValue[2],1.0)
        lColorTable.Build()
    else:
        # 创建肝脏数据的颜色映射表
        lColorTable=vtk.vtkLookupTable()
        lColorTable.SetNumberOfColors(9)
        lColorTable.SetTableValue(0,1.0,0.0,0.0,1.0)
        lColorTable.SetTableValue(1,0.0,1.0,1.0,1.0)
        lColorTable.SetTableValue(2,0.0,1.0,0.0,1.0)
        lColorTable.SetTableValue(3,0.0,0.0,1.0,1.0)
        lColorTable.SetTableValue(4,1.0,1.0,0.0,1.0)
        lColorTable.SetTableValue(5,0.8,0.52,0.25,1.0)
        lColorTable.SetTableValue(6,0.0,0.4,1.0,1.0)
        lColorTable.SetTableValue(7,1.0,0.94,0.84,1.0)
        lColorTable.SetTableValue(8,1.0,0,1.0,1.0)
        lColorTable.Build()
    # 加载血管颜色表
    # 读取colormaps.json文件中的颜色表
    # json文件的绝对路径
    jsonFileName=os.path.join(os.path.dirname(__file__),'colormaps.json')
    if os.path.exists(jsonFileName):
        # 打开文件
        with open(jsonFileName,'r') as fpid:
            colorDic=json.load(fpid)
        # 肝脏颜色表字典
        vesselColorDic=colorDic['vesselLabel']
        vesselColorDict=copy.deepcopy(vesselColorDic)
        # 创建一个颜色表
        vColorTable=vtk.vtkLookupTable()
        vColorTable.SetNumberOfColors(7)
        for i in range(1,8,1):
            colorTableValue=vesselColorDict.values()
            colorValue=list(colorTableValue)[i]
            if max(colorValue)>1:
                colorValue[0]/=255
                colorValue[1]/=255
                colorValue[2]/=255
            vColorTable.SetTableValue(i-1,colorValue[0],colorValue[1],colorValue[2],1.0)
        vColorTable.Build()
    else:
        # 创建肝脏数据的颜色映射表
        vColorTable=vtk.vtkLookupTable()
        vColorTable.SetNumberOfColors(7)
        vColorTable.SetTableValue(0,1.0,0.0,0.0,1.0)
        vColorTable.SetTableValue(1,0.0,0.0,1.0,1.0)
        vColorTable.SetTableValue(2,0.0,1.0,0.0,1.0)
        vColorTable.SetTableValue(3,1.0,1.0,0.0,1.0)
        vColorTable.SetTableValue(4,0.0,1.0,1.0,1.0)
        vColorTable.SetTableValue(5,1.0,0.0,1.0,1.0)
        vColorTable.SetTableValue(6,1.0,0.94,0.84,1.0)
        vColorTable.Build()
    return lColorTable,vColorTable

def Render2Image(InputDir:str,
                SavePicName:str,
                SaveDir:str=os.path.dirname(__file__),
                opacity:list=[0.3,1.0],
                backgroundColor:list=[0.925,0.925,0.925],
                winSize:int=600):
    '''
    该函数用于将多边形数据进行后台渲染,并保存为PNG格式的图像文件。
    
    输入参数：
    
        1、InputDir:输入图像数据的目录
        2、SaveDir：图片的存储路径
        3、opacity:保存图像时肝脏分段的透明度,列表类型，长度为2，
            第一位为肝脏奎诺分段的透明度，第二位为血管数据的不透明度。
        4、backgroundColor:保存图像时的图像背景，列表类型
        5、winSize:保存图像时的图像尺寸

    usage：
        Liver2Image(savepath,surfaceData,vesselData)
    '''
    # 设置默认参数
    vesselFileName='mDIXON-All_vessel_label.nii.gz'
    couinaudFileName='mDIXON-All_couinaud.nii.gz'
    # 绝对路径
    couinaudFilePath=os.path.join(InputDir,couinaudFileName)
    vesselFilePath=os.path.join(InputDir,vesselFileName)
    # 判断两个文件是否同时存在
    if not os.path.exists(vesselFilePath) :
        raise IOError(vesselFilePath+' does not exist.')
    if  not os.path.exists(couinaudFilePath):
        raise IOError(couinaudFilePath+' does not exist.')
    # 判断存储路径是否存在
    if not os.path.exists(SaveDir):
        os.makedirs(SaveDir)
    # 加载数据
    # 1、加载血管数据
    vReader=vtk.vtkNIFTIImageReader()
    vReader.SetFileName(vesselFilePath)
    vReader.Update()
    vesselData=vReader.GetOutput()
    # 2、加载肝脏数据
    lReader=vtk.vtkNIFTIImageReader()
    lReader.SetFileName(couinaudFilePath)
    lReader.Update()
    liverData=lReader.GetOutput()
    # 数据可视化
    # 设置渲染窗口
    renwin=vtk.vtkRenderWindow()
    renderer=vtk.vtkRenderer()
    aCamera = vtk.vtkCamera()
    # 加载颜色表
    liverColorTable,vesselColorTable=ColorTable()
    vesselActor=DataProcess(vesselData,vesselColorTable,opacity[1],niter=100)
    renderer.AddActor(vesselActor)
    liverActor=DataProcess(liverData,liverColorTable,opacity[0],niter=300)
    renderer.AddActor(liverActor)
    renderer.SetBackground(backgroundColor)
    renwin.AddRenderer(renderer)
    renwin.SetSize(winSize, winSize)#设置窗口大小
    renwin.OffScreenRenderingOn()
    renwin.SetPolygonSmoothing(1)
    # 设置相机视角、焦点、位置等参数
    aCamera.SetViewUp(0, 0, 1)#调整摄像机的顶部的方向
    aCamera.SetPosition(-0.2, -0.4, 0.7)#位置
    aCamera.SetFocalPoint(0, 0, 0)#焦点
    renderer.SetActiveCamera(aCamera)#激活相机
    renderer.ResetCamera()
    renwin.Render()#开始渲染
    wif =vtk.vtkWindowToImageFilter()
    wif.SetInput(renwin)
    wif.SetInputBufferTypeToRGB()
    wif.SetScale(1)
    wif.ReadFrontBufferOff()
    wif.Update()
    saveAbsPath=os.path.join(SaveDir,SavePicName)

    os.makedirs(os.path.dirname(saveAbsPath), exist_ok=True)
    
    # 直接将渲染结果保存为PNG格式的图像
    writer =vtk.vtkPNGWriter()
    writer.SetFileName(saveAbsPath)
    writer.SetInputConnection(wif.GetOutputPort())
    writer.Write()

def Execute(argv):
    '''运行渲染程序'''
    # 设置初始保存文件名    
    vesselSaveFileName='Figure/volume-skeleton-vessel.png'
    liverSaveFileName='Figure/volume-overview-liver.png'
    InputDict=argv[1]
    OutputDict=argv[2]
    Render2Image(InputDict,vesselSaveFileName,OutputDict,opacity=[0,1.0])
    Render2Image(InputDict,liverSaveFileName,OutputDict)


if __name__=='__main__':
    '''用法：
        # 指定文件路径，存储路径
        fileDict='E:/ZhiYu/Seafile/tempfolder/SeveLiverData2/01200516V001'
        saveDict='E:/ZhiYu/Seafile/tempfolder/SeveLiverData2/01200516V001'
        Execute(fileDict,saveDict)
    
    '''
    Execute(sys.argv)


