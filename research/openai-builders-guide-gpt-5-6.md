<!-- Source: https://openai.com/index/builders-guide-to-gpt-5-6/ — captured via Crawl4AI 2026-08-18 -->
[Skip to main content](https://openai.com/index/builders-guide-to-gpt-5-6/#main)
[](https://openai.com/)
  * [Research](https://openai.com/research/index/)
  * Products
  * [Business](https://openai.com/business/)
  * [Developers](https://openai.com/api/)
  * [Company](https://openai.com/about/)
  * [Foundation(opens in a new window)](https://openaifoundation.org/)


Log in[Try ChatGPT(opens in a new window)](https://chatgpt.com/?openaicom-did=839f5688-2404-4c99-8f7a-81670134ccb7&openaicom_referred=true)
  * Research
  * Products
  * Business
  * Developers
  * Company
  * [Foundation(opens in a new window)](https://openaifoundation.org/)


The builder’s guide to GPT‑5.6 | OpenAI
August 13, 2026
Applied AI
# The builder’s guide to GPT‑5.6
Technical lessons from startups in production
Share
Prompt Caching
  * [GPT-5.6 sets a new standard for price-performance](https://openai.com/index/builders-guide-to-gpt-5-6/#gpt-56-sets-a-new-standard-for-price-performance)
  * [A better out-of-the-box experience](https://openai.com/index/builders-guide-to-gpt-5-6/#a-better-out-of-the-box-experience)
  * [Model Selection](https://openai.com/index/builders-guide-to-gpt-5-6/#model-selection)
  * [Evolving the Responses API to architect more efficient agents](https://openai.com/index/builders-guide-to-gpt-5-6/#evolving-the-responses-api-to-architect-more-efficient-agents)
  * [Programmatic Tool Calling](https://openai.com/index/builders-guide-to-gpt-5-6/#programmatic-tool-calling)
  * [Multi-agent](https://openai.com/index/builders-guide-to-gpt-5-6/#multi-agent)
  * [Prompt Caching](https://openai.com/index/builders-guide-to-gpt-5-6/#prompt-caching)
  * [Conclusion](https://openai.com/index/builders-guide-to-gpt-5-6/#conclusion)


  * [GPT-5.6 sets a new standard for price-performance](https://openai.com/index/builders-guide-to-gpt-5-6/#gpt-56-sets-a-new-standard-for-price-performance)
  * [A better out-of-the-box experience](https://openai.com/index/builders-guide-to-gpt-5-6/#a-better-out-of-the-box-experience)
  * [Model Selection](https://openai.com/index/builders-guide-to-gpt-5-6/#model-selection)
  * [Evolving the Responses API to architect more efficient agents](https://openai.com/index/builders-guide-to-gpt-5-6/#evolving-the-responses-api-to-architect-more-efficient-agents)
  * [Programmatic Tool Calling](https://openai.com/index/builders-guide-to-gpt-5-6/#programmatic-tool-calling)
  * [Multi-agent](https://openai.com/index/builders-guide-to-gpt-5-6/#multi-agent)
  * [Prompt Caching](https://openai.com/index/builders-guide-to-gpt-5-6/#prompt-caching)
  * [Conclusion](https://openai.com/index/builders-guide-to-gpt-5-6/#conclusion)


## GPT‑5.6 sets a new standard for price-performance
The GPT‑5.6 model family makes frontier-level agent performance dramatically more affordable, while also advancing the frontier of what is possible.
In this guide, we show how startups are using smarter model selection and new API controls that help with reasoning continuity, multi-agent orchestration, and programmatic tool calling to build faster, more capable agents at a fraction of the cost.
## A better out-of-the-box experience
Since GPT‑5, each model generation has sought to tackle longer-horizon tasks with fewer tokens. GPT‑5.6 continues that trajectory: stronger agent performance, lower costs, with minimal changes to the underlying harness.
Artificial Analysis Coding Index
Cost Latency Output tokensCost
$0$1,000$2,000$3,0004050607080Index scoreAPI cost (USD)GPT-5.6 SolGPT-5.6 TerraGPT-5.6 LunaGPT-5.5Claude Fable 5Claude Opus 4.8Gemini 3.1 Pro Preview
The improvements in top-line cost efficiency are compounded with increased accuracy at lower reasoning efforts. For example, on Agents’ Last Exam, GPT‑5.6 Sol at “low” reasoning outperformed GPT‑5.5 at “high” reasoning when the harness was kept constant. We’ve seen similar success stories in production testing where startups report seeing significant cost improvements across a range of workflows by reducing the reasoning effort from the prior defaults.
> “We dropped GPT‑5.6 into our harness, and low reasoning effort gave us our best results. It knew when the data just wasn’t there, didn’t chase bad leads, and got to the right answer with fewer tokens.”
— Izzy Miller, AI Research Lead, [Hex⁠(opens in a new window)](https://hex.tech/)
## Model Selection
Historically, upgrading to a flagship model at the highest reasoning available has been the best option for long-horizon use cases. This has been in large part due to these models being significantly more capable than cost-optimized models at handling longer contexts and tool calling. This has changed with the 5.6-family: with more test-time compute, Luna and Terra can often perform similar to GPT‑5.4 and 5.5 while being significantly cheaper.
1 of 3
> “Luna keeps 98% of GPT‑5.5’s extraction accuracy at one-eighteenth the cost. That gives our agents high-quality document understanding at a price that makes it practical across many more workflows.”
— Serhii Shchoholiev, Engineering Lead, Agents, [Hypha⁠(opens in a new window)](https://www.hypha.co/)
> “We ran Luna on 106 of our hardest browser tasks, and it completed 78% of them for about $14. The current SOTA model reached 80% for roughly $235. That combination of capability and cost is remarkable for browser agents.”
— Gregor Zunic, Co-Founder, [Browser Use⁠(opens in a new window)](https://browser-use.com/)
> “Luna is now our default model for a number of high-throughput code retrieval and decision modeling workloads. For a key code exploration task in our multi-agent engineering system, it lowered inference costs by 64%, cut response time by 90%, and improved F1 by five points.”
— Animesh Koratana, Founder and CEO, [PlayerZero⁠(opens in a new window)](https://playerzero.ai/)
  * Hypha
  * Browser Use
  * PlayerZero


Consider tasks in BrowseComp: a search-based benchmark that tests a model’s ability to search for obscure facts. Three months ago, GPT‑5.5 (Extra High) scored 84.36% on this benchmark for a total cost of $33.27. At launch, GPT‑5.6 Luna (Extra High) delivers essentially the same performance, scoring 84.04% at a cost of $1.33. We’ve since reduced prices further. [Read more](https://openai.com/index/advancing-the-price-performance-frontier-with-gpt-5-6/) on our latest price cuts.
BrowseComp
Cost Latency Output tokensCost
$0$7$14$21$28$3530%50%70%90%ScoreAPI cost (USD)GPT-5.6 SolGPT-5.6 Sol UltraGPT-5.6 TerraGPT-5.6 LunaGPT-5.5Claude Mythos PreviewClaude Opus 4.8Gemini 3.1 Pro Preview
The smaller 5.6-family models are a strong fit for high-volume workloads, latency-sensitive interactions, and repeated steps within agentic workflows. For example, if you’re operating a legal-tech startup that parses handwritten memos prior to agentic analysis, instead of using a frontier model for the entire use case, you can now use Terra or Luna for extraction and register significant cost savings.
## Evolving the Responses API to architect more efficient agents
In addition to making GPT‑5.6 more performant out of the box, we also shipped new primitives to the Responses API to unlock further gains. We trained GPT‑5.6 end-to-end with three complementary architectural interventions that enable agents to operate more efficiently:
  1. **Reuse work already performed:** by allowing [reasoning to be persisted⁠(opens in a new window)](https://developers.openai.com/api/docs/guides/reasoning#preserve-reasoning-across-calls) across model turns and using [native compaction⁠(opens in a new window)](https://developers.openai.com/api/docs/guides/compaction) to compress long-running conversations, the model can maintain coherence in its work across longer task horizons without getting confused or having to reconstruct prior context.
  2. **Parallel decomposition where appropriate:** using [native multi-agent orchestration⁠(opens in a new window)](https://developers.openai.com/api/docs/guides/responses-multi-agent) allows coordinating multiple agents across parallel workstreams to finish complex tasks faster.
  3. **Move deterministic work into code:** using [programmatic tool calling⁠(opens in a new window)](https://developers.openai.com/api/docs/guides/tools-programmatic-tool-calling) to filter, aggregate, and orchestrate tool outputs outside the model’s context window, reserving model tokens for judgment and reducing cost, latency, and context rot.


Used together, the difference can be dramatic. For example, on ARC-AGI-3, GPT‑5.6 Sol scored 13.3% with the standard harness. After enabling retained reasoning and compaction, however, the score jumped to 38.3%—while using roughly 6× fewer output tokens. No changes to the model, but nearly three times the performance. You can read more on our [ARC-AGI-3 harness investigation](https://openai.com/index/how-two-settings-tripled-our-arc-agi-3-scores/) here.
## Programmatic Tool Calling
Agentic workflows often involve two kinds of work:
  1. Tasks that require judgment
  2. Work that mostly requires moving, filtering, and combining data


When an agent retrieves 100 filings, filters them by date, and identifies relevant transactions, the model shouldn’t have to reason over every intermediate result in its context window. Programmatic Tool Calling lets GPT‑5.6 write JavaScript to orchestrate tools, run independent calls in parallel, and process their outputs outside the context window. The model is left to focus on what requires intelligence: applying judgment.
> “For financial research, the hard part is reliably pulling filings, coordinating tools, and working through the numbers. In our evaluations, GPT‑5.6 using Programmatic Tool Calling matched our rubric quality while using 21% fewer input tokens. That’s the difference between an agent that can discuss financial research and one that can actually carry it out.”
— Alex Wang, Applied AI, [Rogo⁠(opens in a new window)](https://rogo.com/)
## Multi-agent
On complex, parallelizable tasks, distributing actions and reasoning across multiple agent workstreams enables faster task completion as well as higher intelligence. In these setups, the primary agent is responsible for orchestrating the subagents and delegating tasks to them. The subagents pursue their objectives in parallel and finally pass back their output to the primary agent for final synthesis. Teams can start leveraging multi-agent natively by [enabling multi-agent⁠(opens in a new window)](https://developers.openai.com/api/docs/guides/responses-multi-agent) in the Responses API. This is also how the ultra capability setting in ChatGPT works.
> “Qualia runs teams of agents on open-ended research problems, and GPT‑5.6 Sol just clicked. It showed a marked improvement over GPT‑5.5, finished faster than almost every other model we tested, and quickly became our go-to OpenAI model.”
— E Chi, Founder, [Quadrillion⁠(opens in a new window)](https://quadrillion.io/)
> “GPT‑5.6 is the best orchestrator we’ve seen from OpenAI. We threw six specs at it at once (writing, building, and talking through all of them) and it kept track of everything without the quality falling apart.”
— Jon Bell, Co-founder and CPO, [Obvious⁠(opens in a new window)](https://obvious.ai/)
1 of 2
> “Qualia runs teams of agents on open-ended research problems, and GPT‑5.6 Sol just clicked. It showed a marked improvement over GPT‑5.5, finished faster than almost every other model we tested, and quickly became our go-to OpenAI model.”
— E Chi, Founder, [Quadrillion⁠(opens in a new window)](https://quadrillion.io/)
> “GPT‑5.6 is the best orchestrator we’ve seen from OpenAI. We threw six specs at it at once (writing, building, and talking through all of them) and it kept track of everything without the quality falling apart.”
— Jon Bell, Co-founder and CPO, [Obvious⁠(opens in a new window)](https://obvious.ai/)
  * Quadrillion
  * Obvious


Although GPT‑5.6 has a strong sense of the appropriate number of subagents and when to spawn them, multi-agent behavior is very steerable. Instructing the model on when to invoke subagents can increase the likelihood of spawning agents only in situations where the additional token expenditures would result in better performance.
## Prompt Caching
Across the entire family of models, the prompt cache TTL has been extended to a minimum of 30 minutes and cache breakpoints can now be set deterministically within a model’s context window. This has enabled startups to significantly improve their cache hit rate.
> “We added cache breakpoints and workspace-specific keys to a shared 29,000-token prompt and cut uncached input by 28%. The 30-minute cache window was a big unlock too: our agents could reuse the same context across runs instead of starting from scratch.”
— Lorenzo Gentile, AI Engineer, [Ploy⁠(opens in a new window)](https://ploy.ai/)
In addition to setting cache breakpoints, continuing to use an appropriate [prompt_cache_key⁠(opens in a new window)](https://developers.openai.com/api/docs/guides/prompt-caching#improve-cache-hit-rates-with-a-prompt-cache-key) increases the likelihood of requests landing on the same inference engine as one that previously served the same prefix, thereby reducing latency.
## Conclusion
What stands out across these examples is how much the economics of building agents have changed.
Use cases that once required a frontier model at every step can now achieve comparable or better results at a fraction of the cost by using smaller models, tuning reasoning effort, and making efficient architectural choices.
We're excited to see what you all build!
  * 2026
  * API Platform


## About the authors
This guide was developed by [Samarth Madduru⁠(opens in a new window)](https://www.linkedin.com/in/samarthmadduru/), [Prashant Mital⁠(opens in a new window)](https://www.linkedin.com/in/pmital/), [Dave Leo⁠(opens in a new window)](https://www.linkedin.com/in/davidanthonyleo/), and [Julien Reiman⁠(opens in a new window)](https://www.linkedin.com/in/julienreiman/), based on their experience working closely with startups building on GPT‑5.6 from early testing through production.
## Keep reading
[View all](https://openai.com/news/)
![Derya Unutmaz card image](https://images.ctfassets.net/kftzwdyauwt9/6By12NX9sglstfwFKQTzYB/a28d6f84e91a8dae838f240db4c2524c/derya_1x1.png?w=3840&q=90&fm=webp)
[ How GPT-5 helped immunologist Derya Unutmaz solve a 3-year-old mystery Applied AIJun 23, 2026 ](https://openai.com/index/gpt-5-immunology-mystery/)
![Boston's Children Hospital NEJM > Cover image](https://images.ctfassets.net/kftzwdyauwt9/1VrF8z79R2Khy4PWmHRKME/38077532a039ebb39f054e84d6ae89c7/Art_Card.png?w=3840&q=90&fm=webp)
[ Using AI to help physicians diagnose rare genetic diseases affecting children Applied AIJun 18, 2026 ](https://openai.com/index/diagnose-rare-childhood-diseases/)
![Frame \(4\)](https://images.ctfassets.net/kftzwdyauwt9/1cXwxAxok14lQF5HiEO4zi/567dbae4950956776ef4a28f9790df4c/Frame__4_.png?w=3840&q=90&fm=webp)
[ How an astrophysicist uses Codex to help simulate black holes Applied AIJun 11, 2026 ](https://openai.com/index/using-codex-to-simulate-black-holes/)
Research
  * [Research Index](https://openai.com/research/index/)
  * [Research Overview](https://openai.com/research/)
  * [Economic Research](https://openai.com/signals/)


Latest Advancements
  * [GPT-5.6](https://openai.com/index/gpt-5-6/)
  * [GPT-5.5](https://openai.com/index/introducing-gpt-5-5/)
  * [GPT-5.4](https://openai.com/index/introducing-gpt-5-4/)


Safety
  * [Safety Approach](https://openai.com/safety/)
  * [Deployment Safety(opens in a new window)](https://deploymentsafety.openai.com/)
  * [Security & Privacy](https://openai.com/security-and-privacy/)
  * [Trust & Transparency](https://openai.com/trust-and-transparency/)


Products
  * [ChatGPT(opens in a new window)](https://chatgpt.com/?openaicom-did=839f5688-2404-4c99-8f7a-81670134ccb7&openaicom_referred=true)
  * [ChatGPT Business(opens in a new window)](https://chatgpt.com/business/?openaicom-did=839f5688-2404-4c99-8f7a-81670134ccb7&openaicom_referred=true)
  * [ChatGPT Enterprise(opens in a new window)](https://chatgpt.com/business/enterprise/?openaicom-did=839f5688-2404-4c99-8f7a-81670134ccb7&openaicom_referred=true)
  * [ChatGPT for Education(opens in a new window)](https://chatgpt.com/business/education/?openaicom-did=839f5688-2404-4c99-8f7a-81670134ccb7&openaicom_referred=true)
  * [Codex](https://openai.com/codex/)
  * [Release Notes](https://openai.com/products/release-notes/)


API Platform
  * [Overview](https://openai.com/api/)
  * [API Log In(opens in a new window)](https://platform.openai.com/login)
  * [Docs(opens in a new window)](https://developers.openai.com/api/docs)


Business
  * [Overview](https://openai.com/business/)
  * [Solutions](https://openai.com/solutions/)
  * [Resources](https://openai.com/business/learn/)
  * [Customer Stories](https://openai.com/business/customer-stories/)
  * [Partner Network](https://openai.com/business/partners/)
  * [Contact Sales](https://openai.com/contact-sales/)


Developers
  * [Apps SDK(opens in a new window)](https://developers.openai.com/apps-sdk)
  * [Open Models](https://openai.com/open-models/)
  * [Docs(opens in a new window)](https://developers.openai.com/)
  * [Resources(opens in a new window)](https://developers.openai.com/learn)
  * [Developer Forum(opens in a new window)](https://community.openai.com/)


Company
  * [About Us](https://openai.com/about/)
  * [Our Charter](https://openai.com/charter/)
  * [Careers](https://openai.com/careers/)
  * [News](https://openai.com/news/)


Support
  * [Help Center(opens in a new window)](https://help.openai.com/)


More
  * [Stories](https://openai.com/stories/)
  * [Academy](https://openai.com/academy/)
  * [Supply Co.](https://openai.com/supply/)
  * [Livestreams](https://openai.com/live/)
  * [Podcast](https://openai.com/podcast/)
  * [RSS](https://openai.com/news/rss.xml)


Terms & Policies
  * [Terms of Use](https://openai.com/policies/terms-of-use/)
  * [Privacy Policy](https://openai.com/policies/privacy-policy/)
  * [Other Policies ](https://openai.com/policies/)


[(opens in a new window)](https://x.com/OpenAI)[(opens in a new window)](https://www.youtube.com/OpenAI)[(opens in a new window)](https://www.linkedin.com/company/openai)[(opens in a new window)](https://github.com/openai)[(opens in a new window)](https://www.instagram.com/openai/)[(opens in a new window)](https://www.tiktok.com/@openai)[(opens in a new window)](https://discord.gg/openai)
OpenAI © 2015–2026Manage Cookies
EnglishUnited States
We use cookies
We use cookies to help this site function, understand service usage, and support marketing efforts. Visit Manage Cookies to change preferences anytime. View our [Cookie Policy](https://openai.com/policies/cookie-policy/) for more info.
Manage CookiesReject non-essentialAccept all
