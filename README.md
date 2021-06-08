# vtk-rendering-server

默认监听容器的5000端口，通过发起一个http请求来执行一个渲染任务

http://localhost:5000/render?data=/path/to/the/directory&script=id-of-the-script

## 实现方案

在 `Linux` 机器上进行离屏渲染，解决各种软件编译的问题非常困难，所以使用了 `paraview` 官方发布的[镜像](https://hub.docker.com/r/kitware/paraview)来避免大量的编译工作。

本应用主要由两部分组成：

1. 渲染脚本部分：根据具体渲染任务编写的命令行工具
2. `web` 部分：用于接收渲染请求，获取数据路径和渲染程序的路径

``` mermaid
graph TD
  client --请求--> web[web部分] --命令行调用--> script[渲染程序] --返回结果--> client
```

### 渲染脚本部分

由于不同业务渲染的参数不一样，我们需要为每个业务编写相应的渲染脚本，通常由 `python` 编写。命令行格式：`/opt/paraview/bin/pvpython {脚本路径} <任务路径>`。在部署的时候，将相应业务的渲染脚本（不放在本代码仓库）挂载到容器中。

### `Web`部分

使用 `flask` 构建，用于对外提供 `web` 服务，接收渲染任务：根据 `data` 和 `script` 参数找到相应的数据路径和渲染脚本，执行一个 `shell` 命令，完成渲染工作。
