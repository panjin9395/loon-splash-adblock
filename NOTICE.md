# 版权与改动说明

本项目以 GPL-3.0-only 发布，完整许可证见 LICENSE。不提供适销性、适用性或无侵权保证。

闲鱼开屏规则来源：奶思 / fmz200，wool_scripts。
固定版本：https://github.com/fmz200/wool_scripts/blob/6e7bf91a2b412ff75177084e0d593af19a3c5947/Surge/module/split/partX/XianYu.sgmodule#L42-L43
许可：https://github.com/fmz200/wool_scripts/blob/6e7bf91a2b412ff75177084e0d593af19a3c5947/LICENSE

2026-10-20，panjin9395 将其中单一开屏 Map Local 空 JSON 动作转换为 Loon reject-dict，收窄路径版本及结尾边界；删除所有非开屏行为（不分发完整上游文件）。提供 rules.json、build.py 和生成结果作为完整对应源码。

上游 README 提醒部分内容来自其他开源项目，不宣称本规则原始请求发现归我们独有。保留上游请求：不要在中国大陆平台传播上游内容。本项目发布于 GitHub，不代表上游作者认可或背书。

kelee / 可莉插件没有复制或改写进发布物。其索引仓库的 CC BY-NC-SA 不等于插件本体授权，插件中心另有禁止二改/再分发说明。第三方镜像不能替代授权。

## v0.2.0 增补

2026-10-20 新增规则仍来源奶思 / fmz200；得物原规则另署 Runestoner，保留该署名。
固定上游提交：5d5f63fcf98bc69d5f8f1b1bae6f86a01ee4bb97。
许可：https://github.com/fmz200/wool_scripts/blob/5d5f63fcf98bc69d5f8f1b1bae6f86a01ee4bb97/LICENSE
每条来源的精确路径、行号、原规则、内容哈希见 sources.json，作为对应源代码随本仓库公开。只选择开屏分支，拆分精确主机，限定HTTPS和完整路径；保持reject或空JSON动作，不复制整模块及其远程脚本。screening.json引用来源片段用于审查，不作为运行规则。未证明当前App版本兼容，不声称上游背书。

## v0.2.1 增补

同一固定fmz200提交下新增7款的8条独立开屏分支，署名奶思 / fmz200；原规则、行号、文件哈希继续记录在sources.json。deep-review.json只保留审查所需片段及引用；无关数字匹配去除内容仅留行号/哈希。未复制外部脚本、Cookie采集或签到功能。
