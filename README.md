<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/header-dark.svg">
  <img src="assets/header-light.svg" alt="PlainZH · 中文清晰写作。让读者看懂，也知道怎么用。" width="1200">
</picture>

**给 Agent 的中文写作技能。** 起草、改写和审阅回复、说明、方案与汇报，按读者需要组织内容，保留事实和原意。

[开始使用](#开始使用)　 /　 [看看改写](#看看改写)　 /　 [案例精选](showcase/README.md)　 /　 [技能全文](SKILL.md)

## 开始使用

通过 [Skills CLI](https://github.com/vercel-labs/skills) 安装到支持的 Agent：

```sh
npx skills add Cmoon-cyl/plainzh
```

提供材料，告诉 Agent 写给谁、用来做什么：

```text
用 $plainzh 改写这份进展说明。
写给刚接手的同事，让他看清：
改了什么，验证了什么，
还有哪些问题。

[粘贴原文或提供文件]
```

也可以说「只润色，保留结构」「重写成可独立阅读的说明」，或「后续按 PlainZH 的原则回复我」。默认交付正文，需要修改说明或 diff 时再提出。

<details>
<summary>手动安装到 Codex</summary>

```sh
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
git clone https://github.com/Cmoon-cyl/plainzh.git \
  "${CODEX_HOME:-$HOME/.codex}/skills/plainzh"
```

安装后新开会话或重新加载技能。已有同名目录时，先保留自己的修改。

</details>

## 看看改写

同事想知道登录问题修到了哪一步。这段演示保留变更、测试结果和未验证范围，把它们从层层铺垫中提出来。

**改写前**

> 本次迭代聚焦登录流程的稳定性建设，围绕超时场景下的异常处理能力进行了针对性优化。通过修复重试逻辑，我们进一步夯实了登录链路的可靠性基础。目前，相关单元测试已全部通过，端到端验证尚未开展，后续仍需结合完整流程确认实际效果。

**改写后**

> 已修复登录超时后的重试逻辑，相关单元测试全部通过。端到端测试还没做，完整登录流程的实际效果仍需验证。

遇到复杂内容，改写也可能增加篇幅：补上已有的背景，拆开条件，解释清楚关系。下面五个案例各展示一种用途。

| 你要写什么 | 看这个案例 |
|---|---|
| 让同事找到入口、辨别状态 | [月报说明：根据反馈改到具体位置](showcase/reader-feedback.md) · 1.0.4 实际模型输出 |
| 让负责人掌握进展和发布条件 | [项目周报：已审核，还没有发布](showcase/weekly-update.md) |
| 让开发者查找实现规则 | [技术方案：未知结果、超时和取消](showcase/technical-proposal.md) |
| 让读者理解故障原因 | [故障分析：为什么压缩后又触发压缩](showcase/incident-analysis.md) |
| 让用户了解功能和适用范围 | [产品介绍：生成建议之后还要做什么](showcase/product-update.md) |

除标明的实际模型输出外，案例均为编辑整理的演示稿；每页提供原稿、修改说明和事实核对。[查看案例来源与验证范围](showcase/README.md#这些案例能说明什么)。

## 写作依据

以 **ISO 24495-1:2023** 的四项清晰语言原则为框架：

| 原则 | 写作时关注的问题 |
|---|---|
| 内容切合需要 | 读者要理解、判断或完成什么？必要的事实、条件和限制是否齐全？ |
| 容易找到 | 读者会怎样查找？标题、顺序和图表是否帮助定位？ |
| 容易理解 | 背景和关系是否说清？是否要靠猜测才能理解？ |
| 能够使用 | 读者能否用这些信息解决问题？发现问题后怎样修改并再次检查？ |

四项原则贯穿写作与修改。PlainZH 要求核对遗漏和新增事实，保留术语、数字、状态、条件与承诺；技术表达还参考 **ASD-STE100** 的名称一致、条件先行和操作关系等方法。

模型回读属于文本自查，实际阅读效果需要读者反馈或使用证据。PlainZH 是中文写作实践，不是标准译本或合规认证，也不把英语受控词表和单词数限制套到中文。

[信息组织](references/information-design.md) · [技术写作](references/technical-writing.md) · [保真边界](references/examples.md) · [来源与适用范围](references/sources.md)

## 帮它改得更好

改写漏了条件、改变了原意，或读起来仍然费劲？欢迎提交 [Issue](https://github.com/Cmoon-cyl/plainzh/issues)，附上原文、改稿、目标读者和卡住的地方。请先去掉敏感信息。

[MIT License](LICENSE)
