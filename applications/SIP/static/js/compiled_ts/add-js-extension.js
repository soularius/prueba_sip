import fs from 'fs.js';
import path from 'path.js';
function addJsExtension(dir) {
    const files = fs.readdirSync(dir);
    files.forEach(file => {
        let fullPath = path.join(dir, file);
        if (fs.statSync(fullPath).isDirectory()) {
            addJsExtension(fullPath);
        }
        else if (fullPath.endsWith('.js')) {
            let content = fs.readFileSync(fullPath, 'utf8');
            content = content.replace(/from\s+(['"])(.*?)(\1)/g, (match, p1, p2) => {
                if (!p2.endsWith('.js') && !p2.startsWith('http')) {
                    return `from ${p1}${p2}.js${p1}`;
                }
                return match;
            });
            fs.writeFileSync(fullPath, content, 'utf8');
        }
    });
}
addJsExtension('../static/js/compiled_ts');
