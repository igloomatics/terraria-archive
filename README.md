# Terraria 国服/国际服存档转换器

一个纯浏览器端的 Terraria 存档签名转换工具。电脑端和国际服按同一类处理：国服使用 `xindong`（十六进制 `78 69 6E 64 6F 6E 67`），国际服 / 电脑端使用 `relogic`。人物 `.plr` 使用 AES-128-CBC 加密，网页会用 Terraria 固定的 UTF-16LE 密钥/IV `h3y_gUyZ` 解密、替换后再加密，并下载转换后的副本。

电脑端与国际服在签名层面相同，因此这两个方向会校验文件后原样导出；这不代表不同游戏版本之间一定兼容。跨平台时应尽量保持游戏版本一致，并同时迁移对应的 `.wld/.plr` 备份文件。

文件只在浏览器内处理，不会上传服务器。请先备份原存档。

## 在线使用

部署到 GitHub Pages 后，打开仓库的 Pages 地址即可使用。网页入口是 https://igloomatics.github.io/terraria-archive/ 。

## 本地使用

```bash
python3 terraria_converter.py serve
```

然后打开 <http://127.0.0.1:8765/index.html>。

命令行转换（适用于未加密的地图文件）：

```bash
python3 terraria_converter.py convert 地图.wld -o 地图国际.wld
```

人物 `.plr` 请使用网页入口；命令行脚本保持为简单的原位替换工具，不会尝试把加密的人物文件当作明文处理。


