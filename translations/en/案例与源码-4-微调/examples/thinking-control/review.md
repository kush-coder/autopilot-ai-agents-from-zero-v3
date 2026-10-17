# Thinking Mode Diagnosis: Verifying the 12 Predictions One by One

The following checks the 12 responses for validation set items 1, 6, and 8, using the same B prompt. The responses below were read directly from the original prediction files, without deleting any analysis, English snippets, or repeated words.

| Model and template            | Contains analysis section | Forms a complete list | Format passes |
| ----------------------------- | ------------------------- | --------------------- | ------------- |
| Original model / qwen3_nothink | 3/3                       | 0/3                   | 0/3           |
| Original model / qwen3         | 0/3                       | 2/3                   | 2/3           |
| Adapter / qwen3_nothink        | 0/3                       | 2/3                   | 2/3           |
| Adapter / qwen3                | 0/3                       | 2/3                   | 2/3           |

"Forms a complete list" only describes whether the response ends with a list; it does not indicate that all topic information is present. "Format passes" uses the course's original scoring script. All response content still needs to be read item by item.

**Mechanism confirmed:** In the locked LLaMA-Factory version, `qwen3_nothink` does not add an empty thinking block; `qwen3` with `enable_thinking=False` adds that block at the start of the assistant's turn. The actual difference in the input is only the final 4 tokens. The user message is identical, and the reference answer does not enter the generation input.

**Response phenomena observed:** The original model's analysis sections changed from 3/3 to 0/3, and the number of format-passing responses changed from 0/3 to 2/3; English rewrites, omitted words, and repetitions still occur. Both Adapter groups have 2/3 format-passing responses, and the repeated output of F68050 and item 8 has not disappeared. The 6 responses from the two qwen3_nothink groups are verbatim identical to the previously sampled responses with the same configuration.

**Scope of conclusions:** This supports locating the reason why the original model still outputs analysis under the current conditions in the actual template processing difference. It has been ruled out that the reference answer leaked this time, that the model/Adapter fingerprints changed, or that precision was inconsistent. This cannot prove that the new template is suitable for all inputs, that the Adapter is superior to a fully optimized original model, or that the model is ready for deployment. The Adapter's training template is qwen3_nothink; what is compared here is the inference template, so the results cannot be interpreted as a comparison of the effects of the two training templates.

For file usage and local recalculation, see the [example description](../README.md). The draft of the 10-item annotation is in the [reference annotation review](annotation-review.md) and was not used for rescoring.

## Validation Set Item 1

**Frozen reference answer:** `独头掘进巷道;降温试验系统;制冷降温;焓差;制冷系数`

<details>
<summary>View fixed B prompt and complete input</summary>

```text
请从下面的输入中抽取能够概括文章主题的关键词。
只输出一行关键词，关键词之间使用英文分号 ; 分隔。
不要输出“关键词：”、序号、解释或分析过程，不要重复关键词。
关键词应有原文依据，保留影响含义的完整名称，不为凑数量拆开短语。
原文同时给出全称和简称时优先使用全称，只有简称时保留简称。

待处理输入：
关键词抽取：
金属矿山独头掘进巷道制冷系数是计算独头掘进巷道降温需冷量非常重要的参数之一,关系到能否达到预期降温效果及影响着降温工程的的经济投入。利用“金属矿山深部开采降温试验系统”分别模拟通风降温、加大风量降温、制冷降温、加大制冷降温4种条件下独头掘进巷道的降温过程,并分析独头掘进巷道降温效果,在通风及加大风量降温后,独头掘进巷道内温度先下降然后趋于稳定,再也无法下降,只有通过制冷措施,对独头掘进工作面进行降温。通过监测数据的焓差值计算出降温制冷系数,同时利用多次试验得出制冷系数范围在1．38~1．68,进而为独头掘进巷道降温设计提供设计依据。
```

</details>

### Original Model / qwen3_nothink

Contains analysis section: yes; Forms a complete list: no; Format passes: no.

Contains a <think> analysis section and multiple lines; no final list is formed. The analysis mentions original content such as refrigeration coefficient and test system, but the end of the response is still discussing word selection and has not yet delivered usable keywords.

Original file: [Original model / qwen3_nothink, row 1](../../../../../%E6%A1%88%E4%BE%8B%E4%B8%8E%E6%BA%90%E7%A0%81-4-%E5%BE%AE%E8%B0%83/examples/thinking-control/%E5%8E%9F%E5%A7%8B%E6%A8%A1%E5%9E%8B-qwen3_nothink-%E5%85%B3%E9%97%AD%E6%80%9D%E8%80%83.jsonl ":ignore").

```text
<think>
好的，我需要从用户提供的输入中提取能够概括文章主题的关键词。首先，我需要仔细阅读并理解原文内容。

原文主要讲的是金属矿山独头掘进巷道的降温系统，特别是制冷系数的重要性。提到了几个关键点：制冷系数、降温试验系统、四种降温条件（通风、加大风量、制冷、加大制冷）以及制冷系数的范围。用户要求只输出一行关键词，用英文分号分隔，不能有序号、解释或分析过程，还要保留原文的完整名称，优先使用全称。

首先，我需要确定哪些是核心概念。原文中的关键词包括“金属矿山独头掘进巷道制冷系数”、“降温试验系统”、“通风降温”、“加大风量降温”、“制冷降温”、“制冷系数范围”。这些都直接对应原文的主题。

接下来，检查是否有其他可能的关键词，但用户要求只输出一行，所以需要确保没有重复或冗余的。同时，要确保使用全称，如果存在全称和简称的话，优先使用全称。例如，“金属矿山深部开采降温试验系统”是全称，而“降温试验系统”是简称，但用户可能希望保留全称
```

### Original Model / qwen3

Contains analysis section: no; Forms a complete list: yes; Format passes: yes.

Passes the existing form check; forms a single-line list. Returns metal-mining-drainage-coefficient;cooling-coefficient, without preserving the complete Chinese names from the original text; drainage has no corresponding term in the original, and major information such as single-heading tunnel and test system is omitted.

Original file: [Original model / qwen3, row 1](../../../../../%E6%A1%88%E4%BE%8B%E4%B8%8E%E6%BA%90%E7%A0%81-4-%E5%BE%AE%E8%B0%83/examples/thinking-control/%E5%8E%9F%E5%A7%8B%E6%A8%A1%E5%9E%8B-qwen3-%E5%85%B3%E9%97%AD%E6%80%9D%E8%80%83.jsonl ":ignore").

```text
metal-mining-drainage-coefficient;cooling-coefficient
```

### Adapter / qwen3_nothink

Contains analysis section: no; Forms a complete list: yes; Format passes: yes.

Passes the existing form check; forms a single-line list. Metal mine, single-heading tunnel, and refrigeration coefficient all have support in the original text; missing reference words such as cooling test system, refrigeration cooling, and enthalpy difference. Metal mine is not included in the reference answer, so it is not judged as an unsupported word for that reason.

Original file: [Adapter / qwen3_nothink, row 1](../../../../../%E6%A1%88%E4%BE%8B%E4%B8%8E%E6%BA%90%E7%A0%81-4-%E5%BE%AE%E8%B0%83/examples/thinking-control/Adapter-qwen3_nothink-%E5%85%B3%E9%97%AD%E6%80%9D%E8%80%83.jsonl ":ignore").

```text
金属矿山;独头掘进巷道;制冷系数
```

### Adapter / qwen3

Contains analysis section: no; Forms a complete list: yes; Format passes: yes.

Passes the existing form check; forms a single-line list. Changed to English phrases metal mining;cooling coefficient;metal mining deep mining;cooling system, without preserving the complete original names, and omitting the specific names of single-heading tunnel and test system. Improvement cannot be judged solely from the absence of an analysis section.

Original file: [Adapter / qwen3, row 1](../../../../../%E6%A1%88%E4%BE%8B%E4%B8%8E%E6%BA%90%E7%A0%81-4-%E5%BE%AE%E8%B0%83/examples/thinking-control/Adapter-qwen3-%E5%85%B3%E9%97%AD%E6%80%9D%E8%80%83.jsonl ":ignore").

```text
metal mining;cooling coefficient;metal mining deep mining;cooling system
```

## Validation Set Item 6

**Frozen reference answer:** `夏波蒂;马铃薯;榆林市;种植表现;炸条;杂交育成;推广栽培;试种;食用品质;技术简介;试验站;农科所;加拿大;产量高;有性;审定;沙滩;品种;农业;母本`

<details>
<summary>View fixed B prompt and complete input</summary>

```text
请从下面的输入中抽取能够概括文章主题的关键词。
只输出一行关键词，关键词之间使用英文分号 ; 分隔。
不要输出“关键词：”、序号、解释或分析过程，不要重复关键词。
关键词应有原文依据，保留影响含义的完整名称，不为凑数量拆开短语。
原文同时给出全称和简称时优先使用全称，只有简称时保留简称。

待处理输入：
识别出下文中的关键词：
夏波蒂是加拿大福瑞克通农业试验站用"F58050"为 母本,"Bakeking"为父本经有性杂交育成,1987年引入我国试种,未经过审定或认定,但被辛普劳公司作为炸条品 种在各地种植.2003年由榆林市农科所弓1人我市试种,通过5年观察,该品种产量高,炸条品质和食用品质优良,适 宜在我市北部风沙滩水地区推广栽培,现将种植表现及栽·培技术简介如下:
```

</details>

### Original Model / qwen3_nothink

Contains analysis section: yes; Forms a complete list: no; Format passes: no.

Contains an English <think> analysis section and multiple lines; no final list is formed. The analysis arbitrarily writes hybrid corn variety and Xinping Company, which are not in the original text; the answer cannot be compiled for the model from the analysis text.

Original file: [Original model / qwen3_nothink, row 2](../../../../../%E6%A1%88%E4%BE%8B%E4%B8%8E%E6%BA%90%E7%A0%81-4-%E5%BE%AE%E8%B0%83/examples/thinking-control/%E5%8E%9F%E5%A7%8B%E6%A8%A1%E5%9E%8B-qwen3_nothink-%E5%85%B3%E9%97%AD%E6%80%9D%E8%80%83.jsonl ":ignore").

```text
<think>
Okay, let's tackle this. The user wants me to extract keywords from the provided text that summarize the article's main topic. The output should be one line with the keywords separated by semicolons, no markdown, and no extra explanations or numbers.

First, I need to read through the input carefully. The text talks about a hybrid corn variety developed through crossbreeding between two parents: F58050 as the mother and Bakeking as the father. The variety was introduced in 1987 by the Canadian agricultural experiment station, but it wasn't approved or tested. It was later used by Xinping Company as a炸条 (which I think translates to "fry strip" or "fry product") crop in various regions. Then there's a mention of trials in 2003 by the local agricultural research institute in榆林, leading to high yield and good quality, suitable for cultivation in the northern wind-swept areas of the city.

Now, the main elements here are the hybrid variety, the parents (F58050 and Bakeking), the introduction date (1987), the approval status (not approved or tested), the use by Xinping Company, and the trials in 2
```

### Original Model / qwen3

Contains analysis section: no; Forms a complete list: yes; Format passes: yes.

Passes the existing form check; forms a single-line list. F58050 and Bakeking both have support in the original text, but only the parent line numbers/names are returned, omitting the topic variety Shepody and planting performance information.

Original file: [Original model / qwen3, row 2](../../../../../%E6%A1%88%E4%BE%8B%E4%B8%8E%E6%BA%90%E7%A0%81-4-%E5%BE%AE%E8%B0%83/examples/thinking-control/%E5%8E%9F%E5%A7%8B%E6%A8%A1%E5%9E%8B-qwen3-%E5%85%B3%E9%97%AD%E6%80%9D%E8%80%83.jsonl ":ignore").

```text
F58050;Bakeking
```

### Adapter / qwen3_nothink

Contains analysis section: no; Forms a complete list: yes; Format passes: yes.

Passes the existing form check; forms a single-line list. F58050 and Bakeking have support in the original text, while F68050 does not; still omits topic information such as Shepody.

Original file: [Adapter / qwen3_nothink, row 2](../../../../../%E6%A1%88%E4%BE%8B%E4%B8%8E%E6%BA%90%E7%A0%81-4-%E5%BE%AE%E8%B0%83/examples/thinking-control/Adapter-qwen3_nothink-%E5%85%B3%E9%97%AD%E6%80%9D%E8%80%83.jsonl ":ignore").

```text
F58050;Bakeking;F68050
```

### Adapter / qwen3

Contains analysis section: no; Forms a complete list: yes; Format passes: yes.

Passes the existing form check; forms a single-line list. Verbatim identical to the qwen3_nothink response: still contains the unsupported word F68050 and omits topic information such as Shepody.

Original file: [Adapter / qwen3, row 2](../../../../../%E6%A1%88%E4%BE%8B%E4%B8%8E%E6%BA%90%E7%A0%81-4-%E5%BE%AE%E8%B0%83/examples/thinking-control/Adapter-qwen3-%E5%85%B3%E9%97%AD%E6%80%9D%E8%80%83.jsonl ":ignore").

```text
F58050;Bakeking;F68050
```

## Validation Set Item 8

**Frozen reference answer:** `恩诺沙星;日本鳗鲡;残留;高效液相色谱法`

<details>
<summary>View fixed B prompt and complete input</summary>

```text
请从下面的输入中抽取能够概括文章主题的关键词。
只输出一行关键词，关键词之间使用英文分号 ; 分隔。
不要输出“关键词：”、序号、解释或分析过程，不要重复关键词。
关键词应有原文依据，保留影响含义的完整名称，不为凑数量拆开短语。
原文同时给出全称和简称时优先使用全称，只有简称时保留简称。

待处理输入：
抽取出文本中的关键词：
采用高效液相色谱法检测日本鳗鲡肌肉、血清、肠、鳃和肝脏组织中恩诺沙星及其代谢物环丙沙星的残留.方法的日内和日间变异系数分别为1.86%和2.53%,标准添加回收率为(95±6)%;最低测量限为1.0 μg/kg.用现场试验方法研究恩诺沙星在鳗鱼体内的代谢残留规律.对约50 g鳗鱼按9 mg/kg鱼体重每天给药2次,连续投喂7 d.给药期间鳗鱼体内的药物含量呈锯齿状上升,停药60 d后鳗鱼肠、鳃和肝脏组织中药物即下降至1～5 μg/kg.肌肉和血清中药物残留到90 d,分别消除至3 μg/kg和4 μg/kg.所测组织的药物残留至停药120 d后降到检测限以下.故鳗鱼的停药期不应低于120 d.
```

</details>

### Original Model / qwen3_nothink

Contains analysis section: yes; Forms a complete list: no; Format passes: no.

Contains a <think> analysis section and multiple lines; no final list is formed. The response is discussing how to select tissues, drugs, and test data, and is still analyzing at the end.

Original file: [Original model / qwen3_nothink, row 3](../../../../../%E6%A1%88%E4%BE%8B%E4%B8%8E%E6%BA%90%E7%A0%81-4-%E5%BE%AE%E8%B0%83/examples/thinking-control/%E5%8E%9F%E5%A7%8B%E6%A8%A1%E5%9E%8B-qwen3_nothink-%E5%85%B3%E9%97%AD%E6%80%9D%E8%80%83.jsonl ":ignore").

```text
<think>
好的，我需要从用户提供的文本中提取关键词，然后用英文分号分隔。首先，我得仔细阅读原文，找出所有重要的信息点。

原文提到检测的是日本鳗鲡的肌肉、血清、肠、鳃和肝脏组织中的恩诺沙星和环丙沙星的残留。方法的日内和日间变异系数、标准添加回收率、最低测量限等数据。然后是用现场试验研究代谢残留规律，给药量和时间，以及停药后的残留情况，最后得出停药期不应低于120天。

接下来，我需要确定哪些是核心关键词。首先，检测的组织是肌肉、血清、肠、鳃、肝脏，所以这些应该作为关键词。然后是药物名称恩诺沙星和环丙沙星，以及检测方法的名称高效液相色谱法。还有数据部分，比如变异系数、回收率、最低限等，但用户要求只输出关键词，所以可能不需要这些数据，除非它们有影响含义。不过用户说要保留影响含义的完整名称，所以可能需要保留这些数据，但可能不需要单独列出，因为用户只要求关键词，而数据可能属于方法细节。

然后，检查
```

### Original Model / qwen3

Contains analysis section: no; Forms a complete list: no; Format passes: no.

Repeats enoxacin, with an empty item after the semicolon at the end; no complete usable list is formed. Outputs English words such as enolamide and enoxacin that are not in the original text, and does not preserve the original names such as enrofloxacin, ciprofloxacin, and Japanese eel. Here the English words are not manually mapped to the correct drug names.

Original file: [Original model / qwen3, row 3](../../../../../%E6%A1%88%E4%BE%8B%E4%B8%8E%E6%BA%90%E7%A0%81-4-%E5%BE%AE%E8%B0%83/examples/thinking-control/%E5%8E%9F%E5%A7%8B%E6%A8%A1%E5%9E%8B-qwen3-%E5%85%B3%E9%97%AD%E6%80%9D%E8%80%83.jsonl ":ignore").

```text
enolamide; enoxacin; enoxacin; enoxacin; enoxacin; enoxacin; enoxacin; enoxacin; enoxacin; enoxacin; enoxacin; enoxacin; enoxacin; enoxacin; enoxacin; enoxacin; enoxacin; enoxacin; enoxacin; enoxacin; enoxacin; enoxacin; enoxacin; enoxacin; enoxacin; enoxacin; enoxacin; enoxacin; enoxacin; enoxacin; enoxacin; enoxacin; enoxacin; enoxacin; enoxacin; enoxacin; enoxacin; enoxacin; enoxacin; enoxacin; enoxacin; enoxacin; enoxacin; enoxacin; enoxacin; enoxacin; enoxacin; enoxacin; enoxacin; enoxacin; enoxacin; enoxacin; enoxacin; enoxacin; enoxacin; enoxacin; enoxacin; enoxacin; enoxacin; enoxacin; enoxacin; enoxacin; enoxacin; enoxacin;
```

### Adapter / qwen3_nothink

Contains analysis section: no; Forms a complete list: no; Format passes: no.

Repeats enoxacin, with an empty item after the semicolon at the end; no complete usable list is formed. Does not preserve the original Chinese drug, research subject, and method names; do not normalize the repeated English words and treat them as correct answers.

Original file: [Adapter / qwen3_nothink, row 3](../../../../../%E6%A1%88%E4%BE%8B%E4%B8%8E%E6%BA%90%E7%A0%81-4-%E5%BE%AE%E8%B0%83/examples/thinking-control/Adapter-qwen3_nothink-%E5%85%B3%E9%97%AD%E6%80%9D%E8%80%83.jsonl ":ignore").

```text
enoxacin; enoxacin; enoxacin; enoxacin; enoxacin; enoxacin; enoxacin; enoxacin; enoxacin; enoxacin; enoxacin; enoxacin; enoxacin; enoxacin; enoxacin; enoxacin; enoxacin; enoxacin; enoxacin; enoxacin; enoxacin; enoxacin; enoxacin; enoxacin; enoxacin; enoxacin; enoxacin; enoxacin; enoxacin; enoxacin; enoxacin; enoxacin; enoxacin; enoxacin; enoxacin; enoxacin; enoxacin; enoxacin; enoxacin; enoxacin; enoxacin; enoxacin; enoxacin; enoxacin; enoxacin; enoxacin; enoxacin; enoxacin; enoxacin; enoxacin; enoxacin; enoxacin; enoxacin; enoxacin; enoxacin; enoxacin; enoxacin; enoxacin; enoxacin; enoxacin; enoxacin; enoxacin; enoxacin; enoxacin;
```

### Adapter / qwen3

Contains analysis section: no; Forms a complete list: no; Format passes: no.

Repeats enoxacin, with an empty item after the semicolon at the end; no complete usable list is formed. Verbatim identical to the qwen3_nothink response; the empty thinking block does not resolve the repeated output for this item.

Original file: [Adapter / qwen3, row 3](../../../../../%E6%A1%88%E4%BE%8B%E4%B8%8E%E6%BA%90%E7%A0%81-4-%E5%BE%AE%E8%B0%83/examples/thinking-control/Adapter-qwen3-%E5%85%B3%E9%97%AD%E6%80%9D%E8%80%83.jsonl ":ignore").

```text
enoxacin; enoxacin; enoxacin; enoxacin; enoxacin; enoxacin; enoxacin; enoxacin; enoxacin; enoxacin; enoxacin; enoxacin; enoxacin; enoxacin; enoxacin; enoxacin; enoxacin; enoxacin; enoxacin; enoxacin; enoxacin; enoxacin; enoxacin; enoxacin; enoxacin; enoxacin; enoxacin; enoxacin; enoxacin; enoxacin; enoxacin; enoxacin; enoxacin; enoxacin; enoxacin; enoxacin; enoxacin; enoxacin; enoxacin; enoxacin; enoxacin; enoxacin; enoxacin; enoxacin; enoxacin; enoxacin; enoxacin; enoxacin; enoxacin; enoxacin; enoxacin; enoxacin; enoxacin; enoxacin; enoxacin; enoxacin; enoxacin; enoxacin; enoxacin; enoxacin; enoxacin; enoxacin; enoxacin; enoxacin;
```
