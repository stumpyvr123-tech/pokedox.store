from pathlib import Path
import re

help_data_map = {
    'index.html': {
        'overview': {'title': 'Overview', 'sub': {
            'Home Hub': 'Main site starting point.',
            'What it does': 'Launch pages and change language here.',
            'Quick tips': 'Open help or use Spanish mode.'
        }},
        'navigation': {'title': 'Navigation', 'sub': {
            'Page Buttons': 'Visit each page using the buttons below.',
            'Language Globe': 'Open the language selector.',
            'Help Button': 'Open this help menu and explore tabs.'
        }},
        'features': {'title': 'Features', 'sub': {
            'Tabbed Help': 'More tabs and nested submenus live inside here.',
            'Inline Popup': 'The menu stays inside the current page.',
            'Toasts': 'Language changes show a temporary notice.'
        }},
        'faq': {'title': 'FAQ', 'sub': {
            'Language Switch': 'Choose English or Español from the globe.',
            'Page Links': 'Buttons route to each site section.',
            'Return Home': 'Use the home button anytime.'
        }}
    },
    'about.html': {
        'what': {'title': 'What is this?', 'sub': {
            'Page purpose': 'Explains the website and projects.',
            'Content': 'Shows what is built here.',
            'Updates': 'More pages and changes will arrive.'
        }},
        'purpose': {'title': 'Purpose', 'sub': {
            'Experiment': 'Try ideas and web apps in one place.',
            'Learn': 'Practice coding and design skills.',
            'Build': 'Create new pages and features.'
        }},
        'navigation': {'title': 'Navigation', 'sub': {
            'Back Home': 'Return with the home button.',
            'Page Links': 'Use buttons to move around.',
            'Help': 'Open help for page details.'
        }},
        'faq': {'title': 'FAQ', 'sub': {
            'Why Here?': 'This domain is for experimentation.',
            'How to Use': 'Click buttons to explore pages.',
            'More Soon': 'More content will be added soon.'
        }}
    },
    'documenting.html': {
        'what': {'title': 'What is this?', 'sub': {
            'Content': 'Notes and coding journey information.',
            'Video': 'A link to a tutorial video is included.',
            'Purpose': 'Documents development progress.'
        }},
        'video': {'title': 'Video', 'sub': {
            'Watch': 'Open the YouTube guide from the page.',
            'Tutorial': 'Learn from the video walkthrough.',
            'Link': 'Use the link provided on the page.'
        }},
        'navigation': {'title': 'Navigation', 'sub': {
            'Back Home': 'Home returns to the main site.',
            'Link': 'Video opens in a new tab.',
            'Help': 'Use help for page details.'
        }},
        'faq': {'title': 'FAQ', 'sub': {
            'Why Video?': 'Provides extra learning support.',
            'Page Use': 'Tracks coding progress and notes.',
            'Next Step': 'Explore other pages afterward.'
        }}
    },
    'system-requirements.html': {
        'browser': {'title': 'Browser', 'sub': {
            'Supported': 'Chrome, Firefox, Edge, and Safari work best.',
            'Modern': 'Needs HTML5 and CSS3 support.',
            'Update': 'Use the newest browser version.'
        }},
        'troubleshoot': {'title': 'Troubleshoot', 'sub': {
            'Refresh': 'Reload the page if something breaks.',
            'JS': 'Enable JavaScript for all features.',
            'Update': 'Keep the browser current.'
        }},
        'navigation': {'title': 'Navigation', 'sub': {
            'Back Home': 'Use the home button to return.',
            'Other Pages': 'Select another page from the menu.',
            'Help': 'Open help if you need guidance.'
        }},
        'faq': {'title': 'FAQ', 'sub': {
            'Why Errors': 'Old browsers can cause rendering issues.',
            'Best Result': 'Use a modern browser for stability.',
            'Page Load': 'Check your internet connection.'
        }}
    },
    'index-es.html': {
        'overview': {'title': 'Resumen', 'sub': {
            'Centro': 'Inicio de nittany34.com.',
            'Qué hace': 'Abre páginas y cambia idioma.',
            'Consejos': 'Usa ayuda o el modo español.'
        }},
        'navigation': {'title': 'Navegación', 'sub': {
            'Botones': 'Visita cada página del sitio.',
            'Globo': 'Abre el selector de idioma.',
            'Ayuda': 'Abre el menú de ayuda.'
        }},
        'features': {'title': 'Características', 'sub': {
            'Pestañas': 'Más pestañas y submenús dentro de la ayuda.',
            'Popup': 'El menú permanece dentro de la página.',
            'Avisos': 'El cambio de idioma muestra una notificación.'
        }},
        'faq': {'title': 'Preguntas', 'sub': {
            'Idioma': 'Elige English o Español con el globo.',
            'Enlaces': 'Los botones van a cada sección.',
            'Inicio': 'Vuelve a la página principal cuando quieras.'
        }}
    },
    'about-es.html': {
        'what': {'title': '¿Qué es esto?', 'sub': {
            'Propósito': 'Explica el sitio y los proyectos.',
            'Contenido': 'Muestra lo que se construye aquí.',
            'Actualizaciones': 'Más proyectos llegarán pronto.'
        }},
        'purpose': {'title': 'Propósito', 'sub': {
            'Experimentar': 'Probar ideas y apps web.',
            'Aprender': 'Practicar programación y diseño.',
            'Construir': 'Crear nuevas páginas y funciones.'
        }},
        'navigation': {'title': 'Navegación', 'sub': {
            'Volver': 'Regresa con el botón de inicio.',
            'Enlaces': 'Usa botones para moverte.',
            'Ayuda': 'Abre ayuda para más detalles.'
        }},
        'faq': {'title': 'Preguntas', 'sub': {
            'Por qué aquí?': 'Dominio usado para experimentos.',
            'Cómo usar': 'Haz clic para explorar páginas.',
            'Más tarde': 'Pronto habrá más contenido.'
        }}
    },
    'documenting-es.html': {
        'what': {'title': '¿Qué es esto?', 'sub': {
            'Contenido': 'Notas e información de codificación.',
            'Video': 'Enlace a un video tutorial.',
            'Propósito': 'Documenta el progreso de desarrollo.'
        }},
        'video': {'title': 'Video', 'sub': {
            'Ver': 'Abre la guía en YouTube.',
            'Tutorial': 'Aprende con el video.',
            'Enlace': 'Usa el enlace en la página.'
        }},
        'navigation': {'title': 'Navegación', 'sub': {
            'Volver': 'Botón de inicio regresa al sitio.',
            'Enlace': 'Video abre en una nueva pestaña.',
            'Ayuda': 'Usa ayuda si necesitas.'
        }},
        'faq': {'title': 'Preguntas', 'sub': {
            'Por qué video?': 'Recurso extra para aprender.',
            'Uso': 'Sigue tu progreso de codificación.',
            'Siguiente': 'Explora otras páginas después.'
        }}
    },
    'system-requirements-es.html': {
        'browser': {'title': 'Navegador', 'sub': {
            'Compatibles': 'Chrome, Firefox, Edge y Safari funcionan mejor.',
            'Moderno': 'Necesita soporte HTML5/CSS3.',
            'Actualizar': 'Usa la versión más reciente.'
        }},
        'troubleshoot': {'title': 'Solución', 'sub': {
            'Recargar': 'Actualiza la página si falla.',
            'JS': 'Activa JavaScript.',
            'Actualizar': 'Mantén el navegador al día.'
        }},
        'navigation': {'title': 'Navegación', 'sub': {
            'Volver': 'Botón Inicio para regresar.',
            'Otras': 'Usa los botones de página.',
            'Ayuda': 'Abre ayuda si necesitas guía.'
        }},
        'faq': {'title': 'Preguntas', 'sub': {
            'Errores': 'Navegadores antiguos pueden fallar.',
            'Mejor': 'Usa navegador moderno.',
            'Carga': 'Verifica tu conexión a internet.'
        }}
    }
}

new_css = '''        .help-button {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            width: 42px;
            height: 42px;
            font-size: 1.1rem;
            border-radius: 50%;
            margin-left: 8px;
        }
        .help-menu {
            display: none;
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background-color: rgba(255, 255, 255, 0.98);
            color: rgb(0, 0, 0);
            border: 2px solid black;
            padding: 18px;
            border-radius: 18px;
            text-align: left;
            z-index: 1500;
            width: min(420px, 92vw);
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.25);
        }
        .help-tabs {
            display: flex;
            justify-content: space-between;
            gap: 6px;
            margin-bottom: 12px;
        }
        .help-tab {
            flex: 1;
            padding: 10px 12px;
            border-radius: 8px;
            border: 1px solid black;
            background: rgba(0, 0, 0, 0.08);
            cursor: pointer;
            font-family: 'Courier New', monospace;
            color: rgb(0, 0, 0);
            transition: background 0.2s, color 0.2s;
        }
        .help-tab.active {
            background: black;
            color: rgb(0, 255, 13);
            border-color: rgb(0, 255, 13);
        }
        .help-submenu {
            display: flex;
            flex-wrap: wrap;
            gap: 6px;
            margin-bottom: 12px;
        }
        .help-subtab {
            flex: 1 1 45%;
            padding: 8px 10px;
            border-radius: 8px;
            border: 1px solid rgba(0,0,0,0.2);
            background: rgba(0, 0, 0, 0.04);
            cursor: pointer;
            font-family: 'Courier New', monospace;
            color: rgb(0, 0, 0);
            text-align: center;
        }
        .help-subtab.active {
            background: rgba(0, 255, 13, 0.15);
            border-color: rgb(0, 255, 13);
        }
        .help-content {
            padding: 12px;
            background: rgba(0, 183, 255, 0.12);
            border-radius: 10px;
            min-height: 140px;
            font-size: 0.95rem;
            line-height: 1.5;
        }
'''

js_template = '''<script>
        const helpData = {
{help_data}
        };
        function toggleLanguageMenu() {
            const menu = document.getElementById('language-menu');
            if (!menu) return;
            menu.style.display = menu.style.display === 'block' ? 'none' : 'block';
            const help = document.getElementById('help-menu');
            if (help) help.style.display = 'none';
        }
        function toggleHelpMenu() {
            const menu = document.getElementById('help-menu');
            if (!menu) return;
            if (menu.style.display === 'block') {
                menu.style.display = 'none';
            } else {
                const firstTab = Object.keys(helpData)[0];
                openHelpTab(firstTab);
                menu.style.display = 'block';
            }
            const lang = document.getElementById('language-menu');
            if (lang) lang.style.display = 'none';
        }
        function openHelpTab(tab) {
            const data = helpData[tab];
            if (!data) return;
            const submenu = document.getElementById('help-submenu');
            submenu.innerHTML = '';
            const firstSub = Object.keys(data.sub || {})[0] || null;
            if (data.sub) {
                Object.keys(data.sub).forEach((subtab) => {
                    const btn = document.createElement('button');
                    btn.type = 'button';
                    btn.className = 'help-subtab';
                    btn.textContent = subtab;
                    btn.onclick = () => openHelpSubtab(tab, subtab);
                    btn.dataset.subtab = subtab;
                    submenu.appendChild(btn);
                });
            }
            openHelpSubtab(tab, firstSub);
            document.querySelectorAll('.help-tab').forEach(btn => {
                btn.classList.toggle('active', btn.dataset.tab === tab);
            });
        }
        function openHelpSubtab(tab, subtab) {
            const data = helpData[tab];
            if (!data) return;
            const content = document.getElementById('help-content');
            const subContent = data.sub && data.sub[subtab];
            const title = data.title || '';
            if (subContent) {
                content.innerHTML = '<strong>' + title + ' \u2014 ' + subtab + '</strong><p style="margin-top:10px;">' + subContent + '</p>';
            } else {
                content.innerHTML = '<strong>' + title + '</strong><p style="margin-top:10px;">' + (data.text || 'No details available.') + '</p>';
            }
            document.querySelectorAll('.help-subtab').forEach(btn => {
                btn.classList.toggle('active', btn.dataset.subtab === subtab);
            });
        }
        function buildHelpTabs() {
            const tabs = document.querySelectorAll('.help-tab');
            if (!tabs.length) return;
            tabs.forEach(btn => {
                btn.addEventListener('click', () => openHelpTab(btn.dataset.tab));
            });
        }
        function switchToEnglish() {
            showLanguageNotice('Switching to English...');
            setTimeout(() => window.location.href = window.location.pathname.endsWith('-es.html') ? 'index.html' : 'index.html', 600);
        }
        function switchToSpanish() {
            showLanguageNotice('Cambiando a EspaÃ±ol...');
            setTimeout(() => window.location.href = window.location.pathname.endsWith('-es.html') ? 'index-es.html' : 'index-es.html', 600);
        }
        function showLanguageNotice(message) {
            const notice = document.getElementById('language-notice');
            if (!notice) return;
            notice.textContent = message;
            notice.style.display = 'block';
            notice.style.opacity = '1';
            setTimeout(() => { notice.style.opacity = '0'; setTimeout(() => notice.style.display = 'none', 300); }, 1800);
        }
        document.addEventListener('click', (event) => {
            const langMenu = document.getElementById('language-menu');
            const helpMenu = document.getElementById('help-menu');
            const langButton = document.querySelector('.language-toggler');
            const helpButton = document.querySelector('.help-button');
            if (langMenu && langButton && !langMenu.contains(event.target) && !langButton.contains(event.target)) {
                langMenu.style.display = 'none';
            }
            if (helpMenu && helpButton && !helpMenu.contains(event.target) && !helpButton.contains(event.target)) {
                helpMenu.style.display = 'none';
            }
        });
        document.addEventListener('keydown', (event) => {
            const helpMenu = document.getElementById('help-menu');
            if (event.key === 'Escape' && helpMenu) {
                helpMenu.style.display = 'none';
            }
        });
        document.addEventListener('DOMContentLoaded', buildHelpTabs);
    </script>'''


def js_value(value):
    safe = value.replace("'", "\\'").replace('\\', '\\\\')
    return safe

for filename, data in help_data_map.items():
    path = Path(filename)
    if not path.exists():
        print('missing', filename)
        continue
    content = path.read_text()
    content = re.sub(r'\s*\.help-button \{.*?\.help-content \{.*?\}\s*', new_css, content, flags=re.S)
    content = re.sub(r'<div style="position: relative; text-align: center; margin-bottom: 20px;">.*?<div id="language-notice" class="language-notice"></div>\s*</div>', '', content, flags=re.S)
    # preserve the original language label if present
    label_match = re.search(r'<span class="language-label">([^<]+)</span>', content)
    label = label_match.group(1) if label_match else 'English'
    tabs_html = ''
    for tab_id, tab_obj in data.items():
        tabs_html += f'                <button class="help-tab" type="button" data-tab="{tab_id}" onclick="openHelpTab(\'{tab_id}\')">{tab_obj["title"]}</button>\n'
    help_html = f'''    <div style="position: relative; text-align: center; margin-bottom: 20px;">
        <button onclick="toggleLanguageMenu()" class="button-link language-toggler" type="button">
            <span class="globe">🌐</span>
            <span class="language-label">{label}</span>
            <span class="language-arrow">▼</span>
        </button>
        <button onclick="toggleHelpMenu()" class="button-link help-button" type="button">?</button>
        <div id="language-menu" class="language-menu">
            <button onclick="switchToEnglish()" class="button-link" type="button">English</button>
            <button onclick="switchToSpanish()" class="button-link" type="button">Español</button>
        </div>
        <div id="help-menu" class="help-menu">
            <div style="display:flex; align-items:center; justify-content:space-between; margin-bottom:10px; gap:10px;">
                <div style="font-weight:bold; font-size:1rem;">Help Menu</div>
                <button onclick="toggleHelpMenu()" style="background:none; border:none; font-size:1.2rem; cursor:pointer;">×</button>
            </div>
            <div class="help-tabs">
{tabs_html}            </div>
            <div id="help-submenu" class="help-submenu"></div>
            <div id="help-content" class="help-content"></div>
        </div>
        <div id="language-notice" class="language-notice"></div>
    </div>'''
    # Insert help_html before first <h1> or <body>
    body_index = content.find('<h1')
    if body_index == -1:
        body_index = content.find('<body>')
        if body_index == -1:
            body_index = 0
    content = content[:body_index] + help_html + '\n\n' + content[body_index:]
    # Replace last script block
    content = re.sub(r'<script>.*?</script>\s*</body>', js_template + '\n</body>', content, flags=re.S)
    # build helpData JS
    data_lines = []
    for tab_id, tab_obj in data.items():
        parts = []
        for sub_id, sub_text in tab_obj['sub'].items():
            parts.append(f"                '{js_value(sub_id)}': '{js_value(sub_text)}'")
        sub_text = ',\n'.join(parts)
        data_lines.append(f"            '{js_value(tab_id)}': {{ title: '{js_value(tab_obj['title'])}', sub: {{\n{sub_text}\n            }} }}")
    help_js = ',\n'.join(data_lines)
    content = content.replace('{help_data}', help_js)
    path.write_text(content)
    print('patched', filename)
