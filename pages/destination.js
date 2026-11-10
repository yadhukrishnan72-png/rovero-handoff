// Rovero destination page (countries and regions). Reads window.ROVERO_PAGE (see ../data/pages/*.js and the README).
//
// Plan fields: gb, days, price; coverage (key into ROVERO_PAGE.coverage: the countries this plan works in; regions only);
// optional: voice + sms (Data + Voice), perDay (Unlimited allowance), tag (e.g. 'Most popular'), local: true (lightning badge).
// The page logic never checks sizes or names: tabs, tiles, notices and the country sheet are all driven by this data.
//
// Developer hooks (CustomEvents on document):
//   'rovero:select'  detail = { kind, plan }            fired when the selected plan changes
//   'rovero:pay'     detail = { kind, plan, page }      fired when "Pay now" is pressed
(function () {
  const P = window.ROVERO_PAGE;
  if (!P) return;
  const $ = (id) => document.getElementById(id);
  const usd = (n) => `$${n.toFixed(2)}`;
  const PLANS = P.plans || {};
  const COVERAGE = P.coverage || {};
  const isRegion = P.kind === 'region';

  // ---- 1. text tokens and kind-specific blocks --------------------------------------------------------------
  const tokens = { name: P.name, the: P.the || P.name };
  const sub = (s) => s.replace(/\{(\w+)\}/g, (m, k) => (k in tokens ? tokens[k] : m));
  document.title = sub(document.title);
  document.querySelectorAll('meta[name="description"]').forEach((m) => m.setAttribute('content', sub(m.getAttribute('content'))));
  const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
  for (let n = walker.nextNode(); n; n = walker.nextNode()) {
    if (n.nodeValue.includes('{')) n.nodeValue = sub(n.nodeValue);
  }
  document.querySelectorAll('[data-for]').forEach((el) => { el.hidden = el.dataset.for !== P.kind; });

  // ---- 2. hero image, networks, related destinations --------------------------------------------------------
  const hero = $('hero-img');
  hero.src = P.image;
  hero.alt = P.alt || '';

  if (!isRegion && (P.networks || []).length) {
    $('nets').hidden = false;
    $('nets-list').replaceChildren(...P.networks.map((n) => {
      const li = document.createElement('li');
      li.append(n.name + ' ');
      if (n.tech) {
        const s = document.createElement('span');
        s.textContent = n.tech;
        li.append(s);
      }
      return li;
    }));
  }

  const GLOBE = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c2.5 2.6 3.8 5.6 3.8 9S14.5 18.4 12 21c-2.5-2.6-3.8-5.6-3.8-9S9.5 5.6 12 3z"/></svg>';
  if ((P.related || []).length) {
    $('related').hidden = false;
    $('related-title').textContent = P.relatedTitle || 'Explore more eSIM plans';
    $('related-text').textContent = P.relatedText || 'Travelling to several places? Browse more destinations and keep using the same rovero eSIM.';
    $('related-list').replaceChildren(...P.related.map((r) => {
      const li = document.createElement('li');
      const a = document.createElement('a');
      a.href = r.href || '#';
      const ic = document.createElement('span');
      ic.className = 'chip__icon';
      ic.setAttribute('aria-hidden', 'true');
      if (r.image) {
        const img = document.createElement('img');
        img.src = r.image;
        img.alt = '';
        img.width = img.height = 32;
        ic.append(img);
      } else {
        ic.innerHTML = GLOBE;
      }
      a.append(ic, r.label);
      li.append(a);
      return li;
    }));
  }

  // ---- 3. plan picker ---------------------------------------------------------------------------------------
  const list = $('plan-list');
  const tabsEl = $('tabs');
  const localNote = $('local-note');
  const unlNote = $('unl-note');
  if (P.unlimitedNote) {
    const t = $('unl-text');
    const s = document.createElement('strong');
    s.textContent = P.unlimitedNote.strong || '';
    t.append(s, P.unlimitedNote.text || '');
  }
  const out = { plan: $('o-plan'), price: $('o-price') };
  const BOLT = '<svg viewBox="0 0 36 36" aria-hidden="true"><rect width="36" height="36" rx="8" fill="#FFF4D9"/><path d="M19 10 18 16h7v2l-8 8.5h-1V20H9v-1z" fill="#F0B100" stroke="#F0B100" stroke-width=".8" stroke-linejoin="round"/></svg>';
  const TAB_LABELS = { data: 'Data', voice: 'Data + Voice', unlimited: 'Unlimited' };

  const names = (id) => [...(COVERAGE[id] || [])].sort((a, b) => a.localeCompare(b));
  const count = (p) => (COVERAGE[p.coverage] || []).length;
  const label = (p) => `${p.gb}${p.voice ? ` + ${p.voice}` : ''}${p.sms ? ` + ${p.sms}` : ''}`;
  const plural = (n) => `${n} ${n === 1 ? 'country' : 'countries'}`;
  const kinds = Object.keys(PLANS).filter((k) => (PLANS[k] || []).length);
  let kind = kinds[0];
  let selected = 0;
  let sheetPlan = 0;

  function fill(ul, emptyEl, all, query) {
    const q = query.trim().toLowerCase();
    const shown = q ? all.filter((n) => n.toLowerCase().includes(q)) : all;
    ul.replaceChildren(...shown.map((n) => {
      const li = document.createElement('li');
      li.textContent = n;
      return li;
    }));
    emptyEl.hidden = shown.length > 0;
  }

  function summarise() {
    const p = PLANS[kind][selected];
    out.plan.textContent = `${label(p)} · ${p.days} days`;
    out.price.textContent = usd(p.price);
    document.dispatchEvent(new CustomEvent('rovero:select', { detail: { kind, plan: p } }));
  }

  function select(i) {
    selected = i;
    [...list.children].forEach((el, n) => {
      el.classList.toggle('is-on', n === i);
      el.querySelector('.plan__pick').setAttribute('aria-checked', String(n === i));
    });
    summarise();
  }

  function render() {
    const recommended = PLANS[kind].findIndex((p) => p.tag);
    selected = recommended >= 0 ? recommended : 0;
    localNote.hidden = !PLANS[kind].some((p) => p.local);
    unlNote.hidden = !(kind === 'unlimited' && P.unlimitedNote);

    list.replaceChildren(...PLANS[kind].map((p, i) => {
      const el = document.createElement('div');
      el.className = 'plan' + (p.voice ? ' plan--voice' : '');
      el.setAttribute('role', 'presentation');
      // The overlay button (.plan__pick) carries the radio role; the countries link sits above it
      el.innerHTML = `
        <button type="button" class="plan__pick" role="radio"></button>
        <span class="plan__dot" aria-hidden="true"></span>
        <span class="plan__data" aria-hidden="true"></span>
        ${p.voice || p.perDay ? '<span class="plan__voice" aria-hidden="true"></span>' : ''}
        <span class="plan__meta" aria-hidden="true"></span>
        ${isRegion && p.coverage ? '<button type="button" class="plan__countries"></button>' : ''}
        <span class="plan__price" aria-hidden="true"></span>`;

      const data = el.querySelector('.plan__data');
      data.textContent = p.gb;
      if (!/^\d/.test(p.gb)) data.classList.add('plan__data--word');

      const extra = el.querySelector('.plan__voice');
      if (p.voice) {
        for (const t of [`+ ${p.voice}`, `+ ${p.sms}`]) {
          const s = document.createElement('span');
          s.textContent = t;
          extra.append(s, ' ');
        }
      } else if (p.perDay) {
        extra.textContent = p.perDay;
      }

      el.querySelector('.plan__meta').textContent = `${p.days} days`;
      el.querySelector('.plan__price').textContent = usd(p.price);
      el.querySelector('.plan__pick').setAttribute(
        'aria-label',
        `${label(p)}, ${p.days} days, ${usd(p.price)}${isRegion && p.coverage ? `, ${plural(count(p))}` : ''}`);

      const link = el.querySelector('.plan__countries');
      if (link) {
        link.textContent = `${plural(count(p))} ›`;
        link.setAttribute('aria-label', `View the ${plural(count(p))} included in the ${label(p)} plan`);
        link.addEventListener('click', () => openSheet(i));
      }
      if (p.local) {
        const b = document.createElement('span');
        b.className = 'plan__local';
        b.setAttribute('role', 'img');
        b.setAttribute('aria-label', 'Local plan');
        b.innerHTML = BOLT;
        el.append(b);
      }
      if (p.tag) {
        const t = document.createElement('span');
        t.className = 'plan__tag';
        t.textContent = p.tag;
        el.append(t);
      }
      el.querySelector('.plan__pick').addEventListener('click', () => select(i));
      return el;
    }));
    select(selected);
  }

  list.addEventListener('keydown', (e) => {
    if (!e.target.classList.contains('plan__pick')) return;
    const n = PLANS[kind].length;
    const step = { ArrowDown: 1, ArrowRight: 1, ArrowUp: -1, ArrowLeft: -1 }[e.key];
    if (!step) return;
    e.preventDefault();
    select((selected + step + n) % n);
    list.children[selected].querySelector('.plan__pick').focus();
  });

  // Tabs appear only when there is more than one kind of plan
  if (kinds.length > 1) {
    tabsEl.replaceChildren(...kinds.map((k) => {
      const b = document.createElement('button');
      b.className = 'tabs__btn';
      b.type = 'button';
      b.setAttribute('role', 'tab');
      b.setAttribute('aria-selected', String(k === kind));
      b.dataset.kind = k;
      b.textContent = TAB_LABELS[k];
      b.addEventListener('click', () => {
        kind = k;
        [...tabsEl.children].forEach((t) => t.setAttribute('aria-selected', String(t === b)));
        render();
      });
      return b;
    }));
  } else {
    tabsEl.hidden = true;
  }

  // ---- 4. countries sheet (regions) -------------------------------------------------------------------------
  const dlg = {
    el: $('cty-dlg'), sub: $('dlg-sub'), list: $('dlg-list'), search: $('dlg-search'),
    empty: $('dlg-empty'), pick: $('dlg-pick'), close: $('dlg-close'), title: $('dlg-title'),
  };
  function renderSheet() {
    const p = PLANS[kind][sheetPlan];
    dlg.title.textContent = `Countries in the ${label(p)} plan`;
    dlg.sub.textContent = `${plural(count(p))} · ${p.days} days`;
    dlg.pick.textContent = sheetPlan === selected ? 'Done' : 'Choose this plan';
    fill(dlg.list, dlg.empty, names(p.coverage), dlg.search.value);
  }
  function openSheet(i) {
    sheetPlan = i;
    dlg.search.value = '';
    renderSheet();
    dlg.el.showModal();
    dlg.list.scrollTop = 0;
  }
  dlg.search.addEventListener('input', renderSheet);
  dlg.close.addEventListener('click', () => dlg.el.close());
  dlg.pick.addEventListener('click', () => { select(sheetPlan); dlg.el.close(); });
  dlg.el.addEventListener('click', (e) => { if (e.target === dlg.el) dlg.el.close(); });

  $('pay').addEventListener('click', () => {
    document.dispatchEvent(new CustomEvent('rovero:pay', { detail: { kind, plan: PLANS[kind][selected], page: P.code } }));
  });

  if (kinds.length) render();
  document.documentElement.classList.add('ready');
})();
