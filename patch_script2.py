from pathlib import Path
import re

files = ['index.html','about.html','documenting.html','system-requirements.html','index-es.html','about-es.html','documenting-es.html','system-requirements-es.html']

common_script = '''<script>
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
                content.innerHTML = '<strong>' + title + ' — ' + subtab + '</strong><p style="margin-top:10px;">' + subContent + '</p>';
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
            const pathname = window.location.pathname;
            showLanguageNotice('Switching to English...');
            setTimeout(() => {
                if (pathname.endsWith('-es.html')) {
                    window.location.href = pathname.replace(/-es\.html$/, '.html');
                } else {
                    window.location.href = 'index.html';
                }
            }, 600);
        }
        function switchToSpanish() {
            const pathname = window.location.pathname;
            showLanguageNotice('Cambiando a Español...');
            setTimeout(() => {
                if (pathname.endsWith('.html') && !pathname.endsWith('-es.html')) {
                    window.location.href = pathname.replace(/\.html$/, '-es.html');
                } else {
                    window.location.href = 'index-es.html';
                }
            }, 600);
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


def js_safe(value):
    return value.replace('\\', '\\\\').replace("'", "\\'")

for filename in files:
    path = Path(filename)
    if not path.exists():
        print('missing', filename)
        continue
    content = path.read_text()
    data = help_data_map[filename]
    blocks = []
    for tab_id, tab in data.items():
        subs = []
        for sub_id, sub_text in tab['sub'].items():
            subs.append("                '%s': '%s'" % (js_safe(sub_id), js_safe(sub_text)))
        blocks.append("            '%s': { title: '%s', sub: {\n%s\n            } }" % (js_safe(tab_id), js_safe(tab['title']), ',\n'.join(subs)))
    help_data_js = ',\n'.join(blocks)
    final_script = common_script.replace('{help_data}', help_data_js)
    content = re.sub(r'<script>[\s\S]*?</script>', final_script, content, flags=re.S)
    path.write_text(content)
    print('updated script', filename)
