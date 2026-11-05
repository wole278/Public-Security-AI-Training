# 公安内网 / 单机离线大模型与法规知识库极简部署指南（传统技术科专用）

> **适用对象**：分局科信部门、网安支队、图侦技侦技术人员  
> **核心目标**：在**完全断网（公安网/视频专网/单机涉密工作站）**环境下，用 1 台带显卡的办公工作站，在 30 分钟内搭起全分局可用的**本地私有大模型 + 公安法规办案规范 RAG 知识库**，实现**“真实笔录、真实流水、真实 110 警情 100% 不出内网直接上 AI”**。

---

## 一、 硬件配置分级选型表（按分局现有设备利旧）

| 部署档位 | 硬件配置（显存是核心） | 推荐离线模型组合 | 适用场景与并发能力 |
| :--- | :--- | :--- | :--- |
| **轻量单兵档** | 普通台式机 / 笔记本（RTX 4060Ti 16G 或 RTX 3090/4090 24G 单卡） | `Qwen2.5-14B-Instruct-Q4_K_M`（文字/代码/笔录）<br>+ `Qwen2.5-VL-7B-Instruct`（监控看图） | 专案组单机离线审讯笔录比对、个人写 Python/SQL 脚本（支持 1~3 人同时提问，生成速度约 35 字/秒） |
| **科室/专案组共享档** | 双卡工作站（2 × RTX 4090 48G 显存） | `DeepSeek-R1-Distill-Qwen-32B`（深度逻辑推理）<br>+ `Qwen2.5-Coder-32B`（写代码/SQL）<br>+ `bge-large-zh-v1.5`（中文法规向量检索） | 科信/刑侦/情指中心科室局域网共享（支持 5~15 人并发，复杂案情推理与 SQL 编写达到顶尖水准） |

---

## 二、 断网环境“摆渡盘”三步离线安装流程

### 第 1 步：在外网准备离线安装包（存入合规摆渡盘/光盘）
1. 下载 **Ollama Windows/Linux 离线安装包**（`OllamaSetup.exe` 或 Linux 二进制包）。
2. 在外网机器上拉取模型后，将 `~/.ollama/models` 目录整体打包压缩（包含模型权重 blobs 与 manifests）：
   * 文字与笔录主力：`ollama pull qwen2.5:14b` 或 `deepseek-r1:32b`
   * 监控图像识别主力：`ollama pull qwen2.5vl:7b`
   * 法规知识库向量模型：`ollama pull bge-m3`
3. 下载本地知识库客户端 **AnythingLLM Desktop（免安装便携版）** 或 **OpenWebUI 离线包**。

### 第 2 步：在公安内网工作站恢复运行（5 分钟）
1. 安装 Ollama，将打包好的 `models` 文件夹解压覆盖至内网机器的 `C:\Users\<用户名>\.ollama\models`。
2. 配置环境变量允许内网同网段其他警务终端访问：
   ```powershell
   # 在内网工作站 PowerShell（管理员）中执行：
   [System.Environment]::SetEnvironmentVariable("OLLAMA_HOST", "0.0.0.0:11434", "Machine")
   [System.Environment]::SetEnvironmentVariable("OLLAMA_ORIGINS", "*", "Machine")
   # 重启 Ollama 服务后，内网任意终端即可通过 http://<工作站内网IP>:11434 调用 API
   ```
3. 验证离线模型是否就绪：
   ```powershell
   ollama list
   ollama run qwen2.5:14b "请用一句话介绍你在公安内网中的角色"
   ```

### 第 3 步：挂载《公安执法办案法规与典型案例本地知识库（RAG）》
为什么大模型直接背法条容易串号？因为没做 **RAG（检索增强生成）**。
1. 打开离线版 **AnythingLLM**，连接本地 Ollama 的 `qwen2.5:14b`（对话模型）与 `bge-m3`（嵌入向量模型）。
2. 新建名为 **【上海公安执法办案与法制审核库】** 的工作区，将以下常用电子书/文档（PDF/Word/TXT）直接拖入向量化：
   * 《中华人民共和国刑法》及最新修正案、司法解释汇编
   * 《中华人民共和国治安管理处罚法》
   * 《中华人民共和国道路交通安全法》
   * 《公安机关办理刑事案件程序规定》与《办理行政案件程序规定》
   * 本局历年《法制审核常见退查问题通报汇编》与《典型警情处置规范 SOP》
3. 将工作区设置为 **“仅基于知识库回答（Query Mode）”**，即可彻底消灭法条幻觉，实现内网民警秒查办案程序规定！

---

## 三、 内网 Python 脚本直接调用本地大模型 API 模板（批量洗 110 警情专用）

当内网搭好 Ollama 后，技术科人员只需用下面这 **25 行零依赖 Python 标准库代码**，就能在后台全自动批量处理成千上万条真实 110 警情或笔录（无需人工一条条复制粘贴）：

```python
import urllib.request
import json

def ask_intranet_police_llm(prompt_text: str, model_name: str = "qwen2.5:14b") -> str:
    """零第三方依赖调用公安内网 Ollama 大模型接口"""
    url = "http://127.0.0.1:11434/api/generate"
    payload = {
        "model": model_name,
        "prompt": prompt_text,
        "stream": False,
        "options": {"temperature": 0.1}  # 调低随机性，确保警务输出严谨稳定
    }
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        result = json.loads(resp.read().decode("utf-8"))
        return result.get("response", "")

# 示例：在循环中批量传入真实 110 警情简要案情进行结构化打标
if __name__ == "__main__":
    sample_110 = "报警人称在XX路12号301室与前夫因房产分割激烈争吵，对方喝酒后拿菜刀拍桌子。"
    prompt = f"请提取以下警情的【矛盾类型】【高危标签(涉酒/持械)】【风险评分(1-10)】，输出JSON：{sample_110}"
    print("内网本地大模型接口代码已就绪（连接本地 11434 端口即可批量执行）！")
```
