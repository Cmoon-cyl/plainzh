# 故障分析：为什么压缩后又触发压缩

[全部案例](README.md) / [PlainZH 首页](../README.md)

**写给谁**：需要理解故障机制的开发者。常规上下文压缩失败后，系统启用备用压缩，但备用流程返回成功后仍反复触发压缩。

**材料来源**：沿用本仓库已公开的技术片段；改稿为编辑演示，不是某次测试的原始输出。

## 原文与改稿

按字符对照：左栏高亮删除或替换的文字，右栏高亮新增或替换的文字；未改部分不标记。样稿中的 Markdown 标记保留为文字。

<table>
<tr><th width="50%">原文 · 删除处高亮并加删除线</th><th width="50%">改稿 · 新增处高亮并加下划线</th></tr>
<tr>
<td valign="top">
<p><mark><del>反复循环的主放大器是</del></mark>备用压缩<mark><del>的状态</del></mark>处理<mark><del>语义</del></mark>不<mark><del>一致</del></mark>。常规压缩成功会清历史消息<mark><del>、</del></mark>用摘要替换新增消息；备用压缩<mark><del>却</del></mark>只<mark><del>压缩</del></mark>新增消息，历史消息和固定上下文<mark><del>都保留</del></mark>。<mark><del>与此同时，</del></mark>旧版分段逻辑不<mark><del>是</del></mark> token<mark><del>-aware、merge</del></mark> 后<mark><del>没有二</del></mark>次归并，<mark><del>也</del></mark>没有压缩后目标<mark><del>水位</del></mark>和冷却<mark><del>区</del></mark>间。<mark><del>结果是</del></mark>备用压缩<mark><del>在技术上</del></mark>成功<mark><del>、在压缩水位上</del></mark>却<mark><del>不合格，</del></mark>任务很快再次触发。</p>
</td>
<td valign="top">
<p>备用压缩<mark><ins>与常规压缩</ins></mark>处理<mark><ins>的内容</ins></mark>不<mark><ins>同，这是反复触发压缩的主要放大因素</ins></mark>。常规压缩成功<mark><ins>后，</ins></mark>会清<mark><ins>空</ins></mark>历史消息<mark><ins>，并</ins></mark>用摘要替换新增消息；备用压缩只<mark><ins>处理</ins></mark>新增消息，<mark><ins>保留</ins></mark>历史消息和固定上下文。</p>
<p>旧版分段逻辑不<mark><ins>按</ins></mark> token <mark><ins>数控制大小，合并结果</ins></mark>后<mark><ins>也不再做一</ins></mark>次归并<mark><ins>压缩。此外</ins></mark>，没有<mark><ins>设定</ins></mark>压缩后<mark><ins>的</ins></mark>目标<mark><ins>长度</ins></mark>和<mark><ins>两次压缩之间的</ins></mark>冷却间<mark><ins>隔</ins></mark>。</p>
<p><mark><ins>因此，在这次故障中，</ins></mark>备用压缩<mark><ins>虽然返回</ins></mark>成功<mark><ins>，整个请求</ins></mark>却<mark><ins>仍然过长。</ins></mark>任务很快再次触发<mark><ins>压缩，形成反复循环</ins></mark>。</p>
</td>
</tr>
</table>

## 为什么这样改

先交代两条流程分别处理了哪些内容，再说明分段、归并和触发方面的限制，最后解释为什么反复压缩。这里需要保留推理过程，不能只把结论改短。

“旧版”限定分段逻辑的适用范围，不能省掉。本例已确认请求仍然过长，因此保留这一确定判断，不改成“可能过长”或“无法判断是否过长”。

## 哪些含义必须保留

- 常规压缩成功后清空历史消息，并用摘要替换新增消息；备用压缩保留历史消息和固定上下文。
- 旧版分段不按 token 数控制大小，合并后没有二次归并。
- 没有设定压缩后的目标长度和冷却间隔。
- 本例中备用流程返回成功，但整个请求仍然过长，任务很快再次触发压缩。
- 原稿指出主要放大因素，改稿没有把它说成唯一原因。

[继续看其他案例](README.md) · [查看保真边界](../references/examples.md)
