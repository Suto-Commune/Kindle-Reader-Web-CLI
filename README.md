一键运行：`python main.py`

kindle端: http://IP:5000

web端: http://IP:8080

---

如何部署：
```
pip install -r requirements.txt
start.bat

```
or [使用docker](https://hub.docker.com/repository/docker/lolingnatsumi/kindle-reader-web-cli/general)

---

在[render](https://dashboard.render.com/)中部署：

1. 注册后选择新建`Web Service`


![image](https://user-images.githubusercontent.com/63963655/213427406-1780a1c8-480a-43f4-822b-4c1379532ef8.png)

2. 翻到下面的`Public Git repository`,填入`https://github.com/Suto-Commune/Kindle-Reader-Web-CLI/`,然后点击`Continue`



![image](https://user-images.githubusercontent.com/63963655/213428040-af80a7b1-9d89-4ead-81a7-941ac846587d.png)

3. 填入名称（想填什么填什么）


![image](https://user-images.githubusercontent.com/63963655/213428416-c61f9ecd-415c-4643-bf95-eda10b1ec8bf.png)

4. 选择节点

![image](https://user-images.githubusercontent.com/63963655/213428503-bc47f6af-ed1a-4a07-a044-1826ab5e932a.png)

5. 拉到`Environment`选择`Docker`


![image](https://user-images.githubusercontent.com/63963655/213428709-b14667fb-cba1-47f6-aaef-2e702ba9fe14.png)

6.  点击`Create Web Service'


![image](https://user-images.githubusercontent.com/63963655/213428841-891c8802-9e92-42b1-b298-d65cc4f3ac6a.png)

7. 点击`Environment`，点击`Add Environment Variable`

8. `KEY`填写`PORT`,`value`填写`80`,填写完毕点击`Save Changes`


![image](https://user-images.githubusercontent.com/63963655/213429546-1fa1e2bc-ddb2-4a3a-956a-3bc98be75c0e.png)

9. 拉到最上面，下图中框选的地方就是部署的地址，访问即可


![image](https://user-images.githubusercontent.com/63963655/213429617-6fad7e1c-f3c1-4a66-9b3a-de9d5c4ed338.png)

说明:
```
http://你的地址/reader #reader服务端的地址
http://你的地址/ #kindle客户端地址
```

注意！第一次进入reader服务端的地址可能会报错，请把
`//你的地址/reader3`
改为
`//你的地址/reader/reader3`

在下图中红色框选的位置设置

![image](https://user-images.githubusercontent.com/63963655/213430327-00319e48-92d4-43bd-854b-d28329f86caa.png)
