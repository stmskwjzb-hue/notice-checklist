"""Forward execution from supplied inputs and public skill format only."""
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent
INPUT = ROOT.parent / 'forward-inputs.json'
CHECKER = Path(r'E:\Codex_Research\2026-10-28\openai-oss-skill\outputs\notice-checklist\skills\notice-checklist\scripts\check_result.py')
PYTHON = r'C:\Users\viets\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe'
CASES = {case['id']: case for case in json.loads(INPUT.read_text(encoding='utf-8-sig'))}
RESULTS = {}
ZONE = '通知未注明时区；所列钟点应按哪个时区理解？确认前不生成带偏移的标准时间。'


def fact(case_id, number, text, quote=None):
    return {'text': text, 'evidence': [{'source_id': CASES[case_id]['sources'][number - 1]['id'], 'location': '用户提供文本（唯一段落）', 'quote': quote or text}]}


def both(case_id, text, quote1, quote2):
    result = fact(case_id, 1, text, quote1)
    result['evidence'] += fact(case_id, 2, text, quote2)['evidence']
    return result


def due(value, iso=None):
    return {**value, 'iso': iso}


def task(action, *, status='active', deadline=None, materials=None, prerequisites=None, submission=None, changes=None, questions=None):
    return {'id': '', 'action': action, 'status': status, 'deadline': deadline, 'materials': materials or [], 'prerequisites': prerequisites or [], 'submission': submission, 'changes': changes or [], 'questions': questions or []}


def save(case_id, tasks, questions=None):
    for number, item in enumerate(tasks, 1):
        item['id'] = f'{case_id}-T{number}'
    RESULTS[case_id] = {'schema_version': 1, 'tasks': tasks, 'questions': questions or []}


c = 'C01'
save(c, [task(
    fact(c, 1, '申请助学金：提交申请材料', '申请助学金的同学'),
    status='needs_confirmation',
    deadline=due(fact(c, 2, '现行截止：2026年11月3日17:00；时区未注明', '截止时间改为2026年11月3日17:00')),
    materials=[fact(c, 1, name) for name in ['申请表', '身份证复印件', '成绩单']],
    submission=fact(c, 1, '发送至 aid@example.org', '发送至本通知写明的收件邮箱：aid@example.org'),
    changes=[both(c, '截止由2026年11月1日17:00延至2026年11月3日17:00；材料和收件邮箱保留', '2026年11月1日17:00前，将申请表、身份证复印件、成绩单发送至本通知写明的收件邮箱：aid@example.org', '截止时间改为2026年11月3日17:00，其余要求不变。')],
    questions=[ZONE]
)])

c = 'C02'
save(c, [task(
    fact(c, 1, '需续办门禁卡的员工：办理门禁卡续办', '需续办门禁卡的员工'),
    status='needs_confirmation', deadline=due(fact(c, 1, '续办截止：2026年11月4日17:00前；时区未注明', '2026年11月4日17:00前')),
    materials=[fact(c, 1, '续办表')],
    submission=fact(c, 1, '将续办表交到行政前台', '把续办表交到行政前台'),
    changes=[fact(c, 2, '续办安排维持原通知', '门禁卡续办安排不变。')], questions=[ZONE]
), task(
    fact(c, 1, '已取消的证件照拍摄：原活动时间为2026年11月2日15:00，地点为一楼（活动时间，非提交截止）', '2026年11月2日15:00到一楼拍证件照'),
    status='cancelled', materials=[fact(c, 1, '原需携带工牌；随该活动取消，无须为该活动准备', '携带工牌')],
    changes=[fact(c, 2, '11月2日的证件照拍摄取消', '11月2日的证件照拍摄取消。')]
)])

c = 'C03'
save(c, [task(
    both(c, '提交验收材料；截止日期存在冲突', '验收材料请于2026年11月5日17:00前上传到项目资料库', '验收材料请于2026年11月6日17:00前上传到项目资料库'),
    status='needs_confirmation',
    deadline=due(both(c, '甲：2026年11月5日17:00；乙：2026年11月6日17:00；未确定哪条生效', '2026年11月5日17:00前', '2026年11月6日17:00前')),
    materials=[both(c, '盖章验收表', '盖章验收表', '盖章验收表')],
    submission=both(c, '上传到项目资料库', '上传到项目资料库', '上传到项目资料库'),
    questions=['请项目组确认有效截止为11月5日还是11月6日；两条均无明确更正关系。', ZONE]
)])

c = 'C04'
save(c, [task(
    fact(c, 1, '参加研学活动的同学：交回执', '请参加研学活动的同学在本周五18:00前，将家长签字的回执交给班主任。'),
    status='needs_confirmation', deadline=due(fact(c, 1, '本周五18:00前；原消息日期未提供，不能确定年月日', '本周五18:00前')),
    materials=[fact(c, 1, '家长签字的回执')],
    prerequisites=[fact(c, 1, '回执须经家长签字', '家长签字的回执')],
    submission=fact(c, 1, '交给班主任', '交给班主任'),
    questions=['请确认原消息发送日期或明确截止年月日；不能用本次整理日期代替截图的日期。', ZONE]
)], ['仅收到截图转写，未收到原图；原时间被裁掉，无法检查截图日期和转写准确性。'])

c = 'C05'
save(c, [task(
    fact(c, 1, '实习报名：发送个人简历', '报名同学请把个人简历发到intern@example.org'),
    status='needs_confirmation', deadline=due(fact(c, 1, '11月2日17:00截止；年份未标明', '11月2日17:00截止')),
    materials=[fact(c, 1, '个人简历')], submission=fact(c, 1, '发到 intern@example.org', '发到intern@example.org'),
    questions=['请确认活动年份及该旧海报是否仍有效。', ZONE]
)])

c = 'C06'
save(c, [task(
    both(c, '全班同学填写班级信息表；逐字转发合并为一项', '全班同学在2026年10月30日20:00前填写班级信息表', '全班同学在2026年10月30日20:00前填写班级信息表'),
    status='needs_confirmation', deadline=due(both(c, '2026年10月30日20:00前；时区未注明', '2026年10月30日20:00前', '2026年10月30日20:00前')),
    materials=[both(c, '班级信息表', '班级信息表', '班级信息表')],
    submission=both(c, '班级群置顶的在线表单', '提交入口为班级群置顶的在线表单', '提交入口为班级群置顶的在线表单'), questions=[ZONE]
)])

c = 'C07'
save(c, [task(
    fact(c, 1, '用户（2026级研究生）：提交安全承诺书', '2026级本科生及研究生均须在2026年11月3日17:00前提交安全承诺书到各自辅导员处。'),
    status='needs_confirmation', deadline=due(fact(c, 1, '研究生仍为2026年11月3日17:00前；时区未注明', '2026年11月3日17:00前')),
    materials=[fact(c, 1, '安全承诺书')], submission=fact(c, 1, '交到本人辅导员处', '到各自辅导员处'),
    changes=[fact(c, 2, '本科生延期不适用于研究生', '仅2026级本科生截止时间延至2026年11月5日17:00，研究生安排不变。')], questions=[ZONE]
), task(
    fact(c, 1, '室友若为2026级本科生：提交安全承诺书', '2026级本科生及研究生均须在2026年11月3日17:00前提交安全承诺书到各自辅导员处。'),
    status='needs_confirmation', deadline=due(fact(c, 2, '仅2026级本科生延至2026年11月5日17:00；时区未注明', '仅2026级本科生截止时间延至2026年11月5日17:00')),
    materials=[fact(c, 1, '安全承诺书')], submission=fact(c, 1, '交到室友本人辅导员处', '到各自辅导员处'),
    prerequisites=[fact(c, 2, '该延期仅适用于2026级本科生', '仅2026级本科生')],
    changes=[both(c, '2026级本科生截止由11月3日17:00延至11月5日17:00；材料、接收人保留', '2026年11月3日17:00前提交安全承诺书到各自辅导员处。', '仅2026级本科生截止时间延至2026年11月5日17:00')],
    questions=['请确认室友是否为2026级本科生；通知未给出其他年级本科生的安排。', ZONE]
)])

c = 'C08'
save(c, [task(
    fact(c, 1, '第1步：到社区前台填写报名表', '有意参加的居民须在2026年11月3日18:00前，到社区前台填写报名表。'),
    status='needs_confirmation', deadline=due(fact(c, 1, '报名截止：2026年11月3日18:00前；时区未注明', '2026年11月3日18:00前')),
    materials=[fact(c, 1, '报名表')], submission=fact(c, 1, '社区前台现场填写报名表', '到社区前台填写报名表'), questions=[ZONE]
), task(
    fact(c, 1, '第2步：2026年11月8日14:00在社区二楼参加急救讲座（活动时间，非报名截止）', '急救讲座于2026年11月8日14:00在社区二楼举行。'),
    materials=[fact(c, 1, '携带报名回执', '参加时请携带报名回执。')],
    prerequisites=[fact(c, 1, '先完成报名', '有意参加的居民须在2026年11月3日18:00前，到社区前台填写报名表。')],
    questions=['讲座钟点未注明时区；请与报名时间一并确认。']
)])

c = 'C09'
save(c, [task(
    fact(c, 1, '必做：新入组成员于2026年11月4日09:00到实验楼301参加安全培训（活动时间，非提交截止）。可选准备：提前十分钟到场、自愿携带笔记本。不要求提交培训心得。', '2026年11月4日09:00，新入组成员须到实验楼301参加安全培训，必须携带校园卡。建议提前十分钟到场，可自愿携带笔记本；不要求提交培训心得。'),
    materials=[fact(c, 1, '必须携带校园卡', '必须携带校园卡')],
    prerequisites=[fact(c, 1, '通知要求适用对象：新入组成员', '新入组成员须到实验楼301参加安全培训')],
    questions=['活动钟点未注明时区；需要日历化时请先确认。']
)])

c = 'C10'
save(c, [task(
    both(c, '季度复盘会安排待确认；两份文件地点均为会议室A', '季度复盘会：2026年11月6日10:00，会议室A。', '季度复盘会：2026年11月7日10:00，会议室A。'),
    status='needs_confirmation',
    questions=['活动时间冲突：C10-S1为2026年11月6日10:00，C10-S2为2026年11月7日10:00。请运营协调组确认哪份生效；文件名和上传顺序不能确定效力。', '以上均为活动时间，不是提交截止；钟点时区也未注明。']
)])

c = 'C11'
save(c, [task(
    fact(c, 1, '完成校园摄影赛报名；附件信息缺失', '校园摄影赛报名请在2026年11月10日17:00前完成。'),
    status='needs_confirmation', deadline=due(fact(c, 1, '2026年11月10日17:00前；时区未注明', '2026年11月10日17:00前')),
    questions=['正文说明材料、报名入口、文件格式见附件；附件不可读，这三项均待确认，不能补造材料或入口。', ZONE]
)], ['C11-S2《附件：报名说明.pdf（扫描模糊，当前无法辨认）》为空文本、无法辨认。请提供可读附件或逐字文字；所需材料、报名入口、文件格式均缺失。'])

c = 'C12'
save(c, [task(
    fact(c, 1, '志愿者：提交纸质报名表', '志愿者请于2026年11月2日18:00前，在社团服务台交纸质报名表。'),
    status='needs_confirmation', deadline=due(fact(c, 1, '2026年11月2日18:00前；时区未注明', '2026年11月2日18:00前')),
    materials=[fact(c, 1, '纸质报名表')], submission=fact(c, 1, '交到社团服务台', '在社团服务台交纸质报名表'), questions=[ZONE]
)])

c = 'C13'
save(c, [task(
    fact(c, 1, '申请课程替代：提交申请材料', '申请课程替代的同学须在2026年11月6日17:00前提交课程替代申请表及原课程成绩单。'),
    status='needs_confirmation', deadline=due(fact(c, 1, '2026年11月6日17:00前；时区未注明', '2026年11月6日17:00前')),
    materials=[fact(c, 1, '课程替代申请表'), fact(c, 1, '原课程成绩单')],
    questions=['通知没有说明接收人、提交地点或线上入口；请教务确认提交方式及纸质/电子要求。', ZONE]
)])

c = 'C14'
save(c, [task(
    fact(c, 1, '读书会是否恢复举办待确认；原活动为2026年11月2日19:00（活动时间，非提交截止）', '读书会于2026年11月2日19:00在活动室A举行'),
    status='needs_confirmation',
    materials=[fact(c, 1, '若确认恢复，原通知要求参加者带一本书', '参加者带一本书')],
    changes=[fact(c, 2, '10月27日明确取消，要求不用到场', '原定11月2日的读书会取消，请不用到场。'), fact(c, 3, '10月28日仅称地点改为活动室B，未明确说明撤销取消', '11月2日读书会地点改为活动室B。')],
    questions=['请组织者明确：读书会是否恢复举办、是否仍在11月2日19:00于活动室B举行；仅换地点不足以明确撤销此前取消。未确认前不把到场当成已确定待办。', '若恢复，活动钟点按哪个时区理解？']
)])

c = 'C15'
save(c, [task(
    fact(c, 1, '提交差旅报销单', '差旅报销单请于2026年11月3日17:00前交财务'),
    status='needs_confirmation',
    deadline=due(both(c, '报销原截止2026年11月3日17:00；可能被延至11月6日17:00，所指不明，暂不能确定现行截止', '2026年11月3日17:00前', '上面那项截止延后到2026年11月6日17:00')),
    materials=[fact(c, 1, '差旅报销单')], submission=fact(c, 1, '交财务', '交财务'),
    changes=[fact(c, 2, '补充只说“上面那项”，无法确定是否修改报销截止', '补充：上面那项截止延后到2026年11月6日17:00。')],
    questions=['请部门明确延后截止针对报销、盘点，还是两项；不能擅自把报销改到11月6日。', ZONE]
), task(
    fact(c, 1, '提交资产盘点表', '资产盘点表请于2026年11月4日17:00前交行政'),
    status='needs_confirmation',
    deadline=due(both(c, '盘点原截止2026年11月4日17:00；可能被延至11月6日17:00，所指不明，暂不能确定现行截止', '2026年11月4日17:00前', '上面那项截止延后到2026年11月6日17:00')),
    materials=[fact(c, 1, '资产盘点表')], submission=fact(c, 1, '交行政', '交行政'),
    changes=[fact(c, 2, '补充只说“上面那项”，无法确定是否修改盘点截止', '补充：上面那项截止延后到2026年11月6日17:00。')],
    questions=['请部门明确延期对应哪项；不能依据句子位置推定盘点延期。', ZONE]
)])

c = 'C16'
save(c, [task(
    fact(c, 1, '第1步：先通过安全测验（用户尚未通过）', '尚未通过测验的同学须先通过测验，再申请预约。'),
    questions=['通知未单列安全测验的报名方式、时间或地点；请向实验室确认如何及时参加。']
), task(
    fact(c, 1, '第2步：通过测验后，申请设备预约', '已通过安全测验的同学，可在本邮件发送日的次日17:00前，将签字的设备预约单交到实验室302。'),
    status='needs_confirmation',
    deadline=due(fact(c, 1, '本邮件发送日的次日17:00前；按用户提供的邮件标签（发送于2026年10月28日09:00），对应2026年10月29日17:00；时区未注明', '本邮件发送日的次日17:00前')),
    materials=[fact(c, 1, '签字的设备预约单')],
    prerequisites=[fact(c, 1, '先通过安全测验，再申请预约', '尚未通过测验的同学须先通过测验，再申请预约。')],
    submission=fact(c, 1, '将签字的设备预约单交到实验室302', '将签字的设备预约单交到实验室302'),
    questions=[ZONE, '若无法在本次预约截止前通过测验，请实验室确认下一次预约安排；通知没有承诺延期。']
)])


summary = {'evaluation': 'forward tool and format execution only', 'input_file': str(INPUT), 'skill_checker': str(CHECKER), 'python': PYTHON, 'cases': [], 'untested_limits': ['Structural success does not establish semantic entailment, completeness, source authority, OCR accuracy, location accuracy or authenticity.', 'Only supplied text/transcriptions were available; no original screenshots or PDFs were inspected.', 'No browsing, installations, calendar actions or messages were performed.', 'No baseline, expected-answer file, behavior cases, design document or rubric was read.', 'No production skill, script or documentation was edited.']}
log = []
for case_id, interpretation in RESULTS.items():
    folder = ROOT / case_id
    folder.mkdir(parents=True, exist_ok=True)
    (folder / 'sources.json').write_text(json.dumps({'sources': CASES[case_id]['sources']}, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    (folder / 'result.json').write_text(json.dumps(interpretation, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    command = [PYTHON, '-X', 'utf8', str(CHECKER), '--sources', str(folder / 'sources.json'), '--result', str(folder / 'result.json'), '--markdown', str(folder / 'checklist.md')]
    run = subprocess.run(command, capture_output=True, text=True, encoding='utf-8', errors='replace')
    (folder / 'checker-first-run.log').write_text(f'exit_code={run.returncode}\nstdout:\n{run.stdout}\nstderr:\n{run.stderr}', encoding='utf-8')
    summary['cases'].append({'id': case_id, 'checker_exit_code': run.returncode, 'task_count': len(interpretation['tasks']), 'fixes': [], 'first_attempt_exit_code': run.returncode, 'sources_snapshot_exact': True, 'markdown_created': (folder / 'checklist.md').exists()})
    log.append(f'{case_id}: first checker exit {run.returncode}; {len(interpretation["tasks"])} tasks; no fixes.\n{run.stdout}{run.stderr}'.rstrip())
(ROOT / 'run-summary.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
(ROOT / 'run-log.txt').write_text('\n\n'.join(log) + '\n', encoding='utf-8')
print(json.dumps({'case_count': len(summary['cases']), 'passing': sum(item['checker_exit_code'] == 0 for item in summary['cases']), 'tasks': sum(item['task_count'] for item in summary['cases']), 'failures': [item for item in summary['cases'] if item['checker_exit_code'] != 0]}, ensure_ascii=False))
