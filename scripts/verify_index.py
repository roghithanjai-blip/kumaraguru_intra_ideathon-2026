import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

print('Total lines in index.html:', len(content.splitlines()))

# Let's count problem statements per domain in domainsData
pos = content.rfind('const domainsData = {')
js_block = content[pos:pos+150000]

domains = ['automotive', 'lifesciences', 'software', 'energy', 'designtextiles']
for d in domains:
    d_pos = js_block.find(f'"{d}":')
    if d_pos != -1:
        # find statements array
        st_pos = js_block.find('"statements":', d_pos)
        # find codes in this block up to next domain or end
        # find next domain pos
        next_poses = [js_block.find(f'"{nd}":', d_pos + 10) for nd in domains if js_block.find(f'"{nd}":', d_pos + 10) != -1]
        end_pos = min(next_poses) if next_poses else js_block.find('domainsData.education')
        d_sub = js_block[d_pos:end_pos]
        codes = re.findall(r'"code":\s*"([^"]+)"', d_sub)
        titles = re.findall(r'"title":\s*"([^"]+)"', d_sub)
        print(f"Domain: {d:<16} Count: {len(codes)} | First: {codes[0]} ('{titles[0]}') | Last: {codes[-1]} ('{titles[-1]}')")

all_codes = re.findall(r'"code":\s*"(KII26\d+)"', js_block)
print(f"\nTotal problem statement codes in domainsData: {len(all_codes)}")
print(f"Are all 75 codes unique? {len(set(all_codes)) == 75}")

# Check venue and date mentions in HTML
print("\n--- Checking Venue & Date mentions in index.html ---")
venue_matches = [line.strip() for line in content.splitlines() if 'venue' in line.lower()]
for line in venue_matches[:5]:
    print("Venue line:", line)

# Find modal sections
print("\n--- Modal elements in index.html ---")
lines = content.splitlines()
for i, l in enumerate(lines):
    if any(m in l for m in ['id="circles-modal', 'id="circle-list-view', 'id="circle-detail-view', 'id="modal-statement-list']):
        print(f"Line {i+1}: {l.strip()[:100]}")


