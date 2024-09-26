import os

import typer

app = typer.Typer(no_args_is_help=True)


ESLINT_CONF = """import globals from "globals";
import pluginJs from "@eslint/js";
import tseslint from "typescript-eslint";
import pluginVue from "eslint-plugin-vue";


export default [
  {files: ["**/*.{js,mjs,cjs,ts,vue}"]},
  {languageOptions: { globals: globals.browser }},
  pluginJs.configs.recommended,
  ...tseslint.configs.recommended,
  ...pluginVue.configs["flat/essential"],
  {files: ["**/*.vue"], languageOptions: {parserOptions: {parser: tseslint.parser}}},
];"""

TAILWIND_CONF = """/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}"""

TAILWIND_CSS = """@tailwind base;
@tailwind components;
@tailwind utilities;"""


@app.command()
def vue():
    """vue3-vite-typescript"""
    project_name = typer.prompt('请输入项目名称', prompt_suffix=': ')
    os.system(f'pnpm create vite@latest {project_name} --template vue-ts')
    os.system(f'cd {project_name} && pnpm i')
    # eslint
    os.system(
        f'cd {project_name} && pnpm i -D eslint @eslint/create-config @eslint/js eslint-plugin-vue typescript-eslint'
    )
    with open(f'{project_name}/eslint.config.js', 'w') as f:
        f.write(ESLINT_CONF)
    # os.system(f'cd {project_name} && npx eslint --init')

    # prettier
    os.system(
        f'cd {project_name} && pnpm i -D prettier eslint-config-prettier eslint-plugin-prettier'
    )
    os.system(f'touch {project_name}/.prettierrc.js')

    # tailwind css
    os.system(f'cd {project_name} && pnpm i -D tailwindcss postcss autoprefixer')
    os.system(f'cd {project_name} && npx tailwindcss init -p')
    with open(f'{project_name}/tailwind.config.js', 'w') as f:
        f.write(TAILWIND_CONF)
    with open(f'{project_name}/src/style.css', 'w') as f:
        f.write(TAILWIND_CSS)


if __name__ == '__main__':
    app()
