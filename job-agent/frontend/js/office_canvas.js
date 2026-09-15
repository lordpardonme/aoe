/**
 * AOE Operations Floor — Authentic Munder Difflin 2D Tilemap & Pixel-Art Engine
 * Renders the genuine LimeZu RPG Modern Office tileset (office.tmj) and procedural character sprites.
 * Layer order matches Munder Difflin TiledMapRenderer (all tile layers composited first, characters on top).
 */

(function(window) {
  'use strict';

  class OfficeFloorEngine {
    constructor(canvasId) {
      this.canvas = document.getElementById(canvasId);
      if (!this.canvas) return;
      this.ctx = this.canvas.getContext('2d');
      this.width = 1088;
      this.height = 704;
      this.scale = 1;

      this.selectedAgentId = 'michael';
      this.hoveredDesk = null;
      this.tick = 0;
      this.particles = [];
      this.flyingEnvelopes = [];
      this.copierPrinting = false;
      this.copierTimer = 0;

      // Authentic Munder Difflin Complete Composited Floor Layer
      this.floorFullImg = new Image();
      this.floorFullImg.src = 'assets/maps/office_floor_full.png';

      // Fallback layers
      this.floorBelowImg = new Image();
      this.floorBelowImg.src = 'assets/maps/office_floor_below.png';
      this.furnitureAboveImg = new Image();
      this.furnitureAboveImg.src = 'assets/maps/office_furniture_above.png';

      // Authentic Scranton Cast & Coordinate Map (34x22 Tile Grid @ 32px per tile)
      // Stool coordinates centered on chairs
      this.agents = {
        michael: {
          id: 'michael',
          name: 'Michael Scott',
          role: 'regional_manager',
          title: 'Regional Manager (Supervisor)',
          status: 'idle',
          deskX: 112, // Tile (3, 5) - CEO Office stool
          deskY: 176,
          screenX: 96,
          screenY: 136,
          facing: 'down',
          bubbleText: '',
          bubbleTimer: 0,
          quote: "That's what she said!",
          stats: { completed: 18, tokens: '4.2k', score: '100%' }
        },
        jim: {
          id: 'jim',
          name: 'Jim Halpert',
          role: 'job_scout',
          title: 'Job Scout & Taxonomy Extractor',
          status: 'idle',
          deskX: 80, // Tile (2, 13) - Bullpen Row 1, Stool 1
          deskY: 432,
          screenX: 73,
          screenY: 391,
          facing: 'down',
          bubbleText: '',
          bubbleTimer: 0,
          quote: "*looks at camera*",
          stats: { completed: 14, tokens: '3.1k', score: '96%' }
        },
        dwight: {
          id: 'dwight',
          name: 'Dwight Schrute',
          role: 'resume_architect',
          title: 'Resume Architect (1-Page Bahnschrift)',
          status: 'idle',
          deskX: 208, // Tile (6, 13) - Bullpen Row 1, Stool 2
          deskY: 432,
          screenX: 201,
          screenY: 391,
          facing: 'down',
          bubbleText: '',
          bubbleTimer: 0,
          quote: "Question: What bear is best? False.",
          stats: { completed: 14, tokens: '5.2k', score: '99%' }
        },
        pam: {
          id: 'pam',
          name: 'Pam Beesly',
          role: 'intake_reception',
          title: 'Reception & Candidate Evidence Intake',
          status: 'idle',
          deskX: 336, // Tile (10, 13) - Bullpen Row 1, Stool 3
          deskY: 432,
          screenX: 329,
          screenY: 391,
          facing: 'down',
          bubbleText: '',
          bubbleTimer: 0,
          quote: "Dunder Mifflin, this is Pam.",
          stats: { completed: 22, tokens: '2.4k', score: '98%' }
        },
        ryan: {
          id: 'ryan',
          name: 'Ryan Howard',
          role: 'outreach_copywriter',
          title: 'Outreach Copywriter (3-Sentence Pitch)',
          status: 'idle',
          deskX: 464, // Tile (14, 13) - Bullpen Row 1, Stool 4
          deskY: 432,
          screenX: 457,
          screenY: 391,
          facing: 'down',
          bubbleText: '',
          bubbleTimer: 0,
          quote: "Just drafted a 3-sentence hook.",
          stats: { completed: 9, tokens: '2.8k', score: '94%' }
        },
        angela: {
          id: 'angela',
          name: 'Angela Martin',
          role: 'quality_auditor',
          title: 'Quality Auditor (First-Reader & WCAG AA)',
          status: 'idle',
          deskX: 592, // Tile (18, 13) - Bullpen Row 1, Stool 5
          deskY: 432,
          screenX: 585,
          screenY: 391,
          facing: 'down',
          bubbleText: '',
          bubbleTimer: 0,
          quote: "First-Reader score must be flawless.",
          stats: { completed: 14, tokens: '1.5k', score: '100%' }
        },
        andy: {
          id: 'andy',
          name: 'Andy Bernard',
          role: 'sales_outreach',
          title: 'Regional Outreach (Cornell Pitch)',
          status: 'idle',
          deskX: 720, // Tile (22, 13) - Bullpen Row 1, Stool 6
          deskY: 432,
          screenX: 713,
          screenY: 391,
          facing: 'down',
          bubbleText: '',
          bubbleTimer: 0,
          quote: "Rit-dit-dit-di-doo! Andy Bernard, Cornell '95.",
          stats: { completed: 11, tokens: '1.8k', score: '95%' }
        },
        toby: {
          id: 'toby',
          name: 'Toby Flenderson',
          role: 'recruiter_radar',
          title: 'Annex Radar (Gmail Recruiter Scanner)',
          status: 'idle',
          deskX: 880, // Tile (27, 6) - Top Right Annex Stool
          deskY: 208,
          screenX: 873,
          screenY: 167,
          facing: 'down',
          bubbleText: '',
          bubbleTimer: 0,
          quote: "Checking Gmail in the annex...",
          stats: { completed: 25, tokens: '950', score: '100%' }
        },
        kevin: {
          id: 'kevin',
          name: 'Kevin Malone',
          role: 'accountant',
          title: 'Accounting & Analytics',
          status: 'idle',
          deskX: 80, // Tile (2, 18) - Bullpen Row 2, Stool 1
          deskY: 592,
          screenX: 73,
          screenY: 551,
          facing: 'down',
          bubbleText: '',
          bubbleTimer: 0,
          quote: "A mistake plus keleven gets you home by seven.",
          stats: { completed: 12, tokens: '1.2k', score: '92%' }
        },
        oscar: {
          id: 'oscar',
          name: 'Oscar Martinez',
          role: 'accountant',
          title: 'Senior Accounting & Ledger Auditor',
          status: 'idle',
          deskX: 208, // Tile (6, 18) - Bullpen Row 2, Stool 2
          deskY: 592,
          screenX: 201,
          screenY: 551,
          facing: 'down',
          bubbleText: '',
          bubbleTimer: 0,
          quote: "Actually, that's not how it works.",
          stats: { completed: 19, tokens: '3.4k', score: '99%' }
        },
        stanley: {
          id: 'stanley',
          name: 'Stanley Hudson',
          role: 'sales',
          title: 'Senior Sales & Account Retention',
          status: 'idle',
          deskX: 336, // Tile (10, 18) - Bullpen Row 2, Stool 3
          deskY: 592,
          screenX: 329,
          screenY: 551,
          facing: 'down',
          bubbleText: '',
          bubbleTimer: 0,
          quote: "Did I stutter?",
          stats: { completed: 16, tokens: '2.1k', score: '96%' }
        },
        phyllis: {
          id: 'phyllis',
          name: 'Phyllis Vance',
          role: 'sales',
          title: 'Regional Sales & Client Relationships',
          status: 'idle',
          deskX: 464, // Tile (14, 18) - Bullpen Row 2, Stool 4
          deskY: 592,
          screenX: 457,
          screenY: 551,
          facing: 'down',
          bubbleText: '',
          bubbleTimer: 0,
          quote: "Bob Vance, Vance Refrigeration.",
          stats: { completed: 15, tokens: '1.9k', score: '95%' }
        },
        kelly: {
          id: 'kelly',
          name: 'Kelly Kapoor',
          role: 'customer_support',
          title: 'Customer Service & Engagement',
          status: 'idle',
          deskX: 592, // Tile (18, 18) - Bullpen Row 2, Stool 5
          deskY: 592,
          screenX: 585,
          screenY: 551,
          facing: 'down',
          bubbleText: '',
          bubbleTimer: 0,
          quote: "Number one: how dare you?",
          stats: { completed: 17, tokens: '2.5k', score: '97%' }
        },
        meredith: {
          id: 'meredith',
          name: 'Meredith Palmer',
          role: 'supplier_relations',
          title: 'Supplier Relations & Purchasing',
          status: 'idle',
          deskX: 720, // Tile (22, 18) - Bullpen Row 2, Stool 6
          deskY: 592,
          screenX: 713,
          screenY: 551,
          facing: 'down',
          bubbleText: '',
          bubbleTimer: 0,
          quote: "It's 5 o'clock somewhere.",
          stats: { completed: 10, tokens: '1.1k', score: '90%' }
        },
        creed: {
          id: 'creed',
          name: 'Creed Bratton',
          role: 'quality_assurance',
          title: 'Quality Assurance (Quabity Assuance)',
          status: 'idle',
          deskX: 656, // Tile (20, 8) - Mid-row stool
          deskY: 272,
          screenX: 649,
          screenY: 231,
          facing: 'down',
          bubbleText: '',
          bubbleTimer: 0,
          quote: "Nobody steals from Creed Bratton.",
          stats: { completed: 8, tokens: '800', score: '99%' }
        }
      };

      // Backward-compatible aliases
      this.agents.supervisor = this.agents.michael;
      this.agents.scout = this.agents.jim;
      this.agents.resume_architect = this.agents.dwight;
      this.agents.copywriter = this.agents.ryan;
      this.agents.quality_reviewer = this.agents.angela;
      this.agents.recruiter_scanner = this.agents.toby;
      this.agents.andy_bernard = this.agents.andy;

      this.initCanvas();
      this.bindEvents();
      this.startLoop();
    }

    initCanvas() {
      const dpr = window.devicePixelRatio || 1;
      this.canvas.width = this.width * dpr;
      this.canvas.height = this.height * dpr;
      this.ctx.scale(dpr, dpr);
      this.ctx.imageSmoothingEnabled = false;
    }

    bindEvents() {
      window.addEventListener('resize', () => this.initCanvas());

      this.canvas.addEventListener('mousemove', (e) => {
        const rect = this.canvas.getBoundingClientRect();
        const scaleX = this.width / rect.width;
        const scaleY = this.height / rect.height;
        const mouseX = (e.clientX - rect.left) * scaleX;
        const mouseY = (e.clientY - rect.top) * scaleY;

        let found = null;
        for (const key of Object.keys(this.agents)) {
          const agent = this.agents[key];
          if (agent.id !== key) continue;
          // Hitbox covering desk + computer + chair
          if (
            mouseX >= agent.deskX - 32 &&
            mouseX <= agent.deskX + 32 &&
            mouseY >= agent.deskY - 50 &&
            mouseY <= agent.deskY + 20
          ) {
            found = agent.id;
            break;
          }
        }
        this.hoveredDesk = found;
        this.canvas.style.cursor = found ? 'pointer' : 'default';
      });

      this.canvas.addEventListener('click', (e) => {
        const rect = this.canvas.getBoundingClientRect();
        const scaleX = this.width / rect.width;
        const scaleY = this.height / rect.height;
        const mouseX = (e.clientX - rect.left) * scaleX;
        const mouseY = (e.clientY - rect.top) * scaleY;

        for (const key of Object.keys(this.agents)) {
          const agent = this.agents[key];
          if (agent.id !== key) continue;
          if (
            mouseX >= agent.deskX - 32 &&
            mouseX <= agent.deskX + 32 &&
            mouseY >= agent.deskY - 50 &&
            mouseY <= agent.deskY + 20
          ) {
            this.selectAgent(agent.id);
            if (window.AOECommandCenter && typeof window.AOECommandCenter.onAgentSelected === 'function') {
              window.AOECommandCenter.onAgentSelected(agent);
            }
            break;
          }
        }
      });
    }

    selectAgent(agentId) {
      if (this.agents[agentId]) {
        this.selectedAgentId = agentId;
      }
    }

    setAgentStatus(agentId, status, bubble = '') {
      const agent = this.agents[agentId];
      if (agent) {
        agent.status = status;
        if (bubble) {
          agent.bubbleText = bubble;
          agent.bubbleTimer = 180;
        }
      }
    }

    showBubble(agentId, text, duration = 180) {
      const agent = this.agents[agentId];
      if (agent) {
        agent.bubbleText = text;
        agent.bubbleTimer = duration;
      }
    }

    sendEnvelope(fromAgentId, toAgentId, artifact = 'CV Draft') {
      const from = this.agents[fromAgentId];
      const to = this.agents[toAgentId];
      if (!from || !to) return;

      this.flyingEnvelopes.push({
        fromX: from.deskX,
        fromY: from.deskY - 20,
        toX: to.deskX,
        toY: to.deskY - 20,
        progress: 0,
        speed: 0.024,
        artifact: artifact
      });
    }

    triggerCopier() {
      this.copierPrinting = true;
      this.copierTimer = 120;
    }

    startLoop() {
      const loop = () => {
        this.render();
        requestAnimationFrame(loop);
      };
      requestAnimationFrame(loop);
    }

    render() {
      this.tick++;
      const ctx = this.ctx;
      ctx.clearRect(0, 0, this.width, this.height);
      ctx.imageSmoothingEnabled = false;

      // 1. Pristine Full Tilemap (Floors, Walls, Desks, Stools, Props, Copier, Kitchen)
      if (this.floorFullImg.complete && this.floorFullImg.naturalWidth > 0) {
        ctx.drawImage(this.floorFullImg, 0, 0, this.width, this.height);
      } else if (this.floorBelowImg.complete && this.floorBelowImg.naturalWidth > 0) {
        ctx.drawImage(this.floorBelowImg, 0, 0, this.width, this.height);
        if (this.furnitureAboveImg.complete) ctx.drawImage(this.furnitureAboveImg, 0, 0, this.width, this.height);
      } else {
        ctx.fillStyle = '#1a1320';
        ctx.fillRect(0, 0, this.width, this.height);
      }

      // 2. Animated CRT Monitor Screens (DeskScreen Logic)
      this.drawMonitorScreens(ctx);

      // 3. Authentic Cast Members (Stationed Seated on Stools, Unoccluded Faces)
      this.drawAgents(ctx);

      // 4. Dynamic Props (Animated Xerox Copier, Coffee Steam)
      this.drawAnimatedProps(ctx);

      // 5. Flying Envelopes & Sparkle Dust
      this.drawFlyingEnvelopes(ctx);
      this.drawParticles(ctx);

      // 6. Interactive UI Overlays (Selected desk frame, hover tooltip, speech bubbles)
      this.drawUIOverlays(ctx);
    }

    drawMonitorScreens(ctx) {
      for (const key of Object.keys(this.agents)) {
        const agent = this.agents[key];
        if (agent.id !== key || !agent.screenX) continue;

        const isWorking = agent.status === 'working';
        const sx = agent.screenX;
        const sy = agent.screenY;

        if (isWorking) {
          // Lit blue CRT desktop
          ctx.fillStyle = '#38bdf8';
          ctx.fillRect(sx, sy, 14, 8);

          // Scrolling scan lines
          ctx.fillStyle = 'rgba(255, 255, 255, 0.7)';
          const p1 = (this.tick * 0.5) % 6;
          const p2 = ((this.tick * 0.5) + 3) % 6;
          ctx.fillRect(sx + 1, Math.floor(sy + 1 + p1), 8, 1);
          ctx.fillRect(sx + 1, Math.floor(sy + 1 + p2), 6, 1);

          // Blinking white cursor
          if (Math.floor(this.tick / 15) % 2 === 0) {
            ctx.fillStyle = '#ffffff';
            ctx.fillRect(sx + 10, sy + 5, 2, 2);
          }

          // Ambient glow
          ctx.fillStyle = 'rgba(56, 189, 248, 0.15)';
          ctx.beginPath();
          ctx.arc(agent.deskX, agent.deskY - 24, 18, 0, Math.PI * 2);
          ctx.fill();
        } else {
          // Dimmed standby screen
          ctx.fillStyle = '#1e293b';
          ctx.fillRect(sx, sy, 14, 8);
        }
      }
    }

    drawAgents(ctx) {
      for (const key of Object.keys(this.agents)) {
        const agent = this.agents[key];
        if (agent.id !== key) continue;
        this.drawCharacter(ctx, agent);
      }
    }

    drawCharacter(ctx, agent) {
      const isWorking = agent.status === 'working';
      const bob = isWorking ? Math.sin(this.tick * 0.35) * 1.2 : Math.sin(this.tick * 0.05) * 0.5;

      const x = agent.deskX;
      const y = agent.deskY;

      // Authentic Munder Difflin Seated Sprite (Cropped legs tucked under desk)
      const scale = 1.6;
      const sw = 18 * scale;
      const sh = 24 * scale; // seated height
      const phase = isWorking ? Math.floor(this.tick / 8) % 3 : 0;
      const isBack = agent.facing === 'up';
      const sx = Math.round(x - sw / 2);
      const sy = Math.round(y - sh + 8 + bob);

      if (window.PortraitArt && typeof window.PortraitArt.paintSeatedSprite === 'function') {
        window.PortraitArt.paintSeatedSprite(ctx, agent.id, phase, isBack, scale, sx, sy);
      } else if (window.PortraitArt && typeof window.PortraitArt.paintSceneSprite === 'function') {
        window.PortraitArt.paintSceneSprite(ctx, agent.id, phase, isBack, scale, sx, sy);
      } else {
        ctx.fillStyle = '#1e293b';
        ctx.fillRect(x - 9, y - 24, 18, 24);
      }
    }

    drawAnimatedProps(ctx) {
      // 1. Green Xerox Machine (Located near Cafeteria at tile 30, 14 -> x: 960, y: 448)
      const cpx = 968;
      const cpy = 448;

      // Blinking Green LED on Copier
      const ledOn = this.copierPrinting ? (this.tick % 10 < 5) : true;
      ctx.fillStyle = ledOn ? '#22c55e' : '#15803d';
      ctx.beginPath();
      ctx.arc(cpx + 32, cpy + 10, 3, 0, Math.PI * 2);
      ctx.fill();

      // Paper Sheet Ejection Animation
      if (this.copierPrinting && this.copierTimer > 0) {
        this.copierTimer--;
        const slide = (this.tick % 16);
        ctx.fillStyle = '#ffffff';
        ctx.fillRect(cpx - 10 - slide, cpy + 26, 14, 10);
        ctx.strokeStyle = '#334155';
        ctx.lineWidth = 1;
        ctx.strokeRect(cpx - 10 - slide, cpy + 26, 14, 10);

        if (this.copierTimer === 0) {
          this.copierPrinting = false;
        }
      }

      // 2. Coffee Maker Steam (Located on kitchen counter at x: 772, y: 636)
      if (this.tick % 6 === 0) {
        this.particles.push({
          x: 772 + (Math.random() * 4 - 2),
          y: 636,
          vx: (Math.random() - 0.5) * 0.3,
          vy: -0.6 - Math.random() * 0.4,
          life: 25,
          color: 'rgba(240, 240, 240, 0.7)'
        });
      }
    }

    drawFlyingEnvelopes(ctx) {
      for (let i = this.flyingEnvelopes.length - 1; i >= 0; i--) {
        const env = this.flyingEnvelopes[i];
        env.progress += env.speed;

        const t = env.progress;
        env.x = env.fromX + (env.toX - env.fromX) * t;
        const arc = Math.sin(t * Math.PI) * 45;
        env.y = env.fromY + (env.toY - env.fromY) * t - arc;

        // Golden sparkle trail
        if (this.tick % 2 === 0) {
          this.particles.push({
            x: env.x,
            y: env.y,
            vx: (Math.random() - 0.5) * 0.6,
            vy: (Math.random() - 0.5) * 0.6,
            life: 20,
            color: '#fbbf24'
          });
        }

        // Crisp pixel envelope
        ctx.fillStyle = '#fef08a';
        ctx.fillRect(env.x - 7, env.y - 5, 14, 10);
        ctx.strokeStyle = '#b45309';
        ctx.lineWidth = 1;
        ctx.strokeRect(env.x - 7, env.y - 5, 14, 10);

        ctx.beginPath();
        ctx.moveTo(env.x - 7, env.y - 5);
        ctx.lineTo(env.x, env.y);
        ctx.lineTo(env.x + 7, env.y - 5);
        ctx.stroke();

        if (env.progress >= 1) {
          this.flyingEnvelopes.splice(i, 1);
        }
      }
    }

    drawParticles(ctx) {
      for (let i = this.particles.length - 1; i >= 0; i--) {
        const p = this.particles[i];
        p.x += p.vx;
        p.y += p.vy;
        p.life--;

        ctx.fillStyle = p.color;
        ctx.fillRect(p.x, p.y, 2, 2);

        if (p.life <= 0) {
          this.particles.splice(i, 1);
        }
      }
    }

    drawUIOverlays(ctx) {
      for (const key of Object.keys(this.agents)) {
        const agent = this.agents[key];
        if (agent.id !== key) continue;

        const isSelected = this.selectedAgentId === agent.id;
        const isHovered = this.hoveredDesk === agent.id;

        // Clean selection frame around desk + stool
        if (isSelected) {
          ctx.strokeStyle = '#f59e0b';
          ctx.lineWidth = 2;
          ctx.strokeRect(agent.deskX - 22, agent.deskY - 48, 44, 56);

          // Subtle corner accents
          ctx.fillStyle = '#f59e0b';
          ctx.fillRect(agent.deskX - 23, agent.deskY - 49, 4, 4);
          ctx.fillRect(agent.deskX + 19, agent.deskY - 49, 4, 4);
          ctx.fillRect(agent.deskX - 23, agent.deskY + 5, 4, 4);
          ctx.fillRect(agent.deskX + 19, agent.deskY + 5, 4, 4);
        } else if (isHovered) {
          ctx.strokeStyle = '#38bdf8';
          ctx.lineWidth = 1.5;
          ctx.setLineDash([4, 2]);
          ctx.strokeRect(agent.deskX - 22, agent.deskY - 48, 44, 56);
          ctx.setLineDash([]);

          // Overhead hover tooltip
          this.drawHoverTooltip(ctx, agent.deskX, agent.deskY - 56, agent.name, agent.title.split('(')[0].trim());
        }

        // Overhead Speech Bubble (when talking or working)
        if (agent.bubbleText && agent.bubbleTimer > 0) {
          agent.bubbleTimer--;
          this.drawSpeechBubble(ctx, agent.deskX, agent.deskY - 50, agent.bubbleText, '#ffffff', '#0f172a', '#2563eb');
        } else if (agent.status === 'working') {
          const dots = '.'.repeat((Math.floor(this.tick / 15) % 3) + 1);
          this.drawSpeechBubble(ctx, agent.deskX, agent.deskY - 50, 'working' + dots, '#ecfdf5', '#065f46', '#10b981');
        } else if (agent.id === 'michael' && !agent.bubbleText) {
          this.drawSpeechBubble(ctx, agent.deskX, agent.deskY - 50, 'awaiting', '#ffffff', '#334155', '#94a3b8');
        }
      }
    }

    drawHoverTooltip(ctx, x, y, name, role) {
      ctx.font = 'bold 9px "Inter", sans-serif';
      const nameWidth = ctx.measureText(name).width;
      ctx.font = '8px "Inter", sans-serif';
      const roleWidth = ctx.measureText(role).width;
      const w = Math.max(nameWidth, roleWidth) + 16;
      const h = 26;
      const bx = Math.round(x - w / 2);
      const by = Math.round(y - h);

      // Pixel dark panel
      ctx.fillStyle = 'rgba(26, 19, 32, 0.95)';
      ctx.fillRect(bx, by, w, h);
      ctx.strokeStyle = '#787684';
      ctx.lineWidth = 1;
      ctx.strokeRect(bx, by, w, h);

      // Name
      ctx.font = 'bold 9px "Inter", sans-serif';
      ctx.fillStyle = '#ffffff';
      ctx.textAlign = 'center';
      ctx.fillText(name, x, by + 11);

      // Role
      ctx.font = '8px "Inter", sans-serif';
      ctx.fillStyle = '#94a3b8';
      ctx.fillText(role, x, by + 21);
    }

    drawSpeechBubble(ctx, x, y, text, bgColor = '#ffffff', textColor = '#1e293b', borderColor = '#475569') {
      ctx.font = 'bold 8.5px "Inter", sans-serif';
      const textWidth = ctx.measureText(text).width;
      const pad = 6;
      const w = textWidth + pad * 2;
      const h = 15;
      const bx = Math.round(x - w / 2);
      const by = Math.round(y - h);

      ctx.fillStyle = bgColor;
      ctx.fillRect(bx, by, w, h);
      ctx.strokeStyle = borderColor;
      ctx.lineWidth = 1;
      ctx.strokeRect(bx, by, w, h);

      // Pointer triangle
      ctx.beginPath();
      ctx.moveTo(x - 3, by + h);
      ctx.lineTo(x, by + h + 3);
      ctx.lineTo(x + 3, by + h);
      ctx.fillStyle = bgColor;
      ctx.fill();

      ctx.fillStyle = textColor;
      ctx.textAlign = 'center';
      ctx.fillText(text, x, by + 10);
    }
  }

  window.OfficeFloorEngine = OfficeFloorEngine;

})(window);
