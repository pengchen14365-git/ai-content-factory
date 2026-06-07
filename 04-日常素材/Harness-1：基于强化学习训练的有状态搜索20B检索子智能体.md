---
 title: "Harness-1：基于强化学习训练的有状态搜索20B检索子智能体"
 date: "2026年6月7日"
 tags: [Saved]
 source: "AI HOT — 精选"
 link: "https://www.marktechpost.com/2026/06/06/meet-harness-1-a-20b-retrieval-subagent-trained-with-reinforcement-learning-inside-a-stateful-search-harness-on-gpt-oss-20b"
 author: "noreply@aihot.virxact.com (MarkTechPost（RSS）)"
 feedTitle: "AI HOT — 精选"
 summary: "UIUC与Chroma联合推出Harness-1，一个20B参数的检索子智能体。它通过强化学习在一个有状态搜索框架中训练，该框架维护候选池、重要性标注集、证据图和验证记录，由策略决定搜索、筛选、验证及停止的时机。Harness-1在8个基准测试上达到0.730平均curated recall，比下一个最佳开源子智能体高出11.4个百分点，仅落后于Opus-4.6。模型权重和框架代码均已公开。"
 guid: "https://aihot.virxact.com/cmq3eppdj06j7sl97koo7u9xf"
---

# Harness-1：基于强化学习训练的有状态搜索20B检索子智能体

Most search agents are trained as policies over a growing transcript. The model decides how to search. It must also remember what it saw, which evidence matters, and which claims it checked. A team of researchers from University of Illinois Urbana-Champaign, UC Berkeley, and Chroma argues this asks too much. Reinforcement learning ends up optimizing both search decisions and routine bookkeeping at once.

Their answer is **Harness-1**, a 20B retrieval subagent built on gpt-oss-20b. It was trained with reinforcement learning inside a stateful search harness. The harness holds the bookkeeping. The policy keeps the semantic decisions. The weights and harness code are publicly released.

![](https://www.marktechpost.com/wp-content/uploads/2026/06/Screenshot-2026-06-06-at-11.13.42-PM-1.png)

https://arxiv.org/pdf/2606.02373

**What is Harness-1 Actually**
------------------------------

Harness-1 produces a ranked set of documents for a downstream answering model. It does not answer questions itself. It runs inside a state-machine harness centered on a per-episode WORKINGMEMORY.

Each turn works as a loop. The harness renders compact search state along with recent actions. The model emits one structured action. The harness executes it, updates state, and renders the next observation.

**The Stateful Harness: What Moves Out of the Policy**
------------------------------------------------------

The research team calls its principle stateful cognitive offloading. The policy decides what to search, curate, and verify, and when to stop. The harness maintains the recoverable state around those decisions.

That state includes several pieces. A candidate pool holds compressed, deduplicated documents. An importance-tagged curated set is the final output, capped at 30 documents. Tags take four values: very\_high, high, fair, or low. A full-text store keeps every retrieved chunk outside the prompt.

An evidence graph adds structure. A regex extractor scans each chunk for proper nouns, years, and dates. The harness then renders frequent entities, bridge documents, and singletons. Bridge documents contain two or more frequent entities. Singletons appear in one document and suggest follow-up leads.

The policy works through eight tools. These are fan\_out\_search, search\_corpus, grep\_corpus, read\_document, review\_docs, curate, verify, and end\_search. Search outputs are compressed with sentence-BM25, keeping the top four sentences. Two-level deduplication removes repeats by chunk ID and content fingerprint.

One design choice addresses cold starts. The first successful search auto-seeds the curated set with eight reranked results at fair importance. The policy then promotes strong documents and removes weak ones. This turns the task from building from scratch into refinement.

The research team names three requirements for a trainable harness. These are warm-started curation, compact derived-state rendering, and diversity-preserving incentives. Harness-1 implements all three.

**How It is Trained**
---------------------

Training splits along the same line as the harness. Supervised fine-tuning teaches the model to operate the interface. Reinforcement learning improves search decisions over the maintained state.

A single teacher, GPT-5.4, runs live inside the full harness. After filtering, 899 trajectories remain for SFT. The model uses LoRA at rank 32 for three epochs. The step-550 checkpoint initializes RL.

RL uses on-policy CISPO with a 40-turn cap and terminal-only reward. It trains only on SEC queries. Groups with identical rewards are dropped from the gradient. Training ran on Tinker.

The reward separates discovery from selection. It also adds a tool-diversity bonus. Without that bonus, the agent collapses to repeated search. Curated recall then plateaus near 0.53. With the bonus, diversity stabilizes and recall reaches about 0.60.

**The Benchmark Case**
----------------------

Harness-1 was evaluated on eight benchmarks spanning web, finance, patents, and multi-hop QA. The main metric is curated recall: coverage of relevant documents in the final set. Trajectory recall counts evidence encountered anywhere in the episode.

Model

Type

Avg Curated Recall

Avg Trajectory Recall

Harness-1 (20B)

Open small

0.730

0.807

Tongyi DeepResearch 30B

Open small

0.616

0.673

Context-1 (20B)

Open small

0.603

0.756

Search-R1 (32B)

Open small

0.289

0.289

GPT-OSS-20B

Open small

0.262

0.590

Qwen3 (32B)

Open small

0.216

0.446

Opus-4.6

Frontier

0.764

0.794

GPT-5.4

Frontier

0.709

0.752

Sonnet-4.6

Frontier

0.688

0.725

Kimi-K2.5

Frontier

0.647

0.794

GPT-OSS-120B

Frontier

0.496

0.769

_Averages across eight benchmarks, from Figure 1 of the paper. Frontier models run as zero-shot retrievers under the Context-1 harness._

Harness-1 reaches 0.730 average curated recall. That beats the next open subagent, Tongyi DeepResearch 30B, by 11.4 points. Among the frontier searchers tested, only Opus-4.6 scores higher on average.

The transfer pattern is the clearest signal of the mechanism. SFT used four benchmark families; RL used only SEC. On those source-family tasks, Harness-1 gained 7.9 points over the closest open baseline. On four held-out benchmarks, it gained 17.0 points. That is a 2.2x larger gain on tasks furthest from training data.

Ablations support the harness claim. Disabling all harness mechanisms drops Recall by 12.2 percent relative on BrowseComp+. The trained policy keeps searching but cannot rank what it sees.

![](https://www.marktechpost.com/wp-content/uploads/2026/06/Screenshot-2026-06-06-at-11.15.46-PM-1.png)

https://arxiv.org/pdf/2606.02373

**Use Cases**
-------------

The method targets evidence-seeking retrieval where documents support an answer. Several workflows fit this shape.

One is literature and patent review. The evidence graph and curated set help organize many sources. Another is financial-filing analysis. The SEC case study recovers an exact executive-transition date across multiple 8-Ks.

A third is multi-hop fact-checking. The fan\_out\_search and verify tools resolve ambiguous entities before committing. A fourth is modular RAG. The curated set feeds a frozen generator, and better sets yield higher answer accuracy.

**Strengths and Weaknesses**
----------------------------

#### **Strengths**

*   Highest average curated recall among the open models tested, and behind only Opus-4.6 overall.
*   Gains hold on held-out benchmarks, suggesting domain-general search operations.
*   Trained on 4,352 unique items, far fewer than several baselines.
*   Open checkpoint and harness code, servable with common runtimes.

#### **Weaknesses**

*   The evidence graph uses regex extraction, not full entity linking.
*   The verify tool is an LLM proxy that can err on ambiguous claims.
*   Sentence-BM25 compression may drop context tied to discourse structure.
*   The research team reports point estimates without full confidence intervals.

**Key Takeaways**
-----------------

*   Harness-1 is a 20B search agent that moves search bookkeeping into the environment, leaving semantic decisions to the policy.
*   It hits 0.730 average curated recall across eight benchmarks, beating the next open subagent by 11.4 points.
*   Among the searchers tested, only Opus-4.6 scores higher on average curated recall.
*   Gains are largest on held-out benchmarks (+17.0 vs +7.9 points), suggesting the learned search operations transfer.
*   Weights and harness code are public, servable via vLLM, SGLang, or Transformers.

**Marktechpost’s Visual Explainer**
-----------------------------------

Stateful Search Agents 1 / 7

Research Guide

A retrieval subagent trained with reinforcement learning inside a search harness that holds the bookkeeping.

20B · gpt-oss-20b base UIUC · UC Berkeley · Chroma arXiv:2606.02373 Open weights & code

The Core Idea

### Split the work between policy and harness

Most search agents pack search decisions and routine bookkeeping into one growing transcript. Harness-1 separates the two. The paper calls this stateful cognitive offloading.

Policy decides

*   What to search
*   Which documents to keep
*   What claims to verify
*   When to stop

Harness maintains

*   Candidate pool
*   Curated evidence
*   Verification records
*   Context budget

Inside the Harness

### Environment-side working memory

*   **Candidate pool** — compressed, deduplicated documents
*   **Curated set** — importance-tagged, capped at 30 (very\_high / high / fair / low)
*   **Evidence graph** — entities, bridges, and singletons via regex extraction
*   **Verification cache** — claim to document to yes/no verdict
*   **Full-text store** — every retrieved chunk kept outside the prompt
*   **Compression** — sentence-BM25 keeps the top four sentences

Policy Actions

### Eight tools edit the state

fan\_out\_search

search\_corpus

grep\_corpus

read\_document

review\_docs

curate

verify

end\_search

The first successful search auto-seeds the curated set with eight reranked documents at fair importance. The policy then promotes strong documents and removes weak ones.

Training

### SFT to operate the interface, RL to search

**SFT:** GPT-5.4 teacher inside the harness · 899 trajectories · LoRA rank 32 · step-550 checkpoint

**RL:** on-policy CISPO · SEC queries only · 40-turn cap · terminal reward · trained on Tinker

**Data scale:** 4,352 unique training items (899 SFT + 3,453 RL)

Three trainability requirements: warm-started curation, compact derived-state rendering, and diversity-preserving incentives.

Results

### What the numbers show

0.730 average curated recall  
across eight benchmarks

**+11.4 pts** over the next open subagent, Tongyi DeepResearch 30B

Among the searchers tested, only **Opus-4.6** scores higher on average

Transfer: **+17.0** on held-out vs **+7.9** on source-family (2.2x gap)

Ablation: removing all harness mechanisms drops Recall **12.2%** relative

Get Started

### Run it yourself

**Serve:** vLLM, SGLang, or Transformers

**Checkpoint:** pat-jj/harness-1 (Hugging Face, 21B params, BF16)

**Code:** github.com/pat-jj/harness-1

**Paper:** arXiv:2606.02373

Harness-1 returns a curated set of documents for a downstream answering model. It does not answer questions itself.

Curated by **Marktechpost** — practitioner-first AI/ML research, news, and dev tooling for engineers.

* * *

Check out the **[Paper](https://arxiv.org/pdf/2606.02373),** [**Model weights**](https://huggingface.co/pat-jj/harness-1) and **[GitHub Repo](https://github.com/pat-jj/harness-1).** Also, feel free to follow us on **[Twitter](https://x.com/intent/follow?screen_name=marktechpost)** and don’t forget to join our **[150k+ ML SubReddit](https://www.reddit.com/r/machinelearningnews/)** and Subscribe to **[our Newsletter](https://www.aidevsignals.com/)**. Wait! are you on telegram? **[now you can join us on telegram as well.](https://t.me/machinelearningresearchnews)**

Need to partner with us for promoting your GitHub Repo OR Hugging Face Page OR Product Release OR Webinar etc.? **[Connect with us](https://forms.gle/wbash1wF6efRj8G58)**

[![](https://www.marktechpost.com/wp-content/uploads/2026/06/Screenshot-2026-06-05-at-3.40.16-AM.png)](https://tinyurl.com/ms4xwdj4?via=marktechpost)

  [Source](https://www.marktechpost.com/2026/06/06/meet-harness-1-a-20b-retrieval-subagent-trained-with-reinforcement-learning-inside-a-stateful-search-harness-on-gpt-oss-20b)