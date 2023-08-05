# Propor

## 介绍
项目传输（支持文件夹，仅支持传输到 MacOS、Linux）

## 安装
```
pip3 install propor
```

## 使用
- 进入需要传输的项目目录输入命令
```
D:\Project\> propor host to_path  # propor 192.168.0.1 index
```
- `Project`：需要传输的项目目录
- `host`：远程主机地址
- `to_path`：传输到指定目录（可为空，默认为‘./’）
- 在程序中可以通过 `from propor import transfer_file` 导入方法