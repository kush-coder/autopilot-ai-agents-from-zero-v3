# Reference Annotation Review of Validation Samples

The following are draft recommendations formed by comparing against the given original text. They have not yet been externally professionally confirmed, have not been written back to the dataset, and have not been used to modify old scores. All recommended terms can be found verbatim in the corresponding input; this only demonstrates textual basis, not that the selected terms are optimal. Different articles are not required to have a fixed number of keywords.

## Item 1

| Item               | Record                                                                                                               |
| ------------------ | -------------------------------------------------------------------------------------------------------------------- |
| Original reference answer       | Single-heading excavation roadway; cooling test system; refrigeration cooling; enthalpy difference; coefficient of performance                                                                   |
| Recommended answer (draft) | Single-heading excavation roadway; metal mine deep mining cooling test system; refrigeration cooling; enthalpy difference value; coefficient of performance                                                 |
| Basis for modification           | Retains the research object, the full name of the test system, the cooling method, and the core calculated quantity. The test system and enthalpy difference value are expanded according to the original wording to avoid treating name differences directly as content errors. |
| Full name           | Single-heading excavation roadway and coefficient of performance are retained; the system name is recorded according to the full name in the original text.                                                               |
| Topical relevance         | Focuses on the roadway cooling object, test method, and calculated quantities.                                                                               |
| Basis in original text           | The original reference terms can be compared with the original text, in which cooling test system and enthalpy difference use abbreviated forms.                                                             |
| Term selection scope           | For now, not all four test conditions and values are included; the granularity of enthalpy difference remains to be unified.                                                                 |
| Items to confirm           | The annotation granularity of "enthalpy difference" versus "enthalpy difference value" and whether the full system name should be retained every time need to be standardized and professionally reviewed.                                       |

<details>
<summary>Compare with complete original text</summary>

```text
关键词抽取：
金属矿山独头掘进巷道制冷系数是计算独头掘进巷道降温需冷量非常重要的参数之一,关系到能否达到预期降温效果及影响着降温工程的的经济投入。利用“金属矿山深部开采降温试验系统”分别模拟通风降温、加大风量降温、制冷降温、加大制冷降温4种条件下独头掘进巷道的降温过程,并分析独头掘进巷道降温效果,在通风及加大风量降温后,独头掘进巷道内温度先下降然后趋于稳定,再也无法下降,只有通过制冷措施,对独头掘进工作面进行降温。通过监测数据的焓差值计算出降温制冷系数,同时利用多次试验得出制冷系数范围在1．38~1．68,进而为独头掘进巷道降温设计提供设计依据。
```

</details>

## Item 2

| Item               | Record                                                                                                       |
| ------------------ | ---------------------------------------------------------------------------------------------------------- |
| Original reference answer       | Neural network; target recognition; BP algorithm; moment invariants                                                                          |
| Recommended answer (draft) | BP neural network; aerial fighter target recognition; invariant moment theory; Levenberg-Marguardt optimization algorithm                                         |
| Basis for modification           | Highlights the recognition task, the input feature method, and the optimization algorithm emphasized in the article; uses complete expressions from the original text to replace generic terms or expressions that do not explicitly appear.             |
| Full name           | Uses BP neural network and aerial fighter target recognition to clarify the method and task object.                                                        |
| Topical relevance         | Centers on the recognition method, input features, and the emphasized optimization algorithm.                                                                   |
| Basis in original text           | Neural network and target recognition are generalizations from the original text; the relationship between BP algorithm, moment invariants, and the original terms remains to be verified.                                   |
| Term selection scope           | Aircraft model and all training algorithms are not included for now as method details; the complete spelling corresponding to LM retains the doubtful point from the original text.                                |
| Items to confirm           | The spelling of Levenberg-Marguardt is retained as in the original text; the suspected spelling issue must be checked against the original source; the relationship between "moment invariants" and "invariant moment theory" requires professional confirmation. |

<details>
<summary>Compare with complete original text</summary>

```text
提出了一种利用BP神经网络用于空中战机目标识别的方法.首先,分别用300张不同姿态的F-16和F-22战斗机图片建立样本图库.其次,利用不变矩理论,提取图片的不变矩作为神经网络的输入量,分别采用基本梯度下降算法、有动量和自适应学习速率梯度下降算法和Levenberg-Marguardt优化算法训练BP网络.然后从样本图库中随机抽取两种型号飞机图片各30张作为空中打击目标进行识别,结果表明采用LM优化算法的BP网络具有一定的抗噪声能力.
识别出上文中的关键词
```

</details>

## Item 3

| Item               | Record                                                                                                         |
| ------------------ | ------------------------------------------------------------------------------------------------------------ |
| Original reference answer       | Ionic liquid; sugarcane bagasse; eucalyptus wood; saccharification yield                                                                                |
| Recommended answer (draft) | Ionic liquid; EmimAc; AmimCl; sugarcane bagasse; eucalyptus wood; enzymatic saccharification method; pretreatment                                                         |
| Basis for modification           | Covers two treatment materials, two types of biomass, the detection method, and the treatment topic; the original text does not directly state "saccharification yield," so it is not used unconfirmed as the sole standard term. |
| Full name           | Retains the abbreviations of the two ionic liquids and does not expand chemical names on its own.                                                                   |
| Topical relevance         | Covers treatment materials, biomass objects, and pretreatment effect research.                                                                   |
| Basis in original text           | Saccharification yield does not appear directly; the original text only explicitly states enzymatic saccharification method and effect comparison.                                                     |
| Term selection scope           | The draft includes specific treatment materials and methods, and does not include temperature, duration, or multiples.                                                         |
| Items to confirm           | EmimAc and AmimCl appear only as abbreviations in the text, and chemical names are not completed on their own; whether saccharification yield should be used as an implicit evaluation indicator needs to be checked against the original text.            |

<details>
<summary>Compare with complete original text</summary>

```text
采用酶解糖化法检测离子液体EmimAc和AmimCl对生物质(甘蔗渣和桉木)的预处理效果,考察了温度、时间和固/液质量比对离子液体预处理效果的影响.结果表明,2种离子液体对2种生物质的最佳预处理温度均为140℃,固液质量比均为1∶15,EmimAc对桉木和甘蔗渣的预处理时间分别是12和4h,而AmimCl所需的时间分别是14和8h,EmimAc对桉木和甘蔗渣的预处理效果分别是传统方法的13.931和3.886倍,而AmimCl对这2种生物质分别是传统方法的4.665和2.835倍.可见EmimAc的预处理效果优于AmimCl.
识别出文本中的关键词
```

</details>

## Item 4

| Item               | Record                                                                                                 |
| ------------------ | ---------------------------------------------------------------------------------------------------- |
| Original reference answer       | An County; citrus scab; planting area; fruit industry production; occurrence and damage; introduction; seedlings; disease occurrence; disease                                       |
| Recommended answer (draft) | Citrus scab; Wan'an County; fruit industry production                                                                           |
| Basis for modification           | Retains the complete disease name and region name, removes the truncated "An County"; reduces overlapping generic terms such as area, disease occurrence, and disease, and selects terms around regional disease impact. |
| Full name           | An County should be restored to Wan'an County according to the original text; citrus scab is retained in full.                                                       |
| Topical relevance         | The article's focus is the local disease and its impact on fruit industry production.                                                             |
| Basis in original text           | Disease name, region, seedlings, introduction, etc. can all be found in the original text; having a basis does not mean every term must be selected.                                 |
| Term selection scope           | Reduces generic terms such as disease occurrence and disease, and area details; whether the introduction factor is included separately remains to be determined according to task needs.                               |
| Items to confirm           | The original text's 2120/3000 is approximately 70.7%, which is inconsistent with the written 73%; the original source needs to be checked; this revision does not modify the input or values.               |

<details>
<summary>Compare with complete original text</summary>

```text
柑桔疮痂病是柑桔重要病害之一。近年来，由于苗木的调运引种和生产上的疏忽，柑桔疮痂病在万安县发生危害有加重趋势，全县柑桔种植面积3000hm2，发病面积2120 hm2，占柑桔种植面积的73%，对全县果业生产造成严重威胁。
关键词识别
```

</details>

## Item 5

| Item               | Record                                                                                                     |
| ------------------ | -------------------------------------------------------------------------------------------------------- |
| Original reference answer       | Astrometry; atmospheric effects; method: numerical                                                                              |
| Recommended answer (draft) | Ground-based GPS (Global Positioning System); atmospheric water vapor; water vapor tomography technology; GAMIT software; severe convective weather    |
| Basis for modification           | The recommended terms directly correspond to the observation technology, research object, processing method, software, and application scenario in the abstract; the relationship between the current reference terms and these topics is unclear. |
| Full name           | Retains the parenthesized full names of ground-based GPS and water vapor tomography as in the original text.                                                                  |
| Topical relevance         | The abstract centers on water vapor observation, inversion, and severe convective weather applications.                                                                 |
| Basis in original text           | The original references astrometry, atmospheric effects, and method: numerical do not appear with these exact wordings and may come from another domain classification.                            |
| Term selection scope           | First proposes an abstract extraction draft; it must be confirmed whether this task is to extract keywords from the original text or to assign domain classification terms.                                     |
| Items to confirm           | The original annotations may use domain classification terms, and the data source and task definition need to be checked; the way parenthesized full names are retained should also be unified in new annotations.             |

<details>
<summary>Compare with complete original text</summary>

```text
地基GPS(Global Positioning System)探测大气水汽主要包括3个方面的内容:一是观测天顶方向的大气水汽总量(Precipitable Water vapor,PW);二是遥测倾斜的信号路径上的水汽总量(Slant-path Water vapor,SW);三是应用组网的GPS站倾斜路径观测反演局地上空的水汽三维信息,即水汽层析(water vapor tomography)技术.简单介绍了上海地区稠密的地基GPS网,并且在该网的基础上通过GAMIT软件计算出的整层水汽PW和各个方向上的梯度信息及观测残差,来获得GPS测定的SW,运用层析的技术可获得上海地区水汽的三维分布信息.以2008年8月25日上海罕见的大暴雨为例,分析了水汽三维结果在强对流天气中的应用.
关键词识别
```

</details>

## Item 6

| Item               | Record                                                                                                                                  |
| ------------------ | ------------------------------------------------------------------------------------------------------------------------------------- |
| Original reference answer       | Shepody; potato; Yulin City; planting performance; French fries; hybrid breeding; extension cultivation; trial planting; edible quality; technical introduction; experiment station; agricultural science institute; Canada; high yield; sexual; approval; sandy beach; variety; agriculture; female parent |
| Recommended answer (draft) | Shepody; Yulin City; planting performance; extension cultivation; French fry quality; edible quality                                                                                     |
| Basis for modification           | Prioritizes annotating the main variety, trial region, and planting performance; parent numbers have a basis in the original text but cannot replace the main variety. "Potato" does not appear directly in the given text, so this draft does not add it.                |
| Full name           | Retains Shepody, Yulin City, and French fry quality, avoiding only generic terms such as variety or French fries.                                                                                |
| Topical relevance         | The topic is the planting performance and cultivation of this variety in the local area.                                                                                                  |
| Basis in original text           | Potato does not appear directly in the given input; parent numbers have a basis in the original text, but F68050 does not.                                                                       |
| Term selection scope           | The draft selects the main variety and cultivation performance; whether parent, introduction year, and institutions are included requires unified rules.                                                                      |
| Items to confirm           | The crop category must be confirmed by checking the source; suspected OCR errors such as "弓1人" and "栽·培" need re-checking; whether parent information is included belongs to the term-selection scope agreement.                                      |

<details>
<summary>Compare with complete original text</summary>

```text
识别出下文中的关键词：
夏波蒂是加拿大福瑞克通农业试验站用"F58050"为 母本,"Bakeking"为父本经有性杂交育成,1987年引入我国试种,未经过审定或认定,但被辛普劳公司作为炸条品 种在各地种植.2003年由榆林市农科所弓1人我市试种,通过5年观察,该品种产量高,炸条品质和食用品质优良,适 宜在我市北部风沙滩水地区推广栽培,现将种植表现及栽·培技术简介如下:
```

</details>

## Item 7

| Item               | Record                                                                                                           |
| ------------------ | -------------------------------------------------------------------------------------------------------------- |
| Original reference answer       | Althusser; ideological function; Marxism; theoretical practice; ideological structure; thinker; structuralism; representative figure; sorting out; logic; science; interpretation; association; France; status |
| Recommended answer (draft) | Louis Althusser; Western Marxism; structuralism; ideological function; scientific theoretical practice                                              |
| Basis for modification           | Retains the full name of the figure, intellectual background, and key discussion points; removes terms with weak summarizing power such as status, association, and sorting out, and avoids splitting "ideological function" into shorter parts.               |
| Full name           | Retains the full name of the figure, Louis Althusser, and phrases such as ideological function.                                                                |
| Topical relevance         | Focuses on the figure's intellectual background and discussion of ideological function.                                                                         |
| Basis in original text           | Most of the original reference terms have a lexical basis, but sorting out, association, status, and similar terms are difficult to use independently to summarize the topic of this text.                                             |
| Term selection scope           | Reduces discourse actions and generic terms; the granularity of theoretical concepts remains an item for professional review.                                                               |
| Items to confirm           | The boundaries and granularity between philosophical concepts still require domain review; the current recommendation emphasizes the topic of the given abstract and does not claim to be the only standard answer.                       |

<details>
<summary>Compare with complete original text</summary>

```text
抽取出下文中的关键词：
作为20世纪西方马克思主义代表人物的法国思想家路易·阿尔都塞,以其对马克思理论的结构主义解读而闻名.在其追寻"科学的理论实践"的一整套思想中,关于意识形态的理论占据了十分重要的地位.本文将着重探讨阿尔都塞关于意识形态功能的论述,以期对其意识形态构架的内在逻辑和关联进行梳理和评判.
```

</details>

## Item 8

| Item               | Record                                                                                                       |
| ------------------ | ---------------------------------------------------------------------------------------------------------- |
| Original reference answer       | Enrofloxacin; Japanese eel; residue; high-performance liquid chromatography                                                                      |
| Recommended answer (draft) | High-performance liquid chromatography; Japanese eel; enrofloxacin; ciprofloxacin; drug residue; withdrawal period                                                  |
| Basis for modification           | Retains the detection method, research object, and complete drug names, adds the metabolite explicitly mentioned in the original text and the research result topic; uses "drug residue" to clarify the object of residue. |
| Full name           | Retains the research object and the complete names of the two drugs according to the original text, without translating on its own.                                                         |
| Topical relevance         | Centers on the detection method, drug residue, and withdrawal period research.                                                                       |
| Basis in original text           | The original reference terms all have a basis; ciprofloxacin and withdrawal period are also explicit content in the original text.                                                       |
| Term selection scope           | Whether to add metabolites and result topics belongs to the term-selection scope; not all tissues or dosing values are listed item by item.                                     |
| Items to confirm           | Whether ciprofloxacin and withdrawal period should be listed as keywords needs to be confirmed according to the annotation scope; drug names are kept as in the original text and are not translated or replaced.                 |

<details>
<summary>Compare with full original text</summary>

```text
抽取出文本中的关键词：
采用高效液相色谱法检测日本鳗鲡肌肉、血清、肠、鳃和肝脏组织中恩诺沙星及其代谢物环丙沙星的残留.方法的日内和日间变异系数分别为1.86%和2.53%,标准添加回收率为(95±6)%;最低测量限为1.0 μg/kg.用现场试验方法研究恩诺沙星在鳗鱼体内的代谢残留规律.对约50 g鳗鱼按9 mg/kg鱼体重每天给药2次,连续投喂7 d.给药期间鳗鱼体内的药物含量呈锯齿状上升,停药60 d后鳗鱼肠、鳃和肝脏组织中药物即下降至1～5 μg/kg.肌肉和血清中药物残留到90 d,分别消除至3 μg/kg和4 μg/kg.所测组织的药物残留至停药120 d后降到检测限以下.故鳗鱼的停药期不应低于120 d.
```

</details>

## Item 9

| Item               | Record                                                                                         |
| ------------------ | -------------------------------------------------------------------------------------------- |
| Original reference answer       | Soybean peptide; activated carbon; AB-8 resin; decolorization                                                                |
| Suggested answer (draft) | Soybean peptide; activated carbon; AB-8 type resin; decolorization process; orthogonal experiment                                                 |
| Basis for revision           | Retain the treatment target, the two materials, and the process optimization method; for AB-8 type resin, use the full name as it first appears in the original text.                 |
| Full name           | For AB-8 type resin, use the complete form from its first occurrence in the original text; the correspondence between the two forms is recorded separately.                                 |
| Topic relevance         | Covers the treatment target, decolorization materials, process, and optimization method.                                                     |
| Original-text basis           | The original reference terms have a basis in the original text or a clear abbreviated-form basis; a difference in naming does not automatically equal a semantic error.                                   |
| Term selection scope           | It is suggested to include the orthogonal experiment emphasized in the title, but not to include all process conditions and effect percentages for now.                               |
| Items to confirm           | AB-8 type resin and AB-8 resin can be recorded as corresponding expressions within the text; whether this correspondence should be used in scoring should be agreed separately, and the previous scoring remains unchanged. |

<details>
<summary>Compare with full original text</summary>

```text
关键词识别：
题目：正交试验优化大豆多肽脱色工艺
摘要：对活性炭和AB-8型树脂分步处理大豆多肽的脱色工艺进行优化.以脱色率和肽损失率为指标,考察活性炭用量、脱色时间、脱色温度、脱色pH值对大豆多肽液脱色的影响,并通过正交试验进行优化.结果表明:活性炭脱色最佳条件为活性炭用量2.0％(m/m)、脱色时间50min、脱色温度55℃、pH8.0,此时大豆多肽液脱色率达到57.13％,肽损失率11.37％.用AB-8树脂(0.5g/mL)对活性炭脱色处理过的大豆肽液进行再次脱色处理,脱色9h后脱色率57.99％,肽损失率16.19％.两步脱色后的大豆多肽液总脱色率达到81.97％,肽总损失率26.74％.
```

</details>

## Item 10

| Item               | Record                                                                                         |
| ------------------ | -------------------------------------------------------------------------------------------- |
| Original reference answer       | Political culture; inter-agency competition; enforcement capacity; endogenous demand                                                      |
| Suggested answer (draft) | Level of intellectual property enforcement; political culture theorists; institutional competition theorists; state capacity theorists; enforcement capacity                             |
| Basis for revision           | Cover the article topic and the three explanatory approaches, retaining the original wording; "endogenous demand" has no direct basis in the given abstract, so it is not included in the draft for now. |
| Full name           | It is suggested to retain the topic phrase "level of intellectual property enforcement"; the standardization of the theorist and theory names is yet to be confirmed.                       |
| Topic relevance         | Covers the article topic, the three explanatory approaches, and enforcement capacity.                                                       |
| Original-text basis           | "Endogenous demand" does not appear in the given abstract; this does not mean the full text also lacks it.                                         |
| Term selection scope           | The draft centers on the three approaches and does not expand to concepts outside the abstract; whether to use standardized theoretical terms requires expert review.                         |
| Items to confirm           | Whether the names of the three theorists should be standardized into theoretical names requires domain review; "endogenous demand" may come from outside the abstract, so its source in the original text must be checked. |

<details>
<summary>Compare with full original text</summary>

```text
抽取出文本中的关键词：
美国学者对中国知识产权执法水平的解释形成了三种进路.政治文化论者否认中国古代存在知识产权制度,并将之归结为传统中国的政治文化,认为当代中国的知识产权发展是政治经济权利发展的一部分.机构竞争论者采用了分散式威权主义的分析框架,认为部门之间的竞争会在一定程度上提高知识产权的保护水平.国家能力论者指出,若要提高中国知识产权的保护水平,必须提高国家有关机构的执法能力.在批评三种解释路径的前提性假设的基础上,提出了评述意见.
```

</details>
