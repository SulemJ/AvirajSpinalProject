html_filepath = "d:/spinalProject/medical-history.html"
with open(html_filepath, "r", encoding="utf-8") as f:
    content = f.read()

new_js = """
        // Base64 File Upload Handlers
        let uploadedFilesBase64 = [];

        document.getElementById('fileUpload').addEventListener('change', async function(e) {
            const list = document.getElementById('file-list');
            list.innerHTML = '<div style="color:var(--teal-dark)">Processing files...</div>';
            
            let html = '';
            // Reset base64 arrays to current (simplistic model replaces old selections on re-select)
            uploadedFilesBase64 = []; 
            
            for (let file of this.files) {
                try {
                    const b64 = await readFileAsBase64(file);
                    uploadedFilesBase64.push({ name: file.name, type: file.type, data: b64 });
                    
                    if (file.type.startsWith('image/')) {
                        html += `<div style="display:inline-block; margin-right:8px; text-align:center;">
                                    <img src="${b64}" style="max-width:80px; max-height:80px; border-radius:var(--radius-sm); margin-top:8px; box-shadow: 0 4px 10px rgba(0,0,0,0.05); border:1px solid var(--border-mid)">
                                    <div style="font-size:0.7rem; max-width:80px; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; margin-top:6px;">${file.name}</div>
                                 </div>`;
                    } else {
                        html += `<div style="margin-top:8px;">📄 ${file.name} (Ready)</div>`;
                    }
                } catch(err) {
                    html += `<div style="color:red;">❌ Error loading ${file.name}</div>`;
                }
            }
            list.innerHTML = html;
            saveDraft();
        });

        function readFileAsBase64(file) {
            return new Promise((resolve, reject) => {
                const reader = new FileReader();
                reader.onload = () => resolve(reader.result);
                reader.onerror = error => reject(error);
                reader.readAsDataURL(file);
            });
        }

        /* ── LocalStorage Draft ──────────────────────────────────────── */
        function saveDraft() {
            const data = JSON.parse(localStorage.getItem('spinal_medical_draft') || '{}');
            document.querySelectorAll('input[type="checkbox"], textarea').forEach(el => {
                if (el.type === 'checkbox') {
                    data[el.id] = el.checked;
                } else if (el.id) {
                    data[el.id] = el.value;
                }
            });
            // Store attachments
            data._attachments = uploadedFilesBase64;
            localStorage.setItem('spinal_medical_draft', JSON.stringify(data));
        }

        function loadDraft() {
            const saved = localStorage.getItem('spinal_medical_draft');
            if(saved) {
                const data = JSON.parse(saved);
                Object.entries(data).forEach(([key, val]) => {
                    if (key === '_attachments') {
                        uploadedFilesBase64 = val || [];
                        const list = document.getElementById('file-list');
                        let html = '';
                        uploadedFilesBase64.forEach(f => {
                            if (f.type && f.type.startsWith('image/')) {
                                html += `<div style="display:inline-block; margin-right:8px; text-align:center;">
                                            <img src="${f.data}" style="max-width:80px; max-height:80px; border-radius:var(--radius-sm); margin-top:8px; box-shadow: 0 4px 10px rgba(0,0,0,0.05); border:1px solid var(--border-mid)">
                                            <div style="font-size:0.7rem; max-width:80px; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; margin-top:6px;">${f.name}</div>
                                         </div>`;
                            } else {
                                html += `<div style="margin-top:8px;">📄 ${f.name} (Ready)</div>`;
                            }
                        });
                        list.innerHTML = html;
                    } else {
                        const el = document.getElementById(key);
                        if(el) {
                            if(el.type === 'checkbox') el.checked = val;
                            else el.value = val;
                        }
                    }
                });
            }
        }
"""

start_token = "// File Upload Handlers (Simulation)"
end_token = "document.querySelectorAll('input, textarea').forEach(el => {"

start_idx = content.find(start_token)
end_idx = content.find(end_token)

if start_idx != -1 and end_idx != -1:
    patched = content[:start_idx] + new_js + content[end_idx:]
    with open(html_filepath, "w", encoding="utf-8") as f:
        f.write(patched)
    print("Successfully patched medical-history JavaScript.")
else:
    print("Tokens not found.")
