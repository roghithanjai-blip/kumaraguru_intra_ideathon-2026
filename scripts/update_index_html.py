import json, re

with open('landing.html', 'r', encoding='utf-8') as f:
    html = f.read()

with open('scripts/mapped_domains.json', 'r', encoding='utf-8') as f:
    domains_statements = json.load(f)

# Define the 5 domains metadata matching the original landing page
domains_config = {
    'automotive': {
        'id': 'automotive',
        'name': 'Automotive',
        'icon': 'directions_car',
        'description': 'EV powertrains, battery thermal management, regenerative braking, vehicle telemetry, and micro-mobility platforms.',
        'department': 'Automotive Research Team'
    },
    'lifesciences': {
        'id': 'lifesciences',
        'name': 'Bioscience & Life Sciences',
        'icon': 'biotech',
        'description': 'Conservation genomics, microbial ecology, environmental metagenomics, wildlife forensics, and bioremediation.',
        'department': 'Ré Bioscience'
    },
    'software': {
        'id': 'software',
        'name': 'Education & Campus Technologies',
        'icon': 'school',
        'description': 'Classroom acoustics, assistive listening, laboratory electrical safety, PCB fault testing, and environmental sensing.',
        'department': 'Ré Research Cell & Faculty'
    },
    'energy': {
        'id': 'energy',
        'name': 'Renewable Energy',
        'icon': 'solar_power',
        'description': 'Solar PV end-of-life recovery, wind turbine composite recycling, wave energy, geothermal conversion, and industrial waste-heat capture.',
        'department': 'Ré Forum'
    },
    'designtextiles': {
        'id': 'designtextiles',
        'name': 'Textiles & Materials',
        'icon': 'architecture',
        'description': 'PFAS-free apparel finishes, non-piercing retail tags, mosquito-repellent textiles, handloom authentication, and green composites.',
        'department': 'Ré Research Cell & Faculty'
    }
}

assembled_domains = {}
for key in ['automotive', 'lifesciences', 'software', 'energy', 'designtextiles']:
    assembled_domains[key] = {
        'id': domains_config[key]['id'],
        'name': domains_config[key]['name'],
        'icon': domains_config[key]['icon'],
        'description': domains_config[key]['description'],
        'department': domains_config[key]['department'],
        'statements': domains_statements[key]
    }

domains_json = json.dumps(assembled_domains, indent=6, ensure_ascii=False)

# Build the replacement JavaScript block
js_replacement = f"""    const domainsData = {domains_json};
    // Domain aliases
    domainsData.education = domainsData.software;
    domainsData.textile = domainsData.designtextiles;
    domainsData.bioscience = domainsData.lifesciences;"""

# Locate exact start (line 1281) and end (line 2765)
start_m = re.search(r'\n\s*const domainsData\s*=\s*\{', html[80000:])
if not start_m:
    print("ERROR: Could not find domainsData start around line 1281")
    exit(1)
actual_start = 80000 + start_m.start() + 1

end_m = re.search(r'\n\s*// State variables', html[actual_start:])
if not end_m:
    print("ERROR: Could not find State variables marker after line 1281")
    exit(1)
actual_end = actual_start + end_m.start() + 1

new_html = html[:actual_start] + js_replacement + "\n\n" + html[actual_end:]

print(f"Original length: {len(html)}, New length: {len(new_html)}")

# Enhance renderStatementsList card markup to show draft/placeholder indicators cleanly
old_render_card = """        card.innerHTML = `
        <div class="p-3.5 sm:p-4 rounded-xl bg-surface hover:bg-primary-fixed/20 border border-outline-variant/30 hover:border-primary/50 transition-all duration-150 flex flex-col sm:flex-row sm:items-center justify-between gap-3 shadow-sm hover:shadow-md">
          <div class="flex items-start gap-3">
            <span class="px-2.5 py-1 rounded-md bg-primary text-on-primary font-mono text-xs font-bold tracking-wider shrink-0 mt-0.5">${ps.code}</span>
            <div class="flex flex-col">
              <span class="text-sm sm:text-base font-bold text-on-surface group-hover/item:text-primary transition-colors leading-snug">${ps.title}</span>
              <p class="text-xs text-on-surface-variant line-clamp-1 mt-1 leading-relaxed">${ps.preview || ''}</p>
              <div class="flex items-center gap-2 mt-2">
                <span class="text-[11px] font-medium text-on-surface-variant bg-surface-container-high px-2 py-0.5 rounded">${ps.category || ''}</span>
                <span class="text-[11px] font-medium text-slate-400">•</span>
                <span class="text-[11px] font-medium text-secondary">${ps.complexity || ''}</span>
              </div>
            </div>
          </div>
          <div class="flex items-center gap-1 text-primary text-xs font-bold shrink-0 self-end sm:self-center px-3 py-1.5 rounded-lg bg-primary/5 group-hover/item:bg-primary group-hover/item:text-white transition-all">
            <span>View Brief</span>
            <span class="material-symbols-outlined text-[16px] transform group-hover/item:translate-x-0.5 transition-transform">arrow_forward</span>
          </div>
        </div>
      `;"""

new_render_card = """        const statusBadge = ps.status === 'draft'
          ? `<span class="text-[10px] font-bold text-amber-800 bg-amber-100 px-2 py-0.5 rounded border border-amber-300">Draft</span>`
          : (ps.status === 'placeholder'
            ? `<span class="text-[10px] font-bold text-slate-700 bg-slate-200 px-2 py-0.5 rounded border border-slate-300">Awaiting Submission</span>`
            : '');

        card.innerHTML = `
        <div class="p-3.5 sm:p-4 rounded-xl bg-surface hover:bg-primary-fixed/20 border ${ps.status === 'placeholder' ? 'border-dashed border-slate-400' : 'border-outline-variant/30'} hover:border-primary/50 transition-all duration-150 flex flex-col sm:flex-row sm:items-center justify-between gap-3 shadow-sm hover:shadow-md">
          <div class="flex items-start gap-3">
            <span class="px-2.5 py-1 rounded-md bg-primary text-on-primary font-mono text-xs font-bold tracking-wider shrink-0 mt-0.5">${ps.code}</span>
            <div class="flex flex-col">
              <div class="flex items-center gap-2 flex-wrap">
                <span class="text-sm sm:text-base font-bold text-on-surface group-hover/item:text-primary transition-colors leading-snug">${ps.title}</span>
                ${statusBadge}
              </div>
              <p class="text-xs text-on-surface-variant line-clamp-1 mt-1 leading-relaxed">${ps.preview || ps.desc || ''}</p>
              <div class="flex items-center gap-2 mt-2 flex-wrap">
                <span class="text-[11px] font-medium text-on-surface-variant bg-surface-container-high px-2 py-0.5 rounded">${ps.category || ps.tag || ''}</span>
                <span class="text-[11px] font-medium text-slate-400">•</span>
                <span class="text-[11px] font-medium text-secondary">${ps.complexity || ps.tag || ''}</span>
              </div>
            </div>
          </div>
          <div class="flex items-center gap-1 text-primary text-xs font-bold shrink-0 self-end sm:self-center px-3 py-1.5 rounded-lg bg-primary/5 group-hover/item:bg-primary group-hover/item:text-white transition-all">
            <span>View Brief</span>
            <span class="material-symbols-outlined text-[16px] transform group-hover/item:translate-x-0.5 transition-transform">arrow_forward</span>
          </div>
        </div>
      `;"""

if old_render_card in new_html:
    new_html = new_html.replace(old_render_card, new_render_card, 1)
    print("Updated renderStatementsList card markup successfully!")
else:
    print("Warning: old_render_card not matched directly.")

# Update openDetailModal support text, requested_by, and badges
old_detail_code = """      if (reqByEl) reqByEl.innerHTML = `Requested by: <strong class=\"text-on-surface\">${currentDomain ? currentDomain.department : 'Ré Research Cell & Faculty'}</strong>`;
      if (descEl) descEl.textContent = ps.desc;
      if (pillEl) pillEl.textContent = currentDomain ? currentDomain.name : "Research Domain";
      if (supportEl) supportEl.textContent = ps.support || `Selected teams receive dedicated workstation access at KCT Centre of Excellence labs and mentor guidance.`;"""

new_detail_code = """      if (catBadge && ps.status === 'draft') {
        catBadge.textContent = `${ps.tag || ps.category} · Draft (Pending Confirmation)`;
      } else if (catBadge && ps.status === 'placeholder') {
        catBadge.textContent = `${ps.tag || 'Reserved'} · Awaiting Submission`;
      }
      if (reqByEl) reqByEl.innerHTML = `Requested by: <strong class=\"text-on-surface\">${ps.requested_by || (currentDomain ? currentDomain.department : 'Ré Research Cell & Faculty')}</strong>`;
      if (descEl) descEl.textContent = ps.desc;
      if (pillEl) pillEl.textContent = currentDomain ? currentDomain.name : "Research Domain";
      if (supportEl) {
        if (ps.branches && ps.branches.length > 0) {
          supportEl.textContent = `Suggested branches: ${ps.branches.join(', ')}`;
        } else if (ps.status === 'draft') {
          supportEl.textContent = 'Draft specification — pending confirmation with research circle.';
        } else if (ps.status === 'placeholder') {
          supportEl.textContent = 'Slot reserved awaiting submission.';
        } else {
          supportEl.textContent = ps.support || `Selected teams receive dedicated workstation access at KCT Centre of Excellence labs and mentor guidance.`;
        }
      }"""

if old_detail_code in new_html:
    new_html = new_html.replace(old_detail_code, new_detail_code, 1)
    print("Updated openDetailModal successfully!")
else:
    print("Warning: old_detail_code not matched directly.")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(new_html)

print("Saved updated index.html successfully!")
