# 公开数学工作流：可复用部分与六槽适配

## 核心思路

OpenAI 的公开案例没有把模型当作一次性“证明机”，而是把研究级证明拆成可验证的循环：

1. 先产生少量高层种子思路；
2. 每个种子分别要求端到端严谨证明；
3. 用独立上下文检查证明和引用，只报关键缺口；
4. 针对明确缺口修订，无法修补则换路线；
5. 人类专家选择问题、判断哪条路线值得继续、核验正确性和归属；
6. 最后从少量候选中选择最可信版本，而不是把一次采样当成定论。

`First Proof` 附录给出的公开模板大体对应“思路生成—成证—验证—修订”四种角色。OpenAI 同时明确披露：模型会生成貌似可信但错误的证明，对提示脚手架和热身题敏感，也可能复现已有结果却不给出处。

Ernest Ryu 的案例补充了一个很实用的经验：让新会话检查旧会话的工作，比让同一会话自检更可靠。专家仍需逐步复核并决定何时丢弃路线。

后续公开证据把边界说得更清楚：

- Aletheia 在数百道标为开放的问题上采用“生成—验证—修订”，允许放弃；大规模审计显示技术正确、真正回答题意、独立重发现和文献已解必须分开统计。
- AlphaProof Nexus 对已形式化研究题的消融显示，简单的独立证明者加 Lean 反馈能覆盖很多成功；复杂进化和更多代理主要帮助最难尾部。三至六路通常更省成本，但不能宣称等价于更大扇出。
- First Proof 第二批及 ProofCouncil 表明条件式作者—批评者循环、按需调用异质委员会/计算节点和最终新鲜批评者是可行架构，同时也显示复杂 harness 的成本远高于单次模型调用。ProofCouncil 的六个角色不是“六条常驻证明路线”。
- Leiden Declaration 强调工具、算力、失败分母、归属、独立验证和数学理解都要披露。

## 本 skill 的增强

公开工作流主要解决“如何提高证明成功率”。本 skill 额外解决研究审计中的四个问题：

- **前提所有权：**只有主实例能改前提，证明者不能让命题在手里悄悄变容易。
- **命题版本化：**每次前提变化都新建冻结版本，旧反例和失败证明永久保留。
- **证明与命题分离：**验证者要区分“命题为假”和“收到的证明没覆盖最终定义域”。
- **正确性与新颖性分离：**在证明前后都做既有工作占位检查，避免漂亮地重证经典定理。
- **题意忠实性：**自然语言命题、形式陈述和原作者数学意图分三层核对，防止通过最容易的字面解释获得空洞正确答案。
- **证据式调度：**最多六槽，但先启动少量高差异路线，只给产生新对象的路线续费。
- **完整分母与归属：**记录全部候选、失败路线、提示、成本以及人和模型分别贡献了什么。

## 六槽下的可复用协议

1. 主实例计入六槽，不把六槽都当证明者。
2. 首轮只启动两至三条结构不同的路线，并保留反例/审计能力。
3. 每条路线先给一个工作单元；只有显式反例、可核查构造、严格弱关键引理或完整证明才能晋级。
4. 完整候选出现后，立即把同质生成槽改派给逻辑验证、领域风险、形式检查和新颖性审计。
5. 致命缺口回到新路线，小缺口才交原作者定向修订；修订稿再换新验证者。
6. 票数、模型自信和自然语言评分不是证明；形式内核也只证明编码后的陈述。

ProofCouncil 的消融给出两个直接警告：同一有状态批评者曾七次放行一份后来仍被新鲜批评者拒绝的未完成证明；另一次批评者因未核实引用中的技术断言而误放行。故上下文独立的最终审计和外部定理条件核验不能省。其 FirstProof 运行约为每题 350 美元，而单次强模型约 12 美元；多角色只应由中间证据触发。

不要照搬“假定肯定证明存在”、固定工作时长、只展示成功项或大规模常驻扇出。已知答案的基准复现可以使用隔离的肯定偏置路线，但它没有额外证据权重。

## 何时加入热身题

热身题只用于帮助模型找结构，不能暗示目标结论必真。选择与主问题同构但更简单、且答案已知的命题。完成热身后开启新上下文，把可复用结构作为一条种子路线，而不是把热身答案直接类比过去。

## 来源

- OpenAI, “Our First Proof submissions”: https://openai.com/index/first-proof-submissions/
- First Proof proof attempts and prompt appendix: https://cdn.openai.com/pdf/26177a73-3b75-4828-8c91-e8f1cf27aaa0/oai_first_proof.pdf
- OpenAI, “Early experiments in accelerating science with GPT-5”: https://openai.com/index/accelerating-science-gpt-5/
- OpenAI, “How GPT-5 helped mathematician Ernest Ryu solve a 40-year-old open problem”: https://openai.com/index/gpt-5-mathematical-discovery/
- DeepMind, “Towards Autonomous Mathematics Research”: https://arxiv.org/abs/2602.10177
- DeepMind, “Advancing Mathematics Research with AI-Driven Formal Proof Search”: https://arxiv.org/abs/2605.22763
- “First Proof Second Batch”: https://arxiv.org/abs/2606.18119
- “ProofCouncil”: https://arxiv.org/abs/2607.09474
- Leiden Declaration on Artificial Intelligence and Mathematics: https://leidendeclaration.ai/

这些来源支持工作流，不构成对任何具体数学结论的正确性背书。
