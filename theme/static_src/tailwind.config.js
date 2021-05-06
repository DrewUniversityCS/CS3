/**
 * This is a minimal config.
 *
 * If you need the full config, get it from here:
 * https://unpkg.com/browse/tailwindcss@latest/stubs/defaultConfig.stub.js
 */

module.exports = {
    /**
     * Stylesheet generation mode.
     *
     * Set mode to "jit" if you want to generate your styles on-demand as you author your templates;
     * Set mode to "aot" if you want to generate the stylesheet in advance and purge later (aka legacy mode).
     */
    mode: "jit",

    purge: [
        /**
         * HTML. Paths to Django template files that will contain Tailwind CSS classes.
         */
        /*  Templates within theme app (e.g. base.html) */
        '../templates/**/*.html',

        /* Templates in other apps. Adjust the following line so that it matches
         * your project structure.
         */
        '../../templates/**/*.html',

        /**
         * JS: If you use Tailwind CSS in JavaScript, uncomment the following lines and make sure
         * patterns match your project structure.
         */
        /* JS 1: Ignore any JavaScript in node_modules folder. */
        // '!../../**/node_modules',
        /* JS 2: Process all JavaScript files in the project. */
        // '../../**/*.js',

        /**
         * Python: If you use Tailwind CSS classes in Python, uncomment the following line
         * and make sure the pattern below matches your project structure.
         */
        // '../../**/*.py'
    ],
    darkMode: false, // or 'media' or 'class'
    theme: {
        extend: {
            backgroundImage: theme => ({
                'no-data': "url('/static/images/signal_heropattern.svg')",
                'endlessclouds': "url('/static/images/endless-clouds_heropattern.svg')",
                'foundation': "url('/static/images/aztec_heropattern.svg')",
                'arrows': "url('/static/images/charlie-brown_heropattern.svg')"
            }),
            animation: {
                'spin-1': 'spin 3s linear infinite',
                'spin-2': 'spin 4s linear infinite',
                'spin-3': 'spin 5s linear infinite',
            },
            colors: {
                teal: {
                    darkest: '#006657',
                    dark: '#00a38b',
                    DEFAULT: '#00c4a8',
                    light: '#00E0BF',
                    lightest: '#0AFFDA',
                }
            }
        },
    },
    variants: {
        extend: {},
    },
    plugins: [
        /**
         * '@tailwindcss/forms' is the forms plugin that provides a minimal styling
         * for forms. If you don't like it or have own styling for forms,
         * comment the line below to disable '@tailwindcss/forms'.
         */
        require('@tailwindcss/forms'),
        require('@tailwindcss/typography'),
        require('@tailwindcss/line-clamp'),
        require('@tailwindcss/aspect-ratio'),
    ],
}
