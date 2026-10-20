"""Deterministic offline builder. SPDX-License-Identifier: GPL-3.0-only"""
import json, pathlib, collections
ROOT=pathlib.Path(__file__).resolve().parent

def render():
    spec=json.loads((ROOT/'rules.json').read_text())
    rules=spec['rules']
    assert rules and len({r['pattern'] for r in rules})==len(rules)
    hosts=sorted({r['hostname'] for r in rules})
    assert all('*' not in h for h in hosts)
    text='\n'.join([
      '#!name=开屏广告精简合集（闲鱼首版）',
      '#!desc=v'+spec['version']+'；仅闲鱼开屏专用接口；非全覆盖；待手机验证。GPL-3.0；来源奶思/fmz200。',
      '#!author=panjin9395；上游奶思/fmz200',
      '#!homepage=https://github.com/panjin9395/loon-splash-adblock',
      '#!date=2026-10-20',
      '# License: GPL-3.0-only; see LICENSE and NOTICE.md',
      '# Modified: keep only splash, narrow URL bounds, convert to Loon reject-dict.',
      '[Rewrite]',
      *[r['pattern']+' '+r['action'] for r in rules],
      '', '[Mitm]', 'hostname = '+', '.join(hosts), ''
    ])
    return text

def coverage():
    items=json.loads((ROOT/'candidates.json').read_text())
    counts=collections.Counter(x['status'] for x in items)
    lines=['# 候选覆盖矩阵','',f'候选 {len(items)} 项；这是原始候选标签数量，不是已核实App数量。移动联通电信保留合称，简称未自动展开。',
           '仅 included=true 表示本版本有规则，仍不代表手机有效。所有其他候选均不在插件内。',
           '',json.dumps(dict(counts),ensure_ascii=False),'',
           '|候选|类别|状态|iOS核验|来源/许可|手机|', '|---|---|---|---|---|---|']
    for x in items:
        lines.append('|'+ '|'.join([x['name'],'、'.join(x['categories']),x['status'],x['ios_status'],x['source_status']+'；'+x['license_status'],x['device_status']])+'|')
    return '\n'.join(lines)+'\n'

if __name__=='__main__':
    (ROOT/'splash-adblock.lpx').write_text(render())
    (ROOT/'coverage.md').write_text(coverage())
    print('构建完成：splash-adblock.lpx、coverage.md')
