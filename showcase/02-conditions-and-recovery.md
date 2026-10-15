# 把异常条件和处理动作放在一起

[← 返回案例索引](README.md)

来源类型：技术方案。一个长段落混合了状态记录、幂等冲突、结果未知、等待超时和取消权限。

## 改写前

状态库记录写前意图、请求hash、远端引用、事件游标、attempt、锁/租约及outbox。相同operation_key只代表同一请求；同key不同hash冲突。submit结果unknown时先reconcile原写入；后端不能核对则停留unknown，不能为了继续验收重提。等待超时只停止本地等待，不默认取消远端任务。取消按资源所有权和精确运行引用进行，不能取消同会话其他调用。

## 改写后

状态库记录写前意图、请求 hash、远端引用、事件游标、attempt、锁/租约和 outbox。同一 operation_key 只能对应同一请求；key 相同而 hash 不同，必须报冲突。

submit 结果为 unknown 时，先 reconcile 原写入；后端无法核对时保留 unknown，不得为继续验收而重新提交。等待超时只结束本地等待，不默认取消远端任务。取消操作必须核对资源所有权和精确运行引用，不得取消同一会话中的其他调用。

## 改了什么

将状态记录与幂等约束放在第一段；第二段按结果未知、超时、取消分别说明处理要求。

**保留的含义：** unknown 不变成失败；无法核对时不重新提交；本地超时不默认取消远端任务；取消不能影响同会话的其他调用。

**脱敏说明：** 会话对象名改为通用名称；hash、operation_key、submit、reconcile、unknown 等通用术语保留。

<details>
<summary>查看 unified diff</summary>

```diff
--- before.md
+++ after.md
@@ -1 +1,3 @@
-状态库记录写前意图、请求hash、远端引用、事件游标、attempt、锁/租约及outbox。相同operation_key只代表同一请求；同key不同hash冲突。submit结果unknown时先reconcile原写入；后端不能核对则停留unknown，不能为了继续验收重提。等待超时只停止本地等待，不默认取消远端任务。取消按资源所有权和精确运行引用进行，不能取消同会话其他调用。
+状态库记录写前意图、请求 hash、远端引用、事件游标、attempt、锁/租约和 outbox。同一 operation_key 只能对应同一请求；key 相同而 hash 不同，必须报冲突。
+
+submit 结果为 unknown 时，先 reconcile 原写入；后端无法核对时保留 unknown，不得为继续验收而重新提交。等待超时只结束本地等待，不默认取消远端任务。取消操作必须核对资源所有权和精确运行引用，不得取消同一会话中的其他调用。
```

</details>
