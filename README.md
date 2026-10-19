<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/header-dark.svg">
  <img src="assets/header-light.svg" alt="PlainZH · 中文清晰写作：把话写清楚。" width="1200">
</picture>

<p align="center">让 Agent 回复、开发说明、模型答疑和工作汇报更清楚、更自然。</p>
<p align="center"><a href="#改写效果">看改写效果</a>　 /　 <a href="#安装与使用">安装使用</a>　 /　 <a href="#写作方法">了解方法</a>　 /　 <a href="SKILL.md">阅读 Skill</a></p>

PlainZH 是一套中文写作 Skill，适合日常与 Agent 协作时的回复和文档。它根据读者要理解、判断或完成的事选取和组织信息，写清依据、条件和限制，让内容足以支持当前用途。

改写会保留事实、术语、条件和必要的分寸。技术说明保持准确，工作汇报照顾沟通场合，已经清楚的句子可以不改。

## 改写效果

### 开发迭代：写清改了什么、验证了什么

<table>
<tr><th width="50%">改写前</th><th width="50%">PlainZH 改写</th></tr>
<tr>
<td valign="top"><p>本次迭代聚焦登录流程的稳定性建设，围绕超时场景下的异常处理能力进行了针对性优化。通过修复重试逻辑，我们进一步夯实了登录链路的可靠性基础。目前，相关单元测试已全部通过，端到端验证尚未开展，后续仍需结合完整流程确认实际效果。</p></td>
<td valign="top"><p>已修复登录超时后的重试逻辑，相关单元测试全部通过。端到端测试还没做，完整登录流程的实际效果仍需验证。</p></td>
</tr>
</table>

保留变更、测试结果和未验证范围，删去对成果的空泛评价。

<details>
<summary><strong>模型答疑：去掉重复解释，直接回答问题</strong></summary>

<table>
<tr><th width="50%">改写前</th><th width="50%">PlainZH 改写</th></tr>
<tr>
<td valign="top"><p>这是一个非常关键的问题。要准确理解“提交成功”的含义，我们需要将其放在任务处理的完整生命周期中来看。提交成功并不等同于处理完成，它所代表的是任务已经进入队列这一阶段性状态。换句话说，从任务入队到最终完成之间，还存在后续处理环节，因此仍需通过查询任务状态来确认最终结果。</p></td>
<td valign="top"><p>“提交成功”表示任务已进入队列，还不代表处理完成。要确认结果，需要继续查询任务状态。</p></td>
</tr>
</table>

“任务已入队”和“任务已完成”的区别保留，读者也知道怎样确认结果。

</details>

<details>
<summary><strong>技术方案：把密集规则拆成可查找的条件</strong></summary>

<table>
<tr><th width="50%">改写前</th><th width="50%">PlainZH 改写</th></tr>
<tr>
<td valign="top"><p>状态库记录写前意图、请求hash、远端引用、事件游标、attempt、锁/租约及outbox。相同operation_key只代表同一请求；同key不同hash冲突。submit结果unknown时先reconcile原写入；后端不能核对则停留unknown，不能为了继续验收重提。等待超时只停止本地等待，不默认取消远端任务。取消按资源所有权和精确运行引用进行，不能取消同Session其他调用。</p></td>
<td valign="top"><p><strong>保存恢复所需的信息</strong></p><p>状态库需要记录准备执行的写入、请求 hash、远端引用和事件游标，还要保存 attempt、锁或租约，以及 outbox。这些信息用于判断上次执行到了哪里，以及请求是否可以继续处理。</p><p><strong>分清重试、超时和取消</strong></p><ul><li><strong>请求去重</strong>：同一个 <code>operation_key</code> 对应同一请求。如果 key 相同但 hash 不同，报冲突。</li><li><strong>提交结果未知</strong>：如果 <code>submit</code> 返回 <code>unknown</code>，先用 <code>reconcile</code> 核对原来的写入。后端无法核对时，保留 <code>unknown</code>，不能为了继续验收而重新提交。</li><li><strong>等待超时</strong>：只停止本地等待，默认不取消远端任务。</li><li><strong>取消任务</strong>：根据资源归属和精确的运行引用执行取消，不能影响同一 Session 中的其他调用。</li></ul></td>
</tr>
</table>

用小标题区分要保存的信息和异常处理规则，再按条件列出处理方式，方便开发者逐项核对。[阅读完整案例与修改说明](showcase/technical-proposal.md)。

</details>

<details>
<summary><strong>故障分析：把抽象术语展开成具体原因</strong></summary>

<table>
<tr><th width="50%">改写前</th><th width="50%">PlainZH 改写</th></tr>
<tr>
<td valign="top"><p>反复循环的主放大器是备用压缩的状态处理语义不一致。常规压缩成功会清历史消息、用摘要替换新增消息；备用压缩却只压缩新增消息，历史消息和固定上下文都保留。与此同时，旧版分段逻辑不是 token-aware、merge 后没有二次归并，也没有压缩后目标水位和冷却区间。结果是备用压缩在技术上成功、在压缩水位上却不合格，任务很快再次触发。</p></td>
<td valign="top"><p>备用压缩与常规压缩处理的内容不同。常规压缩成功后，会清空历史消息，并用摘要替换新增消息；备用压缩只处理新增消息，保留历史消息和固定上下文。</p><p>备用压缩还有几个限制：分段时不按 token 数控制大小，合并结果后不再做一次归并压缩，也没有设定压缩后的目标长度和两次压缩之间的冷却间隔。</p><p>因此，备用压缩虽然返回成功，整个请求却仍然过长。任务继续执行后，很快就会再次触发压缩，形成反复循环。</p></td>
</tr>
</table>

说明两种压缩分别处理哪些内容，再解释为什么会反复触发。篇幅有所增加，原因更容易读懂。[阅读修改说明](showcase/incident-analysis.md)。

</details>

前两组为演示短稿。更多对照见[案例目录](showcase/README.md)和[改写示例](references/examples.md)。

## 安装与使用

通过 [Skills CLI](https://github.com/vercel-labs/skills) 安装到支持的 Agent：

```sh
npx skills add Cmoon-cyl/plainzh
```

安装后，直接提供文字、文件或起草材料：

```text
用 $plainzh 改写这段开发进展，让同事看清改了什么、验证了什么、还有什么没完成。

[粘贴原文]
```

也可以指定用途和修改范围：

- `后续用 $plainzh 的原则回复我，直接给出结论，保留依据和不确定性。`
- `用 $plainzh 写这次迭代的 PR 说明，交代行为变化、验证结果和已知限制。`
- `用 $plainzh 改写这段回答，让刚接触这个概念的开发者看懂。`
- `用 $plainzh 润色这份周报，保留小标题和汇报语气。`

默认交付正文；需要修改说明或前后对照时，直接提出即可。信息不足时，Agent 会指出缺项。

<details>
<summary>手动安装到 Codex</summary>

```sh
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
git clone https://github.com/Cmoon-cyl/plainzh.git \
  "${CODEX_HOME:-$HOME/.codex}/skills/plainzh"
```

安装后新开会话或重新加载技能。已有同名目录时，先保留自己的修改。

</details>

## 写作方法

### ISO 24495-1：按读者的需要组织内容

PlainZH 采用 ISO 24495-1:2023 的四项清晰语言原则，并将它们转成中文写作要求：

| 原则 | 怎样要求 Agent |
|---|---|
| 内容切合需要 | 用读者的问题决定选材和顺序，补齐材料中已有的必要信息，保留条件、例外和不利证据。 |
| 容易找到 | 按连续阅读、随时查阅或操作的需要组织内容，让结论与条件、例外保持对应。 |
| 容易理解 | 补上必要背景和推理环节，写清对象、动作和关系，按需解释术语或使用图表。 |
| 能够使用 | 写作中反复评价并修改，按需要获取目标读者反馈；长期使用的文档还要根据实际使用结果再评价。 |

四项原则贯穿写作和修改，不是依次完成的四道工序。第 4 项在标准中重点落实为评价：模型回读属于文本自查；实际阅读效果，需要目标读者的反馈或使用证据。评价深度结合文档复杂度、受众、误解后果和可用资源确定。

### ASD-STE100：把技术要求写明确

PlainZH 参考 ASD-STE100 Issue 9 中适合中文的技术写作方法：

- **名称一致。** 同一对象沿用同一名称，保留命令、参数和状态值。
- **条件先行。** 先交代操作前提，再写动作，分清先后、同时执行和等待关系。
- **要求清楚。** 独立操作按步骤写，必须执行的动作放在正文中，备注用于补充解释。

ASD-STE100 面向英语。PlainZH 不套用英文受控词表、词性限制或单词数上限，也不提供标准译本或合规认证。[查看来源与适用边界](references/sources.md)。

### Agent 怎样改稿

[SKILL.md](SKILL.md) 要求 Agent 在改稿时完成以下检查：

1. **通读材料，明确用途和范围。** 确定读者的问题，以及正文会承接对话还是独立使用；“只润色”时保留结构，“重写”时可以调整信息顺序。
2. **保护事实与原意。** 保留数字、术语、引用、链接，以及条件、否定、概率、承诺和完成状态。
3. **按用途组织，照顾阅读方式。** 让选材、顺序和图文形式服务读者的问题。懂专业知识不代表知道项目前情，独立文档应带上必要背景和入口。[查看信息设计方法](references/information-design.md)。
4. **核对事实和用途。** 从原文检查是否遗漏，从改稿检查是否新增事实；再按读者的问题确认信息是否够用。有依据时直接补全，不能编造定义、执行条件或验收标准。起草同样守住事实边界。

检查在改稿过程中完成，短回复不必扩写成完整报告。

## 参与改进

如果改写丢了信息、语气不合适或仍然难读，欢迎带上原文、改写结果和目标读者提交 [Issue](https://github.com/Cmoon-cyl/plainzh/issues)。提交前请去掉敏感信息。

[技能说明](SKILL.md) · [技术写作方法](references/technical-writing.md) · [案例目录](showcase/README.md) · [MIT License](LICENSE)
