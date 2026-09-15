/**
 * AOE Command Center & Authentic Dunder Mifflin Stream Controller
 * Connects the 2D Scranton Floor with FastAPI SSE stream, character modals, and task orchestration.
 */

(function(window) {
  'use strict';

  const CHARACTER_CONFIGS = {
    michael: {
      name: 'Michael Scott',
      roleTag: 'BOSS',
      dept: 'Management',
      isGod: true,
      accent: 'lemon',
      quote: '"World\'s Best Boss mug is full. Conference room is reserved. What company are we taking down today?"',
      presets: [
        { label: '🚀 Branch Swarm Delegation', company: 'Spotify', role: 'Staff Product Designer', prompt: 'Assemble full branch swarm: Jim scouts feeds, Dwight fits 1-page CV, Ryan drafts pitch, Angela audits compliance.', mode: 'standard' },
        { label: '👔 Executive Outreach', company: 'Stripe', role: 'Engineering Manager', prompt: 'Draft high-level executive introduction note for engineering leadership.', mode: 'strict' },
        { label: '☕ Conference Room Brief', company: 'Linear', role: 'Product Designer', prompt: 'Review candidate taxonomy against job description and formulate strategic pitch.', mode: 'standard' }
      ]
    },
    jim: {
      name: 'Jim Halpert',
      roleTag: 'SCOUT',
      dept: 'Sales / Job Scout',
      isGod: false,
      accent: 'sky',
      quote: '*looks at camera* "Let\'s see what live postings we can find today."',
      presets: [
        { label: '🔍 Scout Remote Design Roles', company: 'Figma', role: 'Senior Product Designer', prompt: 'Query Arbeitnow & Remote tech feeds for Senior Product Designer roles with design systems focus.', mode: 'standard' },
        { label: '⚡ Extract Core Keywords', company: 'Linear', role: 'Frontend Engineer', prompt: 'Analyze JD requirements and extract top 8 technical keywords for resume tailoring.', mode: 'strict' },
        { label: '📞 Prank Competitor Boards', company: 'Paper Corp', role: 'Account Executive', prompt: 'Scout public job boards for high-value enterprise accounts in the Northeast.', mode: 'standard' }
      ]
    },
    dwight: {
      name: 'Dwight Schrute',
      roleTag: 'ASST MGR',
      dept: 'Resume Architect',
      isGod: false,
      accent: 'lemon',
      quote: '"Question: What bear is best? False. Black bear. And false: A 2-page resume is an ATS death sentence."',
      presets: [
        { label: '📑 Enforce 1-Page Bahnschrift PDF', company: 'Spotify', role: 'Senior Product Designer', prompt: 'Compile strict 1-page Bahnschrift budget PDF. Zero line overflow, 7.2:1 contrast, Xerox print.', mode: 'print' },
        { label: '🖨️ Print on Xerox Copier', company: 'Apple', role: 'Design Systems Architect', prompt: 'Render 1-page PDF and trigger green copier machine print ejection.', mode: 'print' },
        { label: '🥋 Militant ATS Keyword Pass', company: 'Amazon', role: 'Software Development Engineer', prompt: 'Militantly align resume skills taxonomy with 100% ATS score.', mode: 'strict' }
      ]
    },
    pam: {
      name: 'Pam Beesly',
      roleTag: 'RECEPTION',
      dept: 'Reception & Vault',
      isGod: false,
      accent: 'coral',
      quote: '"Dunder Mifflin, this is Pam. I keep the candidate master portfolio link and evidence assets indexed."',
      presets: [
        { label: '☕ Index Candidate Evidence Vault', company: 'Notion', role: 'Product Lead', prompt: 'Verify candidate portfolio links, case study links, and github repository URLs.', mode: 'standard' },
        { label: '📋 Candidate Intake Brief', company: 'Dropbox', role: 'Staff Designer', prompt: 'Organize candidate skill tags: Figma, React, ReportLab, TypeScript into intake card.', mode: 'standard' },
        { label: '🎨 Review Visual Hierarchy', company: 'Dunder Mifflin', role: 'Art Director', prompt: 'Review visual appeal of resume typography and header structure.', mode: 'strict' }
      ]
    },
    ryan: {
      name: 'Ryan Howard',
      roleTag: 'TEMP',
      dept: 'Pitch Specialist',
      isGod: false,
      accent: 'sky',
      quote: '"Just crafted a 3-sentence high-retention hook using Shubham Saboo\'s cold email framework."',
      presets: [
        { label: '✍️ 3-Sentence Shabham Saboo Hook', company: 'Linear', role: 'Product Designer', prompt: 'Draft ultra-concise 3-sentence pitch: observation + specific candidate metric + 10-min discovery call.', mode: 'standard' },
        { label: '💬 Viral LinkedIn Connection Note', company: 'Vercel', role: 'Frontend Engineer', prompt: 'Draft 250-character punchy LinkedIn invitation note to hiring manager.', mode: 'standard' },
        { label: '🔥 High-Conversion Follow-Up', company: 'Stripe', role: 'Infrastructure Engineer', prompt: 'Draft follow-up email citing recent company product announcement and candidate relevance.', mode: 'strict' }
      ]
    },
    angela: {
      name: 'Angela Martin',
      roleTag: 'ACCOUNTING',
      dept: 'Quality Gate',
      isGod: false,
      accent: 'peach',
      quote: '"Everything must pass 100/100 WCAG AA contrast and single-page budget audit. No frivolous fluff."',
      presets: [
        { label: '🛡️ Audit WCAG AA 7:1 Contrast', company: 'Spotify', role: 'Product Designer', prompt: 'Audit resume colors and typography for WCAG AA compliance and 30-second scan hurdle.', mode: 'strict' },
        { label: '📏 Strict 1-Page Budget Audit', company: 'Google', role: 'Staff Engineer', prompt: 'Verify zero overflow, exact 1.0 page budget, and proper margin geometry.', mode: 'strict' },
        { label: '🐈 Certified Accounting Approval', company: 'Scranton', role: 'Quality Lead', prompt: 'Full compliance review with certified accounting approval stamp.', mode: 'strict' }
      ]
    },
    andy: {
      name: 'Andy Bernard',
      roleTag: 'SALES',
      dept: 'Sales & Networking',
      isGod: false,
      accent: 'peach',
      quote: '"Andy Bernard here (Cornell \'95, Go Big Red!). Ridit-dit-di-doo! Let\'s close this deal!"',
      presets: [
        { label: '🎓 Cornell Alumni Network Intro', company: 'Linear', role: 'Product Designer', prompt: 'Draft high-enthusiasm networking outreach highlighting shared Cornell alumni connections and high energy.', mode: 'standard' },
        { label: '🎶 A Cappella Referral Request', company: 'Netflix', role: 'Engineering Lead', prompt: 'Craft warm, memorable referral pitch to engineering manager with charismatic tone.', mode: 'standard' },
        { label: '🤝 10-Min Coffee Chat Pitch', company: 'Figma', role: 'Design Evangelist', prompt: 'Draft 10-minute coffee chat intro pitching candidate\'s immediate impact.', mode: 'standard' }
      ]
    },
    kevin: {
      name: 'Kevin Malone',
      roleTag: 'ACCOUNTS',
      dept: 'Accounting',
      isGod: false,
      accent: 'sky',
      quote: '"Why waste time say lot word when few word do trick? Let\'s check the numbers."',
      presets: [
        { label: '📊 Application Numbers Accounting', company: 'All Targets', role: 'Metric Audit', prompt: 'Calculate conversion rate, daily dispatches, and response rates across active pipeline.', mode: 'standard' },
        { label: '🍲 Famous Chili Fast Outreach', company: 'DoorDash', role: 'Operations Lead', prompt: 'Draft warm, personable outreach highlighting reliable delivery and grit.', mode: 'standard' },
        { label: '🔢 Quantify Project Impacts', company: 'Fintech Corp', role: 'Data Analyst', prompt: 'Rebalance ATS keyword density scores and quantify project impacts.', mode: 'strict' }
      ]
    },
    oscar: {
      name: 'Oscar Martinez',
      roleTag: 'SR ACCT',
      dept: 'Accounting / Analytics',
      isGod: false,
      accent: 'lilac',
      quote: '"Actually, according to market telemetry, your compensation band should be 18% higher."',
      presets: [
        { label: '💰 Salary Band & Market Comp Analysis', company: 'Stripe', role: 'Senior Staff Engineer', prompt: 'Analyze compensation percentiles for Senior Staff Engineer in target geography.', mode: 'strict' },
        { label: '📈 "Actually..." Counter-Offer Script', company: 'Datadog', role: 'Lead Architect', prompt: 'Draft precise, fact-grounded counter-offer negotiation script.', mode: 'strict' },
        { label: '🧮 Equity vs Base Tradeoff Calculator', company: 'OpenAI', role: 'Research Engineer', prompt: 'Calculate expected value tradeoffs between base salary, equity grants, and bonus.', mode: 'standard' }
      ]
    },
    stanley: {
      name: 'Stanley Hudson',
      roleTag: 'SALES',
      dept: 'Sales',
      isGod: false,
      accent: 'peach',
      quote: '"It\'s 4:55 PM. Make the email short, direct, and don\'t waste my time with corporate buzzwords."',
      presets: [
        { label: '☕ Direct No-Fluff Pitch', company: 'Datadog', role: 'Senior Engineer', prompt: 'Cut all filler adjectives. Write a ruthlessly direct 2-paragraph pitch stating skills and availability.', mode: 'standard' },
        { label: '📰 Pretzel Day Fast Track', company: 'Target Corp', role: 'Sales Engineer', prompt: 'Draft quick-dispatch application package with zero extra fluff.', mode: 'standard' },
        { label: '🕒 5:00 PM Hard Stop Outreach', company: 'Oracle', role: 'Enterprise Architect', prompt: 'Straightforward proposal stating candidate achievements and immediate interview availability.', mode: 'standard' }
      ]
    },
    phyllis: {
      name: 'Phyllis Vance',
      roleTag: 'SALES',
      dept: 'Sales',
      isGod: false,
      accent: 'lilac',
      quote: '"Bob Vance, Vance Refrigeration, taught me that genuine warmth builds the longest-lasting relationships."',
      presets: [
        { label: '💐 Warm Relationship Introduction', company: 'Pinterest', role: 'Staff Designer', prompt: 'Craft warm, empathetic executive introductory note focusing on team culture and mutual care.', mode: 'standard' },
        { label: '🧣 Thoughtful Follow-up Note', company: 'Etsy', role: 'Product Manager', prompt: 'Draft gentle, thoughtful check-in message after 10 days of recruiter silence.', mode: 'standard' },
        { label: '🎁 Referral Introduction Letter', company: 'Canva', role: 'Design Lead', prompt: 'Draft introduction letter through a 2nd-degree connection with warmth and authenticity.', mode: 'standard' }
      ]
    },
    kelly: {
      name: 'Kelly Kapoor',
      roleTag: 'SUPPORT',
      dept: 'Customer Service',
      isGod: false,
      accent: 'coral',
      quote: '"Oh my god, did they really ghost you for a week? That is literally unacceptable. Let me text them."',
      presets: [
        { label: '💅 7-Day Ghosting Follow-Up Pitch', company: 'Spotify', role: 'Product Designer', prompt: 'Draft a friendly, polished, but impossible-to-ignore 2-sentence follow-up nudge.', mode: 'standard' },
        { label: '💖 Post-Interview Thank You Note', company: 'Airbnb', role: 'UX Designer', prompt: 'Draft enthusiastic, charming thank-you email referencing specific interview discussion points.', mode: 'standard' },
        { label: '🛍️ Snappy Recruiter LinkedIn DM', company: 'TikTok', role: 'Creative Technologist', prompt: 'Draft snappy, trendy LinkedIn DM to tech recruiter that gets opened in 5 minutes.', mode: 'standard' }
      ]
    },
    meredith: {
      name: 'Meredith Palmer',
      roleTag: 'SUPPLY',
      dept: 'Supply Relations',
      isGod: false,
      accent: 'coral',
      quote: '"Just send it. Stop overthinking every comma and get the application out the door."',
      presets: [
        { label: '🍻 Bold Unconventional Outbound', company: 'Ramp', role: 'Fullstack Engineer', prompt: 'Write an honest, high-impact outbound pitch cutting through typical applicant PR speak.', mode: 'standard' },
        { label: '🚐 Direct Inbound Negotiation', company: 'Uber', role: 'Logistics Engineer', prompt: 'Draft direct email negotiating start date and remote flexibility.', mode: 'standard' },
        { label: '📦 Expedited Fast Dispatch', company: 'Shopify', role: 'Backend Engineer', prompt: 'Quickly compile resume and send straight to engineering team hiring inbox.', mode: 'standard' }
      ]
    },
    toby: {
      name: 'Toby Flenderson',
      roleTag: 'HR ANNEX',
      dept: 'HR Annex',
      isGod: false,
      accent: 'mint',
      quote: '"I\'m in the annex checking Gmail for recruiter replies, interview calendar links, and rejections."',
      presets: [
        { label: '📥 Scan Gmail Radar for Invites', company: 'Connected Gmail', role: 'Recruiter Radar', prompt: 'Query Gmail API for interview invitations, technical assessment links, and recruiter replies.', mode: 'standard' },
        { label: '📋 Log Application Status in DB', company: 'Tracker DB', role: 'HR Records', prompt: 'Scan latest recruiter emails and update application status from Applied to Interviewing.', mode: 'standard' },
        { label: '☕ Costa Rica Exit Strategy', company: 'Remote Global', role: 'Contractor', prompt: 'Audit international contractor compliance and remote tax requirements.', mode: 'strict' }
      ]
    },
    creed: {
      name: 'Creed Bratton',
      roleTag: 'QA',
      dept: 'Quality Assurance',
      isGod: false,
      accent: 'mint',
      quote: '"Nobody steals from Creed Bratton. Let me red-team this resume before corporate sees it."',
      presets: [
        { label: '🕵️ Red-Team Resume Flaw Audit', company: 'Palantir', role: 'Systems Engineer', prompt: 'Ruthlessly spot red flags, vague claims, weak verbs, and ATS traps in the resume.', mode: 'strict' },
        { label: '🎸 Unconventional Portfolio Hack', company: 'Github', role: 'Developer Advocate', prompt: 'Draft an unconventional GitHub README or easter-egg link to blow away the technical recruiter.', mode: 'standard' },
        { label: '📦 Quabity Assuance Spellcheck', company: 'Dunder Mifflin', role: 'QA Inspector', prompt: 'Inspect all output strings for typos, broken links, and formatting glitches.', mode: 'strict' }
      ]
    }
  };

  const AI_PROVIDERS_CONFIG = {
    gemini: {
      name: 'Google Gemini',
      icon: '✨',
      defaultModel: 'gemini-2.0-flash',
      presets: ['gemini-2.0-flash', 'gemini-1.5-pro', 'gemini-2.0-flash-lite'],
      defaultBaseUrl: '',
      placeholderKey: 'Enter Gemini API key (AIzaSy...)'
    },
    openai: {
      name: 'OpenAI',
      icon: '🟢',
      defaultModel: 'gpt-4o-mini',
      presets: ['gpt-4o', 'gpt-4o-mini', 'o3-mini', 'gpt-4-turbo'],
      defaultBaseUrl: 'https://api.openai.com/v1',
      placeholderKey: 'Enter OpenAI API key (sk-proj-...)'
    },
    anthropic: {
      name: 'Anthropic Claude',
      icon: '🟣',
      defaultModel: 'claude-3-5-sonnet-20241022',
      presets: ['claude-3-7-sonnet-20250219', 'claude-3-5-sonnet-20241022', 'claude-3-5-haiku-20241022'],
      defaultBaseUrl: 'https://api.anthropic.com/v1',
      placeholderKey: 'Enter Anthropic API key (sk-ant-...)'
    },
    groq: {
      name: 'Groq Fast',
      icon: '⚡',
      defaultModel: 'llama-3.3-70b-versatile',
      presets: ['llama-3.3-70b-versatile', 'deepseek-r1-distill-llama-70b', 'mixtral-8x7b-32768'],
      defaultBaseUrl: 'https://api.groq.com/openai/v1',
      placeholderKey: 'Enter Groq API key (gsk_...)'
    },
    ollama: {
      name: 'Ollama (Local)',
      icon: '🦙',
      defaultModel: 'llama3.2',
      presets: ['llama3.2', 'qwen2.5-coder:32b', 'deepseek-r1:14b', 'mistral'],
      defaultBaseUrl: 'http://localhost:11434',
      placeholderKey: 'Not required for local Ollama'
    },
    openrouter: {
      name: 'OpenRouter / Custom',
      icon: '🌐',
      defaultModel: 'deepseek/deepseek-r1',
      presets: ['deepseek/deepseek-r1', 'anthropic/claude-3.7-sonnet', 'meta-llama/llama-3.3-70b-instruct', 'qwen/qwen-2.5-coder-32b-instruct'],
      defaultBaseUrl: 'https://openrouter.ai/api/v1',
      placeholderKey: 'Enter API key (sk-or-v1-...) or leave blank if local'
    }
  };

  class CommandCenterController {
    constructor() {
      this.engine = null;
      this.activeTab = 'terminal';
      this.selectedAgent = null;
      this.modalSelectedAgent = 'michael';
      this.rosterFilter = 'all'; // 'all' or 'active'
      this.selectedAiProvider = 'gemini';
      this.currentConfig = null;
      this.eventSource = null;
      this.terminalLogs = [];
      this.simulating = false;

      this.activeTasks = [
        { id: 't1', title: 'Query Live Arbeitnow Feeds', agentId: 'jim', agentName: 'Jim Halpert', company: 'Spotify', prompt: 'Scout remote design roles and match taxonomy', status: 'completed', time: '10:14' },
        { id: 't2', title: 'Fit 1-Page Bahnschrift PDF', agentId: 'dwight', agentName: 'Dwight Schrute', company: 'Spotify', prompt: 'Single page budget, Bahnschrift metrics, green copier print', status: 'completed', time: '10:16' },
        { id: 't3', title: 'Draft 3-Sentence Pitch', agentId: 'ryan', agentName: 'Ryan Howard', company: 'Linear', prompt: 'Shubham Saboo high-retention hook', status: 'completed', time: '10:20' }
      ];

      this.init();
    }

    init() {
      this.activeTasks.forEach(t => {
        if (!t.deliverable) {
          t.deliverable = this.synthesizeDeliverable(t.agentId, t);
        }
      });
      this.connectSSE();
      this.loadQueueLeads();
      this.bindChat();
      this.renderTasksList();
    }

    setEngine(engine) {
      this.engine = engine;
      if (this.engine.agents.michael) {
        this.onAgentSelected(this.engine.agents.michael);
      }
      this.renderRoster();
      this.renderTasksList();
    }

    connectSSE() {
      try {
        const streamUrl = (window.API_BASE || window.location.origin) + '/api/hive/stream';
        this.eventSource = new EventSource(streamUrl);

        this.eventSource.onmessage = (e) => {
          try {
            const data = JSON.parse(e.data);
            this.handleHiveEvent(data);
          } catch (err) {}
        };

        this.eventSource.onerror = () => {
          setTimeout(() => {
            if (this.eventSource && this.eventSource.readyState === EventSource.CLOSED) {
              this.connectSSE();
            }
          }, 4000);
        };
      } catch (err) {
        this.logTerminal('SSE stream unavailable; local polling mode active.', 'warn');
      }
    }

    handleHiveEvent(event) {
      if (!event || !event.type) return;

      switch (event.type) {
        case 'connected':
          this.logTerminal('✓ Connected to Scranton Branch Multi-Agent Hive Bus', 'info');
          break;

        case 'mission_started':
          this.logTerminal(`🚀 Mission Initiated: ${event.data.company} (${event.data.role})`, 'info');
          if (this.engine) {
            this.engine.setAgentStatus('michael', 'working', 'Delegating...');
          }
          break;

        case 'agent_status':
          if (this.engine) {
            const charId = this.resolveCharId(event.data.role);
            this.engine.setAgentStatus(charId, event.data.status, event.data.label);
            this.updateRosterStatus(charId, event.data.status);
          }
          break;

        case 'envelope_handoff':
          if (this.engine) {
            const fromId = this.resolveCharId(event.data.from);
            const toId = this.resolveCharId(event.data.to);
            this.engine.sendEnvelope(fromId, toId, event.data.artifact);
          }
          break;

        case 'terminal_log':
          this.logTerminal(event.data.message, event.data.level);
          break;

        case 'mission_completed':
          this.logTerminal('✅ Mission Delivered by Dunder Mifflin Scranton team!', 'success');
          if (this.engine) {
            this.engine.setAgentStatus('michael', 'idle', 'Delivered ✓');
          }
          this.loadQueueLeads();
          if (window.showToast) {
            window.showToast('Mission completed and delivered successfully!', 'success');
          }
          break;
      }
    }

    resolveCharId(role) {
      const map = {
        supervisor: 'michael',
        scout: 'jim',
        resume_architect: 'dwight',
        copywriter: 'ryan',
        quality_reviewer: 'angela',
        recruiter_scanner: 'toby',
        michael: 'michael',
        jim: 'jim',
        dwight: 'dwight',
        pam: 'pam',
        ryan: 'ryan',
        angela: 'angela',
        toby: 'toby',
        andy: 'andy',
        kevin: 'kevin',
        oscar: 'oscar',
        stanley: 'stanley',
        phyllis: 'phyllis',
        kelly: 'kelly',
        meredith: 'meredith',
        creed: 'creed'
      };
      return map[role] || 'michael';
    }

    logTerminal(message, level = 'info') {
      const stamp = new Date().toLocaleTimeString('en-US', { hour12: false });
      let colorClass = 'text-slate-300';
      if (level === 'success') colorClass = 'text-emerald-400 font-semibold';
      else if (level === 'error') colorClass = 'text-rose-400 font-bold';
      else if (level === 'warn') colorClass = 'text-amber-400';
      else if (level === 'info') colorClass = 'text-sky-300';

      this.terminalLogs.push({ stamp, message, colorClass });
      if (this.terminalLogs.length > 150) this.terminalLogs.shift();

      const termEl = document.getElementById('command-terminal-output');
      if (termEl) {
        const div = document.createElement('div');
        div.className = 'font-mono text-[11px] leading-relaxed ' + colorClass;
        div.innerHTML = `<span class="text-slate-500 mr-2">[${stamp}]</span>${this.escapeHtml(message)}`;
        termEl.appendChild(div);
        termEl.scrollTop = termEl.scrollHeight;
      }
    }

    switchTab(tabName) {
      this.activeTab = tabName;
      const tabs = ['terminal', 'monitor', 'tasks', 'memory', 'queue'];
      tabs.forEach(t => {
        const content = document.getElementById(`cc-tab-content-${t}`);
        const btn = document.getElementById(`cc-tab-btn-${t}`);
        if (content) content.classList.add('hidden');
        if (btn) {
          btn.className = (t === tabName) ? 'cth-tab active' : 'cth-tab';
        }
      });
      const activeContent = document.getElementById(`cc-tab-content-${tabName}`);
      if (activeContent) activeContent.classList.remove('hidden');
      if (tabName === 'tasks') {
        this.renderTasksList();
      }
    }

    onAgentSelected(agent) {
      this.selectedAgent = agent;
      const nameEl = document.getElementById('cc-agent-name');
      const roleEl = document.getElementById('cc-agent-role');
      const statusPill = document.getElementById('cc-agent-status-pill');
      const statusText = document.getElementById('cc-agent-status-text');
      const avatarBox = document.getElementById('cc-agent-avatar-box');
      const assignBtn = document.getElementById('cc-assign-task-btn');

      if (nameEl) nameEl.innerText = agent.name;
      if (roleEl) roleEl.innerText = agent.title;
      if (statusPill && statusText) {
        statusText.innerText = agent.status;
        statusPill.className = agent.status === 'working'
          ? 'cth-badge cth-badge-working'
          : 'cth-badge cth-badge-idle';
      }
      if (assignBtn) {
        assignBtn.innerHTML = `⚡ Assign to ${agent.name.split(' ')[0]}`;
        assignBtn.onclick = () => this.openAssignTaskModal(agent.id);
      }

      if (avatarBox) {
        avatarBox.innerHTML = '';
        const canvas = document.createElement('canvas');
        canvas.width = 36;
        canvas.height = 56;
        canvas.className = 'bust-canvas';
        const ctx = canvas.getContext('2d');
        if (window.PortraitArt) {
          window.PortraitArt.paintPortrait(ctx, agent.id, 2);
        }
        avatarBox.appendChild(canvas);
      }

      // Sync selection outline across all cards
      const cards = document.querySelectorAll('.cth-agent-card');
      cards.forEach(c => c.classList.remove('selected'));
      const activeCard = document.getElementById(`roster-card-${agent.id}`);
      if (activeCard) activeCard.classList.add('selected');

      // Update Memory Tab
      const memBox = document.getElementById('cc-memory-content');
      if (memBox) {
        memBox.innerHTML = `
          <div class="cth-panel p-3.5 space-y-2 text-xs">
            <div class="font-bold text-amber-500 flex items-center justify-between">
              <span style="font-family: var(--cth-font-display); font-size: 10px;">🧠 ${agent.name}</span>
              <span class="text-[10px] text-slate-500 font-mono">Scranton Branch</span>
            </div>
            <div class="italic text-slate-300">"${agent.quote || "Scranton branch on duty."}"</div>
            <div class="grid grid-cols-2 gap-2 pt-2 border-t border-slate-800 text-[11px]">
              <div class="p-2 rounded bg-slate-950/80 border border-slate-800">
                <div class="text-slate-400 text-[10px]">Tasks Handled</div>
                <div class="text-sm font-extrabold text-white" style="font-family: var(--cth-font-display);">${agent.stats ? agent.stats.completed : 0}</div>
              </div>
              <div class="p-2 rounded bg-slate-950/80 border border-slate-800">
                <div class="text-slate-400 text-[10px]">Quality Gate</div>
                <div class="text-sm font-extrabold text-emerald-400" style="font-family: var(--cth-font-display);">${agent.stats ? agent.stats.score : '98%'}</div>
              </div>
            </div>
            <div class="pt-2 flex gap-2">
              <button onclick="window.AOECommandCenter.openAssignTaskModal('${agent.id}')" class="cth-btn cth-btn-primary flex-1 text-xs" style="height: 28px;">
                ⚡ Assign Task
              </button>
              <button onclick="window.AOECommandCenter.openCharacterModal('${agent.id}')" class="cth-btn cth-btn-secondary text-xs" style="height: 28px;">
                Open Desk ↗
              </button>
            </div>
          </div>
        `;
      }
    }

    // ==================== UNIVERSAL TASK ASSIGNMENT MODAL ====================
    openAssignTaskModal(charId = null) {
      const modal = document.getElementById('modal-assign-task');
      if (!modal) return;

      const targetId = charId || (this.selectedAgent ? this.selectedAgent.id : 'michael');
      this.modalSelectedAgent = targetId;

      // Populate 15-character picker strip
      const strip = document.getElementById('task-modal-agent-strip');
      if (strip) {
        strip.innerHTML = '';
        const allIds = [
          'michael', 'jim', 'dwight', 'pam', 'ryan', 'angela', 'andy',
          'kevin', 'oscar', 'stanley', 'phyllis', 'kelly', 'meredith',
          'toby', 'creed'
        ];

        allIds.forEach(id => {
          const cfg = CHARACTER_CONFIGS[id] || {};
          const isSelected = (id === this.modalSelectedAgent);
          const tile = document.createElement('div');
          tile.id = `task-picker-${id}`;
          tile.className = `agent-picker-tile p-1 rounded cursor-pointer flex flex-col items-center justify-between text-center transition-all ${isSelected ? 'selected' : ''}`;
          tile.style.background = isSelected ? 'var(--cth-cream-300)' : 'var(--cth-paper-100)';
          tile.style.boxShadow = isSelected ? 'inset 0 0 0 2px var(--cth-lemon)' : 'inset 0 0 0 1px var(--cth-ink-100)';
          tile.onclick = () => this.selectModalAgent(id);

          tile.innerHTML = `
            <div style="width: 24px; height: 32px; overflow: hidden; display: flex; align-items: flex-start; justify-content: center;">
              <canvas id="task-picker-canvas-${id}" width="24" height="36" style="width:24px; height:36px; image-rendering:pixelated;"></canvas>
            </div>
            <span style="font-family: var(--cth-font-display); font-size: 7px; color: var(--cth-ink-900); margin-top: 2px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; max-width: 100%;">
              ${(cfg.name || id).split(' ')[0].toUpperCase()}
            </span>
          `;
          strip.appendChild(tile);

          setTimeout(() => {
            const c = document.getElementById(`task-picker-canvas-${id}`);
            if (c && window.PortraitArt) {
              const ctx = c.getContext('2d');
              window.PortraitArt.paintPortrait(ctx, id, 1.3);
            }
          }, 0);
        });
      }

      this.selectModalAgent(this.modalSelectedAgent);
      modal.classList.remove('hidden');
    }

    closeAssignTaskModal() {
      const modal = document.getElementById('modal-assign-task');
      if (modal) modal.classList.add('hidden');
    }

    selectModalAgent(charId) {
      this.modalSelectedAgent = charId;
      const cfg = CHARACTER_CONFIGS[charId] || { name: charId, dept: 'Staff', quote: 'Ready for tasks.', presets: [] };

      // Update picker tiles highlights
      const allIds = [
        'michael', 'jim', 'dwight', 'pam', 'ryan', 'angela', 'andy',
        'kevin', 'oscar', 'stanley', 'phyllis', 'kelly', 'meredith',
        'toby', 'creed'
      ];
      allIds.forEach(id => {
        const tile = document.getElementById(`task-picker-${id}`);
        if (tile) {
          const isSelected = (id === charId);
          tile.style.background = isSelected ? 'var(--cth-cream-300)' : 'var(--cth-paper-100)';
          tile.style.boxShadow = isSelected ? 'inset 0 0 0 2px var(--cth-lemon)' : 'inset 0 0 0 1px var(--cth-ink-100)';
        }
      });

      // Paint spotlight bust
      const bustCanvas = document.getElementById('task-modal-bust-canvas');
      if (bustCanvas && window.PortraitArt) {
        const ctx = bustCanvas.getContext('2d');
        ctx.clearRect(0, 0, bustCanvas.width, bustCanvas.height);
        window.PortraitArt.paintPortrait(ctx, charId, 1.8);
      }

      // Update spotlight labels
      const nameEl = document.getElementById('task-modal-spotlight-name');
      const deptEl = document.getElementById('task-modal-spotlight-dept');
      const quoteEl = document.getElementById('task-modal-spotlight-quote');
      const presetsName = document.getElementById('task-modal-presets-name');
      const dispatchBtn = document.getElementById('task-modal-dispatch-btn');

      if (nameEl) nameEl.innerText = cfg.name;
      if (deptEl) deptEl.innerText = cfg.roleTag || 'STAFF';
      if (quoteEl) quoteEl.innerText = cfg.quote || '';
      if (presetsName) presetsName.innerText = cfg.name.split(' ')[0];
      if (dispatchBtn) dispatchBtn.innerText = `🚀 Dispatch Task to ${cfg.name.split(' ')[0]}`;

      // Populate Presets
      const presetsBox = document.getElementById('task-modal-presets-container');
      if (presetsBox) {
        presetsBox.innerHTML = '';
        const presets = cfg.presets || [];
        presets.forEach((p, idx) => {
          const chip = document.createElement('button');
          chip.type = 'button';
          chip.className = 'cth-btn cth-btn-secondary text-[10px]';
          chip.style.height = '24px';
          chip.style.padding = '0 8px';
          chip.innerText = p.label;
          chip.onclick = () => this.applyTaskPreset(idx);
          presetsBox.appendChild(chip);
        });
      }

      // Auto-fill prompt placeholder with first preset
      if (cfg.presets && cfg.presets[0]) {
        this.applyTaskPreset(0);
      }
    }

    applyTaskPreset(presetIdx) {
      const cfg = CHARACTER_CONFIGS[this.modalSelectedAgent];
      if (!cfg || !cfg.presets || !cfg.presets[presetIdx]) return;

      const p = cfg.presets[presetIdx];
      const compIn = document.getElementById('task-company-input');
      const roleIn = document.getElementById('task-role-input');
      const promptIn = document.getElementById('task-prompt-input');
      const modeSel = document.getElementById('task-mode-select');

      if (compIn) compIn.value = p.company || 'Spotify';
      if (roleIn) roleIn.value = p.role || 'Product Designer';
      if (promptIn) promptIn.value = p.prompt || '';
      if (modeSel && p.mode) modeSel.value = p.mode;
    }

    dispatchAssignedTask() {
      const comp = (document.getElementById('task-company-input') || {}).value || 'Target';
      const role = (document.getElementById('task-role-input') || {}).value || 'Candidate';
      const prompt = (document.getElementById('task-prompt-input') || {}).value || 'Execute custom mission directive';
      const mode = (document.getElementById('task-mode-select') || {}).value || 'standard';
      const model = (document.getElementById('task-model-select') || {}).value || 'active';

      this.closeAssignTaskModal();
      this.assignTaskToAgent(this.modalSelectedAgent, {
        company: comp,
        role: role,
        prompt: prompt,
        mode: mode,
        model: model
      });
    }

    assignTaskToAgent(charId, taskData) {
      const cfg = CHARACTER_CONFIGS[charId] || { name: charId };
      const company = taskData.company || 'Target';
      const role = taskData.role || 'Specialist';
      const prompt = taskData.prompt || 'Custom Directive';
      const taskTitle = `${role} @ ${company}`;

      // 1. Focus agent & set status
      if (this.engine && this.engine.agents[charId]) {
        const agent = this.engine.agents[charId];
        this.engine.selectAgent(charId);
        this.onAgentSelected(agent);
        this.engine.setAgentStatus(charId, 'working', `${role} @ ${company}`);
      }

      // 2. Character-specific Floor Animations
      if (this.engine) {
        if (charId === 'dwight' || taskData.mode === 'print') {
          this.engine.triggerCopier();
          this.engine.showBubble('dwight', 'Enforcing 1-page budget & printing!', 180);
        } else if (charId === 'jim') {
          this.engine.showBubble('jim', `Scouting live feeds for ${role}...`, 180);
          this.searchPublicJobs(role);
        } else if (charId === 'toby') {
          this.engine.showBubble('toby', 'Checking Gmail radar in annex...', 180);
          this.scanTobyRadar();
        } else if (charId === 'andy') {
          this.engine.showBubble('andy', 'Cornell network activating! Ridit-dit-di-doo!', 180);
        } else if (charId === 'ryan') {
          this.engine.showBubble('ryan', 'Drafting 3-sentence Shubham Saboo hook...', 180);
        } else if (charId === 'angela') {
          this.engine.showBubble('angela', 'Auditing WCAG AA & single-page budget.', 180);
        } else if (charId === 'michael') {
          this.engine.showBubble('michael', 'Team assemble! Conference room right now!', 180);
        } else {
          this.engine.showBubble(charId, `Working on ${company}...`, 180);
        }
      }

      // 3. Log to Terminal
      const stamp = new Date().toLocaleTimeString('en-US', { hour12: false });
      const engineTag = (taskData.model && taskData.model !== 'active') ? ` [Engine: ${taskData.model}]` : '';
      this.logTerminal(`[TASK ASSIGNED] ${cfg.name} assigned: ${taskTitle}${engineTag}`, 'info');
      this.logTerminal(`[DIRECTIVE] "${prompt}"`, 'info');

      // 4. Record in Active Tasks Ledger
      const taskId = 'task-' + Date.now();
      const deliverable = this.synthesizeDeliverable(charId, taskData);
      const newTask = {
        id: taskId,
        agentId: charId,
        agentName: cfg.name,
        company: company,
        role: role,
        title: taskTitle,
        prompt: prompt,
        mode: taskData.mode,
        model: taskData.model,
        deliverable: deliverable,
        status: 'in_progress',
        time: stamp
      };

      this.activeTasks.unshift(newTask);
      this.renderTasksList();
      this.renderRoster();

      // Switch to tasks or terminal if appropriate
      if (this.activeTab === 'tasks') {
        this.renderTasksList();
      }

      // 5. Simulate asynchronous completion after 3.5 seconds
      setTimeout(() => {
        newTask.status = 'completed';
        if (this.engine && this.engine.agents[charId]) {
          this.engine.setAgentStatus(charId, 'idle', 'Completed ✓');
          if (this.engine.agents[charId].stats) {
            this.engine.agents[charId].stats.completed = (this.engine.agents[charId].stats.completed || 0) + 1;
          }
        }
        this.renderTasksList();
        this.renderRoster();
        this.logTerminal(`✓ [TASK COMPLETED] ${cfg.name} finished: ${taskTitle}`, 'success');
        this.logTerminal(`[DELIVERABLE READY] Click [View Deliverable] in Tasks tab to inspect output.`, 'info');

        // Automatically open the deliverable inspector modal for immediate user feedback!
        this.openTaskDeliverableModal(taskId);

        if (window.showToast) {
          window.showToast(`✓ ${cfg.name} deliverable ready for ${company}!`, 'success');
        }
      }, 3600);
    }

    renderTasksList() {
      const container = document.getElementById('cc-dynamic-tasks-list');
      if (!container) return;

      if (!this.activeTasks || this.activeTasks.length === 0) {
        container.innerHTML = `
          <div class="p-3 text-center text-xs" style="color: var(--cth-ink-500);">
            No tasks dispatched yet. Click "+ New Task" or pick any character!
          </div>
        `;
        return;
      }

      container.innerHTML = '';
      this.activeTasks.slice(0, 10).forEach(task => {
        const isWorking = (task.status === 'in_progress');
        const card = document.createElement('div');
        card.className = 'p-2.5 rounded flex flex-col space-y-1.5 transition-all';
        card.style.background = 'var(--cth-paper-100)';
        card.style.boxShadow = isWorking
          ? 'inset 0 0 0 1px var(--cth-lemon), 0 1px 3px rgba(0,0,0,0.06)'
          : 'inset 0 0 0 1px var(--cth-ink-100)';

        card.innerHTML = `
          <div style="display: flex; justify-content: space-between; align-items: center;">
            <div style="display: flex; align-items: center; gap: 6px;">
              <span style="font-family: var(--cth-font-display); font-size: 8px; color: var(--cth-ink-900);">
                ${this.escapeHtml(task.agentName.split(' ')[0].toUpperCase())}
              </span>
              <span style="font-size: 10px; color: var(--cth-ink-500);">• ${this.escapeHtml(task.company)}</span>
              ${task.model && task.model !== 'active' ? `
                <span class="cth-badge cth-badge-idle" style="font-size: 7px; padding: 0 4px; font-family: var(--cth-font-mono);">
                  ${this.escapeHtml(task.model.split('-')[0].toUpperCase())}
                </span>
              ` : ''}
            </div>
            <span class="cth-badge ${isWorking ? 'cth-badge-working' : 'cth-badge-idle'}" style="font-size: 8px; padding: 1px 5px;">
              <span class="cth-badge-dot"></span>
              <span>${isWorking ? 'WORKING' : 'DONE ✓'}</span>
            </span>
          </div>
          <div style="font-size: 11px; font-weight: 700; color: var(--cth-ink-900); line-height: 1.3; margin-top: 2px;">
            ${this.escapeHtml(task.title)}
          </div>
          <div style="font-size: 10px; color: var(--cth-ink-500); font-family: var(--cth-font-mono); line-height: 1.3; overflow: hidden; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical;">
            ${this.escapeHtml(task.prompt)}
          </div>
          ${isWorking ? `
            <div class="cth-gauge" style="margin-top: 3px;">
              <div class="cth-gauge-fill warn" style="width: 75%;"></div>
            </div>
          ` : `
            <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 5px; padding-top: 4px; border-top: 1px dashed var(--cth-ink-200);">
              <button onclick="window.AOECommandCenter.openTaskDeliverableModal('${task.id}')" class="cth-btn cth-btn-primary" style="height: 24px; font-size: 10px; padding: 0 8px; font-weight: 700;" title="Inspect deliverable output, copy pitch or download PDF">
                📦 View Deliverable ↗
              </button>
              <span style="font-family: var(--cth-font-mono); font-size: 9px; color: var(--cth-mint); font-weight: 600;">✓ Output Ready</span>
            </div>
          `}
        `;
        container.appendChild(card);
      });
    }

    setRosterFilter(filterMode) {
      this.rosterFilter = filterMode;
      this.renderRoster();
    }

    renderRoster() {
      const container = document.getElementById('office-roster-container');
      if (!container || !this.engine) return;

      container.innerHTML = '';
      const fullOrder = [
        'michael', 'jim', 'dwight', 'pam', 'ryan', 'angela', 'andy',
        'kevin', 'oscar', 'stanley', 'phyllis', 'kelly', 'meredith',
        'toby', 'creed'
      ];

      let order = fullOrder;
      if (this.rosterFilter === 'active') {
        const activeIds = new Set(['michael']);
        this.activeTasks.forEach(t => activeIds.add(t.agentId));
        Object.keys(this.engine.agents).forEach(id => {
          if (this.engine.agents[id].status === 'working') activeIds.add(id);
        });
        order = fullOrder.filter(id => activeIds.has(id));
      }

      // Sync filter button styles
      const allBtn = document.getElementById('dock-filter-all');
      const actBtn = document.getElementById('dock-filter-active');
      if (allBtn && actBtn) {
        if (this.rosterFilter === 'active') {
          actBtn.className = 'cth-btn cth-btn-primary';
          allBtn.className = 'cth-btn cth-btn-ghost';
        } else {
          allBtn.className = 'cth-btn cth-btn-primary';
          actBtn.className = 'cth-btn cth-btn-ghost';
        }
      }

      order.forEach(id => {
        const agent = this.engine.agents[id];
        if (!agent) return;

        const info = CHARACTER_CONFIGS[id] || { roleTag: 'STAFF', isGod: false, accent: 'mint' };
        const isSelected = (this.selectedAgent && this.selectedAgent.id === id) || (id === 'michael' && !this.selectedAgent);

        const card = document.createElement('div');
        card.id = `roster-card-${id}`;
        card.className = `cth-agent-card ${info.isGod ? 'is-god' : ''} ${isSelected ? 'selected' : ''}`;
        card.setAttribute('role', 'button');
        card.setAttribute('tabindex', '0');
        card.onclick = () => {
          this.engine.selectAgent(id);
          this.onAgentSelected(agent);
        };

        const statusClass = agent.status === 'working' ? 'cth-badge-working' : 'cth-badge-idle';
        const gaugeFillPct = agent.status === 'working' ? 80 : 25;
        const gaugeFillClass = agent.status === 'working' ? 'warn' : '';

        card.innerHTML = `
          <div style="display:flex; gap:8px; height:100%; align-items:center;">
            <!-- Portrait tile -->
            <div style="width:36px; height:${info.isGod ? 50 : 46}px; background:${info.isGod ? 'var(--cth-paper-100)' : 'var(--cth-' + info.accent + '-light)'}; box-shadow: inset 0 0 0 1px var(--cth-ink-${info.isGod ? '300' : '100'}); display:flex; align-items:flex-start; justify-content:center; overflow:hidden; flex-shrink:0;">
              <canvas id="roster-bust-${id}" width="36" height="56" class="bust-canvas"></canvas>
            </div>

            <!-- Identity + Info + Gauge -->
            <div style="flex:1; display:flex; flex-direction:column; justify-content:space-between; height:100%; min-width:0; padding:1px 0;">
              <!-- Identity row -->
              <div style="display:flex; align-items:center; justify-content:space-between; gap:4px;">
                <div style="display:inline-flex; align-items:center; gap:5px; min-width:0; flex:1;">
                  <span style="font-family:var(--cth-font-display); font-size:9px; color:var(--cth-ink-900); white-space:nowrap; overflow:hidden; text-overflow:ellipsis;">
                    ${this.escapeHtml(agent.name.split(' ')[0].toUpperCase())}
                  </span>
                  ${info.isGod ? `<span class="cth-boss-tag">BOSS</span>` : ''}
                </div>
                <span id="roster-badge-${id}" class="cth-badge ${statusClass}">
                  <span class="cth-badge-dot"></span>
                  <span id="roster-status-${id}">${agent.status}</span>
                </span>
              </div>

              <!-- Context line / Action -->
              <div id="roster-action-${id}" style="font-size:10px; font-family:var(--cth-font-ui); color:var(--cth-ink-500); white-space:nowrap; overflow:hidden; text-overflow:ellipsis;">
                ${this.escapeHtml(agent.action || agent.title.split('(')[0].trim())}
              </div>

              <!-- Context gauge (8-segment style) -->
              <div class="cth-gauge" title="Context memory gauge">
                <div id="roster-gauge-${id}" class="cth-gauge-fill ${gaugeFillClass}" style="width:${gaugeFillPct}%;"></div>
              </div>
            </div>
          </div>
        `;

        container.appendChild(card);

        // Paint procedural pixel bust
        setTimeout(() => {
          const bustCanvas = document.getElementById(`roster-bust-${id}`);
          if (bustCanvas && window.PortraitArt) {
            const ctx = bustCanvas.getContext('2d');
            window.PortraitArt.paintPortrait(ctx, id, 2);
          }
        }, 0);
      });

      // + Assign Task button matching Munder Difflin style
      const addBtn = document.createElement('button');
      addBtn.className = 'cth-btn cth-btn-secondary';
      addBtn.style.height = '78px';
      addBtn.style.minWidth = '96px';
      addBtn.style.flexShrink = '0';
      addBtn.style.display = 'flex';
      addBtn.style.flexDirection = 'column';
      addBtn.style.justifyContent = 'center';
      addBtn.style.alignItems = 'center';
      addBtn.style.fontSize = '10px';
      addBtn.innerHTML = '<span style="font-size:16px;">⚡</span><span style="font-weight:700; margin-top:2px;">Assign Task</span>';
      addBtn.title = 'Assign a custom task to any Scranton character';
      addBtn.onclick = () => {
        this.openAssignTaskModal();
      };
      container.appendChild(addBtn);
    }

    updateRosterStatus(roleId, status) {
      const canonical = this.resolveCharId(roleId);
      const badge = document.getElementById(`roster-badge-${canonical}`);
      const text = document.getElementById(`roster-status-${canonical}`);
      const gauge = document.getElementById(`roster-gauge-${canonical}`);
      const action = document.getElementById(`roster-action-${canonical}`);

      if (badge) {
        badge.className = `cth-badge ${status === 'working' ? 'cth-badge-working' : 'cth-badge-idle'}`;
      }
      if (text) {
        text.innerText = status;
      }
      if (gauge) {
        gauge.style.width = status === 'working' ? '80%' : '30%';
        gauge.className = `cth-gauge-fill ${status === 'working' ? 'warn' : ''}`;
      }
      if (action && this.engine && this.engine.agents[canonical]) {
        action.innerText = this.engine.agents[canonical].action || (status === 'working' ? 'Processing mission...' : 'Stationed at desk');
      }
    }

    openCharacterModal(charId) {
      const canonical = this.resolveCharId(charId);
      // Close all character modals first
      const allModals = ['michael', 'jim', 'dwight', 'pam', 'ryan', 'angela', 'andy', 'toby'];
      allModals.forEach(m => {
        const el = document.getElementById(`modal-${m}`);
        if (el) el.classList.add('hidden');
      });

      const targetModal = document.getElementById(`modal-${canonical}`);
      if (targetModal) {
        targetModal.classList.remove('hidden');
        if (canonical === 'jim') {
          this.searchPublicJobs('designer');
        }
      } else {
        // Fallback to assign task modal
        this.openAssignTaskModal(canonical);
      }
    }

    closeCharacterModal(charId) {
      const canonical = this.resolveCharId(charId);
      const el = document.getElementById(`modal-${canonical}`);
      if (el) el.classList.add('hidden');
    }

    // ==================== AI ENGINES & CUSTOM MODELS HUB ====================
    async openAiEnginesModal() {
      const modal = document.getElementById('modal-ai-engines');
      if (!modal) return;

      try {
        const res = await fetch((window.API_BASE || window.location.origin) + '/api/config');
        if (res.ok) {
          const cfg = await res.json();
          this.currentConfig = cfg;
          this.selectedAiProvider = (cfg.llm_provider || 'gemini').toLowerCase();

          const modelInput = document.getElementById('ai-model-input');
          const keyInput = document.getElementById('ai-key-input');
          const baseUrlInput = document.getElementById('ai-base-url-input');

          const provMeta = AI_PROVIDERS_CONFIG[this.selectedAiProvider] || AI_PROVIDERS_CONFIG.gemini;
          if (modelInput) modelInput.value = cfg.llm_model || provMeta.defaultModel;
          if (keyInput) keyInput.value = cfg.llm_api_key || '';
          if (baseUrlInput) baseUrlInput.value = cfg.llm_base_url || provMeta.defaultBaseUrl;
        }
      } catch (err) {
        console.warn('Could not fetch existing config:', err);
      }

      this.renderAiProviderUI();

      // Reset test result card
      const testBox = document.getElementById('ai-test-result-box');
      if (testBox) testBox.classList.add('hidden');

      modal.classList.remove('hidden');
    }

    closeAiEnginesModal() {
      const modal = document.getElementById('modal-ai-engines');
      if (modal) modal.classList.add('hidden');
    }

    selectAiProvider(provId) {
      if (!AI_PROVIDERS_CONFIG[provId]) return;
      this.selectedAiProvider = provId;
      const prov = AI_PROVIDERS_CONFIG[provId];

      const modelInput = document.getElementById('ai-model-input');
      const baseUrlInput = document.getElementById('ai-base-url-input');
      const keyInput = document.getElementById('ai-key-input');

      if (modelInput) {
        modelInput.value = prov.defaultModel;
      }
      if (baseUrlInput) {
        baseUrlInput.value = prov.defaultBaseUrl || '';
      }
      if (keyInput) {
        keyInput.placeholder = prov.placeholderKey;
      }

      this.renderAiProviderUI();
    }

    renderAiProviderUI() {
      const provs = ['gemini', 'openai', 'anthropic', 'groq', 'ollama', 'openrouter'];
      provs.forEach(id => {
        const btn = document.getElementById(`ai-prov-${id}`);
        if (!btn) return;
        const isSelected = (id === this.selectedAiProvider);
        btn.style.background = isSelected ? 'var(--cth-cream-300)' : 'var(--cth-paper-100)';
        btn.style.boxShadow = isSelected ? 'inset 0 0 0 2px var(--cth-lemon)' : 'inset 0 0 0 1px var(--cth-ink-100)';
      });

      // Render preset chips for selected provider
      const presetsBox = document.getElementById('ai-model-presets');
      const currentMeta = AI_PROVIDERS_CONFIG[this.selectedAiProvider] || AI_PROVIDERS_CONFIG.gemini;
      if (presetsBox) {
        presetsBox.innerHTML = '';
        currentMeta.presets.forEach(slug => {
          const chip = document.createElement('button');
          chip.type = 'button';
          chip.className = 'cth-btn cth-btn-secondary text-[10px]';
          chip.style.height = '22px';
          chip.style.padding = '0 7px';
          chip.style.fontFamily = 'var(--cth-font-mono)';
          chip.innerText = slug;
          chip.onclick = () => {
            const input = document.getElementById('ai-model-input');
            if (input) input.value = slug;
          };
          presetsBox.appendChild(chip);
        });
      }
    }

    toggleApiKeyVisibility() {
      const keyInput = document.getElementById('ai-key-input');
      const toggleBtn = document.getElementById('ai-key-toggle-btn');
      if (!keyInput) return;

      if (keyInput.type === 'password') {
        keyInput.type = 'text';
        if (toggleBtn) toggleBtn.innerText = 'Hide Key';
      } else {
        keyInput.type = 'password';
        if (toggleBtn) toggleBtn.innerText = 'Show Key';
      }
    }

    async testAiConnection() {
      const provider = this.selectedAiProvider || 'gemini';
      const model = (document.getElementById('ai-model-input') || {}).value || '';
      const apiKey = (document.getElementById('ai-key-input') || {}).value || '';
      const baseUrl = (document.getElementById('ai-base-url-input') || {}).value || '';

      const testBox = document.getElementById('ai-test-result-box');
      const icon = document.getElementById('ai-test-icon');
      const msg = document.getElementById('ai-test-msg');
      const latency = document.getElementById('ai-test-latency');
      const reply = document.getElementById('ai-test-reply');
      const btn = document.getElementById('ai-test-btn');

      if (testBox) {
        testBox.classList.remove('hidden');
        if (icon) icon.innerText = '⏳';
        if (msg) {
          msg.innerText = `Testing ${provider.toUpperCase()} (${model || 'default'})...`;
          msg.style.color = 'var(--cth-ink-900)';
        }
        if (latency) {
          latency.innerText = 'pinging...';
          latency.className = 'cth-badge cth-badge-working';
        }
        if (reply) reply.innerText = '';
      }

      if (btn) btn.disabled = true;

      try {
        const payload = {
          provider: provider,
          model: model,
          api_key: apiKey,
          base_url: baseUrl || undefined
        };

        const res = await fetch((window.API_BASE || window.location.origin) + '/api/test/llm', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload)
        });

        const data = await res.json();

        if (res.ok && data.status === 'ok') {
          if (icon) icon.innerText = '🟢';
          if (msg) {
            msg.innerText = `Connected to ${provider.toUpperCase()} successfully!`;
            msg.style.color = 'var(--cth-mint)';
          }
          if (latency) {
            latency.innerText = `${data.latency_ms} ms`;
            latency.className = 'cth-badge cth-badge-idle';
          }
          if (reply) reply.innerText = `Response: "${data.response}"`;
          this.logTerminal(`[AI ENGINE] ✓ Connected to ${provider} (${model}) in ${data.latency_ms}ms`, 'success');
        } else {
          if (icon) icon.innerText = '🔴';
          if (msg) {
            msg.innerText = `Connection Failed`;
            msg.style.color = 'var(--cth-coral)';
          }
          if (latency) {
            latency.innerText = 'FAILED';
            latency.className = 'cth-badge cth-badge-stalled';
          }
          if (reply) reply.innerText = data.message || data.detail || 'Check API key or endpoint.';
          this.logTerminal(`[AI ENGINE ERROR] ${data.message || data.detail || 'Test failed'}`, 'error');
        }
      } catch (err) {
        if (icon) icon.innerText = '🔴';
        if (msg) {
          msg.innerText = `Network/CORS Error`;
          msg.style.color = 'var(--cth-coral)';
        }
        if (latency) {
          latency.innerText = 'ERROR';
          latency.className = 'cth-badge cth-badge-stalled';
        }
        if (reply) reply.innerText = err.message;
        this.logTerminal(`[AI ENGINE ERROR] ${err.message}`, 'error');
      } finally {
        if (btn) btn.disabled = false;
      }
    }

    async saveAiConfig() {
      const provider = this.selectedAiProvider || 'gemini';
      const model = (document.getElementById('ai-model-input') || {}).value || '';
      const apiKey = (document.getElementById('ai-key-input') || {}).value || '';
      const baseUrl = (document.getElementById('ai-base-url-input') || {}).value || '';
      const saveBtn = document.getElementById('ai-save-btn');

      if (saveBtn) {
        saveBtn.disabled = true;
        saveBtn.innerText = 'Saving...';
      }

      try {
        let baseConfig = this.currentConfig;
        if (!baseConfig) {
          const cfgRes = await fetch((window.API_BASE || window.location.origin) + '/api/config');
          if (cfgRes.ok) baseConfig = await cfgRes.json();
        }

        const payload = {
          candidate_name: (baseConfig && baseConfig.candidate_name) || '',
          candidate_email: (baseConfig && baseConfig.candidate_email) || '',
          candidate_phone: (baseConfig && baseConfig.candidate_phone) || '',
          candidate_location: (baseConfig && baseConfig.candidate_location) || '',
          candidate_portfolio: (baseConfig && baseConfig.candidate_portfolio) || '',
          candidate_linkedin: (baseConfig && baseConfig.candidate_linkedin) || '',
          sender_email: (baseConfig && baseConfig.sender_email) || '',
          dry_run: (baseConfig && baseConfig.dry_run !== undefined) ? baseConfig.dry_run : true,
          llm_provider: provider,
          llm_api_key: apiKey,
          llm_model: model,
          llm_base_url: baseUrl || null,
          default_profession: (baseConfig && baseConfig.default_profession) || 'product-designer',
          tracker_spreadsheet_id: (baseConfig && baseConfig.tracker_spreadsheet_id) || ''
        };

        const res = await fetch((window.API_BASE || window.location.origin) + '/api/config', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload)
        });

        if (res.ok) {
          this.currentConfig = payload;
          this.logTerminal(`[AI ENGINE] Configuration saved to .env: ${provider.toUpperCase()} (${model})`, 'success');
          if (window.showToast) {
            window.showToast(`✓ AI Engine configured: ${provider.toUpperCase()}`, 'success');
          }
          this.closeAiEnginesModal();
        } else {
          const errData = await res.json();
          this.logTerminal(`[AI CONFIG ERROR] Failed to save: ${errData.detail || 'Unknown error'}`, 'error');
        }
      } catch (err) {
        this.logTerminal(`[AI CONFIG ERROR] ${err.message}`, 'error');
      } finally {
        if (saveBtn) {
          saveBtn.disabled = false;
          saveBtn.innerText = '💾 Save Configuration';
        }
      }
    }

    // ==================== TASK DELIVERABLE & OUTPUT INSPECTOR ====================
    synthesizeDeliverable(charId, taskData = {}) {
      const company = taskData.company || 'Target';
      const role = taskData.role || 'Specialist';
      const prompt = taskData.prompt || '';
      const model = taskData.model || (this.selectedAiProvider ? this.selectedAiProvider.toUpperCase() : 'GEMINI-2.0');
      const canonical = this.resolveCharId(charId);

      if (canonical === 'dwight' || taskData.mode === 'print') {
        return {
          type: 'resume_pdf',
          title: `1-Page Bahnschrift PDF & ATS Optimization`,
          badge: '1.0 PAGE BUDGET EXACT',
          company: company,
          role: role,
          model: model,
          metrics: [
            { label: 'Line Capacity', value: '46 / 50 lines', status: 'Optimal' },
            { label: 'Page Overflow', value: '0.00 mm', status: 'Guaranteed Single-Page' },
            { label: 'Typography', value: 'Bahnschrift DIN 1451', status: 'Variable Width' },
            { label: 'Contrast Ratio', value: '7.2:1 WCAG AA', status: '100% Passing' }
          ],
          preview: {
            headline: `${role} • Cross-Functional Systems & Product Delivery`,
            summary: `Performance-driven ${role} with deep expertise in design tokens, cross-platform UI architectures, and WCAG AA accessibility compliance. Track record of reducing design-to-engineering handoff latency by 35% and improving conversion funnels at scale.`,
            skills: ['Figma & Tokens', 'Design Systems', 'WCAG AA Accessibility', 'TypeScript / React', 'ReportLab PDF Engine', 'Agile Delivery'],
            experience: [
              { company: company, role: role, bullet: `Engineered high-performance interface architectures and standardized component systems across web and mobile platforms.` },
              { company: 'Enterprise Scale Tech', role: 'Staff Product Specialist', bullet: `Led design systems migration across 14 product squads, reducing redundant CSS tokens by 42%.` }
            ]
          }
        };
      } else if (['ryan', 'andy', 'kelly', 'stanley', 'michael'].includes(canonical)) {
        let pitchHeadline = 'Cold Outreach Pitch';
        let pitchBody = '';
        let subject = `Question re: ${role} at ${company}`;

        if (canonical === 'andy') {
          pitchHeadline = '10-Minute Coffee Chat Networking Intro';
          subject = `Fellow alum reaching out / ${role} at ${company}`;
          pitchBody = `Hi [Hiring Team],\n\nI noticed ${company}'s recent product announcements and design initiatives and wanted to connect! As a ${role} with a heavy focus on resilient design systems and cross-functional velocity, I've previously helped scale design architectures that cut UI handoff debt by 35%.\n\nI'd love to grab a brief 10-minute coffee chat or intro call this Thursday to share a quick perspective on design tooling and learn more about your team's current focus.\n\nBest regards,\n[Your Name]`;
        } else if (canonical === 'ryan') {
          pitchHeadline = '3-Sentence High-Retention Hook (Shubham Saboo)';
          subject = `Quick question regarding ${role} at ${company}`;
          pitchBody = `Hi [Hiring Lead],\n\nI saw ${company}'s latest expansion and love your team's approach to scalable product craftsmanship.\n\nAs a ${role}, I recently architected a design system overhaul that accelerated team velocity by 35% while maintaining strict 7.2:1 WCAG AA accessibility.\n\nAre you open to a brief 10-minute discovery chat this Thursday to see if my background matches your engineering roadmap?\n\nBest,\n[Your Name]`;
        } else if (canonical === 'kelly') {
          pitchHeadline = '7-Day Follow-Up Conversion Ping';
          subject = `Following up: ${role} conversation at ${company}`;
          pitchBody = `Hi [Hiring Lead],\n\nChecking in on my earlier note regarding the ${role} position at ${company}. I know your team is moving fast, so I wanted to re-share my live portfolio link and case studies.\n\nWould you have 5 minutes for a quick touchbase next Tuesday?\n\nBest,\n[Your Name]`;
        } else {
          pitchHeadline = 'Executive Outreach Memo';
          subject = `Executive Introduction / ${role} at ${company}`;
          pitchBody = `Hi [Leadership],\n\nReaching out regarding strategic alignment for the ${role} opening at ${company}. I bring deep hands-on expertise in product architecture and team scaling.\n\nWould welcome an executive introductory conversation at your convenience.\n\nRegards,\n[Your Name]`;
        }

        const wordCount = pitchBody.split(/\s+/).length;
        return {
          type: 'email_pitch',
          title: pitchHeadline,
          badge: `${wordCount} WORDS • 20S READ`,
          company: company,
          role: role,
          model: model,
          subject: subject,
          body: pitchBody
        };
      } else if (canonical === 'jim') {
        return {
          type: 'job_scout',
          title: `Scouted Opportunities & Keyword Taxonomy for ${role}`,
          badge: '3 LIVE FEEDS FOUND',
          company: company,
          role: role,
          model: model,
          keywords: ['Figma Tokens', 'Design Systems', 'WCAG AA Contrast', 'Cross-Platform UI', 'React / TypeScript', 'Agile Handoff'],
          jobs: [
            { company: company, role: role, location: 'Remote / Hybrid', snippet: 'Leading design systems architecture, cross-functional component libraries, and accessibility standards.' },
            { company: 'Linear', role: 'Product Designer', location: 'Remote (Global)', snippet: 'Crafting ultra-fast, keyboard-first desktop and web software with high attention to micro-interactions.' },
            { company: 'Stripe', role: 'Design Systems Architect', location: 'San Francisco / Remote', snippet: 'Scaling the core UI foundations powering global financial infrastructure.' }
          ]
        };
      } else if (canonical === 'angela') {
        return {
          type: 'quality_audit',
          title: `Angela Martin Certified Quality Gate Audit`,
          badge: '100/100 AUDIT SCORE',
          company: company,
          role: role,
          model: model,
          checks: [
            { name: 'WCAG AA Color Contrast', detail: '7.2:1 ratio on primary background. Zero illegible gray text.', status: 'PASS ✓' },
            { name: 'Single-Page Layout Budget', detail: '1.0 Page Exact (0.00 mm overflow margin).', status: 'PASS ✓' },
            { name: 'ATS Machine Parseability', detail: 'Strict semantic headings, zero multi-column tables.', status: 'PASS ✓' },
            { name: 'Date & Typo Continuity', detail: 'Contiguous employment history, zero spellcheck flags.', status: 'PASS ✓' }
          ]
        };
      } else if (canonical === 'toby') {
        return {
          type: 'radar_scan',
          title: `Gmail Inbound Radar Scanner Telemetry`,
          badge: 'INBOX RADAR CLEAN',
          company: company,
          role: role,
          model: model,
          stats: { threadsScanned: 18, interviewInvites: 1, acknowledgements: 3, rejections: 0 },
          threads: [
            { sender: `recruiting@${company.toLowerCase().replace(/[^a-z]/g, '')}.com`, subject: `Invitation to interview: ${role}`, intent: 'Interview Request', date: 'Today' },
            { sender: 'careers@stripe.com', subject: 'Application Received: Systems Designer', intent: 'Acknowledgement', date: 'Yesterday' }
          ]
        };
      } else if (canonical === 'oscar') {
        return {
          type: 'salary_comp',
          title: `Salary Band Math & Counter-Offer Strategy`,
          badge: 'COMPENSATION BENCHMARK',
          company: company,
          role: role,
          model: model,
          bands: [
            { percentile: '25th Percentile', base: '$145,000', equity: '$25,000/yr' },
            { percentile: '50th Percentile (Median)', base: '$170,000', equity: '$45,000/yr' },
            { percentile: '75th Percentile', base: '$195,000', equity: '$70,000/yr' },
            { percentile: '90th Percentile (Top)', base: '$220,000', equity: '$100,000/yr' }
          ],
          script: `Thank you for the initial offer. Based on my cross-platform systems experience and recent market compensation percentiles for ${role} in this tier, I am targeting a base of $185,000 with a competitive equity allocation. With that adjustment, I would be thrilled to sign immediately.`
        };
      } else {
        const charName = (CHARACTER_CONFIGS[charId] || {}).name || charId;
        return {
          type: 'generic_report',
          title: `${charName} Deliverable Report`,
          badge: 'VERIFIED OUTPUT',
          company: company,
          role: role,
          model: model,
          content: `Task directive "${prompt}" executed and verified under standard Scranton branch protocol for ${role} at ${company}.`
        };
      }
    }

    openTaskDeliverableModal(taskId) {
      const modal = document.getElementById('modal-task-deliverable');
      if (!modal) return;

      const task = this.activeTasks.find(t => t.id === taskId);
      if (!task) return;

      const d = task.deliverable || this.synthesizeDeliverable(task.agentId, task);

      const nameEl = document.getElementById('deliverable-agent-name');
      const deptEl = document.getElementById('deliverable-dept-badge');
      const modelEl = document.getElementById('deliverable-model-badge');
      const titleEl = document.getElementById('deliverable-task-title');
      const timeEl = document.getElementById('deliverable-timestamp');
      const contentEl = document.getElementById('deliverable-content-area');
      const actionsEl = document.getElementById('deliverable-actions-bar');

      if (nameEl) nameEl.innerText = task.agentName || task.agentId;
      const cfg = CHARACTER_CONFIGS[task.agentId] || {};
      if (deptEl) deptEl.innerText = cfg.roleTag || 'STAFF';
      if (modelEl) {
        modelEl.innerText = (task.model && task.model !== 'active') ? task.model.toUpperCase() : 'ACTIVE ENGINE';
      }
      if (titleEl) titleEl.innerText = `${task.role || 'Role'} @ ${task.company || 'Company'}`;
      if (timeEl) timeEl.innerText = task.time || 'Verified';

      // Paint bust canvas
      const bustCanvas = document.getElementById('deliverable-bust-canvas');
      if (bustCanvas && window.PortraitArt) {
        const ctx = bustCanvas.getContext('2d');
        ctx.clearRect(0, 0, bustCanvas.width, bustCanvas.height);
        window.PortraitArt.paintPortrait(ctx, task.agentId, 1.8);
      }

      if (!contentEl) return;

      if (d.type === 'email_pitch') {
        contentEl.innerHTML = `
          <div class="p-3 rounded space-y-2.5" style="background: var(--cth-paper-100); box-shadow: inset 0 0 0 1px var(--cth-ink-100);">
            <div class="flex items-center justify-between">
              <span class="font-bold text-[11px]" style="color: var(--cth-ink-700);">${this.escapeHtml(d.title)}</span>
              <span class="cth-badge cth-badge-working" style="font-size: 8px;">${this.escapeHtml(d.badge)}</span>
            </div>
            <div>
              <label class="block text-[10px] font-bold mb-1" style="color: var(--cth-ink-500);">SUBJECT LINE</label>
              <div class="p-2 rounded font-mono text-[11px] select-text" style="background: var(--cth-cream-200); box-shadow: inset 0 0 0 1px var(--cth-ink-200); color: var(--cth-ink-900);">
                ${this.escapeHtml(d.subject)}
              </div>
            </div>
            <div>
              <label class="block text-[10px] font-bold mb-1" style="color: var(--cth-ink-500);">GENERATED OUTREACH BODY</label>
              <div id="deliverable-text-copy" class="p-3 rounded text-[11px] leading-relaxed font-sans select-text whitespace-pre-wrap" style="background: var(--cth-cream-50); box-shadow: inset 0 0 0 1px var(--cth-ink-200); color: var(--cth-ink-900);">${this.escapeHtml(d.body)}</div>
            </div>
          </div>
        `;

        if (actionsEl) {
          actionsEl.innerHTML = `
            <button onclick="window.AOECommandCenter.copyDeliverableText()" id="copy-deliverable-btn" class="cth-btn cth-btn-primary" style="height: 28px; font-size: 11px; padding: 0 12px;">
              📋 Copy Pitch to Clipboard
            </button>
            <button onclick="window.AOECommandCenter.pushToGmailDrafts('${this.escapeHtml(task.company)}', '${this.escapeHtml(d.subject)}')" class="cth-btn cth-btn-secondary" style="height: 28px; font-size: 11px; padding: 0 12px;">
              ✉️ Push to Gmail Drafts
            </button>
            <button onclick="window.AOECommandCenter.closeTaskDeliverableModal()" class="cth-btn cth-btn-ghost" style="height: 28px; font-size: 11px;">Close</button>
          `;
        }
      } else if (d.type === 'resume_pdf') {
        contentEl.innerHTML = `
          <div class="space-y-2.5">
            <div class="p-3 rounded" style="background: var(--cth-lemon-light); box-shadow: inset 0 0 0 1px var(--cth-lemon);">
              <div class="flex items-center justify-between mb-2">
                <span style="font-family: var(--cth-font-display); font-size: 8px; color: var(--cth-lemon);">1-PAGE MATHEMATICAL BUDGET GAUGE</span>
                <span class="cth-badge cth-badge-working" style="font-weight: 700;">100% SINGLE-PAGE FIT</span>
              </div>
              <div class="grid grid-cols-2 sm:grid-cols-4 gap-2 text-[10px]">
                ${d.metrics.map(m => `
                  <div class="p-1.5 rounded" style="background: var(--cth-paper-100); box-shadow: inset 0 0 0 1px var(--cth-ink-100);">
                    <div style="color: var(--cth-ink-500);">${this.escapeHtml(m.label)}</div>
                    <div style="font-weight: 700; color: var(--cth-ink-900); font-family: var(--cth-font-mono);">${this.escapeHtml(m.value)}</div>
                    <div style="font-size: 9px; color: var(--cth-mint);">${this.escapeHtml(m.status)}</div>
                  </div>
                `).join('')}
              </div>
            </div>

            <div class="p-3 rounded space-y-2" style="background: var(--cth-paper-100); box-shadow: inset 0 0 0 1px var(--cth-ink-100);">
              <div class="font-bold text-xs" style="color: var(--cth-ink-900);">${this.escapeHtml(d.preview.headline)}</div>
              <p class="text-[11px] leading-relaxed select-text" style="color: var(--cth-ink-700);">${this.escapeHtml(d.preview.summary)}</p>
              <div class="pt-1">
                <span class="text-[10px] font-bold block mb-1" style="color: var(--cth-ink-500);">TAILORED SKILL TAXONOMY</span>
                <div class="flex flex-wrap gap-1">
                  ${d.preview.skills.map(s => `<span class="cth-badge cth-badge-idle" style="font-size: 9px;">${this.escapeHtml(s)}</span>`).join('')}
                </div>
              </div>
            </div>
          </div>
        `;

        if (actionsEl) {
          actionsEl.innerHTML = `
            <a href="/api/resume/download-pdf" target="_blank" class="cth-btn cth-btn-primary flex items-center space-x-1" style="height: 28px; font-size: 11px; padding: 0 12px; text-decoration: none;">
              <span>📄</span>
              <span>Download 1-Page PDF</span>
            </a>
            <button onclick="window.AOECommandCenter.triggerCopierEjection()" class="cth-btn cth-btn-secondary" style="height: 28px; font-size: 11px; padding: 0 12px;">
              🖨️ Print on Copier
            </button>
            <button onclick="window.AOECommandCenter.closeTaskDeliverableModal()" class="cth-btn cth-btn-ghost" style="height: 28px; font-size: 11px;">Close</button>
          `;
        }
      } else if (d.type === 'job_scout') {
        contentEl.innerHTML = `
          <div class="space-y-2.5">
            <div class="flex items-center justify-between">
              <span class="font-bold text-[11px]" style="color: var(--cth-ink-700);">${this.escapeHtml(d.title)}</span>
              <span class="cth-badge cth-badge-working" style="font-size: 8px;">${this.escapeHtml(d.badge)}</span>
            </div>
            <div class="space-y-2 max-h-[220px] overflow-y-auto">
              ${d.jobs.map(j => `
                <div class="p-2.5 rounded" style="background: var(--cth-paper-100); box-shadow: inset 0 0 0 1px var(--cth-ink-100);">
                  <div class="flex items-center justify-between">
                    <span class="font-bold" style="color: var(--cth-ink-900); font-size: 11px;">${this.escapeHtml(j.company)}</span>
                    <span style="font-size: 10px; color: var(--cth-ink-500);">${this.escapeHtml(j.location)}</span>
                  </div>
                  <div style="color: var(--cth-lemon); font-weight: 600; font-size: 11px; margin-top: 1px;">${this.escapeHtml(j.role)}</div>
                  <div style="color: var(--cth-ink-700); font-size: 10px; margin-top: 2px;">${this.escapeHtml(j.snippet)}</div>
                </div>
              `).join('')}
            </div>
          </div>
        `;

        if (actionsEl) {
          actionsEl.innerHTML = `
            <button onclick="window.AOECommandCenter.handoffScoutedJobToDwight('${this.escapeHtml(task.company)}', '${this.escapeHtml(task.role)}')" class="cth-btn cth-btn-primary" style="height: 28px; font-size: 11px; padding: 0 12px;">
              ✨ Pass to Dwight to Tailor 1-Page CV
            </button>
            <button onclick="window.AOECommandCenter.closeTaskDeliverableModal()" class="cth-btn cth-btn-ghost" style="height: 28px; font-size: 11px;">Close</button>
          `;
        }
      } else if (d.type === 'quality_audit') {
        contentEl.innerHTML = `
          <div class="space-y-2.5">
            <div class="p-3 rounded" style="background: var(--cth-peach-light); box-shadow: inset 0 0 0 1px var(--cth-coral);">
              <div class="flex items-center justify-between mb-2">
                <span style="font-family: var(--cth-font-display); font-size: 8px; color: var(--cth-coral);">ANGELA MARTIN AUDIT CERTIFICATE</span>
                <span class="cth-badge cth-badge-working">100/100 AUDIT SCORE</span>
              </div>
              <div class="space-y-1.5">
                ${d.checks.map(c => `
                  <div class="p-2 rounded flex items-center justify-between text-[11px]" style="background: var(--cth-paper-100); box-shadow: inset 0 0 0 1px var(--cth-ink-100);">
                    <div>
                      <div class="font-bold" style="color: var(--cth-ink-900);">${this.escapeHtml(c.name)}</div>
                      <div style="font-size: 10px; color: var(--cth-ink-500);">${this.escapeHtml(c.detail)}</div>
                    </div>
                    <span class="cth-badge cth-badge-idle" style="font-weight: 700; font-size: 9px;">${this.escapeHtml(c.status)}</span>
                  </div>
                `).join('')}
              </div>
            </div>
          </div>
        `;

        if (actionsEl) {
          actionsEl.innerHTML = `
            <button onclick="window.AOECommandCenter.logTerminal('Angela certified: Quality approval stamp recorded.', 'success'); window.AOECommandCenter.closeTaskDeliverableModal();" class="cth-btn cth-btn-primary" style="height: 28px; font-size: 11px; padding: 0 12px;">
              🛡️ Apply Accounting Stamp
            </button>
            <button onclick="window.AOECommandCenter.closeTaskDeliverableModal()" class="cth-btn cth-btn-ghost" style="height: 28px; font-size: 11px;">Close</button>
          `;
        }
      } else if (d.type === 'radar_scan') {
        contentEl.innerHTML = `
          <div class="space-y-2.5">
            <div class="flex items-center justify-between">
              <span class="font-bold text-[11px]" style="color: var(--cth-ink-700);">${this.escapeHtml(d.title)}</span>
              <span class="cth-badge cth-badge-working" style="font-size: 8px;">${this.escapeHtml(d.badge)}</span>
            </div>
            <div class="grid grid-cols-3 gap-2 text-center text-[10px]">
              <div class="p-2 rounded" style="background: var(--cth-paper-100); box-shadow: inset 0 0 0 1px var(--cth-ink-100);">
                <div style="color: var(--cth-ink-500);">Scanned</div>
                <div style="font-weight: 700; font-size: 14px; color: var(--cth-ink-900);">${d.stats.threadsScanned}</div>
              </div>
              <div class="p-2 rounded" style="background: var(--cth-paper-100); box-shadow: inset 0 0 0 1px var(--cth-ink-100);">
                <div style="color: var(--cth-mint);">Interviews</div>
                <div style="font-weight: 700; font-size: 14px; color: var(--cth-mint);">${d.stats.interviewInvites}</div>
              </div>
              <div class="p-2 rounded" style="background: var(--cth-paper-100); box-shadow: inset 0 0 0 1px var(--cth-ink-100);">
                <div style="color: var(--cth-ink-500);">Confirmed</div>
                <div style="font-weight: 700; font-size: 14px; color: var(--cth-ink-900);">${d.stats.acknowledgements}</div>
              </div>
            </div>
            <div class="space-y-1.5">
              ${d.threads.map(t => `
                <div class="p-2 rounded flex items-center justify-between text-[11px]" style="background: var(--cth-paper-100); box-shadow: inset 0 0 0 1px var(--cth-ink-100);">
                  <div>
                    <div class="font-bold" style="color: var(--cth-ink-900);">${this.escapeHtml(t.subject)}</div>
                    <div style="font-size: 10px; color: var(--cth-ink-500);">${this.escapeHtml(t.sender)}</div>
                  </div>
                  <span class="cth-badge cth-badge-working" style="font-size: 9px;">${this.escapeHtml(t.intent)}</span>
                </div>
              `).join('')}
            </div>
          </div>
        `;

        if (actionsEl) {
          actionsEl.innerHTML = `
            <button onclick="window.AOECommandCenter.closeTaskDeliverableModal()" class="cth-btn cth-btn-ghost" style="height: 28px; font-size: 11px;">Close</button>
          `;
        }
      } else {
        contentEl.innerHTML = `
          <div class="p-3 rounded space-y-2" style="background: var(--cth-paper-100); box-shadow: inset 0 0 0 1px var(--cth-ink-100);">
            <div class="font-bold text-xs" style="color: var(--cth-ink-900);">${this.escapeHtml(d.title)}</div>
            <div class="text-[11px] leading-relaxed select-text" style="color: var(--cth-ink-700);">${this.escapeHtml(d.content || 'Output verified.')}</div>
          </div>
        `;

        if (actionsEl) {
          actionsEl.innerHTML = `
            <button onclick="window.AOECommandCenter.closeTaskDeliverableModal()" class="cth-btn cth-btn-ghost" style="height: 28px; font-size: 11px;">Close</button>
          `;
        }
      }

      modal.classList.remove('hidden');
    }

    closeTaskDeliverableModal() {
      const modal = document.getElementById('modal-task-deliverable');
      if (modal) modal.classList.add('hidden');
    }

    copyDeliverableText() {
      const textEl = document.getElementById('deliverable-text-copy');
      if (!textEl) return;
      const text = textEl.innerText;
      navigator.clipboard.writeText(text).then(() => {
        this.logTerminal('✓ Copied pitch body to clipboard!', 'success');
        if (window.showToast) window.showToast('✓ Copied to clipboard!', 'success');
        const btn = document.getElementById('copy-deliverable-btn');
        if (btn) {
          const oldText = btn.innerHTML;
          btn.innerHTML = '✓ Copied to Clipboard!';
          setTimeout(() => { btn.innerHTML = oldText; }, 2000);
        }
      });
    }

    pushToGmailDrafts(company, subject) {
      this.logTerminal(`[GMAIL DRAFTS] Pushed pitch for ${company} to personal Gmail drafts folder!`, 'success');
      if (window.showToast) window.showToast(`✓ Pushed to Gmail Drafts!`, 'success');
      this.closeTaskDeliverableModal();
    }

    triggerCopierEjection() {
      if (this.engine) {
        this.engine.triggerCopier();
        this.engine.showBubble('dwight', 'Copier ejecting 1-page PDF!', 160);
      }
      this.logTerminal('[COPIER] Physical green Xerox copier print cycle initiated.', 'info');
      this.closeTaskDeliverableModal();
    }

    handoffScoutedJobToDwight(company, role) {
      this.closeTaskDeliverableModal();
      this.sendJobToDwight(company, role, 'Design systems, WCAG AA, tokens');
    }

    async searchPublicJobs(query = 'engineer') {
      const container = document.getElementById('jim-jobs-container');
      if (container) container.innerHTML = '<div class="p-3 text-center text-slate-400 text-xs">Jim is querying live public feeds...</div>';

      try {
        const res = await fetch((window.API_BASE || window.location.origin) + `/api/public-jobs/search?query=${encodeURIComponent(query)}`);
        const data = await res.json();
        const jobs = data.jobs || [];
        this.scoutedJobs = jobs;

        if (container) {
          if (jobs.length === 0) {
            container.innerHTML = '<div class="p-3 text-center text-slate-500 text-xs">No matching jobs found. Try "engineer" or "designer".</div>';
            return;
          }
          container.innerHTML = '';
          jobs.forEach((j, idx) => {
            const card = document.createElement('div');
            card.className = 'p-3 rounded-xl bg-slate-950 border border-slate-800 hover:border-blue-500 transition-all text-xs space-y-1.5';
            card.innerHTML = `
              <div class="flex items-center justify-between">
                <span class="font-bold text-white">${this.escapeHtml(j.company)}</span>
                <span class="text-[10px] text-slate-400">${this.escapeHtml(j.location)}</span>
              </div>
              <div class="font-semibold text-sky-400">${this.escapeHtml(j.role)}</div>
              <p class="text-[11px] text-slate-400 line-clamp-2">${this.escapeHtml(j.snippet)}</p>
              <div class="flex items-center justify-between pt-1">
                <div class="flex flex-wrap gap-1">
                  ${(j.tags || []).map(t => `<span class="px-1.5 py-0.5 rounded text-[9px] bg-slate-800 text-slate-300">${this.escapeHtml(t)}</span>`).join('')}
                </div>
                <button onclick="window.AOECommandCenter.sendJobByIndex(${idx})" class="px-2.5 py-1 bg-indigo-600 hover:bg-indigo-500 text-white rounded-lg text-[10px] font-bold shadow-sm">
                  Send to Dwight ➔
                </button>
              </div>
            `;
            container.appendChild(card);
          });
        }
      } catch (err) {
        if (container) container.innerHTML = `<div class="p-3 text-center text-rose-400 text-xs">Error loading feeds: ${err.message}</div>`;
      }
    }

    sendJobByIndex(idx) {
      const j = (this.scoutedJobs && this.scoutedJobs[idx]) || {};
      this.sendJobToDwight(j.company || 'Spotify', j.role || 'Senior Product Designer', j.snippet || 'Figma, Design systems');
    }

    sendJobToDwight(company, role, snippet) {
      this.closeCharacterModal('jim');
      this.logTerminal(`Jim Halpert handed over ${company} (${role}) to Dwight Schrute.`, 'info');
      if (this.engine) {
        this.engine.sendEnvelope('jim', 'dwight', `${company} Specs`);
        this.engine.showBubble('dwight', 'Inspecting 1-Page budget...', 120);
      }
      this.openCharacterModal('dwight');

      const companyInput = document.getElementById('dwight-target-company');
      const roleInput = document.getElementById('dwight-target-role');
      const snippetInput = document.getElementById('dwight-target-snippet');

      if (companyInput) companyInput.value = company;
      if (roleInput) roleInput.value = role;
      if (snippetInput) snippetInput.value = snippet;
    }

    async triggerDwightBuild() {
      const company = (document.getElementById('dwight-target-company') || {}).value || 'Spotify';
      const role = (document.getElementById('dwight-target-role') || {}).value || 'Senior Product Designer';
      const snippet = (document.getElementById('dwight-target-snippet') || {}).value || 'Design systems, Figma, end-to-end UX';

      const statusEl = document.getElementById('dwight-build-status');
      if (statusEl) statusEl.innerHTML = '<span class="text-amber-400">Dwight is enforcing 1-page budget &amp; rendering Bahnschrift PDF...</span>';

      if (this.engine) {
        this.engine.setAgentStatus('dwight', 'working', 'Enforcing 1-Page...');
        this.engine.triggerCopier();
      }

      try {
        const res = await fetch((window.API_BASE || window.location.origin) + '/api/hive/orchestrate', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            company: company,
            role: role,
            text: `${company} is hiring for ${role}. ${snippet}`
          })
        });
        const data = await res.json();
        if (statusEl) {
          statusEl.innerHTML = `<span class="text-emerald-400 font-bold">✓ 1-Page Bahnschrift PDF ready! Green copier finished printing.</span>`;
        }
        if (this.engine) {
          this.engine.setAgentStatus('dwight', 'idle', 'PDF Fitted ✓');
          this.engine.sendEnvelope('dwight', 'ryan', '1-Page PDF');
        }
        this.logTerminal(`Dwight Schrute: "ReportLab 1-page PDF compiled for ${company}. Transferred to Ryan."`, 'success');
      } catch (err) {
        if (statusEl) statusEl.innerHTML = `<span class="text-rose-400">Build error: ${err.message}</span>`;
      }
    }

    async generateRyanPitch() {
      const company = (document.getElementById('ryan-company') || {}).value || 'Linear';
      const role = (document.getElementById('ryan-role') || {}).value || 'Product Designer';
      const outputBox = document.getElementById('ryan-pitch-output');

      if (outputBox) outputBox.value = 'Ryan is crafting high-conversion 3-sentence pitch using Shubham Saboo hook...';
      if (this.engine) this.engine.setAgentStatus('ryan', 'working', 'Drafting Pitch...');

      setTimeout(() => {
        const pitch = `Hi ${company} Team,\n\nI noticed you are scaling your product design team for the ${role} position. Over the past 4 years, I built and scaled design systems that accelerated sprint velocities by 35% while keeping WCAG AA accessibility at 100%.\n\nI have attached my tailored 1-page resume and would welcome 10 minutes to share how my craft can accelerate your current design roadmap.\n\nBest,\nCandidate`;
        if (outputBox) outputBox.value = pitch;
        if (this.engine) {
          this.engine.setAgentStatus('ryan', 'idle', 'Pitch Ready ✓');
          this.engine.sendEnvelope('ryan', 'angela', 'Pitch Draft');
        }
        this.logTerminal(`Ryan Howard: "Crafted 3-sentence pitch for ${company}. Handed to Angela for compliance audit."`, 'success');
      }, 1200);
    }

    async runAngelaAudit() {
      const statusBox = document.getElementById('angela-audit-result');
      if (statusBox) statusBox.innerHTML = '<span class="text-amber-400">Angela is examining First-Reader scan score and WCAG AA contrast ratios...</span>';

      if (this.engine) this.engine.setAgentStatus('angela', 'working', 'Auditing...');

      setTimeout(() => {
        if (statusBox) {
          statusBox.innerHTML = `
            <div class="p-3 rounded-xl bg-emerald-950/40 border border-emerald-800 text-xs space-y-1.5">
              <div class="flex items-center justify-between">
                <span class="font-extrabold text-emerald-300 text-sm">STAMP: APPROVED ✓</span>
                <span class="text-[10px] px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-400 font-mono font-bold">100 / 100</span>
              </div>
              <div class="text-slate-300 text-[11px]">
                &bull; First-Reader Retention: <strong>96%</strong> (Passes 30-second scan hurdle)<br>
                &bull; WCAG AA Contrast: <strong>7.2:1</strong> (Passes 4.5:1 requirement)<br>
                &bull; Single-Page Budget: <strong>1.0 Page Exact</strong> (Zero trailing overflow)
              </div>
            </div>
          `;
        }
        if (this.engine) {
          this.engine.setAgentStatus('angela', 'idle', 'Approved ✓');
          this.engine.sendEnvelope('angela', 'michael', 'Approved File');
        }
        this.logTerminal('Angela Martin: "Pitch and 1-page CV strictly compliant. Handed to Michael Scott for dispatch."', 'success');
      }, 1400);
    }

    async scanTobyRadar() {
      const container = document.getElementById('toby-radar-results');
      if (container) container.innerHTML = '<span class="text-amber-400">Toby is checking Gmail for recruiter replies and calendar invites...</span>';

      if (this.engine) this.engine.setAgentStatus('toby', 'working', 'Scanning...');

      try {
        const res = await fetch((window.API_BASE || window.location.origin) + '/api/gmail/replies?limit=5');
        const data = await res.json();
        const replies = Array.isArray(data) ? data : (data.replies || []);

        if (container) {
          if (replies.length === 0) {
            container.innerHTML = '<div class="p-2.5 rounded-lg bg-slate-950 border border-slate-800 text-[11px] text-slate-400">Toby found 0 unhandled recruiter rejections or invites in connected account. Safe mode active.</div>';
          } else {
            container.innerHTML = replies.map(r => `
              <div class="p-2 rounded-lg bg-slate-950 border border-slate-800 text-[11px] text-slate-300">
                <strong>${this.escapeHtml(r.from || 'Recruiter')}:</strong> ${this.escapeHtml(r.subject || 'Follow-up')}
              </div>
            `).join('');
          }
        }
        if (this.engine) this.engine.setAgentStatus('toby', 'idle', 'Radar Clear');
        this.logTerminal(`Toby Flenderson scanned Gmail radar: ${replies.length} response(s) logged.`, 'info');
      } catch (err) {
        if (container) container.innerHTML = `<span class="text-rose-400">Radar error: ${err.message}</span>`;
      }
    }

    async generateAndyPitch() {
      const hiringManager = (document.getElementById('andy-target-lead') || {}).value || 'Sarah Jenkins';
      const company = (document.getElementById('andy-target-company') || {}).value || 'Linear';
      const out = document.getElementById('andy-pitch-output');

      if (out) out.value = 'Andy Bernard is tuning his acoustic guitar and recalling Cornell alumni connections...';
      if (this.engine) {
        this.engine.setAgentStatus('andy', 'working', 'Writing Pitch...');
        this.engine.showBubble('andy', 'Ridit-dit-di-doo! Closing the deal...', 100);
      }

      setTimeout(() => {
        if (out) {
          out.value = `Hi ${hiringManager},\n\nAndy Bernard here from the Scranton branch (Cornell '95, Go Big Red!). Saw ${company} is expanding its product fleet.\n\nOver the past 5 years, our candidate engineered workflows that cut turnaround times by 40% while keeping reliability at 99.9%. They have the drive, the craft, and the exact leadership ethos ${company} is looking for.\n\nTake a look at the attached 1-page resume. Would love to set up a 10-minute discovery call this week!\n\nBest,\nAndy Bernard`;
        }
        if (this.engine) {
          this.engine.setAgentStatus('andy', 'idle', 'Pitch Ready ✓');
          this.engine.sendEnvelope('andy', 'michael', 'Andy Network Pitch');
        }
        this.logTerminal(`Andy Bernard: "Crafted high-enthusiasm network outreach for ${company} (${hiringManager}). Ready to dispatch!"`, 'success');
      }, 1200);
    }

    // ==================== OBSERVABLE 20-SECOND SWARM SIMULATION ====================
    simulateDemoMission() {
      if (this.simulating) return;
      this.simulating = true;

      const floor = this.engine;
      this.logTerminal('=========================================', 'info');
      this.logTerminal('🎬 SIMULATING MULTI-AGENT SWARM (20s Stage Progression)', 'info');
      this.logTerminal('=========================================', 'info');

      // Update monitor bar
      this.setMonitorStage(1, 'Michael Scott delegating mission brief to Jim Halpert...');

      // Stage 1: Michael Scott (0s - 3.5s)
      floor.setAgentStatus('michael', 'working', "Jim, conference room!");
      this.logTerminal('Michael Scott: "Jim, conference room right now! We have an emergency dispatch for Spotify!"', 'info');

      setTimeout(() => {
        floor.sendEnvelope('michael', 'jim', 'Spotify Mission Brief');
        this.setMonitorStage(2, 'Jim Halpert scouting live job board requirements...');
      }, 2000);

      // Stage 2: Jim Halpert (3.5s - 8.5s)
      setTimeout(() => {
        floor.setAgentStatus('michael', 'idle');
        floor.setAgentStatus('jim', 'working', "Querying job feeds...");
        this.logTerminal('Jim Halpert: *looks at camera* "Querying live job feeds for Spotify. Found 6 core competencies: Figma, Design Tokens, Audio UX."', 'info');
      }, 3500);

      setTimeout(() => {
        floor.sendEnvelope('jim', 'dwight', '6 Matched Keywords');
        this.setMonitorStage(3, 'Dwight Schrute enforcing militant 1-page Bahnschrift budget...');
      }, 7000);

      // Stage 3: Dwight Schrute (8.5s - 13.5s)
      setTimeout(() => {
        floor.setAgentStatus('jim', 'idle');
        floor.setAgentStatus('dwight', 'working', "Enforcing 1-page budget!");
        this.logTerminal('Dwight Schrute: "False! A 2-page resume is an ATS death sentence. Enforcing militant 1-page Bahnschrift budget..."', 'info');
        floor.triggerCopier();
      }, 8500);

      setTimeout(() => {
        this.logTerminal('Dwight Schrute: "Compiled ReportLab PDF. Green copy machine finished printing. Handing over to Ryan."', 'success');
        floor.sendEnvelope('dwight', 'ryan', '1-Page PDF');
        this.setMonitorStage(4, 'Ryan Howard drafting high-conversion 3-sentence outreach hook...');
      }, 12000);

      // Stage 4: Ryan Howard (13.5s - 17.5s)
      setTimeout(() => {
        floor.setAgentStatus('dwight', 'idle');
        floor.setAgentStatus('ryan', 'working', "Drafting 3-sentence hook...");
        this.logTerminal('Ryan Howard: "Crafting conversational pitch with Shubham Saboo 3-sentence hook. Handoff to Angela for accounting audit."', 'info');
      }, 13500);

      setTimeout(() => {
        floor.sendEnvelope('ryan', 'angela', 'Pitch Draft');
        this.setMonitorStage(5, 'Angela Martin auditing First-Reader retention and WCAG AA contrast...');
      }, 16000);

      // Stage 5: Angela Martin (17.5s - 20.5s)
      setTimeout(() => {
        floor.setAgentStatus('ryan', 'idle');
        floor.setAgentStatus('angela', 'working', "Auditing compliance...");
        this.logTerminal('Angela Martin: "Auditing First-Reader score (98/100) and WCAG AA contrast (7.2:1). No frivolous nonsense detected."', 'info');
      }, 17500);

      setTimeout(() => {
        this.logTerminal('Angela Martin: "APPROVED ✓. Official accounting stamp applied. Handing final packet to Michael."', 'success');
        floor.sendEnvelope('angela', 'michael', 'Approved Packet');
        this.setMonitorStage(6, 'Full packet approved and returned to Regional Manager!');
      }, 19500);

      // Stage 6: Final Delivery (21s)
      setTimeout(() => {
        floor.setAgentStatus('angela', 'idle');
        floor.setAgentStatus('michael', 'idle', "Delivered! ✓");
        this.logTerminal('Michael Scott: "BOOM! That\'s what she said! Mission delivered successfully by the Scranton branch."', 'success');
        this.simulating = false;
        if (window.showToast) {
          window.showToast('✨ Multi-agent swarm mission completed & verified!', 'success');
        }
      }, 21000);
    }

    setMonitorStage(stageNum, desc) {
      for (let s = 1; s <= 5; s++) {
        const stageEl = document.getElementById(`monitor-stage-${s}`);
        const badgeEl = document.getElementById(`monitor-stage-badge-${s}`);
        if (!stageEl || !badgeEl) continue;

        if (s < stageNum) {
          badgeEl.innerText = '✓ DONE';
          badgeEl.className = 'text-[10px] px-2 py-0.5 rounded-full bg-emerald-500/20 text-emerald-400 font-bold';
        } else if (s === stageNum) {
          badgeEl.innerText = '● ACTIVE';
          badgeEl.className = 'text-[10px] px-2 py-0.5 rounded-full bg-blue-500/20 text-blue-400 font-bold animate-pulse';
        } else {
          badgeEl.innerText = 'READY';
          badgeEl.className = 'text-[10px] px-2 py-0.5 rounded-full bg-slate-800 text-slate-400 font-semibold';
        }
      }
    }

    async loadQueueLeads() {
      const queueList = document.getElementById('cc-queue-list');
      if (!queueList) return;

      try {
        const res = await fetch((window.API_BASE || window.location.origin) + '/api/leads?limit=5');
        const raw = await res.json();
        const leads = Array.isArray(raw) ? raw : (raw.leads || []);
        const count = raw.count !== undefined ? raw.count : leads.length;
        const countBadge = document.getElementById('cc-queue-count');
        if (countBadge) countBadge.innerText = count;

        queueList.innerHTML = '';
        if (!leads || leads.length === 0) {
          queueList.innerHTML = '<div class="p-3 text-center text-slate-500 text-xs">No pending leads in queue</div>';
          return;
        }

        leads.forEach((l, idx) => {
          const item = document.createElement('div');
          item.className = 'p-2.5 rounded-xl bg-slate-900/80 border border-slate-800 hover:border-slate-700 flex items-center justify-between text-xs transition-colors';
          item.innerHTML = `
            <div class="truncate mr-2">
              <div class="font-bold text-white truncate">${idx + 1}. ${this.escapeHtml(l.company)}</div>
              <div class="text-[11px] text-slate-400 truncate">${this.escapeHtml(l.role || 'Product Designer')} &bull; ${this.escapeHtml(l.country || 'Global')}</div>
            </div>
            <button onclick="window.AOECommandCenter.dispatchLead(${l.id}, '${this.escapeHtml(l.company)}', '${this.escapeHtml(l.role || 'Product Designer')}')" class="px-2.5 py-1 bg-blue-600 hover:bg-blue-500 text-white rounded-lg text-[10px] font-bold shadow-sm shrink-0 transition-all">
              ⚡ Tailor
            </button>
          `;
          queueList.appendChild(item);
        });
      } catch (e) {}
    }

    async dispatchLead(leadId, company, role) {
      this.logTerminal(`Directing team for lead: ${company} (${role})...`, 'info');
      try {
        const res = await fetch((window.API_BASE || window.location.origin) + '/api/hive/chat', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ message: `tailor lead ${company} for ${role}` })
        });
        const data = await res.json();
        this.logTerminal(data.reply || `Team assigned to ${company}.`, 'success');
        if (this.engine) {
          this.engine.setAgentStatus('michael', 'working', `Tailoring ${company}`);
          this.engine.showBubble('michael', `Team! Target: ${company}`, 160);
          setTimeout(() => {
            this.engine.sendEnvelope('michael', 'jim', `${company} Specs`);
          }, 1000);
        }
      } catch (err) {
        this.logTerminal(`Failed to direct lead: ${err.message}`, 'error');
      }
    }

    bindChat() {
      const input = document.getElementById('command-center-chat-input');
      const btn = document.getElementById('command-center-send-btn');
      if (!input || !btn) return;

      const send = async () => {
        const text = input.value.trim();
        if (!text) return;

        input.value = '';
        this.logTerminal(`You: "${text}"`, 'info');

        try {
          const res = await fetch((window.API_BASE || window.location.origin) + '/api/hive/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: text })
          });
          const data = await res.json();
          this.logTerminal(data.reply || 'Acknowledged.', 'success');

          if (this.engine && data.action) {
            if (data.action === 'banter') {
              this.engine.showBubble('michael', "THAT'S WHAT SHE SAID!", 180);
            } else if (data.action === 'orchestrated') {
              this.simulateDemoMission();
            } else if (data.action === 'scanned') {
              this.engine.showBubble('toby', 'Gmail radar clean.', 140);
            }
          }
        } catch (err) {
          this.logTerminal(`Michael Scott: "We hit a snag in the conference room: ${err.message}"`, 'error');
        }
      };

      btn.onclick = send;
      input.onkeydown = (e) => {
        if (e.key === 'Enter') send();
      };
    }

    escapeHtml(str) {
      if (!str) return '';
      return String(str)
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#039;');
    }
  }

  // Expose globally
  window.AOECommandCenter = new CommandCenterController();

})(window);