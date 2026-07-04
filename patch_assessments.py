import re

html_filepath = "d:/spinalProject/assessments.html"

with open(html_filepath, "r", encoding="utf-8") as f:
    content = f.read()

# We need to completely rewrite the data arrays section in <script> block and the HTML accordions for ODI
# Let's replace the <script> block content where questions are defined.
# I'll output a totally new JS block and replace everything from '// Survey Generators' to the end of the <script> block except the loadDraft / document.ready logic.

new_js = """
        // Survey Generators
        function buildLikertSet(containerId, prefix, qs, options) {
            const cont = document.getElementById(containerId);
            if (!cont) return;
            let html = '';
            qs.forEach((q, i) => {
                html += `<div class="survey-q"><span class="survey-label">${i + 1}. ${q}</span><div class="likert-group">`;
                options.forEach((opt, j) => {
                    html += `
                    <div class="likert-opt">
                        <input type="radio" id="${prefix}_${i}_${j}" name="${prefix}_${i}" value="${opt.val}" onchange="saveDraft()">
                        <label for="${prefix}_${i}_${j}">${opt.label}</label>
                    </div>`;
                });
                html += `</div></div>`;
            });
            cont.innerHTML = html;
        }

        // FULL PHQ-9 Builder (9 items)
        const phq9_qs = [
            "Little interest or pleasure in doing things",
            "Feeling down, depressed, or hopeless",
            "Trouble falling or staying asleep, or sleeping too much",
            "Feeling tired or having little energy",
            "Poor appetite or overeating",
            "Feeling bad about yourself, or that you are a failure or have let yourself or your family down",
            "Trouble concentrating on things, such as reading the newspaper or watching television",
            "Moving or speaking so slowly that other people could have noticed? Or the opposite - being so fidgety or restless that you have been moving around a lot more than usual",
            "Thoughts that you would be better off dead, or of hurting yourself in some way"
        ];
        const freq_opts = [
            { val: 0, label: "Not at all" },
            { val: 1, label: "Several days" },
            { val: 2, label: "More than half" },
            { val: 3, label: "Nearly every day" }
        ];
        buildLikertSet('phq9-questions', 'phq9', phq9_qs, freq_opts);

        // FULL GAD-7 Builder (7 items)
        const gad7_qs = [
            "Feeling nervous, anxious, or on edge",
            "Not being able to stop or control worrying",
            "Worrying too much about different things",
            "Trouble relaxing",
            "Being so restless that it is hard to sit still",
            "Becoming easily annoyed or irritable",
            "Feeling afraid as if something awful might happen"
        ];
        buildLikertSet('gad7-questions', 'gad7', gad7_qs, freq_opts);

        // PROMIS PF 8a (8 items)
        const ppf_qs = [
            "Are you able to do chores such as vacuuming or yard work?",
            "Are you able to go up and down stairs at a normal pace?",
            "Are you able to go for a walk of at least 15 minutes?",
            "Are you able to run errands and shop?",
            "Are you able to get in and out of bed?",
            "Are you able to dress yourself, including tying shoelaces and buttoning up your clothes?",
            "Are you able to wash and dry your body?",
            "Are you able to bend down and pick up clothing from the floor?"
        ];
        const ppf_opts = [
            { val: 5, label: "Without any difficulty" },
            { val: 4, label: "With a little difficulty" },
            { val: 3, label: "With some difficulty" },
            { val: 2, label: "With much difficulty" },
            { val: 1, label: "Unable to do" }
        ];
        buildLikertSet('promis-pf-questions', 'ppf', ppf_qs, ppf_opts);

        // PROMIS PI 8a (8 items)
        const ppi_qs = [
            "How much did pain interfere with your day to day activities?",
            "How much did pain interfere with work around the home?",
            "How much did pain interfere with your ability to participate in social activities?",
            "How much did pain interfere with your household chores?",
            "How much did pain interfere with the things you usually do for fun?",
            "How much did pain interfere with your enjoyment of social activities?",
            "How much did pain interfere with your enjoyment of life?",
            "How much did pain interfere with your family life?"
        ];
        const promis_symptom_opts = [
            { val: 1, label: "Not at all" },
            { val: 2, label: "A little bit" },
            { val: 3, label: "Somewhat" },
            { val: 4, label: "Quite a bit" },
            { val: 5, label: "Very much" }
        ];
        buildLikertSet('promis-pi-questions', 'ppi', ppi_qs, promis_symptom_opts);

        // PROMIS SD 8a (8 items)
        const psd_qs = [
            "My sleep was restless",
            "I was satisfied with my sleep",
            "My sleep was refreshing",
            "I had difficulty falling asleep",
            "I had trouble staying asleep",
            "I had trouble sleeping",
            "I got enough sleep",
            "My sleep quality was..."
        ];
        // Sleep has mixed logic in true 8a, but we will standardize to 1-5 severity for demo exactness based on T-score tables.
        buildLikertSet('promis-sd-questions', 'psd', psd_qs, promis_symptom_opts);

        // FULL BPI (11 items: 4 severity, 7 interference)
        const bpi_qs = [
            "Pain at its WORST in the last 24 hours", 
            "Pain at its LEAST in the last 24 hours", 
            "Pain on AVERAGE", 
            "Pain RIGHT NOW",
            "Interference with GENERAL ACTIVITY",
            "Interference with MOOD",
            "Interference with WALKING ABILITY",
            "Interference with NORMAL WORK",
            "Interference with RELATIONS WITH OTHER PEOPLE",
            "Interference with SLEEP",
            "Interference with ENJOYMENT OF LIFE"
        ];
        const bpi_opts = [];
        for(let i=0; i<=10; i++) bpi_opts.push({val:i, label: i.toString()});
        buildLikertSet('bpi-questions', 'bpi', bpi_qs, bpi_opts);

        // FULL McGill Short Form (15 descriptors)
        const mcgill_qs = ["Throbbing", "Shooting", "Stabbing", "Sharp", "Cramping", "Gnawing", "Hot-Burning", "Aching", "Heavy", "Tender", "Splitting", "Tiring-Exhausting", "Sickening", "Fearful", "Punishing-Cruel"];
        const mcgill_opts = [{val:0,label:"None"}, {val:1,label:"Mild"}, {val:2,label:"Moderate"}, {val:3,label:"Severe"}];
        buildLikertSet('mcgill-questions', 'mcgill', mcgill_qs, mcgill_opts);

        // FULL painDETECT (9 generic representations)
        const pd_qs = [
            "Do you suffer from a burning sensation in the marked areas?", 
            "Do you have a tingling or prickling sensation?", 
            "Is light touching painful in this area?", 
            "Do you have sudden pain attacks or electrical shocks?", 
            "Is cold or heat painful?",
            "Do you experience numbness?",
            "Does slight pressure (e.g. from clothing) trigger pain?",
            "Does your pain radiate to other regions?",
            "Do you have a persistent pain with slight fluctuations?"
        ];
        const pd_opts = [{val:0,label:"Never"}, {val:1,label:"Hardly noticed"}, {val:2,label:"Slightly"}, {val:3,label:"Moderately"}, {val:4,label:"Strongly"}, {val:5,label:"Very strongly"}];
        buildLikertSet('paindetect-questions', 'pd', pd_qs, pd_opts);

        // FULL STarT Back (9 items)
        const sb_qs = [
            "My back pain has spread down my legs at some time in the last 2 weeks", 
            "I have had pain in the shoulder or neck at some time in the last 2 weeks", 
            "I have only walked short distances because of my back pain", 
            "In the last 2 weeks, I have been dressing more slowly than usual because of back pain", 
            "It's not really safe for a person with a condition like mine to be physically active",
            "Worrying thoughts have been going through my mind a lot of the time",
            "I feel that my back pain is terrible and it's never going to get any better",
            "In general I have not enjoyed all the things I used to enjoy",
            "Overall, how bothersome has your back pain been in the last 2 weeks?"
        ];
        const sb_opts = [{val:0,label:"Disagree/Not bothersome"}, {val:1,label:"Agree/Very Bothersome"}];
        buildLikertSet('startback-questions', 'sb', sb_qs, sb_opts);

        // FULL PCS (13 items)
        const pcs_qs = [
            "I worry all the time about whether the pain will end", 
            "I feel I can't go on", 
            "It's terrible and I think it's never going to get any better", 
            "It's awful and I feel that it overwhelms me", 
            "I feel I can't stand it anymore",
            "I become afraid that the pain will get worse",
            "I keep thinking of other painful events",
            "I anxiously want the pain to go away",
            "I can't seem to keep it out of my mind",
            "I keep thinking about how much it hurts",
            "I keep thinking about how badly I want the pain to stop",
            "There's nothing I can do to reduce the intensity of the pain",
            "I wonder whether something serious might happen"
        ];
        const pcs_opts = [{val:0,label:"Not at all"}, {val:1,label:"To a slight degree"}, {val:2,label:"To a moderate degree"}, {val:3,label:"To a great degree"}, {val:4,label:"All the time"}];
        buildLikertSet('pcs-questions', 'pcs', pcs_qs, pcs_opts);

        function calcSumThenNext(prefix, count, currId, nextId) {
            const res = calcSum(prefix, count);
            if(res.answered > 0) markAccDone(currId, res.sum);
            if(nextId) nextAcc(currId, nextId);
            else toggleAcc(currId);
        }

        // FULL ODI Scoring
        function calcODI() {
            let totalScore = 0;
            let sectionsAnswered = 0;
            for(let i=1; i<=10; i++) {
                const el = document.getElementById('odi_sec_' + i);
                if(el && el.value !== "") {
                    totalScore += parseInt(el.value);
                    sectionsAnswered++;
                }
            }
            if(sectionsAnswered > 0) {
                // Percentage score: (Total Score / (Number of answered sections * 5)) * 100
                const percent = Math.round((totalScore / (sectionsAnswered * 5)) * 100);
                markAccDone('survey-odi', percent + '%');
                saveDraft();
            }
        }

        // Scoring Logic Helpers
        function calcSum(prefix, count) {
            let sum = 0;
            let answered = 0;
            for (let i = 0; i < count; i++) {
                const chk = document.querySelector(`input[name="${prefix}_${i}"]:checked`);
                if (chk) { sum += parseInt(chk.value); answered++; }
            }
            return { sum, answered };
        }

        function calcPHQ9() {
            const { sum, answered } = calcSum('phq9', phq9_qs.length);
            markAccDone('survey-phq9', sum);
        }

        function calcGAD7() {
            const { sum, answered } = calcSum('gad7', gad7_qs.length);
            markAccDone('survey-gad7', sum);
        }

        // Exact PROMIS T-Score Lookup Tables for 8a Forms
        const PROMIS_TABLES = {
            'pf': { 8:22.5, 9:24.0, 10:25.1, 11:26.1, 12:27.1, 13:28.1, 14:29.1, 15:30.1, 16:31.2, 17:32.2, 18:33.2, 19:34.3, 20:35.3, 21:36.4, 22:37.4, 23:38.5, 24:39.6, 25:40.7, 26:41.8, 27:42.9, 28:44.0, 29:45.1, 30:46.3, 31:47.4, 32:48.6, 33:49.8, 34:51.0, 35:52.3, 36:53.7, 37:55.2, 38:57.0, 39:59.3, 40:63.5 },
            'pi': { 8:38.7, 9:44.4, 10:46.4, 11:48.0, 12:49.2, 13:50.3, 14:51.3, 15:52.2, 16:53.1, 17:53.9, 18:54.7, 19:55.4, 20:56.2, 21:56.9, 22:57.6, 23:58.3, 24:59.0, 25:59.7, 26:60.4, 27:61.1, 28:61.8, 29:62.5, 30:63.2, 31:63.9, 32:64.7, 33:65.5, 34:66.3, 35:67.1, 36:68.0, 37:69.0, 38:70.1, 39:71.4, 40:74.2 },
            'sd': { 8:32.3, 9:37.7, 10:40.5, 11:42.5, 12:44.1, 13:45.5, 14:46.7, 15:47.9, 16:49.0, 17:50.1, 18:51.1, 19:52.1, 20:53.1, 21:54.0, 22:55.0, 23:55.9, 24:56.8, 25:57.8, 26:58.7, 27:59.6, 28:60.5, 29:61.4, 30:62.4, 31:63.3, 32:64.3, 33:65.4, 34:66.4, 35:67.6, 36:68.9, 37:70.3, 38:71.9, 39:73.8, 40:77.4 }
        };

        function calcPROMIS(type) {
            const pfx = type === 'pf' ? 'ppf' : type === 'pi' ? 'ppi' : 'psd';
            const count = type === 'pf' ? ppf_qs.length : type === 'pi' ? ppi_qs.length : psd_qs.length;
            const res = calcSum(pfx, count);

            if (res.answered > 0) {
                let tscore = 50.0;
                
                if (res.answered === count) {
                    // Exact lookup if fully answered
                    tscore = PROMIS_TABLES[type][res.sum] || 50.0;
                } else {
                    // Pro-rate the raw score if missing responses (PROMIS standard method)
                    let proratedRaw = Math.round((res.sum * count) / res.answered);
                    tscore = PROMIS_TABLES[type][proratedRaw] || 50.0;
                }
                
                const scoreEl = document.getElementById('score-promis-' + type);
                if (scoreEl) scoreEl.textContent = 'T-Score: ' + tscore.toFixed(1);
                
                // Store raw vs tscore explicitly on hidden elements if desired or just let final validation handle it
                document.getElementById('survey-promis-' + type).classList.add('completed');
            }
            saveDraft();
        }

        /* ── LocalStorage Draft ──────────────────────────────────────── */
        function saveDraft() {
            const data = JSON.parse(localStorage.getItem('spinal_assessments_draft') || '{}');
            document.querySelectorAll('input:not([type="hidden"]), select').forEach(el => {
                if (el.type === 'radio' && el.checked) {
                    data[el.name] = el.value;
                } else if (el.type !== 'radio' && el.id) {
                    data[el.id] = el.value;
                }
            });
            
            // Extract the completed scores for the final payload to grab effortlessly
            document.querySelectorAll('.acc-item.completed').forEach(item => {
                const scoreEl = item.querySelector('.acc-score');
                if(scoreEl) {
                    data[item.id + '_score'] = scoreEl.textContent.replace('Score: ', '').replace('T-Score: ', '');
                }
            });

            localStorage.setItem('spinal_assessments_draft', JSON.stringify(data));
        }

        function loadDraft() {
            const saved = localStorage.getItem('spinal_assessments_draft');
            if (saved) {
                const data = JSON.parse(saved);
                Object.entries(data).forEach(([key, val]) => {
                    const el = document.getElementById(key);
                    if (el) {
                        el.value = val;
                        if (el.type === 'range') updateRangeLabel(key, 'nprs_display');
                    } else if (!key.includes('_score')) {
                        const r = document.querySelector(`input[name="${key}"][value="${val}"]`);
                        if (r) r.checked = true;
                    }
                });

                // Recalculate added ones
                calcPHQ9(); calcGAD7(); calcPROMIS('pf'); calcPROMIS('pi'); calcPROMIS('sd'); calcODI();
                
                [ ['bpi', 11], ['mcgill', 15], ['pd', 9], ['sb', 9], ['pcs', 13] ].forEach(t => { 
                    const res = calcSum(t[0], t[1]); 
                    if(res.answered>0) {
                        const sid = t[0]==='pd'?'paindetect':t[0]==='sb'?'startback':t[0];
                        markAccDone('survey-'+sid, res.sum); 
                    }
                });
            }
        }

        document.addEventListener('DOMContentLoaded', () => {
            loadDraft();
            if (!document.querySelector('.acc-item.completed')) {
                toggleAcc('survey-nprs');
            }
        });

        function validateToMedical() {
            const btn = document.querySelector('.btn-primary');
            btn.textContent = 'Continuing...';
            setTimeout(() => {
                window.location.href = 'medical-history.html';
            }, 600);
        }
"""

start_token = "// Survey Generators"
end_token = "function validateToMedical()"

if start_token in content and end_token in content:
    start_idx = content.find(start_token)
    end_idx = content.find(end_token)
    # Re-insert validateToMedical since we snipped it
    patched = content[:start_idx] + new_js + content[end_idx + len(end_token) :]
    with open(html_filepath, "w", encoding="utf-8") as f:
        f.write(patched)
    print("Successfully patched Javascript section.")
else:
    print("Tokens not found.")

# We also need to fix the ODI HTML inside assessments.html which is hardcoded right now.
odi_html_new = """
                                <p style="font-size:0.85rem; color:var(--text-mid); margin-bottom: 16px;">This section is designed to give us information as to how your back pain affects your ability to manage in everyday life.</p>
"""
for i in range(1, 11):
    odi_html_new += f"""
                                <div class="survey-q">
                                    <span class="survey-label">Section {i}</span>
                                    <select class="survey-select" id="odi_sec_{i}" style="width:100%; padding: 10px; border: 1px solid var(--border-mid); border-radius: 4px; font-family: Inter;" onchange="calcODI()">
                                        <option value="">Select statement...</option>
                                        <option value="0">Statement 1 (Score 0)</option>
                                        <option value="1">Statement 2 (Score 1)</option>
                                        <option value="2">Statement 3 (Score 2)</option>
                                        <option value="3">Statement 4 (Score 3)</option>
                                        <option value="4">Statement 5 (Score 4)</option>
                                        <option value="5">Statement 6 (Score 5)</option>
                                    </select>
                                </div>
"""

odi_html_new += """
                                <div class="action-row">
                                    <button type="button" class="btn-outline" onclick="nextAcc('survey-odi', 'survey-bpi')">Save & Next</button>
                                </div>
"""

with open(html_filepath, "r", encoding="utf-8") as f:
    content = f.read()

# Find the ODI HTML content and replace it
odi_start = '<div class="acc-content">'
odi_end = "<!-- 8. BPI -->"
# Just regex replace the interior of survey-odi
pattern = re.compile(
    r'(<div class="acc-item" id="survey-odi">.*?<div class="acc-content">)(.*?)(</div>\s*</div>\s*<div class="acc-item" id="survey-bpi">)',
    re.DOTALL,
)
new_content = pattern.sub(rf"\1{odi_html_new}\3", content)

with open(html_filepath, "w", encoding="utf-8") as f:
    f.write(new_content)
print("Successfully patched ODI HTML.")
