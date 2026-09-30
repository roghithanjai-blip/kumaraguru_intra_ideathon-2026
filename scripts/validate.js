import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const problemsPath = path.resolve(__dirname, '../src/data/problems.json');

console.log('--- Validating problems.json ---');

if (!fs.existsSync(problemsPath)) {
  console.error(`ERROR: File not found: ${problemsPath}`);
  process.exit(1);
}

const raw = fs.readFileSync(problemsPath, 'utf-8');
let problems;
try {
  problems = JSON.parse(raw);
} catch (err) {
  console.error('ERROR: Invalid JSON:', err.message);
  process.exit(1);
}

if (!Array.isArray(problems)) {
  console.error('ERROR: Root element in problems.json must be an array');
  process.exit(1);
}

const EXPECTED_DOMAINS = ['Automotive', 'Bioscience', 'Education', 'Renewable Energy', 'Textile'];
const REQUIRED_FIELDS = ['code', 'domain', 'tag', 'title', 'requested_by', 'context', 'scope', 'deliverables'];

let hasError = false;
const seenCodes = new Set();
const domainCounts = {};

EXPECTED_DOMAINS.forEach((d) => (domainCounts[d] = 0));

problems.forEach((p, idx) => {
  const identifier = p.code || `Index ${idx}`;

  // Check required fields
  for (const field of REQUIRED_FIELDS) {
    if (p[field] === undefined || p[field] === null || p[field] === '') {
      console.error(`ERROR [${identifier}]: Missing or empty required field '${field}'`);
      hasError = true;
    }
  }

  // Check scope and deliverables arrays
  if (!Array.isArray(p.scope) || p.scope.length === 0) {
    console.error(`ERROR [${identifier}]: 'scope' must be a non-empty array`);
    hasError = true;
  }
  if (!Array.isArray(p.deliverables) || p.deliverables.length === 0) {
    console.error(`ERROR [${identifier}]: 'deliverables' must be a non-empty array`);
    hasError = true;
  }

  // Check duplicate codes
  if (p.code) {
    if (seenCodes.has(p.code)) {
      console.error(`ERROR: Duplicate problem statement code '${p.code}' found!`);
      hasError = true;
    }
    seenCodes.add(p.code);
  }

  // Check valid domain
  if (!EXPECTED_DOMAINS.includes(p.domain)) {
    console.error(`ERROR [${identifier}]: Unknown domain '${p.domain}'`);
    hasError = true;
  } else {
    domainCounts[p.domain] = (domainCounts[p.domain] || 0) + 1;
  }

  // Check status if present
  if (p.status && !['final', 'draft', 'placeholder'].includes(p.status)) {
    console.error(`ERROR [${identifier}]: Invalid status '${p.status}'`);
    hasError = true;
  }
});

console.log('\n--- Domain Problem Counts ---');
for (const domain of EXPECTED_DOMAINS) {
  const count = domainCounts[domain] || 0;
  console.log(`  ${domain.padEnd(18)}: ${count} / 15`);
  if (count !== 15) {
    console.error(`ERROR: Domain '${domain}' has ${count} records (expected exactly 15)!`);
    hasError = true;
  }
}

console.log(`Total Problems Checked: ${problems.length} (Expected: 75)`);
if (problems.length !== 75) {
  console.error(`ERROR: Expected total 75 problems, but found ${problems.length}!`);
  hasError = true;
}

if (hasError) {
  console.error('\n❌ VALIDATION FAILED!');
  process.exit(1);
} else {
  console.log('\n✅ VALIDATION PASSED: All 75 problems verified across 5 domains with zero errors!');
  process.exit(0);
}
