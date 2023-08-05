from textwrap import indent, dedent

from zmei_generator.contrib.channels.extensions.pages.stream import StreamPageExtension
from zmei_generator.contrib.react.extensions.page.react import ReactPageExtension
from zmei_generator.generator.imports import ImportSet
from zmei_generator.generator.utils import generate_file, format_uri


def generate(target_path, project):
    has_react = False

    react_pages = []
    index_imports = ImportSet()

    for app_name, application in project.applications.items():
        if not application.pages_support(ReactPageExtension):
            continue

        has_react = True

        for name, page in application.pages.items():
            ext = page.get_own_or_parent_extension(ReactPageExtension)
            if not ext:
                continue

            name = f'{page.name.capitalize()}'
            name_ui = f'{page.name.capitalize()}Ui'

            if page.uri:
                react_pages.append((app_name.capitalize(), name, format_uri(page.uri)))

            page_component_name = f'Page{page.name.capitalize()}'

            react_components_imports = ImportSet()
            react_components_imports.add('react', 'React')
            # react_components_imports.add(f'../Components/{el.tag}', '*' + el.tag)

            imports = ImportSet()
            imports.add('react', 'React')
            imports.add(f'./{name_ui}', name_ui)
            imports.add(f'../../layout', 'BaseLayout')
            imports.add(f'../layouts/{app_name.capitalize()}Layout', f'{app_name.capitalize()}Layout')

            react_components_imports.add(f'../Reducers/{page_component_name}Reducers',
                                         f'*reloadPageDataAction')

            index_imports.add(f'./pages/{name}', '*' + name)

            wrappers = [
                f'PageContextProvider',
                f'BaseLayout',
                f'{app_name.capitalize()}Layout'
            ]

            def wrap(source, cmp_list):
                source = indent(source, '    ')

                if not len(cmp_list):
                    return dedent(source)

                w = cmp_list.pop()

                return wrap(f'<{w} {{...this.props}} page={{this}}>\n{source}\n</{w}>', wrappers)

            streams = page.list_own_or_parent_extensions(StreamPageExtension)
            generate_file(target_path, 'react/src/{}/pages/{}.jsx'.format(app_name, name),
                          'react/page.jsx.tpl', {
                              'imports': imports.import_sting_js(),
                              'name': name,
                              'page': page,
                              'ext': ReactPageExtension,
                              'app_name': app_name,
                              'streams': streams,
                              'source': wrap(f'<{name_ui}  {{...this.props}} page={{this}}>{{this.renderContent()}}</{name_ui}>', wrappers)
                          })

            generate_file(target_path, f'react/src/{app_name}/pages/{name_ui}.jsx',
                          'react/cmp.jsx.tpl', {
                              'name': name_ui,
                              'source': f"<>{{children || 'Empty react component. Edit {name_ui}.jsx'}}</>"
                          })

        generate_file(target_path, f'react/src/{app_name}/layouts/{app_name.capitalize()}Layout.jsx',
                      'react/cmp.jsx.tpl', {
                          'name': f'{app_name.capitalize()}Layout',
                          'source': '<>{children}</>'
                      })

    if has_react:
        generate_file(target_path, f'react/src/layout.jsx',
                      'react/cmp.jsx.tpl', {
                          'name': f'BaseLayout',
                          'source': '<>{children}</>'
                      })
        generate_file(target_path, f'react/src/index.scss', 'react/index.scss.tpl', {
            'pages': react_pages
        })
        generate_file(target_path, 'app/utils/react.py', 'react/utils.py.tpl')
        generate_file(target_path, 'react/src/index.jsx', 'react/index.jsx.tpl')
        generate_file(target_path, 'react/src/state.jsx', 'react/state.js.tpl')
        generate_file(target_path, 'react/src/streams.jsx', 'react/streams.js.tpl')
        generate_file(target_path, 'react/src/reducer.jsx', 'react/reducer.js.tpl', {
            'name': 'Root'
        })
        generate_file(target_path, 'react/src/router.jsx', 'react/router.jsx.tpl', {
            'name': 'Root',
            'pages': react_pages
        })

        generate_file(target_path, 'react/package.json', 'react/package.json.tpl', {
            'packages': {}
        })
        generate_file(target_path, 'react/webpack.config.js', 'react/webpack.config.js.tpl', {
            'entries': {'all': f'./src/index.jsx'}
        })
