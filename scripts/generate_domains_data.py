import json

with open('src/data/problems.json', 'r', encoding='utf-8') as f:
    problems = json.load(f)

# Group by domain
by_domain = {
    'automotive': [],
    'lifesciences': [],
    'software': [],
    'energy': [],
    'designtextiles': []
}

for p in problems:
    domain = p['domain']
    
    # Map domain to key
    key = None
    if domain == 'Automotive':
        key = 'automotive'
    elif domain == 'Bioscience':
        key = 'lifesciences'
    elif domain == 'Education':
        key = 'software'
    elif domain == 'Renewable Energy':
        key = 'energy'
    elif domain == 'Textile':
        key = 'designtextiles'
    
    tag = p.get('tag', '')
    tag_parts = [t.strip() for t in tag.split('·')]
    category = tag_parts[0] if len(tag_parts) > 0 else tag
    complexity = tag_parts[1] if len(tag_parts) > 1 else tag
    
    context = p.get('context', '')
    # Preview: first sentence or up to 130 chars
    first_sentence = context.split('. ')[0]
    if not first_sentence.endswith('.'):
        first_sentence += '.'
    preview = first_sentence if len(first_sentence) <= 150 else context[:130] + '…'
    
    entry = {
        'code': p['code'],
        'title': p['title'],
        'category': category,
        'complexity': complexity,
        'tag': tag,
        'preview': preview,
        'desc': context,
        'techScope': p.get('scope', []),
        'deliverables': p.get('deliverables', []),
        'status': p.get('status', 'final'),
        'requested_by': p.get('requested_by', '')
    }
    
    if p.get('branches'):
        entry['branches'] = p['branches']
    if p.get('source_ref'):
        entry['source_ref'] = p['source_ref']
        
    by_domain[key].append(entry)

print("Mapped problem statements per domain key:")
for k, v in by_domain.items():
    print(f"  {k}: {len(v)} statements (first: {v[0]['code']}, last: {v[-1]['code']})")

with open('scripts/mapped_domains.json', 'w', encoding='utf-8') as f:
    json.dump(by_domain, f, indent=2, ensure_ascii=False)
