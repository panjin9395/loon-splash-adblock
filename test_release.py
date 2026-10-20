"""Offline checks, NOT a Loon emulator or real-device test. GPL-3.0-only."""
import collections, hashlib, json, pathlib, re, unittest
from build import render,coverage
ROOT=pathlib.Path(__file__).resolve().parent
BASE='https://acs.m.goofish.com/gw/mtop.taobao.idlecommerce.splash.ads/'
POS=[BASE+'2.0/',BASE+'1.0/',BASE+'2.0/?test=1',BASE+'2.0/?',BASE+'12.34/?a=b&c=d']
NEG=[BASE,BASE+'2.0',BASE+'2.0/extra',BASE+'2.0/#fragment',BASE+'2.0/?a=1\nnext',BASE+'2.0evil/',BASE+'v2/',BASE+'2.0/extra?x=1',BASE+'2.0/?x=1#fragment',BASE.replace('https:','http:')+'2.0/',BASE.replace('acs.m.goofish.com','g-acs.m.goofish.com')+'2.0/',BASE.replace('acs.m.goofish.com','acs.m.goofish.com.attacker.invalid')+'2.0/',BASE.replace('acs.m.goofish.com','acs.m.goofish.com@attacker.invalid')+'2.0/',BASE.replace('splash.ads','splash.async.ads')+'1.0/',BASE.replace('splash.ads','splash.ads.extra')+'2.0/']
for api in ['mtop.taobao.idle.trade.full.info','mtop.taobao.idlehome.home.nextfresh','mtop.taobao.idle.item.recommend.list','mtop.taobao.idle.login','mtop.taobao.idle.pay','mtop.taobao.idle.signin']:
    NEG.append('https://acs.m.goofish.com/gw/'+api+'/1.0/')
NEG+=['https://example.invalid/?redirect='+BASE+'2.0/','https://acsXmXgoofishXcom/gw/mtop.taobao.idlecommerce.splash.ads/2.0/']
ALLOWED={'LICENSE','NOTICE.md','README.md','CHANGELOG.md','rules.json','candidates.json','candidate-groups.json','sources.json','build.py','test_release.py','splash-adblock.lpx','coverage.md','tests-report.json','.gitignore'}
class ReleaseTests(unittest.TestCase):
    def test_build_deterministic(self):
        self.assertEqual(render(),render())
        self.assertEqual(render(),(ROOT/'splash-adblock.lpx').read_text())
        self.assertEqual(coverage(),(ROOT/'coverage.md').read_text())
    def test_candidates_complete(self):
        groups=json.loads((ROOT/'candidate-groups.json').read_text())
        expected=set(n for s in groups.values() for n in s.split('/'))
        items=json.loads((ROOT/'candidates.json').read_text())
        self.assertEqual(set(x['name'] for x in items),expected)
        self.assertEqual(len(items),len(expected))
        self.assertEqual(len(items),285)
        self.assertEqual([x['name'] for x in items if x['included']],['闲鱼'])
        for x in items:
            self.assertTrue(all(x[k] for k in ['status','ios_status','source_status','license_status','device_status']))
    def test_regex_cases(self):
        pat=json.loads((ROOT/'rules.json').read_text())['rules'][0]['pattern']
        compiled=re.compile(pat)
        for url in POS:
            with self.subTest(positive=url): self.assertIsNotNone(compiled.search(url))
        for url in NEG:
            with self.subTest(negative=url): self.assertIsNone(compiled.search(url))
    def test_sections_and_no_dependencies(self):
        t=render()
        self.assertEqual(re.findall(r'^\[([^]]+)\]$',t,re.M),['Rewrite','Mitm'])
        lines=[l for l in t.splitlines() if l.startswith('^')]
        self.assertEqual(len(lines),1)
        pat,action=lines[0].split(' ')
        self.assertEqual(action,'reject-dict')
        self.assertEqual(pat,json.loads((ROOT/'rules.json').read_text())['rules'][0]['pattern'])
        self.assertEqual(re.findall(r'^hostname = (.+)$',t,re.M),['acs.m.goofish.com'])
        self.assertNotIn('*',re.findall(r'^hostname = (.+)$',t,re.M)[0])
        for term in ['script-path','jq-path','data-path','[General]','[Host]','[Script]','[Rule]']:
            self.assertNotIn(term,t)
        self.assertEqual(json.loads((ROOT/'sources.json').read_text())['runtime_dependencies'],[])
    def test_license_and_source(self):
        source=json.loads((ROOT/'sources.json').read_text())['sources'][0]
        self.assertEqual(hashlib.sha256((ROOT/'LICENSE').read_bytes()).hexdigest(),source['license_sha256'])
        self.assertIn('GNU GENERAL PUBLIC LICENSE',(ROOT/'LICENSE').read_text())
        self.assertIn(source['revision'],(ROOT/'NOTICE.md').read_text())
    def test_public_allowlist_and_secret_patterns(self):
        for p in ROOT.iterdir():
            if p.name in ('.git','__pycache__'): continue
            self.assertTrue(p.is_file() and p.name in ALLOWED,p.name)
            if p.name=='test_release.py':continue
            text=p.read_text()
            for pattern in [r'-----BEGIN [A-Z ]*PRIVATE KEY',r'(?i)ca-p12\s*=',r'(?i)ca-passphrase\s*=',r'gh[pousr]_[A-Za-z0-9]{30,}',r'(?i)(?:password|token|secret|authorization)\s*[=:]\s*["\x27]?[A-Za-z0-9_+/=-]{20,}',r'https?://[^\s/]+:[^\s/]+@',r'012357\.top',r'192\.168\.',r'CCZX_WiFi']:
                self.assertIsNone(re.search(pattern,text),p.name+' potential secret')

if __name__=='__main__':
    suite=unittest.defaultTestLoader.loadTestsFromTestCase(ReleaseTests)
    result=unittest.TextTestRunner(verbosity=2).run(suite)
    candidates=json.loads((ROOT/'candidates.json').read_text())
    report={'success':result.wasSuccessful(),'tests_run':result.testsRun,'failures':len(result.failures),'errors':len(result.errors),'positive_url_cases':len(POS),'negative_url_cases':len(NEG),'candidate_count':len(candidates),'included_count':sum(x['included'] for x in candidates),'status_counts':dict(collections.Counter(x['status'] for x in candidates)),'plugin_sha256':hashlib.sha256((ROOT/'splash-adblock.lpx').read_bytes()).hexdigest(),'script_fixture':'不适用：无脚本；URL为人工边界测试样例，非抓包','native_loon_parser':'未验证','real_device':'未验证','privacy':'发布白名单和敏感模式扫描；私密原配置未包含在仓库'}
    (ROOT/'tests-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(report,ensure_ascii=False))
    raise SystemExit(not result.wasSuccessful())
