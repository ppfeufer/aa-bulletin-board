import globals from 'globals'; // Import the globals package
import js from '@eslint/js'; // Import the ESLint JavaScript configuration
import { defineConfig } from 'eslint/config'; // Import the defineConfig function from ESLint
import deprecate from 'eslint-plugin-deprecate'; // Import the deprecate plugin

export default defineConfig([
    {
        languageOptions: {
            globals: {
                ...globals.browser,
                ...globals.commonjs,
                ...globals.jquery,
            },
            parserOptions: {
                ...js.configs.recommended.parserOptions,
                ecmaVersion: 'latest',
                ecmaFeatures: {
                    impliedStrict: true,
                },
                sourceType: 'module',
            },
        },
        rules: {
            ...js.configs.recommended.rules,
            indent: ['error', 4],
            quotes: ['error', 'single', {
                avoidEscape: true,
                allowTemplateLiterals: true
            }],
            semi: [2, 'always'],
            'deprecate/function': 2,
            'deprecate/member-expression': 2,
            'deprecate/import': 2,
        },
        plugins: {
            deprecate
        },
    }
]);
