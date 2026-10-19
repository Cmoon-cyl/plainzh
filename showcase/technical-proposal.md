# 技术方案：未知结果、超时和取消

[全部案例](README.md) / [PlainZH 首页](../README.md)

**写给谁**：实现与评审异步任务方案的开发者，需要按条件查找恢复规则。

**材料来源**：沿用本仓库已公开的技术片段；改稿为编辑演示，不是某次测试的原始输出。

## 原文与改稿

按字符对照：左栏高亮删除或替换的文字，右栏高亮新增或替换的文字；未改部分不标记。样稿中的 Markdown 标记保留为文字。

<table>
<tr><th width="50%">原文 · 删除处高亮并加删除线</th><th width="50%">改稿 · 新增处高亮并加下划线</th></tr>
<tr>
<td valign="top">
<p>状态库记录写前意图、请求hash、远端引用、事件游标、attempt、锁/租约及outbox。相同operation_key只代表同一请求；<mark><del>同</del></mark>key<mark><del>不</del></mark>同hash冲突。submit结果unknown<mark><del>时</del></mark>先reconcile原写入<mark><del>；</del></mark>后端<mark><del>不能</del></mark>核对<mark><del>则停留</del></mark>unknown，不能为了继续验收重提。等待超时只停止本地等待，<mark><del>不</del></mark>默认取消远端任务。取消<mark><del>按</del></mark>资源所有权和精确运行引用<mark><del>进</del></mark>行，不能取消同Session其他调用。</p>
</td>
<td valign="top">
<p><mark><ins>### 状态库记录什么</ins></mark></p>
<p>状态库记录写前意图、请求<mark><ins> </ins></mark>hash、远端引用、事件游标、attempt、锁/租约及<mark><ins> </ins></mark>outbox。</p>
<p><mark><ins>### 遇到不同情况怎样处理</ins></mark></p>
<p><mark><ins>| 情况 | 规则 |</ins></mark><br><mark><ins>|---|---|</ins></mark><br><mark><ins>| 请求使用</ins></mark>相同<mark><ins>的 `</ins></mark>operation_key<mark><ins>` | </ins></mark>只代表同一请求；<mark><ins>如果 </ins></mark>key<mark><ins> 相</ins></mark>同<mark><ins>但 </ins></mark>hash<mark><ins> 不同，报</ins></mark>冲突。<mark><ins> |</ins></mark><br><mark><ins>| `</ins></mark>submit<mark><ins>` 的</ins></mark>结果<mark><ins>为 `</ins></mark>unknown<mark><ins>` | </ins></mark>先<mark><ins>用 `</ins></mark>reconcile<mark><ins>` 核对</ins></mark>原写入<mark><ins>。</ins></mark>后端<mark><ins>无法</ins></mark>核对<mark><ins>时，保持 `</ins></mark>unknown<mark><ins>`</ins></mark>，不能为了继续验收<mark><ins>而</ins></mark>重<mark><ins>新</ins></mark>提<mark><ins>交</ins></mark>。<mark><ins> |</ins></mark><br><mark><ins>| </ins></mark>等待超时<mark><ins> | </ins></mark>只停止本地等待，默认<mark><ins>不</ins></mark>取消远端任务。<mark><ins> |</ins></mark><br><mark><ins>| </ins></mark>取消<mark><ins>任务 | 根据</ins></mark>资源所有权和精确<mark><ins>的</ins></mark>运行引用<mark><ins>执</ins></mark>行，不能取消同<mark><ins>一 </ins></mark>Session<mark><ins> 中的</ins></mark>其他调用。<mark><ins> |</ins></mark></p>
</td>
</tr>
</table>

## 为什么这样改

把“需要保存什么”和“遇到情况怎样处理”分成两部分。异常规则按条件排成表格，方便评审时找到对应行为，不要求读者先拆解整段文字。

保留 `operation_key`、`unknown`、`reconcile` 等准确名称。“同一个 key”只说明请求身份，不能据此补写后端已实现去重；“等待超时”也不能写成远端任务已经停止。

## 哪些含义必须保留

- 状态库中的七类信息均保留，未凭术语名称补充字段定义。
- 相同 `operation_key` 代表同一请求；同 key 不同 hash 属于冲突。
- 提交结果未知时先核对原写入；无法核对则保持未知，禁止为继续验收而重提。
- 等待超时只停止本地等待，默认不取消远端任务。
- 取消按资源所有权和精确运行引用执行，不能取消同一 Session 的其他调用。

[继续看其他案例](README.md) · [查看保真边界](../references/examples.md)
